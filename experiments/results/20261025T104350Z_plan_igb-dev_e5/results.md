# IGBench results (20261025T104350Z_plan_igb-dev_e5)

Benchmark `igbench-v1` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:sbert | 0.820 | 0.543 | 0.337 | 0.894 | 0.929 | 0.886 | 0.057 |
| ig:rule/index:sbert | 0.775 | 0.549 | 0.343 | 0.893 | 0.902 | 0.857 | 0.086 |
| ig:rule/index:sbert+rnorm=minmax | 0.811 | 0.566 | 0.340 | 0.897 | 0.898 | 0.829 | 0.086 |
| ig:rule/index:sbert+align=0 | 0.798 | 0.543 | 0.331 | 0.882 | 0.891 | 0.829 | 0.057 |
| ig:gold/gold:sbert | 0.757 | 0.549 | 0.329 | 0.853 | 0.920 | 0.886 | 0.057 |
| ig:gold/gold:sbert+rnorm=minmax | 0.836 | 0.566 | 0.349 | 0.908 | 0.922 | 0.886 | 0.057 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:sbert | 0.826 | 0.519 | 0.943 | 0.906 |
| ig:rule/index:sbert | 0.777 | 0.525 | 0.913 | 0.875 |
| ig:rule/index:sbert+rnorm=minmax | 0.816 | 0.544 | 0.909 | 0.844 |
| ig:rule/index:sbert+align=0 | 0.802 | 0.519 | 0.902 | 0.844 |
| ig:gold/gold:sbert | 0.757 | 0.525 | 0.933 | 0.906 |
| ig:gold/gold:sbert+rnorm=minmax | 0.843 | 0.544 | 0.936 | 0.906 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:sbert | 0.361 | 0.780 | 0.894 |
| ig:rule/index:sbert | 0.356 | 0.801 | 0.893 |
| ig:rule/index:sbert+rnorm=minmax | 0.353 | 0.811 | 0.897 |
| ig:rule/index:sbert+align=0 | 0.330 | 0.789 | 0.882 |
| ig:gold/gold:sbert | 0.360 | 0.783 | 0.853 |
| ig:gold/gold:sbert+rnorm=minmax | 0.336 | 0.780 | 0.908 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | aggregate (n=3) | compare (n=10) | explain (n=7) | monitor (n=5) | predict (n=8) |
|---|---|---|---|---|---|
| ctx:sbert | 0.948 | 0.829 | 0.835 | 0.773 | 0.798 |
| ig:rule/index:sbert | 0.893 | 0.843 | 0.794 | 0.682 | 0.690 |
| ig:rule/index:sbert+rnorm=minmax | 0.926 | 0.853 | 0.817 | 0.733 | 0.771 |
| ig:rule/index:sbert+align=0 | 0.926 | 0.820 | 0.799 | 0.698 | 0.792 |
| ig:gold/gold:sbert | 0.854 | 0.809 | 0.772 | 0.745 | 0.648 |
| ig:gold/gold:sbert+rnorm=minmax | 0.925 | 0.844 | 0.855 | 0.782 | 0.827 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:sbert | 0.834 |
| ig:rule/index:sbert | 0.847 |
| ig:rule/index:sbert+rnorm=minmax | 0.835 |
| ig:rule/index:sbert+align=0 | 0.826 |
| ig:gold/gold:sbert | 0.865 |
| ig:gold/gold:sbert+rnorm=minmax | 0.833 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:rule/index:sbert | 1.000 | 0.825 | 0.970 | 0.833 | 0.812 | 0.812 | 0.688 | 0.188 | 0.494 | 0.783 |
| ig:rule/index:sbert+rnorm=minmax | 1.000 | 0.825 | 0.970 | 0.833 | 0.812 | 0.812 | 0.688 | 0.188 | 0.494 | 0.783 |
| ig:rule/index:sbert+align=0 | 1.000 | 0.825 | 0.970 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | – | – |
| ig:gold/gold:sbert | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.520 | 0.792 |
| ig:gold/gold:sbert+rnorm=minmax | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.520 | 0.792 |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:sbert | – | 95.1 / 82.2 / 93.8 | – | – | – | – | 95.2 / 82.2 / 93.8 | 3.427 |
| ig:rule/index:sbert | 0.6 / 0.2 / 1.2 | 86.4 / 88.4 / 91.9 | 1.9 / 0.5 / 7.0 | 28.7 / 21.0 / 45.7 | 669.2 / 203.7 / 2747.5 | 0.1 / 0.1 / 0.2 | 701.4 / 263.2 / 2798.1 | 12.024 |
| ig:rule/index:sbert+rnorm=minmax | 0.4 / 0.4 / 0.5 | 86.9 / 88.7 / 94.0 | 1.8 / 0.6 / 5.8 | 45.6 / 20.8 / 352.3 | 701.8 / 303.0 / 2800.8 | 0.1 / 0.1 / 0.2 | 750.6 / 389.2 / 2837.9 | 12.222 |
| ig:rule/index:sbert+align=0 | 0.4 / 0.3 / 0.5 | 89.2 / 90.3 / 94.6 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.4 / 0.3 / 0.7 | 0.8 / 0.8 / 1.3 | 3.604 |
| ig:gold/gold:sbert | 0.1 / 0.1 / 0.2 | 85.8 / 86.6 / 92.1 | 0.5 / 0.2 / 1.4 | 24.0 / 24.2 / 40.2 | 880.4 / 342.4 / 3802.2 | 0.1 / 0.1 / 0.2 | 906.5 / 376.1 / 3830.3 | 16.884 |
| ig:gold/gold:sbert+rnorm=minmax | 0.1 / 0.1 / 0.2 | 87.5 / 86.5 / 93.0 | 0.6 / 0.2 / 1.5 | 54.1 / 23.7 / 378.6 | 935.1 / 356.0 / 4021.4 | 0.1 / 0.1 / 0.2 | 991.2 / 412.5 / 4056.7 | 17.44 |

