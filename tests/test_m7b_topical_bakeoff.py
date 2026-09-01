from dataclasses import replace
import pytest
from intention.architecture.embedding import load_embedding_registry
from intention.architecture.huggingface import HuggingFaceEmbeddingProvider
from intention.evaluation.topical_bakeoff import *

def test_exact_split_and_stratum_balance():
    contract=load_bakeoff_contract(); dev,holdout=derive_topic_split()
    assert dev==contract["split"]["development_ids"] and holdout==contract["split"]["holdout_ids"]
    assert len(dev)==len(holdout)==30
    assert sum(q<=30 for q in dev)==sum(q>30 for q in dev)==15

def test_holdout_is_fail_closed():
    require_development_topics([1,60])
    with pytest.raises(PermissionError,match="locked holdout"):require_development_topics([1,2])

def test_dense_input_leakage_guard():
    validate_dense_inputs(["population of Italian cities"],["{\"title\":\"cities\"}"])
    with pytest.raises(ValueError,match="forbidden"):validate_dense_inputs(["population"],["{\"usefulness_label\":2}"])

def test_exact_model_registrations_and_formatting():
    registry=load_embedding_registry()
    qwen=registry.models["Qwen3-Embedding-4B"].record
    assert qwen["revision"]==qwen["tokenizer_revision"]=="5cf2132abc99cad020ac570b19d031efec650f2b"
    assert qwen["dimensions"]==[2560] and qwen["trust_remote_code_required"] is False
    nemo=registry.models["Nemotron-3-Embed-1B-BF16"].record
    assert nemo["revision"]=="f880174635613cff04033875fc6a69296cb72006" and nemo["dimensions"]==[2048]
    provider=HuggingFaceEmbeddingProvider(nemo,model_factory=lambda **_:object(),tokenizer_factory=lambda **_:object())
    assert provider._format("topic","query")=="query: topic"
    assert provider._format("table","document")=="passage: table"

def test_remote_code_is_rejected():
    record=dict(load_embedding_registry().models["Qwen3-Embedding-4B"].record,trust_remote_code_required=True)
    with pytest.raises(ValueError,match="remote-code"):HuggingFaceEmbeddingProvider(record,model_factory=lambda **_:None,tokenizer_factory=lambda **_:None)

def test_known_relevant_recall_and_unjudged_diagnostics():
    qrels={"a":2,"b":1,"c":0}
    assert known_relevant_recall(["a","x","c"],qrels,2)==.5
    assert known_relevant_recall(["x"],{"c":0},1)==0
    assert unjudged_diagnostic(["a","x","c"],qrels,3)=={"judged_count_in_topK":2,"unjudged_count_in_topK":1,"unjudged_rate":1/3}

def test_bpref_hand_computable_and_unjudged_ignored():
    assert bpref(["n","x","r1","r2"],{"r1":2,"r2":1,"n":0})==.5
    assert bpref(["x"],{"n":0})==0

def _result(model,r,b,t,s,status="complete"):
    return {"model":model,"status":status,"known_relevant_recall_at_100":r,"bpref":b,"embedding_wall_seconds":t,"physical_index_bytes":s}

def test_winner_primary_and_all_tie_breakers():
    eligible={"a","b"}
    assert select_encoder([_result("a",.8,.2,20,20),_result("b",.7,.9,1,1)],eligible)["rule"]=="recall_at_100"
    assert select_encoder([_result("a",.8,.8,20,20),_result("b",.795,.7,1,1)],eligible)["rule"]=="bpref"
    assert select_encoder([_result("a",.8,.8,10,20),_result("b",.795,.795,20,1)],eligible)["rule"]=="embedding_wall_time"
    assert select_encoder([_result("a",.8,.8,10,20),_result("b",.795,.795,10.5,1)],eligible)=={"status":"selected","winner":"b","rule":"physical_index_bytes"}

def test_reference_and_api_models_cannot_win_or_substitute():
    eligible={"open"}; results=[_result("gemini",1,1,1,1),_result("BM25",1,1,1,1),_result("open",.1,.1,9,9)]
    assert select_encoder(results,eligible)["winner"]=="open"
    assert select_encoder([_result("open",0,0,0,0,"not_executed")],eligible)["status"]=="blocked"

def test_depth_saturation_rule():
    assert select_candidate_depth({5:.7,10:.795,20:.8,50:.81,100:.81})==10
    assert select_candidate_depth({5:.7,10:.75,20:.77,50:.78,100:.8})==100

def test_exact_search_enforced_and_timed():
    require_exact_search(True,10)
    with pytest.raises(RuntimeError,match="exact cosine"):require_exact_search(False,10)
    with pytest.raises(TimeoutError):require_exact_search(True,7200.1)

def test_paid_default_cost_gate():
    assert paid_execution_status(environ={})["code"]=="paid_execution_not_authorized"
    assert paid_execution_status(76,environ={"INTENTION_ALLOW_PAID_EMBEDDING_BAKEOFF":"1"})["code"]=="cost_cap_exceeded"
    assert paid_execution_status(75,environ={"INTENTION_ALLOW_PAID_EMBEDDING_BAKEOFF":"1"})["status"]=="authorized"

def test_structured_pilot_failure_and_hybrid_ordering():
    outcome=local_pilot_preflight(["m"],False)[0]
    assert outcome["status"]=="not_executed" and outcome["failure"]["code"]=="accelerator_unavailable"
    with pytest.raises(RuntimeError):assert_hybrid_cannot_change_winner(None,{})
    assert assert_hybrid_cannot_change_winner("m",{"BM25":.1})["winner_unchanged"] is True

def test_development_evaluation_is_topical_complete_and_stratified():
    ids=[1,32]; ranking=["r","h","n",*map(str,range(97))]
    result=evaluate_development_rankings({q:ranking for q in ids},{q:{"r":1,"h":2,"n":0} for q in ids},ids)
    assert result["paper_result"] is False and result["topic_count"]==2
    assert result["metrics"]["known_relevant_recall_at_5"]=={"all":1,"QS1":1,"QS2":1}
    assert result["metrics"]["mrr_at_10"]["all"]==.5
    with pytest.raises(ValueError,match="duplicate"):evaluate_development_rankings({1:["x"]*100},{1:{"x":1}},[1])

def test_preflight_never_claims_selection_without_execution():
    report=preflight_report(False,{})
    assert report["winner"]["status"]=="blocked" and report["holdout"]["status"]=="locked_not_evaluated"
    assert all(item["failure"]["code"]=="accelerator_unavailable" for item in report["local_pilots"])
