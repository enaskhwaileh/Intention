# IGBench results (20261025T105915Z_plan_igb-test_bge)

Benchmark `igbench-v1-test` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:sbert | 0.808 | 0.510 | 0.305 | 0.879 | 0.975 | 0.950 | 0.000 |
| ig:rule/index:sbert | 0.751 | 0.490 | 0.335 | 0.887 | 0.892 | 0.850 | 0.050 |
| ig:rule/index:sbert+rnorm=minmax | 0.823 | 0.540 | 0.330 | 0.912 | 0.950 | 0.900 | 0.050 |
| ig:rule/index:sbert+align=0 | 0.811 | 0.530 | 0.310 | 0.883 | 0.967 | 0.950 | 0.000 |
| ig:gold/gold:sbert | 0.781 | 0.540 | 0.340 | 0.937 | 0.929 | 0.900 | 0.000 |
| ig:gold/gold:sbert+rnorm=minmax | 0.843 | 0.550 | 0.335 | 0.918 | 0.975 | 0.950 | 0.000 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:sbert | 0.804 | 0.495 | 0.974 | 0.947 |
| ig:rule/index:sbert | 0.744 | 0.474 | 0.886 | 0.842 |
| ig:rule/index:sbert+rnorm=minmax | 0.819 | 0.526 | 0.947 | 0.895 |
| ig:rule/index:sbert+align=0 | 0.807 | 0.516 | 0.965 | 0.947 |
| ig:gold/gold:sbert | 0.775 | 0.526 | 0.925 | 0.895 |
| ig:gold/gold:sbert+rnorm=minmax | 0.840 | 0.537 | 0.974 | 0.947 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:sbert | 0.437 | 0.797 | 0.879 |
| ig:rule/index:sbert | 0.295 | 0.735 | 0.887 |
| ig:rule/index:sbert+rnorm=minmax | 0.387 | 0.821 | 0.912 |
| ig:rule/index:sbert+align=0 | 0.437 | 0.800 | 0.883 |
| ig:gold/gold:sbert | 0.345 | 0.824 | 0.937 |
| ig:gold/gold:sbert+rnorm=minmax | 0.437 | 0.831 | 0.918 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | compare (n=8) | explain (n=3) | monitor (n=5) | predict (n=4) |
|---|---|---|---|---|
| ctx:sbert | 0.794 | 0.763 | 0.799 | 0.867 |
| ig:rule/index:sbert | 0.783 | 0.812 | 0.591 | 0.813 |
| ig:rule/index:sbert+rnorm=minmax | 0.803 | 0.803 | 0.817 | 0.856 |
| ig:rule/index:sbert+align=0 | 0.774 | 0.756 | 0.803 | 0.912 |
| ig:gold/gold:sbert | 0.778 | 0.830 | 0.674 | 0.856 |
| ig:gold/gold:sbert+rnorm=minmax | 0.803 | 0.804 | 0.843 | 0.923 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:sbert | 0.871 |
| ig:rule/index:sbert | 0.913 |
| ig:rule/index:sbert+rnorm=minmax | 0.885 |
| ig:rule/index:sbert+align=0 | 0.872 |
| ig:gold/gold:sbert | 0.903 |
| ig:gold/gold:sbert+rnorm=minmax | 0.885 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:rule/index:sbert | 1.000 | 0.815 | 0.950 | 1.000 | 1.000 | 0.947 | 0.807 | 0.000 | 0.568 | 0.648 |
| ig:rule/index:sbert+rnorm=minmax | 1.000 | 0.815 | 0.950 | 1.000 | 1.000 | 0.947 | 0.807 | 0.000 | 0.568 | 0.648 |
| ig:rule/index:sbert+align=0 | 1.000 | 0.815 | 0.950 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | – | – |
| ig:gold/gold:sbert | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.614 | 0.761 |
| ig:gold/gold:sbert+rnorm=minmax | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.614 | 0.761 |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:sbert | – | 113.4 / 92.7 / 101.2 | – | – | – | – | 113.4 / 92.7 / 101.3 | 2.382 |
| ig:rule/index:sbert | 1.0 / 0.3 / 2.1 | 90.1 / 90.7 / 95.2 | 2.0 / 0.3 / 7.1 | 22.5 / 22.6 / 35.1 | 313.9 / 144.0 / 1060.1 | 0.1 / 0.1 / 0.1 | 340.6 / 190.5 / 1106.7 | 5.08 |
| ig:rule/index:sbert+rnorm=minmax | 0.4 / 0.4 / 0.4 | 90.1 / 91.8 / 96.8 | 2.1 / 0.3 / 7.1 | 35.0 / 21.1 / 33.3 | 358.4 / 143.7 / 1179.1 | 0.1 / 0.1 / 0.1 | 397.0 / 178.9 / 1203.1 | 5.366 |
| ig:rule/index:sbert+align=0 | 0.3 / 0.3 / 0.4 | 91.2 / 92.4 / 96.3 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.4 / 0.4 / 0.6 | 0.7 / 0.7 / 1.2 | 2.275 |
| ig:gold/gold:sbert | 0.1 / 0.1 / 0.2 | 93.9 / 92.4 / 102.2 | 0.7 / 0.2 / 2.4 | 95.3 / 21.8 / 340.4 | 309.5 / 176.8 / 841.9 | 0.1 / 0.1 / 0.1 | 406.7 / 232.6 / 1149.2 | 5.248 |
| ig:gold/gold:sbert+rnorm=minmax | 0.1 / 0.1 / 0.2 | 94.9 / 94.2 / 99.0 | 0.7 / 0.2 / 2.1 | 23.0 / 23.6 / 33.7 | 295.1 / 131.9 / 837.2 | 0.1 / 0.1 / 0.1 | 320.1 / 175.3 / 860.0 | 4.911 |

