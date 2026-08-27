from __future__ import annotations
import re
from datetime import date
from typing import Any

def norm(v: Any) -> str: return " ".join(re.findall(r"[a-z0-9]+", str(v).lower()))
def match_value(kind: str, expected: Any, observed: Any) -> float:
    if kind == "existential": return float(expected == "*" and observed not in (None,"",(),[]))
    if kind == "exact": return float(expected == observed)
    if kind == "normalized": return float(norm(expected) == norm(observed))
    if kind == "semantic":
        a,b=set(norm(expected).split()),set(norm(observed).split()); return len(a&b)/len(a|b) if a|b else 0.0
    if kind == "numerical":
        try: return float(float(observed) <= float(expected))
        except (TypeError,ValueError): return 0.0
    if kind == "set_containment":
        need={norm(v) for v in (expected if isinstance(expected,(list,tuple,set)) else [expected])}; have={norm(v) for v in (observed if isinstance(observed,(list,tuple,set)) else [observed])}; return float(need <= have)
    if kind == "interval":
        try:
            a,b=map(str,expected); c,d=map(str,observed); overlap=max(a,c)<=min(b,d); contained=c<=a and b<=d
            return 1.0 if contained else .5 if overlap else 0.0
        except (TypeError,ValueError): return 0.0
    if kind == "granularity":
        order={"event":0,"day":1,"week":2,"month":3,"quarter":4,"year":5}; a,b=norm(expected),norm(observed)
        return 1.0 if a==b else .5 if a in order and b in order and abs(order[a]-order[b])==1 else 0.0
    raise ValueError(f"unknown matching rule: {kind}")
