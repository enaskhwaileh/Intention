"""Versioned intention library, consistency validation, and read-only inspection."""
import copy
import json
from pathlib import Path

CATALOG_DIRECTORY = Path(__file__).parent / "library"
CANONICAL_IL_PATH = CATALOG_DIRECTORY / "intention-library-v0.3.json"
LEGACY_IL_PATH = Path(__file__).parent / "docs/ab_proposal/action-base-v0.1.json"
# This is a code capability boundary, not a flag the catalogue can grant itself.
GROUNDABLE_INTENTION_IDS = frozenset({"compare.groups", "compare.groups.trajectories", "compare.time"})


class IntentionLibraryError(ValueError):
    pass


def _require(condition, message):
    if not condition:
        raise IntentionLibraryError(message)


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


def validate_intention_library(il):
    _require(isinstance(il, dict), "IL_ROOT")
    for key in ("il_version", "axes", "roles", "intentions", "predicates", "requirement_templates"):
        _require(key in il, f"IL_MISSING_{key.upper()}")
    _require(isinstance(il["il_version"], str) and bool(il["il_version"]), "IL_VERSION")
    _strings(il["axes"], "IL_AXES", nonempty=True)
    roles = _records(il["roles"], "IL_ROLES")
    intentions = _records(il["intentions"], "IL_ACTIONS")
    predicates = _records(il["predicates"], "IL_PREDICATES")
    templates = _records(il["requirement_templates"], "IL_TEMPLATES")
    for role in roles.values():
        _require(isinstance(role.get("type"), str) and bool(role["type"]), "IL_ROLE_TYPE")
        if "min_items" in role:
            _require(type(role["min_items"]) is int and role["min_items"] >= 1, "IL_ROLE_CARDINALITY")
    for intention_id, intention in intentions.items():
        _require(type(intention.get("abstract")) is bool, "IL_ABSTRACT")
        _require(isinstance(intention.get("definition"), str) and bool(intention["definition"]), "IL_DEFINITION")
        seen, parent = {intention_id}, intention.get("parent")
        while parent is not None:
            _require(isinstance(parent, str) and parent in intentions and parent not in seen, "IL_PARENT")
            seen.add(parent)
            parent = intentions[parent].get("parent")
        _strings(intention.get("required_roles"), "IL_INTENTION_ROLE", allowed=roles)
        _strings(intention.get("requirements"), "IL_INTENTION_REQUIREMENT", allowed=templates)
        cardinalities = intention.get("minimum_cardinalities", {})
        _require(isinstance(cardinalities, dict), "IL_INTENTION_CARDINALITY")
        _require(all(k in roles and type(v) is int and v >= 1 for k, v in cardinalities.items()), "IL_INTENTION_CARDINALITY")
    for predicate in predicates.values():
        _require(isinstance(predicate.get("axis"), str) and predicate["axis"] in il["axes"], "IL_PREDICATE_AXIS")
        _strings(predicate.get("argument_roles"), "IL_PREDICATE_ROLE", allowed=roles)
    for template in templates.values():
        _require(isinstance(template.get("predicate"), str) and template["predicate"] in predicates, "IL_TEMPLATE_PREDICATE")
        _require(template.get("axis") == predicates[template["predicate"]]["axis"], "IL_TEMPLATE_AXIS")
        _require(template.get("modality") in ("required", "preferred", "forbidden"), "IL_TEMPLATE_MODALITY")
        _strings(template.get("bind_present_roles"), "IL_TEMPLATE_ROLE", allowed=roles)
    if "library_schema_version" in il:
        _validate_library(il)
    else:
        # Only the frozen v0.1 format may omit the library capability contract.
        _require(il["il_version"] == "0.1.0-draft", "IL_LIBRARY_SCHEMA_REQUIRED")
    return il


