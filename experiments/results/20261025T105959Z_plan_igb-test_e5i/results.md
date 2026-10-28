# IGBench results (20261025T105959Z_plan_igb-test_e5i)

Benchmark `igbench-v1-test` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:sbert | 0.813 | 0.490 | 0.320 | 0.905 | 0.931 | 0.900 | 0.050 |
| ig:rule/index:sbert | 0.729 | 0.500 | 0.330 | 0.883 | 0.869 | 0.850 | 0.050 |
| ig:rule/index:sbert+rnorm=minmax | 0.819 | 0.550 | 0.335 | 0.927 | 0.950 | 0.900 | 0.050 |
| ig:rule/index:sbert+align=0 | 0.816 | 0.510 | 0.320 | 0.909 | 0.960 | 0.950 | 0.000 |
| ig:gold/gold:sbert | 0.774 | 0.550 | 0.340 | 0.935 | 0.917 | 0.900 | 0.000 |
| ig:gold/gold:sbert+rnorm=minmax | 0.836 | 0.570 | 0.340 | 0.933 | 0.975 | 0.950 | 0.000 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:sbert | 0.807 | 0.474 | 0.928 | 0.895 |
| ig:rule/index:sbert | 0.719 | 0.484 | 0.862 | 0.842 |
| ig:rule/index:sbert+rnorm=minmax | 0.813 | 0.537 | 0.947 | 0.895 |
| ig:rule/index:sbert+align=0 | 0.810 | 0.495 | 0.958 | 0.947 |
| ig:gold/gold:sbert | 0.767 | 0.537 | 0.913 | 0.895 |
| ig:gold/gold:sbert+rnorm=minmax | 0.832 | 0.558 | 0.974 | 0.947 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:sbert | 0.412 | 0.784 | 0.905 |
| ig:rule/index:sbert | 0.295 | 0.708 | 0.883 |
| ig:rule/index:sbert+rnorm=minmax | 0.345 | 0.835 | 0.927 |
| ig:rule/index:sbert+align=0 | 0.437 | 0.805 | 0.909 |
| ig:gold/gold:sbert | 0.345 | 0.799 | 0.935 |
| ig:gold/gold:sbert+rnorm=minmax | 0.395 | 0.854 | 0.933 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | compare (n=8) | explain (n=3) | monitor (n=5) | predict (n=4) |
|---|---|---|---|---|
| ctx:sbert | 0.811 | 0.890 | 0.794 | 0.780 |
| ig:rule/index:sbert | 0.787 | 0.859 | 0.657 | 0.606 |
| ig:rule/index:sbert+rnorm=minmax | 0.826 | 0.883 | 0.799 | 0.782 |
| ig:rule/index:sbert+align=0 | 0.798 | 0.893 | 0.797 | 0.818 |
| ig:gold/gold:sbert | 0.791 | 0.841 | 0.650 | 0.847 |
| ig:gold/gold:sbert+rnorm=minmax | 0.818 | 0.868 | 0.816 | 0.876 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:sbert | 0.860 |
| ig:rule/index:sbert | 0.872 |
| ig:rule/index:sbert+rnorm=minmax | 0.865 |
| ig:rule/index:sbert+align=0 | 0.859 |
| ig:gold/gold:sbert | 0.899 |
| ig:gold/gold:sbert+rnorm=minmax | 0.875 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:rule/index:sbert | 1.000 | 0.815 | 0.950 | 1.000 | 1.000 | 0.947 | 0.807 | 0.000 | 0.554 | 0.639 |
| ig:rule/index:sbert+rnorm=minmax | 1.000 | 0.815 | 0.950 | 1.000 | 1.000 | 0.947 | 0.807 | 0.000 | 0.554 | 0.639 |
| ig:rule/index:sbert+align=0 | 1.000 | 0.815 | 0.950 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | – | – |
| ig:gold/gold:sbert | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.600 | 0.740 |
| ig:gold/gold:sbert+rnorm=minmax | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.600 | 0.740 |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:sbert | – | 128.8 / 102.7 / 109.5 | – | – | – | – | 128.9 / 102.7 / 109.5 | 2.706 |
| ig:rule/index:sbert | 0.9 / 0.3 / 1.5 | 102.8 / 103.9 / 107.4 | 2.0 / 0.3 / 6.0 | 83.7 / 24.0 / 53.7 | 366.4 / 177.2 / 1156.4 | 0.1 / 0.1 / 0.1 | 454.2 / 272.4 / 1363.6 | 5.886 |
| ig:rule/index:sbert+rnorm=minmax | 0.4 / 0.4 / 0.4 | 107.6 / 107.6 / 110.3 | 1.6 / 0.3 / 5.5 | 81.3 / 22.8 / 34.4 | 385.8 / 174.6 / 1243.5 | 0.1 / 0.1 / 0.1 | 470.3 / 209.8 / 1279.2 | 6.012 |
| ig:rule/index:sbert+align=0 | 0.4 / 0.4 / 0.4 | 105.4 / 104.1 / 111.4 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.4 / 0.4 / 0.6 | 0.8 / 0.7 / 1.1 | 2.691 |
| ig:gold/gold:sbert | 0.1 / 0.1 / 0.2 | 106.8 / 106.6 / 111.7 | 0.7 / 0.2 / 2.2 | 142.2 / 24.7 / 358.8 | 399.4 / 304.9 / 1114.1 | 0.1 / 0.1 / 0.1 | 543.6 / 407.5 / 1231.9 | 5.881 |
| ig:gold/gold:sbert+rnorm=minmax | 0.1 / 0.1 / 0.1 | 110.4 / 110.8 / 112.6 | 0.7 / 0.2 / 1.4 | 94.9 / 26.1 / 41.4 | 369.7 / 177.8 / 1055.3 | 0.1 / 0.1 / 0.1 | 466.7 / 208.6 / 1183.2 | 5.675 |

