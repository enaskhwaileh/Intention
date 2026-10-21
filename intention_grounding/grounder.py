"""Intention Library-constrained model proposal followed by deterministic card construction."""
import json
from dataclasses import dataclass

from .intention_library import ancestry, is_groundable
from .interpreter.core import parse_response, ContractError
from .groq_config import groq_api_key, groq_model_id
from .provider_errors import provider_diagnostic

CARD_SCHEMA_VERSION = "2.0"
GROUNDING_PROMPT_VERSION = "canonical-il-v0.3-grounder-v3"


@dataclass
class ReplayGrounderProvider:
    raw_response: str

    @property
    def metadata(self):
        return {"provider": "manual-replay", "fixture_origin": "manually_authored"}

    def invoke(self, interpretation, il):
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

    def invoke(self, interpretation, il):
        key = groq_api_key()
        catalogue = {key: {field: value for field, value in intention.items()
                           if field in {"parent", "abstract", "definition", "required_roles",
                                        "minimum_cardinalities", "selection"}}
                     for key, intention in il["intentions"].items()
                     if is_groundable(key, il) or key == "compare"}
        prompt = ("Select exactly one supported Intention Library intention ID. Do not invent IDs, values, or evidence. "
                  "Return only JSON with keys il_version,input_id,intention_id,bindings,evidence. "
                  "bindings maps each role to a nonempty list of {intention_instance_id,argument_index}; indices refer "
                  "to the structured intention record arguments. evidence is a nonempty list of interpreter evidence IDs. "
                  "Only select an intention when its meaning and inherited required roles are supported.\nIL=" +
                  json.dumps({"il_version": il["il_version"], "intentions": catalogue}))
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
            "grounded_intention": None, "status": status, "reasons": [reason],
            "provider_error": provider_error}


def _validate_proposal(proposal, interpretation, il):
    if not isinstance(proposal, dict) or set(proposal) != {"il_version", "input_id", "intention_id", "bindings", "evidence"}:
        raise ValueError("INVALID_MODEL_RESPONSE")
    if proposal["il_version"] != il["il_version"]:
        raise ValueError("IL_VERSION_MISMATCH")
    if proposal["input_id"] != interpretation["input_id"]:
        raise ValueError("INPUT_MISMATCH")
    if not isinstance(proposal["intention_id"], str) or proposal["intention_id"] not in il["intentions"]:
        raise ValueError("UNKNOWN_INTENTION_ID")
    if il["intentions"][proposal["intention_id"]]["abstract"]:
        raise ValueError("ABSTRACT_INTENTION_NOT_GROUNDABLE")
    if not is_groundable(proposal["intention_id"], il):
        raise ValueError("INTENTION_CATALOG_ONLY")
    if not isinstance(proposal["bindings"], dict) or not isinstance(proposal["evidence"], list) or not proposal["evidence"]:
        raise ValueError("MISSING_ARGUMENTS_OR_EVIDENCE")
    evidence_ids = {x["id"] for x in interpretation["evidence"]}
    if any(not isinstance(x, str) or x not in evidence_ids for x in proposal["evidence"]):
        raise ValueError("UNKNOWN_EVIDENCE")
    intentions = {x["id"]: x for x in interpretation["intentions"]}
    resolved = {}
    used_evidence = set()
    for role, refs in proposal["bindings"].items():
        if role not in il["roles"] or not isinstance(refs, list) or not refs:
            raise ValueError("INVALID_BINDING")
        resolved[role] = []
        for ref in refs:
            if not isinstance(ref, dict) or set(ref) != {"intention_instance_id", "argument_index"}:
                raise ValueError("INVALID_BINDING")
            if not isinstance(ref["intention_instance_id"], str):
                raise ValueError("INVALID_BINDING")
            intention = intentions.get(ref["intention_instance_id"])
            index = ref["argument_index"]
            if intention is None or type(index) is not int or not 0 <= index < len(intention["arguments"]):
                raise ValueError("INVALID_BINDING")
            argument = intention["arguments"][index]
            if argument["role"] != role:
                raise ValueError("INVALID_BINDING")
            resolved[role].append({"value": argument["value"], "source": ref})
            used_evidence.update(argument["value"]["evidence"])
    if not used_evidence or not used_evidence <= set(proposal["evidence"]):
        raise ValueError("MISSING_ARGUMENT_EVIDENCE")
    required = []
    for node in ancestry(proposal["intention_id"], il):
        required.extend(il["intentions"][node].get("required_roles", []))
    missing = [role for role in required if role not in resolved]
    if missing:
        raise ValueError("MISSING_REQUIRED_ROLE:" + ",".join(missing))
    for role in required:
        spec = il["roles"][role]
        values = [x["value"]["literal"] for x in resolved[role]]
        if len(values) < spec.get("min_items", 1) or (spec.get("unique") and len(set(values)) != len(values)):
            raise ValueError("ROLE_CARDINALITY:" + role)
    for role, minimum in il["intentions"][proposal["intention_id"]].get("minimum_cardinalities", {}).items():
        if len(resolved.get(role, [])) < minimum:
            raise ValueError("ROLE_CARDINALITY:" + role)
    return resolved


