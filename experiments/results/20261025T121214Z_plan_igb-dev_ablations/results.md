# IGBench results (20261025T121214Z_plan_igb-dev_ablations)

Benchmark `igbench-v1` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:bm25 | 0.768 | 0.486 | 0.323 | 0.851 | 0.895 | 0.800 | 0.143 |
| ig:gold/gold:bm25 | 0.796 | 0.537 | 0.334 | 0.882 | 0.879 | 0.771 | 0.143 |
| ig:gold/gold:bm25+comb=linear | 0.762 | 0.531 | 0.314 | 0.844 | 0.902 | 0.829 | 0.114 |
| ig:gold/gold:bm25+comb=lexicographic | 0.687 | 0.509 | 0.300 | 0.809 | 0.801 | 0.686 | 0.143 |
| ig:gold/gold:bm25+soft=0 | 0.800 | 0.537 | 0.337 | 0.884 | 0.893 | 0.800 | 0.143 |
| ig:gold/gold:bm25+alpha=0.25 | 0.802 | 0.526 | 0.337 | 0.887 | 0.886 | 0.771 | 0.143 |
| ig:gold/gold:bm25+alpha=0.75 | 0.762 | 0.520 | 0.317 | 0.854 | 0.887 | 0.800 | 0.143 |
| ig:gold/gold:bm25+alpha=1.0 | 0.735 | 0.526 | 0.309 | 0.824 | 0.901 | 0.829 | 0.114 |
| ig:gold/gold:bm25+k=20 | 0.794 | 0.537 | 0.334 | 0.882 | 0.879 | 0.771 | 0.143 |
| ig:gold/gold:bm25+k=100 | 0.796 | 0.537 | 0.334 | 0.882 | 0.879 | 0.771 | 0.143 |
| ig:gold/gold:bm25+bind=0.7 | 0.796 | 0.543 | 0.343 | 0.882 | 0.879 | 0.771 | 0.143 |
| ig:gold/index:bm25 | 0.796 | 0.537 | 0.334 | 0.882 | 0.879 | 0.771 | 0.143 |
| ig:rule/gold:bm25 | 0.781 | 0.503 | 0.329 | 0.865 | 0.898 | 0.829 | 0.114 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:bm25 | 0.779 | 0.469 | 0.917 | 0.844 |
| ig:gold/gold:bm25 | 0.809 | 0.525 | 0.898 | 0.812 |
| ig:gold/gold:bm25+comb=linear | 0.772 | 0.519 | 0.924 | 0.875 |
| ig:gold/gold:bm25+comb=lexicographic | 0.690 | 0.494 | 0.813 | 0.719 |
| ig:gold/gold:bm25+soft=0 | 0.814 | 0.525 | 0.914 | 0.844 |
| ig:gold/gold:bm25+alpha=0.25 | 0.816 | 0.512 | 0.906 | 0.812 |
| ig:gold/gold:bm25+alpha=0.75 | 0.772 | 0.506 | 0.908 | 0.844 |
| ig:gold/gold:bm25+alpha=1.0 | 0.742 | 0.512 | 0.923 | 0.875 |
| ig:gold/gold:bm25+k=20 | 0.807 | 0.525 | 0.898 | 0.812 |
| ig:gold/gold:bm25+k=100 | 0.809 | 0.525 | 0.898 | 0.812 |
| ig:gold/gold:bm25+bind=0.7 | 0.809 | 0.531 | 0.898 | 0.812 |
| ig:gold/index:bm25 | 0.809 | 0.525 | 0.898 | 0.812 |
| ig:rule/gold:bm25 | 0.792 | 0.487 | 0.920 | 0.875 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:bm25 | 0.306 | 0.711 | 0.851 |
| ig:gold/gold:bm25 | 0.311 | 0.781 | 0.882 |
| ig:gold/gold:bm25+comb=linear | 0.349 | 0.781 | 0.844 |
| ig:gold/gold:bm25+comb=lexicographic | 0.316 | 0.748 | 0.809 |
| ig:gold/gold:bm25+soft=0 | 0.316 | 0.781 | 0.884 |
| ig:gold/gold:bm25+alpha=0.25 | 0.311 | 0.756 | 0.887 |
| ig:gold/gold:bm25+alpha=0.75 | 0.340 | 0.757 | 0.854 |
| ig:gold/gold:bm25+alpha=1.0 | 0.349 | 0.767 | 0.824 |
| ig:gold/gold:bm25+k=20 | 0.311 | 0.781 | 0.882 |
| ig:gold/gold:bm25+k=100 | 0.311 | 0.781 | 0.882 |
| ig:gold/gold:bm25+bind=0.7 | 0.311 | 0.781 | 0.882 |
| ig:gold/index:bm25 | 0.311 | 0.781 | 0.882 |
| ig:rule/gold:bm25 | 0.321 | 0.716 | 0.865 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | aggregate (n=3) | compare (n=10) | explain (n=7) | monitor (n=5) | predict (n=8) |
|---|---|---|---|---|---|
| ctx:bm25 | 0.939 | 0.804 | 0.775 | 0.668 | 0.773 |
| ig:gold/gold:bm25 | 0.964 | 0.855 | 0.827 | 0.728 | 0.741 |
| ig:gold/gold:bm25+comb=linear | 0.919 | 0.848 | 0.810 | 0.708 | 0.644 |
| ig:gold/gold:bm25+comb=lexicographic | 0.783 | 0.756 | 0.735 | 0.701 | 0.549 |
| ig:gold/gold:bm25+soft=0 | 0.964 | 0.859 | 0.827 | 0.728 | 0.753 |
| ig:gold/gold:bm25+alpha=0.25 | 0.964 | 0.856 | 0.831 | 0.727 | 0.762 |
| ig:gold/gold:bm25+alpha=0.75 | 0.943 | 0.829 | 0.826 | 0.712 | 0.642 |
| ig:gold/gold:bm25+alpha=1.0 | 0.810 | 0.795 | 0.805 | 0.701 | 0.639 |
| ig:gold/gold:bm25+k=20 | 0.964 | 0.855 | 0.827 | 0.724 | 0.733 |
| ig:gold/gold:bm25+k=100 | 0.964 | 0.855 | 0.827 | 0.728 | 0.741 |
| ig:gold/gold:bm25+bind=0.7 | 0.979 | 0.833 | 0.831 | 0.734 | 0.755 |
| ig:gold/index:bm25 | 0.964 | 0.855 | 0.827 | 0.728 | 0.741 |
| ig:rule/gold:bm25 | 0.979 | 0.808 | 0.802 | 0.672 | 0.780 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:bm25 | 0.803 |
| ig:gold/gold:bm25 | 0.860 |
| ig:gold/gold:bm25+comb=linear | 0.829 |
| ig:gold/gold:bm25+comb=lexicographic | 0.839 |
| ig:gold/gold:bm25+soft=0 | 0.861 |
| ig:gold/gold:bm25+alpha=0.25 | 0.851 |
| ig:gold/gold:bm25+alpha=0.75 | 0.859 |
| ig:gold/gold:bm25+alpha=1.0 | 0.859 |
| ig:gold/gold:bm25+k=20 | 0.863 |
| ig:gold/gold:bm25+k=100 | 0.873 |
| ig:gold/gold:bm25+bind=0.7 | 0.862 |
| ig:gold/index:bm25 | 0.860 |
| ig:rule/gold:bm25 | 0.800 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:gold/gold:bm25 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.497 | 0.789 |
| ig:gold/gold:bm25+comb=linear | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.497 | 0.789 |
| ig:gold/gold:bm25+comb=lexicographic | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.497 | 0.789 |
| ig:gold/gold:bm25+soft=0 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.497 | 0.789 |
| ig:gold/gold:bm25+alpha=0.25 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.497 | 0.789 |
| ig:gold/gold:bm25+alpha=0.75 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.497 | 0.789 |
| ig:gold/gold:bm25+alpha=1.0 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.497 | 0.789 |
| ig:gold/gold:bm25+k=20 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.603 | 0.784 |
| ig:gold/gold:bm25+k=100 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.453 | 0.797 |
| ig:gold/gold:bm25+bind=0.7 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.623 | 0.740 |
| ig:gold/index:bm25 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.497 | 0.789 |
| ig:rule/gold:bm25 | 1.000 | 0.825 | 0.970 | 0.417 | 0.344 | 0.344 | 0.328 | 0.656 | 0.423 | 0.815 |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:bm25 | – | 5.0 / 4.8 / 7.1 | – | – | – | – | 5.1 / 4.9 / 7.2 | 0.183 |
| ig:gold/gold:bm25 | 0.1 / 0.1 / 0.2 | 3.4 / 3.0 / 5.7 | 0.6 / 0.2 / 1.3 | 27.7 / 26.0 / 53.7 | 1096.5 / 379.6 / 4454.9 | 0.1 / 0.1 / 0.2 | 1126.1 / 403.1 / 4492.7 | 17.119 |
| ig:gold/gold:bm25+comb=linear | 0.1 / 0.1 / 0.2 | 4.6 / 3.0 / 6.4 | 0.6 / 0.2 / 1.5 | 25.6 / 21.1 / 38.5 | 1091.4 / 438.5 / 4390.7 | 0.1 / 0.1 / 0.2 | 1119.0 / 463.9 / 4424.0 | 17.261 |
| ig:gold/gold:bm25+comb=lexicographic | 0.1 / 0.1 / 0.2 | 3.7 / 3.1 / 6.1 | 0.6 / 0.2 / 1.5 | 42.9 / 20.6 / 111.9 | 1076.4 / 393.3 / 4265.7 | 0.1 / 0.1 / 0.2 | 1121.3 / 419.5 / 4377.0 | 16.781 |
| ig:gold/gold:bm25+soft=0 | 0.1 / 0.1 / 0.2 | 5.0 / 3.2 / 7.6 | 0.6 / 0.2 / 1.5 | 23.3 / 21.4 / 33.9 | 1095.7 / 447.4 / 4328.4 | 0.1 / 0.1 / 0.2 | 1121.0 / 469.5 / 4360.5 | 17.495 |
| ig:gold/gold:bm25+alpha=0.25 | 0.1 / 0.1 / 0.3 | 3.6 / 3.1 / 5.8 | 0.7 / 0.3 / 2.1 | 43.6 / 19.6 / 128.2 | 1091.7 / 373.3 / 4443.5 | 0.1 / 0.1 / 0.2 | 1137.4 / 398.5 / 4574.5 | 17.144 |
| ig:gold/gold:bm25+alpha=0.75 | 0.1 / 0.1 / 0.2 | 5.0 / 3.1 / 6.8 | 0.6 / 0.2 / 1.4 | 24.4 / 21.2 / 33.8 | 1088.7 / 411.5 / 4319.7 | 0.1 / 0.1 / 0.1 | 1115.0 / 436.9 / 4351.1 | 17.474 |
| ig:gold/gold:bm25+alpha=1.0 | 0.1 / 0.1 / 0.2 | 3.8 / 3.2 / 6.3 | 0.6 / 0.2 / 1.6 | 46.7 / 20.0 / 175.5 | 1118.4 / 398.0 / 4310.1 | 0.1 / 0.1 / 0.1 | 1167.2 / 425.2 / 4518.8 | 17.236 |
| ig:gold/gold:bm25+k=20 | 0.1 / 0.1 / 0.2 | 4.7 / 3.1 / 6.2 | 0.6 / 0.3 / 1.5 | 9.4 / 7.4 / 20.4 | 620.8 / 71.9 / 2498.5 | 0.1 / 0.0 / 0.1 | 631.5 / 80.2 / 2523.6 | 6.505 |
| ig:gold/gold:bm25+k=100 | 0.1 / 0.1 / 0.2 | 3.5 / 3.1 / 5.4 | 0.6 / 0.3 / 1.6 | 53.1 / 45.5 / 98.1 | 1454.2 / 686.2 / 4636.2 | 0.3 / 0.2 / 0.3 | 1510.4 / 749.1 / 4695.9 | 19.276 |
| ig:gold/gold:bm25+bind=0.7 | 0.2 / 0.1 / 0.2 | 3.7 / 3.1 / 5.9 | 0.6 / 0.3 / 1.5 | 29.7 / 21.1 / 105.8 | 1079.5 / 328.4 / 4514.4 | 0.1 / 0.1 / 0.2 | 1111.2 / 355.5 / 4536.6 | 17.167 |
| ig:gold/index:bm25 | 0.1 / 0.1 / 0.2 | 4.6 / 3.1 / 7.6 | 1.9 / 0.6 / 6.8 | 23.7 / 21.1 / 37.7 | 1088.3 / 420.1 / 4386.7 | 0.1 / 0.1 / 0.1 | 1115.3 / 438.9 / 4418.3 | 17.065 |
| ig:rule/gold:bm25 | 0.7 / 0.4 / 1.3 | 3.8 / 3.7 / 5.7 | 0.5 / 0.2 / 1.4 | 23.0 / 0.0 / 103.4 | 323.0 / 0.0 / 1024.7 | 0.3 / 0.1 / 1.0 | 347.9 / 1.4 / 1131.6 | 6.204 |

