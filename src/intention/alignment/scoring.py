from statistics import mean
from intention.contracts import Capability, RequirementProfile
from intention.knowledge.layer import KnowledgeLayer
from .matching import match_value

def align(profile: RequirementProfile, capabilities: tuple[Capability,...], kg: KnowledgeLayer, eta_o: float=.2, eta_n: float=.5, required_aggregation: str="min", confidence: bool=True) -> tuple[float,dict]:
    if not 0<=eta_o<=1 or not 0<=eta_n<=1: raise ValueError("etas must be in [0,1]")
    by_axis={}; matches=[]
    for req in profile.requirements:
        candidates=[c for c in capabilities if c.predicate==req.predicate and c.axis==req.axis]
        score=max((match_value(kg.predicates[req.predicate].matcher,req.expected,c.value)*(c.confidence if confidence else 1) for c in candidates),default=0.0)
        matches.append((req,score)); by_axis.setdefault(req.axis,{"req":[],"opt":[],"neg":[]})[req.polarity].append(score)
    active=set(by_axis); axis_scores={}
    for axis,groups in by_axis.items():
        r=(min(groups["req"]) if required_aggregation=="min" else mean(groups["req"])) if groups["req"] else 1.0
        o=mean(groups["opt"]) if groups["opt"] else 0.0; n=mean(groups["neg"]) if groups["neg"] else 0.0
        axis_scores[axis]=r*((1-eta_o)+eta_o*o)*(1-eta_n*n)
    denom=sum(profile.weights[x] for x in active)
    score=sum(profile.weights[x]/denom*axis_scores[x] for x in active) if denom else 0.0
    return score,{"axis_scores":axis_scores,"matches":[{"predicate":r.predicate,"score":s} for r,s in matches]}
