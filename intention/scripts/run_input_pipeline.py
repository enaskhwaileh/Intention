from pathlib import Path

from intention.iekl.graph_loader import load_iekl_graph
from intention.interpretation.intention_grounder import IntentionGrounder
from intention.interpretation.profile_instantiator import ProfileInstantiator
from intention.interpretation.separator import QueryIntentionSeparator
from intention.interpretation.validator import ProfileValidator
from intention.llm.mock_client import MockLLMClient
from intention.pipeline.input_pipeline import InputInterpretationPipeline
from intention.utils.io import read_jsonl, write_jsonl


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    graph = load_iekl_graph(root / "resources/iekl/intention_graph.yaml")
    pipeline = InputInterpretationPipeline(
        separator=QueryIntentionSeparator(MockLLMClient()),
        grounder=IntentionGrounder(graph),
        instantiator=ProfileInstantiator(graph),
        validator=ProfileValidator(graph),
    )

    outputs = [
        pipeline.run(input_id=row["id"], user_input=row["text"])
        for row in read_jsonl(root / "data/inputs/example_inputs.jsonl")
    ]
    output_path = root / "data/outputs/input_pipeline_outputs.jsonl"
    write_jsonl(output_path, outputs)
    print(f"wrote {len(outputs)} input pipeline outputs to {output_path}")
