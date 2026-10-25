"""Experiment harness for RQ1-RQ4 on IGBench (or any benchmark in the same format).

  python -m intention_grounding.experiments --systems main        # RQ1 + RQ2 + RQ4 timing
  python -m intention_grounding.experiments --systems ablations   # RQ4 component ablations
  python -m intention_grounding.experiments --systems all --context bm25,tfidf,lsa[,sbert]

Systems
  ctx:<m>             context matching only on the full input u (baselines)
  ig:<interp>/<res>:<m>  full framework; interp in {gold, rule, llm}, res in {gold, index, llm}
Labels are read only by the evaluator, after predictions are written.
"""
import argparse
import hashlib
import json
import math
import platform
import statistics
import time
from datetime import datetime, timezone
from pathlib import Path

from . import corpus, il
from .context import ContextMatcher
from .grounder import IndexResolver, LLMResolver, ReplayResolver
from .interpreter import LLMInterpreter, ReplayInterpreter, RuleInterpreter
from .pipeline import Pipeline

ROOT = Path(__file__).resolve().parent.parent
BENCH = ROOT / "benchmarks" / "igbench_v1" / "queries.json"
RESULTS = ROOT / "experiments" / "results"
K = 10


# ------------------------------------------------------------------ metrics (evaluator only)
def dcg(gains):
    return sum((2 ** g - 1) / math.log2(i + 2) for i, g in enumerate(gains))


def query_metrics(ranked, labels, k=K):
    gains = [labels.get(t, 0) for t in ranked[:k]]
    ideal = sorted(labels.values(), reverse=True)[:k]
    useful = {t for t, g in labels.items() if g == 2}
    first = next((i for i, t in enumerate(ranked) if t in useful), None)
    return {"ndcg@10": dcg(gains) / dcg(ideal) if dcg(ideal) > 0 else None,
            "p@5": sum(1 for t in ranked[:5] if t in useful) / 5 if useful else None,
            "p@10": sum(1 for t in ranked[:10] if t in useful) / 10 if useful else None,
            "r@10": sum(1 for t in ranked[:10] if t in useful) / len(useful) if useful else None,
            "mrr": (1 / (first + 1) if first is not None else 0.0) if useful else None,
            "useful@1": (1.0 if ranked and ranked[0] in useful else 0.0) if useful else None,
            "r@1": (1.0 * sum(1 for t in ranked[:1] if t in useful) / len(useful)) if useful else None,
            "r@5": (sum(1 for t in ranked[:5] if t in useful) / len(useful)) if useful else None,
            "topical_only@1": (1.0 if ranked and labels.get(ranked[0], 0) == 1 else 0.0)}


def mean(values):
    values = [v for v in values if v is not None]
    return round(sum(values) / len(values), 4) if values else None


def swap_accuracy(rankings, queries):
    """RQ2: for queries of one topic with different intentions, a table useful only for intention a should
    rank above a table useful only for intention b in a's ranking (pairwise, ties = 0.5)."""
    by_group, scores = {}, []
    for qd in queries:
        if qd["gold_grounding_status"] == "grounded":
            by_group.setdefault(qd["pair_group"], []).append(qd)
    details = []
    for group, qs in by_group.items():
        for a in qs:
            for b in qs:
                if a is b:
                    continue
                ua = {t for t, g in a["labels"].items() if g == 2} - {t for t, g in b["labels"].items() if g == 2}
                ub = {t for t, g in b["labels"].items() if g == 2} - {t for t, g in a["labels"].items() if g == 2}
                if not ua or not ub:
                    continue
                pos = {t: i for i, t in enumerate(rankings[a["query_id"]])}
                inf = len(pos) + 1
                pairs = [(1.0 if pos.get(x, inf) < pos.get(y, inf) else 0.5 if pos.get(x, inf) == pos.get(y, inf) else 0.0)
                         for x in ua for y in ub]
                s = sum(pairs) / len(pairs)
                scores.append(s)
                details.append({"group": group, "a": a["query_id"], "b": b["query_id"], "accuracy": round(s, 4)})
    return mean(scores), details


# ------------------------------------------------------------------ RQ3: interpretation / grounding accuracy
def _norm(text):
    import re
    toks = re.findall(r"[a-z0-9]+", (text or "").casefold())
    return " ".join(t[:-1] if len(t) > 3 and t.endswith("s") and not t.endswith("ss") else t for t in toks)


