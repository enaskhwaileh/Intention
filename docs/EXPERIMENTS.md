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
   (`--context sbert`; e5/instructor via `--context sbert` with another `sbert_model`; TABERTA and semantic matching
   from the authors' prior work as additional `ContextMatcher` methods). The framework is applied on top of each.
4. **Review the labels** with two annotators and report agreement; re-run without code changes.
5. **External generality:** FollowTable once released (map aggregation-level / column-semantics instructions to
   variants), reporting nDCG and its responsiveness score.

## Reproduce

```sh
python -m intention_grounding.experiments --systems main --benchmark benchmarks/igbench_v1/test_queries.json --tag test_main
python -m intention_grounding.experiments --systems ablations --benchmark benchmarks/igbench_v1/test_queries.json --tag test_ablations
python -m intention_grounding.experiments --systems main --tag dev_main
python -m intention_grounding.scaling --sample 300 --seed 7
```
