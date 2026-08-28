import argparse,json
from pathlib import Path
from intention.contracts import Table
from intention.pipeline import run

def fixture():
    raw=json.loads((Path(__file__).resolve().parents[2]/"fixtures/synthetic_tables.json").read_text())
    return [Table(x["table_id"],x["title"],x["description"],tuple(x["rows"]),x["metadata"]) for x in raw["tables"]]
def main():
    parser=argparse.ArgumentParser(); parser.add_argument("command",choices=["smoke","synthetic-benchmark","evaluate-profiler","evaluate-interpreter","profile","interpret","retrieve","build-benchmark","run-baselines","run-main","run-ablations","run-sensitivity","evaluate","generate-paper-tables"]); parser.add_argument("--input",default="vaccine side effects compare measure=rate, comparison dimension=country")
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
    if args.command in {"smoke","profile","interpret","retrieve","run-main"}:
        result=run(args.input,fixture()); print(json.dumps({"knowledge_hash":result["knowledge_hash"],"ranking":[r.__dict__ for r in result["ranking"]]},indent=2)); return
    raise SystemExit(f"{args.command} requires an explicit experiment configuration; no approximation was run")
if __name__=="__main__": main()
