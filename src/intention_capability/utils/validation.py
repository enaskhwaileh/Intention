"""Validation helpers."""

from __future__ import annotations

import pandas as pd


def require_dataframe(df: pd.DataFrame) -> None:
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Expected a pandas DataFrame.")
