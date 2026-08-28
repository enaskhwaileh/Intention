"""Strict external retriever registry; unavailable systems never substitute."""
from dataclasses import dataclass
from pathlib import Path
import yaml
from .serialization import load_retrieval_policy

FIELDS={"role","kind","availability","implementation","model","checkpoint","revision","serialization","input_scope","prompt_instruction","embedding_dimension","hardware","dependencies","failure_reason"}

@dataclass(frozen=True)
class RetrieverRegistration:
    name: str
    role: str
    kind: str
    availability: str
    implementation: str|None
    model: str|None
    checkpoint: str|None
    revision: str|None
    serialization: str
    input_scope: str
    prompt_instruction: str|None
    embedding_dimension: int|None
    hardware: tuple[str,...]
    dependencies: tuple[str,...]
    failure_reason: str|None

@dataclass(frozen=True)
class RetrieverRegistry:
    version: str
    latency_fields: tuple[str,...]
    retrievers: dict[str,RetrieverRegistration]

def load_retriever_registry(path: Path|None=None) -> RetrieverRegistry:
    path=path or Path(__file__).resolve().parents[3]/"configs/baselines/registry.yaml"
    raw=yaml.safe_load(path.read_text())
    if not isinstance(raw,dict) or set(raw)!={"version","latency_fields","retrievers"} or raw["latency_fields"]!=["serialization_ms","inference_ms","total_ms"]: raise ValueError("invalid retriever registry root")
    registrations={}; policy=load_retrieval_policy()
    for name,item in raw["retrievers"].items():
        if not isinstance(item,dict) or set(item)!=FIELDS or item["role"] not in {"first_stage","reranker"} or item["kind"] not in {"deterministic","external"} or item["availability"] not in {"available","blocked"} or item["input_scope"] not in policy.input_scopes or item["serialization"] not in policy.serializations: raise ValueError(f"invalid retriever registration: {name}")
        nullable_strings=("implementation","model","checkpoint","revision","prompt_instruction","failure_reason")
        if any(item[key] is not None and not isinstance(item[key],str) for key in nullable_strings) or not isinstance(item["hardware"],list) or not all(isinstance(value,str) and value for value in item["hardware"]) or not isinstance(item["dependencies"],list) or not all(isinstance(value,str) and value for value in item["dependencies"]) or item["embedding_dimension"] is not None and (not isinstance(item["embedding_dimension"],int) or item["embedding_dimension"]<=0): raise ValueError(f"invalid retriever registration: {name}")
        if item["input_scope"]=="full_input_baseline" and "FullInput" not in name: raise ValueError(f"full-input retriever must be explicitly named: {name}")
        if item["availability"]=="available" and (not item["implementation"] or not item["model"] or not item["revision"] or item["failure_reason"] is not None): raise ValueError(f"incomplete available retriever: {name}")
        if item["kind"]=="external" and item["availability"]=="available" and (not item["checkpoint"] or not item["hardware"] or not item["dependencies"]): raise ValueError(f"incomplete available external retriever: {name}")
        if item["availability"]=="blocked" and (not item["failure_reason"] or item["implementation"] is not None): raise ValueError(f"blocked retriever must fail closed: {name}")
        registrations[name]=RetrieverRegistration(name,hardware=tuple(item["hardware"]),dependencies=tuple(item["dependencies"]),**{key:value for key,value in item.items() if key not in {"hardware","dependencies"}})
    return RetrieverRegistry(raw["version"],tuple(raw["latency_fields"]),registrations)