Context index build (one-off, ms): sbert: 12567 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:rule/index:sbert+rnorm=minmax | ctx:sbert | ndcg@10 | +0.011 | [-0.021, +0.042] | 0.503 | 10/7 |
| ig:rule/index:sbert+rnorm=minmax | ctx:sbert | mrr | -0.025 | [-0.075, +0.000] | 1.000 | 0/1 |
| ig:rule/index:sbert+rnorm=minmax | ctx:sbert | useful@1 | -0.050 | [-0.150, +0.000] | 1.000 | 0/1 |
| ig:rule/index:sbert | ctx:sbert | ndcg@10 | -0.057 | [-0.157, +0.022] | 0.306 | 9/10 |
| ig:rule/index:sbert | ctx:sbert | mrr | -0.083 | [-0.219, +0.037] | 0.375 | 1/3 |
| ig:rule/index:sbert | ctx:sbert | useful@1 | -0.100 | [-0.300, +0.100] | 0.631 | 1/3 |
| ig:rule/index:sbert+align=0 | ctx:sbert | ndcg@10 | +0.001 | [-0.022, +0.022] | 0.947 | 9/6 |
| ig:rule/index:sbert+align=0 | ctx:sbert | mrr | -0.008 | [-0.025, +0.000] | 1.000 | 0/1 |
| ig:rule/index:sbert+align=0 | ctx:sbert | useful@1 | +0.000 | [+0.000, +0.000] | 1.000 | 0/0 |
| ig:gold/gold:sbert+rnorm=minmax | ctx:sbert | ndcg@10 | +0.030 | [+0.002, +0.060] | 0.062 | 11/5 |
| ig:gold/gold:sbert+rnorm=minmax | ctx:sbert | mrr | +0.000 | [+0.000, +0.000] | 1.000 | 0/0 |
| ig:gold/gold:sbert+rnorm=minmax | ctx:sbert | useful@1 | +0.000 | [+0.000, +0.000] | 1.000 | 0/0 |
| ig:gold/gold:sbert | ctx:sbert | ndcg@10 | -0.028 | [-0.096, +0.029] | 0.439 | 10/9 |
| ig:gold/gold:sbert | ctx:sbert | mrr | -0.046 | [-0.154, +0.050] | 0.499 | 1/2 |
| ig:gold/gold:sbert | ctx:sbert | useful@1 | -0.050 | [-0.200, +0.100] | 1.000 | 1/2 |
