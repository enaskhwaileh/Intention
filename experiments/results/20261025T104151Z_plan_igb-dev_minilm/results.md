# IGBench results (20261025T104151Z_plan_igb-dev_minilm)

Benchmark `igbench-v1` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:sbert | 0.769 | 0.474 | 0.297 | 0.840 | 0.838 | 0.743 | 0.143 |
| ig:rule/index:sbert | 0.784 | 0.531 | 0.323 | 0.871 | 0.868 | 0.829 | 0.143 |
| ig:rule/index:sbert+rnorm=minmax | 0.789 | 0.520 | 0.311 | 0.855 | 0.860 | 0.800 | 0.143 |
| ig:rule/index:sbert+align=0 | 0.765 | 0.480 | 0.294 | 0.838 | 0.830 | 0.771 | 0.143 |
| ig:gold/gold:sbert | 0.815 | 0.526 | 0.326 | 0.875 | 0.927 | 0.886 | 0.086 |
| ig:gold/gold:sbert+rnorm=minmax | 0.812 | 0.520 | 0.311 | 0.832 | 0.905 | 0.857 | 0.114 |
| rerank:ce:sbert | 0.808 | 0.537 | 0.314 | 0.869 | 0.917 | 0.857 | 0.114 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:sbert | 0.768 | 0.450 | 0.823 | 0.719 |
| ig:rule/index:sbert | 0.784 | 0.512 | 0.856 | 0.812 |
| ig:rule/index:sbert+rnorm=minmax | 0.790 | 0.500 | 0.847 | 0.781 |
| ig:rule/index:sbert+align=0 | 0.763 | 0.456 | 0.814 | 0.750 |
| ig:gold/gold:sbert | 0.818 | 0.506 | 0.921 | 0.875 |
| ig:gold/gold:sbert+rnorm=minmax | 0.815 | 0.500 | 0.897 | 0.844 |
| rerank:ce:sbert | 0.817 | 0.525 | 0.932 | 0.875 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:sbert | 0.286 | 0.728 | 0.840 |
| ig:rule/index:sbert | 0.329 | 0.758 | 0.871 |
| ig:rule/index:sbert+rnorm=minmax | 0.301 | 0.757 | 0.855 |
| ig:rule/index:sbert+align=0 | 0.296 | 0.717 | 0.838 |
| ig:gold/gold:sbert | 0.362 | 0.776 | 0.875 |
| ig:gold/gold:sbert+rnorm=minmax | 0.334 | 0.754 | 0.832 |
| rerank:ce:sbert | 0.331 | 0.794 | 0.869 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | aggregate (n=3) | compare (n=10) | explain (n=7) | monitor (n=5) | predict (n=8) |
|---|---|---|---|---|---|
| ctx:sbert | 0.966 | 0.762 | 0.808 | 0.673 | 0.730 |
| ig:rule/index:sbert | 0.983 | 0.817 | 0.844 | 0.678 | 0.686 |
| ig:rule/index:sbert+rnorm=minmax | 0.984 | 0.796 | 0.842 | 0.669 | 0.743 |
| ig:rule/index:sbert+align=0 | 0.984 | 0.762 | 0.808 | 0.651 | 0.720 |
| ig:gold/gold:sbert | 0.983 | 0.874 | 0.878 | 0.720 | 0.696 |
| ig:gold/gold:sbert+rnorm=minmax | 0.984 | 0.826 | 0.865 | 0.714 | 0.759 |
| rerank:ce:sbert | 0.945 | 0.800 | 0.840 | 0.727 | 0.827 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:sbert | 0.772 |
| ig:rule/index:sbert | 0.799 |
| ig:rule/index:sbert+rnorm=minmax | 0.777 |
| ig:rule/index:sbert+align=0 | 0.755 |
| ig:gold/gold:sbert | 0.823 |
| ig:gold/gold:sbert+rnorm=minmax | 0.753 |
| rerank:ce:sbert | 0.815 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:rule/index:sbert | 1.000 | 0.825 | 0.970 | 0.833 | 0.812 | 0.812 | 0.688 | 0.188 | 0.479 | 0.753 |
| ig:rule/index:sbert+rnorm=minmax | 1.000 | 0.825 | 0.970 | 0.833 | 0.812 | 0.812 | 0.688 | 0.188 | 0.479 | 0.753 |
| ig:rule/index:sbert+align=0 | 1.000 | 0.825 | 0.970 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | – | – |
| ig:gold/gold:sbert | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.535 | 0.771 |
| ig:gold/gold:sbert+rnorm=minmax | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.535 | 0.771 |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:sbert | – | 95.4 / 85.8 / 91.2 | – | – | – | – | 95.5 / 85.9 / 91.3 | 3.437 |
| ig:rule/index:sbert | 0.7 / 0.4 / 1.8 | 85.2 / 85.4 / 90.3 | 1.9 / 0.6 / 7.1 | 34.0 / 22.5 / 42.0 | 850.8 / 183.3 / 4001.3 | 0.1 / 0.1 / 0.2 | 889.3 / 285.2 / 4026.6 | 15.654 |
| ig:rule/index:sbert+rnorm=minmax | 0.4 / 0.4 / 0.5 | 79.9 / 75.4 / 99.4 | 1.9 / 0.6 / 6.6 | 37.3 / 21.2 / 44.4 | 860.9 / 269.5 / 3972.8 | 0.1 / 0.1 / 0.2 | 901.6 / 291.6 / 4072.0 | 15.679 |
| ig:rule/index:sbert+align=0 | 0.4 / 0.4 / 0.5 | 75.2 / 75.7 / 80.5 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.4 / 0.4 / 0.7 | 0.9 / 0.8 / 1.3 | 3.139 |
| ig:gold/gold:sbert | 0.1 / 0.1 / 0.2 | 75.0 / 75.5 / 78.5 | 0.7 / 0.2 / 1.7 | 24.0 / 22.5 / 42.0 | 864.0 / 287.9 / 4097.0 | 0.1 / 0.1 / 0.2 | 890.1 / 312.4 / 4133.6 | 19.584 |
| ig:gold/gold:sbert+rnorm=minmax | 0.1 / 0.1 / 0.2 | 78.0 / 78.2 / 82.9 | 0.6 / 0.3 / 1.7 | 50.9 / 24.1 / 310.9 | 870.7 / 280.8 / 4149.2 | 0.1 / 0.1 / 0.2 | 923.7 / 384.9 / 4181.0 | 20.609 |
| rerank:ce:sbert | – | 1894.2 / 1192.4 / 5790.8 | – | – | – | – | 9958.8 / 10267.2 / 12598.0 | 23.879 |

