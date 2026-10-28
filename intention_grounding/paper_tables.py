"""Paper tables from the experiment plan (experiments/plan_state.json).

  python -m intention_grounding.paper_tables [--out experiments/paper]

Writes tables.md (all tables with captions), one CSV per table and tables.json (for the results explorer).
Every "Δ" is the paired difference against the same context matcher alone on the same queries, with a
two-sided paired randomization test (10,000 permutations) and bootstrap 95% CI; bold = p < 0.05.

  T1  RQ1  IGBench: nDCG@10 per context matcher x {context only, IG rule, IG gold, IG with each LLM}
  T2  RQ2  intention-swap accuracy for the same systems
  T3  RQ3  construction accuracy of the Interpreter and Grounder (rule, each LLM, gold+LLM, LLM+index)
  T4  baselines on IGBench: rerankers, query-rewrite controls, encoders incl. TABERTA, vs. intention grounding
  T5  TARGET (BIRD, Spider): recall@k / nDCG for context only, IG rule, IG LLM, rerankers, controls
  T6  where the change comes from on TARGET (breakdown by interpretation/grounding outcome)
  T7  RQ4 ablations (IGBench, gold, BM25)
  T8  RQ4 running time per stage (single process)
"""
import argparse
import csv
import json
from pathlib import Path

from .plan import DATASETS, LLMS, MATCHERS, RESULTS, STATE, cells

LLMS["groq"]["label"] = LLMS["groq"]["label"].format(model=LLMS["groq"]["env"]["IG_LLM_MODEL"])
from .report import paired_tests

R_NORM = "+rnorm=minmax"


def _load(run):
    d = RESULTS / run
    per = {}
    for f in d.glob("metrics_*.json"):
        m = json.loads(f.read_text())
        per[m["aggregate"]["system"]] = m
    bd = json.loads((d / "breakdown.json").read_text()) if (d / "breakdown.json").exists() else {}
    return per, bd


class Store:
    def __init__(self):
        self.state = json.loads(STATE.read_text()) if STATE.exists() else {}
        self.cache = {}

    def cell(self, cid):
        s = self.state.get(cid)
        if not s or s.get("status") not in ("done", "check"):
            return None, None
        if cid not in self.cache:
            self.cache[cid] = _load(s["run"])
        return self.cache[cid]

    def system(self, cid, name):
        per, _ = self.cell(cid)
        return None if per is None else per.get(name)


def delta(base, x, metric="ndcg@10"):
    if not base or not x:
        return None
    q = sorted(set(base["per_query"]) & set(x["per_query"]))
    t = paired_tests([base["per_query"][k].get(metric) for k in q], [x["per_query"][k].get(metric) for k in q])
    return t


def fmt(x, metric, base=None, with_delta=True):
    if not x:
        return "–"
    v = x["aggregate"].get(metric)
    if v is None:
        return "–"
    s = f"{v:.3f}"
    if with_delta and base is not None and base is not x:
        t = delta(base, x, metric)
        if t:
            sig = t["p_value"] < 0.05
            s = (f"**{v:.3f}**" if sig else s) + f" ({t['mean_diff']:+.3f})"
    return s


def ig_name(kind, m, profile=None, rnorm=True):
    if kind == "rule":
        return f"ig:rule/index:{m}" + (R_NORM if rnorm else "")
    if kind == "gold":
        return f"ig:gold/gold:{m}" + (R_NORM if rnorm else "")
    return f"ig:llm/llm:{m}+repair=1" + (R_NORM if rnorm else "")


def table_main(st, ds, metric="ndcg@10", rnorm=True):
    head = ["Context matcher", "Context only", "IG rule", "IG gold"] + [f"IG {LLMS[p]['label'].split(' (')[0]}" for p in ("q14", "q32", "groq")]
    rows = []
    for mt in [c for c in MATCHERS if any(x["dataset"] == ds and x["matcher"] == c for x in cells())]:
        m = MATCHERS[mt][0]
        base = st.system(f"{ds}.{mt}", f"ctx:{m}")
        if base is None:
            continue
        row = [MATCHERS[mt][3], fmt(base, metric, with_delta=False),
               fmt(st.system(f"{ds}.{mt}", ig_name("rule", m, rnorm=rnorm)), metric, base),
               fmt(st.system(f"{ds}.{mt}", ig_name("gold", m, rnorm=rnorm)), metric, base)]
        for p in ("q14", "q32", "groq"):
            x = st.system(f"{ds}.{mt}.{p}", ig_name("llm", m, p, rnorm=rnorm))
            b = st.system(f"{ds}.{mt}.{p}", f"ctx:{m}") or base  # API runs may use a sample: compare on the same queries
            row.append(fmt(x, metric, b))
        rows.append(row)
    return head, rows


