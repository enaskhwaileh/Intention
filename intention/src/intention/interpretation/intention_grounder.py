from intention.iekl.graph_store import IEKLGraph
from intention.schemas.intention import GroundedIntention, RawIntention


class IntentionGrounder:
    def __init__(self, graph: IEKLGraph) -> None:
        self.graph = graph

    def ground(self, raw_intention: RawIntention) -> GroundedIntention:
        intention_type = raw_intention.candidate_intention_type
        if not self.graph.has_intention(intention_type):
            raise ValueError(f"unsupported intention type: {intention_type}")

        return GroundedIntention(
            intention_type=intention_type,
            goal=self.graph.get_goal(intention_type),
            slots=raw_intention.slots,
            required_predicates=self.graph.get_required_predicates(intention_type),
            optional_predicates=self.graph.get_optional_predicates(intention_type),
            negative_predicates=self.graph.get_negative_predicates(intention_type),
        )
