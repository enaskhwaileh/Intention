from pathlib import Path

from intention.iekl.graph_loader import load_iekl_graph


ROOT = Path(__file__).resolve().parents[1]


def test_iekl_graph_loads_and_expands_supported_intentions():
    graph = load_iekl_graph(ROOT / "resources/iekl/intention_graph.yaml")

    assert graph.has_intention("compare")
    assert graph.has_intention("predict")
    assert graph.has_predicate("has_grouping_variable")

    compare_required = graph.get_required_predicates("compare")
    assert "has_grouping_variable" in compare_required
    assert "has_comparable_measure" in compare_required

    predict_required = graph.get_required_predicates("predict")
    assert "has_target_variable" in predict_required
    assert "has_predictor_variables" in predict_required
