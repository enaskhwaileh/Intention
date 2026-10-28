# IGBench results (20261025T104818Z_plan_igb-dev_bge)

Benchmark `igbench-v1` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:sbert | 0.806 | 0.531 | 0.337 | 0.886 | 0.858 | 0.743 | 0.143 |
| ig:rule/index:sbert | 0.797 | 0.549 | 0.349 | 0.897 | 0.924 | 0.886 | 0.029 |
| ig:rule/index:sbert+rnorm=minmax | 0.837 | 0.560 | 0.349 | 0.905 | 0.929 | 0.886 | 0.029 |
| ig:rule/index:sbert+align=0 | 0.813 | 0.526 | 0.340 | 0.896 | 0.875 | 0.771 | 0.114 |
| ig:gold/gold:sbert | 0.793 | 0.554 | 0.340 | 0.875 | 0.945 | 0.914 | 0.029 |
| ig:gold/gold:sbert+rnorm=minmax | 0.842 | 0.571 | 0.349 | 0.906 | 0.938 | 0.886 | 0.029 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:sbert | 0.808 | 0.525 | 0.845 | 0.719 |
| ig:rule/index:sbert | 0.798 | 0.544 | 0.917 | 0.875 |
| ig:rule/index:sbert+rnorm=minmax | 0.842 | 0.556 | 0.922 | 0.875 |
| ig:rule/index:sbert+align=0 | 0.816 | 0.519 | 0.863 | 0.750 |
| ig:gold/gold:sbert | 0.794 | 0.550 | 0.940 | 0.906 |
| ig:gold/gold:sbert+rnorm=minmax | 0.848 | 0.569 | 0.932 | 0.875 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:sbert | 0.294 | 0.777 | 0.886 |
| ig:rule/index:sbert | 0.356 | 0.796 | 0.897 |
| ig:rule/index:sbert+rnorm=minmax | 0.356 | 0.808 | 0.905 |
| ig:rule/index:sbert+align=0 | 0.325 | 0.772 | 0.896 |
| ig:gold/gold:sbert | 0.359 | 0.793 | 0.875 |
| ig:gold/gold:sbert+rnorm=minmax | 0.331 | 0.812 | 0.906 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | aggregate (n=3) | compare (n=10) | explain (n=7) | monitor (n=5) | predict (n=8) |
|---|---|---|---|---|---|
| ctx:sbert | 0.986 | 0.825 | 0.831 | 0.716 | 0.771 |
| ig:rule/index:sbert | 0.948 | 0.859 | 0.838 | 0.691 | 0.707 |
| ig:rule/index:sbert+rnorm=minmax | 0.999 | 0.857 | 0.874 | 0.723 | 0.810 |
| ig:rule/index:sbert+align=0 | 0.999 | 0.810 | 0.827 | 0.718 | 0.810 |
| ig:gold/gold:sbert | 0.937 | 0.853 | 0.828 | 0.731 | 0.682 |
| ig:gold/gold:sbert+rnorm=minmax | 0.999 | 0.845 | 0.869 | 0.794 | 0.811 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:sbert | 0.842 |
| ig:rule/index:sbert | 0.855 |
| ig:rule/index:sbert+rnorm=minmax | 0.840 |
| ig:rule/index:sbert+align=0 | 0.833 |
| ig:gold/gold:sbert | 0.853 |
| ig:gold/gold:sbert+rnorm=minmax | 0.840 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:rule/index:sbert | 1.000 | 0.825 | 0.970 | 0.833 | 0.812 | 0.812 | 0.688 | 0.188 | 0.480 | 0.778 |
| ig:rule/index:sbert+rnorm=minmax | 1.000 | 0.825 | 0.970 | 0.833 | 0.812 | 0.812 | 0.688 | 0.188 | 0.480 | 0.778 |
| ig:rule/index:sbert+align=0 | 1.000 | 0.825 | 0.970 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | – | – |
| ig:gold/gold:sbert | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.505 | 0.783 |
| ig:gold/gold:sbert+rnorm=minmax | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.505 | 0.783 |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:sbert | – | 98.9 / 83.9 / 101.3 | – | – | – | – | 98.9 / 83.9 / 101.4 | 3.562 |
| ig:rule/index:sbert | 0.7 / 0.4 / 1.8 | 92.4 / 91.8 / 99.8 | 1.7 / 0.6 / 5.9 | 28.9 / 22.2 / 41.3 | 822.3 / 175.7 / 4154.6 | 0.1 / 0.1 / 0.2 | 854.6 / 228.0 / 4202.3 | 16.398 |
| ig:rule/index:sbert+rnorm=minmax | 0.4 / 0.4 / 0.5 | 95.8 / 95.2 / 101.9 | 1.6 / 0.6 / 5.8 | 57.5 / 24.1 / 353.7 | 858.4 / 174.6 / 4164.0 | 0.1 / 0.1 / 0.2 | 919.0 / 342.3 / 4206.6 | 16.828 |
| ig:rule/index:sbert+align=0 | 0.4 / 0.4 / 0.5 | 97.5 / 97.0 / 101.9 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.4 / 0.4 / 0.7 | 0.9 / 0.8 / 1.4 | 3.95 |
| ig:gold/gold:sbert | 0.1 / 0.1 / 0.2 | 94.9 / 95.6 / 100.8 | 0.6 / 0.2 / 1.4 | 24.5 / 24.6 / 45.0 | 902.5 / 308.7 / 4161.3 | 0.1 / 0.1 / 0.2 | 929.0 / 333.0 / 4201.5 | 20.993 |
| ig:gold/gold:sbert+rnorm=minmax | 0.1 / 0.1 / 0.2 | 93.6 / 93.3 / 99.8 | 0.5 / 0.2 / 1.3 | 48.7 / 23.8 / 325.8 | 939.1 / 321.6 / 4204.6 | 0.1 / 0.1 / 0.2 | 989.7 / 388.6 / 4500.6 | 21.471 |

