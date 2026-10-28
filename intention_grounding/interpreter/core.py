"""Interpreter: interpret(u) = (q_u, iota_u) with diagnostic status s_I (Algorithm 1).

The extracted intention is iota_u = (e_u, B_u, Omega_u): an intention expression
copied from the input, argument candidates and scope restrictions. Each argument
or scope entry is a record (id, label, value, spans) whose spans are exact
substrings of the input. Candidate-table information is never supplied.
"""
from dataclasses import dataclass, field
import time

from ..llm import parse_json_object

STATUS_EXTRACTED, STATUS_NO_INTENTION, STATUS_FAILURE = "extracted", "no_intention", "failure"
CONTRACT_KEYS = {"context_query", "intention_expression", "arguments", "scope"}
ENTRY_KEYS = {"id", "label", "value", "spans"}


@dataclass
class Interpretation:
    input_id: str
    input: str
    status: str
    context_query: str
    intention: dict = None          # {"expression", "arguments", "scope"} or None (= bottom)
    failure: str = None
    provider: dict = field(default_factory=dict)
    raw_response: str = None
    elapsed_ms: float = 0.0

    def to_dict(self):
        return {"input_id": self.input_id, "input": self.input, "status": self.status,
                "context_query": self.context_query, "intention": self.intention,
                "failure": self.failure, "provider": self.provider,
                "raw_response": self.raw_response, "elapsed_ms": self.elapsed_ms}


class ExtractionError(ValueError):
    """Carries only a fixed diagnostic code."""


def _contains(text, span):
    return isinstance(span, str) and span.strip() != "" and span.casefold() in text.casefold()


def validate_extraction(z, u, vocabulary):
    """ValidExtraction(z, u): structure, permitted labels, unique ids, nonempty context
    query and textual occurrence of every cited span and of the intention expression."""
    if not isinstance(z, dict) or set(z) != CONTRACT_KEYS:
        raise ExtractionError("CONTRACT_KEYS")
    q = z["context_query"]
    if not isinstance(q, str) or not q.strip():
        raise ExtractionError("EMPTY_CONTEXT_QUERY")
    expression = z["intention_expression"]
    if expression is not None and not _contains(u, expression):
        raise ExtractionError(f"EXPRESSION_NOT_IN_INPUT: {expression!r} is not a contiguous phrase of the input; copy one phrase exactly")
    ids = set()
    for field_name, labels in (("arguments", vocabulary["argument_labels"]), ("scope", vocabulary["scope_labels"])):
        entries = z[field_name]
        if not isinstance(entries, list):
            raise ExtractionError("ENTRIES_NOT_LIST")
        for entry in entries:
            if not isinstance(entry, dict) or set(entry) != ENTRY_KEYS:
                raise ExtractionError("ENTRY_KEYS")
            if not isinstance(entry["id"], str) or not entry["id"] or entry["id"] in ids:
                raise ExtractionError("DUPLICATE_OR_INVALID_ID")
            ids.add(entry["id"])
            if entry["label"] not in labels:
                other = "scope" if field_name == "arguments" else "arguments"
                other_labels = vocabulary["scope_labels"] if field_name == "arguments" else vocabulary["argument_labels"]
                hint = (f"; it is a {other} label: move entry {entry.get('id')} to \"{other}\"" if entry["label"] in other_labels
                        else f"; use one of {sorted(labels)}")
                raise ExtractionError(f"UNKNOWN_LABEL: {entry['label']!r} is not allowed in \"{field_name}\"{hint}")
            if not isinstance(entry["value"], str) or not entry["value"].strip():
                raise ExtractionError("EMPTY_VALUE")
            spans = entry["spans"]
            if not isinstance(spans, list) or not spans or not all(_contains(u, s) for s in spans):
                bad = next((s for s in (spans or []) if not _contains(u, s)), None)
                raise ExtractionError(f"SPAN_NOT_IN_INPUT: span {bad!r} of entry {entry.get('id')} is not copied from the input")
    if expression is None and z["arguments"]:
        # Arguments without an intention expression are kept only as context.
        pass
    return z


def parse_record(z):
    return {"expression": z["intention_expression"], "arguments": z["arguments"], "scope": z["scope"]}


def interpret(u, provider, vocabulary, *, input_id="input"):
    """Algorithm 1. One extraction attempt; failure falls back to q_u = u.

    A provider with max_repairs > 0 gets that many extra attempts, each told the validator's error
    (an optional extension; max_repairs = 0 reproduces Algorithm 1)."""
    start = time.perf_counter()
    result = Interpretation(input_id=input_id, input=u, status=STATUS_FAILURE, context_query=u)
    try:
        raw, meta = provider.extract(u, vocabulary)
        result.provider = meta
        result.raw_response = raw
    except Exception as exc:  # provider failure
        code = exc.args[0] if exc.args and isinstance(exc.args[0], str) else type(exc).__name__
        result.failure = "PROVIDER_FAILURE:" + code
        result.provider = getattr(provider, "metadata", {})
        result.elapsed_ms = round((time.perf_counter() - start) * 1000, 3)
        return result
    repairs = 0
    while True:
        try:
            z = validate_extraction(parse_json_object(raw), u, vocabulary)
            break
        except (ValueError, ExtractionError, TypeError, KeyError, AttributeError) as exc:
            if not isinstance(exc, (ValueError, ExtractionError)):  # malformed object of an unexpected shape
                exc = ExtractionError(f"MALFORMED_EXTRACTION:{type(exc).__name__}: follow the JSON schema exactly")
            if repairs >= getattr(provider, "max_repairs", 0):
                result.failure = "INVALID_EXTRACTION:" + str(exc)
                result.elapsed_ms = round((time.perf_counter() - start) * 1000, 3)
                return result
            repairs += 1
            try:
                raw, meta = provider.extract(u, vocabulary, feedback={"raw": raw, "error": str(exc)})
            except Exception as exc2:
                code = exc2.args[0] if exc2.args and isinstance(exc2.args[0], str) else type(exc2).__name__
                result.failure = "PROVIDER_FAILURE:" + code
                result.elapsed_ms = round((time.perf_counter() - start) * 1000, 3)
                return result
            result.provider, result.raw_response = {**meta, "repairs": repairs}, raw
    result.context_query = z["context_query"]
    if z["intention_expression"] is None:
        result.status = STATUS_NO_INTENTION
    else:
        result.status = STATUS_EXTRACTED
        result.intention = parse_record(z)
    result.elapsed_ms = round((time.perf_counter() - start) * 1000, 3)
    return result
