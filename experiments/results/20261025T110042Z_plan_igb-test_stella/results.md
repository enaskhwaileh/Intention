# IGBench results (20261025T110042Z_plan_igb-test_stella)

Benchmark `igbench-v1-test` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:sbert | 0.827 | 0.520 | 0.340 | 0.923 | 0.950 | 0.900 | 0.000 |
| ig:rule/index:sbert | 0.793 | 0.530 | 0.365 | 0.978 | 0.894 | 0.850 | 0.050 |
| ig:rule/index:sbert+rnorm=minmax | 0.825 | 0.570 | 0.340 | 0.923 | 0.950 | 0.900 | 0.050 |
| ig:rule/index:sbert+align=0 | 0.795 | 0.550 | 0.335 | 0.915 | 0.867 | 0.750 | 0.050 |
| ig:gold/gold:sbert | 0.800 | 0.550 | 0.360 | 0.968 | 0.913 | 0.900 | 0.000 |
| ig:gold/gold:sbert+rnorm=minmax | 0.832 | 0.580 | 0.355 | 0.952 | 0.942 | 0.900 | 0.000 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:sbert | 0.824 | 0.505 | 0.947 | 0.895 |
| ig:rule/index:sbert | 0.788 | 0.516 | 0.888 | 0.842 |
| ig:rule/index:sbert+rnorm=minmax | 0.822 | 0.558 | 0.947 | 0.895 |
| ig:rule/index:sbert+align=0 | 0.790 | 0.537 | 0.860 | 0.737 |
| ig:gold/gold:sbert | 0.795 | 0.537 | 0.909 | 0.895 |
| ig:gold/gold:sbert+rnorm=minmax | 0.829 | 0.568 | 0.939 | 0.895 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:sbert | 0.407 | 0.796 | 0.923 |
| ig:rule/index:sbert | 0.295 | 0.775 | 0.978 |
| ig:rule/index:sbert+rnorm=minmax | 0.345 | 0.839 | 0.923 |
| ig:rule/index:sbert+align=0 | 0.324 | 0.817 | 0.915 |
| ig:gold/gold:sbert | 0.345 | 0.747 | 0.968 |
| ig:gold/gold:sbert+rnorm=minmax | 0.345 | 0.852 | 0.952 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | compare (n=8) | explain (n=3) | monitor (n=5) | predict (n=4) |
|---|---|---|---|---|
| ctx:sbert | 0.854 | 0.776 | 0.765 | 0.899 |
| ig:rule/index:sbert | 0.793 | 0.871 | 0.726 | 0.810 |
| ig:rule/index:sbert+rnorm=minmax | 0.840 | 0.787 | 0.797 | 0.851 |
| ig:rule/index:sbert+align=0 | 0.777 | 0.796 | 0.733 | 0.902 |
| ig:gold/gold:sbert | 0.787 | 0.848 | 0.719 | 0.886 |
| ig:gold/gold:sbert+rnorm=minmax | 0.828 | 0.817 | 0.762 | 0.931 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:sbert | 0.850 |
| ig:rule/index:sbert | 0.862 |
| ig:rule/index:sbert+rnorm=minmax | 0.862 |
| ig:rule/index:sbert+align=0 | 0.842 |
| ig:gold/gold:sbert | 0.863 |
| ig:gold/gold:sbert+rnorm=minmax | 0.860 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:rule/index:sbert | 1.000 | 0.815 | 0.950 | 1.000 | 1.000 | 0.947 | 0.807 | 0.000 | 0.561 | 0.630 |
| ig:rule/index:sbert+rnorm=minmax | 1.000 | 0.815 | 0.950 | 1.000 | 1.000 | 0.947 | 0.807 | 0.000 | 0.561 | 0.630 |
| ig:rule/index:sbert+align=0 | 1.000 | 0.815 | 0.950 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | – | – |
| ig:gold/gold:sbert | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.593 | 0.750 |
| ig:gold/gold:sbert+rnorm=minmax | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.593 | 0.750 |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:sbert | – | 131.2 / 110.3 / 120.2 | – | – | – | – | 131.3 / 110.4 / 120.2 | 2.757 |
| ig:rule/index:sbert | 0.9 / 0.3 / 1.5 | 109.5 / 110.4 / 115.1 | 1.8 / 0.3 / 6.2 | 26.3 / 26.2 / 36.8 | 308.1 / 176.5 / 999.1 | 0.1 / 0.1 / 0.1 | 338.3 / 209.5 / 1037.1 | 5.548 |
| ig:rule/index:sbert+rnorm=minmax | 0.4 / 0.4 / 0.4 | 110.9 / 110.7 / 116.6 | 1.9 / 0.4 / 6.0 | 40.9 / 23.3 / 31.1 | 323.1 / 185.7 / 993.0 | 0.1 / 0.1 / 0.1 | 367.3 / 208.9 / 1030.2 | 5.755 |
| ig:rule/index:sbert+align=0 | 0.4 / 0.3 / 0.4 | 116.5 / 116.0 / 120.6 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.4 / 0.4 / 0.7 | 0.8 / 0.8 / 1.2 | 2.852 |
| ig:gold/gold:sbert | 0.1 / 0.1 / 0.1 | 115.6 / 115.5 / 121.7 | 0.6 / 0.2 / 1.8 | 47.9 / 21.6 / 31.0 | 334.5 / 189.8 / 991.6 | 0.1 / 0.1 / 0.1 | 384.1 / 243.1 / 1025.8 | 5.587 |
| ig:gold/gold:sbert+rnorm=minmax | 0.1 / 0.1 / 0.1 | 110.8 / 110.9 / 114.0 | 0.8 / 0.2 / 2.8 | 23.1 / 23.4 / 34.0 | 292.7 / 166.3 / 812.9 | 0.1 / 0.1 / 0.1 | 317.9 / 187.8 / 837.9 | 5.246 |

