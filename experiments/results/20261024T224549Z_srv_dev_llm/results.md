# IGBench results (20261024T224549Z_srv_dev_llm)

Benchmark `igbench-v1` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ig:llm/llm:bm25 | 0.759 | 0.503 | 0.317 | 0.846 | 0.871 | 0.771 | 0.143 |
| ig:llm/llm:tfidf | 0.730 | 0.469 | 0.311 | 0.830 | 0.804 | 0.686 | 0.171 |
| ig:llm/llm:sbert | 0.768 | 0.480 | 0.294 | 0.837 | 0.839 | 0.743 | 0.143 |
| ig:llm/llm:hybrid | 0.802 | 0.560 | 0.331 | 0.881 | 0.838 | 0.714 | 0.171 |
| ig:llm/llm:bm25+rnorm=minmax | 0.762 | 0.503 | 0.317 | 0.846 | 0.871 | 0.771 | 0.143 |
| ig:llm/llm:tfidf+rnorm=minmax | 0.728 | 0.469 | 0.311 | 0.830 | 0.804 | 0.686 | 0.171 |
| ig:llm/llm:sbert+rnorm=minmax | 0.770 | 0.480 | 0.291 | 0.834 | 0.839 | 0.743 | 0.143 |
| ig:llm/llm:hybrid+rnorm=minmax | 0.804 | 0.554 | 0.331 | 0.881 | 0.838 | 0.714 | 0.171 |
| ig:llm/index:bm25 | 0.771 | 0.509 | 0.320 | 0.848 | 0.895 | 0.800 | 0.143 |
| ig:gold/llm:bm25 | 0.791 | 0.531 | 0.334 | 0.882 | 0.874 | 0.771 | 0.143 |
| ig:llm/gold:bm25 | 0.761 | 0.509 | 0.317 | 0.846 | 0.876 | 0.771 | 0.143 |
| ctx:bm25 | 0.768 | 0.486 | 0.323 | 0.851 | 0.895 | 0.800 | 0.143 |
| ctx:tfidf | 0.730 | 0.469 | 0.314 | 0.832 | 0.795 | 0.657 | 0.200 |
| ctx:sbert | 0.769 | 0.474 | 0.297 | 0.840 | 0.838 | 0.743 | 0.143 |
| ctx:hybrid | 0.814 | 0.543 | 0.334 | 0.884 | 0.876 | 0.771 | 0.143 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ig:llm/llm:bm25 | 0.769 | 0.487 | 0.891 | 0.812 |
| ig:llm/llm:tfidf | 0.739 | 0.463 | 0.817 | 0.719 |
| ig:llm/llm:sbert | 0.767 | 0.456 | 0.824 | 0.719 |
| ig:llm/llm:hybrid | 0.809 | 0.544 | 0.854 | 0.750 |
| ig:llm/llm:bm25+rnorm=minmax | 0.772 | 0.487 | 0.891 | 0.812 |
| ig:llm/llm:tfidf+rnorm=minmax | 0.736 | 0.463 | 0.817 | 0.719 |
| ig:llm/llm:sbert+rnorm=minmax | 0.769 | 0.456 | 0.824 | 0.719 |
| ig:llm/llm:hybrid+rnorm=minmax | 0.811 | 0.537 | 0.854 | 0.750 |
| ig:llm/index:bm25 | 0.782 | 0.494 | 0.917 | 0.844 |
| ig:gold/llm:bm25 | 0.804 | 0.519 | 0.893 | 0.812 |
| ig:llm/gold:bm25 | 0.771 | 0.494 | 0.896 | 0.812 |
| ctx:bm25 | 0.779 | 0.469 | 0.917 | 0.844 |
| ctx:tfidf | 0.739 | 0.463 | 0.807 | 0.688 |
| ctx:sbert | 0.768 | 0.450 | 0.823 | 0.719 |
| ctx:hybrid | 0.821 | 0.525 | 0.896 | 0.812 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ig:llm/llm:bm25 | 0.290 | 0.737 | 0.846 |
| ig:llm/llm:tfidf | 0.242 | 0.673 | 0.830 |
| ig:llm/llm:sbert | 0.286 | 0.745 | 0.837 |
| ig:llm/llm:hybrid | 0.281 | 0.800 | 0.881 |
| ig:llm/llm:bm25+rnorm=minmax | 0.290 | 0.737 | 0.846 |
| ig:llm/llm:tfidf+rnorm=minmax | 0.242 | 0.673 | 0.830 |
| ig:llm/llm:sbert+rnorm=minmax | 0.286 | 0.745 | 0.834 |
| ig:llm/llm:hybrid+rnorm=minmax | 0.281 | 0.798 | 0.881 |
| ig:llm/index:bm25 | 0.318 | 0.747 | 0.848 |
| ig:gold/llm:bm25 | 0.311 | 0.772 | 0.882 |
| ig:llm/gold:bm25 | 0.290 | 0.747 | 0.846 |
| ctx:bm25 | 0.306 | 0.711 | 0.851 |
| ctx:tfidf | 0.228 | 0.684 | 0.832 |
| ctx:sbert | 0.286 | 0.728 | 0.840 |
| ctx:hybrid | 0.312 | 0.789 | 0.884 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | aggregate (n=3) | compare (n=10) | explain (n=7) | monitor (n=5) | predict (n=8) |
|---|---|---|---|---|---|
| ig:llm/llm:bm25 | 0.948 | 0.804 | 0.794 | 0.668 | 0.713 |
| ig:llm/llm:tfidf | 0.940 | 0.738 | 0.766 | 0.649 | 0.705 |
| ig:llm/llm:sbert | 0.984 | 0.758 | 0.815 | 0.673 | 0.721 |
| ig:llm/llm:hybrid | 0.984 | 0.852 | 0.846 | 0.714 | 0.729 |
| ig:llm/llm:bm25+rnorm=minmax | 0.948 | 0.804 | 0.799 | 0.668 | 0.720 |
| ig:llm/llm:tfidf+rnorm=minmax | 0.940 | 0.738 | 0.759 | 0.649 | 0.702 |
| ig:llm/llm:sbert+rnorm=minmax | 0.984 | 0.758 | 0.821 | 0.673 | 0.725 |
| ig:llm/llm:hybrid+rnorm=minmax | 0.984 | 0.852 | 0.846 | 0.714 | 0.736 |
| ig:llm/index:bm25 | 0.948 | 0.812 | 0.794 | 0.668 | 0.755 |
| ig:gold/llm:bm25 | 0.964 | 0.837 | 0.827 | 0.728 | 0.741 |
| ig:llm/gold:bm25 | 0.948 | 0.811 | 0.794 | 0.668 | 0.713 |
| ctx:bm25 | 0.939 | 0.804 | 0.775 | 0.668 | 0.773 |
| ctx:tfidf | 0.940 | 0.736 | 0.738 | 0.649 | 0.734 |
| ctx:sbert | 0.966 | 0.762 | 0.808 | 0.673 | 0.730 |
| ctx:hybrid | 0.984 | 0.853 | 0.831 | 0.714 | 0.789 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ig:llm/llm:bm25 | 0.810 |
| ig:llm/llm:tfidf | 0.807 |
| ig:llm/llm:sbert | 0.780 |
| ig:llm/llm:hybrid | 0.819 |
| ig:llm/llm:bm25+rnorm=minmax | 0.810 |
| ig:llm/llm:tfidf+rnorm=minmax | 0.802 |
| ig:llm/llm:sbert+rnorm=minmax | 0.780 |
| ig:llm/llm:hybrid+rnorm=minmax | 0.819 |
| ig:llm/index:bm25 | 0.830 |
| ig:gold/llm:bm25 | 0.840 |
| ig:llm/gold:bm25 | 0.830 |
| ctx:bm25 | 0.803 |
| ctx:tfidf | 0.799 |
| ctx:sbert | 0.772 |
| ctx:hybrid | 0.808 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:llm/llm:bm25 | 0.389 | 0.746 | 0.909 | 0.194 | 0.125 | 0.125 | 0.125 | 0.875 | 0.487 | 1.000 |
| ig:llm/llm:tfidf | 0.389 | 0.746 | 0.909 | 0.194 | 0.125 | 0.125 | 0.125 | 0.875 | 0.488 | 1.000 |
| ig:llm/llm:sbert | 0.389 | 0.746 | 0.909 | 0.194 | 0.125 | 0.125 | 0.125 | 0.875 | 0.452 | 1.000 |
| ig:llm/llm:hybrid | 0.389 | 0.746 | 0.909 | 0.194 | 0.125 | 0.125 | 0.125 | 0.875 | 0.488 | 1.000 |
| ig:llm/llm:bm25+rnorm=minmax | 0.389 | 0.746 | 0.909 | 0.194 | 0.125 | 0.125 | 0.125 | 0.875 | 0.487 | 1.000 |
| ig:llm/llm:tfidf+rnorm=minmax | 0.389 | 0.746 | 0.909 | 0.194 | 0.125 | 0.125 | 0.125 | 0.875 | 0.488 | 1.000 |
| ig:llm/llm:sbert+rnorm=minmax | 0.389 | 0.746 | 0.909 | 0.194 | 0.125 | 0.125 | 0.125 | 0.875 | 0.452 | 1.000 |
| ig:llm/llm:hybrid+rnorm=minmax | 0.389 | 0.746 | 0.909 | 0.194 | 0.125 | 0.125 | 0.125 | 0.875 | 0.488 | 1.000 |
| ig:llm/index:bm25 | 0.389 | 0.746 | 0.909 | 0.361 | 0.281 | 0.188 | 0.208 | 0.719 | 0.567 | 0.927 |
| ig:gold/llm:bm25 | 1.000 | 1.000 | 1.000 | 0.861 | 0.875 | 0.875 | 0.875 | 0.125 | 0.486 | 0.776 |
| ig:llm/gold:bm25 | 0.389 | 0.746 | 0.909 | 0.250 | 0.156 | 0.156 | 0.141 | 0.844 | 0.500 | 1.000 |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ig:llm/llm:bm25 | 30278.1 / 5457.9 / 67492.2 | 14.9 / 13.9 / 24.6 | 1001.1 / 0.0 / 3555.6 | 16.9 / 0.0 / 54.1 | 132.1 / 0.0 / 593.2 | 0.5 / 0.4 / 0.8 | 31428.9 / 8691.7 / 67492.5 | 91.398 |
| ig:llm/llm:tfidf | 5.5 / 5.5 / 8.9 | 8.2 / 7.5 / 8.4 | 0.7 / 0.0 / 3.0 | 13.3 / 0.0 / 40.4 | 137.8 / 0.0 / 530.9 | 0.5 / 0.4 / 0.9 | 158.2 / 6.5 / 643.6 | 4.477 |
| ig:llm/llm:sbert | 5.8 / 5.6 / 11.2 | 129.5 / 120.3 / 135.4 | 0.8 / 0.1 / 4.1 | 11.0 / 0.0 / 46.0 | 120.8 / 0.0 / 308.2 | 0.4 / 0.4 / 0.6 | 139.2 / 6.7 / 578.5 | 8.842 |
| ig:llm/llm:hybrid | 5.8 / 4.9 / 11.0 | 139.4 / 139.1 / 162.1 | 0.7 / 0.0 / 3.1 | 20.1 / 0.0 / 48.2 | 178.4 / 0.0 / 1161.0 | 0.5 / 0.4 / 0.8 | 205.9 / 6.9 / 1222.2 | 11.253 |
| ig:llm/llm:bm25+rnorm=minmax | 4.8 / 4.5 / 7.7 | 15.1 / 14.4 / 24.9 | 0.6 / 0.0 / 2.6 | 4.3 / 0.0 / 37.2 | 125.0 / 0.0 / 330.0 | 0.4 / 0.4 / 0.8 | 135.4 / 5.8 / 375.0 | 4.909 |
| ig:llm/llm:tfidf+rnorm=minmax | 6.2 / 6.1 / 9.0 | 6.2 / 5.1 / 11.4 | 0.6 / 0.0 / 2.2 | 2.6 / 0.0 / 20.7 | 96.4 / 0.0 / 183.4 | 0.5 / 0.5 / 1.2 | 106.5 / 7.3 / 210.6 | 3.396 |
| ig:llm/llm:sbert+rnorm=minmax | 6.2 / 5.6 / 11.2 | 90.5 / 78.0 / 91.9 | 0.6 / 0.0 / 3.2 | 2.9 / 0.0 / 24.9 | 79.8 / 0.0 / 189.1 | 0.4 / 0.4 / 0.8 | 90.1 / 7.2 / 215.8 | 6.219 |
| ig:llm/llm:hybrid+rnorm=minmax | 4.9 / 4.8 / 7.9 | 109.4 / 102.5 / 139.6 | 0.6 / 0.0 / 2.9 | 3.5 / 0.0 / 29.9 | 121.3 / 0.0 / 671.2 | 0.4 / 0.4 / 0.8 | 131.0 / 6.2 / 706.1 | 8.15 |
| ig:llm/index:bm25 | 6.0 / 5.6 / 10.0 | 5.1 / 4.7 / 8.0 | 0.7 / 0.0 / 3.7 | 10.0 / 0.0 / 45.3 | 807.8 / 0.0 / 5680.7 | 0.5 / 0.5 / 1.1 | 825.6 / 9.0 / 5722.9 | 14.446 |
| ig:gold/llm:bm25 | 0.1 / 0.1 / 0.1 | 12.0 / 10.7 / 17.8 | 3122.3 / 3040.9 / 6656.1 | 54.2 / 38.2 / 60.7 | 1287.4 / 455.3 / 5964.1 | 0.2 / 0.2 / 0.5 | 4466.2 / 4103.2 / 10802.5 | 34.746 |
| ig:llm/gold:bm25 | 8.1 / 8.2 / 13.3 | 7.7 / 6.6 / 16.6 | 0.3 / 0.0 / 1.2 | 5.2 / 0.0 / 38.6 | 267.3 / 0.0 / 589.1 | 0.6 / 0.6 / 1.1 | 281.9 / 9.6 / 639.6 | 6.541 |
| ctx:bm25 | – | 16.7 / 16.8 / 25.1 | – | – | – | – | 17.2 / 17.2 / 25.6 | 0.623 |
| ctx:tfidf | – | 13.3 / 13.4 / 15.9 | – | – | – | – | 13.8 / 13.9 / 16.6 | 0.499 |
| ctx:sbert | – | 100.8 / 94.1 / 122.3 | – | – | – | – | 100.8 / 94.1 / 122.4 | 3.631 |
| ctx:hybrid | – | 144.3 / 147.0 / 156.2 | – | – | – | – | 144.7 / 147.4 / 156.5 | 5.212 |