def _match(a, b):
    ta, tb = set(_norm(a).split()), set(_norm(b).split())
    return bool(ta and tb) and len(ta & tb) / len(ta | tb) >= 0.5


def entry_f1(pred, gold):
    used, tp = set(), 0
    for g in gold:
        for i, p in enumerate(pred):
            if i not in used and p["label"] == g["label"] and _match(p["value"], g["value"]):
                used.add(i)
                tp += 1
                break
    if not pred and not gold:
        return 1.0
    prec = tp / len(pred) if pred else 0.0
    rec = tp / len(gold) if gold else 0.0
    return 2 * prec * rec / (prec + rec) if prec + rec else 0.0


def interpretation_accuracy(report, qd):
    interp, gold = report["interpretation"], qd["gold_interpretation"]
    gold_has = gold["intention_expression"] is not None
    pred_has = interp["status"] == "extracted"
    out = {"intention_presence": float(gold_has == pred_has), "extraction_valid": float(interp["status"] != "failure")}
    if gold_has and pred_has:
        out["argument_f1"] = entry_f1(interp["intention"]["arguments"], gold["arguments"])
        out["scope_f1"] = entry_f1(interp["intention"]["scope"], gold["scope"])
    g = report["grounding"]
    out["grounding_status"] = float(g["status"] == qd["gold_grounding_status"])
    if qd["gold_grounding_status"] == "grounded":
        variant = g["g_u"]["variant_id"] if g["g_u"] else None
        out["family"] = float(bool(variant) and variant.split(".")[0] == qd["gold_family"])
        out["variant"] = float(variant == qd["gold_variant"])
        if g["g_u"]:
            gold_vals = {role: [next(e["value"] for e in gold["arguments"] if e["id"] == r) for r in refs]
                         for role, refs in qd["gold_grounding"]["bindings"].items()}
            pred_vals = {role: [v["value"] for v in vals] for role, vals in g["g_u"]["bindings"].items()}
            roles = set(gold_vals) | set(pred_vals)
            out["binding_accuracy"] = sum(1 for r in roles if r in gold_vals and r in pred_vals and
                                          all(any(_match(p, gv) for p in pred_vals[r]) for gv in gold_vals[r])) / len(roles)
        else:
            out["binding_accuracy"] = 0.0
    return out


def assessment_accuracy(report, labels):
    """How well the Aligner's categorical state separates useful (2) from non-useful assessed tables."""
    tp = fp = fn = tn = 0
    for tid, a in report["assessments"].items():
        useful = labels.get(tid, 0) == 2
        sup = a["state"] == "supported"
        tp += useful and sup
        fp += (not useful) and sup
        fn += useful and not sup
        tn += (not useful) and not sup
    return {"tp": tp, "fp": fp, "fn": fn, "tn": tn,
            "violated_useful": sum(1 for t, a in report["assessments"].items() if a["state"] == "violated" and labels.get(t, 0) == 2)}


# ------------------------------------------------------------------ systems
def gold_providers(queries):
    interp = ReplayInterpreter({qd["text"]: qd["gold_interpretation"] for qd in queries if qd.get("gold_interpretation")}, origin="gold_annotation")
    proposals = {qd["text"]: qd["gold_grounding"] for qd in queries if qd["gold_grounding"]}
    return interp, ReplayResolver(proposals, origin="gold_annotation")


def make_system(name, manifest, library, queries, matchers, *, allow_live=False):
    kind, _, rest = name.partition(":")
    if kind == "ctx":
        return {"name": name, "kind": "ctx", "matcher": matchers[rest]}
    spec, _, method = rest.rpartition(":")
    opts = {}
    if "+" in method:
        method, *flags = method.split("+")
        for f in flags:
            k, _, v = f.partition("=")
            opts[k] = v
    interp_name, res_name = spec.split("/")
    gi, gr = gold_providers(queries)
    rep = int(opts.get("repair", 0))  # +repair=1: one validator-guided retry for LLM components
    interp = {"gold": gi, "rule": RuleInterpreter(), "llm": LLMInterpreter(allow_live=allow_live, max_repairs=rep)}[interp_name]
    resolver = {"gold": gr, "index": IndexResolver(library), "llm": LLMResolver(allow_live=allow_live, max_repairs=rep)}[res_name]
    pipe = Pipeline(manifest, library=library, interpreter=interp, resolver=resolver, matcher=matchers[method],
                    k_candidates=int(opts.get("k", 50)), alpha=float(opts.get("alpha", 0.5)),
                    combination=opts.get("comb", "product"), use_soft=opts.get("soft", "1") == "1",
                    binding_threshold=float(opts.get("bind", 0.5)), r_norm=opts.get("rnorm", "none"))
    return {"name": name, "kind": "ig", "pipeline": pipe}


