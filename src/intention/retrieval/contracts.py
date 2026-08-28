"""Provider-independent retrieval request and result records."""
from dataclasses import asdict,dataclass
import json
from pathlib import Path
from jsonschema import Draft202012Validator

INPUT_SCOPES={"topical_only","full_input_baseline"}
FAILURE_CODES={"unavailable","invalid_request","serialization_error","provider_error"}
RETRIEVAL_RESULT_SCHEMA=json.loads((Path(__file__).resolve().parents[3]/"configs/retrieval/result_schema.json").read_text())
Draft202012Validator.check_schema(RETRIEVAL_RESULT_SCHEMA)
RETRIEVAL_RESULT_VALIDATOR=Draft202012Validator(RETRIEVAL_RESULT_SCHEMA)

@dataclass(frozen=True)
class RetrievalRequest:
    query: str
    k: int
    input_scope: str = "topical_only"
    def __post_init__(self):
        if not self.query.strip() or not isinstance(self.k,int) or isinstance(self.k,bool) or self.k<=0:
            raise ValueError("retrieval request requires a query and positive integer k")
        if self.input_scope not in INPUT_SCOPES:
            raise ValueError("unknown retrieval input scope")

@dataclass(frozen=True)
class RetrieverIdentity:
    name: str
    model: str
    checkpoint_revision: str
    adapter_revision: str
    serialization_id: str
    serialization_version: str
    input_scope: str
    registry_version: str
    registry_hash: str
    config_hash: str
    def __post_init__(self):
        fields=(self.name,self.model,self.checkpoint_revision,self.adapter_revision,self.serialization_id,self.serialization_version,self.registry_version,self.registry_hash,self.config_hash)
        if not all(isinstance(value,str) and value for value in fields) or any(len(value)!=64 for value in (self.registry_hash,self.config_hash)):
            raise ValueError("retriever identity fields are required")
        if self.input_scope not in INPUT_SCOPES:
            raise ValueError("invalid retriever input scope")

@dataclass(frozen=True)
class RetrievalCandidate:
    table_id: str
    raw_score: float
    relevance: float
    rank: int
    def __post_init__(self):
        if not self.table_id.strip() or not isinstance(self.rank,int) or isinstance(self.rank,bool) or self.rank<=0:
            raise ValueError("invalid retrieval candidate identity or rank")
        if not isinstance(self.raw_score,(int,float)) or isinstance(self.raw_score,bool) or not isinstance(self.relevance,(int,float)) or isinstance(self.relevance,bool) or not 0<=self.relevance<=1:
            raise ValueError("retrieval relevance must be normalized to [0,1]")

@dataclass(frozen=True)
class ScoreNormalization:
    normalization_id: str
    method: str
    version: str
    fit_scope: str
    config_hash: str
    def __post_init__(self):
        if not all(isinstance(value,str) and value for value in (self.normalization_id,self.method,self.version,self.fit_scope)) or len(self.config_hash)!=64:
            raise ValueError("invalid score normalization provenance")

@dataclass(frozen=True)
class RetrievalTiming:
    serialization_ms: float
    inference_ms: float
    total_ms: float
    clock: str
    def __post_init__(self):
        if not self.clock.strip() or any(not isinstance(value,(int,float)) or isinstance(value,bool) or value<0 for value in (self.serialization_ms,self.inference_ms,self.total_ms)):
            raise ValueError("invalid retrieval timing")
        if self.total_ms+1e-9 < self.serialization_ms+self.inference_ms:
            raise ValueError("total retrieval time cannot be smaller than its components")

@dataclass(frozen=True)
class RetrievalFailure:
    code: str
    message: str
    retryable: bool
    def __post_init__(self):
        if self.code not in FAILURE_CODES or not self.message.strip() or not isinstance(self.retryable,bool):
            raise ValueError("invalid retrieval failure")

@dataclass(frozen=True)
class RetrievalResult:
    status: str
    identity: RetrieverIdentity
    timing: RetrievalTiming
    normalization: ScoreNormalization
    candidates: tuple[RetrievalCandidate,...] = ()
    failure: RetrievalFailure|None = None
    def __post_init__(self):
        if self.status not in {"success","failure"}:
            raise ValueError("invalid retrieval status")
        if (self.status=="success") != (self.failure is None):
            raise ValueError("retrieval failure state is inconsistent")
        if self.status=="failure" and self.candidates:
            raise ValueError("failed retrieval cannot expose candidates")
        if tuple(candidate.rank for candidate in self.candidates)!=tuple(range(1,len(self.candidates)+1)):
            raise ValueError("candidate ranks must be contiguous and one-based")
        if len({candidate.table_id for candidate in self.candidates})!=len(self.candidates):
            raise ValueError("retrieval candidates must be unique")

def retrieval_result_dict(result: RetrievalResult) -> dict:
    payload=json.loads(json.dumps(asdict(result)))
    errors=sorted(RETRIEVAL_RESULT_VALIDATOR.iter_errors(payload),key=lambda error:tuple(map(str,error.absolute_path)))
    if errors: raise ValueError(f"retrieval result violates JSON Schema: {errors[0].message}")
    return payload
