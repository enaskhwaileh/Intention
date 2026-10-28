# IGBench results (20261027T114847Z_plan_igb-dev_bm25_q14)

Benchmark `igbench-v1` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:bm25 | 0.768 | 0.486 | 0.323 | 0.851 | 0.895 | 0.800 | 0.143 |
| ig:llm/llm:bm25 | 0.774 | 0.514 | 0.329 | 0.851 | 0.888 | 0.800 | 0.114 |
| ig:llm/llm:bm25+repair=1 | 0.783 | 0.531 | 0.331 | 0.866 | 0.888 | 0.800 | 0.114 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.797 | 0.531 | 0.337 | 0.878 | 0.909 | 0.829 | 0.114 |
| ig:llm/llm:bm25+repair=1+align=0 | 0.778 | 0.503 | 0.331 | 0.871 | 0.895 | 0.800 | 0.143 |
| ig:gold/llm:bm25+repair=1 | 0.791 | 0.531 | 0.334 | 0.882 | 0.874 | 0.771 | 0.143 |
| ig:llm/index:bm25+repair=1 | 0.780 | 0.531 | 0.331 | 0.866 | 0.879 | 0.771 | 0.143 |
| rerank:llm:bm25 | 0.819 | 0.537 | 0.343 | 0.894 | 0.948 | 0.914 | 0.057 |
| rerank:llmig:bm25 | 0.805 | 0.520 | 0.337 | 0.884 | 0.936 | 0.914 | 0.029 |
| rerank:llmgold:bm25 | 0.804 | 0.526 | 0.331 | 0.877 | 0.907 | 0.857 | 0.086 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:bm25 | 0.779 | 0.469 | 0.917 | 0.844 |
| ig:llm/llm:bm25 | 0.785 | 0.500 | 0.909 | 0.844 |
| ig:llm/llm:bm25+repair=1 | 0.795 | 0.519 | 0.909 | 0.844 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.810 | 0.519 | 0.932 | 0.875 |
| ig:llm/llm:bm25+repair=1+align=0 | 0.789 | 0.487 | 0.917 | 0.844 |
| ig:gold/llm:bm25+repair=1 | 0.804 | 0.519 | 0.893 | 0.812 |
| ig:llm/index:bm25+repair=1 | 0.792 | 0.519 | 0.898 | 0.812 |
| rerank:llm:bm25 | 0.827 | 0.531 | 0.969 | 0.938 |
| rerank:llmig:bm25 | 0.811 | 0.512 | 0.957 | 0.938 |
| rerank:llmgold:bm25 | 0.810 | 0.519 | 0.925 | 0.875 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:bm25 | 0.306 | 0.711 | 0.851 |
| ig:llm/llm:bm25 | 0.316 | 0.747 | 0.851 |
| ig:llm/llm:bm25+repair=1 | 0.316 | 0.774 | 0.866 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.321 | 0.764 | 0.878 |
| ig:llm/llm:bm25+repair=1+align=0 | 0.306 | 0.734 | 0.871 |
| ig:gold/llm:bm25+repair=1 | 0.311 | 0.772 | 0.882 |
| ig:llm/index:bm25+repair=1 | 0.302 | 0.774 | 0.866 |
| rerank:llm:bm25 | 0.365 | 0.778 | 0.894 |
| rerank:llmig:bm25 | 0.374 | 0.766 | 0.884 |
| rerank:llmgold:bm25 | 0.360 | 0.780 | 0.877 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | aggregate (n=3) | compare (n=10) | explain (n=7) | monitor (n=5) | predict (n=8) |
|---|---|---|---|---|---|
| ctx:bm25 | 0.939 | 0.804 | 0.775 | 0.668 | 0.773 |
| ig:llm/llm:bm25 | 0.937 | 0.814 | 0.809 | 0.668 | 0.756 |
| ig:llm/llm:bm25+repair=1 | 0.946 | 0.814 | 0.810 | 0.725 | 0.756 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.947 | 0.821 | 0.821 | 0.717 | 0.805 |
| ig:llm/llm:bm25+repair=1+align=0 | 0.948 | 0.803 | 0.791 | 0.699 | 0.779 |
| ig:gold/llm:bm25+repair=1 | 0.964 | 0.838 | 0.827 | 0.728 | 0.741 |
| ig:llm/index:bm25+repair=1 | 0.946 | 0.811 | 0.791 | 0.714 | 0.756 |
| rerank:llm:bm25 | 0.939 | 0.839 | 0.830 | 0.754 | 0.821 |
| rerank:llmig:bm25 | 0.947 | 0.852 | 0.814 | 0.743 | 0.758 |
| rerank:llmgold:bm25 | 0.964 | 0.854 | 0.831 | 0.749 | 0.726 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:bm25 | 0.803 |
| ig:llm/llm:bm25 | 0.820 |
| ig:llm/llm:bm25+repair=1 | 0.822 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.817 |
| ig:llm/llm:bm25+repair=1+align=0 | 0.810 |
| ig:gold/llm:bm25+repair=1 | 0.840 |
| ig:llm/index:bm25+repair=1 | 0.837 |
| rerank:llm:bm25 | 0.851 |
| rerank:llmig:bm25 | 0.857 |
| rerank:llmgold:bm25 | 0.861 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:llm/llm:bm25 | 0.778 | 0.779 | 0.920 | 0.639 | 0.594 | 0.594 | 0.578 | 0.406 | 0.512 | 0.747 |
| ig:llm/llm:bm25+repair=1 | 1.000 | 0.746 | 0.909 | 0.806 | 0.781 | 0.781 | 0.703 | 0.219 | 0.510 | 0.770 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 1.000 | 0.746 | 0.909 | 0.806 | 0.781 | 0.781 | 0.703 | 0.219 | 0.510 | 0.770 |
| ig:llm/llm:bm25+repair=1+align=0 | 1.000 | 0.746 | 0.909 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | – | – |
| ig:gold/llm:bm25+repair=1 | 1.000 | 1.000 | 1.000 | 0.917 | 0.938 | 0.938 | 0.938 | 0.062 | 0.492 | 0.781 |
| ig:llm/index:bm25+repair=1 | 1.000 | 0.746 | 0.909 | 0.778 | 0.781 | 0.781 | 0.714 | 0.219 | 0.540 | 0.765 |
| rerank:llmig:bm25 | 1.000 | 0.746 | 0.909 | 0.806 | 0.781 | 0.781 | 0.703 | 0.000 | – | – |
| rerank:llmgold:bm25 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | – | – |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:bm25 | – | 5.6 / 5.2 / 7.6 | – | – | – | – | 5.8 / 5.3 / 7.7 | 0.207 |
| ig:llm/llm:bm25 | 6.2 / 6.0 / 10.1 | 4.7 / 4.8 / 7.1 | 1.9 / 1.6 / 4.6 | 16.4 / 19.3 / 34.6 | 854.9 / 71.7 / 4563.7 | 0.2 / 0.1 / 0.8 | 880.5 / 104.1 / 4598.8 | 11.4 |
| ig:llm/llm:bm25+repair=1 | 7.5 / 6.7 / 14.8 | 5.7 / 4.8 / 7.7 | 2.4 / 1.7 / 6.1 | 21.8 / 20.8 / 35.8 | 1088.7 / 219.7 / 4439.8 | 0.2 / 0.1 / 0.4 | 1122.0 / 256.4 / 4566.3 | 15.599 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 7.8 / 5.7 / 19.3 | 5.0 / 4.7 / 7.6 | 2.1 / 1.5 / 5.6 | 37.9 / 20.5 / 133.3 | 1118.1 / 143.8 / 4764.5 | 0.2 / 0.1 / 0.3 | 1167.3 / 174.4 / 4792.2 | 15.999 |
| ig:llm/llm:bm25+repair=1+align=0 | 8.6 / 8.4 / 16.5 | 7.6 / 6.1 / 10.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.7 / 0.6 / 1.3 | 9.4 / 9.0 / 17.1 | 0.405 |
| ig:gold/llm:bm25+repair=1 | 0.2 / 0.1 / 0.2 | 4.5 / 3.9 / 7.2 | 2.6 / 1.8 / 6.5 | 36.7 / 28.0 / 129.1 | 1176.2 / 462.4 / 4614.7 | 0.2 / 0.2 / 0.5 | 1217.6 / 600.3 / 4643.1 | 15.961 |
| ig:llm/index:bm25+repair=1 | 7.4 / 6.8 / 13.0 | 8.4 / 5.6 / 8.3 | 2.2 / 0.9 / 7.4 | 26.5 / 23.5 / 38.8 | 1477.9 / 360.8 / 5202.9 | 0.3 / 0.2 / 0.7 | 1515.7 / 411.2 / 5254.0 | 20.574 |
| rerank:llm:bm25 | – | 57.7 / 45.9 / 151.5 | – | – | – | – | 165.2 / 137.3 / 286.5 | 0.646 |
| rerank:llmig:bm25 | 32.1 / 22.2 / 98.0 | 18.7 / 14.7 / 47.4 | 23.3 / 10.7 / 75.3 | 182.1 / 45.0 / 566.5 | 8427.7 / 549.9 / 29086.2 | 0.2 / 0.2 / 0.5 | 59064.1 / 57440.5 / 84149.3 | 144.866 |
| rerank:llmgold:bm25 | 0.2 / 0.1 / 0.3 | 26.4 / 26.7 / 54.3 | 0.3 / 0.3 / 0.6 | 406.5 / 348.4 / 936.9 | 13089.1 / 2004.4 / 36546.5 | 0.7 / 0.1 / 0.7 | 43978.9 / 42690.1 / 78083.3 | 110.173 |

