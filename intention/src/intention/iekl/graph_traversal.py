from intention.iekl.graph_store import IEKLGraph
from intention.schemas.iekl import IEKLNode


def neighbors(graph: IEKLGraph, node_id: str) -> list[IEKLNode]:
    target_ids = [edge.target for edge in graph.edges if edge.source == node_id]
    return [graph.node_by_id(target_id) for target_id in target_ids]
