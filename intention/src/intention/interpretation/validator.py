from intention.iekl.graph_store import IEKLGraph
from intention.schemas.profile import OperationalIntentionProfile


ALLOWED_AXES = {"semantic", "structural", "coverage", "quality", "behavioral"}


class ProfileValidator:
    def __init__(self, graph: IEKLGraph) -> None:
        self.graph = graph

    def validate(
        self,
        profile: OperationalIntentionProfile,
    ) -> OperationalIntentionProfile:
        errors: list[str] = []

        if not self.graph.has_intention(profile.intention_type):
            errors.append(f"unsupported intention type: {profile.intention_type}")

        if not profile.required_evidence:
            errors.append("required_evidence must not be empty")

        for evidence in profile.required_evidence:
            self._validate_evidence(evidence.predicate, evidence.axis, evidence.priority, "required", errors)

        for evidence in profile.optional_evidence:
            self._validate_evidence(evidence.predicate, evidence.axis, evidence.priority, "optional", errors)

        return profile.model_copy(
            update={
                "validation_status": "invalid" if errors else "valid",
                "validation_errors": errors,
            }
        )

    def _validate_evidence(
        self,
        predicate: str,
        axis: str,
        actual_priority: str,
        expected_priority: str,
        errors: list[str],
    ) -> None:
        if not self.graph.has_predicate(predicate):
            errors.append(f"unsupported predicate: {predicate}")
        if axis not in ALLOWED_AXES:
            errors.append(f"unsupported axis for {predicate}: {axis}")
        if actual_priority != expected_priority:
            errors.append(
                f"{predicate} priority must be {expected_priority}, got {actual_priority}"
            )
