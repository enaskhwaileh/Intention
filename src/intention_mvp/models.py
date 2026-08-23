from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any


class Axis(str, Enum):
    CONTENT = "content"
    STRUCTURE = "structure"
    ANALYSIS = "analysis"
    SCOPE = "scope"
    RELATION = "relation"
    QUALITY = "quality"


class Priority(str, Enum):
    REQUIRED = "required"
    OPTIONAL = "optional"


@dataclass(frozen=True)
class QueryProfile:
    original_input: str
    topic: str
    entities: tuple[str, ...]
    attributes: tuple[str, ...]
    constraints: dict[str, str]
    retrieval_query: str


@dataclass(frozen=True)
class GroundedAction:
    action_type: str
    arguments: dict[str, Any]
    confidence: float
    provenance: str


@dataclass(frozen=True)
class Requirement:
    requirement_id: str
    action_type: str
    axis: Axis
    predicate: str
    expected_value: str | tuple[str, ...] | bool
    priority: Priority
    weight: float
    threshold: float
    confidence: float
    source: str


@dataclass(frozen=True)
class RequirementProfile:
    action: GroundedAction
    requirements: tuple[Requirement, ...]
    validation_status: str
    validation_errors: tuple[str, ...] = ()


@dataclass(frozen=True)
class Capability:
    capability_id: str
    table_id: str
    axis: Axis
    predicate: str
    value: str | tuple[str, ...] | bool
    source_element: str
    confidence: float
    provenance: str


@dataclass(frozen=True)
class CapabilityProfile:
    table_id: str
    capabilities: tuple[Capability, ...]
    validation_status: str
    validation_errors: tuple[str, ...] = ()


@dataclass(frozen=True)
class RequirementMatch:
    requirement_id: str
    capability_id: str | None
    match_score: float
    matching_components: dict[str, float]
    provenance: str | None


@dataclass(frozen=True)
class TableRankingResult:
    table_id: str
    relevance_score: float
    alignment_score: float
    usefulness_score: float
    required_evidence_passed: bool
    matched_requirements: tuple[RequirementMatch, ...]
    missing_requirements: tuple[str, ...]
    explanation: dict[str, Any]


@dataclass(frozen=True)
class PipelineResult:
    query_profile: QueryProfile
    grounded_action: GroundedAction
    requirement_profile: RequirementProfile | None
    ranked_tables: tuple[TableRankingResult, ...]
    status: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