Context index build (one-off, ms): sbert: 11526 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:rule/index:sbert+rnorm=minmax | ctx:sbert | ndcg@10 | -0.005 | [-0.051, +0.032] | 0.818 | 10/8 |
| ig:rule/index:sbert+rnorm=minmax | ctx:sbert | mrr | +0.000 | [-0.100, +0.100] | 1.000 | 2/2 |
| ig:rule/index:sbert+rnorm=minmax | ctx:sbert | useful@1 | +0.000 | [-0.200, +0.200] | 1.000 | 2/2 |
| ig:rule/index:sbert | ctx:sbert | ndcg@10 | -0.036 | [-0.116, +0.043] | 0.428 | 9/9 |
| ig:rule/index:sbert | ctx:sbert | mrr | -0.056 | [-0.200, +0.075] | 0.558 | 2/3 |
| ig:rule/index:sbert | ctx:sbert | useful@1 | -0.050 | [-0.250, +0.150] | 1.000 | 2/3 |
| ig:rule/index:sbert+align=0 | ctx:sbert | ndcg@10 | -0.033 | [-0.075, +0.001] | 0.142 | 7/8 |
| ig:rule/index:sbert+align=0 | ctx:sbert | mrr | -0.083 | [-0.183, +0.000] | 0.253 | 0/3 |
| ig:rule/index:sbert+align=0 | ctx:sbert | useful@1 | -0.150 | [-0.300, +0.000] | 0.253 | 0/3 |
| ig:gold/gold:sbert+rnorm=minmax | ctx:sbert | ndcg@10 | +0.002 | [-0.057, +0.057] | 0.963 | 11/7 |
| ig:gold/gold:sbert+rnorm=minmax | ctx:sbert | mrr | -0.008 | [-0.117, +0.100] | 1.000 | 2/2 |
| ig:gold/gold:sbert+rnorm=minmax | ctx:sbert | useful@1 | +0.000 | [-0.200, +0.200] | 1.000 | 2/2 |
| ig:gold/gold:sbert | ctx:sbert | ndcg@10 | -0.029 | [-0.112, +0.051] | 0.539 | 10/8 |
| ig:gold/gold:sbert | ctx:sbert | mrr | -0.037 | [-0.190, +0.100] | 0.747 | 2/2 |
| ig:gold/gold:sbert | ctx:sbert | useful@1 | +0.000 | [-0.200, +0.200] | 1.000 | 2/2 |
