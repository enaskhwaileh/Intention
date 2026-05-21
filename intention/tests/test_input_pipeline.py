from pathlib import Path

from intention.iekl.graph_loader import load_graph
from intention.pipeline.input_pipeline import run_input_pipeline
from intention.schemas.query import QueryInput


ROOT = Path(__file__).resolve().parents[1]


def test_input_pipeline_creates_operational_profile():
    graph = load_graph(ROOT / "resources/iekl/intention_graph.yaml")
    profile = run_input_pipeline(QueryInput(id="q1", text="show sales revenue"), graph)

    assert profile.input_id == "q1"
    assert profile.intention_id == "analyze_sales"
    assert "sales" in profile.entities
