"""Deterministic quality profiling for tabular datasets."""

from __future__ import annotations

import pandas as pd

from intention_capability.models import QualityProfile
from intention_capability.utils.validation import require_dataframe


class QualityExtractor:
    """Extract basic completeness, uniqueness, and duplication signals."""

    def extract(self, df: pd.DataFrame) -> QualityProfile:
        require_dataframe(df)
        row_count = len(df)
        if row_count == 0:
            rates = {column: 0.0 for column in df.columns}
            return QualityProfile(
                missing_rate_per_column=rates,
                unique_ratio_per_column=rates.copy(),
                empty_string_rate_per_column=rates.copy(),
            )

        missing = {column: float(df[column].isna().mean()) for column in df.columns}
        duplicate_rate = float(df.duplicated().mean())
        unique_ratios = {
            column: float(df[column].dropna().nunique() / row_count) for column in df.columns
        }
        constant_columns = [
            column for column in df.columns if int(df[column].dropna().nunique()) <= 1
        ]
        empty_string_rates = {
            column: float(df[column].astype("string").str.strip().eq("").fillna(False).mean())
            for column in df.columns
        }

        return QualityProfile(
            missing_rate_per_column=missing,
            duplicate_row_rate=duplicate_rate,
            unique_ratio_per_column=unique_ratios,
            constant_columns=constant_columns,
            empty_string_rate_per_column=empty_string_rates,
        )
