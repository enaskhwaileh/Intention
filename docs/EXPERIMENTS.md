# Experimental design and current results

This document fixes the experimental protocol for Section 4 of the paper and records the current runs. All numbers
use **draft author labels** (`draft_author_labels_unreviewed`); treat them as a pilot until the labels are reviewed
(protocol in `DATASET.md`).

## Research questions and how each is measured

| RQ | Question (paper) | Measurement | Script |
|---|---|---|---|
| RQ1 | Does intention-aware alignment improve usefulness ranking over lexical, semantic, structure-aware and instruction-aware retrieval? | nDCG@10 (graded gains), P@5, P@10, R@10, MRR, Useful@1, Topical-only@1; framework on top of each context matcher vs. that matcher alone; paired randomization test + bootstrap CI | `experiments.py --systems main` |
| RQ2 | Does the ranking respond correctly when the intention changes and the topic stays fixed? | Intention-swap accuracy over request pairs of one topic (0.5 = indifferent) | same run |
| RQ3 | How accurately does the framework construct grounded intentions and table capability profiles? | Interpreter: intention presence, argument F1, scope F1. Grounder: status, family, variant, binding accuracy, fallback rate. Aligner: precision/recall of the supported state against useful labels | same run |
| RQ4 | Which components account for effectiveness, and what overhead do they add? | Ablations (below); per-stage time, cold and warm caches; profiling/alignment time vs. table size | `--systems ablations`, `scaling.py` |

**Systems.** `ctx:<m>`: context matching on the full input. `ig:<I>/<R>:<m>`: the framework with Interpreter
`I` ∈ {gold, rule, llm}, resolver `R` ∈ {gold, index, llm} and context matcher `m`. Gold = recorded annotation
(isolates grounding + alignment); rule/index = automatic, no model; llm = the paper's configuration.

**Protocol.** Development set (36 requests) for building the system; design frozen (IL 1.0.0, Profiler 3.0.0,
Aligner 1.0, product combination with λ = 0.5); held-out test set (21 requests, new topics) written and labelled after
the freeze. Report test results as the main table and development results separately. Fixed seeds; context indexes
and profiles are cached and their build time reported separately.

## Results (pilot, draft labels)

### RQ1 / RQ2 – held-out test set (21 requests, 20 with a useful table)

| System | nDCG@10 | P@5 | MRR | Useful@1 | Swap acc. |
|---|---|---|---|---|---|
| ctx:bm25 | 0.828 | 0.530 | 0.917 | 0.85 | 0.871 |
| ctx:tfidf | 0.775 | 0.460 | 0.765 | 0.60 | 0.862 |
| ctx:lsa | 0.806 | 0.540 | 0.829 | 0.70 | 0.863 |
| ig:gold/gold:bm25 | **0.857** | **0.550** | **0.975** | **0.95** | 0.882 |
| ig:rule/index:bm25 | 0.826 | 0.540 | 0.900 | 0.80 | 0.882 |
| ig:gold/gold:tfidf | 0.834 | 0.510 | 0.917 | 0.85 | 0.882 |
| ig:rule/index:tfidf | 0.823 | 0.500 | 0.917 | 0.85 | 0.882 |

Significance vs. the same context matcher (test): gold/gold:tfidf nDCG +0.057 [0.006, 0.103], p = 0.046; MRR +0.152,
p = 0.038. gold/gold:bm25 nDCG +0.027 [−0.018, 0.067], p = 0.25 (11 wins / 5 losses). rule/index:bm25 ≈ bm25.

### Development set (36 requests)

| System | nDCG@10 | P@5 | MRR | Useful@1 | Swap acc. |
|---|---|---|---|---|---|
| ctx:bm25 | 0.768 | 0.486 | 0.895 | 0.80 | 0.804 |
| ctx:tfidf | 0.730 | 0.469 | 0.795 | 0.66 | 0.799 |
| ig:gold/gold:bm25 | 0.796 | 0.537 | 0.879 | 0.77 | 0.860 |
| ig:rule/index:bm25 | 0.788 | 0.531 | 0.910 | 0.83 | 0.843 |
| ig:gold/gold:tfidf | 0.801 | 0.520 | 0.876 | 0.77 | 0.819 |

Significance (dev): gold/gold:tfidf nDCG +0.069 [0.035, 0.106], p < 0.001; gold/gold:bm25 nDCG +0.027, p = 0.047;
rule/index:tfidf nDCG +0.032, p = 0.005.

