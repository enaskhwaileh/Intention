"""Grounder: (g_u, Psi_u, s_G) = ground(iota_u, L)   (Algorithm 2).

A resolver proposes a variant, role-to-entry references and scope references.
Everything after the proposal is deterministic: contract validation, binding of
referenced values, procedure applicability and requirement instantiation.
"""
import copy
import json
import re
import time

from . import il as il_module
from .llm import ChatClient, parse_json_object

GROUNDED, INSUFFICIENT, AMBIGUOUS, UNSUPPORTED, FAILURE, NOT_ATTEMPTED = (
    "grounded", "insufficient", "ambiguous", "unsupported", "failure", "not_attempted")
PROMPT_VERSION = "grounder-v3.1"
PROPOSAL_KEYS = {"status", "variant_id", "bindings", "scope", "justification", "diagnostics"}


# ------------------------------------------------------------------ resolvers
RESOLVER_PROMPT = """You map an extracted analytical intention to a registered Intention Library variant.
Return ONLY one JSON object:
{"status": "proposed"|"insufficient"|"ambiguous"|"unsupported",
 "variant_id": str|null,
 "bindings": {role: [entry_id, ...]},
 "scope": [entry_id, ...],
 "justification": str,
 "diagnostics": [{"code": str, "role": str|null, "entry_refs": [entry_id, ...]}]}
Rules:
- Choose a variant whose outcome is what the input asks for. Use only variant ids and role
  names from the library definitions below.
- Every binding must reference ids of the extracted arguments (e.g. "a1"), never their values
  (write ["a1"], not ["mean"]); never write new values, SQL, predicates or thresholds. The
  entry label must be one of the labels the role admits ("labels" in the role contract), and
  an entry that no role admits is left unbound.
- Reference every extracted scope entry id in "scope" (e.g. ["s1"]); never omit one.
- If a required role has no extracted entry, return "insufficient" and name the role in a
  diagnostic (code MISSING_ROLE). Never select a statistic or prediction target merely
  because it is plausible.
- If two variants remain incompatible readings of the input, return "ambiguous".
- If no registered variant fits, return "unsupported".
Library definitions:
"""


class LLMResolver:
    def __init__(self, client=None, max_repairs=0, **kwargs):
        self.client = client or ChatClient(**kwargs)
        self.max_repairs = max_repairs  # 0 = Algorithm 2 exactly (one proposal)

    @property
    def metadata(self):
        return {"resolver": "llm", "model": self.client.model, "prompt_version": PROMPT_VERSION, "max_repairs": self.max_repairs}

    def propose(self, u, intention, definitions, feedback=None):
        messages = [{"role": "system", "content": RESOLVER_PROMPT + json.dumps(definitions, ensure_ascii=False)},
                    {"role": "user", "content": json.dumps({"input": u, "intention": intention}, ensure_ascii=False)}]
        if feedback:
            messages += [{"role": "assistant", "content": feedback["raw"]},
                         {"role": "user", "content": f"Your previous proposal was rejected by the contract check with error {feedback['error']}. "
                                                     "Return a corrected JSON object for the same input, following every rule above."}]
        raw, record = self.client.complete_json(messages, prompt_version=PROMPT_VERSION)
        return raw, {**self.metadata, **record}


class ReplayResolver:
    def __init__(self, records, origin="authored_gold"):
        self.records = {k.casefold(): v for k, v in records.items()}
        self.origin = origin

    @property
    def metadata(self):
        return {"resolver": "replay", "origin": self.origin}

    def propose(self, u, intention, definitions):
        if u.casefold() not in self.records:
            raise KeyError("NO_RECORDED_PROPOSAL")
        return json.dumps(self.records[u.casefold()]), self.metadata


_CLASSIFICATION_CUES = r"\b(whether|which|class|category|categories|type|survive[ds]?|survival|default|churn|diagnos\w*|yes or no|binary|presence|outcome)\b"


