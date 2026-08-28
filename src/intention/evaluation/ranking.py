import math
from statistics import mean
from .metrics import deterministic_rank

def validate_qrels(qrels,universe):
    universe=tuple(universe)
    if len(universe)!=len(set(universe)) or set(qrels)!=set(universe): raise ValueError("qrels must exactly cover the declared evaluation universe")
    for table_id,labels in qrels.items():
        if set(labels)!={"topical_label","usefulness_label"}: raise ValueError(f"incomplete topical/usefulness judgment: {table_id}")
        if labels["topical_label"] not in {0,1,2}: raise ValueError(f"invalid topical judgment: {table_id}")
        if labels["usefulness_label"] not in {0,1,2,3}: raise ValueError(f"invalid usefulness judgment: {table_id}")
    return True

def _ndcg(ranked_ids,qrels,universe,k,label):
    gains=[qrels[table_id][label] for table_id in ranked_ids[:k]]
    ideal=sorted((qrels[table_id][label] for table_id in universe),reverse=True)[:k]
    dcg=lambda values:sum((2**value-1)/math.log2(index+2) for index,value in enumerate(values))
    denominator=dcg(ideal)
    return dcg(gains)/denominator if denominator else 0.0

def evaluate_ranked_qrels(ranked,qrels,universe,ndcg_cutoffs=(5,10),useful_recall_cutoffs=(5,10,20),useful_threshold=2):
    validate_qrels(qrels,universe)
    ids=[item.get("table_id") for item in ranked]
    if any(set(item)!={"table_id","score"} or not isinstance(item["score"],(int,float)) or not math.isfinite(item["score"]) for item in ranked): raise ValueError("ranked results require finite scored table IDs")
    if len(ids)!=len(set(ids)): raise ValueError("duplicate ranked table ID")
    unknown=set(ids)-set(universe)
    if unknown: raise ValueError(f"unknown ranked table ID: {sorted(unknown)}")
    ordered=deterministic_rank(ranked); ranked_ids=[item["table_id"] for item in ordered]
    useful={table_id for table_id in universe if qrels[table_id]["usefulness_label"]>=useful_threshold}
    result={"ranked_table_ids":ranked_ids}
    for k in ndcg_cutoffs:
        result[f"topical_ndcg@{k}"]=_ndcg(ranked_ids,qrels,universe,k,"topical_label")
        result[f"usefulness_ndcg@{k}"]=_ndcg(ranked_ids,qrels,universe,k,"usefulness_label")
    for k in useful_recall_cutoffs:
        result[f"useful_recall@{k}"]=len(set(ranked_ids[:k])&useful)/len(useful) if useful else 0.0
    result["mrr"]=next((1/index for index,table_id in enumerate(ranked_ids,1) if table_id in useful),0.0)
    return result

def candidate_set_recall(candidate_ids,qrels,universe,useful_threshold=2):
    validate_qrels(qrels,universe)
    if len(candidate_ids)!=len(set(candidate_ids)) or set(candidate_ids)-set(universe): raise ValueError("invalid candidate IDs")
    useful={table_id for table_id in universe if qrels[table_id]["usefulness_label"]>=useful_threshold}
    return len(set(candidate_ids)&useful)/len(useful) if useful else 0.0

def action_switch_qrel_diagnostics(pairs):
    if not pairs: return {"pair_count":0,"pair_accuracy":0.0,"changed_top_rate":0.0}
    correct=[]; changed=[]
    for pair in pairs:
        required={"topic_id","first_ranked","second_ranked","first_qrels","second_qrels","universe"}
        if set(pair)!=required: raise ValueError("invalid action-switch qrel pair")
        validate_qrels(pair["first_qrels"],pair["universe"]); validate_qrels(pair["second_qrels"],pair["universe"])
        first_top=evaluate_ranked_qrels(pair["first_ranked"],pair["first_qrels"],pair["universe"],(1,),())["ranked_table_ids"][0]
        second_top=evaluate_ranked_qrels(pair["second_ranked"],pair["second_qrels"],pair["universe"],(1,),())["ranked_table_ids"][0]
        acceptable=lambda qrels:{table_id for table_id in pair["universe"] if qrels[table_id]["usefulness_label"]==max(value["usefulness_label"] for value in qrels.values())}
        correct.append(first_top in acceptable(pair["first_qrels"]) and second_top in acceptable(pair["second_qrels"]))
        changed.append(first_top!=second_top)
    return {"pair_count":len(pairs),"pair_accuracy":mean(correct),"changed_top_rate":mean(changed)}
