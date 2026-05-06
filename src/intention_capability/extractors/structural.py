"""Deterministic structural profiling for tabular datasets."""

from __future__ import annotations

from dateutil.parser import parse
import pandas as pd

from intention_capability.models import StructuralProfile
from intention_capability.utils.text import contains_any, normalize_name
from intention_capability.utils.validation import require_dataframe


ID_TERMS = {"id", "identifier", "uuid", "code", "key"}
DATE_TERMS = {"date", "time", "year", "month", "day", "timestamp"}
MEASURE_TERMS = {
    "amount",
    "count",
    "dose",
    "doses",
    "number",
    "rate",
    "ratio",
    "score",
    "severity",
    "temperature",
    "total",
    "value",
}


class StructuralExtractor:
    """Extract inspectable structural signals from a DataFrame."""

    def extract(self, df: pd.DataFrame) -> StructuralProfile:
        require_dataframe(df)
        row_count = len(df)
        inferred_types: dict[str, str] = {}
        numeric_columns: list[str] = []
        categorical_columns: list[str] = []
        date_candidates: list[str] = []
        identifier_candidates: list[str] = []
        grouping_candidates: list[str] = []
        measure_candidates: list[str] = []

        for column in df.columns:
            series = df[column]
            normalized = normalize_name(str(column))
            non_null = series.dropna()
            unique_count = int(non_null.nunique())
            unique_ratio = unique_count / row_count if row_count else 0.0

            if pd.api.types.is_numeric_dtype(series):
                inferred_type = "numeric"
                numeric_columns.append(column)
            elif pd.api.types.is_bool_dtype(series):
                inferred_type = "boolean"
                categorical_columns.append(column)
            elif self._looks_like_date(column, non_null):
                inferred_type = "date"
                date_candidates.append(column)
            else:
                inferred_type = "categorical" if unique_ratio <= 0.8 else "text"
                if inferred_type == "categorical":
                    categorical_columns.append(column)

            if contains_any(normalized, ID_TERMS) or normalized.endswith("_id"):
                identifier_candidates.append(column)
            if inferred_type == "numeric" and (
                contains_any(normalized, MEASURE_TERMS) or unique_count > 2
            ):
                measure_candidates.append(column)
            if inferred_type == "date" and column not in date_candidates:
                date_candidates.append(column)
            if (
                inferred_type in {"categorical", "boolean", "date"}
                and column not in identifier_candidates
                and 1 < unique_count <= max(20, row_count * 0.7)
            ):
                grouping_candidates.append(column)

            inferred_types[column] = inferred_type

        return StructuralProfile(
            row_count=row_count,
            column_count=len(df.columns),
            inferred_column_types=inferred_types,
            numeric_columns=numeric_columns,
            categorical_columns=categorical_columns,
            date_candidates=date_candidates,
            identifier_candidates=identifier_candidates,
            grouping_candidates=grouping_candidates,
            measure_candidates=measure_candidates,
        )

    def _looks_like_date(self, column: object, series: pd.Series) -> bool:
        if contains_any(str(column), DATE_TERMS):
            return True
        sample = series.astype(str).head(8).tolist()
        if not sample:
            return False
        parsed = 0
        for value in sample:
            try:
                parse(value, fuzzy=False)
                parsed += 1
            except (ValueError, OverflowError, TypeError):
                continue
        return parsed >= max(2, int(len(sample) * 0.7))
