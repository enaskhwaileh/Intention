# IGBench results (20261027T192950Z_plan_igb-test_bm25_q32)

Benchmark `igbench-v1-test` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:bm25 | 0.828 | 0.530 | 0.345 | 0.935 | 0.917 | 0.850 | 0.100 |
| ig:llm/llm:bm25 | 0.824 | 0.530 | 0.345 | 0.927 | 0.925 | 0.850 | 0.050 |
| ig:llm/llm:bm25+repair=1 | 0.832 | 0.540 | 0.345 | 0.927 | 0.950 | 0.900 | 0.050 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.836 | 0.520 | 0.345 | 0.927 | 0.950 | 0.900 | 0.050 |
| ig:llm/llm:bm25+repair=1+align=0 | 0.829 | 0.530 | 0.340 | 0.923 | 0.917 | 0.850 | 0.150 |
| ig:gold/llm:bm25+repair=1 | 0.852 | 0.550 | 0.350 | 0.940 | 0.975 | 0.950 | 0.000 |
| ig:llm/index:bm25+repair=1 | 0.826 | 0.540 | 0.350 | 0.936 | 0.925 | 0.850 | 0.100 |
| rerank:llm:bm25 | 0.873 | 0.590 | 0.360 | 0.957 | 0.975 | 0.950 | 0.000 |
| rerank:llmig:bm25 | 0.842 | 0.550 | 0.355 | 0.952 | 0.960 | 0.950 | 0.000 |
| rerank:llmgold:bm25 | 0.851 | 0.560 | 0.355 | 0.956 | 0.963 | 0.950 | 0.000 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:bm25 | 0.823 | 0.516 | 0.912 | 0.842 |
| ig:llm/llm:bm25 | 0.832 | 0.526 | 0.947 | 0.895 |
| ig:llm/llm:bm25+repair=1 | 0.840 | 0.537 | 0.974 | 0.947 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.844 | 0.516 | 0.974 | 0.947 |
| ig:llm/llm:bm25+repair=1+align=0 | 0.837 | 0.526 | 0.939 | 0.895 |
| ig:gold/llm:bm25+repair=1 | 0.849 | 0.537 | 0.974 | 0.947 |
| ig:llm/index:bm25+repair=1 | 0.834 | 0.537 | 0.947 | 0.895 |
| rerank:llm:bm25 | 0.871 | 0.579 | 0.974 | 0.947 |
| rerank:llmig:bm25 | 0.838 | 0.537 | 0.958 | 0.947 |
| rerank:llmgold:bm25 | 0.849 | 0.547 | 0.961 | 0.947 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:bm25 | 0.414 | 0.810 | 0.935 |
| ig:llm/llm:bm25 | 0.374 | 0.808 | 0.927 |
| ig:llm/llm:bm25+repair=1 | 0.383 | 0.816 | 0.927 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.383 | 0.794 | 0.927 |
| ig:llm/llm:bm25+repair=1+align=0 | 0.410 | 0.806 | 0.923 |
| ig:gold/llm:bm25+repair=1 | 0.395 | 0.829 | 0.940 |
| ig:llm/index:bm25+repair=1 | 0.333 | 0.816 | 0.936 |
| rerank:llm:bm25 | 0.432 | 0.867 | 0.957 |
| rerank:llmig:bm25 | 0.395 | 0.827 | 0.952 |
| rerank:llmgold:bm25 | 0.395 | 0.841 | 0.956 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | compare (n=8) | explain (n=3) | monitor (n=5) | predict (n=4) |
|---|---|---|---|---|
| ctx:bm25 | 0.812 | 0.800 | 0.750 | 0.909 |
| ig:llm/llm:bm25 | 0.791 | 0.800 | 0.808 | 0.918 |
| ig:llm/llm:bm25+repair=1 | 0.793 | 0.790 | 0.842 | 0.918 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.790 | 0.802 | 0.856 | 0.917 |
| ig:llm/llm:bm25+repair=1+align=0 | 0.812 | 0.802 | 0.802 | 0.909 |
| ig:gold/llm:bm25+repair=1 | 0.793 | 0.833 | 0.849 | 0.918 |
| ig:llm/index:bm25+repair=1 | 0.804 | 0.787 | 0.842 | 0.867 |
| rerank:llm:bm25 | 0.913 | 0.816 | 0.820 | 0.925 |
| rerank:llmig:bm25 | 0.840 | 0.807 | 0.863 | 0.867 |
| rerank:llmgold:bm25 | 0.821 | 0.826 | 0.887 | 0.914 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:bm25 | 0.871 |
| ig:llm/llm:bm25 | 0.879 |
| ig:llm/llm:bm25+repair=1 | 0.879 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.879 |
| ig:llm/llm:bm25+repair=1+align=0 | 0.871 |
| ig:gold/llm:bm25+repair=1 | 0.879 |
| ig:llm/index:bm25+repair=1 | 0.882 |
| rerank:llm:bm25 | 0.882 |
| rerank:llmig:bm25 | 0.882 |
| rerank:llmgold:bm25 | 0.882 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:llm/llm:bm25 | 0.762 | 0.931 | 0.911 | 0.714 | 0.684 | 0.684 | 0.623 | 0.316 | 0.618 | 0.809 |
| ig:llm/llm:bm25+repair=1 | 0.952 | 0.840 | 0.930 | 0.905 | 0.895 | 0.895 | 0.728 | 0.105 | 0.630 | 0.767 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.952 | 0.840 | 0.930 | 0.905 | 0.895 | 0.895 | 0.728 | 0.105 | 0.630 | 0.767 |
| ig:llm/llm:bm25+repair=1+align=0 | 0.952 | 0.840 | 0.930 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | – | – |
| ig:gold/llm:bm25+repair=1 | 1.000 | 1.000 | 1.000 | 0.952 | 0.947 | 0.947 | 0.947 | 0.053 | 0.580 | 0.785 |
| ig:llm/index:bm25+repair=1 | 0.952 | 0.840 | 0.930 | 0.905 | 0.895 | 0.842 | 0.781 | 0.105 | 0.638 | 0.710 |
| rerank:llmig:bm25 | 0.952 | 0.840 | 0.930 | 0.905 | 0.895 | 0.895 | 0.728 | 0.000 | – | – |
| rerank:llmgold:bm25 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | – | – |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:bm25 | – | 5.5 / 5.4 / 6.7 | – | – | – | – | 5.6 / 5.6 / 6.9 | 0.118 |
| ig:llm/llm:bm25 | 2.5 / 2.6 / 3.0 | 4.4 / 4.5 / 6.6 | 1.4 / 1.1 / 3.5 | 17.6 / 20.0 / 33.9 | 293.2 / 87.4 / 843.0 | 0.2 / 0.1 / 0.1 | 315.6 / 114.8 / 880.5 | 2.043 |
| ig:llm/llm:bm25+repair=1 | 3.1 / 2.6 / 5.6 | 4.4 / 4.5 / 6.5 | 1.7 / 1.3 / 3.6 | 27.6 / 17.9 / 64.1 | 329.1 / 234.5 / 716.8 | 0.1 / 0.1 / 0.1 | 362.4 / 256.9 / 861.6 | 2.643 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 2.9 / 2.4 / 4.9 | 4.5 / 4.6 / 6.7 | 1.6 / 0.9 / 3.7 | 25.5 / 17.4 / 74.3 | 331.9 / 251.3 / 724.4 | 0.1 / 0.1 / 0.1 | 362.8 / 274.4 / 806.1 | 2.738 |
| ig:llm/llm:bm25+repair=1+align=0 | 3.0 / 2.4 / 5.4 | 5.7 / 5.0 / 6.6 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.6 / 0.5 / 1.3 | 3.7 / 3.1 / 6.0 | 0.172 |
| ig:gold/llm:bm25+repair=1 | 0.1 / 0.1 / 0.1 | 3.7 / 3.1 / 6.2 | 1.8 / 1.1 / 3.8 | 22.5 / 19.5 / 32.2 | 288.2 / 167.5 / 610.7 | 0.1 / 0.1 / 0.1 | 313.6 / 189.6 / 642.6 | 2.435 |
| ig:llm/index:bm25+repair=1 | 3.0 / 2.6 / 4.9 | 4.5 / 4.6 / 6.6 | 1.3 / 0.3 / 5.0 | 20.0 / 18.3 / 26.9 | 320.3 / 227.8 / 773.3 | 0.1 / 0.1 / 0.1 | 345.5 / 249.7 / 804.9 | 2.785 |
| rerank:llm:bm25 | – | 23.7 / 20.1 / 36.7 | – | – | – | – | 61.9 / 63.4 / 82.9 | 0.361 |
| rerank:llmig:bm25 | 5.6 / 1.5 / 16.6 | 14.2 / 13.0 / 21.8 | 3.4 / 1.2 / 14.2 | 28.0 / 22.9 / 70.9 | 312.1 / 206.6 / 607.5 | 0.1 / 0.1 / 0.1 | 35099.9 / 37490.2 / 45384.2 | 199.586 |
| rerank:llmgold:bm25 | 0.2 / 0.2 / 0.2 | 14.4 / 13.8 / 20.4 | 0.2 / 0.2 / 0.3 | 50.4 / 24.6 / 142.4 | 280.4 / 166.8 / 543.4 | 0.1 / 0.1 / 0.2 | 34360.4 / 38767.4 / 43245.2 | 194.569 |

