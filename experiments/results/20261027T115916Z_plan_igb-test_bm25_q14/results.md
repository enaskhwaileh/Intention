# IGBench results (20261027T115916Z_plan_igb-test_bm25_q14)

Benchmark `igbench-v1-test` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:bm25 | 0.828 | 0.530 | 0.345 | 0.935 | 0.917 | 0.850 | 0.100 |
| ig:llm/llm:bm25 | 0.807 | 0.530 | 0.345 | 0.927 | 0.867 | 0.750 | 0.100 |
| ig:llm/llm:bm25+repair=1 | 0.831 | 0.540 | 0.350 | 0.936 | 0.925 | 0.850 | 0.050 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.831 | 0.530 | 0.345 | 0.927 | 0.925 | 0.850 | 0.050 |
| ig:llm/llm:bm25+repair=1+align=0 | 0.825 | 0.530 | 0.340 | 0.923 | 0.892 | 0.800 | 0.150 |
| ig:gold/llm:bm25+repair=1 | 0.855 | 0.550 | 0.355 | 0.948 | 0.975 | 0.950 | 0.000 |
| ig:llm/index:bm25+repair=1 | 0.820 | 0.550 | 0.350 | 0.936 | 0.900 | 0.800 | 0.100 |
| rerank:llm:bm25 | 0.862 | 0.560 | 0.345 | 0.939 | 1.000 | 1.000 | 0.000 |
| rerank:llmig:bm25 | 0.832 | 0.540 | 0.350 | 0.944 | 0.935 | 0.900 | 0.000 |
| rerank:llmgold:bm25 | 0.839 | 0.550 | 0.350 | 0.944 | 0.967 | 0.950 | 0.000 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:bm25 | 0.823 | 0.516 | 0.912 | 0.842 |
| ig:llm/llm:bm25 | 0.814 | 0.526 | 0.886 | 0.789 |
| ig:llm/llm:bm25+repair=1 | 0.839 | 0.537 | 0.947 | 0.895 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.839 | 0.526 | 0.947 | 0.895 |
| ig:llm/llm:bm25+repair=1+align=0 | 0.833 | 0.526 | 0.912 | 0.842 |
| ig:gold/llm:bm25+repair=1 | 0.852 | 0.537 | 0.974 | 0.947 |
| ig:llm/index:bm25+repair=1 | 0.828 | 0.547 | 0.921 | 0.842 |
| rerank:llm:bm25 | 0.863 | 0.547 | 1.000 | 1.000 |
| rerank:llmig:bm25 | 0.827 | 0.526 | 0.932 | 0.895 |
| rerank:llmgold:bm25 | 0.838 | 0.537 | 0.965 | 0.947 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:bm25 | 0.414 | 0.810 | 0.935 |
| ig:llm/llm:bm25 | 0.352 | 0.808 | 0.927 |
| ig:llm/llm:bm25+repair=1 | 0.372 | 0.816 | 0.936 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.372 | 0.802 | 0.927 |
| ig:llm/llm:bm25+repair=1+align=0 | 0.400 | 0.806 | 0.923 |
| ig:gold/llm:bm25+repair=1 | 0.395 | 0.829 | 0.948 |
| ig:llm/index:bm25+repair=1 | 0.323 | 0.829 | 0.936 |
| rerank:llm:bm25 | 0.445 | 0.839 | 0.939 |
| rerank:llmig:bm25 | 0.385 | 0.816 | 0.944 |
| rerank:llmgold:bm25 | 0.395 | 0.829 | 0.944 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | compare (n=8) | explain (n=3) | monitor (n=5) | predict (n=4) |
|---|---|---|---|---|
| ctx:bm25 | 0.812 | 0.800 | 0.750 | 0.909 |
| ig:llm/llm:bm25 | 0.793 | 0.766 | 0.760 | 0.918 |
| ig:llm/llm:bm25+repair=1 | 0.804 | 0.766 | 0.835 | 0.918 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.794 | 0.778 | 0.844 | 0.917 |
| ig:llm/llm:bm25+repair=1+align=0 | 0.812 | 0.770 | 0.802 | 0.909 |
| ig:gold/llm:bm25+repair=1 | 0.805 | 0.833 | 0.841 | 0.918 |
| ig:llm/index:bm25+repair=1 | 0.804 | 0.770 | 0.831 | 0.867 |
| rerank:llm:bm25 | 0.881 | 0.817 | 0.839 | 0.910 |
| rerank:llmig:bm25 | 0.799 | 0.778 | 0.843 | 0.911 |
| rerank:llmgold:bm25 | 0.810 | 0.807 | 0.851 | 0.912 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:bm25 | 0.871 |
| ig:llm/llm:bm25 | 0.879 |
| ig:llm/llm:bm25+repair=1 | 0.882 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.882 |
| ig:llm/llm:bm25+repair=1+align=0 | 0.871 |
| ig:gold/llm:bm25+repair=1 | 0.882 |
| ig:llm/index:bm25+repair=1 | 0.882 |
| rerank:llm:bm25 | 0.879 |
| rerank:llmig:bm25 | 0.882 |
| rerank:llmgold:bm25 | 0.882 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:llm/llm:bm25 | 0.857 | 0.774 | 0.980 | 0.714 | 0.684 | 0.684 | 0.588 | 0.316 | 0.585 | 0.775 |
| ig:llm/llm:bm25+repair=1 | 1.000 | 0.788 | 0.933 | 0.905 | 0.895 | 0.895 | 0.781 | 0.105 | 0.584 | 0.682 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 1.000 | 0.788 | 0.933 | 0.905 | 0.895 | 0.895 | 0.781 | 0.105 | 0.584 | 0.682 |
| ig:llm/llm:bm25+repair=1+align=0 | 1.000 | 0.788 | 0.933 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | – | – |
| ig:gold/llm:bm25+repair=1 | 1.000 | 1.000 | 1.000 | 0.952 | 0.947 | 0.947 | 0.947 | 0.053 | 0.576 | 0.757 |
| ig:llm/index:bm25+repair=1 | 1.000 | 0.788 | 0.933 | 0.857 | 0.842 | 0.789 | 0.763 | 0.158 | 0.629 | 0.672 |
| rerank:llmig:bm25 | 1.000 | 0.788 | 0.933 | 0.905 | 0.895 | 0.895 | 0.781 | 0.000 | – | – |
| rerank:llmgold:bm25 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | – | – |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:bm25 | – | 5.9 / 5.6 / 6.9 | – | – | – | – | 6.0 / 5.7 / 7.0 | 0.126 |
| ig:llm/llm:bm25 | 4.5 / 4.3 / 6.2 | 4.5 / 5.0 / 6.9 | 2.2 / 1.6 / 5.5 | 26.9 / 21.1 / 62.6 | 340.2 / 102.4 / 895.2 | 0.3 / 0.1 / 0.5 | 374.8 / 129.9 / 989.7 | 2.42 |
| ig:llm/llm:bm25+repair=1 | 5.4 / 4.9 / 7.9 | 5.0 / 4.8 / 7.1 | 2.2 / 1.1 / 5.4 | 35.1 / 18.7 / 149.7 | 355.0 / 259.8 / 729.4 | 0.1 / 0.1 / 0.1 | 398.7 / 282.4 / 852.1 | 2.925 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 6.2 / 5.3 / 10.6 | 7.2 / 5.0 / 9.0 | 2.2 / 1.2 / 5.5 | 18.6 / 20.5 / 27.9 | 404.3 / 324.1 / 818.0 | 0.2 / 0.2 / 0.2 | 432.6 / 355.0 / 859.2 | 3.257 |
| ig:llm/llm:bm25+repair=1+align=0 | 4.6 / 4.6 / 6.4 | 7.2 / 5.2 / 6.9 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.7 / 0.6 / 1.3 | 5.4 / 5.1 / 7.0 | 0.242 |
| ig:gold/llm:bm25+repair=1 | 0.1 / 0.1 / 0.1 | 4.0 / 3.6 / 6.5 | 2.3 / 1.2 / 5.5 | 26.4 / 23.2 / 63.7 | 365.6 / 174.4 / 698.6 | 0.1 / 0.1 / 0.2 | 395.7 / 245.5 / 731.3 | 2.95 |
| ig:llm/index:bm25+repair=1 | 5.5 / 4.6 / 10.4 | 5.0 / 5.0 / 7.0 | 2.1 / 0.3 / 6.8 | 30.4 / 18.8 / 86.0 | 352.7 / 263.3 / 753.4 | 0.1 / 0.1 / 0.2 | 391.9 / 318.4 / 790.3 | 2.827 |
| rerank:llm:bm25 | – | 72.0 / 58.7 / 140.9 | – | – | – | – | 159.1 / 135.7 / 303.7 | 0.429 |
| rerank:llmig:bm25 | 56.8 / 48.2 / 117.2 | 30.3 / 22.6 / 69.9 | 47.5 / 43.0 / 100.1 | 400.4 / 517.0 / 728.1 | 3036.9 / 3539.9 / 6171.2 | 0.4 / 0.2 / 0.3 | 31201.5 / 33924.5 / 40531.5 | 55.454 |
| rerank:llmgold:bm25 | 0.2 / 0.2 / 0.2 | 29.7 / 22.1 / 85.2 | 0.3 / 0.3 / 0.3 | 763.2 / 910.5 / 1041.8 | 4227.1 / 4036.9 / 7755.4 | 0.2 / 0.2 / 0.3 | 31733.2 / 29273.9 / 43984.3 | 54.156 |

