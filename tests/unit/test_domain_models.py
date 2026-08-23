import json

import pytest

from intention.domain.enums import ActionType, Axis, EvidenceState, RequirementCategory
from intention.domain.errors import ContractValidationError
from intention.domain.models import (
    ActionArguments,
    CapabilityProfile,
    EvidenceProvenance,
    GroundedAction,
    IntendedAction,
    OperationalPredicate,
    QueryProfile,
    Requirement,
    RequirementMatch,
    RequirementProfile,
    TableCapability,
)


def supported_action() -> GroundedAction:
    return GroundedAction(
        IntendedAction(ActionType.COMPARE, "compare", True),
        ActionArguments({"measure": "rate", "comparison_dimension": "country"}),
        1.0,
        "deterministic test",
    )


def test_confidence_values_are_bounded():
    with pytest.raises(ContractValidationError, match="between 0 and 1"):
        GroundedAction(
            IntendedAction(ActionType.COMPARE, "compare", True),
            ActionArguments({}),
            1.1,
            "test",
        )


def test_supported_flag_agrees_with_canonical_action():
    with pytest.raises(ContractValidationError, match="must agree"):
        IntendedAction(None, "compare", True)


def test_profile_symbols_cannot_be_reversed():
    with pytest.raises(ContractValidationError, match=r"Psi\*\(I\)"):
        RequirementProfile(supported_action(), "1.0.0", (), symbol="Phi*(T)")
    provenance = EvidenceProvenance("column", "test", "1.0.0")
    capability = TableCapability(
        "T.1", "T", "content.comparable_measure.v1", Axis.CONTENT, "rate", 1.0, provenance
    )
    with pytest.raises(ContractValidationError, match=r"Phi\*\(T\)"):
        CapabilityProfile("T", "1.0.0", (capability,), symbol="Psi*(I)")


def test_predicate_identifier_major_version_matches_registry():
    with pytest.raises(ContractValidationError, match="major version"):
        OperationalPredicate(
            "content.measure.v2", "1.0.0", Axis.CONTENT, "measure", "text"
        )


def test_requirement_categories_are_explicit_and_serializable():
    requirement = Requirement(
        "compare.measure",
        ActionType.COMPARE,
        "content.comparable_measure.v1",
        RequirementCategory.REQUIRED,
        "rate",
        1.0,
    )
    profile = RequirementProfile(supported_action(), "1.0.0", (requirement,))
    assert profile.symbol == "Psi*(I)"
    assert json.loads(json.dumps(profile.to_dict()))["requirements"][0]["category"] == "required"


def test_duplicate_requirement_ids_are_rejected():
    requirement = Requirement(
        "duplicate",
        ActionType.COMPARE,
        "content.comparable_measure.v1",
        RequirementCategory.REQUIRED,
        "rate",
        1.0,
    )
    with pytest.raises(ContractValidationError, match="unique"):
        RequirementProfile(supported_action(), "1.0.0", (requirement, requirement))


def test_missing_and_contradicted_evidence_are_distinct():
    common = dict(
        requirement_id="compare.measure",
        predicate_id="content.comparable_measure.v1",
        category=RequirementCategory.REQUIRED,
        capability_id=None,
        expected_value="rate",
        observed_value=None,
        match_score=0.0,
        capability_confidence=None,
        provenance=None,
        explanation="test evidence state",
    )
    unknown = RequirementMatch(evidence_state=EvidenceState.UNKNOWN, **common)
    contradicted = RequirementMatch(evidence_state=EvidenceState.CONTRADICTED, **common)
    assert unknown.evidence_state is not contradicted.evidence_state


def test_query_constraints_must_be_serializable():
    with pytest.raises(ContractValidationError, match="JSON serializable"):
        QueryProfile("query", "query", constraints={"bad": object()})
