from hashlib import sha256
from pathlib import Path
import json

import numpy as np
import pytest

import intention.evaluation.m7b_full as full
from intention.architecture.serialization import NeuralTableSerializer
from intention.benchmarks.corpus import logical_index_digest,runtime_table_from_normalized_record
from intention.contracts import Table

class _FakeTensor:
    def __init__(self,value):self.value=np.asarray(value,dtype=np.float32)
    @property
    def T(self):return _FakeTensor(self.value.T)
    def __matmul__(self,other):return _FakeTensor(self.value@other.value)
    def detach(self):return self
    def cpu(self):return self
    def numpy(self):return self.value

class _Context:
    def __enter__(self):return self
    def __exit__(self,*_):return False

class _Flags:
    allow_tf32=True

class _FakeTorch:
    float32=np.float32
    cuda=type("Cuda",(),{"empty_cache":lambda _:None})()
    backends=type("Backends",(),{"cuda":type("CudaBackend",(),{"matmul":_Flags()})(),"cudnn":_Flags()})()
    @staticmethod
    def as_tensor(value,**_):return _FakeTensor(value)
    @staticmethod
    def inference_mode():return _Context()

def _unit_rows():
    return [
        {"table_id":"b","shard":0,"logical_checksum":"b"*64},
        {"table_id":"a","shard":0,"logical_checksum":"a"*64},
        {"table_id":"c","shard":1,"logical_checksum":"c"*64},
    ]

def _corpus():
    rows=_unit_rows()
    return {"logical_digest":logical_index_digest((r["table_id"],r["logical_checksum"]) for r in rows),"execution_order_id":full.EXECUTION_ORDER_ID,"full_table_id_digest":full._ids_digest(["a","b","c"])}

def _identity(dimension=2):
    return {"execution_id":"m7b-full-corpus-v1","corpus_digest":"d"*64,"execution_order_id":full.EXECUTION_ORDER_ID,"full_table_id_digest":"e"*64,"source_shard":0,"model":"fake/model","model_revision":"a"*40,"tokenizer_revision":"a"*40,"dimension":dimension,"dtype":"float32","serialization_id":"neural_table_evidence_v1","serialization_version":"1.1.0","serialization_hash":full.EXPECTED_SERIALIZATION_HASH,"selected_batch_size":4}

def _normalized_record(title="ordinary requirements table"):
    return {"table_id":"t","source":{"dataset_id":"wikitables_www2018"},"context":{"page_title":title,"section_title":None,"table_caption":"caption"},"columns":[{"column_id":"c0000","ordinal":0,"header_text":"Requirements"}],"rows":[["natural text"]],"normalization":{"version":"1.0.0","flags":[],"logical_checksum":"f"*64}}

def test_operational_contract_is_exact_and_not_scientific_threshold():
    contract=full.load_full_execution_contract()
    assert contract["version"]=="1.0.0" and contract["partition_count"]==256
    assert contract["batch_sizes"]=={"Qwen3-Embedding-0.6B":64,"Nemotron-3-Embed-1B-BF16":128,"Qwen3-Embedding-4B":32}
    assert not any("effectiveness" in key or "recall" in key for key in contract)

def test_full_contract_compatible_with_frozen_m7b_contract():
    operational=full.load_full_execution_contract(); scientific=full.load_bakeoff_contract()
    assert operational["top_k"]==scientific["quality_search"]["metric_depth"]==100
    assert operational["maximum_exact_search_seconds_per_model"]==scientific["quality_search"]["maximum_seconds_per_model"]==7200
    assert set(operational["batch_sizes"])=={name for name,row in scientific["models"].items() if row["eligible"]}

def test_index_preflight_reuses_m7a_digest_and_shard_order(tmp_path):
    root=tmp_path/"normalized"; (root/"index").mkdir(parents=True); (root/"index/x.parquet").touch()
    rows=_unit_rows(); digest=logical_index_digest((r["table_id"],r["logical_checksum"]) for r in rows)
    result=full.inspect_corpus_identity(tmp_path,index_reader=lambda _:rows,normalized_root=root,expected_count=3,expected_digest=digest,partition_count=2)
    assert result["count"]==3 and result["logical_digest"]==digest
    assert result["full_table_id_digest"]==full._ids_digest(["a","b","c"])
    with pytest.raises(ValueError,match="duplicate"):full.inspect_corpus_identity(tmp_path,index_reader=lambda _:[rows[0],rows[0],rows[2]],normalized_root=root,expected_count=3,expected_digest=digest,partition_count=2)

