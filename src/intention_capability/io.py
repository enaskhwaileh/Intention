"""I/O helpers for capability extraction."""

from __future__ import annotations

from dataclasses import asdict
import json
from pathlib import Path

import pandas as pd

from intention_capability.models import CapabilityProfile


def read_csv(path: str | Path) -> pd.DataFrame:
    """Read a CSV file into a DataFrame."""
    return pd.read_csv(path)


def save_profile_json(profile: CapabilityProfile, path: str | Path) -> None:
    """Serialize a capability profile to pretty JSON."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(asdict(profile), indent=2, sort_keys=True),
        encoding="utf-8",
    )
