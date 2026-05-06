"""Derive action affordances from extracted capability signals."""

from __future__ import annotations

from intention_capability.models import (
    ActionAffordanceProfile,
    CoverageProfile,
    QualityProfile,
    SemanticProfile,
    StructuralProfile,
)
from intention_capability.utils.text import contains_any


TARGET_TERMS = {
    "label",
    "outcome",
    "result",
    "status",
    "side_effect",
    "mortality",
    "risk",
}


class ActionAffordanceExtractor:
    """Assign simple action labels using deterministic rules."""

    def extract(
        self,
        semantic: SemanticProfile,
        structural: StructuralProfile,
        coverage: CoverageProfile,
        quality: QualityProfile,
    ) -> ActionAffordanceProfile:
        grouping_count = len(structural.grouping_candidates)
        measure_count = len(structural.measure_candidates)
        feature_count = structural.column_count
        target_like = [
            column
            for column in structural.inferred_column_types
            if contains_any(str(column), TARGET_TERMS)
        ]
        entity_like_columns = len(semantic.entity_candidates)

        compare = "strong" if grouping_count >= 1 and measure_count >= 1 else "possible"
        aggregate = (
            "strong"
            if measure_count >= 1
            and (grouping_count >= 1 or structural.date_candidates or structural.categorical_columns)
            else "possible"
        )
        predict = "possible" if feature_count >= 5 and target_like else "weak"
        if feature_count >= 8 and target_like:
            predict = "strong"
        join = (
            "possible"
            if structural.identifier_candidates or entity_like_columns >= 2
            else "weak"
        )
        explain = "moderate" if feature_count >= 5 and target_like else "weak"

        return ActionAffordanceProfile(
            compare=compare,
            aggregate=aggregate,
            predict=predict,
            join=join,
            explain=explain,
        )