def table_swap_all(st, ds):
    head = ["Retriever", "System", "Swap acc.", "nDCG@10"]
    rows = []
    for mt in ("bm25", "minilm"):
        m = MATCHERS[mt][0]
        entries = [("retriever alone", f"{ds}.{mt}", f"ctx:{m}"), ("cross-encoder rerank", f"{ds}.{mt}", f"rerank:ce:{m}"),
                   ("IG rule", f"{ds}.{mt}", ig_name("rule", m)), ("IG gold", f"{ds}.{mt}", ig_name("gold", m))]
        for p in ("q14", "q32", "groq"):
            lab = LLMS[p]["label"].split(" (")[0]
            entries += [(f"LLM rerank ({lab})", f"{ds}.{mt}.{p}", f"rerank:llm:{m}"), (f"IG {lab}", f"{ds}.{mt}.{p}", ig_name("llm", m, p)),
                        (f"LLM rerank + IG verdicts ({lab})", f"{ds}.{mt}.{p}", f"rerank:llmig:{m}")]
        for label, cid, name in entries:
            x = st.system(cid, name)
            if x:
                rows.append([MATCHERS[mt][3], label, fmt(x, "swap_accuracy", with_delta=False), fmt(x, "ndcg@10", with_delta=False)])
    return head, rows


def table_components(st, ds):
    keys = [("rq3_argument_f1", "Argument F1"), ("rq3_scope_f1", "Scope F1"), ("rq3_grounding_status", "Status acc."),
            ("rq3_variant", "Variant acc."), ("rq3_binding_accuracy", "Binding acc."), ("fallback_rate", "Fallback ↓"), ("ndcg@10", "nDCG@10")]
    head = ["Interpreter + Grounder"] + [k[1] for k in keys] + ["Interpreter ms", "Grounder ms"]
    rows = []
    entries = [("Rule + index", f"{ds}.bm25", "ig:rule/index:bm25")]
    for p in ("q14", "q32", "groq"):
        lab = LLMS[p]["label"].split(" (")[0]
        entries += [(f"{lab} + {lab}", f"{ds}.bm25.{p}", "ig:llm/llm:bm25+repair=1"),
                    (f"{lab} + index", f"{ds}.bm25.{p}", "ig:llm/index:bm25+repair=1"),
                    (f"gold + {lab}", f"{ds}.bm25.{p}", "ig:gold/llm:bm25+repair=1")]
    entries += [("gold + gold", f"{ds}.bm25", "ig:gold/gold:bm25")]
    for name, cid, sysname in entries:
        x = st.system(cid, sysname)
        if not x:
            continue
        a = x["aggregate"]
        t = a.get("timing", {})
        rows.append([name] + ["–" if a.get(k) is None else f"{a[k]:.3f}" for k, _ in keys] +
                    [f"{(t.get('interpreter_ms') or {}).get('median', 0):.1f}", f"{(t.get('grounder_ms') or {}).get('median', 0):.1f}"])
    return head, rows


