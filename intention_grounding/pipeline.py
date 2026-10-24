"""End-to-end intention-grounded table discovery (Figure 2) with per-stage timing.

  u --Interpreter--> (q_u, iota_u)
  q_u --Context matching--> top-k candidates with r(q_u, T)
  candidates --Table Profiler--> Phi(T)
  iota_u --Grounder (+ Intention Library)--> (g_u, Psi_u, s_G)
  (Psi_u, Phi(T)) --Aligner--> A(T, iota_u)
  U(T | q_u, iota_u) = F(r, A) if grounded, else r          (Eq. 8)
"""
import time
from datetime import datetime, timezone
from pathlib import Path

from . import aligner, il, profiler
from .context import ContextMatcher
from .grounder import ground, GROUNDED
from .interpreter import interpret

ROOT = Path(__file__).resolve().parent.parent
PROFILE_CACHE = ROOT / "data" / "runtime" / "profiles"
STATE_ORDER = {aligner.SUPPORTED: 0, aligner.UNRESOLVED: 1, aligner.VIOLATED: 2}


def combine_linear(r, a, alpha=0.5):
    """F(r, A) = (1 - alpha) r + alpha A: nondecreasing in both arguments, maps to [0, 1]."""
    return (1 - alpha) * r + alpha * a


def combine_product(r, a, lam=0.5):
    """F(r, A) = r (lam + (1 - lam) A): usefulness modulates context relevance; nondecreasing in both, F <= r."""
    return r * (lam + (1 - lam) * a)


class Pipeline:
    def __init__(self, manifest, *, library=None, interpreter, resolver, matcher=None, context_method="bm25",
                 k_candidates=50, k_out=10, alpha=0.5, combination="product", use_soft=True,
                 binding_threshold=0.5, profile_cache=PROFILE_CACHE):
        self.manifest = manifest
        self.tables = {t["table_id"]: t for t in manifest["tables"]}
        self.library = library or il.load()
        self.interpreter, self.resolver = interpreter, resolver
        self.matcher = matcher or ContextMatcher(manifest, context_method)
        self.k_candidates, self.k_out, self.alpha = k_candidates, k_out, alpha
        self.combination, self.use_soft, self.binding_threshold = combination, use_soft, binding_threshold
        self.profile_cache = profile_cache

    def config(self):
        return {"il_version": il.version(self.library), "il_sha256": self.library["_sha256"],
                "context_method": self.matcher.method, "k_candidates": self.k_candidates, "k_out": self.k_out,
                "alpha": self.alpha, "combination": self.combination, "use_soft": self.use_soft,
                "binding_threshold": self.binding_threshold, "profiler_version": profiler.PROFILER_VERSION,
                "aligner_version": aligner.ALIGNER_VERSION,
                "interpreter": getattr(self.interpreter, "metadata", {}), "resolver": getattr(self.resolver, "metadata", {})}

    def run(self, u, *, input_id="input", interpretation=None, grounding=None):
        timing = {}
        t0 = time.perf_counter()
        # 1. Interpreter
        if interpretation is None:
            interpretation = interpret(u, self.interpreter, self.library["vocabulary"], input_id=input_id).to_dict()
        timing["interpreter_ms"] = interpretation.get("elapsed_ms", 0.0)
        q = interpretation["context_query"]
        # 2. Context matching
        candidates, timing["context_matching_ms"] = self.matcher.retrieve(q, self.k_candidates)
        # 3. Grounder
        if grounding is None:
            grounding = ground(interpretation, self.library, self.resolver)
        timing["grounder_ms"] = grounding["elapsed_ms"]
        grounded = grounding["status"] == GROUNDED
        # 4. Table Profiler (only needed when there are requirements to assess)
        profiles, prof_ms, hits = {}, [], 0
        if grounded:
            for tid, _ in candidates:
                p = profiler.profile(self.tables[tid], cache_dir=self.profile_cache)
                profiles[tid] = p
                prof_ms.append(p["elapsed_ms"])
                hits += p["cache_hit"]
        timing["profiler_ms"] = round(sum(prof_ms), 3)
        timing["profiler_cache_hits"] = hits
        timing["profiled_tables"] = len(prof_ms)
        # 5. Aligner
        assessments, align_ms = {}, []
        if grounded:
            for tid, _ in candidates:
                a = aligner.assess(self.tables[tid], profiles[tid], grounding, use_soft=self.use_soft,
                                   binding_threshold=self.binding_threshold)
                assessments[tid] = a
                align_ms.append(a["elapsed_ms"])
        timing["aligner_ms"] = round(sum(align_ms), 3)
        # 6. Ranking
        t_rank = time.perf_counter()
        ranking = []
        for tid, r in candidates:
            a = assessments.get(tid)
            if a is None:
                U, state, A = r, None, None
            else:
                A, state = a["A"], a["state"]
                U = (combine_linear(r, A, self.alpha) if self.combination == "linear" else
                     combine_product(r, A, 1 - self.alpha) if self.combination == "product" else r)
            ranking.append({"table_id": tid, "r": r, "A": A, "state": state, "U": round(U, 6)})
        if grounded and self.combination == "lexicographic":
            ranking.sort(key=lambda x: (STATE_ORDER[x["state"]], -x["A"], -x["r"], x["table_id"]))
        else:
            ranking.sort(key=lambda x: (-x["U"], x["table_id"]))
        for i, item in enumerate(ranking, 1):
            item["rank"] = i
        timing["ranking_ms"] = round((time.perf_counter() - t_rank) * 1000, 3)
        timing["total_ms"] = round((time.perf_counter() - t0) * 1000 + timing["interpreter_ms"], 3)
        return {"input_id": input_id, "input": u, "created": datetime.now(timezone.utc).isoformat(),
                "interpretation": interpretation, "context_query": q, "grounding": grounding,
                "mode": "intention_grounded" if grounded else "context_only_fallback",
                "ranking": ranking, "top_k": [x["table_id"] for x in ranking[: self.k_out]],
                "assessments": assessments, "timing": timing, "config": self.config()}
