#!/usr/bin/env python3
"""Verify the minimum offline environment and registry contracts."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from intention import __version__  # noqa: E402
from intention.knowledge import load_action_registry, load_predicate_registry  # noqa: E402


def main() -> int:
    predicates = load_predicate_registry()
    actions = load_action_registry(predicate_registry=predicates)
    payload = {
        "package_version": __version__,
        "python": sys.version.split()[0],
        "python_supported": sys.version_info >= (3, 10),
        "predicate_registry_version": predicates.version,
        "predicate_count": len(predicates.predicates),
        "action_registry_version": actions.version,
        "actions": sorted(action.value for action in actions.actions),
        "relation_axis_active": False,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["python_supported"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
