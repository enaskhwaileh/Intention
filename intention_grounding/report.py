"""Markdown report (paper-ready tables) from an experiments results directory."""
import json
from pathlib import Path


def _fmt(v):
    return "–" if v is None else (f"{v:.3f}" if isinstance(v, float) else str(v))


def write_report(out):
    out = Path(out)
    data = json.loads((out / "summary.json").read_text())
    env, systems = data["environment"], data["systems"]
    lines = [f"# IGBench results ({out.name})", "",
             f"Benchmark `{env.get('benchmark')}` on corpus `{env['corpus_id']}` ({env['tables']} tables), IL {env['il_version']}, labels: **{env['label_status']}**.",
             f"Python {env['python']} on {env['platform']}. Warm caches: {env['warm']}.", "",
             "## RQ1 – usefulness ranking (queries with at least one useful table)", "",
             "| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |", "|---|---|---|---|---|---|---|---|"]
    for s in systems:
        lines.append(f"| {s['system']} | {_fmt(s['ndcg@10'])} | {_fmt(s['p@5'])} | {_fmt(s['p@10'])} | {_fmt(s['r@10'])} | "
                     f"{_fmt(s['mrr'])} | {_fmt(s['useful@1'])} | {_fmt(s['topical_only@1'])} |")
    lines += ["", "Intention-bearing queries only (gold grounding = grounded):", "",
              "| System | nDCG@10 | P@5 | MRR | Useful@1 |", "|---|---|---|---|---|"]
    for s in systems:
        lines.append(f"| {s['system']} | {_fmt(s['ndcg@10|intention'])} | {_fmt(s['p@5|intention'])} | {_fmt(s['mrr|intention'])} | {_fmt(s['useful@1|intention'])} |")
    lines += ["", "Recall of gold/useful tables at k (TARGET's main retrieval metric):", "",
              "| System | R@1 | R@5 | R@10 |", "|---|---|---|---|"]
    for s in systems:
        lines.append(f"| {s['system']} | {_fmt(s.get('r@1'))} | {_fmt(s.get('r@5'))} | {_fmt(s.get('r@10'))} |")
    ops = sorted({op for s in systems for op in (s.get("by_operation") or {})})
    if ops:
        lines += ["", "nDCG@10 by analytical operation / intention family (n = queries):", "",
                  "| System | " + " | ".join(f"{op} (n={systems[0]['by_operation'].get(op, {}).get('n', 0)})" for op in ops) + " |",
                  "|---|" + "---|" * len(ops)]
        for s in systems:
            lines.append(f"| {s['system']} | " + " | ".join(_fmt((s.get('by_operation') or {}).get(op, {}).get('ndcg@10')) for op in ops) + " |")
    lines += ["", "## RQ2 – response to a change of intention with a fixed topic", "",
              "Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).", "",
              "| System | Swap accuracy |", "|---|---|"]
    for s in systems:
        lines.append(f"| {s['system']} | {_fmt(s['swap_accuracy'])} |")
    rq3 = [s for s in systems if any(k.startswith("rq3_") for k in s)]
    if rq3:
        lines += ["", "## RQ3 – interpretation, grounding and assessment accuracy", "",
                  "| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |",
                  "|---|---|---|---|---|---|---|---|---|---|---|"]
        for s in rq3:
            lines.append(f"| {s['system']} | {_fmt(s.get('rq3_intention_presence'))} | {_fmt(s.get('rq3_argument_f1'))} | {_fmt(s.get('rq3_scope_f1'))} | "
                         f"{_fmt(s.get('rq3_grounding_status'))} | {_fmt(s.get('rq3_family'))} | {_fmt(s.get('rq3_variant'))} | "
                         f"{_fmt(s.get('rq3_binding_accuracy'))} | {_fmt(s.get('fallback_rate'))} | {_fmt(s.get('assessment_precision'))} | {_fmt(s.get('assessment_recall'))} |")
    lines += ["", "## RQ4 – running time per stage (ms per query: mean / median / p95)", "",
              "| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |",
              "|---|---|---|---|---|---|---|---|---|"]
    for s in systems:
        t = s["timing"]
        cell = lambda k: (f"{t[k]['mean']:.1f} / {t[k]['median']:.1f} / {t[k]['p95']:.1f}" if k in t else "–")
        lines.append(f"| {s['system']} | {cell('interpreter_ms')} | {cell('context_matching_ms')} | {cell('grounder_ms')} | "
                     f"{cell('profiler_ms')} | {cell('aligner_ms')} | {cell('ranking_ms')} | {cell('total_ms')} | {s['wall_seconds']} |")
    lines += ["", "Context index build (one-off, ms): " + ", ".join(f"{m}: {v['build_ms']:.0f}{' (cached)' if v['cache_hit'] else ''}"
                                                                   for m, v in env["index"].items()), ""]
    (out / "results.md").write_text("\n".join(lines))
    return out / "results.md"


def paired_tests(a, b, *, permutations=10000, seed=13):
    """Two-sided paired approximate randomization test and bootstrap 95% CI for mean(b - a)."""
    import random
    pairs = [(x, y) for x, y in zip(a, b) if x is not None and y is not None]
    if not pairs:
        return None
    diffs = [y - x for x, y in pairs]
    observed = sum(diffs) / len(diffs)
    rng = random.Random(seed)
    extreme = 0
    for _ in range(permutations):
        s = sum(d if rng.random() < 0.5 else -d for d in diffs) / len(diffs)
        extreme += abs(s) >= abs(observed) - 1e-12
    boots = sorted(sum(rng.choice(diffs) for _ in diffs) / len(diffs) for _ in range(2000))
    return {"n": len(diffs), "mean_diff": round(observed, 4), "p_value": round((extreme + 1) / (permutations + 1), 4),
            "ci95": [round(boots[49], 4), round(boots[1949], 4)], "wins": sum(d > 0 for d in diffs), "losses": sum(d < 0 for d in diffs)}


def significance(out, metrics=("ndcg@10", "mrr", "useful@1")):
    """Compare every ig:*:<m>[+opts] system with ctx:<m> on the same queries."""
    out = Path(out)
    per = {}
    for path in out.glob("metrics_*.json"):
        data = json.loads(path.read_text())
        per[data["aggregate"]["system"]] = data["per_query"]
    rows = []
    for name, pq in per.items():
        if not name.startswith("ig:"):
            continue
        base = "ctx:" + name.split(":")[-1].split("+")[0]
        if base not in per:
            continue
        qids = sorted(pq)
        for metric in metrics:
            res = paired_tests([per[base][q][metric] for q in qids], [pq[q][metric] for q in qids])
            if res:
                rows.append({"system": name, "baseline": base, "metric": metric, **res})
    (out / "significance.json").write_text(json.dumps(rows, indent=1))
    lines = ["", "## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)", "",
             "| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |", "|---|---|---|---|---|---|---|"]
    for r in rows:
        lines.append(f"| {r['system']} | {r['baseline']} | {r['metric']} | {r['mean_diff']:+.3f} | [{r['ci95'][0]:+.3f}, {r['ci95'][1]:+.3f}] | {r['p_value']:.3f} | {r['wins']}/{r['losses']} |")
    with open(out / "results.md", "a") as f:
        f.write("\n".join(lines) + "\n")
    return rows
