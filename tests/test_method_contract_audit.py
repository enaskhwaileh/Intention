"""Regression tests tying the normative mathematics to executable behavior."""
from pathlib import Path
import ast
import yaml
import pytest

from intention.alignment import align, match_value
from intention.contracts import Capability, Provenance, Requirement, RequirementProfile, Table
from intention.interpretation import ground, requirements
from intention.knowledge import load_knowledge
from intention.ranking import rank

ROOT = Path(__file__).parents[1]

def capability(predicate, axis, value, confidence=1.0):
    return Capability(predicate, axis, value, "observed", confidence, Provenance("test", "declared_fixture"))

def profile(kg, requirements):
    return RequirementProfile("COMPARE", tuple(requirements), kg.actions["COMPARE"].weights)

def test_knowledge_exposes_all_seven_kg_components():
    kg = load_knowledge()
    assert kg.action_catalogue
    assert kg.axes == ("sem", "str", "cov", "qual", "aff")
    assert kg.predicates
    assert kg.templates
    assert kg.matching_rules
    assert kg.axis_weights
    assert kg.validation == {"weights_sum_to_one": True, "reject_unknown_fields": True}

@pytest.mark.parametrize("parameters,expected,observed,score", [
    ({"operator":"at_most"},10,9,1),
    ({"operator":"at_least"},10,9,0),
    ({"operator":"equal"},10,10,1),
])
def test_numerical_comparison_operators(parameters,expected,observed,score):
    assert match_value("numerical",expected,observed,parameters) == score

@pytest.mark.parametrize("mode,score", [
    ("containment",0),
    ("overlap",1),
    ("containment_or_overlap",.5),
])
def test_interval_modes(mode,score):
    assert match_value("interval",("2020","2022"),("2021","2024"),{"mode":mode}) == score

def test_invalid_matching_parameters_fail_closed():
    with pytest.raises(ValueError,match="numerical operator"):
        match_value("numerical",1,1,{"operator":"approximately"})
    with pytest.raises(ValueError,match="interval mode"):
        match_value("interval",("1","2"),("1","2"),{"mode":"invented"})

@pytest.mark.parametrize("mutation,error", [
    (lambda raw: raw["predicates"]["has_field"].update({"invented": True}), "invalid predicate"),
    (lambda raw: raw["actions"]["COMPARE"]["weights"].update({"sem": -0.1}), "invalid action"),
    (lambda raw: raw["actions"]["COMPARE"]["requirements"][0].update({"invented": True}), "invalid requirement"),
    (lambda raw: raw.update({"validation": {"weights_sum_to_one": False, "reject_unknown_fields": True}}), "validation constraints"),
])
def test_nested_knowledge_schema_is_fail_closed(tmp_path, mutation, error):
    raw = yaml.safe_load((ROOT / "configs/knowledge/knowledge.yaml").read_text())
    mutation(raw); path = tmp_path / "knowledge.yaml"; path.write_text(yaml.safe_dump(raw))
    with pytest.raises(ValueError, match=error): load_knowledge(path)

def test_m_uses_maximum_compatible_capability_with_confidence():
    kg=load_knowledge(); req=Requirement("numeric_measure","sem","rate","req","test")
    score,trace=align(profile(kg,[req]),(capability("numeric_measure","sem","rate",.4),capability("numeric_measure","sem","rate",.9)),kg,eta_o=0)
    assert trace["matches"][0]["score"] == .9
    assert score == .9

def test_empty_set_conventions_and_active_axis_normalization():
    kg=load_knowledge(); optional=Requirement("missingness_at_most","qual",.2,"opt","test")
    score,trace=align(profile(kg,[optional]),(),kg,eta_o=.2)
    assert trace["axis_components"]["qual"] == {"required":1.0,"optional":0.0,"negative":0.0,"score":.8}
    assert trace["normalized_weights"] == {"qual":1.0}
    assert score == .8

