# IGBench results (20261025T105636Z_plan_igb-test_bm25)

Benchmark `igbench-v1-test` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:bm25 | 0.828 | 0.530 | 0.345 | 0.935 | 0.917 | 0.850 | 0.100 |
| ig:rule/index:bm25 | 0.826 | 0.540 | 0.355 | 0.948 | 0.900 | 0.800 | 0.050 |
| ig:rule/index:bm25+rnorm=minmax | 0.825 | 0.540 | 0.350 | 0.940 | 0.900 | 0.800 | 0.050 |
| ig:rule/index:bm25+align=0 | 0.824 | 0.540 | 0.335 | 0.919 | 0.892 | 0.800 | 0.100 |
| ig:gold/gold:bm25 | 0.857 | 0.550 | 0.355 | 0.948 | 0.975 | 0.950 | 0.000 |
| ig:gold/gold:bm25+rnorm=minmax | 0.861 | 0.550 | 0.350 | 0.940 | 0.975 | 0.950 | 0.000 |
| rerank:ce:bm25 | 0.859 | 0.550 | 0.345 | 0.938 | 1.000 | 1.000 | 0.000 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:bm25 | 0.823 | 0.516 | 0.912 | 0.842 |
| ig:rule/index:bm25 | 0.821 | 0.526 | 0.895 | 0.789 |
| ig:rule/index:bm25+rnorm=minmax | 0.820 | 0.526 | 0.895 | 0.789 |
| ig:rule/index:bm25+align=0 | 0.819 | 0.526 | 0.886 | 0.789 |
| ig:gold/gold:bm25 | 0.854 | 0.537 | 0.974 | 0.947 |
| ig:gold/gold:bm25+rnorm=minmax | 0.858 | 0.537 | 0.974 | 0.947 |
| rerank:ce:bm25 | 0.853 | 0.537 | 1.000 | 1.000 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:bm25 | 0.414 | 0.810 | 0.935 |
| ig:rule/index:bm25 | 0.327 | 0.817 | 0.948 |
| ig:rule/index:bm25+rnorm=minmax | 0.327 | 0.812 | 0.940 |
| ig:rule/index:bm25+align=0 | 0.389 | 0.817 | 0.919 |
| ig:gold/gold:bm25 | 0.395 | 0.829 | 0.948 |
| ig:gold/gold:bm25+rnorm=minmax | 0.395 | 0.824 | 0.940 |
| rerank:ce:bm25 | 0.445 | 0.827 | 0.938 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | compare (n=8) | explain (n=3) | monitor (n=5) | predict (n=4) |
|---|---|---|---|---|
| ctx:bm25 | 0.812 | 0.800 | 0.750 | 0.909 |
| ig:rule/index:bm25 | 0.798 | 0.788 | 0.807 | 0.861 |
| ig:rule/index:bm25+rnorm=minmax | 0.795 | 0.789 | 0.809 | 0.861 |
| ig:rule/index:bm25+align=0 | 0.832 | 0.747 | 0.742 | 0.899 |
| ig:gold/gold:bm25 | 0.805 | 0.833 | 0.849 | 0.918 |
| ig:gold/gold:bm25+rnorm=minmax | 0.801 | 0.825 | 0.876 | 0.918 |
| rerank:ce:bm25 | 0.881 | 0.802 | 0.804 | 0.902 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:bm25 | 0.871 |
| ig:rule/index:bm25 | 0.882 |
| ig:rule/index:bm25+rnorm=minmax | 0.882 |
| ig:rule/index:bm25+align=0 | 0.850 |
| ig:gold/gold:bm25 | 0.882 |
| ig:gold/gold:bm25+rnorm=minmax | 0.882 |
| rerank:ce:bm25 | 0.901 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:rule/index:bm25 | 1.000 | 0.815 | 0.950 | 1.000 | 1.000 | 0.947 | 0.807 | 0.000 | 0.549 | 0.634 |
| ig:rule/index:bm25+rnorm=minmax | 1.000 | 0.815 | 0.950 | 1.000 | 1.000 | 0.947 | 0.807 | 0.000 | 0.549 | 0.634 |
| ig:rule/index:bm25+align=0 | 1.000 | 0.815 | 0.950 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | – | – |
| ig:gold/gold:bm25 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.576 | 0.747 |
| ig:gold/gold:bm25+rnorm=minmax | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.576 | 0.747 |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:bm25 | – | 5.6 / 5.4 / 6.6 | – | – | – | – | 5.7 / 5.5 / 6.8 | 0.12 |
| ig:rule/index:bm25 | 1.0 / 0.4 / 2.0 | 3.7 / 3.7 / 5.4 | 2.0 / 0.4 / 6.4 | 25.5 / 22.8 / 30.1 | 369.3 / 222.3 / 839.7 | 0.1 / 0.1 / 0.1 | 398.9 / 247.7 / 876.3 | 3.113 |
| ig:rule/index:bm25+rnorm=minmax | 0.4 / 0.4 / 0.5 | 5.6 / 3.7 / 7.4 | 2.1 / 0.3 / 6.7 | 21.3 / 18.5 / 34.5 | 345.6 / 217.4 / 723.2 | 0.1 / 0.1 / 0.1 | 370.5 / 240.7 / 757.8 | 3.062 |
| ig:rule/index:bm25+align=0 | 0.4 / 0.4 / 0.4 | 5.2 / 3.6 / 7.2 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.7 / 0.6 / 1.2 | 1.1 / 0.9 / 1.9 | 0.173 |
| ig:gold/gold:bm25 | 0.1 / 0.1 / 0.1 | 3.9 / 3.4 / 6.3 | 0.8 / 0.2 / 3.0 | 27.6 / 23.8 / 57.3 | 337.1 / 236.2 / 639.5 | 0.1 / 0.1 / 0.1 | 366.6 / 255.2 / 668.3 | 2.517 |
| ig:gold/gold:bm25+rnorm=minmax | 0.1 / 0.1 / 0.1 | 4.0 / 3.1 / 6.1 | 0.8 / 0.2 / 3.1 | 25.3 / 22.1 / 39.7 | 343.8 / 238.8 / 684.9 | 0.1 / 0.1 / 0.1 | 371.1 / 257.0 / 718.4 | 2.574 |
| rerank:ce:bm25 | – | 45.9 / 25.2 / 102.1 | – | – | – | – | 4873.9 / 5728.4 / 6063.5 | 7.769 |

