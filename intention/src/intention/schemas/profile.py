from dataclasses import dataclass


@dataclass(frozen=True)
class OperationalProfile:
    input_id: str
    intention_id: str
    profile_type: str
    entities: list[str]
    confidence: float
