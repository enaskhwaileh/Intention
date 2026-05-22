from intention.iekl.graph_store import IEKLGraph
from intention.schemas.intention import GroundedIntention
from intention.schemas.profile import (
    EvidenceRequirement,
    NegativeEvidence,
    OperationalIntentionProfile,
)


class ProfileInstantiator:
    def __init__(self, graph: IEKLGraph) -> None:
        self.graph = graph

    def instantiate(
        self,
        input_id: str,
        grounded_intention: GroundedIntention,
    ) -> OperationalIntentionProfile:
        unit_of_analysis = grounded_intention.slots.get("unit_of_analysis")
        return OperationalIntentionProfile(
            input_id=input_id,
            intention_type=grounded_intention.intention_type,
            goal=grounded_intention.goal,
            unit_of_analysis=str(unit_of_analysis) if unit_of_analysis else None,
            required_evidence=[
                self._evidence_requirement(predicate, "required")
                for predicate in grounded_intention.required_predicates
            ],
            optional_evidence=[
                self._evidence_requirement(predicate, "optional")
                for predicate in grounded_intention.optional_predicates
            ],
            negative_evidence=[
                NegativeEvidence(
                    predicate=predicate,
                    reason=f"Penalize profiles where {predicate} is observed.",
                )
                for predicate in grounded_intention.negative_predicates
            ],
        )

    def _evidence_requirement(self, predicate: str, priority: str) -> EvidenceRequirement:
        spec = self.graph.get_predicate_spec(predicate)
        return EvidenceRequirement(
            predicate=predicate,
            axis=spec.axis,
            expected_evidence=[],
            reason=spec.definition,
            priority=priority,
            testable_from=spec.testable_from,
        )
