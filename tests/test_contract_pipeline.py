import json
from pathlib import Path
import pytest
from intention.__main__ import fixture
from intention.alignment import align, match_value
from intention.contracts import Capability, Provenance
from intention.interpretation import DeterministicInterpreter, ground, requirements
from intention.knowledge import load_knowledge
from intention.pipeline import run

@pytest.mark.parametrize("kind,expected,observed,score",[
 ("exact",True,True,1),("normalized","Side_Effect","side effect",1),
 ("semantic","vaccine adverse events","adverse events",2/3),
 ("numerical",.2,.1,1),("set_containment",["italy"],["italy","france"],1),
 ("interval",("2020","2022"),("2019","2023"),1),
 ("interval",("2020","2022"),("2021","2024"),.5),
 ("granularity","month","week",.5),("existential","*",["age"],1)])
def test_matching_rules(kind,expected,observed,score): assert match_value(kind,expected,observed)==pytest.approx(score)

def test_unknown_rule_rejected():
    with pytest.raises(ValueError): match_value("invented",1,1)

def test_knowledge_exact_vocabulary_and_hash():
    kg=load_knowledge(); assert set(kg.actions)=={"COMPARE","AGGREGATE","PREDICT","EXPLAIN","MONITOR"}; assert len(kg.digest)==64

def test_grounding_rejects_missing_and_invented_arguments():
    kg=load_knowledge(); text="topic compare"
    assert ground(text,{"action":"COMPARE","arguments":{},"topical_query":"topic","spans":[[0,5]]},kg).grounding is None
    assert ground(text,{"action":"COMPARE","arguments":{"measure":"x","comparison_dimension":"g","invented":1},"topical_query":"topic","spans":[[0,5]]},kg).grounding is None

def test_unknown_action_falls_back_to_relevance():
    result=run("vaccine side effects",fixture())
    assert result["requirements"] is None
    assert all(x.alignment is None and x.usefulness==x.relevance for x in result["ranking"])

def test_deterministic_and_action_reversal():
    compare="vaccine side effects compare measure=rate, comparison dimension=country"
    predict="vaccine side effects predict outcome=outcome"
    a=run(compare,fixture()); b=run(compare,fixture()); p=run(predict,fixture())
    assert a["ranking"]==b["ranking"]
    assert a["ranking"][0].table_id=="country_rates"
    assert p["ranking"][0].table_id=="patient_records"

def test_scores_bounded_and_negative_requirement_penalizes():
    kg=load_knowledge(); text="topic predict outcome=outcome"; raw=DeterministicInterpreter().interpret(text); req=requirements(ground(text,raw,kg),kg)
    caps=(Capability("has_field","sem","outcome","observed",1,Provenance("x","x")),Capability("non_identifier_features","aff",("age",),"observed",1,Provenance("x","x")),Capability("adequate_variation","qual",True,"observed",1,Provenance("x","x")),Capability("identifier_only","aff",True,"observed",1,Provenance("x","x")))
    penalized,_=align(req,caps,kg,eta_n=1); unpenalized,_=align(req,caps,kg,eta_n=0)
    assert 0<=penalized<=unpenalized<=1
