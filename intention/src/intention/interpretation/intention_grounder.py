from intention.iekl.graph_store import IEKLGraph
from intention.schemas.intention import RawIntention
from intention.schemas.query import QueryProfile


def ground_intention(profile: QueryProfile, graph: IEKLGraph) -> RawIntention:
    best_node = graph.nodes[0]
    best_overlap = -1
    token_set = set(profile.tokens)

    for node in graph.nodes:
        overlap = len(token_set.intersection(node.keywords))
        if overlap > best_overlap:
            best_node = node
            best_overlap = overlap

    confidence = min(1.0, max(0.1, best_overlap / max(1, len(best_node.keywords))))
    return RawIntention(
        input_id=profile.input_id,
        intention_id=best_node.id,
        label=best_node.label,
        confidence=confidence,
    )