class _Precomputed:
    """Context matcher replaying retrievals computed in the parent process (used by worker processes,
    so GPU encoders and vector stores are only touched by the parent)."""
    def __init__(self, matcher, table):
        self.matcher, self.table, self.last_timing = matcher, table, {}

    def retrieve(self, q, k):
        hit = self.table.get((q, k))
        if hit is None:
            return self.matcher.retrieve(q, k)
        ranked, ms, timing = hit
        self.last_timing = timing
        return ranked, ms

    def __getattr__(self, name):  # method, dense_stats, ... of the real matcher
        return getattr(self.matcher, name)


_WORKER = {}


def _work(item):
    qid, text, interp = item
    return qid, _WORKER["pipe"].run(text, input_id=qid, interpretation=interp)


def run_system(system, queries, k=50, workers=1):
    rankings, reports = {}, {}
    if system["kind"] == "ig" and workers > 1:
        import multiprocessing as mp
        from .interpreter import interpret
        pipe = system["pipeline"]
        interps, table = {}, {}
        from concurrent.futures import ThreadPoolExecutor  # LLM interpreters are I/O bound: interpret in threads
        with ThreadPoolExecutor(max_workers=min(workers, 16)) as ex:
            done = ex.map(lambda qd: (qd["query_id"], interpret(qd["text"], pipe.interpreter, pipe.library["vocabulary"],
                                                                 input_id=qd["query_id"]).to_dict()), queries)
            interps = dict(done)
        for qd in queries:  # context matching in the parent (may use the GPU)
            it = interps[qd["query_id"]]
            key = (it["context_query"], pipe.k_candidates)
            if key not in table:
                ranked, ms = pipe.matcher.retrieve(*key)
                table[key] = (ranked, ms, dict(getattr(pipe.matcher, "last_timing", {}) or {}))
        real = pipe.matcher
        pipe.matcher = _Precomputed(real, table)
        _WORKER["pipe"] = pipe
        try:
            with mp.get_context("fork").Pool(workers) as pool:
                for qid, rep in pool.imap_unordered(_work, [(qd["query_id"], qd["text"], interps[qd["query_id"]]) for qd in queries], chunksize=4):
                    rankings[qid] = [x["table_id"] for x in rep["ranking"]]
                    reports[qid] = rep
        finally:
            pipe.matcher = real
        return rankings, reports
    for qd in queries:
        if system["kind"] == "ctx":
            start = time.perf_counter()
            ranked, ms = system["matcher"].retrieve(qd["text"], k)
            rankings[qd["query_id"]] = [t for t, _ in ranked]
            reports[qd["query_id"]] = {"timing": {"context_matching_ms": ms, **system["matcher"].last_timing, "total_ms": round((time.perf_counter() - start) * 1000, 3)},
                                       "ranking": [{"table_id": t, "r": r, "U": r} for t, r in ranked]}
        else:
            rep = system["pipeline"].run(qd["text"], input_id=qd["query_id"])
            rankings[qd["query_id"]] = [x["table_id"] for x in rep["ranking"]]
            reports[qd["query_id"]] = rep
    return rankings, reports


