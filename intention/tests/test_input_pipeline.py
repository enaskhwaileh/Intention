from pathlib import Path

from intention.iekl.graph_loader import load_iekl_graph
from intention.interpretation.intention_grounder import IntentionGrounder
from intention.interpretation.profile_instantiator import ProfileInstantiator
from intention.interpretation.separator import QueryIntentionSeparator
from intention.interpretation.validator import ProfileValidator
from intention.llm.mock_client import MockLLMClient
from intention.pipeline.input_pipeline import InputInterpretationPipeline


ROOT = Path(__file__).resolve().parents[1]


def _pipeline() -> InputInterpretationPipeline:
    graph = load_iekl_graph(ROOT / "resources/iekl/intention_graph.yaml")
    return InputInterpretationPipeline(
        separator=QueryIntentionSeparator(MockLLMClient()),
        grounder=IntentionGrounder(graph),
        instantiator=ProfileInstantiator(graph),
        validator=ProfileValidator(graph),
    )


def test_pipeline_detects_supported_intentions_and_returns_artifacts():
    examples = [
        ("q1", "Show revenue by customer segment for last quarter", "aggregate"),
        (
            "q2",
            "Compare COVID-19 vaccine side effects between Pfizer and Moderna across European countries.",
            "compare",
        ),
        ("q3", "Predict hospital readmission risk using patient records.", "predict"),
        ("q4", "Explain why unemployment differs across European regions.", "explain"),
        ("q5", "Integrate hospital records with regional demographic data.", "integrate"),
    ]
    pipeline = _pipeline()

    for input_id, user_input, expected_type in examples:
        output = pipeline.run(input_id=input_id, user_input=user_input)

        assert output["raw_intention"]["candidate_intention_type"] == expected_type
        assert output["grounded_intention"]["intention_type"] == expected_type
        assert output["operational_intention_profile"]["validation_status"] == "valid"
        assert "query_profile" in output
        assert "raw_intention" in output
        assert "grounded_intention" in output
        assert "operational_intention_profile" in output
