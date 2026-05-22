from intention.iekl.graph_store import IEKLGraph


def expanded_predicates(graph: IEKLGraph, intention_type: str) -> dict[str, list[str]]:
    return {
        "required": graph.get_required_predicates(intention_type),
        "optional": graph.get_optional_predicates(intention_type),
        "negative": graph.get_negative_predicates(intention_type),
    }