def _validate_library(il):
    _require(il["library_schema_version"] == "1.0", "IL_SCHEMA_VERSION")
    _require(il.get("exhaustive") is False, "IL_EXHAUSTIVENESS")
    policy = il.get("runtime_policy")
    _require(isinstance(policy, dict), "IL_RUNTIME_POLICY")
    enabled = _strings(policy.get("groundable_intention_ids"), "IL_RUNTIME_ACTION", allowed=GROUNDABLE_INTENTION_IDS)
    _require(policy.get("assessment") == "unknown_only" and policy.get("execution") == "not_implemented", "IL_RUNTIME_CAPABILITY")
    contract = il.get("verdict_contract")
    _require(isinstance(contract, dict), "IL_VERDICT_CONTRACT")
    _require(contract.get("states") == ["supported", "violated", "unresolved"] and contract.get("missing_evidence") == "unresolved", "IL_VERDICT_CONTRACT")
    _require(contract.get("gold_access") == "forbidden_to_runtime", "IL_GOLD_ACCESS")
    composition = il.get("composition_policy")
    _require(isinstance(composition, dict), "IL_COMPOSITION")
    _require(composition.get("joint_goals") == "all_of" and composition.get("accepted_alternatives") == "any_of" and composition.get("competing_interpretations") == "ambiguous_not_any_of", "IL_COMPOSITION")
    procedures = _records(il.get("procedures"), "IL_PROCEDURES")
    intentions, roles, templates = il["intentions"], il["roles"], il["requirement_templates"]
    _require(set(enabled) <= set(intentions), "IL_RUNTIME_ACTION")
    referenced = set()
    for aid, intention in intentions.items():
        expected = "abstract" if intention["abstract"] else ("grounding_only" if aid in enabled else "catalog_only")
        _require(intention.get("runtime_support") == expected, "IL_INTENTION_CAPABILITY")
        _require(intention.get("scientific_status") == "proposed_unvalidated", "IL_SCIENTIFIC_STATUS")
        ids = _strings(intention.get("procedure_ids"), "IL_INTENTION_PROCEDURES", allowed=procedures, nonempty=not intention["abstract"])
        _require(not intention["abstract"] or not ids, "IL_ABSTRACT_PROCEDURE")
        if not intention["abstract"]:
            _strings(intention.get("examples"), "IL_EXAMPLES", nonempty=True)
            _strings(intention.get("exclusions"), "IL_EXCLUSIONS", nonempty=True)
        for pid in ids:
            _require(procedures[pid].get("intention_id") == aid, "IL_PROCEDURE_OWNER")
        referenced.update(ids)
    _require(referenced == set(procedures), "IL_ORPHAN_PROCEDURE")
    for proc in procedures.values():
        aid = proc.get("intention_id")
        _require(isinstance(aid, str) and aid in intentions and not intentions[aid]["abstract"], "IL_PROCEDURE_OWNER")
        for field in ("definition", "selection"):
            _require(isinstance(proc.get(field), str) and bool(proc[field]), "IL_PROCEDURE_DESCRIPTION")
        _strings(proc.get("additional_required_roles"), "IL_PROCEDURE_ROLE", allowed=roles)
        _strings(proc.get("additional_requirements"), "IL_PROCEDURE_REQUIREMENT", allowed=templates)
        _require(proc.get("runtime_support") == intentions[aid]["runtime_support"], "IL_PROCEDURE_CAPABILITY")
        _require(proc.get("input_scope") in ("single_table", "table_set", "model_and_table"), "IL_PROCEDURE_SCOPE")
        _require(proc.get("evidence_policy") == "scoped_three_valued_v1", "IL_EVIDENCE_POLICY")
        output = proc.get("output_contract")
        _require(isinstance(output, dict), "IL_OUTPUT_CONTRACT")
        for field in ("kind", "provenance"):
            _require(isinstance(output.get(field), str) and bool(output[field]), "IL_OUTPUT_CONTRACT")
        _strings(output.get("limitations"), "IL_OUTPUT_CONTRACT", nonempty=True)
    for predicate in il["predicates"].values():
        evidence = predicate.get("evidence_contract")
        if isinstance(evidence, dict):
            for state in ("supported", "violated", "unresolved"):
                _require(isinstance(evidence.get(state), str) and bool(evidence[state]), "IL_PREDICATE_EVIDENCE")
        else:
            _require(isinstance(evidence, str) and bool(evidence), "IL_PREDICATE_EVIDENCE")


def load_intention_library(path=CANONICAL_IL_PATH, expected_version=None):
    try:
        il = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise IntentionLibraryError("IL_LOAD_FAILURE") from exc
    validate_intention_library(il)
    if expected_version is not None and il["il_version"] != expected_version:
        raise IntentionLibraryError("IL_VERSION_MISMATCH")
    return il


def ancestry(intention_id, il):
    _require(isinstance(intention_id, str) and intention_id in il["intentions"], "UNKNOWN_INTENTION_ID")
    chain = []
    while intention_id is not None:
        _require(intention_id not in chain, "IL_PARENT")
        chain.append(intention_id)
        intention_id = il["intentions"][intention_id]["parent"]
    return list(reversed(chain))


def is_groundable(intention_id, il):
    intention = il["intentions"].get(intention_id) if isinstance(intention_id, str) else None
    return bool(intention and not intention["abstract"] and intention_id in GROUNDABLE_INTENTION_IDS
                and intention.get("runtime_support", "grounding_only") == "grounding_only")


def describe_intention(intention_id, il):
    """Return unbound procedure definitions; this does not interpret or ground a request."""
    chain = ancestry(intention_id, il)
    roles, requirements = [], []
    for node in chain:
        roles.extend(il["intentions"][node]["required_roles"])
        requirements.extend(il["intentions"][node]["requirements"])
    intention = il["intentions"][intention_id]
    alternatives = []
    for pid in intention.get("procedure_ids", []):
        procedure = il["procedures"][pid]
        required = list(dict.fromkeys(requirements + procedure["additional_requirements"]))
        alternatives.append({"procedure_id": pid, **copy.deepcopy(procedure),
                             "activation_status": "not_evaluated_unbound_templates",
                             "required_roles": list(dict.fromkeys(roles + procedure["additional_required_roles"])),
                             "requirement_templates": {rid: copy.deepcopy(il["requirement_templates"][rid]) for rid in required},
                             "predicate_definitions": {il["requirement_templates"][rid]["predicate"]:
                                                       copy.deepcopy(il["predicates"][il["requirement_templates"][rid]["predicate"]])
                                                       for rid in required},
                             "requirement_logic": {"all_of": required}})
    return {"il_version": il["il_version"], "intention_id": intention_id,
            "intention": copy.deepcopy(intention), "ancestry": chain,
            "required_roles": list(dict.fromkeys(roles)),
            "procedures": alternatives, "procedure_relationship": "alternative_definitions_not_request_selection",
            "children": sorted(aid for aid, item in il["intentions"].items() if item["parent"] == intention_id),
            "groundable": is_groundable(intention_id, il)}


def list_intentions(il):
    return {"il_version": il["il_version"], "exhaustive": False,
            "intentions": [{"id": aid, "parent": item["parent"], "abstract": item["abstract"],
                         "definition": item["definition"],
                         "runtime_support": item.get("runtime_support", "abstract" if item["abstract"] else "grounding_only"),
                         "procedure_ids": item.get("procedure_ids", [])}
                        for aid, item in sorted(il["intentions"].items())]}


