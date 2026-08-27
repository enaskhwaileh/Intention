"""Normative five-axis pipeline records."""
from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class Provenance:
    source: str
    procedure: str
    detail: str = ""

@dataclass(frozen=True)
class Capability:
    predicate: str
    axis: str
    value: Any
    state: str
    confidence: float
    provenance: Provenance
    def __post_init__(self):
        if self.state not in {"observed", "estimated", "inferred"} or not 0 <= self.confidence <= 1:
            raise ValueError("invalid capability state or confidence")

@dataclass(frozen=True)
class Table:
    table_id: str
    title: str
    description: str
    rows: tuple[dict[str, Any], ...]
    metadata: dict[str, Any]

@dataclass(frozen=True)
class Grounding:
    action: str
    arguments: dict[str, Any]

@dataclass(frozen=True)
class Interpretation:
    topical_query: str
    grounding: Grounding | None
    provenance: tuple[tuple[int, int], ...]
    raw_output: dict[str, Any]

@dataclass(frozen=True)
class Requirement:
    predicate: str
    axis: str
    expected: Any
    polarity: str
    provenance: str

@dataclass(frozen=True)
class RequirementProfile:
    action: str
    requirements: tuple[Requirement, ...]
    weights: dict[str, float]

@dataclass(frozen=True)
class RankedTable:
    table_id: str
    relevance: float
    alignment: float | None
    usefulness: float