def table_baselines(st, ds):
    metrics = [("ndcg@10", "nDCG@10"), ("mrr", "MRR"), ("useful@1", "Useful@1"), ("topical_only@1", "Topical-only@1 ↓"), ("swap_accuracy", "Swap acc.")]
    head = ["Method", "Family"] + [m[1] for m in metrics]
    rows = []

    def add(label, family, cid, name, base_cid=None, base_name=None):
        x = st.system(cid, name)
        if not x:
            return
        b = st.system(base_cid or cid, base_name) if base_name else None
        rows.append([label, family] + [fmt(x, k, b) if k in ("ndcg@10", "mrr", "useful@1") else fmt(x, k, with_delta=False) for k, _ in metrics])

    for mt in ("bm25", "tfidf", "minilm", "e5", "bge", "e5i", "stella", "taberta", "hybrid"):
        add(MATCHERS[mt][3], "retrieval (context only)", f"{ds}.{mt}", f"ctx:{MATCHERS[mt][0]}")
    for mt in ("bm25", "minilm"):
        m = MATCHERS[mt][0]
        add(f"Cross-encoder rerank (bge-reranker-v2-m3) over {MATCHERS[mt][3]}", "reranking", f"{ds}.{mt}", f"rerank:ce:{m}", base_name=f"ctx:{m}")
        for p in ("q14", "q32", "groq"):
            add(f"LLM listwise rerank ({LLMS[p]['label'].split(' (')[0]}) over {MATCHERS[mt][3]}", "reranking", f"{ds}.{mt}.{p}", f"rerank:llm:{m}", base_name=f"ctx:{m}")
            add(f"LLM rerank + IG verdicts ({LLMS[p]['label'].split(' (')[0]}) over {MATCHERS[mt][3]}", "combination", f"{ds}.{mt}.{p}", f"rerank:llmig:{m}", base_name=f"ctx:{m}")
            add(f"LLM rerank + gold IG verdicts ({LLMS[p]['label'].split(' (')[0]}) over {MATCHERS[mt][3]}", "combination (oracle)", f"{ds}.{mt}.{p}", f"rerank:llmgold:{m}", base_name=f"ctx:{m}")
        add(f"Query rewrite only (rule q_u) over {MATCHERS[mt][3]}", "control", f"{ds}.{mt}", f"ig:rule/index:{m}+align=0", base_name=f"ctx:{m}")
        for p in ("q14", "q32", "groq"):
            add(f"Query rewrite only ({LLMS[p]['label'].split(' (')[0]} q_u) over {MATCHERS[mt][3]}", "control", f"{ds}.{mt}.{p}", f"ig:llm/llm:{m}+repair=1+align=0", base_name=f"ctx:{m}")
        add(f"IG rule over {MATCHERS[mt][3]}", "ours", f"{ds}.{mt}", ig_name("rule", m), base_name=f"ctx:{m}")
        for p in ("q14", "q32", "groq"):
            add(f"IG {LLMS[p]['label'].split(' (')[0]} over {MATCHERS[mt][3]}", "ours", f"{ds}.{mt}.{p}", ig_name("llm", m, p), base_name=f"ctx:{m}")
        if DATASETS[ds]["gold"]:
            add(f"IG gold over {MATCHERS[mt][3]}", "ours (oracle)", f"{ds}.{mt}", ig_name("gold", m), base_name=f"ctx:{m}")
    return head, rows


def table_target(st, ds):
    metrics = [("r@1", "R@1"), ("r@5", "R@5"), ("r@10", "R@10"), ("ndcg@10", "nDCG@10"), ("mrr", "MRR")]
    head = ["Matcher", "System", "n"] + [m[1] for m in metrics]
    rows = []
    for mt in ("bm25", "minilm", "e5i", "stella", "taberta"):
        m = MATCHERS[mt][0]
        base = st.system(f"{ds}.{mt}", f"ctx:{m}")
        if not base:
            continue
        entries = [("context only", f"{ds}.{mt}", f"ctx:{m}"), ("query rewrite only (rule)", f"{ds}.{mt}", f"ig:rule/index:{m}+align=0"),
                   ("IG rule", f"{ds}.{mt}", ig_name("rule", m)), ("cross-encoder rerank", f"{ds}.{mt}", f"rerank:ce:{m}")]
        for p in ("q14", "q32", "groq"):
            lab = LLMS[p]["label"].split(" (")[0]
            entries += [(f"LLM rerank ({lab})", f"{ds}.{mt}.{p}", f"rerank:llm:{m}"), (f"IG {lab}", f"{ds}.{mt}.{p}", ig_name("llm", m, p))]
        for label, cid, name in entries:
            x = st.system(cid, name)
            if not x:
                continue
            b = st.system(cid, f"ctx:{m}") or base
            rows.append([MATCHERS[mt][3], label, str(x["aggregate"].get("queries", ""))] + [fmt(x, k, b if x is not b else None) for k, _ in metrics])
    return head, rows


def table_breakdown(st, ds):
    head = ["Matcher", "System", "outcome", "questions", "share", "mean Δ nDCG@10", "contribution"]
    rows = []
    for c in cells():
        if c["dataset"] != ds:
            continue
        _, bd = st.cell(c["id"]) if st.state.get(c["id"]) else (None, None)
        for sysname, groups in (bd or {}).items():
            if R_NORM not in sysname or "align=0" in sysname:
                continue
            for k, v in groups.items():
                rows.append([MATCHERS[c["matcher"]][3], sysname + (f" [{c['profile']}]" if c["profile"] else ""), k, str(v["n"]),
                             f"{v['share']:.0%}", f"{v['mean_delta_ndcg@10']:+.3f}", f"{v['contribution']:+.4f}"])
    return head, rows


