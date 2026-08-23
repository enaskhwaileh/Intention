from __future__ import annotations

from .models import Capability, Requirement, RequirementMatch


INCOMPATIBLE_PREDICATES = {
    ("provides_measure", "logistics_measure"),
    ("has_prediction_target", "logistics_measure"),
    ("contains_observed_outcomes", "logistics_measure"),
}


def match_requirement(requirement: Requirement, capability: Capability) -> RequirementMatch:
    predicate = _predicate_compatibility(requirement, capability)
    uses_special_compatibility = requirement.predicate in {
        "covers_geographic_scope",
        "has_compatible_granularity",
        "has_instance_level_rows",
    }
    value = (
        1.0
        if uses_special_compatibility
        else _value_compatibility(requirement.expected_value, capability.value)
    )
    scope = _scope_compatibility(requirement, capability)
    granularity = _granularity_compatibility(requirement, capability)
    components = {
        "predicate_compatibility": predicate,
        "value_compatibility": value,
        "scope_compatibility": scope,
        "granularity_compatibility": granularity,
        "requirement_confidence": requirement.confidence,
        "capability_confidence": capability.confidence,
    }
    score = 1.0
    for component in components.values():
        score *= component
    return RequirementMatch(
        requirement.requirement_id,
        capability.capability_id,
        round(score, 6),
        components,
        capability.provenance,
    )


def best_match(
    requirement: Requirement, capabilities: tuple[Capability, ...]
) -> RequirementMatch:
    candidates = [
        match_requirement(requirement, capability)
        for capability in capabilities
        if capability.axis == requirement.axis
    ]
    if not candidates:
        return RequirementMatch(
            requirement.requirement_id,
            None,
            0.0,
            {"predicate_compatibility": 0.0},
            None,
        )
    return max(candidates, key=lambda match: match.match_score)


def _predicate_compatibility(requirement: Requirement, capability: Capability) -> float:
    if (requirement.predicate, capability.predicate) in INCOMPATIBLE_PREDICATES:
        return 0.0
    return 1.0 if requirement.predicate == capability.predicate else 0.0


def _value_compatibility(
    expected: str | tuple[str, ...] | bool,
    actual: str | tuple[str, ...] | bool,
) -> float:
    if expected == actual:
        return 1.0
    expected_values = {expected} if isinstance(expected, (str, bool)) else set(expected)
    actual_values = {actual} if isinstance(actual, (str, bool)) else set(actual)
    if expected_values <= actual_values:
        return 1.0
    overlap = expected_values & actual_values
    if overlap:
        return len(overlap) / len(expected_values)
    if isinstance(expected, str) and isinstance(actual, str):
        if expected in actual or actual in expected:
            return 0.75
    return 0.0


def _scope_compatibility(requirement: Requirement, capability: Capability) -> float:
    if requirement.predicate != "covers_geographic_scope":
        return 1.0
    return _value_compatibility(requirement.expected_value, capability.value)


def _granularity_compatibility(
    requirement: Requirement, capability: Capability
) -> float:
    if requirement.predicate not in {"has_compatible_granularity", "has_instance_level_rows"}:
        return 1.0
    return _value_compatibility(requirement.expected_value, capability.value)
