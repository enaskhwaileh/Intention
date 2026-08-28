"""Versioned controlled benchmark loader and executor."""
from __future__ import annotations
from dataclasses import dataclass
import json
from pathlib import Path
from intention.contracts import Table
from intention.knowledge.layer import ACTIONS
from intention.pipeline import run

@dataclass(frozen=True)
class SyntheticCase:
    topic_id: str
    variant_id: str
    input_text: str
    gold_action: str
    expected_relevance_top: str
    expected_top: str
    tables: tuple[Table, ...]

def load_synthetic_benchmark(path: Path | None = None) -> tuple[str, tuple[SyntheticCase, ...]]:
    path = path or Path(__file__).resolve().parents[3] / "fixtures/synthetic_benchmark.json"
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict) or set(raw) != {"version", "topics"} or not isinstance(raw["version"], str):
        raise ValueError("invalid synthetic benchmark root")
    cases=[]; topic_ids=set(); variant_ids=set()
    for topic in raw["topics"]:
        if set(topic) != {"topic_id", "topical_query", "tables", "cases"} or topic["topic_id"] in topic_ids:
            raise ValueError("invalid or duplicate synthetic topic")
        topic_ids.add(topic["topic_id"]); tables=[]; table_ids=set()
        for item in topic["tables"]:
            if set(item) != {"table_id","title","description","metadata","rows"} or item["table_id"] in table_ids:
                raise ValueError("invalid or duplicate synthetic table")
            table_ids.add(item["table_id"]); tables.append(Table(item["table_id"],item["title"],item["description"],tuple(item["rows"]),item["metadata"]))
        if len(tables)<2 or len(topic["cases"])<2: raise ValueError("each topic needs at least two tables and variants")
        for item in topic["cases"]:
            if set(item) != {"variant_id","input","gold_action","expected_relevance_top","expected_top"} or item["variant_id"] in variant_ids or item["gold_action"] not in ACTIONS or item["expected_top"] not in table_ids or item["expected_relevance_top"] not in table_ids:
                raise ValueError("invalid synthetic case")
            if not item["input"].lower().startswith(topic["topical_query"].lower()): raise ValueError("case must preserve its topical query prefix")
            variant_ids.add(item["variant_id"]); cases.append(SyntheticCase(topic["topic_id"],item["variant_id"],item["input"],item["gold_action"],item["expected_relevance_top"],item["expected_top"],tuple(tables)))
    if set(case.gold_action for case in cases) != set(ACTIONS): raise ValueError("synthetic benchmark must cover all actions")
    return raw["version"],tuple(cases)

def run_synthetic_benchmark(path: Path | None = None) -> dict:
    version,cases=load_synthetic_benchmark(path); outputs=[]
    for case in cases:
        result=run(case.input_text,list(case.tables)); predicted_action=result["interpretation"].grounding.action if result["interpretation"].grounding else None; top=result["ranking"][0].table_id
        relevance_top=sorted(result["ranking"],key=lambda item:(-item.relevance,item.table_id))[0].table_id
        passed=predicted_action==case.gold_action and top==case.expected_top and relevance_top==case.expected_relevance_top
        outputs.append({"topic_id":case.topic_id,"variant_id":case.variant_id,"gold_action":case.gold_action,"predicted_action":predicted_action,"expected_relevance_top":case.expected_relevance_top,"relevance_top":relevance_top,"expected_top":case.expected_top,"actual_top":top,"alignment_changed_top":top!=relevance_top,"passed":passed,"ranking":[item.__dict__ for item in result["ranking"]]})
    return {"benchmark_version":version,"case_count":len(outputs),"passed":all(item["passed"] for item in outputs),"cases":outputs}
