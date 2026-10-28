# IGBench results (20261025T091715Z_srv_test_llm31_q32)

Benchmark `igbench-v1-test` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:bm25 | 0.828 | 0.530 | 0.345 | 0.935 | 0.917 | 0.850 | 0.100 |
| ctx:tfidf | 0.775 | 0.460 | 0.315 | 0.882 | 0.765 | 0.600 | 0.300 |
| ctx:sbert | 0.690 | 0.340 | 0.270 | 0.780 | 0.814 | 0.700 | 0.150 |
| ctx:hybrid | 0.845 | 0.560 | 0.335 | 0.907 | 0.950 | 0.900 | 0.050 |
| ig:llm/llm:bm25 | 0.824 | 0.530 | 0.345 | 0.927 | 0.925 | 0.850 | 0.050 |
| ig:llm/llm:bm25+repair=1 | 0.827 | 0.540 | 0.345 | 0.927 | 0.925 | 0.850 | 0.050 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.831 | 0.520 | 0.345 | 0.927 | 0.925 | 0.850 | 0.050 |
| ig:llm/llm:tfidf | 0.785 | 0.490 | 0.310 | 0.870 | 0.850 | 0.750 | 0.150 |
| ig:llm/llm:tfidf+repair=1 | 0.800 | 0.490 | 0.320 | 0.888 | 0.875 | 0.800 | 0.100 |
| ig:llm/llm:tfidf+repair=1+rnorm=minmax | 0.791 | 0.490 | 0.315 | 0.878 | 0.850 | 0.750 | 0.150 |
| ig:llm/llm:sbert | 0.699 | 0.430 | 0.280 | 0.801 | 0.852 | 0.750 | 0.050 |
| ig:llm/llm:sbert+repair=1 | 0.741 | 0.490 | 0.300 | 0.846 | 0.877 | 0.800 | 0.050 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.740 | 0.420 | 0.285 | 0.821 | 0.910 | 0.850 | 0.050 |
| ig:llm/llm:hybrid | 0.820 | 0.550 | 0.325 | 0.890 | 0.925 | 0.850 | 0.050 |
| ig:llm/llm:hybrid+repair=1 | 0.833 | 0.540 | 0.340 | 0.923 | 0.925 | 0.850 | 0.050 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | 0.864 | 0.530 | 0.345 | 0.927 | 0.950 | 0.900 | 0.050 |
| ig:gold/llm:bm25 | 0.852 | 0.550 | 0.350 | 0.940 | 0.975 | 0.950 | 0.000 |
| ig:llm/index:bm25+repair=1 | 0.821 | 0.540 | 0.350 | 0.936 | 0.900 | 0.800 | 0.100 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:bm25 | 0.823 | 0.516 | 0.912 | 0.842 |
| ctx:tfidf | 0.770 | 0.442 | 0.752 | 0.579 |
| ctx:sbert | 0.680 | 0.316 | 0.804 | 0.684 |
| ctx:hybrid | 0.839 | 0.547 | 0.947 | 0.895 |
| ig:llm/llm:bm25 | 0.832 | 0.526 | 0.947 | 0.895 |
| ig:llm/llm:bm25+repair=1 | 0.835 | 0.537 | 0.947 | 0.895 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.839 | 0.516 | 0.947 | 0.895 |
| ig:llm/llm:tfidf | 0.794 | 0.484 | 0.868 | 0.789 |
| ig:llm/llm:tfidf+repair=1 | 0.809 | 0.484 | 0.895 | 0.842 |
| ig:llm/llm:tfidf+repair=1+rnorm=minmax | 0.800 | 0.484 | 0.868 | 0.789 |
| ig:llm/llm:sbert | 0.710 | 0.432 | 0.870 | 0.789 |
| ig:llm/llm:sbert+repair=1 | 0.755 | 0.495 | 0.896 | 0.842 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.753 | 0.421 | 0.932 | 0.895 |
| ig:llm/llm:hybrid | 0.827 | 0.547 | 0.947 | 0.895 |
| ig:llm/llm:hybrid+repair=1 | 0.841 | 0.537 | 0.947 | 0.895 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | 0.873 | 0.526 | 0.974 | 0.947 |
| ig:gold/llm:bm25 | 0.849 | 0.537 | 0.974 | 0.947 |
| ig:llm/index:bm25+repair=1 | 0.829 | 0.537 | 0.921 | 0.842 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:bm25 | 0.414 | 0.810 | 0.935 |
| ctx:tfidf | 0.340 | 0.736 | 0.882 |
| ctx:sbert | 0.352 | 0.591 | 0.780 |
| ctx:hybrid | 0.424 | 0.833 | 0.907 |
| ig:llm/llm:bm25 | 0.374 | 0.808 | 0.927 |
| ig:llm/llm:bm25+repair=1 | 0.372 | 0.816 | 0.927 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.372 | 0.794 | 0.927 |
| ig:llm/llm:tfidf | 0.356 | 0.765 | 0.870 |
| ig:llm/llm:tfidf+repair=1 | 0.364 | 0.761 | 0.888 |
| ig:llm/llm:tfidf+repair=1+rnorm=minmax | 0.356 | 0.765 | 0.878 |
| ig:llm/llm:sbert | 0.312 | 0.701 | 0.801 |
| ig:llm/llm:sbert+repair=1 | 0.324 | 0.768 | 0.846 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.399 | 0.676 | 0.821 |
| ig:llm/llm:hybrid | 0.374 | 0.824 | 0.890 |
| ig:llm/llm:hybrid+repair=1 | 0.374 | 0.812 | 0.923 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | 0.424 | 0.802 | 0.927 |
| ig:gold/llm:bm25 | 0.395 | 0.829 | 0.940 |
| ig:llm/index:bm25+repair=1 | 0.323 | 0.816 | 0.936 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | compare (n=8) | explain (n=3) | monitor (n=5) | predict (n=4) |
|---|---|---|---|---|
| ctx:bm25 | 0.812 | 0.800 | 0.750 | 0.909 |
| ctx:tfidf | 0.738 | 0.729 | 0.772 | 0.864 |
| ctx:sbert | 0.665 | 0.675 | 0.683 | 0.756 |
| ctx:hybrid | 0.847 | 0.763 | 0.809 | 0.918 |
| ig:llm/llm:bm25 | 0.791 | 0.800 | 0.808 | 0.918 |
| ig:llm/llm:bm25+repair=1 | 0.793 | 0.758 | 0.842 | 0.918 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.790 | 0.770 | 0.856 | 0.917 |
| ig:llm/llm:tfidf | 0.739 | 0.729 | 0.834 | 0.897 |
| ig:llm/llm:tfidf+repair=1 | 0.742 | 0.755 | 0.873 | 0.897 |
| ig:llm/llm:tfidf+repair=1+rnorm=minmax | 0.740 | 0.728 | 0.862 | 0.891 |
| ig:llm/llm:sbert | 0.701 | 0.675 | 0.697 | 0.825 |
| ig:llm/llm:sbert+repair=1 | 0.758 | 0.814 | 0.691 | 0.825 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.750 | 0.714 | 0.734 | 0.856 |
| ig:llm/llm:hybrid | 0.778 | 0.763 | 0.861 | 0.906 |
| ig:llm/llm:hybrid+repair=1 | 0.793 | 0.817 | 0.854 | 0.906 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | 0.840 | 0.837 | 0.882 | 0.917 |
| ig:gold/llm:bm25 | 0.793 | 0.833 | 0.849 | 0.918 |
| ig:llm/index:bm25+repair=1 | 0.804 | 0.755 | 0.842 | 0.867 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:bm25 | 0.871 |
| ctx:tfidf | 0.862 |
| ctx:sbert | 0.824 |
| ctx:hybrid | 0.860 |
| ig:llm/llm:bm25 | 0.879 |
| ig:llm/llm:bm25+repair=1 | 0.879 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.879 |
| ig:llm/llm:tfidf | 0.882 |
| ig:llm/llm:tfidf+repair=1 | 0.882 |
| ig:llm/llm:tfidf+repair=1+rnorm=minmax | 0.882 |
| ig:llm/llm:sbert | 0.869 |
| ig:llm/llm:sbert+repair=1 | 0.922 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.900 |
| ig:llm/llm:hybrid | 0.879 |
| ig:llm/llm:hybrid+repair=1 | 0.879 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | 0.879 |
| ig:gold/llm:bm25 | 0.879 |
| ig:llm/index:bm25+repair=1 | 0.882 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:llm/llm:bm25 | 0.762 | 0.931 | 0.911 | 0.714 | 0.684 | 0.684 | 0.623 | 0.316 | 0.618 | 0.809 |
| ig:llm/llm:bm25+repair=1 | 0.952 | 0.840 | 0.930 | 0.905 | 0.895 | 0.895 | 0.728 | 0.105 | 0.630 | 0.767 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.952 | 0.840 | 0.930 | 0.905 | 0.895 | 0.895 | 0.728 | 0.105 | 0.630 | 0.767 |
| ig:llm/llm:tfidf | 0.762 | 0.931 | 0.911 | 0.714 | 0.684 | 0.684 | 0.623 | 0.316 | 0.630 | 0.809 |
| ig:llm/llm:tfidf+repair=1 | 0.952 | 0.840 | 0.930 | 0.905 | 0.895 | 0.895 | 0.728 | 0.105 | 0.639 | 0.767 |
| ig:llm/llm:tfidf+repair=1+rnorm=minmax | 0.952 | 0.840 | 0.930 | 0.905 | 0.895 | 0.895 | 0.728 | 0.105 | 0.639 | 0.767 |
| ig:llm/llm:sbert | 0.762 | 0.931 | 0.911 | 0.714 | 0.684 | 0.684 | 0.623 | 0.316 | 0.673 | 0.805 |
| ig:llm/llm:sbert+repair=1 | 0.952 | 0.840 | 0.930 | 0.905 | 0.895 | 0.895 | 0.728 | 0.105 | 0.708 | 0.793 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.952 | 0.840 | 0.930 | 0.905 | 0.895 | 0.895 | 0.728 | 0.105 | 0.708 | 0.793 |
| ig:llm/llm:hybrid | 0.762 | 0.931 | 0.911 | 0.714 | 0.684 | 0.684 | 0.623 | 0.316 | 0.630 | 0.829 |
| ig:llm/llm:hybrid+repair=1 | 0.952 | 0.840 | 0.930 | 0.905 | 0.895 | 0.895 | 0.728 | 0.105 | 0.639 | 0.780 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | 0.952 | 0.840 | 0.930 | 0.905 | 0.895 | 0.895 | 0.728 | 0.105 | 0.639 | 0.780 |
| ig:gold/llm:bm25 | 1.000 | 1.000 | 1.000 | 0.952 | 0.947 | 0.947 | 0.947 | 0.053 | 0.580 | 0.785 |
| ig:llm/index:bm25+repair=1 | 0.952 | 0.840 | 0.930 | 0.905 | 0.895 | 0.842 | 0.781 | 0.105 | 0.638 | 0.710 |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:bm25 | – | 5.2 / 5.4 / 7.0 | – | – | – | – | 5.3 / 5.5 / 7.2 | 0.112 |
| ctx:tfidf | – | 4.8 / 4.2 / 4.8 | – | – | – | – | 5.0 / 4.4 / 4.9 | 0.105 |
| ctx:sbert | – | 97.0 / 80.8 / 151.9 | – | – | – | – | 97.1 / 80.8 / 151.9 | 2.039 |
| ctx:hybrid | – | 85.5 / 86.6 / 90.9 | – | – | – | – | 85.6 / 86.8 / 91.0 | 1.798 |
| ig:llm/llm:bm25 | 16122.3 / 18611.9 / 21228.3 | 8.7 / 9.0 / 13.0 | 8461.9 / 7833.9 / 18498.3 | 20.8 / 30.8 / 37.0 | 202.2 / 123.8 / 505.8 | 0.2 / 0.1 / 0.3 | 24808.4 / 22863.4 / 37088.9 | 66.084 |
| ig:llm/llm:bm25+repair=1 | 2449.1 / 5.4 / 9992.8 | 8.1 / 8.2 / 12.4 | 1755.2 / 2.0 / 7184.9 | 35.5 / 20.8 / 37.4 | 329.1 / 251.9 / 660.0 | 0.1 / 0.1 / 0.1 | 4570.0 / 536.4 / 17293.0 | 28.783 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 7.0 / 6.2 / 10.9 | 5.1 / 4.8 / 6.9 | 2.4 / 1.4 / 5.9 | 17.1 / 18.4 / 27.2 | 238.4 / 141.7 / 508.5 | 0.1 / 0.1 / 0.1 | 265.9 / 178.4 / 533.1 | 2.48 |
| ig:llm/llm:tfidf | 4.0 / 4.3 / 5.5 | 4.6 / 4.4 / 4.8 | 1.9 / 1.0 / 5.8 | 13.1 / 16.0 / 26.5 | 141.1 / 93.8 / 203.9 | 0.2 / 0.1 / 0.1 | 161.1 / 122.8 / 242.5 | 1.649 |
| ig:llm/llm:tfidf+repair=1 | 5.9 / 4.8 / 10.9 | 4.4 / 4.2 / 4.7 | 2.0 / 1.0 / 4.6 | 15.9 / 17.5 / 24.2 | 175.6 / 125.5 / 283.1 | 0.1 / 0.1 / 0.1 | 200.4 / 161.5 / 314.8 | 2.165 |
| ig:llm/llm:tfidf+repair=1+rnorm=minmax | 5.7 / 4.6 / 8.9 | 4.7 / 4.4 / 5.1 | 2.1 / 1.0 / 5.8 | 66.3 / 17.8 / 319.4 | 218.1 / 154.1 / 547.2 | 0.1 / 0.1 / 0.1 | 293.3 / 198.6 / 593.1 | 2.504 |
| ig:llm/llm:sbert | 4.0 / 3.6 / 6.1 | 75.3 / 74.2 / 76.8 | 1.5 / 0.7 / 3.6 | 15.8 / 19.9 / 29.5 | 150.7 / 98.5 / 323.5 | 0.1 / 0.1 / 0.1 | 173.0 / 125.8 / 349.6 | 3.044 |
| ig:llm/llm:sbert+repair=1 | 7.1 / 6.6 / 10.7 | 85.4 / 76.7 / 86.7 | 2.1 / 1.1 / 5.4 | 19.0 / 19.2 / 31.1 | 291.7 / 119.4 / 826.2 | 0.1 / 0.1 / 0.1 | 321.1 / 157.5 / 870.8 | 5.684 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 22.2 / 20.7 / 37.7 | 133.7 / 142.3 / 186.9 | 1.9 / 1.0 / 2.7 | 25.7 / 20.6 / 48.8 | 275.7 / 195.8 / 808.3 | 0.1 / 0.1 / 0.3 | 327.0 / 246.7 / 875.1 | 6.143 |
| ig:llm/llm:hybrid | 4.3 / 4.0 / 5.6 | 86.8 / 84.7 / 97.6 | 2.2 / 1.0 / 5.0 | 65.1 / 22.6 / 365.6 | 234.0 / 104.5 / 608.8 | 0.2 / 0.1 / 0.1 | 306.6 / 152.8 / 992.8 | 3.988 |
| ig:llm/llm:hybrid+repair=1 | 8.2 / 7.4 / 14.9 | 86.7 / 89.3 / 92.8 | 2.2 / 1.0 / 6.0 | 16.9 / 18.2 / 26.1 | 275.1 / 137.8 / 958.9 | 0.1 / 0.1 / 0.1 | 303.5 / 168.9 / 997.5 | 4.829 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | 6.9 / 5.6 / 12.0 | 92.0 / 91.0 / 99.0 | 2.2 / 1.0 / 6.3 | 19.2 / 20.2 / 28.6 | 277.3 / 139.9 / 958.9 | 0.1 / 0.1 / 0.1 | 306.8 / 177.7 / 998.9 | 5.008 |
| ig:gold/llm:bm25 | 0.1 / 0.1 / 0.1 | 4.2 / 3.4 / 6.3 | 6371.2 / 7825.5 / 10745.2 | 30.2 / 35.5 / 41.2 | 194.9 / 115.6 / 364.8 | 0.1 / 0.1 / 0.1 | 6597.8 / 8035.5 / 11308.5 | 34.543 |
| ig:llm/index:bm25+repair=1 | 7.5 / 6.7 / 13.2 | 5.0 / 4.8 / 7.0 | 2.3 / 0.6 / 7.5 | 71.4 / 23.4 / 350.5 | 263.2 / 217.6 / 467.9 | 0.1 / 0.1 / 0.1 | 345.4 / 273.4 / 750.7 | 3.014 |