Context index build (one-off, ms): bm25: 54 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:gold/gold:bm25+rnorm=minmax | ctx:bm25 | ndcg@10 | +0.031 | [-0.013, +0.074] | 0.197 | 12/4 |
| ig:gold/gold:bm25+rnorm=minmax | ctx:bm25 | mrr | +0.058 | [-0.042, +0.175] | 0.498 | 3/1 |
| ig:gold/gold:bm25+rnorm=minmax | ctx:bm25 | useful@1 | +0.100 | [-0.100, +0.300] | 0.625 | 3/1 |
| ig:rule/index:bm25+align=0 | ctx:bm25 | ndcg@10 | -0.004 | [-0.026, +0.014] | 0.716 | 6/5 |
| ig:rule/index:bm25+align=0 | ctx:bm25 | mrr | -0.025 | [-0.125, +0.050] | 1.000 | 1/2 |
| ig:rule/index:bm25+align=0 | ctx:bm25 | useful@1 | -0.050 | [-0.250, +0.100] | 1.000 | 1/2 |
| ig:rule/index:bm25+rnorm=minmax | ctx:bm25 | ndcg@10 | -0.003 | [-0.045, +0.036] | 0.915 | 9/5 |
| ig:rule/index:bm25+rnorm=minmax | ctx:bm25 | mrr | -0.017 | [-0.142, +0.100] | 1.000 | 2/3 |
| ig:rule/index:bm25+rnorm=minmax | ctx:bm25 | useful@1 | -0.050 | [-0.300, +0.150] | 1.000 | 2/3 |
| ig:rule/index:bm25 | ctx:bm25 | ndcg@10 | -0.003 | [-0.045, +0.036] | 0.922 | 9/6 |
| ig:rule/index:bm25 | ctx:bm25 | mrr | -0.017 | [-0.142, +0.100] | 1.000 | 2/3 |
| ig:rule/index:bm25 | ctx:bm25 | useful@1 | -0.050 | [-0.300, +0.150] | 1.000 | 2/3 |
| ig:gold/gold:bm25 | ctx:bm25 | ndcg@10 | +0.027 | [-0.018, +0.067] | 0.247 | 11/5 |
| ig:gold/gold:bm25 | ctx:bm25 | mrr | +0.058 | [-0.042, +0.175] | 0.498 | 3/1 |
| ig:gold/gold:bm25 | ctx:bm25 | useful@1 | +0.100 | [-0.100, +0.300] | 0.625 | 3/1 |
