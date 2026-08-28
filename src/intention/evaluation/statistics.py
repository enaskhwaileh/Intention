import random
import itertools
from statistics import mean

def paired_bootstrap(a,b,iterations=1000,seed=2026,confidence=.95):
    if set(a)!=set(b) or not a: raise ValueError("paired topic mappings required")
    if not 0<confidence<1: raise ValueError("bootstrap confidence must be in (0,1)")
    keys=sorted(a); rng=random.Random(seed); values=[]
    for _ in range(iterations):
        sample=[rng.choice(keys) for _ in keys]; values.append(mean(a[k]-b[k] for k in sample))
    values.sort(); alpha=(1-confidence)/2
    return {"difference":mean(a[k]-b[k] for k in keys),"low":values[int(alpha*iterations)],"high":values[min(iterations-1,int((1-alpha)*iterations))],"confidence":confidence}
def holm(p_values):
    ordered=sorted(enumerate(p_values),key=lambda x:x[1]); out=[0.0]*len(p_values); running=0
    for rank,(index,p) in enumerate(ordered): running=max(running,min(1,p*(len(p_values)-rank))); out[index]=running
    return out

def paired_sign_permutation(a,b,iterations=10000,seed=2026):
    if set(a)!=set(b) or not a: raise ValueError("paired topic mappings required")
    differences=[a[key]-b[key] for key in sorted(a)]; observed=abs(mean(differences)); n=len(differences)
    if n<=16:
        samples=(abs(mean(sign*value for sign,value in zip(signs,differences))) for signs in itertools.product((-1,1),repeat=n))
        values=list(samples); return sum(value>=observed-1e-15 for value in values)/len(values)
    else:
        rng=random.Random(seed); values=[abs(mean((1 if rng.random()<.5 else -1)*value for value in differences)) for _ in range(iterations)]
    return (sum(value>=observed-1e-15 for value in values)+1)/(len(values)+1)

def corrected_paired_tests(comparisons,iterations=10000,seed=2026):
    names=sorted(comparisons); raw=[paired_sign_permutation(*comparisons[name],iterations,seed) for name in names]; adjusted=holm(raw)
    return {name:{"raw_p":raw[i],"adjusted_p":adjusted[i],"correction":"holm","family":"all_predeclared_primary_system_comparisons"} for i,name in enumerate(names)}