def summarise(name, rankings, reports, queries):
    per_query = {}
    for qd in queries:
        m = query_metrics(rankings[qd["query_id"]], qd["labels"])
        rep = reports[qd["query_id"]]
        if "interpretation" in rep and qd.get("gold_interpretation") is not None:
            m.update({f"rq3_{k}": v for k, v in interpretation_accuracy(rep, qd).items()})
            m["mode"] = rep["mode"]
        per_query[qd["query_id"]] = m
    with_useful = [qd["query_id"] for qd in queries if any(g == 2 for g in qd["labels"].values())]
    grounded_gold = [qd["query_id"] for qd in queries if qd["gold_grounding_status"] == "grounded"]
    agg = {"system": name, "queries": len(queries)}
    for key in ("ndcg@10", "p@5", "p@10", "r@1", "r@5", "r@10", "mrr", "useful@1", "topical_only@1"):
        agg[key] = mean(per_query[q][key] for q in with_useful)
        agg[key + "|intention"] = mean(per_query[q][key] for q in grounded_gold if q in with_useful)
    agg["swap_accuracy"], swap_details = swap_accuracy(rankings, queries)
    strata = {}
    for qd in queries:
        op = qd.get("sql_operation") or qd.get("gold_family")
        if op and per_query[qd["query_id"]]["ndcg@10"] is not None:
            strata.setdefault(op, []).append(qd["query_id"])
    agg["by_operation"] = {op: {"n": len(q), "ndcg@10": mean(per_query[x]["ndcg@10"] for x in q),
                                "r@5": mean(per_query[x]["r@5"] for x in q)} for op, q in sorted(strata.items())}
    rq3_keys = sorted({k for m in per_query.values() for k in m if k.startswith("rq3_")})
    for key in rq3_keys:
        agg[key] = mean(per_query[q].get(key) for q in per_query)
    if any("mode" in m for m in per_query.values()):
        agg["fallback_rate"] = mean(1.0 if per_query[q].get("mode") == "context_only_fallback" else 0.0
                                    for q in grounded_gold)
    tp = fp = fn = tn = vu = 0
    for qd in queries:
        rep = reports[qd["query_id"]]
        if rep.get("assessments"):
            a = assessment_accuracy(rep, qd["labels"])
            tp, fp, fn, tn, vu = tp + a["tp"], fp + a["fp"], fn + a["fn"], tn + a["tn"], vu + a["violated_useful"]
    if tp + fp + fn:
        agg["assessment_precision"] = round(tp / (tp + fp), 4) if tp + fp else None
        agg["assessment_recall"] = round(tp / (tp + fn), 4) if tp + fn else None
        agg["violated_but_useful"] = vu
    stages = ["interpreter_ms", "context_matching_ms", "embed_query_ms", "vector_search_ms", "grounder_ms", "profiler_ms", "aligner_ms", "ranking_ms", "total_ms"]
    timing = {}
    for s in stages:
        vals = [reports[q]["timing"].get(s) for q in reports if reports[q]["timing"].get(s) is not None]
        if vals:
            timing[s] = {"mean": round(statistics.mean(vals), 3), "median": round(statistics.median(vals), 3),
                         "p95": round(sorted(vals)[max(0, int(0.95 * len(vals)) - 1)], 3), "max": round(max(vals), 3)}
    agg["timing"] = timing
    return agg, per_query, swap_details


