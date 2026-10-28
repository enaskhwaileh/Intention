# IGBench results (20261027T191744Z_plan_igb-dev_minilm_q32)

Benchmark `igbench-v1` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:sbert | 0.769 | 0.474 | 0.297 | 0.840 | 0.838 | 0.743 | 0.143 |
| ig:llm/llm:sbert | 0.777 | 0.497 | 0.317 | 0.863 | 0.835 | 0.771 | 0.171 |
| ig:llm/llm:sbert+repair=1 | 0.788 | 0.514 | 0.329 | 0.877 | 0.838 | 0.771 | 0.143 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.786 | 0.514 | 0.309 | 0.857 | 0.841 | 0.771 | 0.143 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.759 | 0.469 | 0.294 | 0.837 | 0.820 | 0.743 | 0.143 |
| rerank:llm:sbert | 0.828 | 0.554 | 0.311 | 0.863 | 0.967 | 0.943 | 0.057 |
| rerank:llmig:sbert | 0.818 | 0.549 | 0.314 | 0.866 | 0.926 | 0.886 | 0.057 |
| rerank:llmgold:sbert | 0.803 | 0.537 | 0.306 | 0.819 | 0.931 | 0.914 | 0.057 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:sbert | 0.768 | 0.450 | 0.823 | 0.719 |
| ig:llm/llm:sbert | 0.777 | 0.475 | 0.820 | 0.750 |
| ig:llm/llm:sbert+repair=1 | 0.788 | 0.494 | 0.822 | 0.750 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.787 | 0.494 | 0.826 | 0.750 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.757 | 0.444 | 0.803 | 0.719 |
| rerank:llm:sbert | 0.831 | 0.537 | 0.964 | 0.938 |
| rerank:llmig:sbert | 0.820 | 0.525 | 0.919 | 0.875 |
| rerank:llmgold:sbert | 0.804 | 0.512 | 0.925 | 0.906 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:sbert | 0.286 | 0.728 | 0.840 |
| ig:llm/llm:sbert | 0.286 | 0.724 | 0.863 |
| ig:llm/llm:sbert+repair=1 | 0.286 | 0.742 | 0.877 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.298 | 0.755 | 0.857 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.289 | 0.708 | 0.837 |
| rerank:llm:sbert | 0.368 | 0.801 | 0.863 |
| rerank:llmig:sbert | 0.372 | 0.807 | 0.866 |
| rerank:llmgold:sbert | 0.351 | 0.761 | 0.819 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | aggregate (n=3) | compare (n=10) | explain (n=7) | monitor (n=5) | predict (n=8) |
|---|---|---|---|---|---|
| ctx:sbert | 0.966 | 0.762 | 0.808 | 0.673 | 0.730 |
| ig:llm/llm:sbert | 0.983 | 0.821 | 0.837 | 0.675 | 0.662 |
| ig:llm/llm:sbert+repair=1 | 0.984 | 0.824 | 0.856 | 0.712 | 0.662 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.984 | 0.787 | 0.854 | 0.664 | 0.735 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.984 | 0.770 | 0.786 | 0.649 | 0.706 |
| rerank:llm:sbert | 0.967 | 0.791 | 0.857 | 0.737 | 0.816 |
| rerank:llmig:sbert | 0.984 | 0.802 | 0.872 | 0.723 | 0.758 |
| rerank:llmgold:sbert | 0.983 | 0.805 | 0.868 | 0.729 | 0.689 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:sbert | 0.772 |
| ig:llm/llm:sbert | 0.785 |
| ig:llm/llm:sbert+repair=1 | 0.801 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.768 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.754 |
| rerank:llm:sbert | 0.798 |
| rerank:llmig:sbert | 0.801 |
| rerank:llmgold:sbert | 0.774 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:llm/llm:sbert | 0.750 | 0.853 | 0.958 | 0.556 | 0.531 | 0.500 | 0.516 | 0.469 | 0.500 | 0.651 |
| ig:llm/llm:sbert+repair=1 | 0.944 | 0.774 | 0.935 | 0.750 | 0.719 | 0.688 | 0.630 | 0.281 | 0.566 | 0.711 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.944 | 0.774 | 0.935 | 0.750 | 0.719 | 0.688 | 0.630 | 0.281 | 0.566 | 0.711 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.944 | 0.774 | 0.935 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | – | – |
| rerank:llmig:sbert | 0.944 | 0.774 | 0.935 | 0.750 | 0.719 | 0.688 | 0.630 | 0.000 | – | – |
| rerank:llmgold:sbert | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | – | – |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:sbert | – | 86.9 / 75.7 / 82.4 | – | – | – | – | 87.0 / 75.8 / 82.5 | 3.132 |
| ig:llm/llm:sbert | 2.3 / 2.4 / 2.9 | 76.2 / 76.0 / 82.4 | 1.1 / 1.1 / 3.6 | 26.9 / 0.0 / 45.2 | 799.4 / 0.0 / 4037.1 | 0.1 / 0.1 / 0.3 | 830.4 / 5.7 / 4088.1 | 19.052 |
| ig:llm/llm:sbert+repair=1 | 3.2 / 2.7 / 6.2 | 76.4 / 75.6 / 83.0 | 1.5 / 1.0 / 3.9 | 23.2 / 18.3 / 34.4 | 942.4 / 76.7 / 4076.2 | 0.1 / 0.1 / 0.2 | 971.1 / 107.1 / 4117.4 | 19.109 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 3.1 / 2.6 / 5.1 | 76.9 / 75.7 / 82.3 | 1.3 / 1.0 / 3.6 | 32.2 / 17.7 / 33.8 | 956.8 / 74.7 / 4141.8 | 0.1 / 0.1 / 0.1 | 994.2 / 103.4 / 4507.6 | 19.542 |
| ig:llm/llm:sbert+repair=1+align=0 | 2.4 / 2.1 / 4.0 | 78.6 / 79.2 / 84.4 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.2 / 0.2 / 0.4 | 2.7 / 2.4 / 4.3 | 3.011 |
| rerank:llm:sbert | – | 142.9 / 132.5 / 210.3 | – | – | – | – | 146.2 / 135.9 / 211.9 | 1.363 |
| rerank:llmig:sbert | 2.6 / 1.7 / 6.4 | 115.0 / 96.3 / 203.0 | 1.4 / 1.1 / 2.4 | 22.8 / 20.0 / 37.3 | 1105.5 / 88.4 / 7425.6 | 0.1 / 0.1 / 0.1 | 33880.2 / 34569.9 / 43612.1 | 314.965 |
| rerank:llmgold:sbert | 0.2 / 0.2 / 0.2 | 115.2 / 95.6 / 210.1 | 0.2 / 0.2 / 0.2 | 66.4 / 23.7 / 359.5 | 1581.8 / 269.5 / 10360.4 | 0.1 / 0.1 / 0.1 | 36467.4 / 40302.0 / 48235.0 | 342.52 |

