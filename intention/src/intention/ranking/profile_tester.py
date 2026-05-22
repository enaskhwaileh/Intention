from intention.schemas.profile import OperationalIntentionProfile
from intention.schemas.table_profile import TableProfile


class ProfileTester:
    def test(
        self,
        profile: OperationalIntentionProfile,
        table_profile: TableProfile,
    ) -> dict:
        predicate_results: dict[str, bool] = {}
        evidence_items = profile.required_evidence + profile.optional_evidence

        for evidence in evidence_items:
            axis_payload = getattr(table_profile, evidence.axis)
            predicate_results[evidence.predicate] = bool(axis_payload.get(evidence.predicate))

        required = [item.predicate for item in profile.required_evidence]
        if required:
            satisfied_required = sum(1 for predicate in required if predicate_results.get(predicate))
            score = satisfied_required / len(required)
        else:
            score = 0.0

        return {
            "table_id": table_profile.table_id,
            "intention_type": profile.intention_type,
            "predicate_results": predicate_results,
            "intention_alignment_score": score,
        }
