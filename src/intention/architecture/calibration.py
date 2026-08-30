from abc import ABC,abstractmethod
from dataclasses import dataclass
from hashlib import sha256
import json,math
from intention.retrieval.contracts import ScoreNormalization

class RelevanceCalibrator(ABC):
    @property
    @abstractmethod
    def normalization(self)->ScoreNormalization: ...
    @abstractmethod
    def transform(self,raw_scores:list[float])->list[float]: ...

@dataclass(frozen=True)
class SemanticScoreNormalization(ScoreNormalization):
    calibration_status:str="development_fit_pending"
    def __post_init__(self):
        super().__post_init__()
        if self.calibration_status not in {"development_fit_pending","development_fitted"}:raise ValueError("invalid semantic calibration status")

@dataclass(frozen=True)
class CosineEngineeringMapping(RelevanceCalibrator):
    """Label-free bounded mapping for plumbing, not final paper calibration."""
    version:str="1.0.0"
    @property
    def normalization(self):
        config={"method":"cosine_affine","formula":"(cosine+1)/2","fit_split":"none","calibration_status":"development_fit_pending"}
        digest=sha256(json.dumps(config,sort_keys=True,separators=(",",":")).encode()).hexdigest()
        return SemanticScoreNormalization("semantic_cosine_affine_engineering_v1","cosine_affine","1.0.0","no_labels_engineering_default",digest,"development_fit_pending")
    def transform(self,raw_scores):
        if any(not isinstance(score,(int,float)) or not math.isfinite(score) or not -1-1e-9<=score<=1+1e-9 for score in raw_scores): raise ValueError("cosine score outside finite [-1,1] range")
        return [min(1,max(0,(score+1)/2)) for score in raw_scores]