def test_index_preflight_requires_checksums_and_all_declared_shards(tmp_path):
    root=tmp_path/"normalized"; (root/"index").mkdir(parents=True); (root/"index/x.parquet").touch(); rows=_unit_rows()
    with pytest.raises(ValueError,match="logical checksum"):full.inspect_corpus_identity(tmp_path,index_reader=lambda _:[{**r,"logical_checksum":None} for r in rows],normalized_root=root,expected_count=3,expected_digest="x",partition_count=2)
    with pytest.raises(ValueError,match="256 shards"):full.inspect_corpus_identity(tmp_path,index_reader=lambda _:[{**r,"shard":0} for r in rows],normalized_root=root,expected_count=3,expected_digest="x",partition_count=2)

def test_canonical_adapter_serializer_and_natural_requirements_text():
    record=_normalized_record(); table=runtime_table_from_normalized_record(record); serialized=NeuralTableSerializer().serialize(table).text
    assert "Requirements" in serialized and "ordinary requirements table" in serialized
    assert table.metadata["columns"][0]["header_text"]=="Requirements"

def test_structural_forbidden_metadata_is_rejected_before_serialization(monkeypatch,tmp_path):
    record={**_normalized_record(),"requirements":["forbidden object"]}; called=[]
    class Serializer:
        def serialize(self,table):called.append(table)
    with pytest.raises(ValueError,match="structurally forbidden"):full.serialize_normalized_records([record],Serializer())
    assert called==[]

def test_confirmation_gate_precedes_preflight_and_model_loading(tmp_path):
    touched=[]
    with pytest.raises(PermissionError,match="confirm-full-corpus"):full.full_encode("Qwen3-Embedding-0.6B",tmp_path,tmp_path,confirm_full_corpus=False,preflight_fn=lambda *_:touched.append(True))
    assert touched==[]

def test_full_encode_orchestration_and_resume_use_tiny_mock_shards(tmp_path,monkeypatch):
    model_name="Qwen3-Embedding-0.6B"; registry=full.load_embedding_registry(); record=registry.models[model_name].record; ids=[f"t{shard:03d}" for shard in range(256)]
    corpus={"normalized_root":str(tmp_path/"normalized"),"count":256,"logical_digest":full.EXPECTED_CORPUS_DIGEST,"partition_count":256,"execution_order_id":full.EXECUTION_ORDER_ID,"full_table_id_digest":full._ids_digest(ids)}
    preflight=lambda *_:{"storage":{"passed":True},"corpus":corpus,"serialization":{"id":"neural_table_evidence_v1","version":"1.1.0","hash":full.EXPECTED_SERIALIZATION_HASH}}
    class Model:
        tokenizer=lambda self,batch,**_:{"input_ids":[[1] for _ in batch]}
        calls=0
        def encode(self,batch,**_):
            self.calls+=len(batch); result=np.zeros((len(batch),1024),np.float32); result[:,0]=1; return result
    model=Model()
    monkeypatch.setattr(full,"_load_runtime_model",lambda *_:(model,record,_FakeTorch,0.0,{"expected":"lasttoken","observed":{"lasttoken":True}}))
    def reader(_,shard):
        item={**_normalized_record(),"table_id":ids[shard]}; return [item]
    first=full.full_encode(model_name,tmp_path,tmp_path/"artifacts",confirm_full_corpus=True,preflight_fn=preflight,shard_reader=reader)
    assert first["status"]=="complete" and first["raw_vector_payload_bytes"]==256*1024*4 and first["external_api_spend_usd"]==0
    assert first["embedding_wall_seconds"]>=0 and model.calls==256 and first["physical_index_bytes"]>first["raw_vector_payload_bytes"]
    identity=json.loads((tmp_path/"artifacts"/model_name/"identity.json").read_text()); assert identity["quantization"] is False and identity["persisted_dtype"]=="float32"
    second=full.full_encode(model_name,tmp_path,tmp_path/"artifacts",confirm_full_corpus=True,preflight_fn=preflight,shard_reader=lambda *_:(_ for _ in ()).throw(AssertionError("resume must skip")))
    assert second["status"]=="complete" and model.calls==256