Context index build (one-off, ms): bm25: 144 (cached), hybrid: 18705 (cached), sbert: 1157 (cached), tfidf: 31 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:llm/llm:hybrid+rnorm=minmax | ctx:hybrid | ndcg@10 | -0.009 | [-0.031, +0.007] | 0.448 | 3/4 |
| ig:llm/llm:hybrid+rnorm=minmax | ctx:hybrid | mrr | -0.038 | [-0.095, +0.000] | 0.509 | 0/2 |
| ig:llm/llm:hybrid+rnorm=minmax | ctx:hybrid | useful@1 | -0.057 | [-0.143, +0.000] | 0.509 | 0/2 |
| ig:llm/index:bm25 | ctx:bm25 | ndcg@10 | +0.003 | [-0.016, +0.019] | 0.827 | 6/2 |
| ig:llm/index:bm25 | ctx:bm25 | mrr | +0.000 | [-0.052, +0.043] | 1.000 | 2/1 |
| ig:llm/index:bm25 | ctx:bm25 | useful@1 | +0.000 | [-0.086, +0.086] | 1.000 | 1/1 |
| ig:llm/llm:bm25+rnorm=minmax | ctx:bm25 | ndcg@10 | -0.006 | [-0.032, +0.016] | 0.676 | 5/3 |
| ig:llm/llm:bm25+rnorm=minmax | ctx:bm25 | mrr | -0.024 | [-0.081, +0.029] | 0.509 | 1/2 |
| ig:llm/llm:bm25+rnorm=minmax | ctx:bm25 | useful@1 | -0.029 | [-0.114, +0.057] | 1.000 | 1/2 |
| ig:llm/llm:bm25 | ctx:bm25 | ndcg@10 | -0.009 | [-0.035, +0.012] | 0.516 | 5/3 |
| ig:llm/llm:bm25 | ctx:bm25 | mrr | -0.024 | [-0.081, +0.029] | 0.509 | 1/2 |
| ig:llm/llm:bm25 | ctx:bm25 | useful@1 | -0.029 | [-0.114, +0.057] | 1.000 | 1/2 |
| ig:llm/llm:hybrid | ctx:hybrid | ndcg@10 | -0.011 | [-0.033, +0.006] | 0.341 | 2/5 |
| ig:llm/llm:hybrid | ctx:hybrid | mrr | -0.038 | [-0.095, +0.000] | 0.509 | 0/2 |
| ig:llm/llm:hybrid | ctx:hybrid | useful@1 | -0.057 | [-0.143, +0.000] | 0.509 | 0/2 |
| ig:llm/llm:tfidf+rnorm=minmax | ctx:tfidf | ndcg@10 | -0.002 | [-0.017, +0.012] | 0.873 | 5/2 |
| ig:llm/llm:tfidf+rnorm=minmax | ctx:tfidf | mrr | +0.009 | [-0.031, +0.057] | 1.000 | 1/1 |
| ig:llm/llm:tfidf+rnorm=minmax | ctx:tfidf | useful@1 | +0.029 | [+0.000, +0.086] | 1.000 | 1/0 |
| ig:llm/llm:tfidf | ctx:tfidf | ndcg@10 | -0.000 | [-0.016, +0.016] | 1.000 | 5/2 |
| ig:llm/llm:tfidf | ctx:tfidf | mrr | +0.009 | [-0.031, +0.057] | 1.000 | 1/1 |
| ig:llm/llm:tfidf | ctx:tfidf | useful@1 | +0.029 | [+0.000, +0.086] | 1.000 | 1/0 |
| ig:llm/gold:bm25 | ctx:bm25 | ndcg@10 | -0.007 | [-0.033, +0.015] | 0.604 | 6/2 |
| ig:llm/gold:bm25 | ctx:bm25 | mrr | -0.019 | [-0.076, +0.038] | 0.752 | 2/2 |
| ig:llm/gold:bm25 | ctx:bm25 | useful@1 | -0.029 | [-0.114, +0.057] | 1.000 | 1/2 |
| ig:llm/llm:sbert+rnorm=minmax | ctx:sbert | ndcg@10 | +0.002 | [-0.011, +0.013] | 0.803 | 9/3 |
| ig:llm/llm:sbert+rnorm=minmax | ctx:sbert | mrr | +0.001 | [+0.000, +0.002] | 1.000 | 1/0 |
| ig:llm/llm:sbert+rnorm=minmax | ctx:sbert | useful@1 | +0.000 | [+0.000, +0.000] | 1.000 | 0/0 |
| ig:llm/llm:sbert | ctx:sbert | ndcg@10 | -0.000 | [-0.011, +0.010] | 0.959 | 8/4 |
| ig:llm/llm:sbert | ctx:sbert | mrr | +0.001 | [+0.000, +0.002] | 1.000 | 1/0 |
| ig:llm/llm:sbert | ctx:sbert | useful@1 | +0.000 | [+0.000, +0.000] | 1.000 | 0/0 |
| ig:gold/llm:bm25 | ctx:bm25 | ndcg@10 | +0.022 | [-0.002, +0.047] | 0.090 | 20/9 |
| ig:gold/llm:bm25 | ctx:bm25 | mrr | -0.021 | [-0.086, +0.029] | 0.750 | 1/2 |
| ig:gold/llm:bm25 | ctx:bm25 | useful@1 | -0.029 | [-0.143, +0.057] | 1.000 | 1/2 |
