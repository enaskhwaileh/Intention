"""Strict capability-gold schema, independent from profiler predictions."""
from __future__ import annotations
from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any
from intention.knowledge.layer import KnowledgeLayer

JUDGMENTS={"supported","not_supported","unknown","not_applicable"}; CERTAINTIES={"clear","ambiguous"}
SOURCE_TYPES={"metadata","column","cell_range","table_statistic","documentation","multiple_sources"}
SCOPES={"complete_table","sample","declared_metadata"}
KINDS={"entity","event","entity_time","group","group_time","aggregate_total","mixed","unknown"}
AGGREGATION={"observed","aggregated","mixed","unknown"}

@dataclass(frozen=True)
class GoldCapability:
    predicate: str; judgment: str; value: Any; evidence: dict[str,Any]; certainty: str; ambiguity_reason: str|None
@dataclass(frozen=True)
class GoldTable:
    table_id: str; row_granularity: GoldCapability; capabilities: tuple[GoldCapability,...]
@dataclass(frozen=True)
class GoldDataset:
    version: str; knowledge_hash: str; annotation_status: str; annotators: tuple[str,...]; tables: tuple[GoldTable,...]

def _record(raw,kg,predicate=None):
    allowed={"predicate","judgment","value","evidence","certainty","ambiguity_reason"}
    if not isinstance(raw,dict) or set(raw)!=allowed: raise ValueError("invalid gold capability fields")
    pred=raw["predicate"] if predicate is None else predicate
    if raw["predicate"]!=pred or pred not in kg.predicates or raw["judgment"] not in JUDGMENTS or raw["certainty"] not in CERTAINTIES: raise ValueError("invalid gold capability vocabulary")
    evidence=raw["evidence"]
    if not isinstance(evidence,dict) or set(evidence)!={"source_type","source_locator","inspection_scope"} or evidence["source_type"] not in SOURCE_TYPES or evidence["inspection_scope"] not in SCOPES: raise ValueError("invalid gold evidence")
    if raw["judgment"]=="supported" and raw["value"] is None: raise ValueError("supported gold capability requires a value")
    if raw["judgment"] in {"unknown","not_applicable"} and raw["value"] is not None: raise ValueError("unknown/not-applicable gold value must be null")
    if raw["certainty"]=="ambiguous" and not raw["ambiguity_reason"]: raise ValueError("ambiguous gold judgment requires a reason")
    if pred=="row_granularity" and raw["judgment"]=="supported":
        value=raw["value"]; required={"kind","entity_fields","entity_type","time_fields","time_unit","grouping_fields","aggregation_status","description"}
        if not isinstance(value,dict) or set(value)!=required or value["kind"] not in KINDS or value["aggregation_status"] not in AGGREGATION or not all(isinstance(value[x],list) for x in ("entity_fields","time_fields","grouping_fields")): raise ValueError("invalid row granularity value")
    return GoldCapability(pred,raw["judgment"],raw["value"],evidence,raw["certainty"],raw["ambiguity_reason"])

def load_gold_annotations(path: Path,kg: KnowledgeLayer) -> GoldDataset:
    raw=json.loads(path.read_text()); expected={"version","knowledge_hash","annotation_status","annotators","tables"}
    if not isinstance(raw,dict) or set(raw)!=expected or raw["knowledge_hash"]!=kg.digest or not raw["annotators"]: raise ValueError("invalid gold annotation root")
    tables=[]; ids=set()
    for item in raw["tables"]:
        if set(item)!={"table_id","row_granularity","capabilities"} or item["table_id"] in ids: raise ValueError("invalid or duplicate gold table")
        ids.add(item["table_id"]); row=_record(item["row_granularity"],kg,"row_granularity"); caps=tuple(_record(x,kg) for x in item["capabilities"])
        expected_predicates=set(kg.predicates)-{"row_granularity"}
        if {x.predicate for x in caps}!=expected_predicates or len(caps)!=len(expected_predicates): raise ValueError("gold table must annotate every predicate exactly once")
        tables.append(GoldTable(item["table_id"],row,caps))
    return GoldDataset(raw["version"],raw["knowledge_hash"],raw["annotation_status"],tuple(raw["annotators"]),tuple(tables))
