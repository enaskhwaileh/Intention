from pathlib import Path

import yaml

from intention.interpretation.validator import validate_profile
from intention.schemas.profile import OperationalProfile
from intention.utils.io import read_jsonl, write_jsonl


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    rules = yaml.safe_load((root / "resources/iekl/validation_rules.yaml").read_text())
    rows = read_jsonl(root / "data/outputs/operational_profiles.jsonl")
    reports = [validate_profile(OperationalProfile(**row), rules) for row in rows]
    write_jsonl(root / "data/outputs/validation_reports.jsonl", reports)
    print(f"wrote {len(reports)} validation reports")
