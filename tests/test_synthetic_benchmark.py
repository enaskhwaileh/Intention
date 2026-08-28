import json
from pathlib import Path
import pytest
from intention.benchmarks import load_synthetic_benchmark, run_synthetic_benchmark

ROOT=Path(__file__).parents[1]

def test_benchmark_covers_every_action_and_topic_pairs():
    version,cases=load_synthetic_benchmark(); assert version=="1.0.0"
    assert {case.gold_action for case in cases}=={"COMPARE","AGGREGATE","PREDICT","EXPLAIN","MONITOR"}
    by_topic={}
    for case in cases: by_topic.setdefault(case.topic_id,[]).append(case)
    assert len(by_topic)==3 and all(len(group)==2 for group in by_topic.values())
    assert all(len({case.expected_top for case in group})==2 for group in by_topic.values())

def test_all_gold_actions_rankings_and_relevance_controls_pass():
    result=run_synthetic_benchmark(); assert result["passed"] and result["case_count"]==6
    assert sum(case["alignment_changed_top"] for case in result["cases"])==3
    assert all(case["gold_action"]==case["predicted_action"] for case in result["cases"])

def test_action_variants_preserve_identical_topical_relevance():
    result=run_synthetic_benchmark(); grouped={}
    for case in result["cases"]:
        scores={item["table_id"]:item["relevance"] for item in case["ranking"]}; grouped.setdefault(case["topic_id"],[]).append(scores)
    assert all(values[0]==values[1] for values in grouped.values())

def test_repeatability(): assert run_synthetic_benchmark()==run_synthetic_benchmark()

def test_loader_rejects_missing_action_coverage(tmp_path):
    raw=json.loads((ROOT/"fixtures/synthetic_benchmark.json").read_text()); raw["topics"][-1]["cases"][-1]["gold_action"]="COMPARE"
    path=tmp_path/"benchmark.json"; path.write_text(json.dumps(raw))
    with pytest.raises(ValueError,match="cover all actions"): load_synthetic_benchmark(path)

def test_loader_rejects_duplicate_topic(tmp_path):
    raw=json.loads((ROOT/"fixtures/synthetic_benchmark.json").read_text()); raw["topics"].append(raw["topics"][0])
    path=tmp_path/"benchmark.json"; path.write_text(json.dumps(raw))
    with pytest.raises(ValueError,match="duplicate synthetic topic"): load_synthetic_benchmark(path)
