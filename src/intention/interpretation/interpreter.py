"""Provider interface, deterministic fixture provider, grounding and templates."""
from __future__ import annotations
from abc import ABC, abstractmethod
import re
from intention.contracts import Grounding, Interpretation, Provenance, Requirement, RequirementProfile
from intention.knowledge.layer import KnowledgeLayer

class Interpreter(ABC):
    @abstractmethod
    def interpret(self, text: str) -> dict: ...

class DeterministicInterpreter(Interpreter):
    """Rule provider for tests; output is still schema-grounded below."""
    def interpret(self, text: str) -> dict:
        lower = text.lower()
        action = next((a for key, a in (("compare", "COMPARE"), ("aggregate", "AGGREGATE"), ("predict", "PREDICT"), ("explain", "EXPLAIN"), ("monitor", "MONITOR")) if key in lower), "unknown")
        args = {}
        for key in ("measure", "comparison_dimension", "outcome", "grouping_dimension", "geographic_scope", "temporal_scope"):
            match = re.search(rf"{key.replace('_',' ')}\s*=\s*([^,;]+)", lower)
            if match: args[key] = match.group(1).strip()
        topical = re.split(r"\b(?:compare|aggregate|predict|explain|monitor)\b", text, maxsplit=1, flags=re.I)[0].strip(" ,:;") or text
        return {"action": action, "arguments": args, "topical_query": topical, "spans": [[0, len(text)]]}

def ground(text: str, raw: dict, kg: KnowledgeLayer) -> Interpretation:
    topical = raw.get("topical_query")
    spans = raw.get("spans", [])
    if not isinstance(topical, str) or not topical.strip() or not all(isinstance(s, list) and len(s) == 2 and 0 <= s[0] <= s[1] <= len(text) for s in spans):
        return Interpretation(text, None, (), raw)
    action = raw.get("action")
    if action not in kg.actions or not isinstance(raw.get("arguments"), dict):
        return Interpretation(topical, None, tuple(map(tuple, spans)), raw)
    definition = kg.actions[action]
    declared = set(definition.required_arguments + definition.optional_arguments)
    if set(raw["arguments"]) - declared:
        return Interpretation(topical, None, tuple(map(tuple, spans)), raw)
    args = {k: str(v).strip().lower() for k, v in raw["arguments"].items() if str(v).strip()}
    for key in definition.existential_arguments:
        args.setdefault(key, "*")
    if any(key not in args for key in definition.required_arguments):
        return Interpretation(topical, None, tuple(map(tuple, spans)), raw)
    return Interpretation(topical, Grounding(action, args), tuple(map(tuple, spans)), raw)

def requirements(interp: Interpretation, kg: KnowledgeLayer) -> RequirementProfile | None:
    if interp.grounding is None: return None
    action = kg.actions[interp.grounding.action]; result = []
    for i, template in enumerate(action.requirements):
        if template.value_from:
            if template.value_from not in interp.grounding.arguments:
                if template.conditional: continue
                return None
            expected = interp.grounding.arguments[template.value_from]
        else: expected = template.value
        pred = kg.predicates[template.predicate]
        result.append(Requirement(template.predicate, pred.axis, expected, template.polarity, f"{interp.grounding.action}.requirements[{i}]"))
    return RequirementProfile(interp.grounding.action, tuple(result), action.weights)
