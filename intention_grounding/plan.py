"""The experiment plan for the paper: one uniform matrix, a smoke test, resumable runs, one state file.

  python -m intention_grounding.plan list   [--only PATTERN]     # cells and what each runs
  python -m intention_grounding.plan smoke  [--only PATTERN]     # every cell on a few queries; checks sanity
  python -m intention_grounding.plan run    [--only PATTERN] [--force]
  python -m intention_grounding.plan status

A cell = (dataset, context matcher, LLM profile). Each cell is one call of experiments.py with every system
that belongs to it (context only, intention grounding with gold / rule / LLM components, raw and min-max r,
query-rewrite controls, rerankers). Results go to experiments/results/<UTC>_plan_<cell>; the mapping from
cell to run directory, code version and status is kept in experiments/plan_state.json, which
paper_tables.py reads. Cells are skipped when they already ran with the same specification
(--force reruns). LLM responses are cached, so rerunning an LLM cell replays cached answers.

Blocks (paper sections):
  B1 RQ1/RQ2/RQ3  IGBench dev + test: every matcher x {context, IG gold, IG rule, IG LLM per profile}
  B2 baselines    rerankers (LLM listwise per profile, cross-encoder), query-rewrite controls, TABERTA,
                  instruction-aware encoders (e5-large-instruct, stella = TARGET's best)
  B3 external     TARGET BIRD + Spider: the same matrix without gold annotations
  B4 RQ4          ablations (IGBench, gold, BM25) and single-process timing; scaling is separate (scaling.py)
"""
import argparse
import fnmatch
import hashlib
import json
import os
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "experiments" / "plan_state.json"
RESULTS = ROOT / "experiments" / "results"
SMOKE = ROOT / "experiments" / "smoke"

TABERTA = "/datastore-beast/servers/Enas/enas/tabert/TABERTA_OWL/models/PC_pairwise_contrastive"

# stella's remote code needs transformers 4.x: its cells run in a pinned environment (see docs/EXPERIMENTS.md)
LEGACY_PYTHON = os.environ.get("IG_LEGACY_PYTHON", "/datastore-beast/servers/Enas/intention/venvs/ig-legacy/bin/python")
LEGACY_MATCHERS = {"stella"}

# matcher id -> (method token used in system names, extra CLI args, extra env, label for tables)
MATCHERS = {
    "bm25":    ("bm25", [], {}, "BM25"),
    "tfidf":   ("tfidf", [], {}, "TF-IDF"),
    "minilm":  ("sbert", [], {}, "SBERT all-MiniLM-L6-v2"),
    "e5":      ("sbert", ["--sbert-model", "intfloat/e5-base-v2"], {}, "e5-base-v2"),
    "bge":     ("sbert", ["--sbert-model", "BAAI/bge-base-en-v1.5"], {}, "bge-base-en-v1.5"),
    "e5i":     ("sbert", ["--sbert-model", "intfloat/multilingual-e5-large-instruct"], {}, "multilingual-e5-large-instruct"),
    "stella":  ("sbert", ["--sbert-model", "NovaSearch/stella_en_400M_v5"], {}, "stella_en_400M_v5"),
    "taberta": ("taberta", [], {"IG_TABERTA_MODEL": TABERTA, "IG_TABERTA_VIEW": "row"}, "TABERTA (PC)"),
    "hybrid":  ("hybrid", [], {}, "Hybrid BM25 + MiniLM"),
}

# LLM profiles: endpoint configuration; "local" profiles need serve_llm*.sh running on this machine
LLMS = {
    "q14": {"label": "Qwen2.5-14B-Instruct (AWQ, vLLM)", "local": "serve_llm.sh", "gpu_gb": 23,
            "env": {"IG_LLM_BASE_URL": "http://127.0.0.1:8765/v1", "IG_LLM_API_KEY": "EMPTY", "IG_LLM_MODEL": "Qwen/Qwen2.5-14B-Instruct-AWQ"}},
    "q32": {"label": "Qwen2.5-32B-Instruct (AWQ, vLLM)", "local": "serve_llm_32b.sh", "gpu_gb": 24.5, "max_workers": 4,
            "env": {"IG_LLM_BASE_URL": "http://127.0.0.1:8765/v1", "IG_LLM_API_KEY": "EMPTY", "IG_LLM_MODEL": "Qwen/Qwen2.5-32B-Instruct-AWQ"}},
    # Groq: key and base URL come from intention_grounding/.env; the model is set here (IG_GROQ_MODEL overrides)
    "groq": {"label": "Groq: {model}", "local": None,
             "env": {"IG_LLM_BASE_URL": "https://api.groq.com/openai/v1", "IG_LLM_MODEL": os.environ.get("IG_GROQ_MODEL", "llama-3.3-70b-versatile")}},
}

