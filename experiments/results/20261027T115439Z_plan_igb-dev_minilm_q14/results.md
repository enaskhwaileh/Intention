# IGBench results (20261027T115439Z_plan_igb-dev_minilm_q14)

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
| rerank:llmig:sbert | 0.823 | 0.531 | 0.317 | 0.869 | 0.920 | 0.886 | 0.057 |
| rerank:llmgold:sbert | 0.822 | 0.537 | 0.320 | 0.845 | 0.917 | 0.886 | 0.086 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:sbert | 0.768 | 0.450 | 0.823 | 0.719 |
| ig:llm/llm:sbert | 0.788 | 0.475 | 0.846 | 0.781 |
| ig:llm/llm:sbert+repair=1 | 0.792 | 0.487 | 0.843 | 0.781 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.788 | 0.487 | 0.826 | 0.750 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.757 | 0.444 | 0.803 | 0.719 |
| rerank:llm:sbert | 0.833 | 0.519 | 0.959 | 0.938 |
| rerank:llmig:sbert | 0.825 | 0.506 | 0.912 | 0.875 |
| rerank:llmgold:sbert | 0.823 | 0.512 | 0.910 | 0.875 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:sbert | 0.286 | 0.728 | 0.840 |
| ig:llm/llm:sbert | 0.301 | 0.728 | 0.858 |
| ig:llm/llm:sbert+repair=1 | 0.301 | 0.741 | 0.873 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.298 | 0.746 | 0.850 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.289 | 0.708 | 0.837 |
| rerank:llm:sbert | 0.379 | 0.797 | 0.870 |
| rerank:llmig:sbert | 0.372 | 0.790 | 0.869 |
| rerank:llmgold:sbert | 0.337 | 0.761 | 0.845 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | aggregate (n=3) | compare (n=10) | explain (n=7) | monitor (n=5) | predict (n=8) |
|---|---|---|---|---|---|
| ctx:sbert | 0.966 | 0.762 | 0.808 | 0.673 | 0.730 |
| ig:llm/llm:sbert | 0.965 | 0.817 | 0.844 | 0.673 | 0.711 |
| ig:llm/llm:sbert+repair=1 | 0.966 | 0.817 | 0.850 | 0.695 | 0.711 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.982 | 0.789 | 0.842 | 0.663 | 0.748 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.984 | 0.770 | 0.786 | 0.651 | 0.706 |
| rerank:llm:sbert | 0.967 | 0.801 | 0.851 | 0.757 | 0.805 |
| rerank:llmig:sbert | 0.982 | 0.799 | 0.880 | 0.732 | 0.767 |
| rerank:llmgold:sbert | 0.977 | 0.799 | 0.866 | 0.735 | 0.771 |

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
| rerank:llmig:sbert | 0.832 |
| rerank:llmgold:sbert | 0.763 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:llm/llm:sbert | 0.778 | 0.779 | 0.920 | 0.639 | 0.594 | 0.594 | 0.578 | 0.406 | 0.495 | 0.712 |
| ig:llm/llm:sbert+repair=1 | 1.000 | 0.746 | 0.909 | 0.806 | 0.781 | 0.781 | 0.703 | 0.219 | 0.515 | 0.745 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 1.000 | 0.746 | 0.909 | 0.806 | 0.781 | 0.781 | 0.703 | 0.219 | 0.515 | 0.745 |
| ig:llm/llm:sbert+repair=1+align=0 | 1.000 | 0.746 | 0.909 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | – | – |
| rerank:llmig:sbert | 1.000 | 0.746 | 0.909 | 0.806 | 0.781 | 0.781 | 0.703 | 0.000 | – | – |
| rerank:llmgold:sbert | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | – | – |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:sbert | – | 83.5 / 72.2 / 79.6 | – | – | – | – | 83.5 / 72.2 / 79.6 | 3.007 |
| ig:llm/llm:sbert | 7.2 / 5.9 / 11.7 | 73.4 / 72.4 / 77.8 | 1.6 / 1.2 / 4.0 | 24.7 / 19.7 / 44.8 | 642.7 / 49.8 / 4021.0 | 0.2 / 0.1 / 0.5 | 677.1 / 92.0 / 4050.3 | 12.099 |
| ig:llm/llm:sbert+repair=1 | 7.0 / 6.6 / 13.2 | 73.9 / 72.6 / 78.5 | 1.9 / 1.4 / 4.6 | 27.2 / 20.8 / 40.2 | 813.2 / 103.1 / 4150.1 | 0.1 / 0.1 / 0.4 | 850.4 / 134.7 / 4178.5 | 16.848 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 7.0 / 5.6 / 16.7 | 72.8 / 72.1 / 74.4 | 1.9 / 1.3 / 4.5 | 18.1 / 21.3 / 37.6 | 799.7 / 102.4 / 4046.7 | 0.1 / 0.1 / 0.2 | 827.8 / 131.5 / 4077.7 | 16.364 |
| ig:llm/llm:sbert+repair=1+align=0 | 8.1 / 7.7 / 15.1 | 72.7 / 73.1 / 76.6 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.4 / 0.4 / 0.7 | 8.5 / 8.3 / 15.5 | 3.091 |
| rerank:llm:sbert | – | 751.1 / 736.3 / 1036.4 | – | – | – | – | 765.5 / 740.3 / 1049.7 | 1.877 |
| rerank:llmig:sbert | 57.4 / 8.4 / 340.2 | 622.9 / 669.8 / 1873.0 | 18.8 / 6.1 / 65.3 | 759.5 / 66.5 / 3130.3 | 8080.1 / 604.6 / 31762.0 | 0.1 / 0.1 / 0.3 | 41139.1 / 40004.8 / 60091.4 | 102.033 |
| rerank:llmgold:sbert | 0.2 / 0.2 / 0.2 | 911.1 / 660.5 / 5759.8 | 0.2 / 0.2 / 0.5 | 938.0 / 196.1 / 3670.0 | 9734.1 / 856.3 / 31170.4 | 0.2 / 0.1 / 0.3 | 45236.7 / 48543.2 / 81752.6 | 118.02 |

Context index build (one-off, ms): sbert: 11577 (cached)

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
