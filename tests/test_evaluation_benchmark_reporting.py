import json
import pytest
from intention.benchmarks import check_topic_leakage,pool_results,split_topics,validate_annotations
from intention.evaluation.metrics import action_metrics,argument_metrics,mrr,ndcg,pairwise_accuracy,useful_recall
from intention.evaluation.statistics import holm,paired_bootstrap
from intention.reporting.latex import generate_table

def test_topic_split_is_deterministic_and_leak_free():
    assert split_topics(range(20))==split_topics(range(20)); check_topic_leakage({"train":["a"],"dev":["b"],"test":["c"]})
    with pytest.raises(ValueError,match="leakage"): check_topic_leakage({"train":["a"],"test":["a"]})
def test_pool_requires_ours_and_deduplicates():
    assert pool_results({"Ours":["a","b"],"BM25":["b","c"]},2)==("a","b","c")
    with pytest.raises(ValueError): pool_results({"BM25":["a"]},1)
def test_annotation_validation():
    base={"topic_id":"t","variant_id":"v","table_id":"x","topical_label":2,"usefulness_label":3}
    assert validate_annotations([{**base,"annotator_id":"a"},{**base,"annotator_id":"b"}])
    with pytest.raises(ValueError): validate_annotations([{**base,"annotator_id":"a"}])
def test_metric_regression_values():
    labels=[3,0,2]; assert ndcg(labels,3)==pytest.approx(.9558305893); assert mrr(labels)==1; assert useful_recall(labels,2)==.5
    assert action_metrics(["COMPARE","PREDICT"],["COMPARE","COMPARE"])["accuracy"]==.5
    assert argument_metrics({"a":1,"b":2},{"a":1})=={"precision":1,"recall":.5,"f1":2/3}
    assert pairwise_accuracy([(1,.5,True),(.2,.4,False)])==1
def test_statistics_deterministic_and_corrected():
    assert paired_bootstrap({"a":1,"b":.5},{"a":.5,"b":.5},100)["difference"]==.25
    adjusted=holm([.01,.04]); assert adjusted==pytest.approx([.02,.04])
def test_latex_fails_closed_and_generates(tmp_path):
    run=tmp_path/"system"; run.mkdir(); (run/"metrics.json").write_text(json.dumps({"ndcg@5":.5}))
    output=generate_table([run],["ndcg@5"],tmp_path/"table.tex"); assert "0.500" in output.read_text()
    with pytest.raises(ValueError,match="missing metrics"): generate_table([run],["mrr"],tmp_path/"bad.tex")