class IndexResolver:
    """Deterministic baseline: expression index -> family, role labels -> variant and bindings."""
    def __init__(self, library):
        self.library = library

    @property
    def metadata(self):
        return {"resolver": "index", "version": "index-resolver-v1"}

    def propose(self, u, intention, definitions):
        L = self.library
        expression = (intention.get("expression") or "").casefold()
        args, scope = intention["arguments"], intention["scope"]
        by_label = {}
        for entry in args:
            by_label.setdefault(entry["label"], []).append(entry)
        family, best = None, 0
        for item in L["expression_index"]:
            phrase = item["phrase"]
            if re.search(r"\b" + re.escape(phrase) + r"\b", expression) and len(phrase) > best:
                family, best = item["family"], len(phrase)
        proposal = {"status": "proposed", "variant_id": None, "bindings": {}, "scope": [s["id"] for s in scope],
                    "justification": "", "diagnostics": []}
        if family is None:
            proposal.update(status="unsupported", justification="Expression not in the expression index.",
                            diagnostics=[{"code": "UNKNOWN_EXPRESSION", "role": None, "entry_refs": []}])
            return json.dumps(proposal), self.metadata
        stat = " ".join(e["value"].casefold() for e in by_label.get("statistic", []))
        if family == "compare":
            means = L["variants"]["compare.group_means"]["roles"]["statistic"]["admissible"]
            many = len(by_label.get("groups", []) + by_label.get("time_points", [])) >= 2
            if stat and any(term in stat for term in means):
                variant = "compare.group_means"
            elif many or by_label.get("group_dimension"):
                variant = "compare.observed_values"
            else:
                variant = "compare.group_means"
        elif family == "aggregate":
            variant = "aggregate.group_totals"
        elif family == "predict":
            target = " ".join(e["value"] for e in by_label.get("target", []) + by_label.get("measure", []))
            variant = "predict.classification" if re.search(_CLASSIFICATION_CUES, u + " " + target, re.I) else "predict.regression"
        elif family == "explain":
            variant = "explain.association"
        else:
            variant = "monitor.trend"
        proposal["variant_id"] = variant
        used = set()
        for role, contract in L["variants"][variant]["roles"].items():
            refs = []
            for label in contract["labels"]:
                for entry in by_label.get(label, []):
                    if entry["id"] not in used:
                        refs.append(entry["id"])
                if refs:
                    break
            if contract["max"] is not None:
                refs = refs[:contract["max"]]
            if refs:
                proposal["bindings"][role] = refs
                used.update(refs)
        missing = [r for r, c in L["variants"][variant]["roles"].items() if c["required"] and r not in proposal["bindings"]]
        missing += ["|".join(g) for g in L["variants"][variant].get("requires_one_of", []) if not any(r in proposal["bindings"] for r in g)]
        if missing:
            proposal.update(status="insufficient",
                            diagnostics=[{"code": "MISSING_ROLE", "role": r, "entry_refs": []} for r in missing])
        proposal["justification"] = f"Index phrase -> family {family}; labels -> {variant}."
        return json.dumps(proposal), self.metadata


# --------------------------------------------------------------- validation
class GroundingError(ValueError):
    pass


