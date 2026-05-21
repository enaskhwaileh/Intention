from intention.iekl.graph_store import IEKLGraph
from intention.interpretation.intention_grounder import ground_intention
from intention.interpretation.profile_instantiator import instantiate_profile
from intention.interpretation.separator import separate_query
from intention.schemas.profile import OperationalProfile
from intention.schemas.query import QueryInput


def run_input_pipeline(query: QueryInput, graph: IEKLGraph) -> OperationalProfile:
    query_profile = separate_query(query)
    raw_intention = ground_intention(query_profile, graph)
    return instantiate_profile(query_profile, raw_intention, graph)
