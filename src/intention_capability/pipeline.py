"""Capability extraction pipeline orchestration."""

from __future__ import annotations

from typing import Any

import pandas as pd

from intention_capability.extractors import (
    ActionAffordanceExtractor,
    CoverageExtractor,
    QualityExtractor,
    SemanticExtractor,
    StructuralExtractor,
)
from intention_capability.models import CapabilityProfile
from intention_capability.utils.validation import require_dataframe


class CapabilityExtractionPipeline:
    """Run all Version 0 capability extractors for a table."""

    def __init__(self) -> None:
        self.semantic_extractor = SemanticExtractor()
        self.structural_extractor = StructuralExtractor()
        self.coverage_extractor = CoverageExtractor()
        self.quality_extractor = QualityExtractor()
        self.action_affordance_extractor = ActionAffordanceExtractor()

    def run(
        self,
        df: pd.DataFrame,
        table_id: str,
        table_name: str,
        metadata: dict[str, Any] | None = None,
    ) -> CapabilityProfile:
        require_dataframe(df)
        structural = self.structural_extractor.extract(df)
        semantic = self.semantic_extractor.extract(df, table_name=table_name)
        coverage = self.coverage_extractor.extract(df, structural=structural)
        quality = self.quality_extractor.extract(df)
        action_affordance = self.action_affordance_extractor.extract(
            semantic=semantic,
            structural=structural,
            coverage=coverage,
            quality=quality,
        )

        return CapabilityProfile(
            table_id=table_id,
            table_name=table_name,
            semantic=semantic,
            structural=structural,
            coverage=coverage,
            quality=quality,
            action_affordance=action_affordance,
            metadata=metadata or {},
        )
