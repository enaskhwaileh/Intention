# IGBench results (20261025T105002Z_plan_igb-dev_e5i)

Benchmark `igbench-v1` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:sbert | 0.798 | 0.491 | 0.334 | 0.890 | 0.781 | 0.629 | 0.314 |
| ig:rule/index:sbert | 0.790 | 0.531 | 0.363 | 0.921 | 0.876 | 0.800 | 0.143 |
| ig:rule/index:sbert+rnorm=minmax | 0.837 | 0.549 | 0.351 | 0.915 | 0.886 | 0.800 | 0.143 |
| ig:rule/index:sbert+align=0 | 0.812 | 0.509 | 0.337 | 0.894 | 0.838 | 0.743 | 0.171 |
| ig:gold/gold:sbert | 0.776 | 0.531 | 0.340 | 0.880 | 0.905 | 0.857 | 0.086 |
| ig:gold/gold:sbert+rnorm=minmax | 0.844 | 0.543 | 0.354 | 0.894 | 0.902 | 0.857 | 0.114 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:sbert | 0.801 | 0.475 | 0.781 | 0.625 |
| ig:rule/index:sbert | 0.793 | 0.519 | 0.885 | 0.812 |
| ig:rule/index:sbert+rnorm=minmax | 0.843 | 0.537 | 0.896 | 0.812 |
| ig:rule/index:sbert+align=0 | 0.816 | 0.494 | 0.844 | 0.750 |
| ig:gold/gold:sbert | 0.777 | 0.519 | 0.917 | 0.875 |
| ig:gold/gold:sbert+rnorm=minmax | 0.851 | 0.531 | 0.913 | 0.875 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:sbert | 0.293 | 0.738 | 0.890 |
| ig:rule/index:sbert | 0.324 | 0.784 | 0.921 |
| ig:rule/index:sbert+rnorm=minmax | 0.323 | 0.794 | 0.915 |
| ig:rule/index:sbert+align=0 | 0.311 | 0.760 | 0.894 |
| ig:gold/gold:sbert | 0.356 | 0.770 | 0.880 |
| ig:gold/gold:sbert+rnorm=minmax | 0.331 | 0.762 | 0.894 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | aggregate (n=3) | compare (n=10) | explain (n=7) | monitor (n=5) | predict (n=8) |
|---|---|---|---|---|---|
| ctx:sbert | 1.000 | 0.806 | 0.825 | 0.764 | 0.744 |
| ig:rule/index:sbert | 0.904 | 0.854 | 0.830 | 0.740 | 0.700 |
| ig:rule/index:sbert+rnorm=minmax | 1.000 | 0.886 | 0.875 | 0.751 | 0.779 |
| ig:rule/index:sbert+align=0 | 1.000 | 0.838 | 0.845 | 0.748 | 0.758 |
| ig:gold/gold:sbert | 0.865 | 0.854 | 0.806 | 0.748 | 0.665 |
| ig:gold/gold:sbert+rnorm=minmax | 1.000 | 0.870 | 0.884 | 0.798 | 0.793 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:sbert | 0.835 |
| ig:rule/index:sbert | 0.876 |
| ig:rule/index:sbert+rnorm=minmax | 0.853 |
| ig:rule/index:sbert+align=0 | 0.836 |
| ig:gold/gold:sbert | 0.881 |
| ig:gold/gold:sbert+rnorm=minmax | 0.834 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:rule/index:sbert | 1.000 | 0.825 | 0.970 | 0.833 | 0.812 | 0.812 | 0.688 | 0.188 | 0.548 | 0.773 |
| ig:rule/index:sbert+rnorm=minmax | 1.000 | 0.825 | 0.970 | 0.833 | 0.812 | 0.812 | 0.688 | 0.188 | 0.548 | 0.773 |
| ig:rule/index:sbert+align=0 | 1.000 | 0.825 | 0.970 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | – | – |
| ig:gold/gold:sbert | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.554 | 0.780 |
| ig:gold/gold:sbert+rnorm=minmax | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.554 | 0.780 |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:sbert | – | 121.7 / 106.7 / 112.7 | – | – | – | – | 121.7 / 106.7 / 112.8 | 4.383 |
| ig:rule/index:sbert | 0.7 / 0.4 / 1.2 | 104.4 / 105.1 / 109.9 | 1.8 / 0.6 / 7.4 | 74.6 / 25.1 / 375.3 | 824.0 / 259.3 / 3756.9 | 0.1 / 0.1 / 0.2 | 902.3 / 318.4 / 4325.3 | 17.136 |
| ig:rule/index:sbert+rnorm=minmax | 0.4 / 0.4 / 0.5 | 108.6 / 107.6 / 117.0 | 1.9 / 0.6 / 7.3 | 86.9 / 24.0 / 436.7 | 858.3 / 287.5 / 4073.5 | 0.1 / 0.1 / 0.2 | 948.7 / 359.9 / 4394.5 | 17.652 |
| ig:rule/index:sbert+align=0 | 0.4 / 0.4 / 0.5 | 108.3 / 108.4 / 114.8 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.4 / 0.3 / 0.7 | 0.8 / 0.8 / 1.3 | 4.428 |
| ig:gold/gold:sbert | 0.1 / 0.1 / 0.2 | 107.1 / 107.4 / 112.2 | 0.6 / 0.2 / 1.6 | 118.3 / 30.5 / 785.7 | 1044.9 / 407.2 / 4075.1 | 0.1 / 0.1 / 0.2 | 1165.4 / 477.6 / 4403.4 | 24.03 |
| ig:gold/gold:sbert+rnorm=minmax | 0.1 / 0.1 / 0.2 | 105.9 / 105.7 / 112.5 | 0.6 / 0.2 / 1.6 | 168.8 / 29.1 / 867.2 | 1024.6 / 406.9 / 4104.4 | 0.1 / 0.1 / 0.2 | 1195.6 / 454.7 / 4328.1 | 24.227 |

