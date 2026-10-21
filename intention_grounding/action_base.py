"""Versioned intention library, consistency validation, and read-only inspection."""
import copy
import json
from pathlib import Path

CATALOG_DIRECTORY = Path(__file__).parent / "docs" / "ab_proposal"
CANONICAL_AB_PATH = CATALOG_DIRECTORY / "action-base-v0.2.json"
LEGACY_AB_PATH = CATALOG_DIRECTORY / "action-base-v0.1.json"
# This is a code capability boundary, not a flag the catalogue can grant itself.
GROUNDABLE_ACTION_IDS = frozenset({"compare.groups", "compare.groups.trajectories", "compare.time"})


class ActionBaseError(ValueError):
    pass


def _require(condition, message):
    if not condition:
        raise ActionBaseError(message)


def _strings(value, code, *, allowed=None, nonempty=False):
    _require(isinstance(value, list) and all(isinstance(x, str) and x for x in value), code)
    _require(len(set(value)) == len(value) and (bool(value) or not nonempty), code)
    if allowed is not None:
        _require(set(value) <= set(allowed), code)
    return value


def _records(value, code):
    _require(isinstance(value, dict) and bool(value), code)
    _require(all(isinstance(k, str) and k and isinstance(v, dict) for k, v in value.items()), code)
    return value


def validate_action_base(ab):
    _require(isinstance(ab, dict), "AB_ROOT")
    for key in ("ab_version", "axes", "roles", "actions", "predicates", "requirement_templates"):
        _require(key in ab, f"AB_MISSING_{key.upper()}")
    _require(isinstance(ab["ab_version"], str) and bool(ab["ab_version"]), "AB_VERSION")
    _strings(ab["axes"], "AB_AXES", nonempty=True)
    roles = _records(ab["roles"], "AB_ROLES")
    actions = _records(ab["actions"], "AB_ACTIONS")
    predicates = _records(ab["predicates"], "AB_PREDICATES")
    templates = _records(ab["requirement_templates"], "AB_TEMPLATES")
    for role in roles.values():
        _require(isinstance(role.get("type"), str) and bool(role["type"]), "AB_ROLE_TYPE")
        if "min_items" in role:
            _require(type(role["min_items"]) is int and role["min_items"] >= 1, "AB_ROLE_CARDINALITY")
    for action_id, action in actions.items():
        _require(type(action.get("abstract")) is bool, "AB_ABSTRACT")
        _require(isinstance(action.get("definition"), str) and bool(action["definition"]), "AB_DEFINITION")
        seen, parent = {action_id}, action.get("parent")
        while parent is not None:
            _require(isinstance(parent, str) and parent in actions and parent not in seen, "AB_PARENT")
            seen.add(parent)
            parent = actions[parent].get("parent")
        _strings(action.get("required_roles"), "AB_ACTION_ROLE", allowed=roles)
        _strings(action.get("requirements"), "AB_ACTION_REQUIREMENT", allowed=templates)
        cardinalities = action.get("minimum_cardinalities", {})
        _require(isinstance(cardinalities, dict), "AB_ACTION_CARDINALITY")
        _require(all(k in roles and type(v) is int and v >= 1 for k, v in cardinalities.items()), "AB_ACTION_CARDINALITY")
    for predicate in predicates.values():
        _require(isinstance(predicate.get("axis"), str) and predicate["axis"] in ab["axes"], "AB_PREDICATE_AXIS")
        _strings(predicate.get("argument_roles"), "AB_PREDICATE_ROLE", allowed=roles)
    for template in templates.values():
        _require(isinstance(template.get("predicate"), str) and template["predicate"] in predicates, "AB_TEMPLATE_PREDICATE")
        _require(template.get("axis") == predicates[template["predicate"]]["axis"], "AB_TEMPLATE_AXIS")
        _require(template.get("modality") in ("required", "preferred", "forbidden"), "AB_TEMPLATE_MODALITY")
        _strings(template.get("bind_present_roles"), "AB_TEMPLATE_ROLE", allowed=roles)
    if "library_schema_version" in ab:
        _validate_library(ab)
    else:
        # Only the frozen v0.1 format may omit the library capability contract.
        _require(ab["ab_version"] == "0.1.0-draft", "AB_LIBRARY_SCHEMA_REQUIRED")
    return ab