def table_ablations(st, ds):
    head = ["Variant", "nDCG@10", "MRR", "Useful@1", "Swap acc."]
    per, _ = st.cell(f"{ds}.ablations")
    if not per:
        return head, []
    base = per.get("ig:gold/gold:bm25")
    rows = []
    for name, x in per.items():
        rows.append([name, fmt(x, "ndcg@10", base), fmt(x, "mrr", base), fmt(x, "useful@1", base), fmt(x, "swap_accuracy", with_delta=False)])
    return head, rows


def table_timing(st, ds):
    stages = ["interpreter_ms", "context_matching_ms", "embed_query_ms", "vector_search_ms", "grounder_ms", "profiler_ms", "aligner_ms", "ranking_ms", "total_ms"]
    head = ["System"] + [s.replace("_ms", "") + " (median / p95 ms)" for s in stages]
    per, _ = st.cell(f"{ds}.timing")
    rows = []
    for name, x in (per or {}).items():
        t = x["aggregate"].get("timing", {})
        rows.append([name] + [f"{t[s]['median']:.1f} / {t[s]['p95']:.0f}" if s in t else "–" for s in stages])
    return head, rows


def write(out):
    st = Store()
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    tables = []
    for ds in ("igb-test", "igb-dev"):
        lab = DATASETS[ds]["label"]
        tables += [(f"T1_{ds}", f"T1 (RQ1). {lab}: nDCG@10 of each context matcher alone and with intention grounding (min-max r).", table_main(st, ds)),
                   (f"T1raw_{ds}", f"T1-raw. {lab}: as T1 with the raw context score r.", table_main(st, ds, rnorm=False)),
                   (f"T2_{ds}", f"T2 (RQ2). {lab}: intention-swap accuracy (0.5 = indifferent to the intention).", table_main(st, ds, "swap_accuracy")),
                   (f"T2b_{ds}", f"T2b (RQ2). {lab}: intention-swap accuracy of rerankers vs. intention grounding (does the ranking follow the intention?).", table_swap_all(st, ds)),
                   (f"T3_{ds}", f"T3 (RQ3). {lab}: construction accuracy of Interpreter and Grounder (BM25 candidates).", table_components(st, ds)),
                   (f"T4_{ds}", f"T4. {lab}: baselines from other work vs. intention grounding (Δ against the same matcher alone).", table_baselines(st, ds)),
                   (f"T7_{ds}", f"T7 (RQ4). {lab}: ablations (Δ against the default gold configuration).", table_ablations(st, ds)),
                   (f"T8_{ds}", f"T8 (RQ4). {lab}: running time per stage, one process, cold profile cache.", table_timing(st, ds))]
    for ds in ("bird", "spider"):
        lab = DATASETS[ds]["label"]
        tables += [(f"T5_{ds}", f"T5. {lab}: retrieval quality; Δ against the same matcher alone. API LLM rows use a fixed 300-question sample.", table_target(st, ds)),
                   (f"T6_{ds}", f"T6. {lab}: where the change comes from (outcome of interpretation / grounding per question).", table_breakdown(st, ds))]
    md = ["# Paper tables (generated by intention_grounding.paper_tables)", "",
          "Δ in parentheses: paired difference against the same context matcher alone on the same queries; "
          "**bold** = p < 0.05 (paired randomization test, 10,000 permutations).", ""]
    js = {}
    for key, caption, (head, rows) in tables:
        md += [f"## {caption}", ""]
        if not rows:
            md += ["_no completed runs yet_", ""]
            continue
        md += ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)] + ["| " + " | ".join(r) + " |" for r in rows] + [""]
        with open(out / f"{key}.csv", "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(head)
            w.writerows([[c.replace("**", "") for c in r] for r in rows])
        js[key] = {"caption": caption, "head": head, "rows": rows}
    (out / "tables.md").write_text("\n".join(md))
    (out / "tables.json").write_text(json.dumps(js, indent=1))
    return out / "tables.md"


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--out", default=str(RESULTS.parent / "paper"))
    a = p.parse_args(argv)
    print(write(a.out))


if __name__ == "__main__":
    main()
