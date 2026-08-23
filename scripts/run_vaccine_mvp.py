#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from intention_mvp.loader import load_relevance_scores  # noqa: E402
from intention_mvp.pipeline import run_pipeline  # noqa: E402


def ranking(result) -> str:
    return " > ".join(row.table_id for row in result.ranked_tables)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the deterministic vaccine MVP")
    parser.add_argument(
        "--json-output",
        type=Path,
        help="also write the complete machine-readable result to this path",
    )
    args = parser.parse_args()
    compare = run_pipeline("compare")
    predict = run_pipeline("predict")
    relevance = sorted(load_relevance_scores(), key=load_relevance_scores().get, reverse=True)
    print(f"Relevance: {' > '.join(relevance)}")
    print(f"Compare:   {ranking(compare)}")
    print(f"Predict:   {ranking(predict)}")
    for label, result in (("Compare", compare), ("Predict", predict)):
        print(f"\n{label} explanations:")
        for row in result.ranked_tables:
            gate = "passed" if row.required_evidence_passed else "failed"
            print(
                f"  {row.table_id}: usefulness={row.usefulness_score:.3f}, "
                f"alignment={row.alignment_score:.3f}, gate={gate}"
            )
    payload = {
        "unchanged_relevance_ranking": relevance,
        "compare": compare.to_dict(),
        "predict": predict.to_dict(),
    }
    print("\nJSON:")
    print(json.dumps(payload, indent=2))
    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(
            json.dumps(payload, indent=2) + "\n", encoding="utf-8"
        )


if __name__ == "__main__":
    main()
