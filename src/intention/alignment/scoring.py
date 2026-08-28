from statistics import mean
from intention.contracts import Capability, RequirementProfile
from intention.knowledge.layer import KnowledgeLayer
from .matching import match_value

def align(profile: RequirementProfile, capabilities: tuple[Capability,...], kg: KnowledgeLayer, eta_o: float=.2, eta_n: float=.5, required_aggregation: str="min", confidence: bool=True) -> tuple[float,dict]:
    if not 0<=eta_o<=1 or not 0<=eta_n<=1: raise ValueError("etas must be in [0,1]")
    if required_aggregation not in {"min", "mean"}:
        raise ValueError("required aggregation must be 'min' or the explicit 'mean' ablation")
    if profile.action not in kg.actions:
        raise ValueError(f"unsupported action in requirement profile: {profile.action}")
    if profile.weights != kg.actions[profile.action].weights:
        raise ValueError("requirement profile weights do not match the knowledge layer")
    for requirement in profile.requirements:
        if requirement.predicate not in kg.predicates:
            raise ValueError(f"unknown requirement predicate: {requirement.predicate}")
        if requirement.axis != kg.predicates[requirement.predicate].axis or requirement.polarity not in {"req", "opt", "neg"}:
            raise ValueError(f"invalid requirement contract: {requirement.predicate}")
    for capability in capabilities:
        if capability.predicate not in kg.predicates:
            raise ValueError(f"unknown capability predicate: {capability.predicate}")
        if capability.axis != kg.predicates[capability.predicate].axis:
            raise ValueError(f"capability axis mismatch: {capability.predicate}")
    by_axis={}; matches=[]
    for req in profile.requirements:
        candidates=[c for c in capabilities if c.predicate==req.predicate and c.axis==req.axis]
        predicate = kg.predicates[req.predicate]
        score=max((match_value(predicate.matcher,req.expected,c.value,predicate.parameters)*(c.confidence if confidence else 1) for c in candidates),default=0.0)
        matches.append((req,score)); by_axis.setdefault(req.axis,{"req":[],"opt":[],"neg":[]})[req.polarity].append(score)
    active=tuple(axis for axis in kg.axes if axis in by_axis); axis_scores={}; components={}
    for axis in active:
        groups=by_axis[axis]
        r=(min(groups["req"]) if required_aggregation=="min" else mean(groups["req"])) if groups["req"] else 1.0
        o=mean(groups["opt"]) if groups["opt"] else 0.0; n=mean(groups["neg"]) if groups["neg"] else 0.0
        axis_scores[axis]=r*((1-eta_o)+eta_o*o)*(1-eta_n*n)
        components[axis]={"required":r,"optional":o,"negative":n,"score":axis_scores[axis]}
    denom=sum(profile.weights[x] for x in active)
    score=sum(profile.weights[x]/denom*axis_scores[x] for x in active) if denom else 0.0
    if not 0 <= score <= 1:
        raise AssertionError("alignment score escaped [0,1]")
    normalized_weights={x:profile.weights[x]/denom for x in active} if denom else {}
    return score,{"axis_scores":axis_scores,"axis_components":components,"normalized_weights":normalized_weights,"matches":[{"predicate":r.predicate,"score":s} for r,s in matches]}
