import pytest
from intention.evaluation import (
    action_switch_diagnostics,action_switch_qrel_diagnostics,assert_tuning_allowed,candidate_recall,candidate_set_recall,
    controlled_evaluation_summary,corrected_paired_tests,deterministic_rank,
    dual_ordinal_agreement,evaluate_ranked_qrels,judgment_completeness,load_evaluation_protocol,mrr,ndcg,per_action_metrics,
    paired_bootstrap,quadratic_weighted_kappa,ranking_deltas,require_complete_judgments,validate_qrels,
    topic_first_mean,useful_recall,
)

def test_versioned_protocol_freezes_cutoffs_thresholds_statistics_and_layers():
    protocol=load_evaluation_protocol()
    assert protocol.version=="1.1.0" and len(protocol.digest)==64
    assert protocol.raw["labels"]=={"topical":[0,1,2],"usefulness":[0,1,2,3],"useful_threshold":2}
    assert protocol.raw["ranking"]["ideal_dcg"]=="all_tables_in_declared_universe"
    assert protocol.raw["ranking"]["useful_recall_denominator"]=="all_useful_judged_tables_in_declared_universe"
    assert protocol.raw["statistics"]["bootstrap"]=={"iterations":2000,"seed":2026,"confidence":.95,"unit":"topic"}

def test_hand_computable_ranking_and_retrieval_metrics():
    labels=[3,0,2,0,1,0,0,2,0,0]
    assert ndcg(labels,5)==pytest.approx(.8210727465696264)
    assert ndcg(labels,10)==pytest.approx(.9085118946394064)
    assert mrr(labels,2)==1
    assert useful_recall(labels,5,2)==pytest.approx(2/3)
    assert candidate_recall(["a","x","b","y","c"],["a","b","c","d"],5)==.75

def test_per_action_switch_delta_and_topic_first_diagnostics():
    rows=[{"topic_id":"t1","action":"COMPARE","score":1},{"topic_id":"t1","action":"COMPARE","score":1},{"topic_id":"t1","action":"COMPARE","score":1},{"topic_id":"t2","action":"COMPARE","score":0},{"topic_id":"t1","action":"PREDICT","score":.5}]
    assert per_action_metrics(rows,"score")=={"COMPARE":.5,"PREDICT":.5}
    switches=[{"topic_id":"t","first_top":"a","second_top":"b","expected_first":"a","expected_second":"b"}]
    assert action_switch_diagnostics(switches)=={"pair_count":1,"pair_accuracy":1,"changed_top_rate":1}
    deltas=ranking_deltas([{"topic_id":"t","relevance_only":.4,"action_aware":.7}])
    assert deltas["mean"]==pytest.approx(.3)

def test_ordinal_agreement_missing_policy_and_deterministic_ties():
    assert quadratic_weighted_kappa([0,1,2,3],[0,1,3,2])==pytest.approx(.8)
    ranked=deterministic_rank([{"table_id":"b","score":1},{"table_id":"a","score":1}])
    assert [item["table_id"] for item in ranked]==["a","b"]
    record={"topic_id":"t","variant_id":"v","table_id":"x","annotator_id":"a","topical_label":2,"usefulness_label":2}
    assert require_complete_judgments([record],[("t","v","x","a")])
    with pytest.raises(ValueError,match="missing"): require_complete_judgments([], [("t","v","x","a")])

def test_statistics_use_declared_holm_family_and_controlled_summary_is_not_evidence():
    comparisons={"a_vs_b":({"t1":.7,"t2":.5,"t3":.4},{"t1":.4,"t2":.6,"t3":.2})}
    result=corrected_paired_tests(comparisons)
    assert result["a_vs_b"]["raw_p"]==pytest.approx(.5)
    assert result["a_vs_b"]["correction"]=="holm"
    summary=controlled_evaluation_summary()
    assert summary["classification"]["paper_result"] is False
    assert summary["retrieval"]["candidate_set_recall"]==pytest.approx(2/3)

def test_bootstrap_uses_configured_confidence_quantiles():
    left={f"t{i}":value for i,value in enumerate((0,0,0,1,1,2))}; right={key:0 for key in left}
    narrow=paired_bootstrap(left,right,2000,17,.5); wide=paired_bootstrap(left,right,2000,17,.95)
    assert narrow["confidence"]==.5 and wide["confidence"]==.95
    assert wide["low"]<=narrow["low"]<=narrow["high"]<=wide["high"]
    assert (wide["low"],wide["high"])!=(narrow["low"],narrow["high"])

def _qrels():
    return {"a":{"topical_label":2,"usefulness_label":3},"b":{"topical_label":2,"usefulness_label":3},"c":{"topical_label":1,"usefulness_label":2},"d":{"topical_label":0,"usefulness_label":0}}

@pytest.mark.parametrize("field",["topical_label","usefulness_label"])
def test_complete_qrels_require_both_judgments(field):
    qrels=_qrels(); del qrels["a"][field]
    with pytest.raises(ValueError,match="incomplete"): validate_qrels(qrels,["a","b","c","d"])

def test_ranked_qrels_reject_duplicates_unknowns_and_use_fixed_ideal_universe():
    qrels=_qrels(); universe=["a","b","c","d"]
    with pytest.raises(ValueError,match="duplicate"): evaluate_ranked_qrels([{"table_id":"a","score":1},{"table_id":"a","score":.5}],qrels,universe)
    with pytest.raises(ValueError,match="unknown"): evaluate_ranked_qrels([{"table_id":"z","score":1}],qrels,universe)
    result=evaluate_ranked_qrels([{"table_id":"b","score":1},{"table_id":"a","score":1}],qrels,universe,(5,))
    assert result["ranked_table_ids"]==["a","b"]
    assert result["usefulness_ndcg@5"]<1
    assert result["useful_recall@5"]==pytest.approx(2/3)
    assert candidate_set_recall(["a","b"],qrels,universe)==pytest.approx(2/3)

def test_action_switch_accepts_tied_optimal_tables_from_qrels():
    first=_qrels(); second=_qrels(); second["a"]["usefulness_label"]=1; second["b"]["usefulness_label"]=2; second["c"]["usefulness_label"]=2
    pair={"topic_id":"t","first_ranked":[{"table_id":"b","score":1}],"second_ranked":[{"table_id":"c","score":1}],"first_qrels":first,"second_qrels":second,"universe":["a","b","c","d"]}
    assert action_switch_qrel_diagnostics([pair])["pair_accuracy"]==1

def test_agreement_reports_topical_and_usefulness_separately():
    left=[{"topical_label":0,"usefulness_label":0},{"topical_label":2,"usefulness_label":3}]
    right=[{"topical_label":0,"usefulness_label":0},{"topical_label":1,"usefulness_label":2}]
    assert set(dual_ordinal_agreement(left,right))=={"topical","usefulness"}
    assert judgment_completeness([{"topical_label":2,"usefulness_label":None},{"topical_label":None,"usefulness_label":1}])=={"topical":.5,"usefulness":.5}

@pytest.mark.parametrize("parameter",["usefulness_threshold","candidate_depth","fusion_weights","score_calibration","prompts"])
def test_test_labels_cannot_tune_any_protected_parameter(parameter):
    with pytest.raises(ValueError,match="forbidden"): assert_tuning_allowed("test",parameter)
    assert assert_tuning_allowed("development",parameter) is None
