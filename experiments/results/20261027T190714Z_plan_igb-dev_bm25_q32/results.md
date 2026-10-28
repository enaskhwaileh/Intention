# IGBench results (20261027T190714Z_plan_igb-dev_bm25_q32)

Benchmark `igbench-v1` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:bm25 | 0.768 | 0.486 | 0.323 | 0.851 | 0.895 | 0.800 | 0.143 |
| ig:llm/llm:bm25 | 0.773 | 0.509 | 0.331 | 0.870 | 0.874 | 0.771 | 0.143 |
| ig:llm/llm:bm25+repair=1 | 0.784 | 0.537 | 0.334 | 0.873 | 0.888 | 0.800 | 0.114 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.797 | 0.537 | 0.340 | 0.885 | 0.909 | 0.829 | 0.114 |
| ig:llm/llm:bm25+repair=1+align=0 | 0.777 | 0.503 | 0.331 | 0.871 | 0.895 | 0.800 | 0.143 |
| ig:gold/llm:bm25+repair=1 | 0.791 | 0.531 | 0.334 | 0.882 | 0.869 | 0.771 | 0.143 |
| ig:llm/index:bm25+repair=1 | 0.783 | 0.531 | 0.331 | 0.866 | 0.893 | 0.800 | 0.114 |
| rerank:llm:bm25 | 0.817 | 0.577 | 0.337 | 0.888 | 0.924 | 0.857 | 0.114 |
| rerank:llmig:bm25 | 0.811 | 0.554 | 0.343 | 0.900 | 0.967 | 0.943 | 0.029 |
| rerank:llmgold:bm25 | 0.799 | 0.543 | 0.323 | 0.863 | 0.912 | 0.857 | 0.086 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:bm25 | 0.779 | 0.469 | 0.917 | 0.844 |
| ig:llm/llm:bm25 | 0.784 | 0.494 | 0.893 | 0.812 |
| ig:llm/llm:bm25+repair=1 | 0.796 | 0.525 | 0.909 | 0.844 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.811 | 0.525 | 0.932 | 0.875 |
| ig:llm/llm:bm25+repair=1+align=0 | 0.789 | 0.487 | 0.917 | 0.844 |
| ig:gold/llm:bm25+repair=1 | 0.803 | 0.519 | 0.888 | 0.812 |
| ig:llm/index:bm25+repair=1 | 0.795 | 0.519 | 0.914 | 0.844 |
| rerank:llm:bm25 | 0.822 | 0.562 | 0.932 | 0.875 |
| rerank:llmig:bm25 | 0.816 | 0.531 | 0.979 | 0.969 |
| rerank:llmgold:bm25 | 0.803 | 0.519 | 0.919 | 0.875 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:bm25 | 0.306 | 0.711 | 0.851 |
| ig:llm/llm:bm25 | 0.302 | 0.745 | 0.870 |
| ig:llm/llm:bm25+repair=1 | 0.316 | 0.781 | 0.873 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.321 | 0.772 | 0.885 |
| ig:llm/llm:bm25+repair=1+align=0 | 0.306 | 0.734 | 0.871 |
| ig:gold/llm:bm25+repair=1 | 0.311 | 0.772 | 0.882 |
| ig:llm/index:bm25+repair=1 | 0.316 | 0.774 | 0.866 |
| rerank:llm:bm25 | 0.349 | 0.815 | 0.888 |
| rerank:llmig:bm25 | 0.379 | 0.790 | 0.900 |
| rerank:llmgold:bm25 | 0.360 | 0.795 | 0.863 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | aggregate (n=3) | compare (n=10) | explain (n=7) | monitor (n=5) | predict (n=8) |
|---|---|---|---|---|---|
| ctx:bm25 | 0.939 | 0.804 | 0.775 | 0.668 | 0.773 |
| ig:llm/llm:bm25 | 0.939 | 0.806 | 0.799 | 0.718 | 0.739 |
| ig:llm/llm:bm25+repair=1 | 0.948 | 0.813 | 0.836 | 0.726 | 0.739 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.948 | 0.815 | 0.845 | 0.717 | 0.792 |
| ig:llm/llm:bm25+repair=1+align=0 | 0.948 | 0.803 | 0.791 | 0.697 | 0.779 |
| ig:gold/llm:bm25+repair=1 | 0.964 | 0.848 | 0.827 | 0.730 | 0.724 |
| ig:llm/index:bm25+repair=1 | 0.948 | 0.821 | 0.809 | 0.715 | 0.756 |
| rerank:llm:bm25 | 0.939 | 0.821 | 0.849 | 0.755 | 0.810 |
| rerank:llmig:bm25 | 0.948 | 0.841 | 0.819 | 0.743 | 0.786 |
| rerank:llmgold:bm25 | 0.960 | 0.856 | 0.805 | 0.757 | 0.716 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:bm25 | 0.803 |
| ig:llm/llm:bm25 | 0.806 |
| ig:llm/llm:bm25+repair=1 | 0.822 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.818 |
| ig:llm/llm:bm25+repair=1+align=0 | 0.810 |
| ig:gold/llm:bm25+repair=1 | 0.830 |
| ig:llm/index:bm25+repair=1 | 0.842 |
| rerank:llm:bm25 | 0.837 |
| rerank:llmig:bm25 | 0.836 |
| rerank:llmgold:bm25 | 0.860 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:llm/llm:bm25 | 0.750 | 0.853 | 0.958 | 0.556 | 0.531 | 0.500 | 0.516 | 0.469 | 0.537 | 0.689 |
| ig:llm/llm:bm25+repair=1 | 0.944 | 0.774 | 0.935 | 0.750 | 0.719 | 0.688 | 0.630 | 0.281 | 0.590 | 0.734 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.944 | 0.774 | 0.935 | 0.750 | 0.719 | 0.688 | 0.630 | 0.281 | 0.590 | 0.734 |
| ig:llm/llm:bm25+repair=1+align=0 | 0.944 | 0.774 | 0.935 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | – | – |
| ig:gold/llm:bm25+repair=1 | 1.000 | 1.000 | 1.000 | 0.917 | 0.938 | 0.906 | 0.938 | 0.062 | 0.497 | 0.765 |
| ig:llm/index:bm25+repair=1 | 0.944 | 0.774 | 0.935 | 0.667 | 0.625 | 0.625 | 0.599 | 0.375 | 0.529 | 0.714 |
| rerank:llmig:bm25 | 0.944 | 0.774 | 0.935 | 0.750 | 0.719 | 0.688 | 0.630 | 0.000 | – | – |
| rerank:llmgold:bm25 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | – | – |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:bm25 | – | 5.2 / 5.1 / 7.4 | – | – | – | – | 5.3 / 5.2 / 7.5 | 0.192 |
| ig:llm/llm:bm25 | 2.2 / 2.2 / 3.0 | 4.6 / 4.4 / 6.8 | 1.2 / 1.0 / 3.2 | 14.1 / 0.0 / 34.1 | 890.0 / 0.0 / 4542.5 | 0.2 / 0.1 / 0.7 | 908.3 / 6.3 / 4579.2 | 15.178 |
| ig:llm/llm:bm25+repair=1 | 3.0 / 2.6 / 5.1 | 5.2 / 4.4 / 8.1 | 1.4 / 0.9 / 3.7 | 15.8 / 16.7 / 31.0 | 1011.0 / 72.1 / 4368.4 | 0.1 / 0.1 / 0.3 | 1032.0 / 97.3 / 4397.5 | 15.791 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 3.0 / 2.5 / 5.1 | 4.5 / 4.2 / 6.9 | 1.4 / 1.0 / 3.7 | 16.8 / 16.7 / 71.1 | 993.0 / 81.0 / 4294.0 | 0.1 / 0.1 / 0.2 | 1015.0 / 130.3 / 4324.5 | 15.347 |
| ig:llm/llm:bm25+repair=1+align=0 | 2.9 / 2.5 / 4.8 | 5.4 / 4.2 / 7.6 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.5 / 0.4 / 1.2 | 3.4 / 3.1 / 5.6 | 0.265 |
| ig:gold/llm:bm25+repair=1 | 0.1 / 0.1 / 0.2 | 3.7 / 3.3 / 5.6 | 1.6 / 1.3 / 4.0 | 22.2 / 20.7 / 64.0 | 1220.5 / 310.3 / 4512.5 | 0.1 / 0.1 / 0.2 | 1245.5 / 366.1 / 4543.4 | 16.754 |
| ig:llm/index:bm25+repair=1 | 3.0 / 2.8 / 4.9 | 5.4 / 4.5 / 7.4 | 0.8 / 0.3 / 4.6 | 13.4 / 16.3 / 28.6 | 759.3 / 61.2 / 4334.1 | 0.1 / 0.1 / 0.4 | 777.3 / 84.6 / 4364.0 | 13.014 |
| rerank:llm:bm25 | – | 21.1 / 18.7 / 40.7 | – | – | – | – | 56.4 / 57.6 / 89.8 | 0.542 |
| rerank:llmig:bm25 | 6.0 / 1.6 / 26.5 | 12.8 / 12.8 / 18.2 | 5.0 / 1.5 / 18.1 | 39.7 / 23.3 / 172.0 | 1850.2 / 86.0 / 8075.7 | 0.1 / 0.1 / 0.2 | 28217.6 / 31348.0 / 42815.6 | 262.566 |
| rerank:llmgold:bm25 | 0.2 / 0.2 / 0.2 | 14.1 / 12.1 / 26.5 | 0.2 / 0.2 / 0.4 | 105.6 / 28.2 / 361.3 | 2339.3 / 431.7 / 9058.4 | 0.1 / 0.1 / 0.1 | 28918.6 / 37390.7 / 43410.9 | 275.174 |

