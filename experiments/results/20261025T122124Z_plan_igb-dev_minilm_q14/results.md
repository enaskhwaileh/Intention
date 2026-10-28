# IGBench results (20261025T122124Z_plan_igb-dev_minilm_q14)

Benchmark `igbench-v1` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:sbert | 0.769 | 0.474 | 0.297 | 0.840 | 0.838 | 0.743 | 0.143 |
| ig:llm/llm:sbert | 0.787 | 0.497 | 0.317 | 0.858 | 0.859 | 0.800 | 0.143 |
| ig:llm/llm:sbert+repair=1 | 0.791 | 0.509 | 0.329 | 0.873 | 0.857 | 0.800 | 0.143 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.787 | 0.509 | 0.306 | 0.850 | 0.841 | 0.771 | 0.143 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.759 | 0.469 | 0.294 | 0.837 | 0.820 | 0.743 | 0.143 |
| rerank:llm:sbert | 0.831 | 0.543 | 0.317 | 0.870 | 0.963 | 0.943 | 0.029 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:sbert | 0.768 | 0.450 | 0.823 | 0.719 |
| ig:llm/llm:sbert | 0.788 | 0.475 | 0.846 | 0.781 |
| ig:llm/llm:sbert+repair=1 | 0.792 | 0.487 | 0.843 | 0.781 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.788 | 0.487 | 0.826 | 0.750 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.757 | 0.444 | 0.803 | 0.719 |
| rerank:llm:sbert | 0.833 | 0.519 | 0.959 | 0.938 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:sbert | 0.286 | 0.728 | 0.840 |
| ig:llm/llm:sbert | 0.301 | 0.728 | 0.858 |
| ig:llm/llm:sbert+repair=1 | 0.301 | 0.741 | 0.873 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.298 | 0.746 | 0.850 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.289 | 0.708 | 0.837 |
| rerank:llm:sbert | 0.379 | 0.797 | 0.870 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | aggregate (n=3) | compare (n=10) | explain (n=7) | monitor (n=5) | predict (n=8) |
|---|---|---|---|---|---|
| ctx:sbert | 0.966 | 0.762 | 0.808 | 0.673 | 0.730 |
| ig:llm/llm:sbert | 0.965 | 0.817 | 0.844 | 0.673 | 0.711 |
| ig:llm/llm:sbert+repair=1 | 0.966 | 0.817 | 0.850 | 0.695 | 0.711 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.982 | 0.789 | 0.842 | 0.663 | 0.748 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.984 | 0.770 | 0.786 | 0.651 | 0.706 |
| rerank:llm:sbert | 0.967 | 0.801 | 0.851 | 0.757 | 0.805 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:sbert | 0.772 |
| ig:llm/llm:sbert | 0.802 |
| ig:llm/llm:sbert+repair=1 | 0.804 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.769 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.754 |
| rerank:llm:sbert | 0.850 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:llm/llm:sbert | 0.778 | 0.779 | 0.920 | 0.639 | 0.594 | 0.594 | 0.578 | 0.406 | 0.495 | 0.712 |
| ig:llm/llm:sbert+repair=1 | 1.000 | 0.746 | 0.909 | 0.806 | 0.781 | 0.781 | 0.703 | 0.219 | 0.515 | 0.745 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 1.000 | 0.746 | 0.909 | 0.806 | 0.781 | 0.781 | 0.703 | 0.219 | 0.515 | 0.745 |
| ig:llm/llm:sbert+repair=1+align=0 | 1.000 | 0.746 | 0.909 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | – | – |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:sbert | – | 99.3 / 89.9 / 94.1 | – | – | – | – | 99.4 / 90.0 / 94.2 | 3.578 |
| ig:llm/llm:sbert | 6.1 / 5.5 / 9.9 | 87.9 / 90.0 / 91.8 | 1.6 / 1.2 / 4.2 | 24.1 / 20.4 / 44.6 | 608.3 / 49.4 / 3874.2 | 0.2 / 0.1 / 0.6 | 641.1 / 92.7 / 3905.0 | 12.169 |
| ig:llm/llm:sbert+repair=1 | 8.1 / 7.3 / 20.9 | 88.5 / 88.0 / 92.4 | 2.1 / 1.5 / 4.7 | 28.9 / 22.4 / 47.1 | 779.2 / 101.4 / 3927.2 | 0.1 / 0.1 / 0.2 | 819.3 / 132.8 / 3983.8 | 16.574 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 7.7 / 7.5 / 14.8 | 85.2 / 85.5 / 92.2 | 1.9 / 1.4 / 5.2 | 18.5 / 21.1 / 40.9 | 760.3 / 101.6 / 3851.5 | 0.1 / 0.1 / 0.2 | 789.5 / 138.9 / 3881.0 | 15.933 |
| ig:llm/llm:sbert+repair=1+align=0 | 9.3 / 8.5 / 20.6 | 86.4 / 86.1 / 91.6 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.4 / 0.4 / 0.7 | 9.7 / 8.8 / 21.0 | 3.477 |
| rerank:llm:sbert | – | 507.8 / 196.4 / 1104.6 | – | – | – | – | 34683.0 / 35492.6 / 48969.6 | 88.338 |

Context index build (one-off, ms): sbert: 13468 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:llm/llm:sbert+repair=1+align=0 | ctx:sbert | ndcg@10 | -0.009 | [-0.024, +0.010] | 0.375 | 12/15 |
| ig:llm/llm:sbert+repair=1+align=0 | ctx:sbert | mrr | -0.018 | [-0.063, +0.024] | 0.462 | 2/5 |
| ig:llm/llm:sbert+repair=1+align=0 | ctx:sbert | useful@1 | +0.000 | [-0.086, +0.086] | 1.000 | 1/1 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | ndcg@10 | +0.018 | [-0.005, +0.041] | 0.146 | 19/11 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | mrr | +0.003 | [-0.056, +0.062] | 0.943 | 5/5 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | useful@1 | +0.029 | [-0.057, +0.114] | 1.000 | 2/1 |
| ig:llm/llm:sbert | ctx:sbert | ndcg@10 | +0.018 | [-0.016, +0.054] | 0.348 | 13/10 |
| ig:llm/llm:sbert | ctx:sbert | mrr | +0.021 | [-0.058, +0.105] | 0.645 | 4/4 |
| ig:llm/llm:sbert | ctx:sbert | useful@1 | +0.057 | [-0.057, +0.171] | 0.626 | 3/1 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | ndcg@10 | +0.022 | [-0.013, +0.059] | 0.260 | 19/11 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | mrr | +0.018 | [-0.060, +0.103] | 0.687 | 5/5 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | useful@1 | +0.057 | [-0.057, +0.171] | 0.626 | 3/1 |
