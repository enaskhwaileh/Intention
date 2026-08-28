import pytest
from intention.evaluation import (
    action_switch_diagnostics,assert_tuning_allowed,candidate_recall,
    controlled_evaluation_summary,corrected_paired_tests,deterministic_rank,
    load_evaluation_protocol,mrr,ndcg,per_action_metrics,
    quadratic_weighted_kappa,ranking_deltas,require_complete_judgments,
    topic_first_mean,useful_recall,
)

def test_versioned_protocol_freezes_cutoffs_thresholds_statistics_and_layers():
    protocol=load_evaluation_protocol()
    assert protocol.version=="1.0.0" and len(protocol.digest)==64
    assert protocol.raw["ranking"]=={"ndcg_cutoffs":[5,10],"mrr_threshold":2,"useful_recall_cutoffs":[5,10,20],"tie_break":"score_desc_table_id_asc"}
    assert protocol.raw["statistics"]["bootstrap"]=={"iterations":2000,"seed":2026,"confidence":.95,"unit":"topic"}

def test_hand_computable_ranking_and_retrieval_metrics():
    labels=[3,0,2,0,1,0,0,2,0,0]
    assert ndcg(labels,5)==pytest.approx(.8210727465696264)
    assert ndcg(labels,10)==pytest.approx(.9085118946394064)
    assert mrr(labels,2)==1
    assert useful_recall(labels,5,2)==pytest.approx(2/3)
    assert candidate_recall(["a","x","b","y","c"],["a","b","c","d"],5)==.75

def test_per_action_switch_delta_and_topic_first_diagnostics():
    rows=[{"topic_id":"t1","action":"COMPARE","score":1},{"topic_id":"t1","action":"PREDICT","score":.5},{"topic_id":"t2","action":"COMPARE","score":.5}]
    assert per_action_metrics(rows,"score")=={"COMPARE":.75,"PREDICT":.5}
    assert topic_first_mean(rows,"score")=={"per_topic":{"t1":.75,"t2":.5},"mean":.625}
    switches=[{"topic_id":"t","first_top":"a","second_top":"b","expected_first":"a","expected_second":"b"}]
    assert action_switch_diagnostics(switches)=={"pair_count":1,"pair_accuracy":1,"changed_top_rate":1}
    deltas=ranking_deltas([{"topic_id":"t","relevance_only":.4,"action_aware":.7}])
    assert deltas["mean"]==pytest.approx(.3)

def test_ordinal_agreement_missing_policy_and_deterministic_ties():
    assert quadratic_weighted_kappa([0,1,2,3],[0,1,3,2])==pytest.approx(.8)
    ranked=deterministic_rank([{"table_id":"b","score":1},{"table_id":"a","score":1}])
    assert [item["table_id"] for item in ranked]==["a","b"]
    record={"topic_id":"t","variant_id":"v","table_id":"x","annotator_id":"a","usefulness_label":2}
    assert require_complete_judgments([record],[("t","v","x","a")])
    with pytest.raises(ValueError,match="missing"): require_complete_judgments([], [("t","v","x","a")])

def test_statistics_use_declared_holm_family_and_controlled_summary_is_not_evidence():
    comparisons={"a_vs_b":({"t1":.7,"t2":.5,"t3":.4},{"t1":.4,"t2":.6,"t3":.2})}
    result=corrected_paired_tests(comparisons)
    assert result["a_vs_b"]["raw_p"]==pytest.approx(.5)
    assert result["a_vs_b"]["correction"]=="holm"
    summary=controlled_evaluation_summary()
    assert summary["classification"]["paper_result"] is False
    assert summary["retrieval"]["upper_bound"]==.75

@pytest.mark.parametrize("parameter",["usefulness_threshold","candidate_depth","fusion_weights","score_calibration","prompts"])
def test_test_labels_cannot_tune_any_protected_parameter(parameter):
    with pytest.raises(ValueError,match="forbidden"): assert_tuning_allowed("test",parameter)
    assert assert_tuning_allowed("development",parameter) is None
