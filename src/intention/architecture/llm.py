from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
import json,yaml

@dataclass(frozen=True)
class LLMInterpreterRegistration:
    name:str; provider:str; model:str; revision:str; source:str; observed_date:str; structured_output:str; prompt_version:str; prompt_hash:str; schema_hash:str; parameters:dict; availability:str; failure_reason:str|None

@dataclass(frozen=True)
class LLMRegistry:
    version:str; providers:dict[str,LLMInterpreterRegistration]; digest:str
    def require_available(self,name):
        registration=self.providers[name]
        if registration.availability!="available": raise RuntimeError(f"LLM provider blocked: {registration.failure_reason}")
        return registration

def load_llm_registry(path:Path|None=None):
    root=Path(__file__).resolve().parents[3]; path=path or root/"configs/architecture/llm_registry.yaml"; raw=yaml.safe_load(path.read_text())
    if not isinstance(raw,dict) or set(raw)!={"version","prompt_version","providers"}: raise ValueError("invalid LLM registry")
    prompt_hash=sha256((root/"configs/architecture/interpreter_prompt.txt").read_bytes()).hexdigest(); schema_hash=sha256((root/"configs/interpretation/output_schema.json").read_bytes()).hexdigest(); providers={}
    required={"provider","model","revision","source","observed_date","structured_output","parameters","availability","failure_reason"}
    for name,item in raw["providers"].items():
        if set(item)!=required or item["availability"] not in {"available","blocked"} or (item["availability"]=="blocked")!=(bool(item["failure_reason"])): raise ValueError(f"invalid LLM registration: {name}")
        expected_parameters={"temperature","top_p","top_k","seed","thinking_level"}
        if set(item["parameters"])!=expected_parameters or any(set(value)!={"support","configured","provider_default"} for value in item["parameters"].values()): raise ValueError(f"invalid LLM parameter policy: {name}")
        providers[name]=LLMInterpreterRegistration(name,prompt_version=raw["prompt_version"],prompt_hash=prompt_hash,schema_hash=schema_hash,**item)
    digest=sha256(json.dumps(raw,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    return LLMRegistry(raw["version"],providers,digest)
