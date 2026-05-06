"""Dataclass models for deterministic dataset capability profiles."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class SemanticProfile:
    keywords: list[str] = field(default_factory=list)
    measure_terms: list[str] = field(default_factory=list)
    entity_candidates: dict[str, list[str]] = field(default_factory=dict)
    domain_hints: list[str] = field(default_factory=list)


@dataclass
class StructuralProfile:
    row_count: int
    column_count: int
    inferred_column_types: dict[str, str] = field(default_factory=dict)
    numeric_columns: list[str] = field(default_factory=list)
    categorical_columns: list[str] = field(default_factory=list)
    date_candidates: list[str] = field(default_factory=list)
    identifier_candidates: list[str] = field(default_factory=list)
    grouping_candidates: list[str] = field(default_factory=list)
    measure_candidates: list[str] = field(default_factory=list)


@dataclass
class CoverageProfile:
    categorical_coverage: dict[str, int] = field(default_factory=dict)
    top_values: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    numeric_ranges: dict[str, dict[str, float | None]] = field(default_factory=dict)
    temporal_ranges: dict[str, dict[str, str | None]] = field(default_factory=dict)
    geographic_columns: list[str] = field(default_factory=list)


@dataclass
class QualityProfile:
    missing_rate_per_column: dict[str, float] = field(default_factory=dict)
    duplicate_row_rate: float = 0.0
    unique_ratio_per_column: dict[str, float] = field(default_factory=dict)
    constant_columns: list[str] = field(default_factory=list)
    empty_string_rate_per_column: dict[str, float] = field(default_factory=dict)


@dataclass
class ActionAffordanceProfile:
    compare: str = "weak"
    aggregate: str = "weak"
    predict: str = "weak"
    join: str = "weak"
    explain: str = "weak"


@dataclass
class CapabilityProfile:
    table_id: str
    table_name: str
    semantic: SemanticProfile
    structural: StructuralProfile
    coverage: CoverageProfile
    quality: QualityProfile
    action_affordance: ActionAffordanceProfile
    metadata: dict[str, Any] = field(default_factory=dict)
