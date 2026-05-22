from pathlib import Path

from intention.iekl.graph_loader import load_iekl_graph
from intention.interpretation.intention_grounder import IntentionGrounder
from intention.interpretation.profile_instantiator import ProfileInstantiator
from intention.interpretation.separator import QueryIntentionSeparator
from intention.interpretation.validator import ProfileValidator
from intention.llm.mock_client import MockLLMClient
from intention.pipeline.input_pipeline import InputInterpretationPipeline
from intention.utils.io import read_jsonl, write_jsonl


def build_pipeline(graph_path: str | Path) -> InputInterpretationPipeline:
    graph = load_iekl_graph(graph_path)
    return InputInterpretationPipeline(
        separator=QueryIntentionSeparator(MockLLMClient()),
        grounder=IntentionGrounder(graph),
        instantiator=ProfileInstantiator(graph),
        validator=ProfileValidator(graph),
    )


def run_rows(rows: list[dict], graph_path: str | Path) -> list[dict]:
    pipeline = build_pipeline(graph_path)
    return [pipeline.run(input_id=row["id"], user_input=row["text"]) for row in rows]


def run_from_paths(input_path: str | Path, graph_path: str | Path, output_path: str | Path) -> list[dict]:
    outputs = run_rows(read_jsonl(input_path), graph_path)
    write_jsonl(output_path, outputs)
    return outputs
