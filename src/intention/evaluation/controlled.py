import json
from pathlib import Path
from .annotation import dual_ordinal_agreement,judgment_completeness
from .metrics import per_action_metrics,ranking_deltas
from .protocol import load_evaluation_protocol
from .ranking import action_switch_qrel_diagnostics,candidate_set_recall,evaluate_ranked_qrels
from .statistics import corrected_paired_tests,paired_bootstrap

def controlled_evaluation_summary(path: Path|None=None):
    path=path or Path(__file__).resolve().parents[3]/"fixtures/evaluation_controlled.json"
    data=json.loads(path.read_text()); protocol=load_evaluation_protocol(); threshold=protocol.raw["labels"]["useful_threshold"]; a=data["system_a"]; b=data["system_b"]
    normative=evaluate_ranked_qrels(data["ranked"],data["qrels"],data["universe"],tuple(protocol.raw["ranking"]["ndcg_cutoffs"]),tuple(protocol.raw["ranking"]["useful_recall_cutoffs"]),threshold)
    switch_pairs=[]
    for pair in data["action_switch_pairs"]:
        qrels=lambda usefulness:{table_id:{"topical_label":data["qrels"][table_id]["topical_label"],"usefulness_label":usefulness[table_id]} for table_id in data["universe"]}
        switch_pairs.append({"topic_id":pair["topic_id"],"first_ranked":pair["first_ranked"],"second_ranked":pair["second_ranked"],"first_qrels":qrels(pair["first_usefulness"]),"second_qrels":qrels(pair["second_usefulness"]),"universe":data["universe"]})
    bootstrap=protocol.raw["statistics"]["bootstrap"]
    return {"classification":{"dataset":"controlled_fixture","paper_result":False},"protocol":{"version":protocol.version,"hash":protocol.digest},"interpretation_grounding":{"reported_separately":True},"retrieval":{"candidate_set_recall":candidate_set_recall(data["candidate_ids"],data["qrels"],data["universe"],threshold)},"usefulness_ranking":{**normative,"deltas":ranking_deltas(data["ranking_comparisons"])},"per_action":per_action_metrics(data["action_rows"],"score"),"action_switch":action_switch_qrel_diagnostics(switch_pairs),"annotation":{"agreement":dual_ordinal_agreement(data["annotator_a"],data["annotator_b"]),"completeness":{"annotator_a":judgment_completeness(data["annotator_a"]),"annotator_b":judgment_completeness(data["annotator_b"])}},"statistics":{"bootstrap":paired_bootstrap(a,b,bootstrap["iterations"],bootstrap["seed"],bootstrap["confidence"]),"corrected_tests":corrected_paired_tests({"action_aware_vs_relevance":(a,b)},protocol.raw["statistics"]["paired_test"]["iterations"],protocol.raw["statistics"]["paired_test"]["seed"])}}
