# IGBench results (20261025T180537Z_plan_igb-test_bm25_q32)

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

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:llm/llm:bm25 | 0.762 | 0.931 | 0.911 | 0.714 | 0.684 | 0.684 | 0.623 | 0.316 | 0.618 | 0.809 |
| ig:llm/llm:bm25+repair=1 | 0.952 | 0.840 | 0.930 | 0.905 | 0.895 | 0.895 | 0.728 | 0.105 | 0.630 | 0.767 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.952 | 0.840 | 0.930 | 0.905 | 0.895 | 0.895 | 0.728 | 0.105 | 0.630 | 0.767 |
| ig:llm/llm:bm25+repair=1+align=0 | 0.952 | 0.840 | 0.930 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | – | – |
| ig:gold/llm:bm25+repair=1 | 1.000 | 1.000 | 1.000 | 0.952 | 0.947 | 0.947 | 0.947 | 0.053 | 0.580 | 0.785 |
| ig:llm/index:bm25+repair=1 | 0.952 | 0.840 | 0.930 | 0.905 | 0.895 | 0.842 | 0.781 | 0.105 | 0.638 | 0.710 |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:bm25 | – | 5.5 / 5.4 / 6.8 | – | – | – | – | 5.6 / 5.5 / 7.0 | 0.118 |
| ig:llm/llm:bm25 | 5.5 / 5.3 / 7.7 | 4.6 / 4.6 / 6.9 | 2.2 / 1.6 / 5.8 | 21.1 / 23.2 / 36.2 | 360.4 / 130.7 / 874.0 | 0.2 / 0.1 / 0.3 | 390.2 / 200.7 / 916.5 | 2.143 |
| ig:llm/llm:bm25+repair=1 | 2359.1 / 8.0 / 9582.1 | 4.9 / 4.5 / 6.7 | 307.0 / 1.8 / 5.4 | 26.6 / 21.5 / 56.8 | 383.3 / 290.3 / 746.2 | 0.1 / 0.1 / 0.1 | 3077.1 / 664.4 / 10049.4 | 19.54 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 5.7 / 5.5 / 9.6 | 6.5 / 4.6 / 6.8 | 2.0 / 1.0 / 5.3 | 17.3 / 18.5 / 27.8 | 382.6 / 266.1 / 747.0 | 0.1 / 0.1 / 0.1 | 408.8 / 291.5 / 788.3 | 2.76 |
| ig:llm/llm:bm25+repair=1+align=0 | 5.3 / 5.1 / 9.0 | 6.7 / 5.1 / 7.6 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.7 / 0.5 / 1.3 | 6.1 / 5.7 / 10.1 | 0.219 |
| ig:gold/llm:bm25+repair=1 | 0.1 / 0.1 / 0.1 | 3.8 / 3.2 / 6.3 | 2.7 / 1.8 / 5.4 | 26.6 / 23.4 / 51.9 | 331.6 / 235.1 / 633.8 | 0.1 / 0.1 / 0.1 | 362.0 / 269.3 / 663.7 | 2.439 |
| ig:llm/index:bm25+repair=1 | 5.1 / 4.1 / 7.7 | 4.9 / 4.6 / 6.7 | 2.0 / 0.3 / 6.7 | 29.7 / 17.7 / 24.9 | 384.9 / 253.3 / 814.8 | 0.1 / 0.1 / 0.1 | 422.7 / 276.1 / 849.6 | 2.771 |
| rerank:llm:bm25 | – | 37.8 / 27.7 / 76.0 | – | – | – | – | 43679.5 / 45378.9 / 68808.0 | 70.043 |

Context index build (one-off, ms): bm25: 55 (cached)

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
