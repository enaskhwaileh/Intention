from dataclasses import replace

from intention_mvp.config import load_action_catalogue
from intention_mvp.loader import (
    ground_action,
    load_capability_profiles,
    load_query_profile,
    load_requirement_profile,
)
from intention_mvp.matching import best_match, match_requirement
from intention_mvp.models import CapabilityProfile, RequirementProfile
from intention_mvp.pipeline import run_pipeline
from intention_mvp.validation import validate_capability_profile, validate_requirement_profile


def ids(result) -> list[str]:
    return [row.table_id for row in result.ranked_tables]


def test_action_templates_load():
    catalogue = load_action_catalogue()
    assert set(catalogue["actions"]) == {"compare", "predict"}
    assert load_requirement_profile(ground_action("compare")).validation_status == "valid"


def test_requirement_profile_validation_rejects_undefined_predicate():
    profile = load_requirement_profile(ground_action("compare"))
    invalid_requirement = replace(profile.requirements[0], predicate="not_defined")
    candidate = RequirementProfile(
        profile.action, (invalid_requirement, *profile.requirements[1:]), "unchecked"
    )
    validated = validate_requirement_profile(
        candidate, set(load_action_catalogue()["predicates"])
    )
    assert validated.validation_status == "invalid"
    assert "undefined predicate: not_defined" in validated.validation_errors


def test_capability_profiles_validate_and_have_provenance():
    profiles = load_capability_profiles()
    assert all(profile.validation_status == "valid" for profile in profiles)
    assert all(
        capability.provenance and capability.source_element
        for profile in profiles
        for capability in profile.capabilities
    )


def test_capability_validation_rejects_missing_provenance():
    profile = load_capability_profiles()[0]
    broken = replace(profile.capabilities[0], provenance="")
    validated = validate_capability_profile(
        CapabilityProfile(profile.table_id, (broken,), "unchecked")
    )
    assert validated.validation_status == "invalid"


def test_exact_requirement_capability_match():
    requirement = load_requirement_profile(ground_action("compare")).requirements[0]
    capability = load_capability_profiles()[0].capabilities[0]
    match = match_requirement(requirement, capability)
    assert match.match_score == 1.0
    assert match.matching_components["value_compatibility"] == 1.0


def test_partial_value_match_is_transparent():
    requirement = load_requirement_profile(ground_action("compare")).requirements[0]
    patient_profile = next(p for p in load_capability_profiles() if p.table_id == "C")
    match = best_match(requirement, patient_profile.capabilities)
    assert 0.0 < match.match_score < 1.0
    assert match.matching_components["value_compatibility"] == 0.75


def test_missing_required_evidence_remains_explicit():
    logistics = next(row for row in run_pipeline("compare").ranked_tables if row.table_id == "D")
    assert logistics.required_evidence_passed is False
    assert logistics.missing_requirements
    assert logistics.explanation["missing_requirements"]


def test_compare_ranking():
    assert ids(run_pipeline("compare")) == ["B", "C", "A", "D"]


def test_predict_ranking():
    assert ids(run_pipeline("predict")) == ["C", "B", "A", "D"]


def test_same_query_and_candidates_change_ranking_by_action():
    compare = run_pipeline("compare")
    predict = run_pipeline("predict")
    assert compare.query_profile == predict.query_profile == load_query_profile()
    assert {row.table_id for row in compare.ranked_tables} == {
        row.table_id for row in predict.ranked_tables
    }
    assert ids(compare) != ids(predict)


def test_unsupported_action_falls_back_to_relevance():
    result = run_pipeline("explain")
    assert result.status == "UnsupportedActionFallback"
    assert ids(result) == ["A", "B", "C", "D"]


def test_explanation_is_provenance_grounded():
    result = run_pipeline("predict")
    for row in result.ranked_tables:
        assert "grounded_action" in row.explanation
        for trace in (
            row.explanation["satisfied_requirements"]
            + row.explanation["partially_satisfied_requirements"]
        ):
            assert trace["capability_id"]
            assert trace["provenance"]
            assert trace["components"]
