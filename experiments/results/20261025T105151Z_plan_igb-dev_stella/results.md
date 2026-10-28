# IGBench results (20261025T105151Z_plan_igb-dev_stella)

Benchmark `igbench-v1` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:sbert | 0.844 | 0.571 | 0.351 | 0.902 | 0.887 | 0.800 | 0.114 |
| ig:rule/index:sbert | 0.826 | 0.549 | 0.363 | 0.917 | 0.919 | 0.886 | 0.057 |
| ig:rule/index:sbert+rnorm=minmax | 0.851 | 0.566 | 0.354 | 0.902 | 0.929 | 0.886 | 0.057 |
| ig:rule/index:sbert+align=0 | 0.842 | 0.554 | 0.346 | 0.895 | 0.900 | 0.829 | 0.086 |
| ig:gold/gold:sbert | 0.829 | 0.543 | 0.357 | 0.906 | 0.941 | 0.914 | 0.057 |
| ig:gold/gold:sbert+rnorm=minmax | 0.862 | 0.554 | 0.357 | 0.905 | 0.948 | 0.914 | 0.057 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:sbert | 0.850 | 0.556 | 0.897 | 0.812 |
| ig:rule/index:sbert | 0.831 | 0.531 | 0.933 | 0.906 |
| ig:rule/index:sbert+rnorm=minmax | 0.857 | 0.550 | 0.944 | 0.906 |
| ig:rule/index:sbert+align=0 | 0.847 | 0.537 | 0.911 | 0.844 |
| ig:gold/gold:sbert | 0.834 | 0.525 | 0.956 | 0.938 |
| ig:gold/gold:sbert+rnorm=minmax | 0.870 | 0.537 | 0.964 | 0.938 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:sbert | 0.335 | 0.809 | 0.902 |
| ig:rule/index:sbert | 0.361 | 0.801 | 0.917 |
| ig:rule/index:sbert+rnorm=minmax | 0.361 | 0.811 | 0.902 |
| ig:rule/index:sbert+align=0 | 0.349 | 0.806 | 0.895 |
| ig:gold/gold:sbert | 0.365 | 0.793 | 0.906 |
| ig:gold/gold:sbert+rnorm=minmax | 0.365 | 0.798 | 0.905 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | aggregate (n=3) | compare (n=10) | explain (n=7) | monitor (n=5) | predict (n=8) |
|---|---|---|---|---|---|
| ctx:sbert | 0.999 | 0.850 | 0.885 | 0.716 | 0.852 |
| ig:rule/index:sbert | 0.983 | 0.892 | 0.873 | 0.710 | 0.744 |
| ig:rule/index:sbert+rnorm=minmax | 1.000 | 0.888 | 0.898 | 0.707 | 0.828 |
| ig:rule/index:sbert+align=0 | 1.000 | 0.851 | 0.879 | 0.733 | 0.835 |
| ig:gold/gold:sbert | 0.983 | 0.908 | 0.855 | 0.774 | 0.712 |
| ig:gold/gold:sbert+rnorm=minmax | 1.000 | 0.901 | 0.888 | 0.777 | 0.829 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:sbert | 0.878 |
| ig:rule/index:sbert | 0.827 |
| ig:rule/index:sbert+rnorm=minmax | 0.814 |
| ig:rule/index:sbert+align=0 | 0.798 |
| ig:gold/gold:sbert | 0.840 |
| ig:gold/gold:sbert+rnorm=minmax | 0.812 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:rule/index:sbert | 1.000 | 0.825 | 0.970 | 0.833 | 0.812 | 0.812 | 0.688 | 0.188 | 0.474 | 0.776 |
| ig:rule/index:sbert+rnorm=minmax | 1.000 | 0.825 | 0.970 | 0.833 | 0.812 | 0.812 | 0.688 | 0.188 | 0.474 | 0.776 |
| ig:rule/index:sbert+align=0 | 1.000 | 0.825 | 0.970 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | – | – |
| ig:gold/gold:sbert | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.502 | 0.792 |
| ig:gold/gold:sbert+rnorm=minmax | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.502 | 0.792 |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:sbert | – | 122.8 / 110.5 / 116.7 | – | – | – | – | 122.8 / 110.5 / 116.8 | 4.421 |
| ig:rule/index:sbert | 0.7 / 0.4 / 1.6 | 111.3 / 111.5 / 114.7 | 1.7 / 0.6 / 5.5 | 30.1 / 22.2 / 53.9 | 830.6 / 218.5 / 3918.3 | 0.1 / 0.1 / 0.2 | 864.2 / 299.8 / 3966.4 | 16.155 |
| ig:rule/index:sbert+rnorm=minmax | 0.4 / 0.4 / 0.5 | 117.9 / 116.9 / 122.7 | 1.7 / 0.6 / 5.7 | 34.8 / 21.3 / 44.7 | 890.8 / 226.2 / 3892.9 | 0.1 / 0.1 / 0.2 | 928.8 / 277.5 / 4177.3 | 16.981 |
| ig:rule/index:sbert+align=0 | 0.4 / 0.4 / 0.5 | 110.7 / 110.6 / 118.7 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.4 / 0.4 / 0.8 | 0.9 / 0.8 / 1.4 | 4.449 |
| ig:gold/gold:sbert | 0.1 / 0.1 / 0.2 | 107.9 / 107.9 / 115.1 | 0.7 / 0.2 / 1.6 | 26.6 / 26.9 / 47.5 | 961.4 / 400.9 / 4124.0 | 0.1 / 0.1 / 0.2 | 990.2 / 443.2 / 4163.1 | 20.805 |
| ig:gold/gold:sbert+rnorm=minmax | 0.1 / 0.1 / 0.2 | 111.5 / 111.6 / 116.8 | 0.6 / 0.2 / 1.6 | 66.3 / 24.4 / 310.3 | 985.2 / 454.0 / 4171.2 | 0.1 / 0.1 / 0.2 | 1053.5 / 542.4 / 4204.7 | 21.325 |

