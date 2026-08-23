"""Canonical enumerations shared across pipeline stages."""

from enum import Enum


class StringEnum(str, Enum):
    def __str__(self) -> str:
        return self.value


class Axis(StringEnum):
    CONTENT = "content"
    STRUCTURE = "structure"
    ANALYSIS = "analysis"
    SCOPE = "scope"
    RELATION = "relation"
    QUALITY = "quality"


class ActionType(StringEnum):
    COMPARE = "compare"
    AGGREGATE = "aggregate"
    PREDICT = "predict"
    EXPLAIN = "explain"
    MONITOR = "monitor"


class RequirementCategory(StringEnum):
    REQUIRED = "required"
    OPTIONAL = "optional"
    NEGATIVE = "negative"


class EvidenceState(StringEnum):
    SATISFIED = "satisfied"
    PARTIALLY_SATISFIED = "partially_satisfied"
    UNKNOWN = "unknown"
    CONTRADICTED = "contradicted"
    NOT_APPLICABLE = "not_applicable"


class FeasibilityPolicy(StringEnum):
    HARD = "hard"
    SOFT = "soft"
    LEXICOGRAPHIC = "lexicographic"


class PipelineStatus(StringEnum):
    SUCCESS = "success"
    UNSUPPORTED_ACTION_FALLBACK = "unsupported_action_fallback"
    GROUNDING_FAILURE_FALLBACK = "grounding_failure_fallback"
    INVALID_INPUT = "invalid_input"
