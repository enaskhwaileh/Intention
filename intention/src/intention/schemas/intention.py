from dataclasses import dataclass


@dataclass(frozen=True)
class RawIntention:
    input_id: str
    intention_id: str
    label: str
    confidence: float
