"""Normative five-axis pipeline records."""
from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class Provenance:
    source: str
    procedure: str
    detail: str = ""
    def __post_init__(self):
        if not self.source.strip() or not self.procedure.strip():
            raise ValueError("provenance source and procedure must be non-empty")

@dataclass(frozen=True)
class Capability:
    predicate: str
    axis: str
    value: Any
    state: str
    confidence: float
    provenance: Provenance
    def __post_init__(self):
        if not self.predicate.strip() or not self.axis.strip() or self.value is None:
            raise ValueError("capability predicate, axis, and value are required")
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
    def __post_init__(self):
        if not self.action.strip():
            raise ValueError("grounded action must be non-empty")

@dataclass(frozen=True)
class Interpretation:
    topical_query: str
    grounding: Grounding | None
    provenance: tuple[tuple[int, int], ...]
    raw_output: dict[str, Any]
    def __post_init__(self):
        if not self.topical_query.strip():
            raise ValueError("topical query must be non-empty")

@dataclass(frozen=True)
class Requirement:
    predicate: str
    axis: str
    expected: Any
    polarity: str
    provenance: str
    def __post_init__(self):
        if not self.predicate.strip() or not self.axis.strip() or not self.provenance.strip():
            raise ValueError("requirement identifiers and provenance must be non-empty")
        if self.polarity not in {"req", "opt", "neg"} or self.expected is None:
            raise ValueError("invalid requirement polarity or expected value")

@dataclass(frozen=True)
class RequirementProfile:
    action: str
    requirements: tuple[Requirement, ...]
    weights: dict[str, float]
    def __post_init__(self):
        if not self.action.strip() or not self.requirements:
            raise ValueError("requirement profile must have an action and requirements")

@dataclass(frozen=True)
class RankedTable:
    table_id: str
    relevance: float
    alignment: float | None
    usefulness: float
    def __post_init__(self):
        values = (self.relevance, self.usefulness) if self.alignment is None else (self.relevance, self.alignment, self.usefulness)
        if not self.table_id.strip() or any(not 0 <= value <= 1 for value in values):
            raise ValueError("ranked table fields and scores are invalid")
