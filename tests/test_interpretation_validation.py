import copy,json
from pathlib import Path
import pytest
from intention.interpretation import DeterministicInterpreter,ExternalStructuredProvider,evaluate_interpreter,ground,load_normalization,load_provider,requirements
from intention.interpretation.schema import ProviderArtifact
from intention.knowledge import load_knowledge

ROOT=Path(__file__).parents[1]

def artifact(text): return DeterministicInterpreter().interpret(text)

def test_interpretation_gold_regression():
    result=evaluate_interpreter(); assert result["passed"] and result["case_count"]==12
    assert result["action"]=={"accuracy":1.0,"macro_f1":1.0}
    assert result["arguments"]=={"precision":1.0,"recall":1.0,"f1":1.0}
    assert result["grounding_accuracy"]==result["joint_frame_accuracy"]==result["provenance_span_accuracy"]==1

def test_raw_provider_artifact_is_separate_from_validated_output():
    text="topic predict outcome=result"; raw=artifact(text); interp=ground(text,raw,load_knowledge())
    assert raw.raw_response is not interp.validated_output and raw.content is not raw.raw_response
    assert interp.grounding.action=="PREDICT"

@pytest.mark.parametrize("mutation",[
    lambda content: content.update({"confidence":.99}),
    lambda content: content["arguments"].update({"invented":"x"}),
    lambda content: content["provenance"]["topic_spans"][0].update({"text":"fabricated"}),
    lambda content: content.update({"action":"VISUALIZE"}),
])
def test_malformed_or_invented_provider_output_falls_back(mutation):
    text="topic compare measure=rate, comparison dimension=country"; original=artifact(text); content=copy.deepcopy(original.content); mutation(content); bad=ProviderArtifact("test","test","1","1.0.0",content,{"untrusted":content}); interp=ground(text,bad,load_knowledge())
    assert interp.grounding is None and interp.status in {"invalid_output","invalid_arguments"}
    assert interp.topical_query=="topic" and interp.topical_status=="deterministic_fallback"
    assert interp.grounding_status in {"invalid_provider","invalid_arguments"}

@pytest.mark.parametrize("mutation",[
    lambda content: content.update({"arguments":[]}),
    lambda content: content["topical"].update({"entities":"not-an-array"}),
    lambda content: content["provenance"]["topic_spans"][0].update({"start":"0"}),
    lambda content: content["ambiguity"].update({"candidates":"COMPARE"}),
])
def test_declared_json_schema_rejects_malformed_types(mutation):
    text="topic compare measure=rate, comparison dimension=country"; content=copy.deepcopy(artifact(text).content); mutation(content)
    interpreted=ground(text,ProviderArtifact("test","test","1","1.0.0",content,content),load_knowledge())
    assert interpreted.status=="invalid_output" and interpreted.grounding_status=="invalid_provider"

def test_argument_value_must_be_supported_by_its_own_cited_span():
    text="topic compare measure=rate, comparison dimension=country"; content=copy.deepcopy(artifact(text).content)
    content["arguments"]["measure"]="country"
    interpreted=ground(text,ProviderArtifact("test","test","1","1.0.0",content,content),load_knowledge())
    assert interpreted.status=="invalid_output" and interpreted.topical_query=="topic"

def test_invalid_provider_without_safe_topic_does_not_reuse_action_input():
    text="compare measure=rate"; content=copy.deepcopy(artifact(text).content); content["arguments"]=[]
    interpreted=ground(text,ProviderArtifact("test","test","1","1.0.0",content,content),load_knowledge())
    assert interpreted.topical_query is None and interpreted.topical_fields is None
    assert interpreted.topical_status=="failed" and interpreted.grounding_status=="invalid_provider"

def test_ambiguity_and_missing_arguments_are_not_guessed():
    kg=load_knowledge(); ambiguous="topic compare and predict outcome=result"; missing="topic compare measure=rate"
    assert ground(ambiguous,artifact(ambiguous),kg).status=="fallback"
    interpreted=ground(missing,artifact(missing),kg); assert interpreted.status=="missing_required" and interpreted.grounding is None

def test_existential_binding_only_for_declared_schema_field():
    text="topic predict outcome=result"; interpreted=ground(text,artifact(text),load_knowledge())
    assert interpreted.grounding.arguments=={"outcome":"result","observational_unit":"*"}
    profile=requirements(interpreted,load_knowledge())
    assert any(req.predicate=="row_granularity" and req.expected=="*" and req.polarity=="req" for req in profile.requirements)

def test_external_provider_is_fail_closed_and_receives_schema():
    with pytest.raises(RuntimeError,match="no structured-output client"): ExternalStructuredProvider("external","model","rev").interpret("text")
    captured={}
    def client(**kwargs): captured.update(kwargs); return {"content":artifact(kwargs["text"]).content,"provider_raw":"kept"}
    output=ExternalStructuredProvider("external","model","rev",client).interpret("topic monitor measure=value")
    assert captured["schema"]["additionalProperties"] is False and output.raw_response["provider_raw"]=="kept"
    assert output.content is not output.raw_response["content"]

def test_provider_configuration_is_strict(tmp_path):
    assert isinstance(load_provider(),DeterministicInterpreter)
    raw={"schema_version":"1.0.0","provider":"external","model":"m","revision":"r","temperature":0,"raw_artifact_policy":"retain","validated_artifact_policy":"separate","invented":True}; path=tmp_path/"provider.yaml"
    import yaml; path.write_text(yaml.safe_dump(raw))
    with pytest.raises(ValueError,match="provider configuration"): load_provider(path)

def test_normalization_catalogue_is_hashed_and_aliases_unique():
    catalogue=load_normalization(); assert len(catalogue.digest)==64 and catalogue.value_aliases["annually"]=="year"
