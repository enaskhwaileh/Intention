# IGBench results (20261025T180143Z_plan_igb-dev_stella_q32)

Benchmark `igbench-v1` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:sbert | 0.844 | 0.571 | 0.351 | 0.902 | 0.887 | 0.800 | 0.114 |
| ig:llm/llm:sbert | 0.812 | 0.560 | 0.343 | 0.890 | 0.885 | 0.829 | 0.086 |
| ig:llm/llm:sbert+repair=1 | 0.814 | 0.560 | 0.349 | 0.896 | 0.908 | 0.857 | 0.086 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.856 | 0.571 | 0.351 | 0.900 | 0.933 | 0.886 | 0.086 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.844 | 0.560 | 0.346 | 0.895 | 0.909 | 0.829 | 0.114 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:sbert | 0.850 | 0.556 | 0.897 | 0.812 |
| ig:llm/llm:sbert | 0.815 | 0.544 | 0.895 | 0.844 |
| ig:llm/llm:sbert+repair=1 | 0.818 | 0.544 | 0.920 | 0.875 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.863 | 0.556 | 0.948 | 0.906 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.850 | 0.544 | 0.922 | 0.844 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:sbert | 0.335 | 0.809 | 0.902 |
| ig:llm/llm:sbert | 0.337 | 0.804 | 0.890 |
| ig:llm/llm:sbert+repair=1 | 0.341 | 0.808 | 0.896 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.355 | 0.813 | 0.900 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.339 | 0.807 | 0.895 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | aggregate (n=3) | compare (n=10) | explain (n=7) | monitor (n=5) | predict (n=8) |
|---|---|---|---|---|---|
| ctx:sbert | 0.999 | 0.850 | 0.885 | 0.716 | 0.852 |
| ig:llm/llm:sbert | 0.999 | 0.886 | 0.871 | 0.724 | 0.675 |
| ig:llm/llm:sbert+repair=1 | 0.999 | 0.893 | 0.843 | 0.765 | 0.675 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.999 | 0.878 | 0.890 | 0.777 | 0.828 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.999 | 0.842 | 0.882 | 0.765 | 0.837 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:sbert | 0.878 |
| ig:llm/llm:sbert | 0.850 |
| ig:llm/llm:sbert+repair=1 | 0.852 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.836 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.821 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:llm/llm:sbert | 0.750 | 0.853 | 0.958 | 0.556 | 0.531 | 0.500 | 0.516 | 0.469 | 0.510 | 0.679 |
| ig:llm/llm:sbert+repair=1 | 0.944 | 0.774 | 0.935 | 0.750 | 0.719 | 0.688 | 0.630 | 0.281 | 0.554 | 0.720 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.944 | 0.774 | 0.935 | 0.750 | 0.719 | 0.688 | 0.630 | 0.281 | 0.554 | 0.720 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.944 | 0.774 | 0.935 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | – | – |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:sbert | – | 108.0 / 94.0 / 108.9 | – | – | – | – | 108.1 / 94.1 / 108.9 | 3.891 |
| ig:llm/llm:sbert | 5.6 / 4.6 / 7.8 | 98.0 / 95.1 / 108.8 | 1.6 / 1.1 / 4.0 | 13.8 / 0.0 / 35.2 | 829.7 / 0.0 / 4174.4 | 0.2 / 0.1 / 0.6 | 851.5 / 10.4 / 4226.0 | 19.157 |
| ig:llm/llm:sbert+repair=1 | 7.2 / 6.2 / 13.5 | 97.9 / 96.6 / 106.7 | 2.1 / 1.4 / 5.7 | 25.2 / 20.4 / 44.9 | 975.2 / 116.7 / 4127.9 | 0.2 / 0.1 / 0.6 | 1010.9 / 159.5 / 4174.4 | 19.422 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 6.4 / 5.3 / 13.8 | 95.7 / 95.2 / 105.8 | 2.0 / 1.4 / 5.3 | 98.4 / 20.0 / 358.4 | 965.1 / 96.2 / 4000.9 | 0.1 / 0.1 / 0.4 | 1072.9 / 148.2 / 4376.1 | 19.972 |
| ig:llm/llm:sbert+repair=1+align=0 | 9.2 / 8.0 / 18.5 | 89.9 / 88.7 / 99.2 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.4 / 0.4 / 0.7 | 9.7 / 8.4 / 19.0 | 3.74 |

Context index build (one-off, ms): sbert: 27058 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:llm/llm:sbert+repair=1+align=0 | ctx:sbert | ndcg@10 | +0.001 | [-0.010, +0.013] | 0.920 | 7/9 |
| ig:llm/llm:sbert+repair=1+align=0 | ctx:sbert | mrr | +0.023 | [+0.000, +0.069] | 1.000 | 1/0 |
| ig:llm/llm:sbert+repair=1+align=0 | ctx:sbert | useful@1 | +0.029 | [+0.000, +0.086] | 1.000 | 1/0 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | ndcg@10 | +0.012 | [-0.005, +0.029] | 0.206 | 13/9 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | mrr | +0.047 | [-0.024, +0.123] | 0.311 | 4/1 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | useful@1 | +0.086 | [-0.029, +0.200] | 0.373 | 4/1 |
| ig:llm/llm:sbert | ctx:sbert | ndcg@10 | -0.031 | [-0.086, +0.010] | 0.306 | 7/12 |
| ig:llm/llm:sbert | ctx:sbert | mrr | -0.002 | [-0.083, +0.074] | 1.000 | 3/2 |
| ig:llm/llm:sbert | ctx:sbert | useful@1 | +0.029 | [-0.086, +0.171] | 1.000 | 3/2 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | ndcg@10 | -0.029 | [-0.085, +0.015] | 0.354 | 10/16 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | mrr | +0.021 | [-0.075, +0.109] | 0.692 | 4/2 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | useful@1 | +0.057 | [-0.086, +0.200] | 0.694 | 4/2 |
