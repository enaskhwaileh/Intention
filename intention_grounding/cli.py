"""One-command interpreter -> grounder -> profiler -> conservative aligner pipeline."""
import argparse
import json
from datetime import datetime, timezone
from importlib.resources import files
from pathlib import Path
import uuid

from .intention_library import (CANONICAL_IL_PATH, IntentionLibraryError, describe_intention,
                          list_intentions, load_intention_library)
from .aligner import compare_card
from .grounder import GroqGrounderProvider, ReplayGrounderProvider, ground
from .groq_config import groq_model_id
from .interpreter.core import interpret
from .interpreter.providers import GroqProvider, ReplayProvider, list_available_models
from .provider_errors import provider_diagnostic
from .profiler import profile_paths


def _write(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _offline_inputs(il_version=None):
    replay = json.loads(files("intention_grounding.interpreter").joinpath("fixtures/replay.json").read_text())
    case = replay[2]  # compare.time: complete canonical required roles and exact evidence.
    doc = json.loads(case["raw_response"])
    refs, evidence = {}, []
    for index, argument in enumerate(doc["intentions"][0]["arguments"]):
        refs.setdefault(argument["role"], []).append({"intention_instance_id": "a1", "argument_index": index})
        evidence.extend(argument["value"]["evidence"])
    proposal = {"il_version": il_version or load_intention_library()["il_version"], "input_id": doc["input_id"],
                "intention_id": "compare.time", "bindings": refs, "evidence": list(dict.fromkeys(evidence))}
    return case["input_id"], case["input"], ReplayProvider(case["raw_response"]), ReplayGrounderProvider(json.dumps(proposal))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("offline", "groq", "discovery"), default="offline")
    parser.add_argument("--input-id", default="live-input-1")
    parser.add_argument("--input", help="Natural-language request; required in groq mode")
    parser.add_argument("--model", help="Groq model ID; overrides GROQ_MODEL_ID")
    parser.add_argument("--list-models", action="store_true",
                        help="List model IDs visible to GROQ_API_KEY; makes one authenticated API call")
    parser.add_argument("--dataset", action="append", type=Path, help="Local CSV/JSON table (repeatable)")
    parser.add_argument("--dataset-metadata", type=Path, help="JSON provenance record for supplied tables")
    parser.add_argument("--max-tables", type=int, default=None)
    parser.add_argument("--output", type=Path, default=Path("outputs/pipeline"))
    parser.add_argument("--il", dest="il", type=Path, default=CANONICAL_IL_PATH,
                        help="Canonical Intention Library JSON path")
    inspection = parser.add_mutually_exclusive_group()
    inspection.add_argument("--list-intentions", action="store_true", help="List the IL offline as JSON")
    inspection.add_argument("--intention", help="Inspect an intention and its separate procedure definitions offline")
    parser.add_argument('--case', help='Authored real-data demonstration case ID')
    parser.add_argument('--request', type=Path, help='Closed structured request JSON for discovery mode')
    parser.add_argument('--withhold-semantics', action='store_true', help='Explicit missing-documentation diagnostic')
    parser.add_argument('--no-execute', action='store_true', help='Assess and rank without SQL execution')
    parser.add_argument('--retrieval', choices=('bm25','sbert','sbert-full'), help='Natural-language default: SBERT topical query; structured default: BM25')
    parser.add_argument('--allow-live-generation', action='store_true', help='Use only with an approved spending budget: at most one Groq attempt, no retries; cached responses reused')
    parser.add_argument('--mock-response', type=Path, help='Explicit diagnostic: authored Interpreter JSON, never live model verification')
    args = parser.parse_args(argv)
    if args.max_tables is not None and args.max_tables < 1:parser.error('--max-tables must be positive')
    if args.mock_response and not args.input:parser.error('--mock-response requires --input')
    if args.input and args.mode == 'offline': args.mode = 'discovery'
    if args.mode == 'discovery' and sum(bool(x) for x in (args.input,args.request,args.case)) != 1:
        parser.error('Discovery requires exactly one of --input, --request, or --case; no authored-role fallback')
    if args.mode == 'discovery' and args.input:
        from .discovery import run_text, save_report
        provider = ReplayProvider(args.mock_response.read_text()) if args.mock_response else None
        report = run_text(args.input,input_id=args.input_id,model=args.model,provider=provider,
                          allow_live=args.allow_live_generation,retrieval_method=args.retrieval or 'sbert',
                          execute=not args.no_execute,candidate_limit=args.max_tables)
        path=save_report(report,args.output)
        print('status='+report.get('status','completed')+' abstained='+str(report['abstained']))
        if report.get('failure'): print('failure='+report['failure'])
        print('predictions='+str(path))
        return 2 if report.get('status')=='failed' else 0
    if args.mode == 'discovery':
        from .discovery import run, save_report, ROOT
        try:
            options = {}
            if args.request:
                request = json.loads(args.request.read_text())
            else:
                cases = json.loads((ROOT/'data/requests/demo-v1.json').read_text())['cases']
                case = next((c for c in cases if c['request']['request_id'] == args.case), None)
                if case is None: parser.error('Unknown demonstration case')
                request, options = case['request'], case['run_options']
            report = run(request, execute=not args.no_execute,
                         withhold_semantics=args.withhold_semantics or options.get('withhold_semantics', False),
                         retrieval_method=args.retrieval or 'bm25', topical_query=request['topic'],candidate_limit=args.max_tables)
            path = save_report(report, args.output)
        except (OSError, ValueError, RuntimeError, ImportError) as exc:
            print('discovery_error=' + type(exc).__name__ + ': ' + str(exc))
            return 2
        print('input_mode=' + request['input_mode'] + ' grounding=' + report['grounded_intention']['status'])
        for table in report['ranking']:
            print(table['rank'], table['table_id'], table['overall_state'], round(table['retrieval_score'], 6))
        print('abstained=' + str(report['abstained']) + ' effectiveness=pending_independent_judgments')
        print('predictions=' + str(path))
        return 0
    if args.list_intentions or args.intention is not None:
        try:
            il = load_intention_library(args.il)
            result = list_intentions(il) if args.list_intentions else describe_intention(args.intention, il)
        except IntentionLibraryError as exc:
            print(f"library_error={exc}")
            return 2
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
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
    il = load_intention_library(args.il)
    if args.mode == "offline":
        input_id, user_input, interpreter_provider, grounder_provider = _offline_inputs(il["il_version"])
    else:
        input_id, user_input = args.input_id, args.input
        interpreter_provider, grounder_provider = GroqProvider(model=model), GroqGrounderProvider(model=model)
    run_id = "run-" + uuid.uuid4().hex[:12]
    output = args.output / run_id
    output.mkdir(parents=True, exist_ok=False)
    interpreted = interpret(input_id, user_input, interpreter_provider)
    grounded = ground(interpreted, il, grounder_provider, run_id=run_id)
    paths = sorted(args.dataset or [Path(files("intention_grounding").joinpath("fixtures/offline_table.csv"))], key=str)
    if args.max_tables is not None:
        paths = paths[:args.max_tables]
    if args.dataset_metadata:
        source_metadata = json.loads(args.dataset_metadata.read_text(encoding="utf-8"))
    else:
        source_metadata = ({"dataset_id": "local", "source_url": None, "license": None, "benchmark_eligible": False}
                           if args.dataset else json.loads(files("intention_grounding").joinpath("fixtures/offline-source-metadata.json").read_text()))
    if not isinstance(source_metadata.get("dataset_id"), str) or not source_metadata["dataset_id"]:
        parser.error("dataset metadata must contain a nonempty dataset_id")
    profiles = profile_paths(paths, dataset_id=source_metadata["dataset_id"], source_metadata=source_metadata)
    comparison = compare_card(grounded["grounded_intention"], profiles)
    (output / "interpreter.raw.txt").write_text(interpreted["raw_response"] or "", encoding="utf-8")
    _write(output / "interpretation.json", {k: v for k, v in interpreted.items() if k != "raw_response"})
    (output / "grounder.raw.txt").write_text(grounded["raw_response"] or "", encoding="utf-8")
    _write(output / "grounding.json", {k: v for k, v in grounded.items() if k != "raw_response"})
    _write(output / "table-profiles.json", profiles)
    _write(output / "comparison.json", comparison)
    manifest = {"run_id": run_id, "created_at": datetime.now(timezone.utc).isoformat(), "mode": args.mode,
                "il_path": str(args.il), "il_version": il["il_version"], "input_id": input_id,
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
