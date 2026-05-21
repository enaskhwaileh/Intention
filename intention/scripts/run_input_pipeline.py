from pathlib import Path

from intention.pipeline.full_pipeline import run_from_config


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    profiles = run_from_config(root / "configs" / "pipeline.yaml")
    print(f"wrote {len(profiles)} operational profiles")
