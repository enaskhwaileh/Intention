# Experiment plan for the paper

One uniform matrix, run by `python -m intention_grounding.plan`, smoke-tested before the full run, resumable, with
a single state file (`experiments/plan_state.json`) and generated tables (`python -m intention_grounding.paper_tables`
→ `experiments/paper/tables.md` + CSV). Every number in the paper should come from these two commands.

## Design

A **cell** = (dataset, context matcher, LLM profile). Each cell runs all systems that belong to it on exactly the same
queries, so every comparison is paired.

| Axis | Values |
|---|---|
| Datasets | IGBench dev (36 requests, used for design decisions), IGBench test (21, held out), TARGET BIRD dev (1,533 questions, 75 tables), TARGET Spider test (2,147 questions, 180 tables) |
| Context matchers | BM25, TF-IDF, SBERT all-MiniLM-L6-v2, e5-base-v2, bge-base-en-v1.5, multilingual-e5-large-instruct (instruction-aware; used by TARGET), stella_en_400M_v5 (TARGET's best retriever), **TABERTA (PC model, RowView)**, Hybrid BM25 + MiniLM. TARGET: BM25, MiniLM, e5-large-instruct, stella, TABERTA |
| Interpreter + Grounder | gold (oracle, IGBench only); rule + index (no model); LLM + LLM with Qwen2.5-14B, Qwen2.5-32B (local, vLLM) and a Groq-hosted model |
| Ranking | F(r, A) = r(0.5 + 0.5A) with raw r and with r rescaled (min-max) over the candidates |

Systems per cell:

- `ctx:<m>`: the matcher alone (baseline).
- `ig:<I>/<G>:<m>[+rnorm=minmax]`: intention grounding on top of the matcher.
- `ig:...+align=0`: **query-rewrite control**: retrieval with the Interpreter's q_u, no grounding/alignment.
- `rerank:ce:<m>`: **cross-encoder reranker** (bge-reranker-v2-m3) over the matcher's top 20.
- `rerank:llm:<m>`: **LLM listwise reranker** with the same LLM, judging usefulness for the request from the same
  table documentation (title, description, attributes), without the Intention Library, profiles or alignment.
- Component isolation (RQ3): `ig:gold/llm` (LLM Grounder alone), `ig:llm/index` (LLM Interpreter alone).

## Mapping to research questions and tables

| RQ / section | Question | Table |
|---|---|---|
| RQ1 | Does intention grounding improve usefulness ranking over each context matcher, and over rerankers? | T1 (per matcher × configuration), T4 (all baselines), T5 (TARGET) |
| RQ2 | Does the ranking respond to the intention when the topic is fixed? | T2 (intention-swap accuracy) |
| RQ3 | How accurately are intentions extracted and grounded, per component and LLM? | T3 |
| Generality | Does it hold on an established benchmark, and where does the change come from? | T5, T6 (breakdown by interpretation/grounding outcome) |
| RQ4 | Which components matter; what does each stage cost? | T7 (ablations), T8 (running time), scaling (`scaling.py`) |

## Protocol

1. Decisions (prompt versions, r normalisation, thresholds) are taken on IGBench dev; IGBench test is reported as the
   main result. The prompt v3.1 fixes were prompted by errors seen in a test run; this is stated, and the zero-shot
   v3.0 results are kept as an appendix row.
2. Every Δ is paired against the same matcher on the same queries (randomization test, 10,000 permutations,
   bootstrap 95% CI). API-hosted LLMs on TARGET use a fixed random sample of 300 questions per dataset (seed 13);
   their baselines are computed on the same sample.
3. All LLM responses are cached (content-addressed by model, prompt and messages): reruns replay them exactly.
   Temperature 0, JSON mode, at most one validator-guided repair (`+repair=1`, reported as an extension of
   Algorithms 1–2; `repair=0` rows are kept).
4. Smoke test before the full run: `plan smoke` runs a representative cell of every code path on 6–12 queries and
   checks that every system ran, none collapsed (nDCG@10 < 0.05), no request ended in an error, and LLM systems
   actually used the LLM.
5. Reproducibility: code version and cell specification are hashed into the state file; stella runs in a pinned
   environment (`venvs/ig-legacy`, transformers 4.44) because its model code does not run on transformers 5.

## Issues found by the smoke test and fixed before the full run

- LLM server and GPU encoders competing for GPU memory → vLLM memory share lowered (32B: 0.72, 14B: 0.55).
- stella requires xformers and transformers 4.x → memory-efficient attention off (model card) and pinned environment.
- LLM Interpreter mixing argument and scope labels; the repair could not help because the validator only reported
  `UNKNOWN_LABEL` → validator and contract messages now name the offending label/reference and where it belongs
  (the validation rules are unchanged). On a BIRD smoke sample, Interpreter failures fell from 7/12 to 1/12.
- A malformed LLM answer (a list where an id was expected) crashed a run → malformed answers are now contract
  failures, and any unexpected error is recorded per request and ranked by context alone, never aborting a run.
- TABERTA model 7 (`wikidbs-public/TABERTA/7_hybrid_model_reg`) and model 6 produce collapsed embeddings
  (mean cosine between different tables 0.92–0.97; R@1 = 0 on BIRD); the PC model (TABERTA_OWL) is used as the
  TABERTA baseline, with its training serialization (RowView).

## Commands

```sh
source /datastore-beast/servers/Enas/intention/env.sh
python -m intention_grounding.plan list                         # 86 cells
python -m intention_grounding.plan smoke --only "igb-dev.*"     # quick sanity
python -m intention_grounding.plan run --skip-profile groq      # full run (resumable)
python -m intention_grounding.plan run --only "*.groq"          # Groq cells once the key is in intention_grounding/.env
python -m intention_grounding.plan status
python -m intention_grounding.paper_tables                      # experiments/paper/tables.md
```