def _validate_library(ab):
    _require(ab["library_schema_version"] == "1.0", "IL_SCHEMA_VERSION")
    _require(ab.get("exhaustive") is False, "IL_EXHAUSTIVENESS")
    policy = ab.get("runtime_policy")
    _require(isinstance(policy, dict), "IL_RUNTIME_POLICY")
    enabled = _strings(policy.get("groundable_action_ids"), "IL_RUNTIME_ACTION", allowed=GROUNDABLE_ACTION_IDS)
    _require(policy.get("assessment") == "unknown_only" and policy.get("execution") == "not_implemented", "IL_RUNTIME_CAPABILITY")
    contract = ab.get("verdict_contract")
    _require(isinstance(contract, dict), "IL_VERDICT_CONTRACT")
    _require(contract.get("states") == ["supported", "violated", "unresolved"] and contract.get("missing_evidence") == "unresolved", "IL_VERDICT_CONTRACT")
    _require(contract.get("gold_access") == "forbidden_to_runtime", "IL_GOLD_ACCESS")
    composition = ab.get("composition_policy")
    _require(isinstance(composition, dict), "IL_COMPOSITION")
    _require(composition.get("joint_goals") == "all_of" and composition.get("accepted_alternatives") == "any_of" and composition.get("competing_interpretations") == "ambiguous_not_any_of", "IL_COMPOSITION")
    procedures = _records(ab.get("procedures"), "IL_PROCEDURES")
    actions, roles, templates = ab["actions"], ab["roles"], ab["requirement_templates"]
    _require(set(enabled) <= set(actions), "IL_RUNTIME_ACTION")
    referenced = set()
    for aid, action in actions.items():
        expected = "abstract" if action["abstract"] else ("grounding_only" if aid in enabled else "catalog_only")
        _require(action.get("runtime_support") == expected, "IL_ACTION_CAPABILITY")
        _require(action.get("scientific_status") == "proposed_unvalidated", "IL_SCIENTIFIC_STATUS")
        ids = _strings(action.get("procedure_ids"), "IL_ACTION_PROCEDURES", allowed=procedures, nonempty=not action["abstract"])
        _require(not action["abstract"] or not ids, "IL_ABSTRACT_PROCEDURE")
        if not action["abstract"]:
            _strings(action.get("examples"), "IL_EXAMPLES", nonempty=True)
            _strings(action.get("exclusions"), "IL_EXCLUSIONS", nonempty=True)
        for pid in ids:
            _require(procedures[pid].get("action_id") == aid, "IL_PROCEDURE_OWNER")
        referenced.update(ids)
    _require(referenced == set(procedures), "IL_ORPHAN_PROCEDURE")
    for proc in procedures.values():
        aid = proc.get("action_id")
        _require(isinstance(aid, str) and aid in actions and not actions[aid]["abstract"], "IL_PROCEDURE_OWNER")
        for field in ("definition", "selection"):
            _require(isinstance(proc.get(field), str) and bool(proc[field]), "IL_PROCEDURE_DESCRIPTION")
        _strings(proc.get("additional_required_roles"), "IL_PROCEDURE_ROLE", allowed=roles)
        _strings(proc.get("additional_requirements"), "IL_PROCEDURE_REQUIREMENT", allowed=templates)
        _require(proc.get("runtime_support") == actions[aid]["runtime_support"], "IL_PROCEDURE_CAPABILITY")
        _require(proc.get("input_scope") in ("single_table", "table_set", "model_and_table"), "IL_PROCEDURE_SCOPE")
        _require(proc.get("evidence_policy") == "scoped_three_valued_v1", "IL_EVIDENCE_POLICY")
        output = proc.get("output_contract")
        _require(isinstance(output, dict), "IL_OUTPUT_CONTRACT")
        for field in ("kind", "provenance"):
            _require(isinstance(output.get(field), str) and bool(output[field]), "IL_OUTPUT_CONTRACT")
        _strings(output.get("limitations"), "IL_OUTPUT_CONTRACT", nonempty=True)
    for predicate in ab["predicates"].values():
        evidence = predicate.get("evidence_contract")
        if isinstance(evidence, dict):
            for state in ("supported", "violated", "unresolved"):
                _require(isinstance(evidence.get(state), str) and bool(evidence[state]), "IL_PREDICATE_EVIDENCE")
        else:
            _require(isinstance(evidence, str) and bool(evidence), "IL_PREDICATE_EVIDENCE")


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
    _require(isinstance(action_id, str) and action_id in ab["actions"], "UNKNOWN_ACTION_ID")
    chain = []
    while action_id is not None:
        _require(action_id not in chain, "AB_PARENT")
        chain.append(action_id)
        action_id = ab["actions"][action_id]["parent"]
    return list(reversed(chain))


