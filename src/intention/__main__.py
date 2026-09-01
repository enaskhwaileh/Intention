import argparse,json,os
from pathlib import Path
from intention.contracts import Table
from intention.pipeline import run

def fixture():
    raw=json.loads((Path(__file__).resolve().parents[2]/"fixtures/synthetic_tables.json").read_text())
    return [Table(x["table_id"],x["title"],x["description"],tuple(x["rows"]),x["metadata"]) for x in raw["tables"]]
def main():
    parser=argparse.ArgumentParser(); parser.add_argument("command",choices=["smoke","operational-smoke","synthetic-benchmark","evaluate-profiler","evaluate-interpreter","evaluate-controlled","demo-snapshot","audit-wikitables-source","preflight-wikitables-corpus","acquire-wikitables-corpus","normalize-wikitables-corpus","audit-wikitables-resolution","profile","interpret","retrieve","build-benchmark","run-baselines","run-main","run-ablations","run-sensitivity","evaluate","generate-paper-tables"]); parser.add_argument("--input",default="vaccine side effects compare measure=rate, comparison dimension=country"); parser.add_argument("--check",action="store_true"); parser.add_argument("--source-root"); parser.add_argument("--network",action="store_true"); parser.add_argument("--data-root",default="data"); parser.add_argument("--output-root"); parser.add_argument("--report-path"); parser.add_argument("--qrels-path"); parser.add_argument("--normalized-root"); parser.add_argument("--limit",type=int); parser.add_argument("--batch-size",type=int)
    args=parser.parse_args()
    if args.command == "synthetic-benchmark":
        from intention.benchmarks import run_synthetic_benchmark
        result=run_synthetic_benchmark(); print(json.dumps(result,indent=2)); raise SystemExit(0 if result["passed"] else 1)
    if args.command == "evaluate-profiler":
        from intention.benchmarks import load_synthetic_benchmark
        from intention.knowledge import load_knowledge
        from intention.profiling import evaluate_profiles,load_gold_annotations,profile_table
        kg=load_knowledge(); gold=load_gold_annotations(Path(__file__).resolve().parents[2]/"fixtures/synthetic_capability_gold.json",kg); _,cases=load_synthetic_benchmark(); tables={table.table_id:table for case in cases for table in case.tables}; result=evaluate_profiles(gold,{key:profile_table(value) for key,value in tables.items()}); print(json.dumps(result,indent=2)); return
    if args.command == "evaluate-interpreter":
        from intention.interpretation import evaluate_interpreter
        result=evaluate_interpreter(); print(json.dumps(result,indent=2)); raise SystemExit(0 if result["passed"] else 1)
    if args.command == "evaluate-controlled":
        from intention.evaluation import controlled_evaluation_summary
        print(json.dumps(controlled_evaluation_summary(),indent=2)); return
    if args.command == "demo-snapshot":
        from intention.demonstrator import write_current_snapshot
        print(write_current_snapshot(check=args.check)); return
    if args.command == "audit-wikitables-source":
        from intention.benchmarks.source_audit import audit_source,blocked_source_audit,load_source_contract
        root=args.source_root or os.environ.get("INTENTION_WIKITABLES_SOURCE_ROOT")
        result=audit_source(Path(root)) if root else blocked_source_audit(load_source_contract(),[{"component":"source_files","reason":"canonical metadata root is not configured","required_action":"set --source-root or INTENTION_WIKITABLES_SOURCE_ROOT to an already acquired pinned repository checkout"}])
        print(json.dumps(result.to_dict(),indent=2)); return
    if args.command == "preflight-wikitables-corpus":
        from intention.benchmarks.corpus import corpus_preflight
        print(json.dumps(corpus_preflight(network=args.network),indent=2)); return
    if args.command == "acquire-wikitables-corpus":
        from intention.benchmarks.wikitables import acquire_archive
        print(json.dumps(acquire_archive(Path(args.data_root),network=args.network),indent=2)); return
    if args.command == "normalize-wikitables-corpus":
        from intention.benchmarks.wikitables import normalize_archive
        archive=Path(args.data_root)/"raw/wikitables-www2018/WP_tables.zip"; output=Path(args.output_root or Path(args.data_root)/"normalized/wikitables-www2018")
        print(json.dumps(normalize_archive(archive,output,args.limit,args.batch_size,None if args.report_path is None else Path(args.report_path)),indent=2)); return
    if args.command == "audit-wikitables-resolution":
        from intention.benchmarks.wikitables import audit_qrel_resolution
        if not args.qrels_path or not args.normalized_root:raise SystemExit("--qrels-path and --normalized-root are required")
        indexes=sorted((Path(args.normalized_root)/"index").glob("*.parquet")); print(json.dumps(audit_qrel_resolution(Path(args.qrels_path),indexes),indent=2)); return
    if args.command == "operational-smoke":
        from intention.architecture.operational import OperationalReadinessProbe,operational_smoke_status
        print(json.dumps(operational_smoke_status(OperationalReadinessProbe().inspect()),indent=2)); return
    if args.command in {"smoke","profile","interpret","retrieve","run-main"}:
        result=run(args.input,fixture()); print(json.dumps({"knowledge_hash":result["knowledge_hash"],"ranking":[r.__dict__ for r in result["ranking"]]},indent=2)); return
    raise SystemExit(f"{args.command} requires an explicit experiment configuration; no approximation was run")
if __name__=="__main__": main()