Context index build (one-off, ms): bm25: 51 (cached), hybrid: 12626 (cached), sbert: 969 (cached), tfidf: 18 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:llm/llm:hybrid+repair=1 | ctx:hybrid | ndcg@10 | -0.018 | [-0.065, +0.027] | 0.487 | 8/10 |
| ig:llm/llm:hybrid+repair=1 | ctx:hybrid | mrr | -0.025 | [-0.100, +0.050] | 1.000 | 1/2 |
| ig:llm/llm:hybrid+repair=1 | ctx:hybrid | useful@1 | -0.050 | [-0.200, +0.100] | 1.000 | 1/2 |
| ig:llm/llm:bm25 | ctx:bm25 | ndcg@10 | -0.004 | [-0.050, +0.036] | 0.886 | 6/5 |
| ig:llm/llm:bm25 | ctx:bm25 | mrr | +0.008 | [-0.100, +0.125] | 1.000 | 2/2 |
| ig:llm/llm:bm25 | ctx:bm25 | useful@1 | +0.000 | [-0.200, +0.200] | 1.000 | 2/2 |
| ig:llm/llm:hybrid | ctx:hybrid | ndcg@10 | -0.030 | [-0.073, +0.008] | 0.212 | 5/8 |
| ig:llm/llm:hybrid | ctx:hybrid | mrr | -0.025 | [-0.100, +0.050] | 1.000 | 1/2 |
| ig:llm/llm:hybrid | ctx:hybrid | useful@1 | -0.050 | [-0.200, +0.100] | 1.000 | 1/2 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | ndcg@10 | +0.050 | [-0.015, +0.106] | 0.135 | 11/6 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | mrr | +0.096 | [-0.017, +0.217] | 0.244 | 4/1 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | useful@1 | +0.150 | [-0.050, +0.350] | 0.370 | 4/1 |
| ig:llm/llm:tfidf | ctx:tfidf | ndcg@10 | +0.009 | [-0.041, +0.054] | 0.725 | 7/5 |
| ig:llm/llm:tfidf | ctx:tfidf | mrr | +0.085 | [-0.048, +0.217] | 0.242 | 6/2 |
| ig:llm/llm:tfidf | ctx:tfidf | useful@1 | +0.150 | [-0.100, +0.400] | 0.455 | 5/2 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | ctx:hybrid | ndcg@10 | +0.012 | [-0.031, +0.050] | 0.569 | 6/9 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | ctx:hybrid | mrr | +0.000 | [-0.075, +0.075] | 1.000 | 1/1 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | ctx:hybrid | useful@1 | +0.000 | [-0.150, +0.150] | 1.000 | 1/1 |
| ig:llm/index:bm25+repair=1 | ctx:bm25 | ndcg@10 | -0.007 | [-0.060, +0.042] | 0.799 | 10/7 |
| ig:llm/index:bm25+repair=1 | ctx:bm25 | mrr | -0.017 | [-0.150, +0.125] | 1.000 | 3/4 |
| ig:llm/index:bm25+repair=1 | ctx:bm25 | useful@1 | -0.050 | [-0.300, +0.200] | 1.000 | 3/4 |
| ig:llm/llm:sbert | ctx:sbert | ndcg@10 | +0.011 | [-0.068, +0.082] | 0.791 | 11/3 |
| ig:llm/llm:sbert | ctx:sbert | mrr | +0.037 | [-0.108, +0.192] | 0.705 | 4/3 |
| ig:llm/llm:sbert | ctx:sbert | useful@1 | +0.050 | [-0.200, +0.300] | 1.000 | 4/3 |
| ig:llm/llm:tfidf+repair=1 | ctx:tfidf | ndcg@10 | +0.023 | [-0.029, +0.071] | 0.399 | 10/6 |
| ig:llm/llm:tfidf+repair=1 | ctx:tfidf | mrr | +0.110 | [-0.023, +0.246] | 0.152 | 7/2 |
| ig:llm/llm:tfidf+repair=1 | ctx:tfidf | useful@1 | +0.200 | [-0.050, +0.450] | 0.297 | 6/2 |
| ig:llm/llm:bm25+repair=1 | ctx:bm25 | ndcg@10 | -0.001 | [-0.051, +0.043] | 0.958 | 9/7 |
| ig:llm/llm:bm25+repair=1 | ctx:bm25 | mrr | +0.008 | [-0.125, +0.142] | 1.000 | 3/3 |
| ig:llm/llm:bm25+repair=1 | ctx:bm25 | useful@1 | +0.000 | [-0.250, +0.250] | 1.000 | 3/3 |
| ig:gold/llm:bm25 | ctx:bm25 | ndcg@10 | +0.023 | [-0.021, +0.063] | 0.327 | 10/6 |
| ig:gold/llm:bm25 | ctx:bm25 | mrr | +0.058 | [-0.042, +0.175] | 0.498 | 3/1 |
| ig:gold/llm:bm25 | ctx:bm25 | useful@1 | +0.100 | [-0.100, +0.300] | 0.625 | 3/1 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | ndcg@10 | +0.051 | [-0.045, +0.141] | 0.310 | 14/5 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | mrr | +0.062 | [-0.092, +0.225] | 0.519 | 5/3 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | useful@1 | +0.100 | [-0.150, +0.400] | 0.725 | 5/3 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | ctx:bm25 | ndcg@10 | +0.002 | [-0.048, +0.047] | 0.921 | 9/7 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | ctx:bm25 | mrr | +0.008 | [-0.125, +0.142] | 1.000 | 3/3 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | ctx:bm25 | useful@1 | +0.000 | [-0.250, +0.250] | 1.000 | 3/3 |
| ig:llm/llm:tfidf+repair=1+rnorm=minmax | ctx:tfidf | ndcg@10 | +0.015 | [-0.035, +0.060] | 0.560 | 9/6 |
| ig:llm/llm:tfidf+repair=1+rnorm=minmax | ctx:tfidf | mrr | +0.085 | [-0.048, +0.217] | 0.242 | 6/2 |
| ig:llm/llm:tfidf+repair=1+rnorm=minmax | ctx:tfidf | useful@1 | +0.150 | [-0.100, +0.400] | 0.455 | 5/2 |