DATASETS = {
    "igb-dev":  {"args": [], "store": "chroma", "gold": True, "workers": 16, "label": "IGBench dev"},
    "igb-test": {"args": ["--benchmark", "benchmarks/igbench_v1/test_queries.json"], "store": "chroma", "gold": True, "workers": 16, "label": "IGBench test"},
    "bird":     {"args": ["--corpus", "data/corpus/target-bird-validation/manifest.json", "--benchmark", "benchmarks/target/bird-validation.json"],
                 "store": "faiss", "gold": False, "workers": 32, "label": "TARGET BIRD (dev)"},
    "spider":   {"args": ["--corpus", "data/corpus/target-spider-test/manifest.json", "--benchmark", "benchmarks/target/spider-test.json"],
                 "store": "faiss", "gold": False, "workers": 32, "label": "TARGET Spider (test)"},
}

IGB_MATCHERS = ["bm25", "tfidf", "minilm", "e5", "bge", "e5i", "stella", "taberta", "hybrid"]
TARGET_MATCHERS = ["bm25", "minilm", "e5i", "stella", "taberta"]
RERANK_MATCHERS = {"bm25", "minilm"}
LLM_PROFILES = ["q14", "q32", "groq"]
# rate-limited APIs: run TARGET on a fixed random sample (same seed for every system)
API_SAMPLE = {"bird": 300, "spider": 300}


def systems_for(dataset, matcher, profile):
    m = MATCHERS[matcher][0]
    gold = DATASETS[dataset]["gold"]
    if profile is None:
        s = [f"ctx:{m}", f"ig:rule/index:{m}", f"ig:rule/index:{m}+rnorm=minmax", f"ig:rule/index:{m}+align=0"]
        if gold:
            s += [f"ig:gold/gold:{m}", f"ig:gold/gold:{m}+rnorm=minmax"]
        if matcher in RERANK_MATCHERS:
            s += [f"rerank:ce:{m}"]
        return s
    s = [f"ctx:{m}", f"ig:llm/llm:{m}", f"ig:llm/llm:{m}+repair=1", f"ig:llm/llm:{m}+repair=1+rnorm=minmax",
         f"ig:llm/llm:{m}+repair=1+align=0"]
    if gold and matcher == "bm25":  # component isolation (RQ3)
        s += ["ig:gold/llm:bm25+repair=1", "ig:llm/index:bm25+repair=1"]
    if matcher in RERANK_MATCHERS:
        s += [f"rerank:llm:{m}"]
        if gold:  # combination: LLM reranker + intention grounding's verdicts (same LLM; gold = oracle grounding)
            s += [f"rerank:llmig:{m}", f"rerank:llmgold:{m}"]
    return s


def cells():
    out = []
    for ds in DATASETS:
        ms = IGB_MATCHERS if DATASETS[ds]["gold"] else TARGET_MATCHERS
        for mt in ms:
            for prof in [None] + LLM_PROFILES:
                if prof is not None and mt not in ("bm25", "minilm", "hybrid", "bge", "taberta", "stella"):
                    continue  # LLM configurations on the main matchers only (cost)
                if prof is not None and not DATASETS[ds]["gold"] and mt not in ("bm25", "minilm", "taberta"):
                    continue
                cid = f"{ds}.{mt}" + (f".{prof}" if prof else "")
                out.append({"id": cid, "block": "B1" if DATASETS[ds]["gold"] else "B3", "dataset": ds, "matcher": mt,
                            "profile": prof, "systems": systems_for(ds, mt, prof)})
    for ds in ("igb-dev", "igb-test"):
        from .experiments import ABLATIONS
        out.append({"id": f"{ds}.ablations", "block": "B4", "dataset": ds, "matcher": "bm25", "profile": None, "systems": ["ctx:bm25", "ig:gold/gold:bm25"] + list(ABLATIONS)})
        out.append({"id": f"{ds}.timing", "block": "B4", "dataset": ds, "matcher": "bm25", "profile": None, "workers": 1,
                    "systems": ["ctx:bm25", "ig:gold/gold:bm25", "ig:rule/index:bm25"]})
    return out


