"""Deterministic, credential-free milestone demonstration artifacts."""
from __future__ import annotations

from dataclasses import asdict
from hashlib import sha256
import json
from pathlib import Path

from intention.__main__ import fixture
from intention.alignment import align
from intention.interpretation import DeterministicInterpreter,ground,requirements
from intention.knowledge import load_knowledge
from intention.profiling import profile_table
from intention.ranking import rank
from intention.retrieval import BM25Retriever

SNAPSHOT_SCHEMA_VERSION="1.0.0"
CURRENT_MILESTONE=4
CURRENT_PIPELINE_COMMIT="6d9109c7e76a70e0fd005a43f7b7c9a859c525e6"
DEFAULT_INPUT="vaccine side effects compare measure=rate, comparison dimension=country"

def create_snapshot(text: str=DEFAULT_INPUT,root: Path|None=None,implementation_commit: str|None=None,milestone: int=CURRENT_MILESTONE) -> dict:
    root=root or Path(__file__).resolve().parents[2]
    kg=load_knowledge(); tables=fixture(); artifact=DeterministicInterpreter().interpret(text)
    interpretation=ground(text,artifact,kg); requirement_profile=requirements(interpretation,kg)
    candidates=[] if interpretation.topical_query is None else BM25Retriever().retrieve(interpretation.topical_query,tables,20)
    profiles={table.table_id:profile_table(table) for table in tables}
    alignments={}
    if requirement_profile is not None:
        for table,_ in candidates:
            score,diagnostics=align(requirement_profile,profiles[table.table_id],kg)
            alignments[table.table_id]={"score":score,"diagnostics":diagnostics}
    ranking=rank(candidates,profiles,requirement_profile,kg)
    stages={
        "user_input":{"text":text},
        "topical_interpretation":{
            "query":interpretation.topical_query,
            "fields":getattr(interpretation,"topical_fields",{"query":interpretation.topical_query}),
            "status":getattr(interpretation,"topical_status","available"),
            "provenance_spans":[list(span) for span in interpretation.provenance],
        },
        "grounded_action":None if interpretation.grounding is None else asdict(interpretation.grounding),
        "requirements":None if requirement_profile is None else asdict(requirement_profile),
        "retrieved_candidates":[{"table_id":table.table_id,"relevance":score} for table,score in candidates],
        "capability_profiles":{key:[asdict(capability) for capability in value] for key,value in sorted(profiles.items())},
        "alignment":alignments,
        "final_ranking":[asdict(item) for item in ranking],
    }
    stage_digest=sha256(json.dumps(stages,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    return {
        "snapshot_schema_version":SNAPSHOT_SCHEMA_VERSION,
        "milestone":{"number":milestone,"label":f"milestone_{milestone:02d}"},
        "classification":{
            "dataset":"synthetic_demo",
            "paper_result":False,
            "notice":"Demonstration output only; not a paper result.",
        },
        "provenance":{
            "implementation_commit":implementation_commit or CURRENT_PIPELINE_COMMIT,
            "knowledge_version":kg.version,
            "knowledge_hash":kg.digest,
            "provider":"deterministic",
            "generator":"python -m intention demo-snapshot",
        },
        "stage_order":list(stages),
        "stages":stages,
        "stage_digest":stage_digest,
    }

def write_current_snapshot(root: Path|None=None,check: bool=False) -> Path:
    root=root or Path(__file__).resolve().parents[2]
    target=root/"demo_snapshots"/f"milestone_{CURRENT_MILESTONE:02d}"/"snapshot.json"
    rendered=json.dumps(create_snapshot(root=root),indent=2,sort_keys=False)+"\n"
    if check:
        if not target.exists() or target.read_text()!=rendered:
            raise RuntimeError(f"demo snapshot is stale: {target}")
        return target
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(rendered)
    return target