### RQ3 – construction accuracy

| Configuration | Argument F1 | Scope F1 | Grounding status | Variant | Binding acc. | Fallback | Assessment P / R |
|---|---|---|---|---|---|---|---|
| rule/index (test) | 0.815 | 0.950 | 1.000 | 0.947 | 0.807 | 0.000 | 0.55 / 0.63 |
| rule/index (dev) | 0.825 | 0.970 | 0.833 | 0.812 | 0.688 | 0.188 | 0.48 / 0.78 |
| gold/gold (test) | – | – | – | – | – | – | 0.58 / 0.75 |

Assessment precision is bounded by design: the Aligner judges whether a table *can support* the procedure, not whether
it is on topic, so on-topic filtering comes from $r$ and the product combination. The LLM rows are filled by running
`--systems ig:llm/llm:bm25 --allow-live` with a key.

### RQ4 – ablations (test set, gold/gold, BM25)

| Variant | nDCG@10 | MRR | Useful@1 |
|---|---|---|---|
| Product F, λ = 0.5 (default) | 0.857 | 0.975 | 0.95 |
| Linear F, α = 0.5 | 0.806 | 0.923 | 0.90 |
| Lexicographic (state, A, r) | 0.742 | 0.912 | 0.90 |
| No soft indicators | 0.854 | 0.975 | 0.95 |
| λ = 0.75 / 0.25 / 0 (α = 0.25 / 0.75 / 1) | 0.861 / 0.808 / 0.764 | 0.975 / 0.927 / 0.908 | 0.95 / 0.90 / 0.90 |
| k = 20 / 100 candidates | 0.862 / 0.857 | 0.975 / 0.975 | 0.95 / 0.95 |
| Binding threshold 0.7 | 0.875 | 1.000 | 1.00 |
| gold extraction + index resolver | 0.847 | 0.950 | 0.90 |
| rule extraction + gold grounding | 0.829 | 0.892 | 0.80 |

Ranking that lets the categorical state dominate (lexicographic) or lets $A$ dominate ($\lambda \to 0$) is worse than
modulating context relevance: supported but off-topic tables otherwise rise above on-topic ones. The binding threshold
of 0.7 is better on test but was not better on development (0.796 → 0.796); the default stays at 0.5.

### RQ4 – running time (ms per request, 3,300-table corpus, single CPU)

| Stage | Cold profile cache (test, gold/gold:bm25) | Warm caches |
|---|---|---|
| Interpreter (rule) / LLM | 0.1–0.4 | 0.1–0.3 (LLM latency recorded per call when used) |
| Context matching (BM25 / LSA) | 5–10 / 28–31 | 5 / 28 |
| Grounder (index) | 0.2–0.4 | 0.2–0.3 |
| Table Profiler (50 candidates) | mean 2,005, median 1,469 | mean 14, median 10 |
| Aligner (50 candidates) | mean 1,083, median 132 | mean 1,034, median 124 |
| Ranking | 0.1 | 0.1 |

One-off index build: BM25 45 ms, TF-IDF 11 ms, LSA 1.2 s. Scalability (`experiments/scaling/`, 314 tables incl. all
large tables): profiling costs about 1.3 s per million cells plus 46 ms (median 18 ms per table); alignment of one
grounded intention against one table has a median below 1 ms and grows with the scoped scans of large tables (up to
~4 s for the 400k-row OWID tables, dominated by loading the table).

## What the pilot shows and what the paper still needs

1. **Direction is consistent, effect is modest on this benchmark.** Gains appear for every context matcher on both
   splits; they are significant for TF-IDF on both splits and for BM25 on development. BM25 alone is already strong
   because each topic cluster is small and the requests name the topic. The paper needs more requests (target ≈150
   over ≈30 topics) and larger same-topic clusters with structural variation (Figure 1 situations) for adequate power.