def spec_hash(cell):
    from . import aligner, grounder, profiler
    from .interpreter import providers
    code = "|".join([profiler.PROFILER_VERSION, aligner.ALIGNER_VERSION, grounder.PROMPT_VERSION, providers.PROMPT_VERSION])
    payload = json.dumps([cell["dataset"], cell["matcher"], cell["profile"], sorted(cell["systems"]), MATCHERS[cell["matcher"]][1:3],
                          LLMS.get(cell["profile"] or "", {}).get("env"), code], sort_keys=True)
    return hashlib.sha256(payload.encode()).hexdigest()[:12]


def load_state():
    return json.loads(STATE.read_text()) if STATE.exists() else {}


def save_state(state, cell_id=None):
    """Write the state; with cell_id, merge only that cell into the file as it is now (several plan runs may share it)."""
    import fcntl
    STATE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE.with_suffix(".lock"), "w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        if cell_id is not None:
            current = load_state()
            current[cell_id] = state[cell_id]
            state = current
        tmp = STATE.with_suffix(f".{os.getpid()}.tmp")
        tmp.write_text(json.dumps(state, indent=1))
        os.replace(tmp, STATE)


def endpoint_model(base_url, key="EMPTY"):
    try:
        req = urllib.request.Request(base_url.rstrip("/") + "/models", headers={"Authorization": "Bearer " + key, "User-Agent": "intention-grounding/1.0 (+python)"})
        with urllib.request.urlopen(req, timeout=10) as r:
            return {m["id"] for m in json.loads(r.read()).get("data", [])}
    except Exception:
        return set()


OUR_VLLM = "/datastore-beast/servers/Enas/intention/venvs/vllm/bin/vllm serve"  # never touch other users' servers


def gpu_free_gb():
    try:
        out = subprocess.run(["nvidia-smi", "--query-gpu=memory.free", "--format=csv,noheader,nounits"], capture_output=True, text=True).stdout
        return float(out.split()[0]) / 1024
    except Exception:
        return 0.0


