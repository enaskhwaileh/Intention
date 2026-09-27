"""AB-constrained model proposal followed by deterministic card construction."""
import json
from dataclasses import dataclass

from .action_base import ancestry
from .interpreter.core import parse_response, ContractError
from .groq_config import groq_api_key, groq_model_id
from .provider_errors import provider_diagnostic

CARD_SCHEMA_VERSION = "1.0"
GROUNDING_PROMPT_VERSION = "canonical-ab-v0.1-grounder-v1"


@dataclass
class ReplayGrounderProvider:
    raw_response: str

    @property
    def metadata(self):
        return {"provider": "manual-replay", "fixture_origin": "manually_authored"}

    def invoke(self, interpretation, ab):
        return self.raw_response


class GroqGrounderProvider:
    def __init__(self, *, model=None, temperature=0.0, max_tokens=4096, timeout=30.0,
                 max_retries=0, client_factory=None):
        self.model, self.temperature, self.max_tokens = groq_model_id(model), temperature, max_tokens
        self.timeout, self.max_retries, self.client_factory = timeout, max_retries, client_factory

    @property
    def metadata(self):
        return {"provider": "groq", "model": self.model, "prompt_version": GROUNDING_PROMPT_VERSION,
                "generation_settings": {"temperature": self.temperature, "max_tokens": self.max_tokens,
                                        "response_format": {"type": "json_object"}}}

    def invoke(self, interpretation, ab):
        key = groq_api_key()
        catalogue = {key: {field: value for field, value in action.items()
                           if field in {"parent", "abstract", "definition", "required_roles",
                                        "minimum_cardinalities", "selection"}}
                     for key, action in ab["actions"].items()}
        prompt = ("Select exactly one supported Action Base ID. Do not invent IDs, values, or evidence. "
                  "Return only JSON with keys ab_version,input_id,action_id,bindings,evidence. "
                  "bindings maps each role to a nonempty list of {action_id,argument_index}; indices refer "
                  "to the interpreter action arguments. evidence is a nonempty list of interpreter evidence IDs. "
                  "Only select an action when its meaning and inherited required roles are supported.\nAB=" +
                  json.dumps({"ab_version": ab["ab_version"], "actions": catalogue}))
        factory = self.client_factory
        if factory is None:
            from groq import Groq
            factory = Groq
        with factory(api_key=key, timeout=self.timeout, max_retries=self.max_retries) as client:
            response = client.chat.completions.create(
                model=self.model, temperature=self.temperature, max_tokens=self.max_tokens,
                response_format={"type": "json_object"},
                messages=[{"role": "system", "content": prompt},
                          {"role": "user", "content": json.dumps(interpretation, ensure_ascii=False)}])
            return response.choices[0].message.content


def _non_grounded(status, reason, raw=None, proposal=None, metadata=None, provider_error=None):
    return {"metadata": metadata or {}, "raw_response": raw, "model_proposal": proposal,
            "grounded_card": None, "status": status, "reasons": [reason],
            "provider_error": provider_error}


def _validate_proposal(proposal, interpretation, ab):
    if not isinstance(proposal, dict) or set(proposal) != {"ab_version", "input_id", "action_id", "bindings", "evidence"}:
        raise ValueError("INVALID_MODEL_RESPONSE")
    if proposal["ab_version"] != ab["ab_version"]:
        raise ValueError("AB_VERSION_MISMATCH")
    if proposal["input_id"] != interpretation["input_id"]:
        raise ValueError("INPUT_MISMATCH")
    if proposal["action_id"] not in ab["actions"]:
        raise ValueError("UNKNOWN_ACTION_ID")
    if not isinstance(proposal["bindings"], dict) or not isinstance(proposal["evidence"], list) or not proposal["evidence"]:
        raise ValueError("MISSING_ARGUMENTS_OR_EVIDENCE")
    evidence_ids = {x["id"] for x in interpretation["evidence"]}
    if any(x not in evidence_ids for x in proposal["evidence"]):
        raise ValueError("UNKNOWN_EVIDENCE")
    actions = {x["id"]: x for x in interpretation["actions"]}
    resolved = {}
    used_evidence = set()
    for role, refs in proposal["bindings"].items():
        if role not in ab["roles"] or not isinstance(refs, list) or not refs:
            raise ValueError("INVALID_BINDING")
        resolved[role] = []
        for ref in refs:
            if not isinstance(ref, dict) or set(ref) != {"action_id", "argument_index"}:
                raise ValueError("INVALID_BINDING")
            action = actions.get(ref["action_id"])
            index = ref["argument_index"]
            if action is None or type(index) is not int or not 0 <= index < len(action["arguments"]):
                raise ValueError("INVALID_BINDING")
            argument = action["arguments"][index]
            if argument["role"] != role:
                raise ValueError("INVALID_BINDING")
            resolved[role].append({"value": argument["value"], "source": ref})
            used_evidence.update(argument["value"]["evidence"])
    if not used_evidence or not used_evidence <= set(proposal["evidence"]):
        raise ValueError("MISSING_ARGUMENT_EVIDENCE")
    required = []
    for node in ancestry(proposal["action_id"], ab):
        required.extend(ab["actions"][node].get("required_roles", []))
    missing = [role for role in required if role not in resolved]
    if missing:
        raise ValueError("MISSING_REQUIRED_ROLE:" + ",".join(missing))
    for role in required:
        spec = ab["roles"][role]
        values = [x["value"]["literal"] for x in resolved[role]]
        if len(values) < spec.get("min_items", 1) or (spec.get("unique") and len(set(values)) != len(values)):
            raise ValueError("ROLE_CARDINALITY:" + role)
    for role, minimum in ab["actions"][proposal["action_id"]].get("minimum_cardinalities", {}).items():
        if len(resolved.get(role, [])) < minimum:
            raise ValueError("ROLE_CARDINALITY:" + role)
    return resolved


