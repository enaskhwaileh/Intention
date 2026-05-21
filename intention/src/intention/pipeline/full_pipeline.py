from pathlib import Path

import yaml

from intention.iekl.graph_loader import load_graph
from intention.pipeline.input_pipeline import run_input_pipeline
from intention.schemas.query import QueryInput
from intention.utils.io import read_jsonl, write_jsonl


def run_from_config(config_path: str | Path) -> list[dict]:
    config_path = Path(config_path)
    root = config_path.parents[1]
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    paths = config["paths"]
    graph = load_graph(root / paths["iekl_graph"])
    rows = read_jsonl(root / paths["inputs"])

    profiles = [
        run_input_pipeline(QueryInput(id=row["id"], text=row["text"]), graph)
        for row in rows
    ]
    write_jsonl(root / paths["operational_profiles"], profiles)
    return [profile.__dict__ for profile in profiles]
