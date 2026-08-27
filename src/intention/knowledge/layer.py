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
    predicates: dict[str, PredicateDef]
    actions: dict[str, ActionDef]
    digest: str

def load_knowledge(path: Path | None = None) -> KnowledgeLayer:
    path = path or Path(__file__).resolve().parents[3] / "configs/knowledge/knowledge.yaml"
    raw_text = path.read_text(encoding="utf-8")
    raw = yaml.safe_load(raw_text)
    if not isinstance(raw, dict) or set(raw) != {"version", "axes", "predicates", "actions", "validation"}:
        raise ValueError("knowledge root fields are invalid")
    if tuple(raw["axes"]) != AXES or set(raw["actions"]) != set(ACTIONS):
        raise ValueError("knowledge must define exactly the canonical axes and actions")
    predicates = {}
    for name, item in raw["predicates"].items():
        if set(item) != {"axis", "matcher"} or item["axis"] not in AXES or item["matcher"] not in MATCHERS:
            raise ValueError(f"invalid predicate {name}")
        predicates[name] = PredicateDef(**item)
    actions = {}
    for name, item in raw["actions"].items():
        allowed = {"description", "required_arguments", "optional_arguments", "existential_arguments", "weights", "requirements"}
        if set(item) - allowed or set(item["weights"]) != set(AXES) or abs(sum(item["weights"].values()) - 1) > 1e-9:
            raise ValueError(f"invalid action {name}")
        declared = set(item["required_arguments"] + item["optional_arguments"])
        if not set(item["existential_arguments"]) <= declared:
            raise ValueError(f"invalid existential arguments for {name}")
        templates = []
        for template in item["requirements"]:
            if template["predicate"] not in predicates or template["polarity"] not in POLARITIES:
                raise ValueError(f"invalid requirement for {name}")
            if ("value" in template) == ("value_from" in template):
                raise ValueError("requirement must have exactly one value source")
            if template.get("value_from") not in declared and "value_from" in template:
                raise ValueError(f"undeclared argument in {name}")
            templates.append(RequirementTemplate(**template))
        actions[name] = ActionDef(tuple(item["required_arguments"]), tuple(item["optional_arguments"]), tuple(item["existential_arguments"]), dict(item["weights"]), tuple(templates))
    canonical = json.dumps(raw, sort_keys=True, separators=(",", ":")).encode()
    return KnowledgeLayer(str(raw["version"]), predicates, actions, sha256(canonical).hexdigest())