def ensure_llm(profile):
    """Local profiles: make sure the right model is served (start/replace vLLM). API profiles: check the key."""
    cfg = LLMS[profile]
    want = cfg["env"]["IG_LLM_MODEL"]
    if cfg["local"] is None:
        from .llm import config
        os.environ.update({k: v for k, v in cfg["env"].items()})
        key = config()["api_key"]
        if not key:
            return False, "no API key (intention_grounding/.env)"
        models = endpoint_model(cfg["env"]["IG_LLM_BASE_URL"], key)
        return (want in models), (f"model {want} available" if want in models else f"model {want} not offered; have {sorted(models)[:12]}")
    url = cfg["env"]["IG_LLM_BASE_URL"]
    if want in endpoint_model(url):
        return True, "already served"
    need = LLMS[profile].get("gpu_gb", 16)
    log_path = ROOT / "experiments" / f"server_{profile}_serve.log"
    for attempt in range(1, 41):  # shared GPU: other jobs may take memory back while the model loads -> retry
        subprocess.run(["pkill", "-f", OUR_VLLM], check=False)
        time.sleep(15)
        waited = 0
        while not (gpu_free_gb() >= need and (time.sleep(120) or gpu_free_gb() >= need)):  # free twice, 2 min apart
            if waited % 1800 == 0:
                print(f"== waiting for {need} GB free GPU memory (free now: {gpu_free_gb():.1f} GB)", flush=True)
            time.sleep(300)
            waited += 300
            if waited > 72 * 3600:
                return False, "GPU never had enough free memory"
        print(f"== starting {want} (attempt {attempt}, {gpu_free_gb():.1f} GB free)", flush=True)
        with open(log_path, "w") as log:
            subprocess.Popen(["bash", str(ROOT / cfg["local"])], stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
        for _ in range(120):
            time.sleep(10)
            if want in endpoint_model(url):
                return True, f"started (attempt {attempt})"
            if "Engine process failed to start" in log_path.read_text(errors="replace"):
                break
        print(f"== {want} did not come up (attempt {attempt}); retrying in 10 minutes", flush=True)
        time.sleep(600)
    return False, "vLLM did not come up after 40 attempts"


def command(cell, *, smoke=False, out=None):
    ds = DATASETS[cell["dataset"]]
    _, margs, _, _ = MATCHERS[cell["matcher"]]
    method = MATCHERS[cell["matcher"]][0]
    python = LEGACY_PYTHON if cell["matcher"] in LEGACY_MATCHERS and os.path.exists(LEGACY_PYTHON) else sys.executable
    cmd = [python, "-m", "intention_grounding.experiments", "--vector-store", ds["store"], *ds["args"], *margs,
           "--context", method, "--systems", ",".join(cell["systems"]), "--workers", str(cell.get("workers", min(ds["workers"], LLMS[cell["profile"]].get("max_workers", 99)) if cell["profile"] else ds["workers"]))]
    if cell["profile"]:
        cmd.append("--allow-live")
        if LLMS[cell["profile"]]["local"] is None and cell["dataset"] in API_SAMPLE:
            cmd += ["--sample", str(API_SAMPLE[cell["dataset"]])]
    if smoke:
        cmd += ["--limit", "6" if ds["gold"] else "12", "--out", str(out), "--tag", "smoke_" + cell["id"].replace(".", "_")]
    else:
        cmd += ["--tag", "plan_" + cell["id"].replace(".", "_")]
    return cmd


def env_for(cell):
    env = dict(os.environ, PYTHONUNBUFFERED="1")
    env.update(MATCHERS[cell["matcher"]][2])
    if cell["profile"]:
        env.update(LLMS[cell["profile"]]["env"])
        env.setdefault("IG_LLM_TIMEOUT", "600")
    return env


def check(run_dir, cell):
    """Sanity checks on a finished run: every system present; no system collapsed; LLM systems actually used the LLM."""
    problems = []
    summary = json.loads((run_dir / "summary.json").read_text())
    got = {s["system"]: s for s in summary["systems"]}
    for name in cell["systems"]:
        s = got.get(name)
        if s is None:
            problems.append(f"{name}: missing")
            continue
        if s.get("ndcg@10") is not None and s["ndcg@10"] < 0.05:
            problems.append(f"{name}: nDCG@10 {s['ndcg@10']} (collapsed?)")
    for f in run_dir.glob("predictions_*.jsonl"):
        errs = [json.loads(line) for line in f.read_text().splitlines() if '"mode": "error:' in line]
        if errs:
            problems.append(f"{f.stem}: {len(errs)} request(s) ended in an error ({errs[0].get('mode')})")
    for f in run_dir.glob("predictions_ig_llm*.jsonl"):
        rows = [json.loads(line) for line in f.read_text().splitlines() if line.strip()]
        fails = [r for r in rows if str((r.get("interpretation") or {}).get("failure") or "").startswith("PROVIDER_FAILURE")]
        if fails:
            problems.append(f"{f.stem}: {len(fails)}/{len(rows)} LLM calls failed (PROVIDER_FAILURE: {(fails[0]['interpretation'] or {}).get('failure')})")
    for f in run_dir.glob("predictions_rerank_llm*.jsonl"):
        rows = [json.loads(line) for line in f.read_text().splitlines() if line.strip()]
        fb = [r for r in rows if str(r.get("status") or "").startswith("fallback")]
        if len(fb) > max(1, 0.1 * len(rows)):
            problems.append(f"{f.stem}: {len(fb)}/{len(rows)} reranker calls fell back ({fb[0]['status'][:200]})")
    return problems


def run_cells(selected, *, smoke=False, force=False):
    state = load_state()
    by_profile = {}
    for c in selected:
        by_profile.setdefault(c["profile"], []).append(c)
    out_root = SMOKE / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") if smoke else RESULTS
    report = []
    for profile in sorted(by_profile, key=lambda p: (p is not None, p or "")):
        if profile is None and any(endpoint_model(LLMS[p]["env"]["IG_LLM_BASE_URL"]) for p in LLMS if LLMS[p]["local"]):
            subprocess.run(["pkill", "-f", OUR_VLLM], check=False)  # free the GPU for encoders / cross-encoder
            time.sleep(20)
            print("== stopped local LLM server for cells without an LLM", flush=True)
        pending = [c for c in by_profile[profile] if smoke or force or not (state.get(c["id"], {}).get("status") == "done"
                                                                              and state[c["id"]].get("spec") == spec_hash(c))]
        if profile and not pending:
            for c in by_profile[profile]:
                report.append((c["id"], "cached", state[c["id"]]["run"]))
            continue
        if profile:
            ok, why = ensure_llm(profile)
            print(f"== LLM profile {profile}: {why}", flush=True)
            if not ok:
                for c in by_profile[profile]:
                    report.append((c["id"], "skipped", why))
                continue
        for c in by_profile[profile]:
            h = spec_hash(c)
            prev = state.get(c["id"])
            if not smoke and not force and prev and prev.get("status") == "done" and prev.get("spec") == h:
                report.append((c["id"], "cached", prev["run"]))
                continue
            t0 = time.time()
            print(f"== [{datetime.now().strftime('%H:%M:%S')}] {'smoke' if smoke else 'run'} {c['id']}: {len(c['systems'])} systems", flush=True)
            tag = ("smoke_" if smoke else "plan_") + c["id"].replace(".", "_")
            for attempt in range(3):  # an LLM server lost mid-cell (shared GPU): restart it and rerun; cached answers replay
                proc = subprocess.run(command(c, smoke=smoke, out=out_root), cwd=ROOT, env=env_for(c), capture_output=True, text=True)
                runs = sorted((out_root if smoke else RESULTS).glob(f"*_{tag}"))
                lost = proc.returncode == 0 and runs and (runs[-1] / "summary.json").exists() and \
                    any("PROVIDER_FAILURE" in p for p in check(runs[-1], c))
                if not (lost and profile and LLMS[profile]["local"]):
                    break
                print(f"   -> LLM calls failed (server lost?); restarting the server and rerunning (attempt {attempt + 2})", flush=True)
                ensure_llm(profile)
            if proc.returncode != 0 or not runs or not (runs[-1] / "summary.json").exists():
                err = (proc.stderr or proc.stdout).strip().splitlines()[-3:]
                report.append((c["id"], "FAILED", " | ".join(err)))
                print(f"   -> FAILED {' | '.join(err)}", flush=True)
                if not smoke:
                    state[c["id"]] = {"status": "failed", "spec": h, "error": err, "at": datetime.now(timezone.utc).isoformat()}
                    save_state(state, c["id"])
                continue
            run = runs[-1]
            problems = check(run, c)
            if not smoke:
                from .breakdown import breakdown
                breakdown(run)
                state[c["id"]] = {"status": "done" if not problems else "check", "spec": h, "run": run.name, "problems": problems,
                                  "block": c["block"], "dataset": c["dataset"], "matcher": c["matcher"], "profile": c["profile"],
                                  "seconds": round(time.time() - t0, 1), "at": datetime.now(timezone.utc).isoformat()}
                save_state(state, c["id"])
            report.append((c["id"], "ok" if not problems else "CHECK", "; ".join(problems) or f"{time.time() - t0:.0f}s"))
            print(f"   -> {report[-1][1]} {report[-1][2]}", flush=True)
    print("\n== summary")
    for cid, st, info in report:
        print(f"  {st:8s} {cid:32s} {info}")
    return report


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("action", choices=["list", "smoke", "run", "status"])
    p.add_argument("--only", default="*", help="glob over cell ids, comma-separated (e.g. 'igb-*.bm25*,bird.*')")
    p.add_argument("--skip-profile", default="", help="comma-separated LLM profiles to leave out")
    p.add_argument("--force", action="store_true")
    a = p.parse_args(argv)
    pats = a.only.split(",")
    skip = set(filter(None, a.skip_profile.split(",")))
    selected = [c for c in cells() if any(fnmatch.fnmatch(c["id"], pt) for pt in pats) and (c["profile"] or "") not in skip]
    if a.action == "list":
        for c in selected:
            print(f"{c['block']}  {c['id']:28s} {len(c['systems']):2d} systems  {', '.join(c['systems'])}")
        print(f"{len(selected)} cells")
    elif a.action == "status":
        st = load_state()
        for c in selected:
            s = st.get(c["id"], {})
            print(f"{s.get('status', '-'):7s} {c['id']:28s} {s.get('run', '')} {'; '.join(s.get('problems', []) or [])}")
    else:
        run_cells(selected, smoke=a.action == "smoke", force=a.force)


if __name__ == "__main__":
    main()
