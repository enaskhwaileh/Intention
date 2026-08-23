import pytest

from intention.domain.enums import ActionType, Axis, RequirementCategory
from intention.domain.errors import RegistryValidationError
from intention.domain.models import (
    ActionArguments,
    CapabilityProfile,
    EvidenceProvenance,
    GroundedAction,
    IntendedAction,
    Requirement,
    RequirementProfile,
    TableCapability,
)
from intention.knowledge import load_action_registry, load_predicate_registry
from intention.knowledge.validation import validate_capability_profile, validate_requirement_profile


def test_requirement_profile_references_registered_predicates():
    grounded = GroundedAction(
        IntendedAction(ActionType.COMPARE, "compare", True),
        ActionArguments({"measure": "rate", "comparison_dimension": "country"}),
        1.0,
        "test",
    )
    requirement = Requirement(
        "compare.measure",
        ActionType.COMPARE,
        "content.comparable_measure.v1",
        RequirementCategory.REQUIRED,
        "rate",
        1.0,
    )
    validate_requirement_profile(
        RequirementProfile(grounded, "1.0.0", (requirement,)),
        load_action_registry(),
        load_predicate_registry(),
    )


def test_capability_axis_must_match_registered_predicate():
    capability = TableCapability(
        "T.1",
        "T",
        "content.comparable_measure.v1",
        Axis.QUALITY,
        "rate",
        1.0,
        EvidenceProvenance("rate", "test", "1.0.0"),
    )
    with pytest.raises(RegistryValidationError, match="axis mismatch"):
        validate_capability_profile(
            CapabilityProfile("T", "1.0.0", (capability,)), load_predicate_registry()
        )
