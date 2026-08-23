from __future__ import annotations

from .models import Axis, CapabilityProfile, Priority, RequirementProfile


SUPPORTED_VALUE_TYPES = (str, tuple, bool)


def validate_requirement_profile(
    profile: RequirementProfile, defined_predicates: set[str]
) -> RequirementProfile:
    errors: list[str] = []
    if not profile.requirements:
        errors.append("requirement profile must not be empty")
    for requirement in profile.requirements:
        if requirement.predicate not in defined_predicates:
            errors.append(f"undefined predicate: {requirement.predicate}")
        if not isinstance(requirement.axis, Axis):
            errors.append(f"invalid axis: {requirement.axis}")
        if requirement.priority not in (Priority.REQUIRED, Priority.OPTIONAL):
            errors.append(f"invalid priority: {requirement.priority}")
        if not isinstance(requirement.expected_value, SUPPORTED_VALUE_TYPES):
            errors.append(f"unsupported value type: {requirement.requirement_id}")
    if not any(requirement.axis is not Axis.CONTENT for requirement in profile.requirements):
        errors.append("at least one non-topical operational requirement is required")
    return RequirementProfile(
        action=profile.action,
        requirements=profile.requirements,
        validation_status="invalid" if errors else "valid",
        validation_errors=tuple(errors),
    )


def validate_capability_profile(profile: CapabilityProfile) -> CapabilityProfile:
    errors: list[str] = []
    for capability in profile.capabilities:
        if not capability.predicate:
            errors.append(f"missing predicate: {capability.capability_id}")
        if not capability.source_element or not capability.provenance:
            errors.append(f"missing provenance: {capability.capability_id}")
        if not 0.0 <= capability.confidence <= 1.0:
            errors.append(f"invalid confidence: {capability.capability_id}")
    return CapabilityProfile(
        table_id=profile.table_id,
        capabilities=profile.capabilities,
        validation_status="invalid" if errors else "valid",
        validation_errors=tuple(errors),
    )
