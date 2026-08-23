"""Serializable validated contracts for the full research pipeline.

The models intentionally contain no profiling, retrieval, or ranking business
logic. They define stable stage boundaries for later phases.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Mapping

from .enums import (
    ActionType,
    Axis,
    EvidenceState,
    FeasibilityPolicy,
    PipelineStatus,
    RequirementCategory,
)
from .errors import ContractValidationError


JSONValue = str | int | float | bool | None | list["JSONValue"] | dict[str, "JSONValue"]


def _nonempty(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ContractValidationError(f"{field_name} must be a non-empty string")


def _bounded(value: float, field_name: str) -> None:
    if not 0.0 <= value <= 1.0:
        raise ContractValidationError(f"{field_name} must be between 0 and 1")


def _jsonable(value: Any, field_name: str) -> None:
    try:
        import json

        json.dumps(value, sort_keys=True)
    except (TypeError, ValueError) as exc:
        raise ContractValidationError(f"{field_name} must be JSON serializable") from exc


class SerializableContract:
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RawUserInput(SerializableContract):
    text: str
    request_id: str

    def __post_init__(self) -> None:
        _nonempty(self.text, "text")
        _nonempty(self.request_id, "request_id")


@dataclass(frozen=True)
class QueryProfile(SerializableContract):
    original_input: str
    topical_query: str
    entities: tuple[str, ...] = ()
    attributes: tuple[str, ...] = ()
    constraints: Mapping[str, JSONValue] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _nonempty(self.original_input, "original_input")
        _nonempty(self.topical_query, "topical_query")
        _jsonable(dict(self.constraints), "constraints")


@dataclass(frozen=True)
class IntendedAction(SerializableContract):
    canonical_action: ActionType | None
    surface_form: str
    supported: bool
    ambiguity: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _nonempty(self.surface_form, "surface_form")
        if self.supported != (self.canonical_action is not None):
            raise ContractValidationError("supported must agree with canonical_action")


@dataclass(frozen=True)
class ActionArguments(SerializableContract):
    values: Mapping[str, JSONValue]
    missing_required: tuple[str, ...] = ()
    conflicting: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _jsonable(dict(self.values), "action arguments")


@dataclass(frozen=True)
class GroundedAction(SerializableContract):
    intended_action: IntendedAction
    arguments: ActionArguments
    confidence: float
    provenance: str

    def __post_init__(self) -> None:
        _bounded(self.confidence, "confidence")
        _nonempty(self.provenance, "provenance")


@dataclass(frozen=True)
class OperationalPredicate(SerializableContract):
    predicate_id: str
    registry_version: str
    axis: Axis
    description: str
    value_kind: str

    def __post_init__(self) -> None:
        for name in ("predicate_id", "registry_version", "description", "value_kind"):
            _nonempty(getattr(self, name), name)
        if not self.predicate_id.endswith(f".v{self.registry_version.split('.')[0]}"):
            raise ContractValidationError("predicate ID major version must match registry version")


@dataclass(frozen=True)
class Requirement(SerializableContract):
    requirement_id: str
    action: ActionType
    predicate_id: str
    category: RequirementCategory
    expected_value: JSONValue
    weight: float
    operator: str = "equals"
    conditional: bool = False

    def __post_init__(self) -> None:
        _nonempty(self.requirement_id, "requirement_id")
        _nonempty(self.predicate_id, "predicate_id")
        _nonempty(self.operator, "operator")
        _bounded(self.weight, "weight")
        if self.weight == 0.0:
            raise ContractValidationError("weight must be greater than zero")
        _jsonable(self.expected_value, "expected_value")


@dataclass(frozen=True)
class RequirementProfile(SerializableContract):
    action: GroundedAction
    profile_version: str
    requirements: tuple[Requirement, ...]
    symbol: str = "Psi*(I)"

    def __post_init__(self) -> None:
        _nonempty(self.profile_version, "profile_version")
        if self.symbol != "Psi*(I)":
            raise ContractValidationError("action requirement profiles must use Psi*(I)")
        ids = [item.requirement_id for item in self.requirements]
        if len(ids) != len(set(ids)):
            raise ContractValidationError("requirement identifiers must be unique")


@dataclass(frozen=True)
class TableSource(SerializableContract):
    source_id: str
    uri: str
    license: str | None = None
    checksum: str | None = None

    def __post_init__(self) -> None:
        _nonempty(self.source_id, "source_id")
        _nonempty(self.uri, "uri")


@dataclass(frozen=True)
class TableColumn(SerializableContract):
    name: str
    inferred_type: str
    nullable: bool
    sample_values: tuple[JSONValue, ...] = ()

    def __post_init__(self) -> None:
        _nonempty(self.name, "name")
        _nonempty(self.inferred_type, "inferred_type")
        _jsonable(list(self.sample_values), "sample_values")


@dataclass(frozen=True)
class CanonicalTable(SerializableContract):
    table_id: str
    source: TableSource
    title: str
    description: str
    columns: tuple[TableColumn, ...]
    row_count: int

    def __post_init__(self) -> None:
        _nonempty(self.table_id, "table_id")
        if self.row_count < 0:
            raise ContractValidationError("row_count must be non-negative")
        names = [column.name for column in self.columns]
        if len(names) != len(set(names)):
            raise ContractValidationError("column names must be unique")


@dataclass(frozen=True)
class Observation(SerializableContract):
    observation_id: str
    values: Mapping[str, JSONValue]

    def __post_init__(self) -> None:
        _nonempty(self.observation_id, "observation_id")
        _jsonable(dict(self.values), "observation values")


@dataclass(frozen=True)
class EvidenceProvenance(SerializableContract):
    source_element: str
    derivation_method: str
    profiler_version: str
    source_statistic: JSONValue = None

    def __post_init__(self) -> None:
        for name in ("source_element", "derivation_method", "profiler_version"):
            _nonempty(getattr(self, name), name)
        _jsonable(self.source_statistic, "source_statistic")


@dataclass(frozen=True)
class TableCapability(SerializableContract):
    capability_id: str
    table_id: str
    predicate_id: str
    axis: Axis
    value: JSONValue
    confidence: float
    provenance: EvidenceProvenance

    def __post_init__(self) -> None:
        for name in ("capability_id", "table_id", "predicate_id"):
            _nonempty(getattr(self, name), name)
        _bounded(self.confidence, "confidence")
        _jsonable(self.value, "capability value")


@dataclass(frozen=True)
class CapabilityProfile(SerializableContract):
    table_id: str
    profile_version: str
    capabilities: tuple[TableCapability, ...]
    symbol: str = "Phi*(T)"

    def __post_init__(self) -> None:
        _nonempty(self.table_id, "table_id")
        _nonempty(self.profile_version, "profile_version")
        if self.symbol != "Phi*(T)":
            raise ContractValidationError("table capability profiles must use Phi*(T)")
        if any(item.table_id != self.table_id for item in self.capabilities):
            raise ContractValidationError("all capabilities must belong to the profile table")


@dataclass(frozen=True)
class RetrievalCandidate(SerializableContract):
    table_id: str
    raw_score: float
    normalized_score: float
    rank: int
    backend: str
    metadata: Mapping[str, JSONValue] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _nonempty(self.table_id, "table_id")
        _nonempty(self.backend, "backend")
        _bounded(self.normalized_score, "normalized_score")
        if self.rank < 1:
            raise ContractValidationError("rank must be at least one")
        _jsonable(dict(self.metadata), "retrieval metadata")


@dataclass(frozen=True)
class RequirementMatch(SerializableContract):
    requirement_id: str
    predicate_id: str
    category: RequirementCategory
    capability_id: str | None
    expected_value: JSONValue
    observed_value: JSONValue
    evidence_state: EvidenceState
    match_score: float
    capability_confidence: float | None
    provenance: EvidenceProvenance | None
    explanation: str

    def __post_init__(self) -> None:
        _bounded(self.match_score, "match_score")
        if self.capability_confidence is not None:
            _bounded(self.capability_confidence, "capability_confidence")
        _nonempty(self.explanation, "explanation")


@dataclass(frozen=True)
class FeasibilityDecision(SerializableContract):
    policy: FeasibilityPolicy
    feasible: bool
    missing_required: tuple[str, ...]
    contradicted_required: tuple[str, ...]
    multiplier: float = 1.0

    def __post_init__(self) -> None:
        _bounded(self.multiplier, "multiplier")


@dataclass(frozen=True)
class AlignmentResult(SerializableContract):
    table_id: str
    matches: tuple[RequirementMatch, ...]
    required_score: float
    optional_score: float
    negative_penalty: float
    coverage: float
    feasibility: FeasibilityDecision

    def __post_init__(self) -> None:
        for name in ("required_score", "optional_score", "negative_penalty", "coverage"):
            _bounded(getattr(self, name), name)


@dataclass(frozen=True)
class ExplanationTrace(SerializableContract):
    summary: str
    match_ids: tuple[str, ...]
    provenance_count: int

    def __post_init__(self) -> None:
        _nonempty(self.summary, "summary")
        if self.provenance_count < 0:
            raise ContractValidationError("provenance_count must be non-negative")


@dataclass(frozen=True)
class RankedTable(SerializableContract):
    table_id: str
    relevance_score: float
    alignment_score: float
    usefulness_score: float
    rank: int
    feasibility: FeasibilityDecision
    explanation: ExplanationTrace

    def __post_init__(self) -> None:
        for name in ("relevance_score", "alignment_score", "usefulness_score"):
            _bounded(getattr(self, name), name)
        if self.rank < 1:
            raise ContractValidationError("rank must be at least one")


@dataclass(frozen=True)
class PipelineTrace(SerializableContract):
    run_id: str
    status: PipelineStatus
    stages: Mapping[str, JSONValue]

    def __post_init__(self) -> None:
        _nonempty(self.run_id, "run_id")
        _jsonable(dict(self.stages), "stages")


@dataclass(frozen=True)
class BenchmarkJudgment(SerializableContract):
    query_id: str
    table_id: str
    action: ActionType
    topical_relevance: int
    action_suitability: int
    evidence_observability: int
    annotator_id: str

    def __post_init__(self) -> None:
        for name in ("query_id", "table_id", "annotator_id"):
            _nonempty(getattr(self, name), name)
        for name in ("topical_relevance", "action_suitability", "evidence_observability"):
            if getattr(self, name) not in range(4):
                raise ContractValidationError(f"{name} must be an integer from 0 to 3")


@dataclass(frozen=True)
class ExperimentRun(SerializableContract):
    run_id: str
    config_version: str
    code_commit: str
    benchmark_version: str
    random_seed: int
    metrics: Mapping[str, float]

    def __post_init__(self) -> None:
        for name in ("run_id", "config_version", "code_commit", "benchmark_version"):
            _nonempty(getattr(self, name), name)
        if self.random_seed < 0:
            raise ContractValidationError("random_seed must be non-negative")
        if any(not isinstance(value, (int, float)) for value in self.metrics.values()):
            raise ContractValidationError("metrics must be numeric")
