from __future__ import annotations
import re
from typing import Any

def norm(v: Any) -> str: return " ".join(re.findall(r"[a-z0-9]+", str(v).lower()))
def match_value(kind: str, expected: Any, observed: Any, parameters: dict[str, Any] | None = None) -> float:
    parameters = parameters or {}
    if kind == "existential": return float(expected == "*" and observed not in (None,"",(),[]))
    if kind == "exact": return float(expected == observed)
    if kind == "normalized": return float(norm(expected) == norm(observed))
    if kind == "semantic":
        scorer = parameters.get("scorer")
        if not callable(scorer):
            raise RuntimeError("semantic compatibility requires an explicitly configured scorer")
        score = float(scorer(expected, observed))
        if not 0 <= score <= 1:
            raise ValueError("semantic scorer must return a value in [0,1]")
        return score
    if kind == "numerical":
        try:
            expected_number, observed_number = float(expected), float(observed)
        except (TypeError,ValueError): return 0.0
        operator = parameters.get("operator", "at_most")
        if operator == "at_most": return float(observed_number <= expected_number)
        if operator == "at_least": return float(observed_number >= expected_number)
        if operator == "equal": return float(observed_number == expected_number)
        raise ValueError(f"unknown numerical operator: {operator}")
    if kind == "set_containment":
        need={norm(v) for v in (expected if isinstance(expected,(list,tuple,set)) else [expected])}; have={norm(v) for v in (observed if isinstance(observed,(list,tuple,set)) else [observed])}; return float(need <= have)
    if kind == "interval":
        try:
            a,b=map(str,expected); c,d=map(str,observed)
        except (TypeError,ValueError): return 0.0
        if a > b or c > d: return 0.0
        overlap=max(a,c)<=min(b,d); contained=c<=a and b<=d
        mode = parameters.get("mode", "containment_or_overlap")
        if mode == "containment": return float(contained)
        if mode == "overlap": return float(overlap)
        if mode == "containment_or_overlap": return 1.0 if contained else .5 if overlap else 0.0
        raise ValueError(f"unknown interval mode: {mode}")
    if kind == "granularity":
        if expected == "*": return float(observed not in (None,"",(),[],{}))
        if isinstance(observed,dict):
            labels=[observed.get(key) for key in ("kind","entity_type","description") if observed.get(key)]
            return float(norm(expected) in {norm(label) for label in labels})
        order={"event":0,"day":1,"week":2,"month":3,"quarter":4,"year":5}; a,b=norm(expected),norm(observed)
        return 1.0 if a==b else .5 if a in order and b in order and abs(order[a]-order[b])==1 else 0.0
    raise ValueError(f"unknown matching rule: {kind}")