def _contract_valid(z, intention, library):
    """Returns (status, diagnostics) for deterministic contract checks on a proposal."""
    if not isinstance(z, dict) or set(z) != PROPOSAL_KEYS:
        raise GroundingError("PROPOSAL_KEYS")
    entries = {e["id"]: e for e in intention["arguments"]}
    scope_entries = {e["id"]: e for e in intention["scope"]}
    if z["status"] != "proposed":
        if z["status"] not in (INSUFFICIENT, AMBIGUOUS, UNSUPPORTED):
            raise GroundingError("UNKNOWN_STATUS")
        for d in z.get("diagnostics") or []:
            refs = d.get("entry_refs") or []
            if any(r not in entries and r not in scope_entries for r in refs):
                raise GroundingError("DIAGNOSTIC_REFERENCE")
        return z["status"], z.get("diagnostics") or []
    variant = library["variants"].get(z["variant_id"])
    if variant is None:
        raise GroundingError("UNKNOWN_VARIANT")
    if not isinstance(z["bindings"], dict) or not isinstance(z["scope"], list):
        raise GroundingError("BINDINGS_FORMAT")
    for role, refs in z["bindings"].items():
        contract = variant["roles"].get(role)
        if contract is None:
            raise GroundingError("UNKNOWN_ROLE:" + str(role))
        if not isinstance(refs, list) or not refs:
            raise GroundingError("EMPTY_BINDING:" + role)
        for ref in refs:
            entry = entries.get(ref)
            if entry is None:
                raise GroundingError("UNKNOWN_REFERENCE:" + str(ref))
            if entry["label"] not in contract["labels"]:
                raise GroundingError(f"LABEL_NOT_ADMITTED:{role}:{entry['label']}")
        if len(refs) < contract["min"] or (contract["max"] is not None and len(refs) > contract["max"]):
            raise GroundingError("CARDINALITY:" + role)
        admissible = contract.get("admissible")
        if admissible:
            for ref in refs:
                value = entries[ref]["value"].casefold()
                if not any(term in value for term in admissible):
                    return UNSUPPORTED, [{"code": "INADMISSIBLE_VALUE", "role": role, "entry_refs": [ref]}]
    if set(z["scope"]) != set(scope_entries):
        raise GroundingError("SCOPE_NOT_PRESERVED")
    missing = [r for r, c in variant["roles"].items() if c["required"] and r not in z["bindings"]]
    for group in variant.get("requires_one_of", []):
        if not any(r in z["bindings"] for r in group):
            missing.append("|".join(group))
    if missing:
        return INSUFFICIENT, [{"code": "MISSING_ROLE", "role": r, "entry_refs": []} for r in missing]
    return "proposed", []


def _applicable(procedure, bound):
    rule = procedure["applicability"]
    if rule["rule"] == "always":
        return "eligible"
    if rule["rule"] == "excluded_if_statistic_mentions":
        text = " ".join(v["value"] for v in bound.get("statistic", [])).casefold()
        return "excluded" if any(re.search(r"\b" + re.escape(t) + r"\b", text) for t in rule["terms"]) else "eligible"
    return "unresolved"


def _substitute(value, theta):
    if isinstance(value, str) and value.startswith("$"):
        return copy.deepcopy(theta.get(value[1:]))
    if isinstance(value, list):
        return [_substitute(v, theta) for v in value]
    if isinstance(value, dict):
        return {k: _substitute(v, theta) for k, v in value.items()}
    return value


def instantiate(library, variant_id, bound, scope):
    """Psi_u = {(id(P), P^u, H^u_P, S^u_P) : P in P_u}  (Eq. 21)."""
    theta = {role: [v["value"] for v in values] for role, values in bound.items()}
    theta = {role: (values[0] if library["variants"][variant_id]["roles"][role]["max"] == 1 else values)
             for role, values in theta.items()}
    theta["scope"] = [{"label": s["label"], "value": s["value"]} for s in scope]
    version = il_module.version(library)
    psi, decisions = [], {}
    for pid in library["variants"][variant_id]["procedures"]:
        procedure = library["procedures"][pid]
        decision = _applicable(procedure, bound)
        decisions[pid] = decision
        if decision != "eligible":
            continue
        reqs = {"hard": [], "soft": []}
        for kind in ("hard", "soft"):
            for rid in procedure[kind]:
                record = library["requirements"][rid]
                reqs[kind].append({"id": f"{pid}/{rid}", "requirement_id": rid, "pid": pid,
                                   "origin": record["origin"], "axis": record["axis"], "kind": kind,
                                   "predicate": record["predicate"], "params": _substitute(record["params"], theta),
                                   "evidence_rule": record["evidence_rule"], "rationale": record["rationale"],
                                   "provenance": {"il_version": version, "template": rid}})
        psi.append({"procedure_id": pid, "expression": procedure["expression"], "sql": procedure.get("sql"),
                    "hard": reqs["hard"], "soft": reqs["soft"]})
    return psi, decisions, theta