MAIN = ["ctx:bm25", "ctx:tfidf", "ctx:lsa", "ig:gold/gold:bm25", "ig:rule/index:bm25", "ig:gold/gold:tfidf", "ig:rule/index:tfidf"]
ABLATIONS = ["ig:gold/gold:bm25+comb=linear", "ig:gold/gold:bm25+comb=lexicographic", "ig:gold/gold:bm25+soft=0", "ig:gold/gold:bm25+alpha=0.25",
             "ig:gold/gold:bm25+alpha=0.75", "ig:gold/gold:bm25+alpha=1.0", "ig:gold/gold:bm25+k=20", "ig:gold/gold:bm25+k=100",
             "ig:gold/gold:bm25+bind=0.7", "ig:gold/index:bm25", "ig:rule/gold:bm25"]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--systems", default="main", help="main | ablations | all | comma-separated system names")
    parser.add_argument("--context", default="bm25,tfidf,lsa", help="context methods to index")
    parser.add_argument("--benchmark", type=Path, default=BENCH)
    parser.add_argument("--allow-live", action="store_true", help="permit new LLM calls (cost); cached calls are always reused")
    parser.add_argument("--out", type=Path, default=RESULTS)
    parser.add_argument("--warm", action="store_true", help="run every system twice; report the second (warm-cache) pass")
    parser.add_argument("--tag", default="", help="suffix for the results directory name")
    parser.add_argument("--corpus", type=Path, default=None, help="corpus manifest (default: IGBench)")
    parser.add_argument("--sbert-model", default=None, help="sentence-transformers model for sbert/hybrid (default all-MiniLM-L6-v2)")
    parser.add_argument("--workers", type=int, default=1, help="worker processes for intention-grounding systems (queries in parallel)")
    parser.add_argument("--vector-store", default="chroma", choices=["chroma", "faiss", "numpy"], help="vector database for table embeddings")
    args = parser.parse_args(argv)
    bench = json.loads(args.benchmark.read_text())
    queries = bench["queries"]
    manifest, library = corpus.load_manifest(args.corpus) if args.corpus else corpus.load_manifest(), il.load()
    target = [f"{kind}:{m}" for m in args.context.split(",") for kind in ("ctx", "ig:rule/index")]
    if args.allow_live:
        target += [f"ig:llm/llm:{m}" for m in args.context.split(",")]
    names = {"main": MAIN, "ablations": ABLATIONS, "all": MAIN + ABLATIONS, "target": target}.get(args.systems, args.systems.split(","))
    methods = sorted({n.split(":")[-1].split("+")[0] for n in names} | set(args.context.split(",")))
    matchers, index_times = {}, {}
    for m in methods:
        matchers[m] = ContextMatcher(manifest, m, sbert_model=args.sbert_model, vector_store=args.vector_store)
        index_times[m] = {"build_ms": matchers[m].build_ms, "cache_hit": matchers[m].cache_hit, "dense": matchers[m].dense_stats}
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + (f"_{args.tag}" if args.tag else "")
    out = args.out / run_id
    out.mkdir(parents=True, exist_ok=True)
    summary = []
    for name in names:
        system = make_system(name, manifest, library, queries, matchers, allow_live=args.allow_live)
        if args.warm:
            run_system(system, queries, workers=args.workers)
        start = time.perf_counter()
        rankings, reports = run_system(system, queries, workers=args.workers)
        wall = round(time.perf_counter() - start, 3)
        agg, per_query, swap = summarise(name, rankings, reports, queries)
        agg["wall_seconds"] = wall
        summary.append(agg)
        safe = name.replace(":", "_").replace("/", "-").replace("+", "_").replace("=", "")
        with open(out / f"predictions_{safe}.jsonl", "w") as f:
            for qd in queries:
                rep = reports[qd["query_id"]]
                f.write(json.dumps({"query_id": qd["query_id"], "ranking": rep["ranking"][:50],
                                    "timing": rep["timing"], "mode": rep.get("mode"),
                                    "interpretation": rep.get("interpretation"), "grounding": {k: v for k, v in rep.get("grounding", {}).items() if k != "psi_u"},
                                    "assessments": {t: {"state": a["state"], "A": a["A"], "best_procedure": a["best_procedure"],
                                                        "procedures": [{"procedure_id": p["procedure_id"], "state": p["state"], "score": p["score"],
                                                                        "requirements": p["requirements"], "soft": p["soft"]} for p in a["procedures"]]}
                                                    for t, a in rep.get("assessments", {}).items()}}, ensure_ascii=False) + "\n")
        (out / f"metrics_{safe}.json").write_text(json.dumps({"aggregate": agg, "per_query": per_query, "swap": swap}, indent=1))
        print(f"{name:45s} nDCG@10={agg['ndcg@10']}  P@5={agg['p@5']}  MRR={agg['mrr']}  U@1={agg['useful@1']}  swap={agg['swap_accuracy']}  wall={wall}s")
    env = {"python": platform.python_version(), "platform": platform.platform(), "processor": platform.processor(),
           "il_version": il.version(library), "il_sha256": library["_sha256"], "corpus_id": manifest["corpus_id"],
           "tables": len(manifest["tables"]), "benchmark_sha256": hashlib.sha256(args.benchmark.read_bytes()).hexdigest(),
           "label_status": bench["label_status"], "benchmark": bench.get("benchmark"), "index": index_times, "warm": args.warm}
    (out / "summary.json").write_text(json.dumps({"environment": env, "systems": summary}, indent=1))
    from .report import significance, write_report
    write_report(out)
    significance(out)
    print("results:", out)


if __name__ == "__main__":
    main()
