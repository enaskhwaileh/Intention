"""Versioned YAML registry loading and validation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import yaml

from intention.domain.enums import ActionType, Axis, RequirementCategory
from intention.domain.errors import RegistryValidationError
from intention.domain.models import OperationalPredicate


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CONFIG_ROOT = REPOSITORY_ROOT / "configs"


@dataclass(frozen=True)
class RequirementTemplate:
    predicate_id: str
    category: RequirementCategory
    weight: float
    expected: Any = None
    expected_from: str | None = None
    operator: str = "equals"
    conditional: bool = False


@dataclass(frozen=True)
class ActionDefinition:
    action: ActionType
    description: str
    required_arguments: tuple[str, ...]
    optional_arguments: tuple[str, ...]
    grounding_failure_conditions: tuple[str, ...]
    requirements: tuple[RequirementTemplate, ...]

    def by_category(self, category: RequirementCategory) -> tuple[RequirementTemplate, ...]:
        return tuple(item for item in self.requirements if item.category is category)


@dataclass(frozen=True)
class PredicateRegistry:
    version: str
    axes: tuple[Axis, ...]
    inactive_axes: tuple[Axis, ...]
    predicates: dict[str, OperationalPredicate]

    def require(self, predicate_id: str) -> OperationalPredicate:
        try:
            return self.predicates[predicate_id]
        except KeyError as exc:
            raise RegistryValidationError(f"unregistered predicate: {predicate_id}") from exc


@dataclass(frozen=True)
class ActionRegistry:
    version: str
    predicate_registry_version: str
    actions: dict[ActionType, ActionDefinition]

    def require(self, action: ActionType | str) -> ActionDefinition:
        try:
            normalized = action if isinstance(action, ActionType) else ActionType(action)
        except ValueError as exc:
            raise RegistryValidationError(f"unsupported action: {action}") from exc
        try:
            return self.actions[normalized]
        except KeyError as exc:
            raise RegistryValidationError(f"unsupported action: {action}") from exc


def _load_yaml(path: Path) -> dict[str, Any]:
    try:
        with path.open(encoding="utf-8") as handle:
            value = yaml.safe_load(handle)
    except (OSError, yaml.YAMLError) as exc:
        raise RegistryValidationError(f"cannot load registry {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise RegistryValidationError(f"registry {path} must contain a mapping")
    return value


def load_predicate_registry(path: Path | None = None) -> PredicateRegistry:
    raw = _load_yaml(path or DEFAULT_CONFIG_ROOT / "predicates.yaml")
    version = str(raw.get("registry_version", ""))
    try:
        axes = tuple(Axis(value) for value in raw.get("axes", []))
        inactive = tuple(Axis(value) for value in raw.get("inactive_axes", []))
    except ValueError as exc:
        raise RegistryValidationError(f"unknown axis: {exc}") from exc
    if set(axes) != set(Axis):
        raise RegistryValidationError("predicate registry must declare all six canonical axes")
    if not set(inactive) <= set(axes):
        raise RegistryValidationError("inactive axes must be declared axes")
    predicates: dict[str, OperationalPredicate] = {}
    for predicate_id, definition in raw.get("predicates", {}).items():
        if predicate_id in predicates:
            raise RegistryValidationError(f"duplicate predicate: {predicate_id}")
        try:
            predicates[predicate_id] = OperationalPredicate(
                predicate_id=predicate_id,
                registry_version=version,
                axis=Axis(definition["axis"]),
                description=definition["description"],
                value_kind=definition["value_kind"],
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise RegistryValidationError(f"invalid predicate {predicate_id}: {exc}") from exc
    if not predicates:
        raise RegistryValidationError("predicate registry must not be empty")
    return PredicateRegistry(version, axes, inactive, predicates)


def _templates(raw: dict[str, Any]) -> Iterable[RequirementTemplate]:
    for category in RequirementCategory:
        for item in raw.get(category.value, []):
            yield RequirementTemplate(
                predicate_id=item["predicate"],
                category=category,
                weight=float(item["weight"]),
                expected=item.get("expected"),
                expected_from=item.get("expected_from"),
                operator=item.get("operator", "equals"),
                conditional=bool(item.get("conditional", False)),
            )


def load_action_registry(
    path: Path | None = None,
    predicate_registry: PredicateRegistry | None = None,
) -> ActionRegistry:
    predicates = predicate_registry or load_predicate_registry()
    raw = _load_yaml(path or DEFAULT_CONFIG_ROOT / "actions.yaml")
    version = str(raw.get("registry_version", ""))
    predicate_version = str(raw.get("predicate_registry_version", ""))
    if predicate_version != predicates.version:
        raise RegistryValidationError("action and predicate registry versions are incompatible")
    actions: dict[ActionType, ActionDefinition] = {}
    for name, definition in raw.get("actions", {}).items():
        try:
            action = ActionType(name)
        except ValueError as exc:
            raise RegistryValidationError(f"unsupported canonical action: {name}") from exc
        requirements = tuple(_templates(definition.get("requirements", {})))
        for template in requirements:
            predicates.require(template.predicate_id)
            if not 0.0 < template.weight <= 1.0:
                raise RegistryValidationError(f"invalid weight for {name}:{template.predicate_id}")
            if (template.expected is None) == (template.expected_from is None):
                raise RegistryValidationError(
                    f"{name}:{template.predicate_id} must define exactly one expected source"
                )
        for category in RequirementCategory:
            group = [item for item in requirements if item.category is category]
            if group and abs(sum(item.weight for item in group) - 1.0) > 1e-9:
                raise RegistryValidationError(f"{name}:{category.value} weights must sum to 1")
        actions[action] = ActionDefinition(
            action=action,
            description=definition["description"],
            required_arguments=tuple(definition.get("required_arguments", [])),
            optional_arguments=tuple(definition.get("optional_arguments", [])),
            grounding_failure_conditions=tuple(definition.get("grounding_failure_conditions", [])),
            requirements=requirements,
        )
    if set(actions) != set(ActionType):
        raise RegistryValidationError("action registry must define exactly the five canonical actions")
    return ActionRegistry(version, predicate_version, actions)
