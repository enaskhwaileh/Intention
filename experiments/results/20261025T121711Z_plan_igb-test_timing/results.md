# IGBench results (20261025T121711Z_plan_igb-test_timing)

Benchmark `igbench-v1-test` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:bm25 | 0.828 | 0.530 | 0.345 | 0.935 | 0.917 | 0.850 | 0.100 |
| ig:gold/gold:bm25 | 0.857 | 0.550 | 0.355 | 0.948 | 0.975 | 0.950 | 0.000 |
| ig:rule/index:bm25 | 0.826 | 0.540 | 0.355 | 0.948 | 0.900 | 0.800 | 0.050 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:bm25 | 0.823 | 0.516 | 0.912 | 0.842 |
| ig:gold/gold:bm25 | 0.854 | 0.537 | 0.974 | 0.947 |
| ig:rule/index:bm25 | 0.821 | 0.526 | 0.895 | 0.789 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:bm25 | 0.414 | 0.810 | 0.935 |
| ig:gold/gold:bm25 | 0.395 | 0.829 | 0.948 |
| ig:rule/index:bm25 | 0.327 | 0.817 | 0.948 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | compare (n=8) | explain (n=3) | monitor (n=5) | predict (n=4) |
|---|---|---|---|---|
| ctx:bm25 | 0.812 | 0.800 | 0.750 | 0.909 |
| ig:gold/gold:bm25 | 0.805 | 0.833 | 0.849 | 0.918 |
| ig:rule/index:bm25 | 0.798 | 0.788 | 0.807 | 0.861 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:bm25 | 0.871 |
| ig:gold/gold:bm25 | 0.882 |
| ig:rule/index:bm25 | 0.882 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:gold/gold:bm25 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.576 | 0.747 |
| ig:rule/index:bm25 | 1.000 | 0.815 | 0.950 | 1.000 | 1.000 | 0.947 | 0.807 | 0.000 | 0.549 | 0.634 |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:bm25 | – | 5.4 / 5.5 / 6.7 | – | – | – | – | 5.5 / 5.6 / 6.8 | 0.117 |
| ig:gold/gold:bm25 | 0.1 / 0.1 / 0.1 | 5.7 / 4.2 / 6.4 | 0.1 / 0.1 / 0.2 | 38.6 / 39.4 / 49.9 | 226.0 / 152.7 / 529.5 | 0.1 / 0.1 / 0.1 | 271.7 / 196.7 / 558.2 | 5.717 |
| ig:rule/index:bm25 | 0.5 / 0.1 / 0.6 | 6.6 / 4.5 / 9.0 | 0.3 / 0.2 / 0.4 | 37.0 / 39.0 / 49.9 | 198.9 / 158.4 / 315.7 | 0.1 / 0.1 / 0.1 | 244.9 / 215.0 / 342.5 | 5.153 |

Context index build (one-off, ms): bm25: 52 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:rule/index:bm25 | ctx:bm25 | ndcg@10 | -0.003 | [-0.045, +0.036] | 0.922 | 9/6 |
| ig:rule/index:bm25 | ctx:bm25 | mrr | -0.017 | [-0.142, +0.100] | 1.000 | 2/3 |
| ig:rule/index:bm25 | ctx:bm25 | useful@1 | -0.050 | [-0.300, +0.150] | 1.000 | 2/3 |
| ig:gold/gold:bm25 | ctx:bm25 | ndcg@10 | +0.027 | [-0.018, +0.067] | 0.247 | 11/5 |
| ig:gold/gold:bm25 | ctx:bm25 | mrr | +0.058 | [-0.042, +0.175] | 0.498 | 3/1 |
| ig:gold/gold:bm25 | ctx:bm25 | useful@1 | +0.100 | [-0.100, +0.300] | 0.625 | 3/1 |
