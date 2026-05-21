from intention.iekl.graph_store import IEKLGraph
from intention.schemas.intention import RawIntention
from intention.schemas.profile import OperationalProfile
from intention.schemas.query import QueryProfile


def instantiate_profile(
    query_profile: QueryProfile,
    raw_intention: RawIntention,
    graph: IEKLGraph,
) -> OperationalProfile:
    node = graph.node_by_id(raw_intention.intention_id)
    entities = sorted(set(query_profile.tokens).intersection(node.keywords))
    return OperationalProfile(
        input_id=query_profile.input_id,
        intention_id=raw_intention.intention_id,
        profile_type=node.profile_type,
        entities=entities,
        confidence=raw_intention.confidence,
    )