def test_float32_atomic_shard_and_exact_resume(tmp_path):
    vectors=np.array([[1,0],[0,1]],dtype=np.float32); identity=_identity(); root=tmp_path/"shard-000"
    first=full.promote_complete_shard(root,["a","b"],vectors,identity,.2,.3); second=full.promote_complete_shard(root,["a","b"],vectors,identity,.2,.3)
    assert first==second and np.load(root/"vectors.npy").dtype==np.float32
    assert not root.with_name(".shard-000.tmp").exists()

def test_resume_rejects_checksum_model_and_serialization_mismatch(tmp_path):
    root=tmp_path/"shard-000"; full.promote_complete_shard(root,["a"],np.array([[1,0]],np.float32),_identity(),.1,.2)
    (root/"table_ids.txt").write_text("z\n")
    with pytest.raises(ValueError,match="checksum"):full.validate_complete_shard(root,_identity())
    root=tmp_path/"other"; full.promote_complete_shard(root,["a"],np.array([[1,0]],np.float32),_identity(),.1,.2)
    with pytest.raises(ValueError,match="identity"):full.validate_complete_shard(root,{**_identity(),"model_revision":"b"*40})
    with pytest.raises(ValueError,match="identity"):full.validate_complete_shard(root,{**_identity(),"serialization_hash":"c"*64})

@pytest.mark.parametrize("bad",[
    np.array([[1,0]],dtype=np.float64),
    np.array([[np.nan,0]],dtype=np.float32),
    np.array([[0,0]],dtype=np.float32),
    np.array([[2,0]],dtype=np.float32),
    np.array([[1,0,0]],dtype=np.float32),
])
def test_vector_contract_rejects_wrong_dtype_dimension_finite_nonzero_or_l2(bad):
    with pytest.raises(ValueError):full._vector_checks(bad,2)

def test_oom_halves_and_retries_same_records():
    calls=[]
    def encode(batch,size):
        calls.append((list(batch),size))
        if size==4:raise RuntimeError("CUDA out of memory")
        return np.array([[1,0] for _ in batch],np.float32)
    vectors,batch,events,_=full.encode_with_oom_retry(["a","b","c","d"],encode,4,cuda=type("C",(),{"empty_cache":lambda _:None})())
    assert calls[:2]==[(["a","b","c","d"],4),(["a","b"],2)] and batch==2 and len(vectors)==4
    assert events==[{"record_offset":0,"failed_batch_size":4,"new_batch_size":2,"same_records_retried":True}]

def test_batch_one_oom_is_structured_failure():
    with pytest.raises(RuntimeError,match="cuda_oom_at_minimum_batch"):full.encode_with_oom_retry(["a"],lambda *_:(_ for _ in ()).throw(RuntimeError("out of memory")),1)

def test_exact_search_matches_bruteforce_all_shards_and_ties():
    queries=np.array([[1,0],[0,1]],np.float32)
    shards=[(["b","a"],np.array([[1,0],[1,0]],np.float32)),(["c","d"],np.array([[0,1],[-1,0]],np.float32))]
    result=full.exact_search_shards(queries,shards,top_k=3,torch_module=_FakeTorch)
    assert result["searched_table_count"]==4 and [r["table_id"] for r in result["rankings"][0]]==["a","b","c"]
    all_vectors=np.concatenate([shards[0][1],shards[1][1]]); all_ids=shards[0][0]+shards[1][0]
    brute=sorted(zip(all_ids,queries[1]@all_vectors.T),key=lambda x:(-x[1],x[0]))[:3]
    assert [r["table_id"] for r in result["rankings"][1]]==[x[0] for x in brute]
    assert result["allow_tf32"] is False and result["tie_policy"]=="score_descending_then_table_id_ascending"

def test_exact_top_100_is_unique_and_timeout_fails_closed(monkeypatch):
    ids=[f"t{i:03d}" for i in range(120)]; vectors=np.tile(np.array([[1,0]],np.float32),(120,1))
    result=full.exact_search_shards(np.array([[1,0]],np.float32),[(ids,vectors)],top_k=100,torch_module=_FakeTorch)
    assert len(result["rankings"][0])==len({r["table_id"] for r in result["rankings"][0]})==100
    ticks=iter([0,2,2]); monkeypatch.setattr(full,"perf_counter",lambda:next(ticks))
    with pytest.raises(TimeoutError):full.exact_search_shards(np.array([[1,0]],np.float32),[(["a"],np.array([[1,0]],np.float32))],top_k=1,maximum_seconds=1,torch_module=_FakeTorch)

