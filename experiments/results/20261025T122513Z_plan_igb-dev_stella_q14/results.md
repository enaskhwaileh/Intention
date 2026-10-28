# IGBench results (20261025T122513Z_plan_igb-dev_stella_q14)

Benchmark `igbench-v1` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:sbert | 0.844 | 0.571 | 0.351 | 0.902 | 0.887 | 0.800 | 0.114 |
| ig:llm/llm:sbert | 0.816 | 0.554 | 0.349 | 0.895 | 0.904 | 0.857 | 0.086 |
| ig:llm/llm:sbert+repair=1 | 0.818 | 0.560 | 0.351 | 0.899 | 0.927 | 0.886 | 0.086 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.858 | 0.571 | 0.354 | 0.903 | 0.933 | 0.886 | 0.086 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.844 | 0.560 | 0.346 | 0.895 | 0.909 | 0.829 | 0.114 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:sbert | 0.850 | 0.556 | 0.897 | 0.812 |
| ig:llm/llm:sbert | 0.820 | 0.537 | 0.916 | 0.875 |
| ig:llm/llm:sbert+repair=1 | 0.821 | 0.544 | 0.941 | 0.906 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.865 | 0.556 | 0.948 | 0.906 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.850 | 0.544 | 0.922 | 0.844 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:sbert | 0.335 | 0.809 | 0.902 |
| ig:llm/llm:sbert | 0.351 | 0.804 | 0.895 |
| ig:llm/llm:sbert+repair=1 | 0.355 | 0.808 | 0.899 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.355 | 0.813 | 0.903 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.339 | 0.807 | 0.895 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | aggregate (n=3) | compare (n=10) | explain (n=7) | monitor (n=5) | predict (n=8) |
|---|---|---|---|---|---|
| ctx:sbert | 0.999 | 0.850 | 0.885 | 0.716 | 0.852 |
| ig:llm/llm:sbert | 0.949 | 0.884 | 0.877 | 0.716 | 0.715 |
| ig:llm/llm:sbert+repair=1 | 0.949 | 0.884 | 0.864 | 0.744 | 0.715 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.984 | 0.878 | 0.896 | 0.777 | 0.836 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.999 | 0.841 | 0.882 | 0.766 | 0.837 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:sbert | 0.878 |
| ig:llm/llm:sbert | 0.829 |
| ig:llm/llm:sbert+repair=1 | 0.851 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.835 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.821 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:llm/llm:sbert | 0.778 | 0.779 | 0.920 | 0.639 | 0.594 | 0.594 | 0.578 | 0.406 | 0.488 | 0.736 |
| ig:llm/llm:sbert+repair=1 | 1.000 | 0.746 | 0.909 | 0.806 | 0.781 | 0.781 | 0.703 | 0.219 | 0.482 | 0.755 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 1.000 | 0.746 | 0.909 | 0.806 | 0.781 | 0.781 | 0.703 | 0.219 | 0.482 | 0.755 |
| ig:llm/llm:sbert+repair=1+align=0 | 1.000 | 0.746 | 0.909 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | – | – |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:sbert | – | 112.4 / 101.3 / 109.9 | – | – | – | – | 112.4 / 101.3 / 109.9 | 4.047 |
| ig:llm/llm:sbert | 4.6 / 4.4 / 7.4 | 100.3 / 99.6 / 117.3 | 1.6 / 1.1 / 3.9 | 14.4 / 17.2 / 33.0 | 670.4 / 63.0 / 3929.8 | 0.2 / 0.1 / 0.5 | 691.9 / 90.0 / 3958.8 | 12.82 |
| ig:llm/llm:sbert+repair=1 | 4.0 / 3.4 / 7.1 | 112.9 / 112.2 / 128.1 | 2.2 / 1.5 / 5.5 | 47.1 / 25.1 / 275.3 | 990.8 / 313.6 / 5276.0 | 0.2 / 0.1 / 0.3 | 1045.3 / 417.6 / 5343.9 | 19.294 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 7.6 / 6.6 / 14.7 | 105.5 / 104.2 / 119.0 | 2.2 / 1.4 / 6.2 | 18.7 / 20.9 / 41.2 | 833.3 / 190.1 / 4021.1 | 0.1 / 0.1 / 0.5 | 862.9 / 244.0 / 4047.3 | 16.991 |
| ig:llm/llm:sbert+repair=1+align=0 | 4.7 / 4.7 / 7.9 | 105.3 / 103.5 / 118.1 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.4 / 0.3 / 0.7 | 5.2 / 5.1 / 8.2 | 4.222 |

Context index build (one-off, ms): sbert: 11343 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:llm/llm:sbert+repair=1+align=0 | ctx:sbert | ndcg@10 | +0.001 | [-0.010, +0.013] | 0.928 | 7/9 |
| ig:llm/llm:sbert+repair=1+align=0 | ctx:sbert | mrr | +0.023 | [+0.000, +0.069] | 1.000 | 1/0 |
| ig:llm/llm:sbert+repair=1+align=0 | ctx:sbert | useful@1 | +0.029 | [+0.000, +0.086] | 1.000 | 1/0 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | ndcg@10 | +0.013 | [-0.004, +0.031] | 0.142 | 16/8 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | mrr | +0.047 | [-0.024, +0.123] | 0.311 | 4/1 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | useful@1 | +0.086 | [-0.029, +0.200] | 0.373 | 4/1 |
| ig:llm/llm:sbert | ctx:sbert | ndcg@10 | -0.027 | [-0.076, +0.011] | 0.338 | 8/13 |
| ig:llm/llm:sbert | ctx:sbert | mrr | +0.017 | [-0.051, +0.086] | 0.624 | 3/1 |
| ig:llm/llm:sbert | ctx:sbert | useful@1 | +0.057 | [-0.057, +0.171] | 0.624 | 3/1 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | ndcg@10 | -0.025 | [-0.077, +0.016] | 0.397 | 11/16 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | mrr | +0.040 | [-0.037, +0.123] | 0.373 | 4/1 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | useful@1 | +0.086 | [-0.029, +0.200] | 0.373 | 4/1 |