Context index build (one-off, ms): bm25: 59 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:gold/gold:bm25+alpha=1.0 | ctx:bm25 | ndcg@10 | -0.033 | [-0.094, +0.018] | 0.286 | 12/18 |
| ig:gold/gold:bm25+alpha=1.0 | ctx:bm25 | mrr | +0.005 | [-0.084, +0.086] | 0.935 | 3/2 |
| ig:gold/gold:bm25+alpha=1.0 | ctx:bm25 | useful@1 | +0.029 | [-0.114, +0.143] | 1.000 | 3/2 |
| ig:gold/gold:bm25+comb=linear | ctx:bm25 | ndcg@10 | -0.006 | [-0.060, +0.037] | 0.891 | 14/13 |
| ig:gold/gold:bm25+comb=linear | ctx:bm25 | mrr | +0.007 | [-0.080, +0.086] | 0.935 | 3/2 |
| ig:gold/gold:bm25+comb=linear | ctx:bm25 | useful@1 | +0.029 | [-0.114, +0.143] | 1.000 | 3/2 |
| ig:gold/gold:bm25+k=100 | ctx:bm25 | ndcg@10 | +0.027 | [+0.003, +0.053] | 0.047 | 21/8 |
| ig:gold/gold:bm25+k=100 | ctx:bm25 | mrr | -0.017 | [-0.081, +0.038] | 0.750 | 2/2 |
| ig:gold/gold:bm25+k=100 | ctx:bm25 | useful@1 | -0.029 | [-0.143, +0.057] | 1.000 | 1/2 |
| ig:gold/index:bm25 | ctx:bm25 | ndcg@10 | +0.027 | [+0.003, +0.053] | 0.047 | 21/8 |
| ig:gold/index:bm25 | ctx:bm25 | mrr | -0.017 | [-0.081, +0.038] | 0.750 | 2/2 |
| ig:gold/index:bm25 | ctx:bm25 | useful@1 | -0.029 | [-0.143, +0.057] | 1.000 | 1/2 |
| ig:gold/gold:bm25+k=20 | ctx:bm25 | ndcg@10 | +0.025 | [+0.001, +0.051] | 0.065 | 21/8 |
| ig:gold/gold:bm25+k=20 | ctx:bm25 | mrr | -0.017 | [-0.081, +0.038] | 0.750 | 2/2 |
| ig:gold/gold:bm25+k=20 | ctx:bm25 | useful@1 | -0.029 | [-0.143, +0.057] | 1.000 | 1/2 |
| ig:gold/gold:bm25+comb=lexicographic | ctx:bm25 | ndcg@10 | -0.079 | [-0.145, -0.020] | 0.011 | 9/23 |
| ig:gold/gold:bm25+comb=lexicographic | ctx:bm25 | mrr | -0.095 | [-0.213, +0.014] | 0.130 | 3/9 |
| ig:gold/gold:bm25+comb=lexicographic | ctx:bm25 | useful@1 | -0.114 | [-0.286, +0.057] | 0.348 | 3/7 |
| ig:gold/gold:bm25+alpha=0.75 | ctx:bm25 | ndcg@10 | -0.006 | [-0.059, +0.035] | 0.897 | 16/13 |
| ig:gold/gold:bm25+alpha=0.75 | ctx:bm25 | mrr | -0.008 | [-0.090, +0.057] | 1.000 | 3/2 |
| ig:gold/gold:bm25+alpha=0.75 | ctx:bm25 | useful@1 | +0.000 | [-0.114, +0.114] | 1.000 | 2/2 |
| ig:gold/gold:bm25+soft=0 | ctx:bm25 | ndcg@10 | +0.031 | [+0.007, +0.057] | 0.023 | 23/7 |
| ig:gold/gold:bm25+soft=0 | ctx:bm25 | mrr | -0.002 | [-0.059, +0.043] | 1.000 | 2/1 |
| ig:gold/gold:bm25+soft=0 | ctx:bm25 | useful@1 | +0.000 | [-0.086, +0.086] | 1.000 | 1/1 |
| ig:gold/gold:bm25+alpha=0.25 | ctx:bm25 | ndcg@10 | +0.033 | [+0.014, +0.053] | 0.002 | 22/7 |
| ig:gold/gold:bm25+alpha=0.25 | ctx:bm25 | mrr | -0.009 | [-0.067, +0.043] | 1.000 | 2/2 |
| ig:gold/gold:bm25+alpha=0.25 | ctx:bm25 | useful@1 | -0.029 | [-0.143, +0.057] | 1.000 | 1/2 |
| ig:gold/gold:bm25 | ctx:bm25 | ndcg@10 | +0.027 | [+0.003, +0.053] | 0.047 | 21/8 |
| ig:gold/gold:bm25 | ctx:bm25 | mrr | -0.017 | [-0.081, +0.038] | 0.750 | 2/2 |
| ig:gold/gold:bm25 | ctx:bm25 | useful@1 | -0.029 | [-0.143, +0.057] | 1.000 | 1/2 |
| ig:gold/gold:bm25+bind=0.7 | ctx:bm25 | ndcg@10 | +0.027 | [+0.004, +0.051] | 0.035 | 22/8 |
| ig:gold/gold:bm25+bind=0.7 | ctx:bm25 | mrr | -0.017 | [-0.081, +0.038] | 0.750 | 2/2 |
| ig:gold/gold:bm25+bind=0.7 | ctx:bm25 | useful@1 | -0.029 | [-0.143, +0.057] | 1.000 | 1/2 |
| ig:rule/gold:bm25 | ctx:bm25 | ndcg@10 | +0.012 | [-0.003, +0.028] | 0.135 | 14/7 |
| ig:rule/gold:bm25 | ctx:bm25 | mrr | +0.003 | [-0.033, +0.043] | 1.000 | 1/1 |
| ig:rule/gold:bm25 | ctx:bm25 | useful@1 | +0.029 | [+0.000, +0.086] | 1.000 | 1/0 |
