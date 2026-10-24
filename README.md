# Intention Grounding for Dataset Discovery

Implementation of the framework in *Intention Grounding for Dataset Discovery* (Khwaileh, Gatt, Velegrakis).
Given a request `u`, the system retrieves tables that match its context **and** provide the data needed for
the analysis the user intends (compare, aggregate, predict, explain, monitor), and explains every decision.

```
u ──Interpreter──► (q_u, ι_u)
        q_u ──Context matching──► top-k tables T with r(q_u, T)
                     T ──Table Profiler──► Φ(T)
        ι_u ──Grounder (+ Intention Library L)──► (g_u, Ψ_u, s_G)
                    (Φ(T), Ψ_u) ──Aligner──► A(T, ι_u) with requirement verdicts and evidence
        U(T | q_u, ι_u) = F(r, A)  (r alone when ι_u = ⊥ or grounding is not completed)
```

| Paper component | Module | What it does |
|---|---|---|
| Interpreter (§3.1, Alg. 1) | `interpreter/` | One extraction call returning the context query `q_u` and the intention record `ι_u = (e_u, B_u, Ω_u)`; validates JSON, labels, ids and that every span occurs in `u`; status `extracted` / `no_intention` / `failure` (fallback `q_u = u`). Providers: LLM (any OpenAI-compatible endpoint), recorded replay, rule baseline. |
| Intention Library (§3.2) | `library/intention-library-v1.0.json`, `il.py` | Release `L = (J, O, P, R, E, v)`: 5 families, 7 variants, 9 procedures, 9 operators, 55 requirement records over the axes sem/str/cov/qual/aff, evidence rules and an expression index. Registration checks on load. Spec: [docs/INTENTION_LIBRARY.md](docs/INTENTION_LIBRARY.md). |
| Grounder (§3.3, Alg. 2) | `grounder.py` | A resolver (LLM, replay, or the expression-index baseline) proposes a variant and role→entry references; contract validation, value binding, procedure applicability and requirement instantiation `Ψ_u` (Eq. 21) are deterministic. Statuses: grounded, insufficient, ambiguous, unsupported, failure, not_attempted. |
| Context matching (§3.4) | `context.py` | Serialises each table (title, description, attributes and their documentation) and scores `r(q_u, T) ∈ [0, 1]` with BM25, TF-IDF, LSA, Sentence-BERT or a hybrid; returns the top-k candidates. |
| Table Profiler (§3.5) | `profiler.py` | Full-scan capability profile `Φ(T)` for any CSV: types, missingness, distinct values, numeric ranges, temporal extent and grain, geographic level (gazetteer), documented measure kind (count, amount, level, rate, mean, cumulative), keys, panel / wide / aggregated-cell structure. Content-addressed cache. |
| Aligner (§3.6) | `aligner.py` | Binds the symbolic slots of `Ψ_u` to attributes using names, documentation and values; evaluates each requirement with a registered predicate under its evidence rule (supported / violated / unresolved + evidence); combines per procedure (all hard supported → supported, any violated → violated) and across alternative procedures; computes `A(T, ι_u)` with soft indicators. |
| Ranking (§3.7) | `pipeline.py` | `U = F(r, A)`; default `F(r, A) = r (½ + ½ A)` (nondecreasing, `F ≤ r`); linear and lexicographic forms for ablation; context-only fallback when no intention is grounded. Records the running time of every stage. |
| Experiments (§4) | `experiments.py`, `scaling.py`, `report.py` | RQ1–RQ4 on IGBench: baselines, ablations, intention-swap analysis, interpretation/grounding accuracy, per-stage timing and scalability. Design: [docs/EXPERIMENTS.md](docs/EXPERIMENTS.md). |
| Corpus and benchmark | `corpus.py`, `benchmarks/igbench_v1/` | IGBench-v1: 3,300 documented real tables (Our World in Data COVID-19, UCI bike sharing, Rdatasets) with intention-paired queries. Rationale: [docs/DATASET.md](docs/DATASET.md). |

## Setup

```sh
python3 -m venv .venv && ./.venv/bin/pip install -e .           # pandas, numpy, scikit-learn
./.venv/bin/python -m intention_grounding.acquire                # UCI bike tables (once)
./.venv/bin/python -m intention_grounding.corpus fetch           # OWID + Rdatasets at pinned commits (git, ~1.5 GB)
./.venv/bin/python -m intention_grounding.corpus build           # data/corpus/igbench-v1/manifest.json
./.venv/bin/python -m unittest discover -s tests                 # offline tests (Figure 1 fixture)
```

LLM components (optional) read `intention_grounding/.env` (see `.env.example`): `IG_LLM_API_KEY`, `IG_LLM_MODEL`,
`IG_LLM_BASE_URL` (Groq by default; `GROQ_API_KEY` / `GROQ_MODEL_ID` also work). Every LLM response is cached under
`data/runtime/llm-cache/`; new calls happen only with `--allow-live`.

## Use

```sh
python -m intention_grounding.cli "Compare the average survival rate of Titanic passengers across passenger classes" --html run.html
python -m intention_grounding.cli "..." --interpreter llm --resolver llm --allow-live      # LLM Interpreter + Grounder
python -m intention_grounding.cli --describe compare.group_means                           # one Intention Library variant
```

The text output lists the extraction, the grounded variant and procedures, and for every ranked table its state,
`A`, `r`, `U` and the verdict string of the best procedure; `--html` writes an explanation page with the evidence
behind each verdict and the timing of each stage.

## Experiments

```sh
python -m intention_grounding.experiments --systems main --benchmark benchmarks/igbench_v1/test_queries.json
python -m intention_grounding.experiments --systems ablations
python -m intention_grounding.experiments --systems ctx:sbert,ig:gold/gold:sbert --context sbert     # needs .[sbert]
python -m intention_grounding.experiments --systems ig:llm/llm:bm25 --allow-live                      # needs an LLM key
python -m intention_grounding.scaling --sample 300
```

Each run writes `experiments/results/<run>/results.md` (paper-ready tables), `summary.json`, per-system metrics and
predictions. System names: `ctx:<method>` (context only on `u`) and `ig:<interpreter>/<resolver>:<method>[+options]`
with interpreter ∈ {gold, rule, llm}, resolver ∈ {gold, index, llm}, options `comb=product|linear|lexicographic`,
`alpha=`, `k=`, `soft=0|1`, `bind=`.

Current results and their status are in [docs/EXPERIMENTS.md](docs/EXPERIMENTS.md). Usefulness labels are **draft
author labels**; they must be independently reviewed before effectiveness claims are reported.

## Repository layout

- `intention_grounding/` – framework (modules above), `library/` (IL release), `resources/gazetteer.json` (declared country→continent mapping with provenance)
- `benchmarks/igbench_v1/` – query builders and `queries.json` (development) / `test_queries.json` (held-out)
- `data/corpus/igbench-v1/manifest.json` – corpus definition with pinned sources and hashes (tables are rebuilt, not committed)
- `experiments/` – result summaries and scaling measurements
- `docs/` – Intention Library spec, dataset rationale, experimental design
- `tests/` – unit and integration tests (stdlib `unittest`)