Context index build (one-off, ms): bm25: 57 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:llm/llm:bm25+repair=1+align=0 | ctx:bm25 | ndcg@10 | +0.001 | [-0.034, +0.032] | 0.888 | 4/3 |
| ig:llm/llm:bm25+repair=1+align=0 | ctx:bm25 | mrr | +0.000 | [-0.075, +0.075] | 1.000 | 1/1 |
| ig:llm/llm:bm25+repair=1+align=0 | ctx:bm25 | useful@1 | +0.000 | [-0.150, +0.150] | 1.000 | 1/1 |
| ig:llm/llm:bm25 | ctx:bm25 | ndcg@10 | -0.004 | [-0.050, +0.036] | 0.886 | 6/5 |
| ig:llm/llm:bm25 | ctx:bm25 | mrr | +0.008 | [-0.100, +0.125] | 1.000 | 2/2 |
| ig:llm/llm:bm25 | ctx:bm25 | useful@1 | +0.000 | [-0.200, +0.200] | 1.000 | 2/2 |
| ig:llm/index:bm25+repair=1 | ctx:bm25 | ndcg@10 | -0.003 | [-0.055, +0.045] | 0.924 | 10/6 |
| ig:llm/index:bm25+repair=1 | ctx:bm25 | mrr | +0.008 | [-0.125, +0.150] | 1.000 | 3/3 |
| ig:llm/index:bm25+repair=1 | ctx:bm25 | useful@1 | +0.000 | [-0.250, +0.250] | 1.000 | 3/3 |
| ig:gold/llm:bm25+repair=1 | ctx:bm25 | ndcg@10 | +0.023 | [-0.021, +0.063] | 0.327 | 10/6 |
| ig:gold/llm:bm25+repair=1 | ctx:bm25 | mrr | +0.058 | [-0.042, +0.175] | 0.498 | 3/1 |
| ig:gold/llm:bm25+repair=1 | ctx:bm25 | useful@1 | +0.100 | [-0.100, +0.300] | 0.625 | 3/1 |
| ig:llm/llm:bm25+repair=1 | ctx:bm25 | ndcg@10 | +0.003 | [-0.045, +0.047] | 0.899 | 9/6 |
| ig:llm/llm:bm25+repair=1 | ctx:bm25 | mrr | +0.033 | [-0.075, +0.158] | 0.745 | 3/2 |
| ig:llm/llm:bm25+repair=1 | ctx:bm25 | useful@1 | +0.050 | [-0.150, +0.300] | 1.000 | 3/2 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | ctx:bm25 | ndcg@10 | +0.007 | [-0.041, +0.050] | 0.782 | 9/6 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | ctx:bm25 | mrr | +0.033 | [-0.075, +0.158] | 0.745 | 3/2 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | ctx:bm25 | useful@1 | +0.050 | [-0.150, +0.300] | 1.000 | 3/2 |