Context index build (one-off, ms): bm25: 60 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:llm/llm:bm25+repair=1+align=0 | ctx:bm25 | ndcg@10 | -0.003 | [-0.038, +0.028] | 0.828 | 4/4 |
| ig:llm/llm:bm25+repair=1+align=0 | ctx:bm25 | mrr | -0.025 | [-0.100, +0.050] | 1.000 | 1/2 |
| ig:llm/llm:bm25+repair=1+align=0 | ctx:bm25 | useful@1 | -0.050 | [-0.200, +0.100] | 1.000 | 1/2 |
| ig:llm/llm:bm25 | ctx:bm25 | ndcg@10 | -0.020 | [-0.061, +0.015] | 0.377 | 7/7 |
| ig:llm/llm:bm25 | ctx:bm25 | mrr | -0.050 | [-0.150, +0.050] | 0.626 | 1/3 |
| ig:llm/llm:bm25 | ctx:bm25 | useful@1 | -0.100 | [-0.300, +0.100] | 0.626 | 1/3 |
| ig:llm/index:bm25+repair=1 | ctx:bm25 | ndcg@10 | -0.007 | [-0.060, +0.040] | 0.783 | 10/6 |
| ig:llm/index:bm25+repair=1 | ctx:bm25 | mrr | -0.017 | [-0.150, +0.125] | 1.000 | 3/4 |
| ig:llm/index:bm25+repair=1 | ctx:bm25 | useful@1 | -0.050 | [-0.300, +0.200] | 1.000 | 3/4 |
| ig:gold/llm:bm25+repair=1 | ctx:bm25 | ndcg@10 | +0.025 | [-0.019, +0.065] | 0.277 | 11/5 |
| ig:gold/llm:bm25+repair=1 | ctx:bm25 | mrr | +0.058 | [-0.042, +0.175] | 0.498 | 3/1 |
| ig:gold/llm:bm25+repair=1 | ctx:bm25 | useful@1 | +0.100 | [-0.100, +0.300] | 0.625 | 3/1 |
| ig:llm/llm:bm25+repair=1 | ctx:bm25 | ndcg@10 | +0.002 | [-0.048, +0.045] | 0.928 | 10/6 |
| ig:llm/llm:bm25+repair=1 | ctx:bm25 | mrr | +0.008 | [-0.125, +0.142] | 1.000 | 3/3 |
| ig:llm/llm:bm25+repair=1 | ctx:bm25 | useful@1 | +0.000 | [-0.250, +0.250] | 1.000 | 3/3 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | ctx:bm25 | ndcg@10 | +0.002 | [-0.046, +0.044] | 0.923 | 10/6 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | ctx:bm25 | mrr | +0.008 | [-0.125, +0.142] | 1.000 | 3/3 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | ctx:bm25 | useful@1 | +0.000 | [-0.250, +0.250] | 1.000 | 3/3 |
