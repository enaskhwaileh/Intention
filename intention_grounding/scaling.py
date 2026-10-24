"""RQ4 scalability: cost of profiling and alignment as a function of table size.

  python -m intention_grounding.scaling --sample 300 --seed 7

For a seeded random sample of corpus tables (plus every table above the size
threshold), profiles each table without cache, then aligns it against a fixed set
of grounded intentions (one per Intention Library family). Writes a CSV of
(table, rows, columns, cells, bytes, profile_ms, align_ms per family) and a JSON
summary with a least-squares fit of time against cells.
"""
import argparse
import csv
import json
import random
import statistics
import time
from pathlib import Path

from . import aligner, corpus, il, profiler
from .grounder import ReplayResolver, ground
from .interpreter import ReplayInterpreter, interpret

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "experiments" / "scaling"

PROBES = {
    "compare": {"context_query": "average wage across gender", "intention_expression": "Compare",
                "arguments": [{"id": "a1", "label": "statistic", "value": "average", "spans": ["average"]},
                              {"id": "a2", "label": "measure", "value": "wage", "spans": ["wage"]},
                              {"id": "a3", "label": "group_dimension", "value": "gender", "spans": ["gender"]}], "scope": []},
    "aggregate": {"context_query": "total count by year", "intention_expression": "total",
                  "arguments": [{"id": "a1", "label": "statistic", "value": "total", "spans": ["total"]},
                                {"id": "a2", "label": "measure", "value": "count", "spans": ["count"]},
                                {"id": "a3", "label": "group_dimension", "value": "year", "spans": ["year"]}], "scope": []},
    "predict": {"context_query": "price from age", "intention_expression": "Predict",
                "arguments": [{"id": "a1", "label": "target", "value": "price", "spans": ["price"]},
                              {"id": "a2", "label": "predictor", "value": "age", "spans": ["age"]}], "scope": []},
    "explain": {"context_query": "income and education", "intention_expression": "associated with",
                "arguments": [{"id": "a1", "label": "measure", "value": "income", "spans": ["income"]},
                              {"id": "a2", "label": "predictor", "value": "education", "spans": ["education"]}], "scope": []},
    "monitor": {"context_query": "population over time", "intention_expression": "Track",
                "arguments": [{"id": "a1", "label": "measure", "value": "population", "spans": ["population"]}], "scope": []},
}
PROPOSALS = {
    "compare": {"status": "proposed", "variant_id": "compare.group_means", "bindings": {"statistic": ["a1"], "measure": ["a2"], "group_dimension": ["a3"]}},
    "aggregate": {"status": "proposed", "variant_id": "aggregate.group_totals", "bindings": {"statistic": ["a1"], "measure": ["a2"], "group_dimension": ["a3"]}},
    "predict": {"status": "proposed", "variant_id": "predict.regression", "bindings": {"target": ["a1"], "predictor": ["a2"]}},
    "explain": {"status": "proposed", "variant_id": "explain.association", "bindings": {"measure": ["a1"], "predictor": ["a2"]}},
    "monitor": {"status": "proposed", "variant_id": "monitor.trend", "bindings": {"measure": ["a1"]}},
}


def groundings(library):
    out = {}
    for fam, z in PROBES.items():
        text = f"probe {fam} " + " ".join(s for e in z["arguments"] for s in e["spans"]) + " " + z["intention_expression"]
        interp = interpret(text, ReplayInterpreter({text: z}), library["vocabulary"]).to_dict()
        proposal = {**PROPOSALS[fam], "scope": [], "justification": "scaling probe", "diagnostics": []}
        out[fam] = ground(interp, library, ReplayResolver({text: proposal}))
        assert out[fam]["status"] == "grounded", (fam, out[fam]["diagnostics"])
    return out


def fit(xs, ys):
    mx, my = statistics.mean(xs), statistics.mean(ys)
    sxx = sum((x - mx) ** 2 for x in xs)
    slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx if sxx else 0.0
    return {"intercept_ms": round(my - slope * mx, 3), "ms_per_million_cells": round(slope * 1e6, 3)}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--sample", type=int, default=300)
    p.add_argument("--seed", type=int, default=7)
    p.add_argument("--include-large", type=int, default=1_000_000, help="always include tables with at least this many cells")
    args = p.parse_args(argv)
    manifest, library = corpus.load_manifest(), il.load()
    g = groundings(library)
    tables = manifest["tables"]
    rng = random.Random(args.seed)
    chosen = rng.sample(tables, min(args.sample, len(tables)))
    sizes = {}
    for t in tables:
        n_cols = len(t["columns"])
        sizes[t["table_id"]] = n_cols
    large = [t for t in tables if t["table_id"].startswith(("owid.", "uci.")) and t not in chosen]
    chosen += large
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    for t in chosen:
        frames = profiler.FrameCache(capacity=1)
        start = time.perf_counter()
        prof = profiler.profile(t, cache_dir=None, frames=frames)
        profile_ms = (time.perf_counter() - start) * 1000
        rec = {"table_id": t["table_id"], "rows": prof["rows"], "columns": prof["n_columns"],
               "cells": prof["rows"] * prof["n_columns"], "bytes": t["bytes"], "profile_ms": round(profile_ms, 3)}
        for fam, grounding in g.items():
            start = time.perf_counter()
            aligner.assess(t, prof, grounding, frames=frames)
            rec[f"align_{fam}_ms"] = round((time.perf_counter() - start) * 1000, 3)
        rows.append(rec)
    path = OUT / f"scaling_seed{args.seed}_n{len(rows)}.csv"
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    cells = [r["cells"] for r in rows]
    summary = {"tables": len(rows), "seed": args.seed, "cells": {"median": statistics.median(cells), "max": max(cells)},
               "profile_ms": {"median": round(statistics.median(r["profile_ms"] for r in rows), 3),
                              "p95": round(sorted(r["profile_ms"] for r in rows)[int(0.95 * len(rows)) - 1], 3),
                              "fit": fit(cells, [r["profile_ms"] for r in rows])},
               "align_ms": {fam: {"median": round(statistics.median(r[f"align_{fam}_ms"] for r in rows), 3),
                                  "p95": round(sorted(r[f"align_{fam}_ms"] for r in rows)[int(0.95 * len(rows)) - 1], 3),
                                  "fit": fit(cells, [r[f"align_{fam}_ms"] for r in rows])} for fam in g}}
    (OUT / f"scaling_seed{args.seed}_n{len(rows)}.json").write_text(json.dumps(summary, indent=1))
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
