import math
from collections import defaultdict
from statistics import mean

def ndcg(labels,k):
    def dcg(xs): return sum((2**x-1)/math.log2(i+2) for i,x in enumerate(xs[:k]))
    ideal=dcg(sorted(labels,reverse=True)); return dcg(labels)/ideal if ideal else 0.0
def mrr(labels,threshold=2): return next((1/i for i,x in enumerate(labels,1) if x>=threshold),0.0)
def useful_recall(labels,k,threshold=2):
    total=sum(x>=threshold for x in labels); return sum(x>=threshold for x in labels[:k])/total if total else 0.0
def action_metrics(gold,pred,actions=("COMPARE","AGGREGATE","PREDICT","EXPLAIN","MONITOR")):
    if len(gold)!=len(pred): raise ValueError("length mismatch")
    acc=sum(a==b for a,b in zip(gold,pred))/len(gold) if gold else 0.0; fs=[]
    for action in actions:
        tp=sum(a==b==action for a,b in zip(gold,pred)); fp=sum(a!=action and b==action for a,b in zip(gold,pred)); fn=sum(a==action and b!=action for a,b in zip(gold,pred)); fs.append(2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else 0)
    return {"accuracy":acc,"macro_f1":sum(fs)/len(fs)}
def argument_metrics(gold,pred):
    gs=set(gold.items()); ps=set(pred.items()); tp=len(gs&ps); precision=tp/len(ps) if ps else 0; recall=tp/len(gs) if gs else 0
    return {"precision":precision,"recall":recall,"f1":2*precision*recall/(precision+recall) if precision+recall else 0}
def pairwise_accuracy(pairs): return sum(expected==(left>right) for left,right,expected in pairs)/len(pairs) if pairs else 0.0

def candidate_recall(retrieved_ids,useful_ids,k):
    useful=set(useful_ids)
    return len(set(retrieved_ids[:k])&useful)/len(useful) if useful else 0.0

def deterministic_rank(items):
    return sorted(items,key=lambda item:(-item["score"],item["table_id"]))

def topic_first_mean(rows,metric):
    grouped=defaultdict(list)
    for row in rows: grouped[row["topic_id"]].append(float(row[metric]))
    if not grouped: raise ValueError("topic metrics are required")
    per_topic={topic:mean(values) for topic,values in sorted(grouped.items())}
    return {"per_topic":per_topic,"mean":mean(per_topic.values())}

def per_action_metrics(rows,metric):
    grouped=defaultdict(list)
    for row in rows: grouped[row["action"]].append(float(row[metric]))
    return {action:mean(values) for action,values in sorted(grouped.items())}

def action_switch_diagnostics(pairs):
    if not pairs: return {"pair_count":0,"pair_accuracy":0.0,"changed_top_rate":0.0}
    correct=[]; changed=[]
    for pair in pairs:
        required={"topic_id","first_top","second_top","expected_first","expected_second"}
        if set(pair)!=required: raise ValueError("invalid action-switch pair")
        correct.append(pair["first_top"]==pair["expected_first"] and pair["second_top"]==pair["expected_second"])
        changed.append(pair["first_top"]!=pair["second_top"])
    return {"pair_count":len(pairs),"pair_accuracy":mean(correct),"changed_top_rate":mean(changed)}

def ranking_deltas(rows,baseline_key="relevance_only",system_key="action_aware"):
    values=[{"topic_id":row["topic_id"],"delta":float(row[system_key])-float(row[baseline_key])} for row in rows]
    result=topic_first_mean(values,"delta"); result["deltas"]=values; return result
