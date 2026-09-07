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
    return {"logical_digest":logical_index_digest((r["table_id"],r["logical_checksum"]) for r in rows),"execution_order_id":full.EXECUTION_ORDER_ID,"full_table_id_digest":full._ids_digest(["a","b","c"]),"shards":{"0":{"expected_table_count":2,"expected_ordered_table_id_digest":full._ids_digest(["a","b"])},"1":{"expected_table_count":1,"expected_ordered_table_id_digest":full._ids_digest(["c"])}}}

def _tiny_corpus(ids,normalized_root="normalized"):
    return {"normalized_root":str(normalized_root),"count":len(ids),"logical_digest":full.EXPECTED_CORPUS_DIGEST,"partition_count":len(ids),"execution_order_id":full.EXECUTION_ORDER_ID,"full_table_id_digest":full._ids_digest(ids),"shards":{str(shard):{"expected_table_count":1,"expected_ordered_table_id_digest":full._ids_digest([table_id])} for shard,table_id in enumerate(ids)}}

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
    assert result["shards"]=={"0":{"expected_table_count":2,"expected_ordered_table_id_digest":full._ids_digest(["a","b"])},"1":{"expected_table_count":1,"expected_ordered_table_id_digest":full._ids_digest(["c"])}}
    shuffled=full.inspect_corpus_identity(tmp_path,index_reader=lambda _:list(reversed(rows)),normalized_root=root,expected_count=3,expected_digest=digest,partition_count=2)
    assert shuffled["shards"]==result["shards"]
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
    corpus=_tiny_corpus(ids,tmp_path/"normalized")
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

@pytest.mark.parametrize("ids",[[],["t000","extra"],["wrong"],["t000","t000"]],ids=["missing","extra","wrong-id","duplicate"])
def test_physical_source_shard_identity_mismatch_precedes_encoding(tmp_path,monkeypatch,ids):
    model_name="Qwen3-Embedding-0.6B"; record=full.load_embedding_registry().models[model_name].record; expected=[f"t{shard:03d}" for shard in range(256)]; corpus=_tiny_corpus(expected,tmp_path/"normalized")
    preflight=lambda *_:{"storage":{"passed":True},"corpus":corpus,"serialization":{"id":"neural_table_evidence_v1","version":"1.1.0","hash":full.EXPECTED_SERIALIZATION_HASH}}
    class Model:
        calls=0
        tokenizer=lambda self,batch,**_:{"input_ids":[[1] for _ in batch]}
        def encode(self,*_,**__):self.calls+=1; raise AssertionError("encoder must not be called")
    model=Model(); monkeypatch.setattr(full,"_load_runtime_model",lambda *_:(model,record,_FakeTorch,0.0,{}))
    records=[{**_normalized_record(),"table_id":table_id} for table_id in ids]
    with pytest.raises(RuntimeError,match='"code": "physical_source_shard_identity_mismatch"') as error:
        full.full_encode(model_name,tmp_path,tmp_path/"artifacts",confirm_full_corpus=True,preflight_fn=preflight,shard_reader=lambda _,shard:records if shard==0 else [])
    payload=json.loads(str(error.value)); assert payload["source_shard"]==0 and payload["expected_table_count"]==1 and payload["actual_table_count"]==len(ids)
    assert model.calls==0

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

def test_resume_rejects_population_different_from_verified_index(tmp_path):
    root=tmp_path/"shard-000"; full.promote_complete_shard(root,["a"],np.array([[1,0]],np.float32),_identity(),.1,.2)
    expected={**_identity(),"table_count":1,"ordered_table_id_digest":full._ids_digest(["different"])}
    with pytest.raises(ValueError,match="identity"):full.validate_complete_shard(root,expected)

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