def ground(interpretation, library, resolver):
    """Algorithm 2: returns dict(g_u, psi_u, status, diagnostics, provenance, elapsed_ms)."""
    start = time.perf_counter()
    result = {"g_u": None, "psi_u": [], "status": NOT_ATTEMPTED, "diagnostics": [], "resolver": {},
              "raw_proposal": None, "il_version": il_module.version(library), "elapsed_ms": 0.0}

    def done(status, **kw):
        result.update(status=status, **kw)
        result["elapsed_ms"] = round((time.perf_counter() - start) * 1000, 3)
        return result

    if interpretation["status"] != "extracted" or not interpretation.get("intention"):
        return done(NOT_ATTEMPTED, diagnostics=[{"code": "NO_INTENTION_" + interpretation["status"].upper()}])
    intention = interpretation["intention"]
    definitions = il_module.definitions(library)
    try:
        raw, meta = resolver.propose(interpretation["input"], intention, definitions)
        result["resolver"], result["raw_proposal"] = meta, raw
        z = parse_json_object(raw)
    except Exception as exc:
        code = exc.args[0] if exc.args and isinstance(exc.args[0], str) else type(exc).__name__
        return done(FAILURE, diagnostics=[{"code": "RESOLVER_FAILURE:" + code}],
                    resolver=getattr(resolver, "metadata", {}))
    repairs = 0
    while True:
        try:
            status, diagnostics = _contract_valid(z, intention, library)
            break
        except GroundingError as exc:
            if repairs >= getattr(resolver, "max_repairs", 0):
                return done(FAILURE, diagnostics=[{"code": "CONTRACT_INVALID:" + str(exc)}], proposal=z)
            repairs += 1
            try:
                raw, meta = resolver.propose(interpretation["input"], intention, definitions, feedback={"raw": raw, "error": str(exc)})
                result["resolver"], result["raw_proposal"] = {**meta, "repairs": repairs}, raw
                z = parse_json_object(raw)
            except Exception as exc2:
                code = exc2.args[0] if exc2.args and isinstance(exc2.args[0], str) else type(exc2).__name__
                return done(FAILURE, diagnostics=[{"code": "RESOLVER_FAILURE:" + code}], resolver=getattr(resolver, "metadata", {}))
    result["proposal"] = z
    if status != "proposed":
        return done(status, diagnostics=diagnostics)
    entries = {e["id"]: e for e in intention["arguments"]}
    bound = {role: [{"value": entries[r]["value"], "entry": r, "label": entries[r]["label"],
                     "spans": entries[r]["spans"]} for r in refs] for role, refs in z["bindings"].items()}
    scope = [e for e in intention["scope"] if e["id"] in z["scope"]]
    psi, decisions, theta = instantiate(library, z["variant_id"], bound, scope)
    if any(d == "unresolved" for d in decisions.values()):
        return done(INSUFFICIENT, diagnostics=[{"code": "APPLICABILITY_UNRESOLVED"}])
    if not psi or any(not p["hard"] for p in psi):
        return done(FAILURE, diagnostics=[{"code": "NO_ELIGIBLE_PROCEDURE"}])
    g_u = {"variant_id": z["variant_id"], "family": library["variants"][z["variant_id"]]["family"],
           "bindings": bound, "scope": scope, "theta": theta, "procedure_decisions": decisions,
           "il_version": il_module.version(library), "justification": z.get("justification", "")}
    return done(GROUNDED, g_u=g_u, psi_u=psi)
