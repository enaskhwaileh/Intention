from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from statistics import mean
import math,yaml
from intention.evaluation.statistics import paired_bootstrap
from intention.retrieval.serialization import select_candidate_depth

ROOT=Path(__file__).resolve().parents[3]
CONFIG_PATH=ROOT/"configs/benchmarks/m7b_topical_bakeoff.yaml"

@dataclass(frozen=True)
class BakeoffFailure:
    component:str; code:str; reason:str; model:str|None=None

def load_bakeoff_contract(path:Path|None=None)->dict:
    raw=yaml.safe_load((path or CONFIG_PATH).read_text())
    required={"version","split","corpus","qrels","depths","quality_search","bootstrap","pilot","external_api","hybrid","models"}
    if not isinstance(raw,dict) or set(raw)!=required:raise ValueError("invalid M7B contract")
    if raw["depths"]!=[5,10,20,50,100] or raw["quality_search"]!={"metric_depth":100,"cosine_exact":True,"maximum_seconds_per_model":7200}:raise ValueError("quality search contract changed")
    development,holdout=derive_topic_split(raw["split"]["version"],raw["split"]["strata"])
    if development!=raw["split"]["development_ids"] or holdout!=raw["split"]["holdout_ids"]:raise ValueError("declared split does not match deterministic derivation")
    if set(development)&set(holdout) or set(development)|set(holdout)!=set(range(1,61)):raise ValueError("invalid topic partition")
    return raw

