"""Where does the gain come from? Split each intention-grounding system's change against its context
matcher by what the framework did with the request.

  python -m intention_grounding.breakdown experiments/results/<run>

Groups: interpretation status / grounding status (e.g. extracted/grounded, no_intention/not_attempted).
Requests that were not grounded are ranked by context relevance alone, so their change comes only from the
context query q_u produced by the Interpreter; grounded requests add profiling, alignment and F(r, A).
Writes breakdown.json in the run directory and prints a table.
"""
import json
import sys
from collections import defaultdict
from pathlib import Path


def breakdown(run):
    run = Path(run)
    metrics = {}
    for f in run.glob("metrics_*.json"):
        m = json.loads(f.read_text())
        metrics[m["aggregate"]["system"]] = m["per_query"]
    out = {}
    for f in sorted(run.glob("predictions_ig_*.jsonl")):
        rows = [json.loads(line) for line in f.read_text().splitlines() if line.strip()]
        if not rows:
            continue
        name = next((s for s in metrics if s.startswith("ig:") and
                     s.replace(":", "_").replace("/", "-").replace("+", "_").replace("=", "") == f.stem[len("predictions_"):]), None)
        if name is None:
            continue
        base = metrics.get("ctx:" + name.split(":")[-1].split("+")[0])
        if base is None:
            continue
        groups = defaultdict(list)
        for r in rows:
            i, g = r.get("interpretation") or {}, r.get("grounding") or {}
            q = r["query_id"]
            if q in metrics[name] and q in base:
                groups[f"{i.get('status')}/{g.get('status')}"].append(metrics[name][q]["ndcg@10"] - base[q]["ndcg@10"])
        total = sum(len(v) for v in groups.values())
        out[name] = {k: {"n": len(v), "share": round(len(v) / total, 4), "mean_delta_ndcg@10": round(sum(v) / len(v), 4),
                         "contribution": round(sum(v) / total, 4)} for k, v in sorted(groups.items(), key=lambda x: -len(x[1]))}
    (run / "breakdown.json").write_text(json.dumps(out, indent=1))
    return out


def main(argv=None):
    for run in (argv or sys.argv[1:]):
        print("##", run)
        for name, groups in breakdown(run).items():
            print(" ", name)
            for k, v in groups.items():
                print(f"    {k:32s} n={v['n']:5d} ({v['share']:.0%})  mean Δ={v['mean_delta_ndcg@10']:+.4f}  contribution={v['contribution']:+.4f}")


if __name__ == "__main__":
    main()
