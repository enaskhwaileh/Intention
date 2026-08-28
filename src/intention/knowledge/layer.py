"""Strict Action Grounding Knowledge Layer K_G."""
from __future__ import annotations
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any
import json
import yaml

AXES = ("sem", "str", "cov", "qual", "aff")
ACTIONS = ("COMPARE", "AGGREGATE", "PREDICT", "EXPLAIN", "MONITOR")
MATCHERS = {"exact", "normalized", "semantic", "numerical", "set_containment", "interval", "granularity", "existential"}
POLARITIES = {"req", "opt", "neg"}

@dataclass(frozen=True)
class PredicateDef:
    axis: str
    matcher: str
    parameters: dict[str, Any]

@dataclass(frozen=True)
class RequirementTemplate:
    predicate: str
    polarity: str
    value: Any = None
    value_from: str | None = None
    conditional: bool = False

@dataclass(frozen=True)
class ActionDef:
    required_arguments: tuple[str, ...]
    optional_arguments: tuple[str, ...]
    existential_arguments: tuple[str, ...]
    weights: dict[str, float]
    requirements: tuple[RequirementTemplate, ...]

@dataclass(frozen=True)
class KnowledgeLayer:
    version: str
    axes: tuple[str, ...]
    predicates: dict[str, PredicateDef]
    actions: dict[str, ActionDef]
    validation: dict[str, bool]
    digest: str

    @property
    def action_catalogue(self) -> tuple[str, ...]:
        """K_G component A."""
        return tuple(self.actions)

    @property
    def templates(self) -> dict[str, tuple[RequirementTemplate, ...]]:
        """K_G component G."""
        return {name: action.requirements for name, action in self.actions.items()}

    @property
    def matching_rules(self) -> dict[str, tuple[str, dict[str, Any]]]:
        """K_G component M."""
        return {name: (pred.matcher, pred.parameters) for name, pred in self.predicates.items()}

    @property
    def axis_weights(self) -> dict[str, dict[str, float]]:
        """K_G component B."""
        return {name: action.weights for name, action in self.actions.items()}

def load_knowledge(path: Path | None = None) -> KnowledgeLayer:
    path = path or Path(__file__).resolve().parents[3] / "configs/knowledge/knowledge.yaml"
    raw_text = path.read_text(encoding="utf-8")
    raw = yaml.safe_load(raw_text)
    if not isinstance(raw, dict) or set(raw) != {"version", "axes", "predicates", "actions", "validation"}:
        raise ValueError("knowledge root fields are invalid")
    if not isinstance(raw["version"], str) or not raw["version"].strip():
        raise ValueError("knowledge version must be a non-empty string")
    if tuple(raw["axes"]) != AXES or set(raw["actions"]) != set(ACTIONS):
        raise ValueError("knowledge must define exactly the canonical axes and actions")
    expected_validation = {"weights_sum_to_one": True, "reject_unknown_fields": True}
    if raw["validation"] != expected_validation:
        raise ValueError("knowledge validation constraints must be enabled")
    predicates = {}
    for name, item in raw["predicates"].items():
        if not isinstance(name, str) or not name or not isinstance(item, dict) or set(item) != {"axis", "matcher"} or item["axis"] not in AXES:
            raise ValueError(f"invalid predicate {name}")
        matcher = item["matcher"]
        if isinstance(matcher, str):
            matcher_type, parameters = matcher, {}
        elif isinstance(matcher, dict) and "type" in matcher:
            matcher_type = matcher["type"]
            parameters = {key: value for key, value in matcher.items() if key != "type"}
        else:
            raise ValueError(f"invalid predicate {name}")
        if matcher_type not in MATCHERS:
            raise ValueError(f"invalid predicate {name}")
        allowed_parameters = {
            "numerical": {"operator"},
            "interval": {"mode"},
        }.get(matcher_type, set())
        if set(parameters) != allowed_parameters:
            raise ValueError(f"invalid matcher parameters for {name}")
        if matcher_type == "numerical" and parameters["operator"] not in {"at_most", "at_least", "equal"}:
            raise ValueError(f"invalid numerical operator for {name}")
        if matcher_type == "interval" and parameters["mode"] not in {"overlap", "containment", "containment_or_overlap"}:
            raise ValueError(f"invalid interval mode for {name}")
        predicates[name] = PredicateDef(item["axis"], matcher_type, parameters)
    actions = {}
    for name, item in raw["actions"].items():
        allowed = {"description", "required_arguments", "optional_arguments", "existential_arguments", "weights", "requirements"}
        required = {"required_arguments", "optional_arguments", "existential_arguments", "weights", "requirements"}
        if not isinstance(item, dict) or set(item) - allowed or not required <= set(item):
            raise ValueError(f"invalid action {name}")
        arguments = item["required_arguments"] + item["optional_arguments"]
        weights = item["weights"]
        if (
            not all(isinstance(group, list) and all(isinstance(value, str) and value for value in group) for group in (item["required_arguments"], item["optional_arguments"], item["existential_arguments"]))
            or len(arguments) != len(set(arguments))
            or not isinstance(weights, dict)
            or set(weights) != set(AXES)
            or not all(isinstance(value, (int, float)) and not isinstance(value, bool) and value >= 0 for value in weights.values())
            or abs(sum(weights.values()) - 1) > 1e-9
        ):
            raise ValueError(f"invalid action {name}")
        declared = set(arguments)
        if not set(item["existential_arguments"]) <= declared:
            raise ValueError(f"invalid existential arguments for {name}")
        templates = []
        for template in item["requirements"]:
            if not isinstance(template, dict) or set(template) - {"predicate", "polarity", "value", "value_from", "conditional"} or not {"predicate", "polarity"} <= set(template):
                raise ValueError(f"invalid requirement for {name}")
            if template["predicate"] not in predicates or template["polarity"] not in POLARITIES:
                raise ValueError(f"invalid requirement for {name}")
            if ("value" in template) == ("value_from" in template):
                raise ValueError("requirement must have exactly one value source")
            if template.get("value_from") not in declared and "value_from" in template:
                raise ValueError(f"undeclared argument in {name}")
            if "conditional" in template and not isinstance(template["conditional"], bool):
                raise ValueError(f"invalid requirement for {name}")
            templates.append(RequirementTemplate(**template))
        if not templates:
            raise ValueError(f"action {name} must define requirements")
        active_axes = {predicates[template.predicate].axis for template in templates}
        if sum(weights[axis] for axis in active_axes) <= 0:
            raise ValueError(f"action {name} has zero weight over its active axes")
        actions[name] = ActionDef(tuple(item["required_arguments"]), tuple(item["optional_arguments"]), tuple(item["existential_arguments"]), dict(item["weights"]), tuple(templates))
    canonical = json.dumps(raw, sort_keys=True, separators=(",", ":")).encode()
    return KnowledgeLayer(str(raw["version"]), AXES, predicates, actions, dict(raw["validation"]), sha256(canonical).hexdigest())
