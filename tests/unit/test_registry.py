from pathlib import Path

import pytest

from intention.domain.enums import ActionType, Axis, RequirementCategory
from intention.domain.errors import RegistryValidationError
from intention.knowledge.registry import load_action_registry, load_predicate_registry


def test_predicate_registry_has_six_axes_and_inactive_relation():
    registry = load_predicate_registry()
    assert set(registry.axes) == set(Axis)
    assert registry.inactive_axes == (Axis.RELATION,)
    assert registry.predicates


def test_action_registry_has_exactly_five_actions():
    predicates = load_predicate_registry()
    registry = load_action_registry(predicate_registry=predicates)
    assert set(registry.actions) == set(ActionType)
    assert registry.predicate_registry_version == predicates.version


def test_every_template_references_registered_observable_predicate():
    predicates = load_predicate_registry()
    actions = load_action_registry(predicate_registry=predicates)
    for action in actions.actions.values():
        for requirement in action.requirements:
            predicate = predicates.require(requirement.predicate_id)
            assert "suitable_for" not in predicate.predicate_id


def test_category_weights_are_normalized_when_present():
    actions = load_action_registry()
    for action in actions.actions.values():
        for category in RequirementCategory:
            group = action.by_category(category)
            if group:
                assert sum(item.weight for item in group) == pytest.approx(1.0)


def test_explain_contract_is_explicitly_associational():
    explain = load_action_registry().require(ActionType.EXPLAIN)
    assert "exploratory association" in explain.description
    assert "causal" in explain.description


def test_unregistered_predicate_is_rejected(tmp_path: Path):
    path = tmp_path / "actions.yaml"
    original = (Path(__file__).parents[2] / "configs" / "actions.yaml").read_text()
    path.write_text(original.replace("content.comparable_measure.v1", "content.unknown.v1"))
    with pytest.raises(RegistryValidationError, match="unregistered predicate"):
        load_action_registry(path=path)


def test_unsupported_action_has_explicit_registry_failure():
    with pytest.raises(RegistryValidationError, match="unsupported action"):
        load_action_registry().require("visualize")
