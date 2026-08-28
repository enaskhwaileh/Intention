"""Deterministic evidence extraction with explicit observed/inferred provenance."""
from __future__ import annotations
from collections import Counter
from hashlib import sha256
import json
from intention.contracts import Capability, CapabilityProfile, Provenance, Table

PROFILER_VERSION="2.0.0"

def _norm(value): return str(value).strip().lower().replace("_"," ")
def _missing(value): return value is None or value==""
def _identifier_name(column):
    name=_norm(column); return name=="id" or name.endswith(" id") or name.endswith(" identifier")
def _temporal_name(column): return any(token in _norm(column).split() for token in ("date","year","time","timestamp","month"))
def _time_unit(column):
    name=_norm(column)
    return next((unit for unit in ("year","month","date","day","time") if unit in name),"unknown")

def _granularity(table,columns,identifiers,temporal,grouping):
    declared=table.metadata.get("row_granularity")
    if isinstance(declared,dict): return declared,"observed",1.0,Provenance("metadata:row_granularity","declared_metadata","structured")
    text=_norm(declared) if declared else ""
    entity_type=_norm(identifiers[0]).removesuffix(" id") if identifiers else text.replace("-day","").replace("-year","") if text else "unknown"
    has_time=bool(temporal) or any(token in text for token in ("day","year","time"))
    if identifiers: kind="entity_time" if has_time else "entity"
    elif grouping: kind="group_time" if has_time else "group"
    else: kind="unknown"
    aggregation="aggregated" if kind in {"group","group_time"} or any(token in text for token in ("summary","aggregate","group")) else "observed" if kind!="unknown" else "unknown"
    value={"kind":kind,"entity_fields":[_norm(c) for c in identifiers],"entity_type":entity_type,"time_fields":[_norm(c) for c in temporal],"time_unit":_time_unit(temporal[0]) if temporal else "unknown","grouping_fields":[_norm(c) for c in grouping],"aggregation_status":aggregation,"description":f"one row represents {text or kind}"}
    state="observed" if declared else "inferred"; confidence=1.0 if declared else .65
    source="metadata:row_granularity" if declared else "schema"
    procedure="declared_metadata_normalization" if declared else "composite_granularity_heuristic"
    return value,state,confidence,Provenance(source,procedure)

def profile_table(table: Table,complete_table: bool=True) -> tuple[Capability,...]:
    if not table.rows: return ()
    columns=tuple(table.rows[0]); values={c:[row.get(c) for row in table.rows] for c in columns}; caps=[]
    declared_keys=set(table.metadata.get("primary_key",[])); inferred_identifiers={c for c in columns if _identifier_name(c) and c not in declared_keys}; identifiers=[c for c in columns if c in declared_keys or c in inferred_identifiers]
    scan_state="observed" if complete_table else "estimated"; scan_confidence=1.0 if complete_table else .7; scan_procedure="complete_table_scan" if complete_table else "sample_scan_estimate"
    temporal=[c for c in columns if _temporal_name(c)]
    numeric={c for c in columns if (nonmissing:=[v for v in values[c] if not _missing(v)]) and all(isinstance(v,(int,float)) and not isinstance(v,bool) for v in nonmissing)}
    grouping=[]
    for col in columns:
        nonmissing=[v for v in values[col] if not _missing(v)]; unique=len(set(map(str,nonmissing)))
        base=Provenance(f"column:{col}",scan_procedure,f"n={len(table.rows)}")
        caps.append(Capability("has_field","sem",_norm(col),"observed",1.0,base))
        if col in numeric and col not in identifiers and col not in temporal:
            caps.append(Capability("numeric_measure","sem",_norm(col),scan_state,scan_confidence,base))
            caps.append(Capability("adequate_variation","qual",len(set(nonmissing))>1,scan_state,scan_confidence,base))
        meaningful_group=col not in identifiers and col not in temporal and col not in numeric and 1 < unique <= max(20,int(len(table.rows)*.8)+1)
        if meaningful_group:
            grouping.append(col); caps.append(Capability("grouping_field","str",_norm(col),"inferred",.8 if complete_table else .6,Provenance(f"column:{col}","meaningful_cardinality_heuristic",f"distinct={unique};scope={'complete' if complete_table else 'sample'}")))
        caps.append(Capability("missingness_at_most","qual",1-len(nonmissing)/len(table.rows),scan_state,scan_confidence,base))
    features=[c for c in columns if c not in identifiers and c not in temporal]
    identifier_detail=f"declared_keys={sorted(declared_keys)};inferred_identifiers={sorted(inferred_identifiers)}"
    caps.append(Capability("non_identifier_features","aff",list(map(_norm,features)),"inferred",.9,Provenance("schema","identifier_exclusion",identifier_detail))) if features else None
    if bool(columns) and not features: caps.append(Capability("identifier_only","aff",True,"inferred",.9,Provenance("schema","identifier_exclusion",identifier_detail)))
    for col in temporal:
        vals=sorted(str(v) for v in values[col] if not _missing(v))
        if vals: caps.append(Capability("temporal_coverage","cov",[vals[0],vals[-1]],scan_state,scan_confidence,Provenance(f"column:{col}","complete_min_max" if complete_table else "sample_min_max_estimate",f"n={len(vals)}")))
    repeated=False; repetition_source="schema"
    if temporal and identifiers:
        for identifier in identifiers:
            grouped={}
            for row in table.rows:
                if not _missing(row.get(identifier)): grouped.setdefault(str(row.get(identifier)),set()).update(str(row.get(t)) for t in temporal if not _missing(row.get(t)))
            if any(len(times)>1 for times in grouped.values()): repeated=True; repetition_source=f"columns:{identifier},{temporal[0]}"; break
    if repeated:
        caps.append(Capability("repeated_observations","aff",True,"inferred",.85 if complete_table else .6,Provenance(repetition_source,"entity_time_repetition_scan","complete_table" if complete_table else "sample")))
    if "geographic_coverage" in table.metadata:
        caps.append(Capability("geographic_coverage","cov",list(map(_norm,table.metadata["geographic_coverage"])),"observed",1.0,Provenance("metadata:geographic_coverage","declared_metadata","complete declaration")))
    gran,state,confidence,prov=_granularity(table,columns,identifiers,temporal,grouping); caps.append(Capability("row_granularity","str",gran,state,confidence,prov))
    return tuple(caps)

def build_profile(table: Table,knowledge_hash: str,complete_table=True) -> CapabilityProfile:
    payload={"table_id":table.table_id,"title":table.title,"description":table.description,"rows":table.rows,"metadata":table.metadata}
    checksum=sha256(json.dumps(payload,sort_keys=True,separators=(",",":"),default=list).encode()).hexdigest()
    return CapabilityProfile(table.table_id,PROFILER_VERSION,knowledge_hash,checksum,complete_table,profile_table(table,complete_table))
