"""Run deterministic capability extraction for one CSV or a directory of CSVs."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from intention_capability.io import read_csv, save_profile_json
from intention_capability.pipeline import CapabilityExtractionPipeline


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    single = parser.add_argument_group("single file mode")
    single.add_argument("--input", type=Path, help="Path to a CSV file.")
    single.add_argument("--table-id", help="Stable identifier for the table.")
    single.add_argument("--table-name", help="Human-readable table name.")
    single.add_argument("--output", type=Path, help="Path to write the JSON profile.")

    directory = parser.add_argument_group("directory mode")
    directory.add_argument("--input-dir", type=Path, help="Directory containing CSV files.")
    directory.add_argument("--output-dir", type=Path, help="Directory for JSON profiles.")
    return parser.parse_args()


def run_single(
    pipeline: CapabilityExtractionPipeline,
    input_path: Path,
    table_id: str,
    table_name: str,
    output_path: Path,
) -> None:
    df = read_csv(input_path)
    profile = pipeline.run(
        df=df,
        table_id=table_id,
        table_name=table_name,
        metadata={"source_path": str(input_path)},
    )
    save_profile_json(profile, output_path)
    print(f"Wrote {output_path}")


def main() -> None:
    args = parse_args()
    pipeline = CapabilityExtractionPipeline()

    if args.input_dir:
        if not args.output_dir:
            raise SystemExit("--output-dir is required with --input-dir.")
        args.output_dir.mkdir(parents=True, exist_ok=True)
        for input_path in sorted(args.input_dir.glob("*.csv")):
            table_id = input_path.stem
            table_name = input_path.stem.replace("_", " ").title()
            output_path = args.output_dir / f"{table_id}.json"
            run_single(pipeline, input_path, table_id, table_name, output_path)
        return

    required = [args.input, args.table_id, args.table_name, args.output]
    if not all(required):
        raise SystemExit(
            "Single file mode requires --input, --table-id, --table-name, and --output."
        )
    run_single(pipeline, args.input, args.table_id, args.table_name, args.output)


if __name__ == "__main__":
    main()