def test_required_minimum_and_explicit_mean_ablation():
    kg=load_knowledge(); requirements=(Requirement("numeric_measure","sem","rate","req","test"),Requirement("has_field","sem","outcome","req","test")); caps=(capability("numeric_measure","sem","rate"),)
    default,_=align(profile(kg,requirements),caps,kg,eta_o=0)
    ablation,_=align(profile(kg,requirements),caps,kg,eta_o=0,required_aggregation="mean")
    assert default == 0 and ablation == .5
    with pytest.raises(ValueError,match="required aggregation"): align(profile(kg,requirements),caps,kg,required_aggregation="median")

def test_negative_empty_and_full_penalty_boundaries():
    kg=load_knowledge(); negative=Requirement("identifier_only","aff",True,"neg","test")
    unpenalized,_=align(profile(kg,[negative]),(),kg,eta_o=0,eta_n=1)
    penalized,_=align(profile(kg,[negative]),(capability("identifier_only","aff",True),),kg,eta_o=0,eta_n=1)
    assert unpenalized == 1 and penalized == 0

@pytest.mark.parametrize("eta_o",[0,.25,.5,.75,1])
@pytest.mark.parametrize("eta_n",[0,.25,.5,.75,1])
@pytest.mark.parametrize("confidence",[0,.2,.5,.8,1])
def test_alignment_property_scores_are_bounded(eta_o,eta_n,confidence):
    kg=load_knowledge(); reqs=(Requirement("numeric_measure","sem","rate","req","test"),Requirement("missingness_at_most","qual",.2,"opt","test"),Requirement("identifier_only","aff",True,"neg","test")); caps=(capability("numeric_measure","sem","rate",confidence),capability("missingness_at_most","qual",.1,confidence),capability("identifier_only","aff",True,confidence))
    score,_=align(profile(kg,reqs),caps,kg,eta_o=eta_o,eta_n=eta_n)
    assert 0 <= score <= 1

def test_alignment_rejects_axis_mismatch_and_unknown_predicate():
    kg=load_knowledge(); req=Requirement("numeric_measure","sem","rate","req","test")
    with pytest.raises(ValueError,match="axis mismatch"): align(profile(kg,[req]),(capability("numeric_measure","qual","rate"),),kg)
    with pytest.raises(ValueError,match="unknown capability predicate"): align(profile(kg,[req]),(capability("invented","sem","rate"),),kg)

def test_ranking_rejects_unnormalized_relevance_and_fallback_is_exact():
    kg=load_knowledge(); table=Table("T","title","description",(),{})
    with pytest.raises(ValueError,match="normalized"): rank([(table,1.1)],{"T":()},None,kg)
    result=rank([(table,.4)],{"T":()},None,kg,lambda_r=0,lambda_a=1)
    assert result[0].alignment is None and result[0].usefulness == .4

def test_existential_binding_is_schema_authorized_and_conditional_is_omitted():
    kg=load_knowledge(); text="topic predict outcome=result"
    interp=ground(text,{"action":"PREDICT","arguments":{"outcome":"result"},"topical_query":"topic","spans":[[0,len(text)]]},kg)
    assert interp.grounding.arguments["observational_unit"] == "*"
    compare_text="topic compare measure=rate comparison_dimension=country"
    compare=ground(compare_text,{"action":"COMPARE","arguments":{"measure":"rate","comparison_dimension":"country"},"topical_query":"topic","spans":[[0,len(compare_text)]]},kg)
    built=requirements(compare,kg)
    assert "geographic_coverage" not in {item.predicate for item in built.requirements}

def test_normative_modules_do_not_import_legacy_contracts():
    normative=("alignment","profiling","interpretation","retrieval","ranking","benchmarks","baselines","evaluation","reporting")
    forbidden={"intention.domain","intention.knowledge.registry","intention_mvp"}
    for package in normative:
        for path in (ROOT / "src/intention" / package).glob("*.py"):
            tree=ast.parse(path.read_text())
            imports={node.module for node in ast.walk(tree) if isinstance(node,ast.ImportFrom) and node.module}
            assert not any(any(module==name or module.startswith(name+".") for name in forbidden) for module in imports), path
