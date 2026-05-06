"""Small text normalization helpers."""

from __future__ import annotations

import re


TOKEN_PATTERN = re.compile(r"[A-Za-z][A-Za-z0-9]*")


def normalize_name(value: str) -> str:
    """Normalize a table or column name for deterministic matching."""
    return value.strip().lower().replace("-", "_").replace(" ", "_")


def tokenize(value: str) -> list[str]:
    """Extract simple lowercase tokens from names or short labels."""
    return [match.group(0).lower() for match in TOKEN_PATTERN.finditer(value)]


def contains_any(value: str, terms: set[str]) -> bool:
    tokens = set(tokenize(value))
    normalized = normalize_name(value)
    return bool(tokens & terms) or any(term in normalized for term in terms)
