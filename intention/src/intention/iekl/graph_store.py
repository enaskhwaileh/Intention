from dataclasses import dataclass


@dataclass(frozen=True)
class PredicateSpec:
    id: str
    axis: str
    definition: str
    testable_from: list[str]


class IEKLGraph:
    def __init__(
        self,
        intentions: dict[str, dict[str, object]],
        predicates: dict[str, PredicateSpec],
    ) -> None:
        self.intentions = intentions
        self.predicates = predicates

    def has_intention(self, intention_type: str) -> bool:
        return intention_type in self.intentions

    def has_predicate(self, predicate: str) -> bool:
        return predicate in self.predicates

    def get_required_predicates(self, intention_type: str) -> list[str]:
        return self._get_intention_list(intention_type, "requires")

    def get_optional_predicates(self, intention_type: str) -> list[str]:
        return self._get_intention_list(intention_type, "optional_requires")

    def get_negative_predicates(self, intention_type: str) -> list[str]:
        return self._get_intention_list(intention_type, "penalizes")

    def get_predicate_spec(self, predicate: str) -> PredicateSpec:
        if predicate not in self.predicates:
            raise KeyError(f"unknown IEKL predicate: {predicate}")
        return self.predicates[predicate]

    def get_goal(self, intention_type: str) -> str:
        if intention_type not in self.intentions:
            raise KeyError(f"unknown IEKL intention: {intention_type}")
        return str(self.intentions[intention_type].get("goal", intention_type))

    def _get_intention_list(self, intention_type: str, field: str) -> list[str]:
        if intention_type not in self.intentions:
            raise KeyError(f"unknown IEKL intention: {intention_type}")
        values = self.intentions[intention_type].get(field, [])
        return list(values) if isinstance(values, list) else []
