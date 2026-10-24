# IGBench results (20261024T192653Z_mac_dev)

Benchmark `igbench-v1` on corpus `igbench-v1` (3301 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.12.3 on macOS-15.7.9-x86_64-i386-64bit. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:bm25 | 0.768 | 0.486 | 0.323 | 0.851 | 0.895 | 0.800 | 0.143 |
| ctx:tfidf | 0.730 | 0.469 | 0.314 | 0.832 | 0.795 | 0.657 | 0.200 |
| ctx:sbert | 0.769 | 0.474 | 0.297 | 0.840 | 0.838 | 0.743 | 0.143 |
| ctx:hybrid | 0.813 | 0.543 | 0.334 | 0.884 | 0.876 | 0.771 | 0.143 |
| ig:gold/gold:bm25 | 0.796 | 0.537 | 0.334 | 0.882 | 0.879 | 0.771 | 0.143 |
| ig:rule/index:bm25 | 0.788 | 0.531 | 0.331 | 0.875 | 0.909 | 0.829 | 0.114 |
| ig:gold/gold:sbert | 0.815 | 0.526 | 0.326 | 0.875 | 0.927 | 0.886 | 0.086 |
| ig:rule/index:sbert | 0.784 | 0.531 | 0.323 | 0.871 | 0.868 | 0.829 | 0.143 |
| ig:gold/gold:hybrid | 0.821 | 0.531 | 0.340 | 0.891 | 0.900 | 0.829 | 0.114 |
| ig:rule/index:hybrid | 0.811 | 0.549 | 0.337 | 0.891 | 0.886 | 0.771 | 0.114 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:bm25 | 0.779 | 0.469 | 0.917 | 0.844 |
| ctx:tfidf | 0.739 | 0.463 | 0.807 | 0.688 |
| ctx:sbert | 0.768 | 0.450 | 0.823 | 0.719 |
| ctx:hybrid | 0.820 | 0.525 | 0.896 | 0.812 |
| ig:gold/gold:bm25 | 0.809 | 0.525 | 0.898 | 0.812 |
| ig:rule/index:bm25 | 0.801 | 0.519 | 0.932 | 0.875 |
| ig:gold/gold:sbert | 0.818 | 0.506 | 0.921 | 0.875 |
| ig:rule/index:sbert | 0.784 | 0.512 | 0.856 | 0.812 |
| ig:gold/gold:hybrid | 0.829 | 0.512 | 0.922 | 0.875 |
| ig:rule/index:hybrid | 0.818 | 0.531 | 0.906 | 0.812 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:bm25 | 0.306 | 0.711 | 0.851 |
| ctx:tfidf | 0.228 | 0.684 | 0.832 |
| ctx:sbert | 0.286 | 0.728 | 0.840 |
| ctx:hybrid | 0.312 | 0.789 | 0.884 |
| ig:gold/gold:bm25 | 0.311 | 0.781 | 0.882 |
| ig:rule/index:bm25 | 0.321 | 0.782 | 0.875 |
| ig:gold/gold:sbert | 0.362 | 0.776 | 0.875 |
| ig:rule/index:sbert | 0.329 | 0.758 | 0.871 |
| ig:gold/gold:hybrid | 0.349 | 0.778 | 0.891 |
| ig:rule/index:hybrid | 0.318 | 0.796 | 0.891 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | aggregate (n=3) | compare (n=10) | explain (n=7) | monitor (n=5) | predict (n=8) |
|---|---|---|---|---|---|
| ctx:bm25 | 0.939 | 0.804 | 0.775 | 0.668 | 0.773 |
| ctx:tfidf | 0.940 | 0.736 | 0.738 | 0.649 | 0.734 |
| ctx:sbert | 0.966 | 0.762 | 0.808 | 0.673 | 0.730 |
| ctx:hybrid | 0.984 | 0.853 | 0.831 | 0.706 | 0.789 |
| ig:gold/gold:bm25 | 0.964 | 0.855 | 0.827 | 0.728 | 0.741 |
| ig:rule/index:bm25 | 0.964 | 0.831 | 0.807 | 0.699 | 0.770 |
| ig:gold/gold:sbert | 0.983 | 0.874 | 0.878 | 0.720 | 0.696 |
| ig:rule/index:sbert | 0.983 | 0.817 | 0.844 | 0.678 | 0.686 |
| ig:gold/gold:hybrid | 0.983 | 0.883 | 0.852 | 0.768 | 0.730 |
| ig:rule/index:hybrid | 0.983 | 0.892 | 0.829 | 0.705 | 0.737 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:bm25 | 0.803 |
| ctx:tfidf | 0.799 |
| ctx:sbert | 0.772 |
| ctx:hybrid | 0.808 |
| ig:gold/gold:bm25 | 0.860 |
| ig:rule/index:bm25 | 0.843 |
| ig:gold/gold:sbert | 0.823 |
| ig:rule/index:sbert | 0.799 |
| ig:gold/gold:hybrid | 0.834 |
| ig:rule/index:hybrid | 0.841 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:gold/gold:bm25 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.497 | 0.789 |
| ig:rule/index:bm25 | 1.000 | 0.825 | 0.970 | 0.833 | 0.812 | 0.812 | 0.688 | 0.188 | 0.482 | 0.784 |
| ig:gold/gold:sbert | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.535 | 0.771 |
| ig:rule/index:sbert | 1.000 | 0.825 | 0.970 | 0.833 | 0.812 | 0.812 | 0.688 | 0.188 | 0.479 | 0.753 |
| ig:gold/gold:hybrid | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.507 | 0.795 |
| ig:rule/index:hybrid | 1.000 | 0.825 | 0.970 | 0.833 | 0.812 | 0.812 | 0.688 | 0.188 | 0.474 | 0.788 |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:bm25 | – | 7.7 / 7.4 / 11.6 | – | – | – | – | 7.8 / 7.6 / 11.8 | 0.283 |
| ctx:tfidf | – | 5.7 / 5.5 / 6.4 | – | – | – | – | 5.9 / 5.7 / 6.8 | 0.213 |
| ctx:sbert | – | 94.5 / 59.4 / 63.3 | – | – | – | – | 94.6 / 59.5 / 63.3 | 3.405 |
| ctx:hybrid | – | 70.3 / 69.6 / 77.9 | – | – | – | – | 70.5 / 69.8 / 78.3 | 2.538 |
| ig:gold/gold:bm25 | 0.1 / 0.1 / 0.1 | 6.8 / 6.0 / 9.7 | 0.2 / 0.2 / 0.2 | 1458.7 / 620.5 / 3713.5 | 1062.5 / 514.8 / 3690.1 | 0.1 / 0.1 / 0.1 | 2529.7 / 1587.4 / 6123.1 | 91.107 |
| ig:rule/index:bm25 | 0.3 / 0.2 / 0.9 | 7.0 / 6.6 / 10.7 | 0.3 / 0.3 / 0.6 | 154.3 / 15.6 / 565.5 | 924.6 / 175.3 / 3649.7 | 0.1 / 0.1 / 0.1 | 1088.1 / 434.4 / 4200.2 | 39.2 |
| ig:gold/gold:sbert | 0.1 / 0.1 / 0.1 | 62.9 / 62.5 / 66.6 | 0.2 / 0.2 / 0.3 | 560.3 / 251.7 / 1692.0 | 972.8 / 348.3 / 3888.9 | 0.1 / 0.1 / 0.1 | 1597.6 / 875.7 / 5004.6 | 57.57 |
| ig:rule/index:sbert | 0.2 / 0.2 / 0.3 | 63.7 / 62.1 / 68.5 | 0.3 / 0.3 / 0.4 | 62.8 / 16.8 / 202.3 | 872.4 / 286.4 / 3983.0 | 0.1 / 0.1 / 0.1 | 1000.6 / 421.9 / 4064.8 | 36.065 |
| ig:gold/gold:hybrid | 0.1 / 0.1 / 0.1 | 72.0 / 69.8 / 90.1 | 0.2 / 0.2 / 0.3 | 65.3 / 16.7 / 310.7 | 1126.9 / 403.7 / 4314.1 | 0.1 / 0.1 / 0.1 | 1266.1 / 549.0 / 4545.8 | 45.632 |
| ig:rule/index:hybrid | 0.2 / 0.2 / 0.3 | 70.8 / 69.8 / 87.1 | 0.3 / 0.3 / 0.4 | 15.2 / 14.1 / 34.4 | 986.0 / 257.5 / 4146.5 | 0.1 / 0.1 / 0.1 | 1073.9 / 341.0 / 4244.6 | 38.7 |

Context index build (one-off, ms): bm25: 52 (cached), hybrid: 9179 (cached), sbert: 1545 (cached), tfidf: 32 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:gold/gold:bm25 | ctx:bm25 | ndcg@10 | +0.027 | [+0.003, +0.053] | 0.047 | 21/8 |
| ig:gold/gold:bm25 | ctx:bm25 | mrr | -0.017 | [-0.081, +0.038] | 0.750 | 2/2 |
| ig:gold/gold:bm25 | ctx:bm25 | useful@1 | -0.029 | [-0.143, +0.057] | 1.000 | 1/2 |
| ig:gold/gold:hybrid | ctx:hybrid | ndcg@10 | +0.007 | [-0.024, +0.036] | 0.682 | 16/11 |
| ig:gold/gold:hybrid | ctx:hybrid | mrr | +0.024 | [-0.052, +0.100] | 0.626 | 3/2 |
| ig:gold/gold:hybrid | ctx:hybrid | useful@1 | +0.057 | [-0.057, +0.171] | 0.626 | 3/1 |
| ig:gold/gold:sbert | ctx:sbert | ndcg@10 | +0.045 | [-0.007, +0.095] | 0.112 | 23/7 |
| ig:gold/gold:sbert | ctx:sbert | mrr | +0.089 | [-0.015, +0.200] | 0.101 | 7/2 |
| ig:gold/gold:sbert | ctx:sbert | useful@1 | +0.143 | [+0.000, +0.286] | 0.117 | 6/1 |
| ig:rule/index:hybrid | ctx:hybrid | ndcg@10 | -0.002 | [-0.027, +0.023] | 0.900 | 13/12 |
| ig:rule/index:hybrid | ctx:hybrid | mrr | +0.009 | [-0.052, +0.081] | 0.751 | 2/2 |
| ig:rule/index:hybrid | ctx:hybrid | useful@1 | +0.000 | [-0.114, +0.114] | 1.000 | 2/2 |
| ig:rule/index:bm25 | ctx:bm25 | ndcg@10 | +0.019 | [-0.000, +0.041] | 0.069 | 16/8 |
| ig:rule/index:bm25 | ctx:bm25 | mrr | +0.014 | [-0.009, +0.052] | 0.751 | 2/1 |
| ig:rule/index:bm25 | ctx:bm25 | useful@1 | +0.029 | [+0.000, +0.086] | 1.000 | 1/0 |
| ig:rule/index:sbert | ctx:sbert | ndcg@10 | +0.015 | [-0.027, +0.058] | 0.535 | 17/12 |
| ig:rule/index:sbert | ctx:sbert | mrr | +0.030 | [-0.052, +0.117] | 0.495 | 5/5 |
| ig:rule/index:sbert | ctx:sbert | useful@1 | +0.086 | [-0.029, +0.229] | 0.369 | 4/1 |