Context index build (one-off, ms): bm25: 71 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:llm/llm:bm25+repair=1+align=0 | ctx:bm25 | ndcg@10 | +0.009 | [+0.002, +0.019] | 0.019 | 9/3 |
| ig:llm/llm:bm25+repair=1+align=0 | ctx:bm25 | mrr | +0.000 | [+0.000, +0.000] | 1.000 | 0/0 |
| ig:llm/llm:bm25+repair=1+align=0 | ctx:bm25 | useful@1 | +0.000 | [+0.000, +0.000] | 1.000 | 0/0 |
| ig:llm/llm:bm25 | ctx:bm25 | ndcg@10 | +0.005 | [-0.015, +0.023] | 0.636 | 11/7 |
| ig:llm/llm:bm25 | ctx:bm25 | mrr | -0.007 | [-0.064, +0.043] | 1.000 | 1/1 |
| ig:llm/llm:bm25 | ctx:bm25 | useful@1 | +0.000 | [-0.086, +0.086] | 1.000 | 1/1 |
| ig:llm/index:bm25+repair=1 | ctx:bm25 | ndcg@10 | +0.008 | [-0.014, +0.031] | 0.515 | 15/10 |
| ig:llm/index:bm25+repair=1 | ctx:bm25 | mrr | -0.017 | [-0.064, +0.014] | 1.000 | 1/1 |
| ig:llm/index:bm25+repair=1 | ctx:bm25 | useful@1 | -0.029 | [-0.086, +0.000] | 1.000 | 0/1 |
| ig:gold/llm:bm25+repair=1 | ctx:bm25 | ndcg@10 | +0.023 | [-0.002, +0.048] | 0.086 | 20/9 |
| ig:gold/llm:bm25+repair=1 | ctx:bm25 | mrr | -0.021 | [-0.086, +0.029] | 0.750 | 1/2 |
| ig:gold/llm:bm25+repair=1 | ctx:bm25 | useful@1 | -0.029 | [-0.143, +0.057] | 1.000 | 1/2 |
| ig:llm/llm:bm25+repair=1 | ctx:bm25 | ndcg@10 | +0.014 | [-0.009, +0.037] | 0.266 | 15/9 |
| ig:llm/llm:bm25+repair=1 | ctx:bm25 | mrr | -0.007 | [-0.064, +0.043] | 1.000 | 1/1 |
| ig:llm/llm:bm25+repair=1 | ctx:bm25 | useful@1 | +0.000 | [-0.086, +0.086] | 1.000 | 1/1 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | ctx:bm25 | ndcg@10 | +0.028 | [+0.013, +0.045] | 0.000 | 17/7 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | ctx:bm25 | mrr | +0.014 | [+0.000, +0.043] | 1.000 | 1/0 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | ctx:bm25 | useful@1 | +0.029 | [+0.000, +0.086] | 1.000 | 1/0 |
