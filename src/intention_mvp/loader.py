from __future__ import annotations

from typing import Any

from .config import load_action_catalogue, load_vaccine_fixture
from .models import (
    Axis,
    Capability,
    CapabilityProfile,
    GroundedAction,
    Priority,
    QueryProfile,
    Requirement,
    RequirementProfile,
)
from .validation import validate_capability_profile, validate_requirement_profile


def load_query_profile() -> QueryProfile:
    raw = load_vaccine_fixture()["query"]
    return QueryProfile(
        original_input=raw["original_input"],
        topic=raw["topic"],
        entities=tuple(raw["entities"]),
        attributes=tuple(raw["attributes"]),
        constraints=raw["constraints"],
        retrieval_query=raw["retrieval_query"],
    )


def ground_action(action_type: str) -> GroundedAction:
    return GroundedAction(
        action_type=action_type,
        arguments={},
        confidence=1.0,
        provenance="manually supplied demo scenario",
    )


def load_requirement_profile(action: GroundedAction) -> RequirementProfile | None:
    catalogue = load_action_catalogue()
    raw_action = catalogue["actions"].get(action.action_type)
    if raw_action is None:
        return None
    requirements = tuple(
        Requirement(
            requirement_id=f"{action.action_type}.{raw['predicate']}",
            action_type=action.action_type,
            axis=Axis(raw["axis"]),
            predicate=raw["predicate"],
            expected_value=_normalise_value(raw["expected_value"]),
            priority=Priority(raw["priority"]),
            weight=float(raw["weight"]),
            threshold=float(raw["threshold"]),
            confidence=float(raw.get("confidence", 1.0)),
            source="configs/actions.json",
        )
        for raw in raw_action["requirements"]
    )
    unchecked = RequirementProfile(action, requirements, "unchecked")
    return validate_requirement_profile(unchecked, set(catalogue["predicates"]))


def load_capability_profiles() -> tuple[CapabilityProfile, ...]:
    tables = load_vaccine_fixture()["tables"]
    profiles: list[CapabilityProfile] = []
    for table_id, raw_table in tables.items():
        capabilities = tuple(
            Capability(
                capability_id=f"{table_id}.{index}",
                table_id=table_id,
                axis=Axis(raw["axis"]),
                predicate=raw["predicate"],
                value=_normalise_value(raw["value"]),
                source_element=raw["source_element"],
                confidence=float(raw.get("confidence", 1.0)),
                provenance=raw["provenance"],
            )
            for index, raw in enumerate(raw_table["capabilities"], start=1)
        )
        profiles.append(
            validate_capability_profile(
                CapabilityProfile(table_id, capabilities, "unchecked")
            )
        )
    return tuple(profiles)


def load_relevance_scores() -> dict[str, float]:
    return {
        table_id: float(table["relevance"])
        for table_id, table in load_vaccine_fixture()["tables"].items()
    }


def _normalise_value(value: Any) -> str | tuple[str, ...] | bool:
    return tuple(value) if isinstance(value, list) else value