Context index build (one-off, ms): sbert: 15968 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:rule/index:sbert+rnorm=minmax | ctx:sbert | ndcg@10 | +0.006 | [-0.046, +0.060] | 0.817 | 8/9 |
| ig:rule/index:sbert+rnorm=minmax | ctx:sbert | mrr | +0.019 | [-0.100, +0.138] | 1.000 | 2/2 |
| ig:rule/index:sbert+rnorm=minmax | ctx:sbert | useful@1 | +0.000 | [-0.200, +0.200] | 1.000 | 2/2 |
| ig:rule/index:sbert | ctx:sbert | ndcg@10 | -0.079 | [-0.187, +0.015] | 0.170 | 8/10 |
| ig:rule/index:sbert | ctx:sbert | mrr | -0.062 | [-0.238, +0.113] | 0.505 | 2/3 |
| ig:rule/index:sbert | ctx:sbert | useful@1 | -0.050 | [-0.250, +0.150] | 1.000 | 2/3 |
| ig:rule/index:sbert+align=0 | ctx:sbert | ndcg@10 | +0.003 | [-0.014, +0.023] | 0.784 | 7/7 |
| ig:rule/index:sbert+align=0 | ctx:sbert | mrr | +0.029 | [+0.000, +0.083] | 0.504 | 2/0 |
| ig:rule/index:sbert+align=0 | ctx:sbert | useful@1 | +0.050 | [+0.000, +0.150] | 1.000 | 1/0 |
| ig:gold/gold:sbert+rnorm=minmax | ctx:sbert | ndcg@10 | +0.023 | [-0.025, +0.075] | 0.389 | 10/5 |
| ig:gold/gold:sbert+rnorm=minmax | ctx:sbert | mrr | +0.044 | [-0.050, +0.156] | 0.748 | 2/1 |
| ig:gold/gold:sbert+rnorm=minmax | ctx:sbert | useful@1 | +0.050 | [-0.100, +0.200] | 1.000 | 2/1 |
| ig:gold/gold:sbert | ctx:sbert | ndcg@10 | -0.036 | [-0.121, +0.043] | 0.427 | 8/10 |
| ig:gold/gold:sbert | ctx:sbert | mrr | -0.014 | [-0.166, +0.136] | 1.000 | 2/2 |
| ig:gold/gold:sbert | ctx:sbert | useful@1 | +0.000 | [-0.200, +0.200] | 1.000 | 2/2 |