def is_groundable(action_id, ab):
    action = ab["actions"].get(action_id) if isinstance(action_id, str) else None
    return bool(action and not action["abstract"] and action_id in GROUNDABLE_ACTION_IDS
                and action.get("runtime_support", "grounding_only") == "grounding_only")


def describe_intention(action_id, ab):
    """Return unbound procedure definitions; this does not interpret or ground a request."""
    chain = ancestry(action_id, ab)
    roles, requirements = [], []
    for node in chain:
        roles.extend(ab["actions"][node]["required_roles"])
        requirements.extend(ab["actions"][node]["requirements"])
    action = ab["actions"][action_id]
    alternatives = []
    for pid in action.get("procedure_ids", []):
        procedure = ab["procedures"][pid]
        required = list(dict.fromkeys(requirements + procedure["additional_requirements"]))
        alternatives.append({"procedure_id": pid, **copy.deepcopy(procedure),
                             "activation_status": "not_evaluated_unbound_templates",
                             "required_roles": list(dict.fromkeys(roles + procedure["additional_required_roles"])),
                             "requirement_templates": {rid: copy.deepcopy(ab["requirement_templates"][rid]) for rid in required},
                             "predicate_definitions": {ab["requirement_templates"][rid]["predicate"]:
                                                       copy.deepcopy(ab["predicates"][ab["requirement_templates"][rid]["predicate"]])
                                                       for rid in required},
                             "requirement_logic": {"all_of": required}})
    return {"ab_version": ab["ab_version"], "action_id": action_id,
            "action": copy.deepcopy(action), "ancestry": chain,
            "required_roles": list(dict.fromkeys(roles)),
            "procedures": alternatives, "procedure_relationship": "alternative_definitions_not_request_selection",
            "children": sorted(aid for aid, item in ab["actions"].items() if item["parent"] == action_id),
            "groundable": is_groundable(action_id, ab)}


def list_intentions(ab):
    return {"ab_version": ab["ab_version"], "exhaustive": False,
            "actions": [{"id": aid, "parent": item["parent"], "abstract": item["abstract"],
                         "definition": item["definition"],
                         "runtime_support": item.get("runtime_support", "abstract" if item["abstract"] else "grounding_only"),
                         "procedure_ids": item.get("procedure_ids", [])}
                        for aid, item in sorted(ab["actions"].items())]}


# Preferred terminology; compatibility names above share the same implementation.
CANONICAL_IL_PATH = CANONICAL_AB_PATH
IntentionLibraryError = ActionBaseError
load_intention_library = load_action_base
validate_intention_library = validate_action_base
