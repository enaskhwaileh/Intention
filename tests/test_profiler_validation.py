import json
from pathlib import Path
import pytest
from intention.benchmarks import load_synthetic_benchmark
from intention.knowledge import load_knowledge
from intention.profiling import CapabilityRepository,build_profile,evaluate_profiles,load_gold_annotations,profile_table

ROOT=Path(__file__).parents[1]

def corpus():
    _,cases=load_synthetic_benchmark(); return {table.table_id:table for case in cases for table in case.tables}

def test_gold_is_complete_strict_and_knowledge_bound():
    kg=load_knowledge(); gold=load_gold_annotations(ROOT/"fixtures/synthetic_capability_gold.json",kg)
    assert len(gold.tables)==6 and all(len(table.capabilities)==10 for table in gold.tables)
    assert {table.table_id for table in gold.tables}==set(corpus())

def test_gold_rejects_unknown_as_false_value(tmp_path):
    kg=load_knowledge(); raw=json.loads((ROOT/"fixtures/synthetic_capability_gold.json").read_text()); item=raw["tables"][2]["capabilities"][4]; item["value"]=False
    path=tmp_path/"gold.json"; path.write_text(json.dumps(raw))
    with pytest.raises(ValueError,match="must be null"): load_gold_annotations(path,kg)

def test_gold_rejects_missing_predicate(tmp_path):
    kg=load_knowledge(); raw=json.loads((ROOT/"fixtures/synthetic_capability_gold.json").read_text()); raw["tables"][0]["capabilities"].pop()
    path=tmp_path/"gold.json"; path.write_text(json.dumps(raw))
    with pytest.raises(ValueError,match="every predicate"): load_gold_annotations(path,kg)

def test_profile_repository_round_trip_and_immutability(tmp_path):
    kg=load_knowledge(); table=next(iter(corpus().values())); profile=build_profile(table,kg.digest); repository=CapabilityRepository(tmp_path); path=repository.save(profile)
    assert repository.load(table.table_id)==profile and json.loads(path.read_text())["profiler_version"]=="2.0.0"
    changed=build_profile(type(table)(table.table_id,table.title+" changed",table.description,table.rows,table.metadata),kg.digest)
    with pytest.raises(FileExistsError): repository.save(changed)

def test_identifier_columns_are_not_numeric_measures():
    from intention.contracts import Table
    caps=profile_table(Table("ids","","",({"record_id":1,"value":2.0},{"record_id":2,"value":3.0}),{})); measures={cap.value for cap in caps if cap.predicate=="numeric_measure"}
    assert measures=={"value"}

def test_repetition_requires_same_entity_across_time():
    from intention.contracts import Table
    shared_dates=Table("shared","","",({"entity_id":"a","date":"2020-01-01","value":1},{"entity_id":"b","date":"2020-01-01","value":2}),{})
    longitudinal=Table("long","","",({"entity_id":"a","date":"2020-01-01","value":1},{"entity_id":"a","date":"2020-01-02","value":2}),{})
    assert not any(cap.predicate=="repeated_observations" for cap in profile_table(shared_dates))
    assert any(cap.predicate=="repeated_observations" for cap in profile_table(longitudinal))

def test_sample_statistics_are_estimated_and_keys_are_distinguished():
    from intention.contracts import Table
    table=Table("sample","","",({"declared":1,"record_id":10,"value":2.0},{"declared":2,"record_id":11,"value":3.0}),{"primary_key":["declared"]})
    caps=profile_table(table,complete_table=False); statistics=[cap for cap in caps if cap.predicate in {"missingness_at_most","adequate_variation","temporal_coverage"}]
    assert statistics and all(cap.state=="estimated" and cap.confidence==.7 for cap in statistics)
    feature=next(cap for cap in caps if cap.predicate=="non_identifier_features")
    assert "declared_keys=['declared']" in feature.provenance.detail and "inferred_identifiers=['record_id']" in feature.provenance.detail

def test_synthetic_profiler_gold_metrics_regression():
    kg=load_knowledge(); gold=load_gold_annotations(ROOT/"fixtures/synthetic_capability_gold.json",kg); metrics=evaluate_profiles(gold,{key:profile_table(value) for key,value in corpus().items()})
    assert metrics["predicate_macro_f1"]==1
    assert metrics["macro_predicate_count"]==9
    assert metrics["value_macro_score"]==1
    assert metrics["provenance_validity"]==1
    assert metrics["excluded_judgments"]=={"unknown":4,"not_applicable":0}
    assert metrics["row_granularity"]=={"kind_accuracy":1,"aggregation_accuracy":1,"field_macro_f1":1,"exact_accuracy":1}
