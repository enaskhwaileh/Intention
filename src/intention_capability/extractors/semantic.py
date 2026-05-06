"""Shallow deterministic semantic profiling."""

from __future__ import annotations

from collections import Counter

import pandas as pd

from intention_capability.models import SemanticProfile
from intention_capability.utils.text import tokenize
from intention_capability.utils.validation import require_dataframe


MEASURE_TERMS = {
    "age",
    "amount",
    "count",
    "dose",
    "doses",
    "number",
    "rate",
    "risk",
    "score",
    "severity",
    "temperature",
}
DOMAIN_KEYWORDS = {
    "health": {"patient", "vaccine", "side", "effect", "adverse", "severity", "mortality"},
    "logistics": {"shipment", "warehouse", "delivery", "delivered", "destination", "storage"},
    "geography": {"country", "city", "region", "state", "location", "destination"},
}


class SemanticExtractor:
    """Extract lightweight keyword, entity, and domain signals."""

    def extract(self, df: pd.DataFrame, table_name: str = "") -> SemanticProfile:
        require_dataframe(df)
        keyword_counter: Counter[str] = Counter()
        keyword_counter.update(tokenize(table_name))
        for column in df.columns:
            keyword_counter.update(tokenize(str(column)))

        keywords = sorted(keyword_counter)
        measure_terms = sorted(
            {
                token
                for column in df.columns
                for token in tokenize(str(column))
                if token in MEASURE_TERMS or token.endswith("rate")
            }
        )
        entity_candidates = self._entity_candidates(df)
        domain_hints = [
            domain
            for domain, terms in DOMAIN_KEYWORDS.items()
            if set(keywords) & terms
        ]

        return SemanticProfile(
            keywords=keywords,
            measure_terms=measure_terms,
            entity_candidates=entity_candidates,
            domain_hints=domain_hints,
        )

    def _entity_candidates(self, df: pd.DataFrame) -> dict[str, list[str]]:
        candidates: dict[str, list[str]] = {}
        for column in df.columns:
            series = df[column]
            if pd.api.types.is_numeric_dtype(series):
                continue
            non_null = series.dropna().astype(str).str.strip()
            unique_count = int(non_null.nunique())
            if 1 < unique_count <= min(20, max(2, len(df) * 0.8)):
                candidates[column] = non_null.value_counts().head(5).index.tolist()
        return candidates
