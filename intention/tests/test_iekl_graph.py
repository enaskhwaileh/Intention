from pathlib import Path

from intention.iekl.graph_loader import load_graph
from intention.iekl.graph_traversal import neighbors


ROOT = Path(__file__).resolve().parents[1]


def test_load_graph_and_neighbors():
    graph = load_graph(ROOT / "resources/iekl/intention_graph.yaml")

    assert graph.node_by_id("analyze_sales").label == "Analyze sales"
    assert [node.id for node in neighbors(graph, "analyze_sales")] == [
        "inspect_customers",
        "monitor_inventory",
    ]
