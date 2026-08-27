import random
from statistics import mean

def paired_bootstrap(a,b,iterations=1000,seed=2026):
    if set(a)!=set(b) or not a: raise ValueError("paired topic mappings required")
    keys=sorted(a); rng=random.Random(seed); values=[]
    for _ in range(iterations):
        sample=[rng.choice(keys) for _ in keys]; values.append(mean(a[k]-b[k] for k in sample))
    values.sort(); return {"difference":mean(a[k]-b[k] for k in keys),"low":values[int(.025*iterations)],"high":values[min(iterations-1,int(.975*iterations))]}
def holm(p_values):
    ordered=sorted(enumerate(p_values),key=lambda x:x[1]); out=[0.0]*len(p_values); running=0
    for rank,(index,p) in enumerate(ordered): running=max(running,min(1,p*(len(p_values)-rank))); out[index]=running
    return out
