"""One-command interpreter -> grounder -> profiler -> conservative aligner pipeline."""
import argparse
import json
from datetime import datetime, timezone
from importlib.resources import files
from pathlib import Path
import uuid

from .action_base import CANONICAL_IL_PATH, load_intention_library
from .aligner import compare_card
from .grounder import GroqGrounderProvider, ReplayGrounderProvider, ground
from .groq_config import groq_model_id
from .interpreter.core import interpret
from .interpreter.providers import GroqProvider, ReplayProvider, list_available_models
from .provider_errors import provider_diagnostic
from .profiler import profile_paths


def _write(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _offline_inputs():
    replay = json.loads(files("intention_grounding.interpreter").joinpath("fixtures/replay.json").read_text())
    case = replay[2]  # compare.time: complete canonical required roles and exact evidence.
    doc = json.loads(case["raw_response"])
    refs, evidence = {}, []
    for index, argument in enumerate(doc["actions"][0]["arguments"]):
        refs.setdefault(argument["role"], []).append({"action_id": "a1", "argument_index": index})
        evidence.extend(argument["value"]["evidence"])
    proposal = {"ab_version": "0.1.0-draft", "input_id": doc["input_id"],
                "action_id": "compare.time", "bindings": refs, "evidence": list(dict.fromkeys(evidence))}
    return case["input_id"], case["input"], ReplayProvider(case["raw_response"]), ReplayGrounderProvider(json.dumps(proposal))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("offline", "groq"), default="offline")
    parser.add_argument("--input-id", default="live-input-1")
    parser.add_argument("--input", help="Natural-language request; required in groq mode")
    parser.add_argument("--model", help="Groq model ID; overrides GROQ_MODEL_ID")
    parser.add_argument("--list-models", action="store_true",
                        help="List model IDs visible to GROQ_API_KEY; makes one authenticated API call")
    parser.add_argument("--dataset", action="append", type=Path, help="Local CSV/JSON table (repeatable)")
    parser.add_argument("--dataset-metadata", type=Path, help="JSON provenance record for supplied tables")
    parser.add_argument("--max-tables", type=int, default=None)
    parser.add_argument("--output", type=Path, default=Path("outputs/pipeline"))
    parser.add_argument("--il", "--ab", dest="il", type=Path, default=CANONICAL_IL_PATH,
                        help="Intention Library JSON path (--ab is a compatibility alias)")
    args = parser.parse_args(argv)
    if args.list_models:
        try:
            for model_id in list_available_models():
                print(model_id)
        except Exception as exc:
            diagnostic = provider_diagnostic(exc)
            label = diagnostic.get("error_code", diagnostic["exception_type"])
            status = diagnostic.get("http_status")
            print(f"model_list_error={label}" + (f" http_status={status}" if status else ""))
            return 2
        return 0
    if args.mode == "groq" and not args.input:
        parser.error("--input is required in groq mode")
    if args.mode == "groq":
        try:
            model = groq_model_id(args.model)
        except Exception as exc:
            diagnostic = provider_diagnostic(exc)
            print(f"configuration_error={diagnostic.get('error_code', diagnostic['exception_type'])}")
            return 2
    if args.max_tables is not None and args.max_tables < 1:
        parser.error("--max-tables must be positive")
    ab = load_intention_library(args.il)
    if args.mode == "offline":
        input_id, user_input, interpreter_provider, grounder_provider = _offline_inputs()
    else:
        input_id, user_input = args.input_id, args.input
        interpreter_provider, grounder_provider = GroqProvider(model=model), GroqGrounderProvider(model=model)
    run_id = "run-" + uuid.uuid4().hex[:12]
    output = args.output / run_id
    output.mkdir(parents=True, exist_ok=False)
    interpreted = interpret(input_id, user_input, interpreter_provider)
    grounded = ground(interpreted, ab, grounder_provider, run_id=run_id)
    paths = sorted(args.dataset or [Path(files("intention_grounding").joinpath("fixtures/offline_table.csv"))], key=str)
    if args.max_tables is not None:
        paths = paths[:args.max_tables]
    if args.dataset_metadata:
        source_metadata = json.loads(args.dataset_metadata.read_text(encoding="utf-8"))
    else:
        metadata_name = "wikidbs10k-source-metadata.json" if args.dataset else "offline-source-metadata.json"
        source_metadata = json.loads(files("intention_grounding").joinpath("fixtures", metadata_name).read_text())
    if not isinstance(source_metadata.get("dataset_id"), str) or not source_metadata["dataset_id"]:
        parser.error("dataset metadata must contain a nonempty dataset_id")
    profiles = profile_paths(paths, dataset_id=source_metadata["dataset_id"], source_metadata=source_metadata)
    comparison = compare_card(grounded["grounded_card"], profiles)
    (output / "interpreter.raw.txt").write_text(interpreted["raw_response"] or "", encoding="utf-8")
    _write(output / "interpretation.json", {k: v for k, v in interpreted.items() if k != "raw_response"})
    (output / "grounder.raw.txt").write_text(grounded["raw_response"] or "", encoding="utf-8")
    _write(output / "grounding.json", {k: v for k, v in grounded.items() if k != "raw_response"})
    _write(output / "table-profiles.json", profiles)
    _write(output / "comparison.json", comparison)
    manifest = {"run_id": run_id, "created_at": datetime.now(timezone.utc).isoformat(), "mode": args.mode,
                "ab_path": str(args.il), "ab_version": ab["ab_version"], "input_id": input_id,
                "tables": [str(path) for path in paths], "artifact_directory": str(output)}
    _write(output / "run.json", manifest)
    states = {table["overall_state"] for table in comparison["tables"]}
    print(f"run_id={run_id} interpretation={interpreted['failure'] or interpreted['interpretation']['status']} "
          f"grounding={grounded['status']} tables={len(profiles)} alignment={','.join(sorted(states)) or 'not_run'}")
    print(f"artifacts={output}")
    for stage, result in (("interpreter", interpreted), ("grounder", grounded)):
        diagnostic = result.get("provider_error")
        if diagnostic:
            label = diagnostic.get("error_code", diagnostic["exception_type"])
            status = diagnostic.get("http_status")
            print(f"{stage}_provider_error={label}" + (f" http_status={status}" if status else ""))
    return 0 if grounded["status"] == "grounded" else 2


if __name__ == "__main__":
    raise SystemExit(main())
