from dataclasses import asdict
from pathlib import Path
import pytest,yaml
from intention.__main__ import fixture
from intention.baselines.registry import baseline
from intention.contracts import Table
from intention.pipeline import run
from intention.retrieval import (
    BM25Retriever,RetrievalCandidate,Retriever,RetrieverIdentity,
    RetrievalRequest,RetrievalResult,RetrievalTiming,TableSerializer,
    load_retrieval_policy,load_retriever_registry,retrieval_result_dict,
)

ROOT=Path(__file__).parents[1]

def test_candidate_depth_and_serialization_contract_are_frozen():
    policy=load_retrieval_policy()
    assert (policy.primary_k,policy.development_k,policy.sensitivity_k)==(20,(5,10,20,50),(5,10,20,50,100))
    contract=policy.serializations["title_description_schema_v1"]
    assert contract.version=="1.0.0"
    assert contract.visible_components==("title","description","column_names")
    assert {"rows","cell_values","metadata","capability_profiles","grounded_action","action_arguments","full_user_input"}<=set(contract.excluded_components)

def test_table_serializer_exposes_only_declared_components():
    table=Table("secret","Visible title","Visible description",({"column_a":"SECRET_CELL","column_b":7},),{"secret":"SECRET_METADATA"})
    serializer=TableSerializer(load_retrieval_policy().serializations["title_description_schema_v1"])
    output=serializer.serialize(table)
    assert output.text=="Visible title Visible description column_a column_b"
    assert "SECRET_CELL" not in output.text and "SECRET_METADATA" not in output.text
    assert output.serialization_id=="title_description_schema_v1" and len(output.checksum)==64

def test_bm25_implements_common_result_schema_with_identity_rank_and_timing():
    ticks=iter((0,.001,.003)); result=BM25Retriever(clock=lambda:next(ticks),clock_name="test_clock").retrieve(RetrievalRequest("vaccine side effects",2),fixture())
    assert result.status=="success" and result.failure is None
    assert asdict(result.identity)=={"name":"BM25","revision":"1.0.0","serialization_id":"title_description_schema_v1","input_scope":"topical_only"}
    assert result.timing==RetrievalTiming(1,2,3,"test_clock")
    assert [candidate.rank for candidate in result.candidates]==[1,2]
    assert all(0<=candidate.relevance<=1 for candidate in result.candidates)
    assert retrieval_result_dict(result)["identity"]["serialization_id"]=="title_description_schema_v1"

def test_bm25_fails_explicitly_on_full_input_scope():
    result=BM25Retriever(clock=lambda:0).retrieve(RetrievalRequest("topic compare measure=x",2,"full_input_baseline"),fixture())
    assert result.status=="failure" and result.failure.code=="invalid_request" and not result.candidates

class RecordingRetriever(Retriever):
    def __init__(self): self.requests=[]
    @property
    def identity(self): return RetrieverIdentity("recording","1","title_description_schema_v1","topical_only")
    def retrieve(self,request,tables):
        self.requests.append(request)
        return RetrievalResult("success",self.identity,RetrievalTiming(0,0,0,"test"),(RetrievalCandidate(tables[0].table_id,1,1),))

def test_pipeline_passes_only_topical_query_to_first_stage_retriever():
    retriever=RecordingRetriever(); text="vaccine side effects compare measure=rate, comparison dimension=country"
    result=run(text,fixture(),retriever=retriever)
    assert retriever.requests==[RetrievalRequest("vaccine side effects",20,"topical_only")]
    assert text not in [request.query for request in retriever.requests]
    assert result["retrieval"].identity.name=="recording"

def test_registry_names_full_input_baseline_and_fails_closed():
    registry=load_retriever_registry()
    assert registry.latency_fields==("serialization_ms","inference_ms","total_ms")
    assert registry.retrievers["TABERTA-Hybrid"].input_scope=="topical_only"
    assert registry.retrievers["TABERTA-FullInput"].input_scope=="full_input_baseline"
    for name,record in registry.retrievers.items():
        if record.kind=="external":
            assert record.availability=="blocked" and record.failure_reason
    with pytest.raises(RuntimeError,match="no approximation substituted"): baseline("TABERTA-Hybrid")

def test_registry_rejects_external_adapter_marked_available_without_exact_identity(tmp_path):
    raw=yaml.safe_load((ROOT/"configs/baselines/registry.yaml").read_text())
    item=raw["retrievers"]["TABERTA-Hybrid"]
    item.update({"availability":"available","failure_reason":None,"implementation":"adapter","model":"taberta","revision":"exact-revision","hardware":["gpu"],"dependencies":["package==1"]})
    path=tmp_path/"registry.yaml"; path.write_text(yaml.safe_dump(raw))
    with pytest.raises(ValueError,match="incomplete available external"): load_retriever_registry(path)

def test_candidate_schema_rejects_unnormalized_relevance_and_bad_ranks():
    with pytest.raises(ValueError,match="normalized"): RetrievalCandidate("table",1.1,1)
    identity=RetrieverIdentity("x","1","s","topical_only"); timing=RetrievalTiming(0,0,0,"test")
    with pytest.raises(ValueError,match="contiguous"): RetrievalResult("success",identity,timing,(RetrievalCandidate("table",1,2),))