def test_source_hash_and_development_only_materialization(tmp_path,monkeypatch):
    source=tmp_path/"source"; (source/"data").mkdir(parents=True); queries=source/"data/queries.txt"; qrels=source/"data/qrels.txt"
    queries.write_text("1 development query\n2 secret holdout query\n"); qrels.write_text("1 0 table-dev 2\n2 this holdout-content-is-never-materialized\n")
    query_digest=sha256(queries.read_bytes()).hexdigest(); qrel_digest=sha256(qrels.read_bytes()).hexdigest()
    monkeypatch.setattr(full,"load_source_contract",lambda:{"resources":{"queries":{"path":"data/queries.txt","sha256":query_digest},"qrels":{"path":"data/qrels.txt","sha256":qrel_digest}}})
    contract={"split":{"development_ids":[1],"holdout_ids":[2]},"qrels":{"judgment_count":2}}
    loaded=full.load_development_sources(source,contract)
    assert loaded["queries"]=={1:"development query"} and loaded["qrels"]=={1:{"table-dev":2}}
    assert loaded["holdout_qrels_materialized"] is False
    queries.write_text("changed\n")
    with pytest.raises(ValueError,match="SHA-256"):full.load_development_sources(source,contract)

def _evaluation(recall=.8,bpref=.7):
    metrics={f"known_relevant_recall_at_{k}":{"all":recall if k==100 else recall*.99} for k in (5,10,20,50,100)}; metrics["bpref"]={"all":bpref}
    return {"classification":"development_topical_retrieval","topic_count":30,"metrics":metrics}

def _ranking():
    return {"classification":"m7b_exact_development_rankings","searched_table_count":full.EXPECTED_TABLE_COUNT,"holdout_qrels_materialized":False,"query_ids":list(range(30)),"rankings":[[{"table_id":f"t{query}-{rank}"} for rank in range(100)] for query in range(30)]}

def test_provisional_selection_blocks_until_all_three(tmp_path):
    validator=lambda *_:{}
    assert full.provisional_select(tmp_path,validator)["status"]=="blocked"
    for model in full.MODEL_ORDER[:2]:
        root=tmp_path/model; root.mkdir(); (root/"full-encode-report.json").write_text(json.dumps({"status":"complete","embedding_wall_seconds":1,"physical_index_bytes":10})); (root/"exact-development-rankings.json").write_text(json.dumps(_ranking())); (root/"development-evaluation.json").write_text(json.dumps(_evaluation()))
    assert full.provisional_select(tmp_path,validator)["status"]=="blocked" and full.MODEL_ORDER[2] in full.provisional_select(tmp_path,validator)["missing_or_failed_models"]

def test_provisional_selection_reuses_frozen_selection_and_depth(tmp_path,monkeypatch):
    for index,model in enumerate(full.MODEL_ORDER):
        root=tmp_path/model; root.mkdir(); (root/"full-encode-report.json").write_text(json.dumps({"status":"complete","embedding_wall_seconds":index+1,"physical_index_bytes":10+index})); (root/"exact-development-rankings.json").write_text(json.dumps(_ranking())); (root/"development-evaluation.json").write_text(json.dumps(_evaluation(.8-index*.02,.7)))
    calls=[]
    monkeypatch.setattr(full,"select_encoder",lambda results,eligible:(calls.append((results,eligible)) or {"status":"selected","winner":full.MODEL_ORDER[0],"rule":"test"}))
    monkeypatch.setattr(full,"select_candidate_depth",lambda curve:(calls.append(curve) or 20))
    result=full.provisional_select(tmp_path,lambda *_:{})
    assert result["status"]=="complete" and result["provisional_k"]==20 and len(calls)==2
    assert result["encoder_frozen"] is result["candidate_depth_frozen"] is False

def test_harness_reuses_existing_evaluator_and_has_no_external_or_qdrant_path():
    from intention.evaluation.topical_bakeoff import evaluate_development_rankings
    assert full.evaluate_development_rankings is evaluate_development_rankings
    source=Path(full.__file__).read_text()
    assert "qdrant" not in source.lower() and "gemini" not in source.lower() and "voyage" not in source.lower()
