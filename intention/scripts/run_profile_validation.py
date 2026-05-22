from pathlib import Path

from intention.pipeline.full_pipeline import run_from_paths


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    outputs = run_from_paths(
        input_path=root / "data/inputs/example_inputs.jsonl",
        graph_path=root / "resources/iekl/intention_graph.yaml",
        output_path=root / "data/outputs/input_pipeline_outputs.jsonl",
    )
    print(f"wrote {len(outputs)} validated operational profiles")