Context index build (one-off, ms): sbert: 11128 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:llm/llm:sbert+repair=1+align=0 | ctx:sbert | ndcg@10 | -0.009 | [-0.025, +0.010] | 0.355 | 11/15 |
| ig:llm/llm:sbert+repair=1+align=0 | ctx:sbert | mrr | -0.018 | [-0.063, +0.024] | 0.462 | 2/5 |
| ig:llm/llm:sbert+repair=1+align=0 | ctx:sbert | useful@1 | +0.000 | [-0.086, +0.086] | 1.000 | 1/1 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | ndcg@10 | +0.017 | [-0.005, +0.041] | 0.168 | 18/10 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | mrr | +0.003 | [-0.056, +0.062] | 0.943 | 5/5 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | useful@1 | +0.029 | [-0.057, +0.114] | 1.000 | 2/1 |
| ig:llm/llm:sbert | ctx:sbert | ndcg@10 | +0.009 | [-0.034, +0.051] | 0.707 | 13/7 |
| ig:llm/llm:sbert | ctx:sbert | mrr | -0.003 | [-0.093, +0.088] | 0.948 | 4/6 |
| ig:llm/llm:sbert | ctx:sbert | useful@1 | +0.029 | [-0.114, +0.171] | 1.000 | 3/2 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | ndcg@10 | +0.018 | [-0.026, +0.061] | 0.423 | 20/8 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | mrr | -0.001 | [-0.092, +0.090] | 0.987 | 5/6 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | useful@1 | +0.029 | [-0.114, +0.171] | 1.000 | 3/2 |
