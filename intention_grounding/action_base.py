"""Loader and deterministic consistency checks for the canonical proposal AB."""
import json
from pathlib import Path

CANONICAL_AB_PATH = Path(__file__).parent / "docs" / "ab_proposal" / "action-base-v0.1.json"


class ActionBaseError(ValueError):
    pass


def _require(condition, message):
    if not condition:
        raise ActionBaseError(message)


def validate_action_base(ab):
    _require(isinstance(ab, dict), "AB_ROOT")
    for key in ("ab_version", "axes", "roles", "actions", "predicates", "requirement_templates"):
        _require(key in ab, f"AB_MISSING_{key.upper()}")
    _require(isinstance(ab["ab_version"], str) and ab["ab_version"], "AB_VERSION")
    actions, templates, predicates = ab["actions"], ab["requirement_templates"], ab["predicates"]
    for action_id, action in actions.items():
        seen, parent = {action_id}, action.get("parent")
        while parent is not None:
            _require(parent in actions and parent not in seen, "AB_PARENT")
            seen.add(parent)
            parent = actions[parent].get("parent")
        _require(set(action.get("required_roles", [])) <= set(ab["roles"]), "AB_ACTION_ROLE")
        _require(set(action.get("requirements", [])) <= set(templates), "AB_ACTION_REQUIREMENT")
    for predicate in predicates.values():
        _require(predicate.get("axis") in ab["axes"], "AB_PREDICATE_AXIS")
        _require(set(predicate.get("argument_roles", [])) <= set(ab["roles"]), "AB_PREDICATE_ROLE")
    for template_id, template in templates.items():
        _require(template.get("predicate") in predicates, "AB_TEMPLATE_PREDICATE")
        _require(template.get("axis") == predicates[template["predicate"]]["axis"], "AB_TEMPLATE_AXIS")
        _require(set(template.get("bind_present_roles", [])) <= set(ab["roles"]), "AB_TEMPLATE_ROLE")
    return ab


def load_action_base(path=CANONICAL_AB_PATH, expected_version=None):
    try:
        ab = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ActionBaseError("AB_LOAD_FAILURE") from exc
    validate_action_base(ab)
    if expected_version is not None and ab["ab_version"] != expected_version:
        raise ActionBaseError("AB_VERSION_MISMATCH")
    return ab


def ancestry(action_id, ab):
    chain = []
    while action_id is not None:
        chain.append(action_id)
        action_id = ab["actions"][action_id]["parent"]
    return list(reversed(chain))
