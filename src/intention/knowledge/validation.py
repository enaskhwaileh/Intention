"""Cross-contract validation against the canonical registries."""

from intention.domain.errors import RegistryValidationError
from intention.domain.models import CapabilityProfile, RequirementProfile

from .registry import ActionRegistry, PredicateRegistry


def validate_requirement_profile(
    profile: RequirementProfile,
    actions: ActionRegistry,
    predicates: PredicateRegistry,
) -> None:
    canonical = profile.action.intended_action.canonical_action
    if canonical is None:
        raise RegistryValidationError("unsupported actions cannot have a requirement profile")
    actions.require(canonical)
    for requirement in profile.requirements:
        predicates.require(requirement.predicate_id)
        if requirement.action is not canonical:
            raise RegistryValidationError("requirement action does not match grounded action")


def validate_capability_profile(profile: CapabilityProfile, predicates: PredicateRegistry) -> None:
    for capability in profile.capabilities:
        predicate = predicates.require(capability.predicate_id)
        if capability.axis is not predicate.axis:
            raise RegistryValidationError(
                f"axis mismatch for capability {capability.capability_id}"
            )