def _write_validated_full_index(tmp_path,monkeypatch):
    model_name=full.MODEL_ORDER[0]; ids=[f"t{shard:03d}" for shard in range(256)]; corpus=_tiny_corpus(ids)
    model_root=tmp_path/model_name; model_root.mkdir(parents=True)
    identity={"corpus":corpus}; (model_root/"identity.json").write_text(json.dumps(identity))
    seconds=0.0; physical_bytes=0
    for shard,table_id in enumerate(ids):
        expected=full._expected_shard_identity(model_name,shard,corpus,4)
        manifest=full.promote_complete_shard(model_root/"shards"/f"shard-{shard:03d}",[table_id],np.pad(np.array([[1]],np.float32),((0,0),(0,1023))),expected,shard/1000,.1)
        seconds+=manifest["embedding_inference_seconds"]
        physical_bytes+=(model_root/"shards"/f"shard-{shard:03d}"/"vectors.npy").stat().st_size+(model_root/"shards"/f"shard-{shard:03d}"/"table_ids.txt").stat().st_size
    report={"status":"complete","model":model_name,"embedding_wall_seconds":seconds,"physical_index_bytes":physical_bytes}
    report_path=model_root/"full-encode-report.json"; report_path.write_text(json.dumps(report))
    monkeypatch.setattr(full,"EXPECTED_TABLE_COUNT",256)
    return model_name,report_path,seconds,physical_bytes

def test_full_index_recomputes_and_cross_checks_tie_break_values(tmp_path,monkeypatch):
    model_name,report_path,seconds,physical_bytes=_write_validated_full_index(tmp_path,monkeypatch)
    validated=full.validate_full_index(model_name,tmp_path)
    assert validated["validated_embedding_wall_seconds"]==seconds
    assert validated["validated_physical_index_bytes"]==physical_bytes
    report=json.loads(report_path.read_text()); report["embedding_wall_seconds"]+=.001; report_path.write_text(json.dumps(report))
    with pytest.raises(ValueError,match="embedding wall time"):full.validate_full_index(model_name,tmp_path)
    report["embedding_wall_seconds"]=seconds; report["physical_index_bytes"]+=1; report_path.write_text(json.dumps(report))
    with pytest.raises(ValueError,match="physical index bytes"):full.validate_full_index(model_name,tmp_path)

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

def _development_sources():
    query_ids=full.load_bakeoff_contract()["split"]["development_ids"]
    return {"queries":{query_id:f"query {query_id}" for query_id in query_ids},"qrels":{query_id:{f"t{query_id}-000":2} for query_id in query_ids},"query_sha256":"a"*64,"qrels_sha256":"b"*64,"canonical_qrel_judgments":3120,"holdout_qrels_materialized":False,"holdout":"locked_not_evaluated"}