Context index build (one-off, ms): sbert: 10315 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:rule/index:sbert+rnorm=minmax | ctx:sbert | ndcg@10 | -0.010 | [-0.035, +0.012] | 0.405 | 11/16 |
| ig:rule/index:sbert+rnorm=minmax | ctx:sbert | mrr | -0.031 | [-0.074, +0.005] | 0.251 | 1/3 |
| ig:rule/index:sbert+rnorm=minmax | ctx:sbert | useful@1 | -0.057 | [-0.143, +0.000] | 0.501 | 0/2 |
| ig:rule/index:sbert | ctx:sbert | ndcg@10 | -0.045 | [-0.084, -0.011] | 0.019 | 8/22 |
| ig:rule/index:sbert | ctx:sbert | mrr | -0.027 | [-0.083, +0.009] | 0.506 | 1/2 |
| ig:rule/index:sbert | ctx:sbert | useful@1 | -0.029 | [-0.086, +0.000] | 1.000 | 0/1 |
| ig:rule/index:sbert+align=0 | ctx:sbert | ndcg@10 | -0.023 | [-0.046, -0.004] | 0.024 | 11/15 |
| ig:rule/index:sbert+align=0 | ctx:sbert | mrr | -0.037 | [-0.080, +0.000] | 0.252 | 0/3 |
| ig:rule/index:sbert+align=0 | ctx:sbert | useful@1 | -0.057 | [-0.143, +0.000] | 0.507 | 0/2 |
| ig:gold/gold:sbert+rnorm=minmax | ctx:sbert | ndcg@10 | +0.014 | [-0.006, +0.031] | 0.161 | 15/10 |
| ig:gold/gold:sbert+rnorm=minmax | ctx:sbert | mrr | -0.006 | [-0.073, +0.043] | 1.000 | 2/1 |
| ig:gold/gold:sbert+rnorm=minmax | ctx:sbert | useful@1 | +0.000 | [-0.086, +0.086] | 1.000 | 1/1 |
| ig:gold/gold:sbert | ctx:sbert | ndcg@10 | -0.063 | [-0.124, -0.008] | 0.037 | 8/23 |
| ig:gold/gold:sbert | ctx:sbert | mrr | -0.009 | [-0.079, +0.043] | 1.000 | 2/1 |
| ig:gold/gold:sbert | ctx:sbert | useful@1 | +0.000 | [-0.086, +0.086] | 1.000 | 1/1 |
