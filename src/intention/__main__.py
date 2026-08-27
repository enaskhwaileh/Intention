import argparse,json
from pathlib import Path
from intention.contracts import Table
from intention.pipeline import run

def fixture():
    raw=json.loads((Path(__file__).resolve().parents[2]/"fixtures/synthetic_tables.json").read_text())
    return [Table(x["table_id"],x["title"],x["description"],tuple(x["rows"]),x["metadata"]) for x in raw["tables"]]
def main():
    parser=argparse.ArgumentParser(); parser.add_argument("command",choices=["smoke","profile","interpret","retrieve","build-benchmark","run-baselines","run-main","run-ablations","run-sensitivity","evaluate","generate-paper-tables"]); parser.add_argument("--input",default="vaccine side effects compare measure=rate, comparison dimension=country")
    args=parser.parse_args()
    if args.command in {"smoke","profile","interpret","retrieve","run-main"}:
        result=run(args.input,fixture()); print(json.dumps({"knowledge_hash":result["knowledge_hash"],"ranking":[r.__dict__ for r in result["ranking"]]},indent=2)); return
    raise SystemExit(f"{args.command} requires an explicit experiment configuration; no approximation was run")
if __name__=="__main__": main()