def _build_card(proposal, resolved, interpretation, il, run_id):
    bindings = {role: [item["value"] for item in items] for role, items in resolved.items()}
    binding_provenance = {role: [item["source"] for item in items] for role, items in resolved.items()}
    bindings["coverage_policy"] = ["available_observations"]
    binding_provenance["coverage_policy"] = [{"source": "system_policy", "rule_id": "default_available_observations_v1"}]
    requirement_ids = []
    for node in ancestry(proposal["intention_id"], il):
        for template_id in il["intentions"][node].get("requirements", []):
            template = il["requirement_templates"][template_id]
            activation = template.get("activation")
            if activation == "time_points_present" and "time_points" not in resolved:
                continue
            if isinstance(activation, dict):  # complete_grid requires a certificate not proposed by this v1 response.
                continue
            if template_id not in requirement_ids:
                requirement_ids.append(template_id)
    requirements = []
    for template_id in requirement_ids:
        template = il["requirement_templates"][template_id]
        bound = {role: bindings[role] for role in template["bind_present_roles"] if role in bindings}
        requirements.append({"id": template_id, "predicate": template["predicate"], "axis": template["axis"],
                             "modality": template["modality"], "scope": template["scope"], "bindings": bound,
                             "origin": {"intention_id": proposal["intention_id"], "template_id": template_id,
                                        "il_version": il["il_version"]}})
    return {"schema_version": CARD_SCHEMA_VERSION, "input_id": interpretation["input_id"], "run_id": run_id,
            "il_version": il["il_version"], "parent_intention_id": il["intentions"][proposal["intention_id"]]["parent"],
            "intention_id": proposal["intention_id"], "bindings": bindings,
            "binding_provenance": binding_provenance, "model_proposal": proposal,
            "deterministic_validation": {"valid": True, "checks": ["known_intention", "inherited_roles", "cardinality", "evidence_refs"]},
            "requirements": requirements, "requirement_logic": {"all_of": requirement_ids},
            "evidence_provenance": {item["id"]: item for item in interpretation["evidence"] if item["id"] in proposal["evidence"]},
            "unresolved_or_missing_requirements": [], "grounding_status": "grounded"}


def ground(interpreter_envelope, il, provider, *, run_id):
    metadata = {"il_version": il["il_version"]}
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
        raw = provider.invoke(interpretation, il)
    except Exception as exc:
        return _non_grounded("provider_failure", "PROVIDER_FAILURE", metadata=metadata,
                             provider_error=provider_diagnostic(exc))
    if not isinstance(raw, str):
        return _non_grounded("invalid_model_response", "NON_TEXT_RESPONSE", metadata=metadata)
    try:
        proposal = parse_response(raw)
        resolved = _validate_proposal(proposal, interpretation, il)
        card = _build_card(proposal, resolved, interpretation, il, run_id)
    except (ContractError, ValueError) as exc:
        if str(exc) == "INTENTION_CATALOG_ONLY":
            return _non_grounded("unsupported", "INTENTION_CATALOG_ONLY", raw=raw,
                                 proposal=proposal, metadata=metadata)
        return _non_grounded("invalid_model_response", str(exc), raw=raw,
                             proposal=proposal if "proposal" in locals() else None, metadata=metadata)
    return {"metadata": metadata, "raw_response": raw, "model_proposal": proposal,
            "grounded_intention": card, "status": "grounded", "reasons": [],
            "provider_error": None}


def ground_request(record):
    """Ground a validated authored structured request, before seeing any tables.

    This is an explicit non-LLM input mode, not inferred natural-language accuracy.
    The closed request supplies semantic roles, never table or column identifiers.
    """
    from pathlib import Path
    from .contracts import validate_request
    validate_request(record)
    library = json.loads((Path(__file__).parent/'library/compare-procedures-v1.json').read_text())
    base = {'schema_version':'2.0','request_id':record['request_id'],'il_version':library['il_version'],
            'input_mode':record['input_mode'],'intention_type':record['intention_type'],
            'request_evidence':{'text':record['text'],'origin':'authored structured specification; not live NLP'},
            'procedures':[], 'status':record['status']}
    if record['status'] != 'ready':
        base['reason']='REQUEST_'+record['status'].upper()
        return base
    if record['intention_type'] != 'compare':
        base.update(status='unsupported',reason='PREDICT_RUNTIME_NOT_IMPLEMENTED')
        return base
    if record['roles']['statistic']=='unspecified':
        base.update(status='ambiguous',reason='STATISTIC_NOT_SPECIFIED_NO_AUTOMATIC_MEAN')
        return base
    for pid,procedure in library['procedures'].items():
        if procedure['statistic']==record['roles']['statistic'] or record['roles']['statistic']=='documented_or_mean':
            base['procedures'].append({'procedure_id':pid,**procedure,'bindings':record['roles']})
    base['procedure_relationship']='accepted_alternatives' if len(base['procedures'])>1 else 'single'
    base['status']='grounded' if base['procedures'] else 'unsupported'
    return base