Context index build (one-off, ms): sbert: 12661 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:rule/index:sbert+rnorm=minmax | ctx:sbert | ndcg@10 | +0.028 | [+0.005, +0.054] | 0.034 | 17/10 |
| ig:rule/index:sbert+rnorm=minmax | ctx:sbert | mrr | +0.070 | [+0.009, +0.138] | 0.064 | 5/2 |
| ig:rule/index:sbert+rnorm=minmax | ctx:sbert | useful@1 | +0.143 | [+0.029, +0.257] | 0.064 | 5/0 |
| ig:rule/index:sbert | ctx:sbert | ndcg@10 | -0.010 | [-0.051, +0.029] | 0.640 | 13/16 |
| ig:rule/index:sbert | ctx:sbert | mrr | +0.066 | [+0.004, +0.137] | 0.064 | 5/1 |
| ig:rule/index:sbert | ctx:sbert | useful@1 | +0.143 | [+0.029, +0.257] | 0.064 | 5/0 |
| ig:rule/index:sbert+align=0 | ctx:sbert | ndcg@10 | +0.005 | [-0.012, +0.024] | 0.609 | 11/12 |
| ig:rule/index:sbert+align=0 | ctx:sbert | mrr | +0.017 | [-0.033, +0.071] | 0.752 | 2/2 |
| ig:rule/index:sbert+align=0 | ctx:sbert | useful@1 | +0.029 | [-0.057, +0.114] | 1.000 | 2/1 |
| ig:gold/gold:sbert+rnorm=minmax | ctx:sbert | ndcg@10 | +0.034 | [+0.006, +0.065] | 0.033 | 15/12 |
| ig:gold/gold:sbert+rnorm=minmax | ctx:sbert | mrr | +0.080 | [-0.006, +0.164] | 0.112 | 6/1 |
| ig:gold/gold:sbert+rnorm=minmax | ctx:sbert | useful@1 | +0.143 | [+0.000, +0.286] | 0.128 | 6/1 |
| ig:gold/gold:sbert | ctx:sbert | ndcg@10 | -0.015 | [-0.070, +0.036] | 0.654 | 14/17 |
| ig:gold/gold:sbert | ctx:sbert | mrr | +0.087 | [+0.014, +0.169] | 0.031 | 6/1 |
| ig:gold/gold:sbert | ctx:sbert | useful@1 | +0.171 | [+0.057, +0.286] | 0.031 | 6/0 |