Context index build (one-off, ms): sbert: 12533 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:rule/index:sbert+rnorm=minmax | ctx:sbert | ndcg@10 | +0.020 | [-0.008, +0.050] | 0.208 | 17/13 |
| ig:rule/index:sbert+rnorm=minmax | ctx:sbert | mrr | +0.021 | [-0.043, +0.099] | 0.620 | 3/6 |
| ig:rule/index:sbert+rnorm=minmax | ctx:sbert | useful@1 | +0.057 | [-0.057, +0.171] | 0.626 | 3/1 |
| ig:rule/index:sbert | ctx:sbert | ndcg@10 | +0.015 | [-0.027, +0.058] | 0.535 | 17/12 |
| ig:rule/index:sbert | ctx:sbert | mrr | +0.030 | [-0.052, +0.117] | 0.495 | 5/5 |
| ig:rule/index:sbert | ctx:sbert | useful@1 | +0.086 | [-0.029, +0.229] | 0.369 | 4/1 |
| ig:rule/index:sbert+align=0 | ctx:sbert | ndcg@10 | -0.004 | [-0.025, +0.018] | 0.747 | 16/13 |
| ig:rule/index:sbert+align=0 | ctx:sbert | mrr | -0.008 | [-0.041, +0.031] | 0.730 | 2/6 |
| ig:rule/index:sbert+align=0 | ctx:sbert | useful@1 | +0.029 | [+0.000, +0.086] | 1.000 | 1/0 |
| ig:gold/gold:sbert+rnorm=minmax | ctx:sbert | ndcg@10 | +0.043 | [+0.015, +0.072] | 0.004 | 24/6 |
| ig:gold/gold:sbert+rnorm=minmax | ctx:sbert | mrr | +0.067 | [-0.019, +0.160] | 0.163 | 6/3 |
| ig:gold/gold:sbert+rnorm=minmax | ctx:sbert | useful@1 | +0.114 | [-0.029, +0.257] | 0.211 | 5/1 |
| ig:gold/gold:sbert | ctx:sbert | ndcg@10 | +0.045 | [-0.007, +0.095] | 0.112 | 23/7 |
| ig:gold/gold:sbert | ctx:sbert | mrr | +0.089 | [-0.015, +0.200] | 0.101 | 7/2 |
| ig:gold/gold:sbert | ctx:sbert | useful@1 | +0.143 | [+0.000, +0.286] | 0.117 | 6/1 |
