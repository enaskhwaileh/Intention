from __future__ import annotations

import json
from pathlib import Path
from typing import Any


PACKAGE_ROOT = Path(__file__).resolve().parents[2]
CONFIG_ROOT = PACKAGE_ROOT / "configs"
FIXTURE_ROOT = PACKAGE_ROOT / "fixtures"


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_action_catalogue() -> dict[str, Any]:
    return load_json(CONFIG_ROOT / "actions.json")


def load_scoring_config() -> dict[str, Any]:
    return load_json(CONFIG_ROOT / "scoring.json")


def load_vaccine_fixture() -> dict[str, Any]:
    return load_json(FIXTURE_ROOT / "vaccine_mvp.json")
