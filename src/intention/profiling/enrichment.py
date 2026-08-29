from abc import ABC,abstractmethod
from dataclasses import dataclass

ALLOWED_SEMANTIC_ENRICHMENTS={"has_field","numeric_measure","grouping_field","row_granularity"}

@dataclass(frozen=True)
class SemanticEnrichment:
    predicate:str; axis:str; value:object; state:str; confidence:float; model_identity:str; prompt_hash:str; schema_hash:str; evidence:tuple[str,...]; source_fields:tuple[str,...]
    def __post_init__(self):
        if self.predicate not in ALLOWED_SEMANTIC_ENRICHMENTS or self.state!="inferred" or not 0<=self.confidence<=1 or not self.model_identity or len(self.prompt_hash)!=64 or len(self.schema_hash)!=64 or not self.evidence or not self.source_fields: raise ValueError("invalid semantic profiler enrichment")

class SemanticProfilerEnricher(ABC):
    @abstractmethod
    def enrich(self,table)->tuple[SemanticEnrichment,...]: ...

def merge_enrichments(observed,enrichments):
    observed_predicates={capability.predicate for capability in observed}
    accepted=tuple(item for item in enrichments if item.predicate not in observed_predicates)
    rejected=tuple(item for item in enrichments if item.predicate in observed_predicates)
    return {"observed":tuple(observed),"inferred":accepted,"rejected_overwrites":rejected}