def _write_development_artifacts(root,model,recall_marker=0):
    contract=full.load_bakeoff_contract(); query_ids=contract["split"]["development_ids"]; sources=_development_sources()
    model_root=root/model; model_root.mkdir(parents=True,exist_ok=True)
    identity={"model_name":model,"dimension":2,"corpus":{"logical_digest":full.EXPECTED_CORPUS_DIGEST,"execution_order_id":full.EXECUTION_ORDER_ID,"full_table_id_digest":"c"*64},"serialization":{"id":"neural_table_evidence_v1","version":"1.1.0","hash":full.EXPECTED_SERIALIZATION_HASH}}
    np.save(model_root/"development-query-vectors.npy",np.tile(np.array([[1,0]],dtype=np.float32),(30,1)),allow_pickle=False)
    rows=[]
    for query_id in query_ids:
        ids=[f"t{query_id}-{rank:03d}" for rank in range(100)]
        if recall_marker:ids[0]=f"irrelevant-{query_id}"
        rows.append([{"rank":rank+1,"table_id":table_id,"score":float(100-rank)} for rank,table_id in enumerate(ids)])
    ranking={"classification":"m7b_exact_development_rankings","schema_version":full.RANKING_SCHEMA_VERSION,"paper_result":False,"model":model,"split_version":contract["split"]["version"],"query_ids":query_ids,"query_sha256":sources["query_sha256"],"qrels_sha256":sources["qrels_sha256"],"canonical_qrel_judgments":sources["canonical_qrel_judgments"],"model_identity":identity,"corpus_logical_digest":identity["corpus"]["logical_digest"],"execution_order_id":identity["corpus"]["execution_order_id"],"full_table_id_digest":identity["corpus"]["full_table_id_digest"],"serialization_identity":identity["serialization"],"holdout":"locked_not_evaluated","holdout_qrels_materialized":False,"query_vector_dtype":"float32","query_vector_sha256":full._sha(model_root/"development-query-vectors.npy"),"model_load_seconds":1.0,"query_embedding_seconds":1.0,"rankings":rows,"searched_table_count":full.EXPECTED_TABLE_COUNT,"exact_search_seconds":1.0,"backend":"sharded_torch_matmul","compute_dtype":"float32","allow_tf32":False,"tie_policy":"score_descending_then_table_id_ascending"}
    ranking_path=model_root/"exact-development-rankings.json"; ranking_path.write_text(json.dumps(ranking,sort_keys=True,indent=2)+"\n")
    ranked={query_id:[item["table_id"] for item in rows[index]] for index,query_id in enumerate(query_ids)}
    evaluation=full.evaluate_development_rankings(ranked,sources["qrels"],query_ids,contract)
    evaluation=full._evaluation_artifact(model,evaluation,full._sha(ranking_path),sources,query_ids,contract)
    (model_root/"development-evaluation.json").write_text(json.dumps(evaluation,sort_keys=True,indent=2)+"\n")
    (model_root/"full-encode-report.json").write_text(json.dumps({"status":"complete"}))
    validated={"model_root":model_root,"identity":identity,"validated_embedding_wall_seconds":1+recall_marker,"validated_physical_index_bytes":10+recall_marker}
    return validated,sources

def test_provisional_selection_blocks_until_all_three(tmp_path):
    sources=_development_sources(); loader=lambda *_:sources; validator=lambda *_:{}
    assert full.provisional_select(tmp_path,tmp_path,validator,loader)["status"]=="blocked"
    for model in full.MODEL_ORDER[:2]:
        _write_development_artifacts(tmp_path,model)
    validated={model:_write_development_artifacts(tmp_path,model)[0] for model in full.MODEL_ORDER[:2]}
    result=full.provisional_select(tmp_path,tmp_path,lambda model,_:validated[model],loader)
    assert result["status"]=="blocked" and full.MODEL_ORDER[2] in result["missing_or_failed_models"]

def test_provisional_selection_reuses_frozen_selection_and_depth(tmp_path,monkeypatch):
    validated={}
    for index,model in enumerate(full.MODEL_ORDER):validated[model]=_write_development_artifacts(tmp_path,model,index)[0]
    calls=[]
    monkeypatch.setattr(full,"select_encoder",lambda results,eligible:(calls.append((results,eligible)) or {"status":"selected","winner":full.MODEL_ORDER[0],"rule":"test"}))
    monkeypatch.setattr(full,"select_candidate_depth",lambda curve:(calls.append(curve) or 20))
    for index,model in enumerate(full.MODEL_ORDER):validated[model].update({"validated_embedding_wall_seconds":100+index,"validated_physical_index_bytes":1000+index})
    result=full.provisional_select(tmp_path,tmp_path,lambda model,_:validated[model],lambda *_:_development_sources())
    assert result["status"]=="complete" and result["provisional_k"]==20 and len(calls)==2
    assert result["encoder_frozen"] is result["candidate_depth_frozen"] is False
    selection_rows=calls[0][0]
    assert [(row["embedding_wall_seconds"],row["physical_index_bytes"]) for row in selection_rows]==[(100,1000),(101,1001),(102,1002)]

def test_provisional_selection_rejects_query_vector_tampering(tmp_path):
    validated={}; sources=_development_sources()
    for model in full.MODEL_ORDER:validated[model]=_write_development_artifacts(tmp_path,model)[0]
    model=full.MODEL_ORDER[0]
    np.save(tmp_path/model/"development-query-vectors.npy",np.tile(np.array([[0,1]],dtype=np.float32),(30,1)),allow_pickle=False)
    result=full.provisional_select(tmp_path,tmp_path,lambda name,_:validated[name],lambda *_:sources)
    assert result["status"]=="blocked" and model in result["missing_or_failed_models"]

