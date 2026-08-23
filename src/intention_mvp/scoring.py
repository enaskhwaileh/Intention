from __future__ import annotations

from .config import load_scoring_config
from .matching import best_match
from .models import (
    CapabilityProfile,
    Priority,
    Requirement,
    RequirementMatch,
    RequirementProfile,
    TableRankingResult,
)


def rank_with_action(
    profile: RequirementProfile,
    capability_profiles: tuple[CapabilityProfile, ...],
    relevance_scores: dict[str, float],
) -> tuple[TableRankingResult, ...]:
    config = load_scoring_config()
    results = [
        _score_table(profile, capability, relevance_scores[capability.table_id], config)
        for capability in capability_profiles
    ]
    return tuple(sorted(results, key=lambda result: (-result.usefulness_score, result.table_id)))


def relevance_only_ranking(
    action_type: str,
    capability_profiles: tuple[CapabilityProfile, ...],
    relevance_scores: dict[str, float],
) -> tuple[TableRankingResult, ...]:
    results = []
    for profile in capability_profiles:
        relevance = relevance_scores[profile.table_id]
        explanation = {
            "grounded_action": action_type,
            "fallback": "relevance-only ranking",
            "topical_relevance_score": relevance,
            "satisfied_requirements": [],
            "partially_satisfied_requirements": [],
            "missing_requirements": [],
        }
        results.append(
            TableRankingResult(
                profile.table_id, relevance, 0.0, relevance, False, (), (), explanation
            )
        )
    return tuple(sorted(results, key=lambda result: (-result.usefulness_score, result.table_id)))


def _score_table(
    profile: RequirementProfile,
    capabilities: CapabilityProfile,
    relevance: float,
    config: dict,
) -> TableRankingResult:
    pairs = [
        (requirement, best_match(requirement, capabilities.capabilities))
        for requirement in profile.requirements
    ]
    required = [(req, match) for req, match in pairs if req.priority is Priority.REQUIRED]
    optional = [(req, match) for req, match in pairs if req.priority is Priority.OPTIONAL]
    required_score = _weighted_average(required)
    optional_score = _weighted_average(optional)
    if optional:
        alignment = (
            config["alignment"]["required_weight"] * required_score
            + config["alignment"]["optional_weight"] * optional_score
        )
    else:
        alignment = required_score
    gate = all(match.match_score >= req.threshold for req, match in required)
    usefulness = (
        config["usefulness"]["relevance_weight"] * relevance
        + config["usefulness"]["alignment_weight"] * alignment
    )
    demotion_reason = None
    if not gate:
        usefulness *= config["required_gate"]["demotion_multiplier"]
        demotion_reason = "one or more required requirements are below threshold"
    matches = tuple(match for _, match in pairs)
    missing = tuple(
        req.requirement_id for req, match in required if match.match_score == 0.0
    )
    satisfied = [_trace(req, match) for req, match in pairs if match.match_score >= req.threshold]
    partial = [
        _trace(req, match)
        for req, match in pairs
        if 0.0 < match.match_score < req.threshold
    ]
    explanation = {
        "topical_relevance_score": relevance,
        "grounded_action": profile.action.action_type,
        "alignment_score": round(alignment, 6),
        "usefulness_score": round(usefulness, 6),
        "required_evidence_passed": gate,
        "satisfied_requirements": satisfied,
        "partially_satisfied_requirements": partial,
        "missing_requirements": list(missing),
        "demotion_reason": demotion_reason,
    }
    return TableRankingResult(
        capabilities.table_id,
        relevance,
        round(alignment, 6),
        round(usefulness, 6),
        gate,
        matches,
        missing,
        explanation,
    )


def _weighted_average(
    pairs: list[tuple[Requirement, RequirementMatch]],
) -> float:
    if not pairs:
        return 0.0
    denominator = sum(requirement.weight for requirement, _ in pairs)
    return sum(
        requirement.weight * match.match_score for requirement, match in pairs
    ) / denominator


def _trace(requirement: Requirement, match: RequirementMatch) -> dict:
    return {
        "requirement_id": requirement.requirement_id,
        "predicate": requirement.predicate,
        "score": match.match_score,
        "threshold": requirement.threshold,
        "capability_id": match.capability_id,
        "provenance": match.provenance,
        "components": match.matching_components,
    }
