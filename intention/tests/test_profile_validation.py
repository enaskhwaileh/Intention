from pathlib import Path

from intention.iekl.graph_loader import load_iekl_graph
from intention.interpretation.intention_grounder import IntentionGrounder
from intention.interpretation.profile_instantiator import ProfileInstantiator
from intention.interpretation.validator import ProfileValidator
from intention.schemas.intention import RawIntention
from intention.schemas.profile import EvidenceRequirement, OperationalIntentionProfile


ROOT = Path(__file__).resolve().parents[1]


def _validator_and_graph():
    graph = load_iekl_graph(ROOT / "resources/iekl/intention_graph.yaml")
    return ProfileValidator(graph), graph


def test_valid_compare_profile_gets_valid_status():
    validator, graph = _validator_and_graph()
    grounded = IntentionGrounder(graph).ground(
        RawIntention(
            intent_phrase="compare vaccines",
            candidate_intention_type="compare",
            slots={},
        )
    )
    profile = ProfileInstantiator(graph).instantiate("q2", grounded)

    validated = validator.validate(profile)

    assert validated.validation_status == "valid"
    assert validated.validation_errors == []


def test_unsupported_predicate_gets_invalid_status():
    validator, _ = _validator_and_graph()
    profile = OperationalIntentionProfile(
        input_id="q_bad",
        intention_type="compare",
        goal="bad predicate test",
        required_evidence=[
            EvidenceRequirement(
                predicate="unsupported_predicate",
                axis="semantic",
                expected_evidence=[],
                reason="not in graph",
                priority="required",
                testable_from=["semantic"],
            )
        ],
        optional_evidence=[],
        negative_evidence=[],
    )

    validated = validator.validate(profile)

    assert validated.validation_status == "invalid"
    assert "unsupported predicate: unsupported_predicate" in validated.validation_errors


def test_empty_required_evidence_gets_invalid_status():
    validator, _ = _validator_and_graph()
    profile = OperationalIntentionProfile(
        input_id="q_empty",
        intention_type="compare",
        goal="empty required evidence test",
        required_evidence=[],
        optional_evidence=[],
        negative_evidence=[],
    )

    validated = validator.validate(profile)

    assert validated.validation_status == "invalid"
    assert "required_evidence must not be empty" in validated.validation_errors