def test_provisional_selection_blocks_when_pinned_sources_are_unavailable(tmp_path):
    result=full.provisional_select(tmp_path,tmp_path,lambda *_:None,lambda *_:(_ for _ in ()).throw(ValueError("source hash mismatch")))
    assert result["status"]=="blocked" and result["winner"] is None and result["missing_or_failed_models"]==list(full.MODEL_ORDER)

@pytest.mark.parametrize("mutation",[
    "query_id","holdout_query_id","model","model_identity","query_sha","qrel_sha","rank","duplicate","score_order","tie_order","nonfinite","table_count","backend","tf32","evaluation_ranking_sha","evaluation_metric","evaluation_split","missing_metric","per_topic_id",
])
def test_provisional_selection_rejects_independent_artifact_tampering(tmp_path,mutation):
    validated={}; sources=_development_sources()
    for model in full.MODEL_ORDER:validated[model]=_write_development_artifacts(tmp_path,model)[0]
    model=full.MODEL_ORDER[0]; root=tmp_path/model; ranking_path=root/"exact-development-rankings.json"; evaluation_path=root/"development-evaluation.json"
    target=evaluation_path if mutation.startswith("evaluation_") or mutation in {"missing_metric","per_topic_id"} else ranking_path
    payload=json.loads(target.read_text())
    if mutation=="query_id":payload["query_ids"][0]=999
    elif mutation=="holdout_query_id":payload["query_ids"][0]=full.load_bakeoff_contract()["split"]["holdout_ids"][0]
    elif mutation=="model":payload["model"]="wrong-model"
    elif mutation=="model_identity":payload["model_identity"]["dimension"]=3
    elif mutation=="query_sha":payload["query_sha256"]="0"*64
    elif mutation=="qrel_sha":payload["qrels_sha256"]="0"*64
    elif mutation=="rank":payload["rankings"][0][0]["rank"]=2
    elif mutation=="duplicate":payload["rankings"][0][1]["table_id"]=payload["rankings"][0][0]["table_id"]
    elif mutation=="score_order":payload["rankings"][0][1]["score"]=1000
    elif mutation=="tie_order":payload["rankings"][0][0].update({"table_id":"z","score":99}); payload["rankings"][0][1].update({"table_id":"a","score":99})
    elif mutation=="nonfinite":payload["rankings"][0][0]["score"]=float("nan")
    elif mutation=="table_count":payload["searched_table_count"]-=1
    elif mutation=="backend":payload["backend"]="ann"
    elif mutation=="tf32":payload["allow_tf32"]=True
    elif mutation=="evaluation_ranking_sha":payload["exact_ranking_sha256"]="0"*64
    elif mutation=="evaluation_metric":payload["metrics"]["bpref"]["all"]=0.123
    elif mutation=="evaluation_split":payload["split_version"]="wrong"
    elif mutation=="missing_metric":del payload["metrics"]["mrr_at_10"]
    elif mutation=="per_topic_id":payload["per_topic"]["999"]=payload["per_topic"].pop(next(iter(payload["per_topic"])))
    target.write_text(json.dumps(payload))
    result=full.provisional_select(tmp_path,tmp_path,lambda name,_:validated[name],lambda *_:sources)
    assert result["status"]=="blocked" and result["winner"] is None and model in result["missing_or_failed_models"]

def test_harness_reuses_existing_evaluator_and_has_no_external_or_qdrant_path():
    from intention.evaluation.topical_bakeoff import evaluate_development_rankings
    assert full.evaluate_development_rankings is evaluate_development_rankings
    source=Path(full.__file__).read_text()
    assert "qdrant" not in source.lower() and "gemini" not in source.lower() and "voyage" not in source.lower()