Context index build (one-off, ms): sbert: 12436 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:rule/index:sbert+rnorm=minmax | ctx:sbert | ndcg@10 | +0.007 | [-0.007, +0.022] | 0.388 | 14/9 |
| ig:rule/index:sbert+rnorm=minmax | ctx:sbert | mrr | +0.043 | [-0.014, +0.100] | 0.375 | 4/1 |
| ig:rule/index:sbert+rnorm=minmax | ctx:sbert | useful@1 | +0.086 | [-0.029, +0.200] | 0.375 | 4/1 |
| ig:rule/index:sbert | ctx:sbert | ndcg@10 | -0.017 | [-0.057, +0.016] | 0.476 | 11/15 |
| ig:rule/index:sbert | ctx:sbert | mrr | +0.033 | [-0.045, +0.100] | 0.375 | 4/1 |
| ig:rule/index:sbert | ctx:sbert | useful@1 | +0.086 | [-0.029, +0.200] | 0.375 | 4/1 |
| ig:rule/index:sbert+align=0 | ctx:sbert | ndcg@10 | -0.002 | [-0.012, +0.008] | 0.693 | 9/12 |
| ig:rule/index:sbert+align=0 | ctx:sbert | mrr | +0.013 | [-0.003, +0.043] | 1.000 | 1/1 |
| ig:rule/index:sbert+align=0 | ctx:sbert | useful@1 | +0.029 | [+0.000, +0.086] | 1.000 | 1/0 |
| ig:gold/gold:sbert+rnorm=minmax | ctx:sbert | ndcg@10 | +0.018 | [-0.001, +0.038] | 0.087 | 16/8 |
| ig:gold/gold:sbert+rnorm=minmax | ctx:sbert | mrr | +0.061 | [-0.014, +0.140] | 0.187 | 5/1 |
| ig:gold/gold:sbert+rnorm=minmax | ctx:sbert | useful@1 | +0.114 | [+0.000, +0.257] | 0.219 | 5/1 |
| ig:gold/gold:sbert | ctx:sbert | ndcg@10 | -0.014 | [-0.068, +0.033] | 0.690 | 12/16 |
| ig:gold/gold:sbert | ctx:sbert | mrr | +0.054 | [-0.031, +0.140] | 0.219 | 5/1 |
| ig:gold/gold:sbert | ctx:sbert | useful@1 | +0.114 | [+0.000, +0.257] | 0.219 | 5/1 |
