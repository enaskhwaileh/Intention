from __future__ import annotations

from .loader import (
    ground_action,
    load_capability_profiles,
    load_query_profile,
    load_relevance_scores,
    load_requirement_profile,
)
from .models import PipelineResult
from .scoring import rank_with_action, relevance_only_ranking


def run_pipeline(action_type: str) -> PipelineResult:
    query = load_query_profile()
    action = ground_action(action_type)
    capabilities = load_capability_profiles()
    relevance = load_relevance_scores()
    requirements = load_requirement_profile(action)
    if requirements is None:
        return PipelineResult(
            query,
            action,
            None,
            relevance_only_ranking(action_type, capabilities, relevance),
            "UnsupportedActionFallback",
        )
    if requirements.validation_status != "valid":
        return PipelineResult(
            query,
            action,
            requirements,
            relevance_only_ranking(action_type, capabilities, relevance),
            "InvalidRequirementProfileFallback",
        )
    return PipelineResult(
        query,
        action,
        requirements,
        rank_with_action(requirements, capabilities, relevance),
        "Success",
    )