Context index build (one-off, ms): bm25: 58 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:llm/llm:bm25+repair=1+align=0 | ctx:bm25 | ndcg@10 | +0.009 | [+0.002, +0.019] | 0.027 | 8/3 |
| ig:llm/llm:bm25+repair=1+align=0 | ctx:bm25 | mrr | +0.000 | [+0.000, +0.000] | 1.000 | 0/0 |
| ig:llm/llm:bm25+repair=1+align=0 | ctx:bm25 | useful@1 | +0.000 | [+0.000, +0.000] | 1.000 | 0/0 |
| ig:llm/llm:bm25 | ctx:bm25 | ndcg@10 | +0.004 | [-0.018, +0.027] | 0.708 | 8/7 |
| ig:llm/llm:bm25 | ctx:bm25 | mrr | -0.021 | [-0.064, +0.000] | 1.000 | 0/1 |
| ig:llm/llm:bm25 | ctx:bm25 | useful@1 | -0.029 | [-0.086, +0.000] | 1.000 | 0/1 |
| ig:llm/index:bm25+repair=1 | ctx:bm25 | ndcg@10 | +0.015 | [-0.010, +0.038] | 0.260 | 14/7 |
| ig:llm/index:bm25+repair=1 | ctx:bm25 | mrr | -0.002 | [-0.059, +0.043] | 1.000 | 2/1 |
| ig:llm/index:bm25+repair=1 | ctx:bm25 | useful@1 | +0.000 | [-0.086, +0.086] | 1.000 | 1/1 |
| ig:gold/llm:bm25+repair=1 | ctx:bm25 | ndcg@10 | +0.022 | [-0.002, +0.048] | 0.100 | 19/10 |
| ig:gold/llm:bm25+repair=1 | ctx:bm25 | mrr | -0.026 | [-0.090, +0.029] | 0.503 | 1/3 |
| ig:gold/llm:bm25+repair=1 | ctx:bm25 | useful@1 | -0.029 | [-0.143, +0.057] | 1.000 | 1/2 |
| ig:llm/llm:bm25+repair=1 | ctx:bm25 | ndcg@10 | +0.015 | [-0.009, +0.040] | 0.238 | 14/8 |
| ig:llm/llm:bm25+repair=1 | ctx:bm25 | mrr | -0.007 | [-0.064, +0.043] | 1.000 | 1/1 |
| ig:llm/llm:bm25+repair=1 | ctx:bm25 | useful@1 | +0.000 | [-0.086, +0.086] | 1.000 | 1/1 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | ctx:bm25 | ndcg@10 | +0.028 | [+0.014, +0.046] | 0.000 | 15/7 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | ctx:bm25 | mrr | +0.014 | [+0.000, +0.043] | 1.000 | 1/0 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | ctx:bm25 | useful@1 | +0.029 | [+0.000, +0.086] | 1.000 | 1/0 |
