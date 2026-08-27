import math
from collections import defaultdict

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