2. **Run the LLM configuration** (paper's main system) with a key: `ig:llm/llm:{bm25,tfidf}`; responses are cached,
   so the run is paid once. Report LLM token use and latency from `llm-cache`.
3. **Add dense, instruction-aware and structure-aware context matchers** on the Mac environment
   (`--context sbert` with tables and queries embedded by SBERT and stored in ChromaDB; e5/bge via `--sbert-model`; TABERTA and semantic matching
   from the authors' prior work as additional `ContextMatcher` methods). The framework is applied on top of each.
4. **Review the labels** with two annotators and report agreement; re-run without code changes.
5. **External generality:** FollowTable once released (map aggregation-level / column-semantics instructions to
   variants), reporting nDCG and its responsiveness score.

## GPU server runs (beauty, October 2026): dense encoders and score calibration

Environment: `/datastore-beast/servers/Enas/intention/` on beauty (A100 40 GB, 112 cores); code in `Intention/`,
virtual environment `venvs/ig` (Python 3.11, torch 2.6 + CUDA 12.4, sentence-transformers 6.2, ChromaDB 1.5),
caches in `cache/`. `source /datastore-beast/servers/Enas/intention/env.sh` activates everything. Scripts:
`run_server.sh igbench|target`, `run_calibration.sh`, `run_target.sh`. BM25/TF-IDF/MiniLM results reproduce the Mac and
container runs exactly; `--workers N` (queries in parallel, retrieval in the parent) gives identical rankings.

Tables are chunked (title and description, column groups of 12) and embedded once; a table scores its best chunk.
Embedding the 3,300-table corpus (7,938 chunks) with MiniLM takes 6.5 s on the A100.

nDCG@10, change against the same matcher alone, paired randomization p; bold = p < 0.05.

| Context matcher | Split | Context only | IG gold (raw r) | IG gold (min-max r) | IG auto (raw r) | IG auto (min-max r) |
|---|---|---|---|---|---|---|
| BM25 | dev | 0.768 | **0.796** (+0.027, p=0.047) | **0.798** (+0.029, p=0.009) | 0.788 (+0.019, p=0.069) | **0.797** (+0.028, p=0.003) |
| BM25 | test | 0.828 | 0.857 (+0.027, p=0.247) | 0.861 (+0.031, p=0.197) | 0.826 (-0.003, p=0.922) | 0.825 (-0.003, p=0.915) |
| TF-IDF | dev | 0.730 | **0.801** (+0.069, p=0.000) | **0.789** (+0.057, p=0.000) | **0.762** (+0.032, p=0.005) | **0.755** (+0.024, p=0.016) |
| TF-IDF | test | 0.775 | **0.834** (+0.057, p=0.046) | 0.828 (+0.050, p=0.069) | 0.823 (+0.046, p=0.086) | 0.813 (+0.036, p=0.161) |
| SBERT MiniLM-L6 | dev | 0.769 | 0.815 (+0.045, p=0.112) | **0.812** (+0.043, p=0.004) | 0.784 (+0.015, p=0.535) | 0.789 (+0.020, p=0.208) |
| SBERT MiniLM-L6 | test | 0.690 | 0.786 (+0.094, p=0.076) | **0.769** (+0.078, p=0.017) | 0.747 (+0.057, p=0.289) | 0.737 (+0.047, p=0.139) |
| SBERT e5-base-v2 | dev | 0.820 | **0.757** (-0.063, p=0.037) | 0.836 (+0.014, p=0.161) | **0.775** (-0.045, p=0.019) | 0.811 (-0.010, p=0.405) |
| SBERT e5-base-v2 | test | 0.778 | 0.781 (-0.008, p=0.779) | 0.819 (+0.028, p=0.189) | 0.727 (-0.059, p=0.239) | 0.806 (+0.015, p=0.531) |
| SBERT bge-base-en-v1.5 | dev | 0.806 | 0.793 (-0.015, p=0.654) | **0.842** (+0.034, p=0.033) | 0.797 (-0.010, p=0.640) | **0.837** (+0.028, p=0.034) |
| SBERT bge-base-en-v1.5 | test | 0.808 | 0.781 (-0.028, p=0.439) | 0.843 (+0.030, p=0.062) | 0.751 (-0.057, p=0.306) | 0.823 (+0.011, p=0.503) |
| Hybrid (BM25+MiniLM) | dev | 0.814 | 0.821 (+0.006, p=0.726) | 0.820 (+0.006, p=0.457) | 0.811 (-0.003, p=0.843) | 0.822 (+0.008, p=0.263) |
| Hybrid (BM25+MiniLM) | test | 0.845 | 0.842 (-0.009, p=0.756) | 0.878 (+0.026, p=0.329) | 0.828 (-0.022, p=0.465) | 0.852 (+0.001, p=0.979) |

**Finding.** With raw scores, intention grounding helps BM25, TF-IDF and MiniLM but *hurts* the stronger encoders on
development (e5: 0.820 → 0.757, p = 0.037). Their cosine scores occupy a narrow band (≈0.75–0.9), so the factor
(0.5 + 0.5A) outweighs topical relevance and supported off-topic tables rise. Rescaling r over the candidate list
(`+rnorm=minmax`) makes F independent of the matcher's score range: the gold configuration is then never worse than
the matcher alone on either split, and e5/bge become positive (bge dev +0.034, p = 0.033). TF-IDF loses slightly.
The option exists in code; it is not yet the default. Adopting it is a design decision supported by the development set.

## LLM configuration (paper's main system) on the GPU server

Interpreter and Grounder use **Qwen/Qwen2.5-14B-Instruct-AWQ** served by vLLM 0.8.5 on the A100
(`serve_llm.sh`; OpenAI-compatible endpoint, temperature 0, JSON mode; every response cached under
`data/runtime/llm-cache`). Set `IG_LLM_BASE_URL`, `IG_LLM_API_KEY`, `IG_LLM_MODEL` to use any other endpoint.

Prompt versions: **v3.0** = zero-shot prompts as written before any LLM run (the untouched baseline).
**v3.1** fixes two contract errors observed in the first run: the expression example "how has ... changed" invited
non-contiguous expressions, and the resolver wrote values ("mean") instead of entry ids; it adds one illustrative
(invented) example. These errors were seen in the test-set run, so v3.1 is not test-blind; report v3.0 alongside.
`+repair=1`: one validator-guided retry per component (Algorithms 1 and 2 as stated allow none; reported as an extension).

### dev

| Context matcher | Context only | Rule/index | LLM v3.0 (zero-shot) | LLM v3.1 | LLM v3.1 + min-max r | Gold |
|---|---|---|---|---|---|---|
| bm25 | 0.768 | 0.788 (+0.019, p=0.07) | 0.759 (-0.009, p=0.52) | 0.781 (+0.013, p=0.32) | **0.794** (+0.025, p=0.00) | **0.796** (+0.027, p=0.05) |
| tfidf | 0.730 | **0.762** (+0.032, p=0.01) | 0.730 (-0.000, p=1.00) | **0.774** (+0.043, p=0.00) | **0.765** (+0.034, p=0.00) | **0.801** (+0.069, p=0.00) |
| sbert | 0.769 | 0.784 (+0.015, p=0.53) | 0.768 (-0.000, p=0.96) | 0.787 (+0.018, p=0.34) | 0.786 (+0.017, p=0.16) | 0.815 (+0.045, p=0.11) |
| hybrid | 0.814 | 0.811 (-0.003, p=0.84) | 0.802 (-0.011, p=0.34) | 0.807 (-0.006, p=0.68) | 0.819 (+0.005, p=0.41) | 0.821 (+0.006, p=0.73) |

| Configuration (BM25) | Arg. F1 | Scope F1 | Grounding status | Variant | Binding acc. | Fallback | nDCG@10 |
|---|---|---|---|---|---|---|---|
| rule / index | 0.82 | 0.97 | 0.83 | 0.81 | 0.69 | 0.19 | 0.788 |
| LLM v3.0 / LLM v3.0 | 0.75 | 0.91 | 0.19 | 0.12 | 0.12 | 0.88 | 0.759 |
| LLM v3.1 / LLM v3.1 | 0.78 | 0.92 | 0.64 | 0.59 | 0.58 | 0.41 | 0.774 |
| LLM v3.1 / LLM v3.1, one repair | 0.79 | 0.89 | 0.67 | 0.62 | 0.61 | 0.38 | 0.781 |
| LLM v3.1 / index | 0.78 | 0.92 | 0.61 | 0.59 | 0.57 | 0.41 | 0.772 |
| gold / LLM v3.0 | 1.00 | 1.00 | 0.86 | 0.88 | 0.88 | 0.12 | 0.791 |
| gold / LLM v3.1 | 1.00 | 1.00 | 0.92 | 0.94 | 0.94 | 0.06 | 0.791 |
| gold / index | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.796 |

### test

| Context matcher | Context only | Rule/index | LLM v3.0 (zero-shot) | LLM v3.1 | LLM v3.1 + min-max r | Gold |
|---|---|---|---|---|---|---|
| bm25 | 0.828 | 0.826 (-0.003, p=0.92) | 0.820 (-0.008, p=0.53) | 0.807 (-0.020, p=0.38) | 0.810 (-0.018, p=0.43) | 0.857 (+0.027, p=0.25) |
| tfidf | 0.775 | 0.823 (+0.046, p=0.09) | 0.777 (+0.002, p=0.84) | 0.783 (+0.007, p=0.77) | 0.784 (+0.008, p=0.75) | **0.834** (+0.057, p=0.05) |
| sbert | 0.690 | 0.747 (+0.057, p=0.29) | 0.698 (+0.010, p=0.79) | 0.744 (+0.054, p=0.19) | 0.737 (+0.047, p=0.16) | 0.786 (+0.094, p=0.08) |
| hybrid | 0.845 | 0.828 (-0.022, p=0.46) | 0.819 (-0.030, p=0.09) | 0.819 (-0.031, p=0.21) | 0.845 (-0.006, p=0.75) | 0.842 (-0.009, p=0.76) |

| Configuration (BM25) | Arg. F1 | Scope F1 | Grounding status | Variant | Binding acc. | Fallback | nDCG@10 |
|---|---|---|---|---|---|---|---|
| rule / index | 0.81 | 0.95 | 1.00 | 0.95 | 0.81 | 0.00 | 0.826 |
| LLM v3.0 / LLM v3.0 | 0.76 | 0.91 | 0.38 | 0.32 | 0.24 | 0.68 | 0.820 |
| LLM v3.1 / LLM v3.1 | 0.77 | 0.98 | 0.71 | 0.68 | 0.59 | 0.32 | 0.807 |
| LLM v3.1 / LLM v3.1, one repair | 0.77 | 0.98 | 0.71 | 0.68 | 0.59 | 0.32 | 0.807 |
| LLM v3.1 / index | 0.77 | 0.98 | 0.71 | 0.63 | 0.64 | 0.32 | 0.802 |
| gold / LLM v3.0 | 1.00 | 1.00 | 0.90 | 0.89 | 0.89 | 0.11 | 0.850 |
| gold / LLM v3.1 | 1.00 | 1.00 | 0.90 | 0.89 | 0.89 | 0.11 | 0.850 |
| gold / index | 1.00 | 1.00 | 1.00 | 0.95 | 1.00 | 0.00 | 0.847 |

**Finding.** The LLM Grounder is reliable (with the gold extraction it grounds 89–94% correctly and ranks as well as
the index Grounder). The LLM Interpreter with a 14B open model is the bottleneck: argument F1 0.77–0.79, and 32–41%
of intention-bearing requests fall back to context-only ranking (rule baseline: 0–19%). Next: the same runs with a
stronger model (32B/70B open model or an API model); only the three environment variables change.

## Established benchmark: TARGET (RQ1 generality)

TARGET (Ji et al., 2025) standardises table retrieval over established datasets. `target_import.py` converts a
TARGET dataset into a corpus and a benchmark with its gold tables (label 2, binary relevance) and, for BIRD and
Spider, the analytical operation of each question from its gold SQL (mean, total/count, extreme, lookup; grouped).
Recommended order: **BIRD validation** (real databases with documented columns, many aggregate questions),
**InfiAgent-DABench** (data-analysis questions over CSV files), **Spider test** (1,000+ tables). Report R@1/R@5/R@10
and nDCG@10 for context-only matchers (BM25, SBERT) and the framework on top of each (automatic and LLM
configurations), overall and by operation. Because TARGET's relevance is "table needed to answer", not
intention-conditional usefulness, this experiment shows that intention grounding generalises to an external
benchmark without hurting retrieval; the intention-specific claims (RQ2) rest on IGBench.

```sh
pip install datasets
python -m intention_grounding.target_import --dataset bird-validation
python -m intention_grounding.experiments --corpus data/corpus/target-bird-validation/manifest.json \
  --benchmark benchmarks/target/bird-validation.json --systems target --context bm25,sbert --tag bird
```


### Results on the server (rule Interpreter + index Grounder; binary gold-table relevance)

Spider is imported with case-insensitive gold-table matching (TARGET's gold names differ in case from the corpus;
without it only 775 of 2,147 questions kept a gold table). Tables are capped at 2,000 rows.

| Dataset | System | R@1 | R@5 | R@10 | nDCG@10 | MRR | Δ nDCG@10 vs matcher (p) |
|---|---|---|---|---|---|---|---|
| BIRD dev (75 tables, 1,533 q.) | BM25 | 0.426 | 0.773 | 0.875 | 0.762 | 0.810 | |
| | IG automatic · BM25 | 0.443 | 0.814 | 0.893 | 0.791 | 0.836 | +0.029 (p < 0.001; 437 wins / 95 losses) |
| | SBERT MiniLM | 0.486 | 0.877 | 0.963 | 0.863 | 0.893 | |
| | IG automatic · SBERT | 0.487 | 0.878 | 0.960 | 0.862 | 0.894 | −0.001 (p = 0.84) |
| Spider test (180 tables, 2,147 q.) | BM25 | 0.564 | 0.902 | 0.952 | 0.840 | 0.841 | |
| | IG automatic · BM25 | 0.635 | 0.919 | 0.955 | 0.882 | 0.895 | +0.042 (p < 0.001) |
| | SBERT MiniLM | 0.603 | 0.923 | 0.963 | 0.870 | 0.871 | |
| | IG automatic · SBERT | 0.607 | 0.925 | 0.968 | 0.875 | 0.874 | +0.005 (p = 0.016) |

LLM configuration (Qwen2.5-14B, prompts v3.1, one repair):

| Dataset | System | R@1 | R@5 | R@10 | nDCG@10 | MRR | Δ nDCG@10 vs matcher (p) |
|---|---|---|---|---|---|---|---|
| BIRD | IG LLM · BM25 | 0.451 | 0.800 | 0.880 | 0.787 | 0.841 | +0.025 (p < 0.001; 400 / 123) |
| BIRD | IG LLM · SBERT | 0.483 | 0.875 | 0.960 | 0.857 | 0.888 | −0.006 (p = 0.008) |
| Spider | IG LLM · BM25 | 0.593 | 0.910 | 0.953 | 0.858 | 0.864 | +0.018 (p < 0.001; 343 / 75) |
| Spider | IG LLM · SBERT | 0.600 | 0.922 | 0.963 | 0.869 | 0.868 | −0.001 (p = 0.57) |

With the LLM, BIRD questions end as: Interpreter failure 32%, extracted but outside the Library (unsupported) 30%,
grounding contract failure 23%, grounded 8%, insufficient 4%, no intention 3% (`breakdown.json` in each run). Most
TARGET questions are look-ups and counts that the Intention Library does not cover, so TARGET mainly tests that
intention grounding does not hurt topical retrieval: it helps BM25 on both datasets (rule and LLM), is neutral for
SBERT with the rule pipeline, and costs SBERT 0.006 on BIRD with the LLM pipeline.

**Where the gain comes from.** The rule Interpreter recognises an intention in few TARGET questions (text-to-SQL
questions such as "How many …", "What is the highest …"): only 75 of 1,533 BIRD and 85 of 2,147 Spider questions are
grounded. Most of the BM25 gain comes from the context query q_u (operation words removed), which also helps
questions without an intention (BIRD +0.018, Spider +0.048 nDCG@10 on no-intention questions). On grounded questions
alignment adds +0.02 to +0.04 for both BM25 and SBERT. The LLM configuration (running) grounds many more questions;
report the same decomposition for it.

**Running-time bug found and fixed.** One BIRD question took 23 minutes in the Aligner: the Profiler memoised derived
series inside `DataFrame.attrs`, which pandas deep-copies on every operation, recursively through the cached series, so
the cost exploded on wide tables (74-column `cards`). The cache now lives outside `attrs`; rankings are identical
(IGBench test re-run: 0.8569 / 0.8256). After the fix, the rule pipeline on BIRD takes 21 s for all 1,533 questions in one process (before: 23 min with 32
workers); slowest question 1.0 s. IGBench test, one process, cold profile cache (per request, median / p95): context
matching BM25 8 / 11 ms, SBERT 122 / 152 ms (query embedding 11 ms + vector search 104 ms in ChromaDB); Interpreter
(rule) 0.4 ms; Grounder (index) 0.5 ms; Profiler 31–37 / 44–68 ms for 50 candidates; Aligner 210–330 / 1,000–1,150 ms;
ranking 0.15 ms. LLM components (14B on one A100, 16 requests in flight): Interpreter ≈ 4 s, Grounder ≈ 2–3 s per
request. Scaling (314 tables): profiling 1.33 s per million cells + 63 ms; alignment median below 1 ms per table.

## Reproduce

```sh
python -m intention_grounding.experiments --systems main --benchmark benchmarks/igbench_v1/test_queries.json --tag test_main
python -m intention_grounding.experiments --systems ablations --benchmark benchmarks/igbench_v1/test_queries.json --tag test_ablations
python -m intention_grounding.experiments --systems main --tag dev_main
python -m intention_grounding.scaling --sample 300 --seed 7
```
