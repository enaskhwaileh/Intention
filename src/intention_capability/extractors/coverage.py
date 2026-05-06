"""Coverage profiling for categorical, numeric, temporal, and geographic signals."""

from __future__ import annotations

import pandas as pd

from intention_capability.models import CoverageProfile, StructuralProfile
from intention_capability.utils.text import contains_any
from intention_capability.utils.validation import require_dataframe


GEO_TERMS = {"country", "city", "region", "state", "location", "destination"}


class CoverageExtractor:
    """Extract deterministic coverage summaries from a DataFrame."""

    def extract(
        self, df: pd.DataFrame, structural: StructuralProfile | None = None
    ) -> CoverageProfile:
        require_dataframe(df)
        categorical_columns = (
            structural.categorical_columns if structural is not None else self._categorical_columns(df)
        )
        numeric_columns = (
            structural.numeric_columns if structural is not None else self._numeric_columns(df)
        )
        date_columns = structural.date_candidates if structural is not None else []

        categorical_coverage = {
            column: int(df[column].dropna().nunique()) for column in categorical_columns
        }
        top_values = {
            column: [
                {"value": str(value), "count": int(count)}
                for value, count in df[column].dropna().value_counts().head(5).items()
            ]
            for column in categorical_columns
        }
        numeric_ranges = {
            column: {
                "min": self._float_or_none(pd.to_numeric(df[column], errors="coerce").min()),
                "max": self._float_or_none(pd.to_numeric(df[column], errors="coerce").max()),
            }
            for column in numeric_columns
        }
        temporal_ranges = {}
        for column in date_columns:
            parsed = pd.to_datetime(df[column], errors="coerce")
            temporal_ranges[column] = {
                "min": self._date_or_none(parsed.min()),
                "max": self._date_or_none(parsed.max()),
            }
        geographic_columns = [
            column for column in df.columns if contains_any(str(column), GEO_TERMS)
        ]

        return CoverageProfile(
            categorical_coverage=categorical_coverage,
            top_values=top_values,
            numeric_ranges=numeric_ranges,
            temporal_ranges=temporal_ranges,
            geographic_columns=geographic_columns,
        )

    def _categorical_columns(self, df: pd.DataFrame) -> list[str]:
        return [column for column in df.columns if not pd.api.types.is_numeric_dtype(df[column])]

    def _numeric_columns(self, df: pd.DataFrame) -> list[str]:
        return [column for column in df.columns if pd.api.types.is_numeric_dtype(df[column])]

    def _float_or_none(self, value: object) -> float | None:
        return None if pd.isna(value) else float(value)

    def _date_or_none(self, value: object) -> str | None:
        return None if pd.isna(value) else pd.Timestamp(value).date().isoformat()