Context index build (one-off, ms): sbert: 17201 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:rule/index:sbert+rnorm=minmax | ctx:sbert | ndcg@10 | +0.038 | [+0.013, +0.065] | 0.006 | 16/7 |
| ig:rule/index:sbert+rnorm=minmax | ctx:sbert | mrr | +0.105 | [+0.043, +0.176] | 0.004 | 9/0 |
| ig:rule/index:sbert+rnorm=minmax | ctx:sbert | useful@1 | +0.171 | [+0.057, +0.314] | 0.030 | 6/0 |
| ig:rule/index:sbert | ctx:sbert | ndcg@10 | -0.007 | [-0.049, +0.035] | 0.752 | 13/13 |
| ig:rule/index:sbert | ctx:sbert | mrr | +0.095 | [+0.029, +0.176] | 0.022 | 7/1 |
| ig:rule/index:sbert | ctx:sbert | useful@1 | +0.171 | [+0.057, +0.314] | 0.032 | 6/0 |
| ig:rule/index:sbert+align=0 | ctx:sbert | ndcg@10 | +0.014 | [-0.004, +0.031] | 0.162 | 14/7 |
| ig:rule/index:sbert+align=0 | ctx:sbert | mrr | +0.057 | [+0.007, +0.119] | 0.068 | 6/2 |
| ig:rule/index:sbert+align=0 | ctx:sbert | useful@1 | +0.114 | [+0.029, +0.229] | 0.123 | 4/0 |
| ig:gold/gold:sbert+rnorm=minmax | ctx:sbert | ndcg@10 | +0.045 | [+0.018, +0.072] | 0.002 | 20/5 |
| ig:gold/gold:sbert+rnorm=minmax | ctx:sbert | mrr | +0.121 | [+0.048, +0.205] | 0.005 | 9/1 |
| ig:gold/gold:sbert+rnorm=minmax | ctx:sbert | useful@1 | +0.229 | [+0.086, +0.371] | 0.007 | 8/0 |
| ig:gold/gold:sbert | ctx:sbert | ndcg@10 | -0.021 | [-0.077, +0.032] | 0.480 | 12/18 |
| ig:gold/gold:sbert | ctx:sbert | mrr | +0.124 | [+0.048, +0.214] | 0.006 | 9/1 |
| ig:gold/gold:sbert | ctx:sbert | useful@1 | +0.229 | [+0.114, +0.371] | 0.008 | 8/0 |
