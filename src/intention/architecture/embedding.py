from abc import ABC,abstractmethod
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
import json,math,yaml

@dataclass(frozen=True)
class EmbeddingIdentity:
    provider: str; model: str; revision: str; tokenizer_revision: str|None
    dimension: int; normalization: str; similarity: str
    query_instruction: str|None; document_instruction: str|None
    maximum_input_length: int; truncation_policy: str; device: str; config_hash: str
    def __post_init__(self):
        if not all((self.provider,self.model,self.revision,self.normalization,self.similarity,self.truncation_policy,self.device)) or self.dimension<=0 or self.maximum_input_length<=0 or len(self.config_hash)!=64: raise ValueError("invalid embedding identity")

@dataclass(frozen=True)
class EmbeddingFailure:
    code: str; message: str; retryable: bool=False

@dataclass(frozen=True)
class EmbeddingResult:
    status: str; identity: EmbeddingIdentity; vectors: tuple[tuple[float,...],...]; elapsed_ms: float; failure: EmbeddingFailure|None=None
    def __post_init__(self):
        if self.status not in {"success","failure"} or (self.status=="success")!=(self.failure is None): raise ValueError("inconsistent embedding state")
        if not math.isfinite(self.elapsed_ms) or self.elapsed_ms<0: raise ValueError("invalid embedding timing")
        if self.status=="failure" and self.vectors: raise ValueError("failed embedding cannot expose vectors")
        if any(len(vector)!=self.identity.dimension or any(not math.isfinite(value) for value in vector) for vector in self.vectors): raise ValueError("invalid embedding vector")

class EmbeddingProvider(ABC):
    @property
    @abstractmethod
    def identity(self)->EmbeddingIdentity: ...
    @abstractmethod
    def encode_queries(self,texts:list[str])->EmbeddingResult: ...
    @abstractmethod
    def encode_documents(self,texts:list[str])->EmbeddingResult: ...
    def encode_query(self,text:str)->EmbeddingResult: return self.encode_queries([text])
    def encode_document(self,text:str)->EmbeddingResult: return self.encode_documents([text])

class UnavailableEmbeddingProvider(EmbeddingProvider):
    def __init__(self,identity,reason): self._identity=identity; self.reason=reason
    @property
    def identity(self): return self._identity
    def _failure(self): return EmbeddingResult("failure",self.identity,(),0,EmbeddingFailure("unavailable",self.reason))
    def encode_queries(self,texts): return self._failure()
    def encode_documents(self,texts): return self._failure()

@dataclass(frozen=True)
class EmbeddingRegistration:
    name: str; record: dict

@dataclass(frozen=True)
class EmbeddingRegistry:
    version: str; selection_status: str; primary_architecture: str; operational_smoke_encoder:str; models: dict[str,EmbeddingRegistration]; digest: str
    def require_available(self,name):
        if name not in self.models: raise KeyError(name)
        record=self.models[name].record
        if record["availability"]!="available": raise RuntimeError(f"embedding provider blocked: {record['failure_reason']}")
        return self.models[name]

def load_embedding_registry(path:Path|None=None)->EmbeddingRegistry:
    path=path or Path(__file__).resolve().parents[3]/"configs/architecture/embeddings.yaml"; raw=yaml.safe_load(path.read_text())
    if not isinstance(raw,dict) or set(raw)!={"version","selection_status","primary_architecture","operational_smoke_encoder","models"}: raise ValueError("invalid embedding registry")
    required={"category","provider","model","revision","source","license","dimensions","maximum_input_tokens","truncation_policy","query_mode","document_mode","query_instruction","document_instruction","similarity","normalization","requirement","hardware","approximate_cost","availability","failure_reason"}; optional={"tokenizer_revision","dimension_range","api_task_type_supported","title_handling","batch_semantics","api_limitations","operational_role"}
    models={}
    for name,record in raw["models"].items():
        if not required<=set(record) or set(record)-required-optional: raise ValueError(f"invalid embedding record: {name}")
        if record["availability"] not in {"available","blocked"} or (record["availability"]=="blocked")!=(bool(record["failure_reason"])): raise ValueError(f"invalid availability: {name}")
        if record["category"]!="lexical_reference" and (not isinstance(record["dimensions"],list) or not record["dimensions"] or any(not isinstance(value,int) or value<=0 for value in record["dimensions"])): raise ValueError(f"invalid dimensions: {name}")
        if not isinstance(record["hardware"],list) or not record["hardware"] or any(not isinstance(value,str) or not value for value in record["hardware"]): raise ValueError(f"invalid hardware requirement: {name}")
        models[name]=EmbeddingRegistration(name,record)
    digest=sha256(json.dumps(raw,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    if raw["operational_smoke_encoder"] not in models or models[raw["operational_smoke_encoder"]].record.get("operational_role")!="operational_smoke_encoder_not_final_primary": raise ValueError("invalid operational smoke encoder")
    return EmbeddingRegistry(raw["version"],raw["selection_status"],raw["primary_architecture"],raw["operational_smoke_encoder"],models,digest)