def _build_card(proposal, resolved, interpretation, ab, run_id):
    bindings = {role: [item["value"] for item in items] for role, items in resolved.items()}
    binding_provenance = {role: [item["source"] for item in items] for role, items in resolved.items()}
    bindings["coverage_policy"] = ["available_observations"]
    binding_provenance["coverage_policy"] = [{"source": "system_policy", "rule_id": "default_available_observations_v1"}]
    requirement_ids = []
    for node in ancestry(proposal["action_id"], ab):
        for template_id in ab["actions"][node].get("requirements", []):
            template = ab["requirement_templates"][template_id]
            activation = template.get("activation")
            if activation == "time_points_present" and "time_points" not in resolved:
                continue
            if isinstance(activation, dict):  # complete_grid requires a certificate not proposed by this v1 response.
                continue
            if template_id not in requirement_ids:
                requirement_ids.append(template_id)
    requirements = []
    for template_id in requirement_ids:
        template = ab["requirement_templates"][template_id]
        bound = {role: bindings[role] for role in template["bind_present_roles"] if role in bindings}
        requirements.append({"id": template_id, "predicate": template["predicate"], "axis": template["axis"],
                             "modality": template["modality"], "scope": template["scope"], "bindings": bound,
                             "origin": {"action_id": proposal["action_id"], "template_id": template_id,
                                        "ab_version": ab["ab_version"]}})
    return {"schema_version": CARD_SCHEMA_VERSION, "input_id": interpretation["input_id"], "run_id": run_id,
            "ab_version": ab["ab_version"], "selected_parent_action_id": ab["actions"][proposal["action_id"]]["parent"],
            "selected_child_action_id": proposal["action_id"], "bindings": bindings,
            "binding_provenance": binding_provenance, "model_proposal": proposal,
            "deterministic_validation": {"valid": True, "checks": ["known_action", "inherited_roles", "cardinality", "evidence_refs"]},
            "requirements": requirements, "requirement_logic": {"all_of": requirement_ids},
            "evidence_provenance": {item["id"]: item for item in interpretation["evidence"] if item["id"] in proposal["evidence"]},
            "unresolved_or_missing_requirements": [], "grounding_status": "grounded"}


def ground(interpreter_envelope, ab, provider, *, run_id):
    metadata = {"ab_version": ab["ab_version"]}
    try:
        metadata.update(provider.metadata)
    except Exception as exc:
        return _non_grounded("provider_failure", "PROVIDER_FAILURE", metadata=metadata,
                             provider_error=provider_diagnostic(exc))
    if interpreter_envelope.get("failure"):
        return _non_grounded("invalid_interpretation", interpreter_envelope["failure"], metadata=metadata)
    interpretation = interpreter_envelope.get("interpretation")
    if not interpretation:
        return _non_grounded("invalid_interpretation", "MISSING_INTERPRETATION", metadata=metadata)
    status_map = {"ambiguous": "ambiguous", "insufficient": "insufficient_input", "unsupported": "unsupported"}
    if interpretation["status"] != "unambiguous":
        return _non_grounded(status_map[interpretation["status"]], "INTERPRETER_" + interpretation["status"].upper(), metadata=metadata)
    try:
        raw = provider.invoke(interpretation, ab)
    except Exception as exc:
        return _non_grounded("provider_failure", "PROVIDER_FAILURE", metadata=metadata,
                             provider_error=provider_diagnostic(exc))
    if not isinstance(raw, str):
        return _non_grounded("invalid_model_response", "NON_TEXT_RESPONSE", metadata=metadata)
    try:
        proposal = parse_response(raw)
        resolved = _validate_proposal(proposal, interpretation, ab)
        card = _build_card(proposal, resolved, interpretation, ab, run_id)
    except (ContractError, ValueError) as exc:
        return _non_grounded("invalid_model_response", str(exc), raw=raw,
                             proposal=proposal if "proposal" in locals() else None, metadata=metadata)
    return {"metadata": metadata, "raw_response": raw, "model_proposal": proposal,
            "grounded_card": card, "status": "grounded", "reasons": [],
            "provider_error": None}