def derive_topic_split(version="m7b-topic-split-v1",strata=None):
    if version!="m7b-topic-split-v1":raise ValueError("unknown split version")
    strata=strata or {"QS1":[1,30],"QS2":[31,60]}; development=[]; holdout=[]
    for bounds in strata.values():
        ordered=sorted(range(bounds[0],bounds[1]+1),key=lambda q:sha256(f"{version}|{q}".encode()).hexdigest())
        development.extend(sorted(ordered[:len(ordered)//2])); holdout.extend(sorted(ordered[len(ordered)//2:]))
    return sorted(development),sorted(holdout)

def require_development_topics(topic_ids,contract=None):
    contract=contract or load_bakeoff_contract(); requested=set(topic_ids); locked=set(contract["split"]["holdout_ids"])
    if requested&locked:raise PermissionError(f"locked holdout evaluation forbidden: {sorted(requested&locked)}")
    unknown=requested-set(contract["split"]["development_ids"])
    if unknown:raise ValueError(f"unknown development topics: {sorted(unknown)}")

def validate_dense_inputs(query_texts,serialized_documents):
    forbidden=("grounded_action","action_arguments","requirements","capability_profiles","usefulness_label","topical_label","benchmark_labels","full_user_input")
    for text in [*query_texts,*serialized_documents]:
        lowered=text.lower()
        if any(term in lowered for term in forbidden):raise ValueError("dense input contains forbidden action, capability, or gold evidence")

def known_relevant_recall(ranked_ids,qrels,k,threshold=1):
    relevant={table_id for table_id,label in qrels.items() if label>=threshold}
    return len(set(ranked_ids[:k])&relevant)/len(relevant) if relevant else 0.0

def bpref(ranked_ids,qrels,threshold=1):
    relevant={t for t,y in qrels.items() if y>=threshold}; nonrelevant={t for t,y in qrels.items() if y<threshold}
    if not relevant:return 0.0
    if not nonrelevant:return len(set(ranked_ids)&relevant)/len(relevant)
    denominator=min(len(relevant),len(nonrelevant)); seen_nonrelevant=0; contributions=[]
    for table_id in ranked_ids:
        if table_id not in qrels:continue
        if table_id in nonrelevant:seen_nonrelevant+=1
        elif table_id in relevant:contributions.append(1-min(seen_nonrelevant,denominator)/denominator)
    return sum(contributions)/len(relevant)

def unjudged_diagnostic(ranked_ids,qrels,k):
    top=ranked_ids[:k]; judged=sum(table_id in qrels for table_id in top); unjudged=len(top)-judged
    return {"judged_count_in_topK":judged,"unjudged_count_in_topK":unjudged,"unjudged_rate":unjudged/len(top) if top else 0.0}

def macro_by_stratum(per_topic,development_ids):
    groups={"all":[],"QS1":[],"QS2":[]}
    for query_id in development_ids:
        groups["all"].append(per_topic[query_id]); groups["QS1" if query_id<=30 else "QS2"].append(per_topic[query_id])
    return {name:mean(values) for name,values in groups.items()}

def _graded_ndcg(ranked_ids,qrels,k):
    def dcg(labels):return sum((2**label-1)/math.log2(rank+2) for rank,label in enumerate(labels[:k]))
    actual=dcg([qrels.get(table_id,0) for table_id in ranked_ids]); ideal=dcg(sorted(qrels.values(),reverse=True))
    return actual/ideal if ideal else 0.0

def _mrr(ranked_ids,qrels,k,threshold=2):
    return next((1/rank for rank,table_id in enumerate(ranked_ids[:k],1) if qrels.get(table_id,-1)>=threshold),0.0)

def evaluate_development_rankings(rankings,qrels_by_topic,topic_ids,contract=None):
    contract=contract or load_bakeoff_contract(); require_development_topics(topic_ids,contract)
    if set(rankings)!=set(topic_ids) or set(qrels_by_topic)!=set(topic_ids):raise ValueError("complete development rankings and qrels required")
    per_topic={}
    for query_id in topic_ids:
        ranked=list(rankings[query_id]); qrels=qrels_by_topic[query_id]
        if len(ranked)<100:raise ValueError("exact top-100 ranking required")
        if len(ranked)!=len(set(ranked)):raise ValueError("duplicate ranked table ID")
        row={f"known_relevant_recall_at_{k}":known_relevant_recall(ranked,qrels,k) for k in contract["depths"]}
        row.update({"ndcg_at_10":_graded_ndcg(ranked,qrels,10),"mrr_at_10":_mrr(ranked,qrels,10),"bpref":bpref(ranked,qrels)})
        row["unjudged"]={str(k):unjudged_diagnostic(ranked,qrels,k) for k in contract["depths"]}; per_topic[query_id]=row
    metrics={}
    for key in [*(f"known_relevant_recall_at_{k}" for k in contract["depths"]),"ndcg_at_10","mrr_at_10","bpref"]:
        metrics[key]=macro_by_stratum({q:per_topic[q][key] for q in topic_ids},topic_ids)
    return {"classification":"development_topical_retrieval","paper_result":False,"split_version":contract["split"]["version"],"topic_count":len(topic_ids),"metrics":metrics,"per_topic":per_topic}

def paired_model_bootstrap(first,second,contract=None):
    contract=contract or load_bakeoff_contract(); settings=contract["bootstrap"]
    return paired_bootstrap(first,second,settings["iterations"],settings["seed"],settings["confidence"])

def select_encoder(results,eligible):
    candidates=[r for r in results if r["model"] in eligible and r.get("status")=="complete"]
    if not candidates:return {"status":"blocked","winner":None,"reason":"no eligible model completed"}
    candidates.sort(key=lambda r:(-r["known_relevant_recall_at_100"],r["model"])); first=candidates[0]
    if len(candidates)==1:return {"status":"selected","winner":first["model"],"rule":"only_completed_eligible"}
    second=candidates[1]
    if first["known_relevant_recall_at_100"]-second["known_relevant_recall_at_100"]>.01:return {"status":"selected","winner":first["model"],"rule":"recall_at_100"}
    tied=sorted((first,second),key=lambda r:(-r["bpref"],r["model"])); first,second=tied
    if first["bpref"]-second["bpref"]>.01:return {"status":"selected","winner":first["model"],"rule":"bpref"}
    timed=sorted((first,second),key=lambda r:(r["embedding_wall_seconds"],r["model"])); first,second=timed
    if second["embedding_wall_seconds"]>first["embedding_wall_seconds"]*1.1:return {"status":"selected","winner":first["model"],"rule":"embedding_wall_time"}
    sized=sorted((first,second),key=lambda r:(r["physical_index_bytes"],r["model"]))
    return {"status":"selected","winner":sized[0]["model"],"rule":"physical_index_bytes"}

def require_exact_search(exact,elapsed_seconds,contract=None):
    contract=contract or load_bakeoff_contract()
    if exact is not True:raise RuntimeError("model-selection retrieval must use exact cosine search")
    if not math.isfinite(elapsed_seconds) or elapsed_seconds<0:raise ValueError("invalid exact-search timing")
    if elapsed_seconds>contract["quality_search"]["maximum_seconds_per_model"]:raise TimeoutError("exact development search exceeded two-hour model limit")

def external_cost_estimate(model_name,estimated_tokens=None,credentials_present=False,contract=None):
    contract=contract or load_bakeoff_contract(); model=contract["models"][model_name]
    if model["role"]!="external_ceiling":raise ValueError("cost estimates are external-ceiling only")
    if estimated_tokens is not None and (not isinstance(estimated_tokens,int) or estimated_tokens<0):raise ValueError("invalid estimated token volume")
    rate=model["reference_cost_per_million_tokens_usd"]
    return {"provider":"google" if model_name.startswith("gemini") else "voyage_ai","model_alias":model_name,"credentials_present":bool(credentials_present),"estimated_corpus_tokens":estimated_tokens,"reference_cost_per_million_tokens_usd":rate,"estimated_hypothetical_cost_usd":None if estimated_tokens is None else estimated_tokens/1_000_000*rate,"free_quota_status":"unknown","execution_status":"estimate_only_not_executed","actual_spend_usd":0}

def local_pilot_preflight(models,accelerator_available):
    if accelerator_available:return [{"model":m,"status":"ready_for_10k_pilot"} for m in models]
    return [{"model":m,"status":"not_executed","failure":{"code":"accelerator_unavailable","reason":"native unquantized common-accelerator pilot requirement cannot be satisfied; no substitution made"}} for m in models]

def preflight_report(accelerator_available=None,environ=None):
    contract=load_bakeoff_contract(); eligible=[name for name,item in contract["models"].items() if item["eligible"]]
    if accelerator_available is None:
        from intention.evaluation.m7b_pilot import TorchHardwareDetector
        accelerator_available=TorchHardwareDetector().detect().cuda_available
    return {"classification":"m7b_execution_preflight","paper_result":False,"development_only":True,"split_version":contract["split"]["version"],"contract_sha256":sha256(CONFIG_PATH.read_bytes()).hexdigest(),"corpus_digest":contract["corpus"]["logical_digest"],"serialization_id":contract["corpus"]["serialization_id"],"local_pilots":local_pilot_preflight(eligible,accelerator_available),"external_ceilings":{"gemini-embedding-2":external_cost_estimate("gemini-embedding-2",contract=contract),"voyage-4-large":external_cost_estimate("voyage-4-large",contract=contract)},"winner":{"status":"blocked","winner":None,"reason":"full-corpus exact-search results are unavailable"},"candidate_depth":{"status":"not_selected","reason":"encoder is not frozen"},"hybrid":{"status":"not_executed","reason":"encoder and candidate depth must be frozen first"},"holdout":{"status":"locked_not_evaluated","topic_count":30}}

def assert_hybrid_cannot_change_winner(frozen_winner,hybrid_results):
    if not frozen_winner:raise RuntimeError("encoder must be frozen before hybrid diagnostics")
    return {"frozen_encoder":frozen_winner,"hybrid_role":"post_freeze_candidate_generation_diagnostic","winner_unchanged":True,"results":hybrid_results}
