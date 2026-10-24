# IGBench results (20261024T224244Z_srv_test_llm)

Benchmark `igbench-v1-test` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ig:llm/llm:bm25 | 0.820 | 0.520 | 0.345 | 0.935 | 0.883 | 0.800 | 0.150 |
| ig:llm/llm:tfidf | 0.777 | 0.460 | 0.320 | 0.892 | 0.752 | 0.600 | 0.300 |
| ig:llm/llm:sbert | 0.698 | 0.440 | 0.285 | 0.800 | 0.734 | 0.600 | 0.200 |
| ig:llm/llm:hybrid | 0.819 | 0.550 | 0.340 | 0.917 | 0.883 | 0.800 | 0.100 |
| ig:llm/llm:bm25+rnorm=minmax | 0.823 | 0.520 | 0.345 | 0.935 | 0.883 | 0.800 | 0.150 |
| ig:llm/llm:tfidf+rnorm=minmax | 0.768 | 0.450 | 0.310 | 0.870 | 0.749 | 0.600 | 0.300 |
| ig:llm/llm:sbert+rnorm=minmax | 0.702 | 0.410 | 0.275 | 0.780 | 0.759 | 0.650 | 0.200 |
| ig:llm/llm:hybrid+rnorm=minmax | 0.839 | 0.540 | 0.340 | 0.917 | 0.908 | 0.850 | 0.100 |
| ig:llm/index:bm25 | 0.821 | 0.520 | 0.350 | 0.944 | 0.892 | 0.800 | 0.100 |
| ig:gold/llm:bm25 | 0.850 | 0.550 | 0.350 | 0.940 | 0.975 | 0.950 | 0.000 |
| ig:llm/gold:bm25 | 0.813 | 0.510 | 0.340 | 0.919 | 0.879 | 0.800 | 0.150 |
| ctx:bm25 | 0.828 | 0.530 | 0.345 | 0.935 | 0.917 | 0.850 | 0.100 |
| ctx:tfidf | 0.775 | 0.460 | 0.315 | 0.882 | 0.765 | 0.600 | 0.300 |
| ctx:sbert | 0.690 | 0.340 | 0.270 | 0.780 | 0.814 | 0.700 | 0.150 |
| ctx:hybrid | 0.845 | 0.560 | 0.335 | 0.907 | 0.950 | 0.900 | 0.050 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ig:llm/llm:bm25 | 0.815 | 0.505 | 0.877 | 0.789 |
| ig:llm/llm:tfidf | 0.772 | 0.442 | 0.739 | 0.579 |
| ig:llm/llm:sbert | 0.688 | 0.421 | 0.720 | 0.579 |
| ig:llm/llm:hybrid | 0.812 | 0.537 | 0.877 | 0.789 |
| ig:llm/llm:bm25+rnorm=minmax | 0.817 | 0.505 | 0.877 | 0.789 |
| ig:llm/llm:tfidf+rnorm=minmax | 0.762 | 0.432 | 0.736 | 0.579 |
| ig:llm/llm:sbert+rnorm=minmax | 0.692 | 0.390 | 0.747 | 0.632 |
| ig:llm/llm:hybrid+rnorm=minmax | 0.833 | 0.526 | 0.903 | 0.842 |
| ig:llm/index:bm25 | 0.815 | 0.505 | 0.886 | 0.789 |
| ig:gold/llm:bm25 | 0.847 | 0.537 | 0.974 | 0.947 |
| ig:llm/gold:bm25 | 0.807 | 0.495 | 0.873 | 0.789 |
| ctx:bm25 | 0.823 | 0.516 | 0.912 | 0.842 |
| ctx:tfidf | 0.770 | 0.442 | 0.752 | 0.579 |
| ctx:sbert | 0.680 | 0.316 | 0.804 | 0.684 |
| ctx:hybrid | 0.839 | 0.547 | 0.947 | 0.895 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ig:llm/llm:bm25 | 0.402 | 0.798 | 0.935 |
| ig:llm/llm:tfidf | 0.333 | 0.736 | 0.892 |
| ig:llm/llm:sbert | 0.289 | 0.698 | 0.800 |
| ig:llm/llm:hybrid | 0.362 | 0.824 | 0.917 |
| ig:llm/llm:bm25+rnorm=minmax | 0.402 | 0.798 | 0.935 |
| ig:llm/llm:tfidf+rnorm=minmax | 0.333 | 0.724 | 0.870 |
| ig:llm/llm:sbert+rnorm=minmax | 0.339 | 0.666 | 0.780 |
| ig:llm/llm:hybrid+rnorm=minmax | 0.412 | 0.812 | 0.917 |
| ig:llm/index:bm25 | 0.324 | 0.798 | 0.944 |
| ig:gold/llm:bm25 | 0.395 | 0.829 | 0.940 |
| ig:llm/gold:bm25 | 0.402 | 0.785 | 0.919 |
| ctx:bm25 | 0.414 | 0.810 | 0.935 |
| ctx:tfidf | 0.340 | 0.736 | 0.882 |
| ctx:sbert | 0.352 | 0.591 | 0.780 |
| ctx:hybrid | 0.424 | 0.833 | 0.907 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | compare (n=8) | explain (n=3) | monitor (n=5) | predict (n=4) |
|---|---|---|---|---|
| ig:llm/llm:bm25 | 0.812 | 0.805 | 0.761 | 0.850 |
| ig:llm/llm:tfidf | 0.732 | 0.761 | 0.785 | 0.844 |
| ig:llm/llm:sbert | 0.673 | 0.813 | 0.532 | 0.876 |
| ig:llm/llm:hybrid | 0.826 | 0.796 | 0.739 | 0.864 |
| ig:llm/llm:bm25+rnorm=minmax | 0.812 | 0.805 | 0.761 | 0.862 |
| ig:llm/llm:tfidf+rnorm=minmax | 0.732 | 0.729 | 0.785 | 0.821 |
| ig:llm/llm:sbert+rnorm=minmax | 0.673 | 0.711 | 0.615 | 0.871 |
| ig:llm/llm:hybrid+rnorm=minmax | 0.826 | 0.807 | 0.800 | 0.878 |
| ig:llm/index:bm25 | 0.809 | 0.805 | 0.809 | 0.799 |
| ig:gold/llm:bm25 | 0.793 | 0.833 | 0.841 | 0.918 |
| ig:llm/gold:bm25 | 0.824 | 0.802 | 0.761 | 0.793 |
| ctx:bm25 | 0.812 | 0.800 | 0.750 | 0.909 |
| ctx:tfidf | 0.738 | 0.729 | 0.772 | 0.864 |
| ctx:sbert | 0.665 | 0.675 | 0.683 | 0.756 |
| ctx:hybrid | 0.847 | 0.763 | 0.809 | 0.918 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ig:llm/llm:bm25 | 0.871 |
| ig:llm/llm:tfidf | 0.863 |
| ig:llm/llm:sbert | 0.842 |
| ig:llm/llm:hybrid | 0.862 |
| ig:llm/llm:bm25+rnorm=minmax | 0.871 |
| ig:llm/llm:tfidf+rnorm=minmax | 0.859 |
| ig:llm/llm:sbert+rnorm=minmax | 0.821 |
| ig:llm/llm:hybrid+rnorm=minmax | 0.862 |
| ig:llm/index:bm25 | 0.874 |
| ig:gold/llm:bm25 | 0.879 |
| ig:llm/gold:bm25 | 0.874 |
| ctx:bm25 | 0.871 |
| ctx:tfidf | 0.862 |
| ctx:sbert | 0.824 |
| ctx:hybrid | 0.860 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:llm/llm:bm25 | 0.762 | 0.758 | 0.911 | 0.381 | 0.316 | 0.316 | 0.237 | 0.684 | 0.484 | 0.789 |
| ig:llm/llm:tfidf | 0.762 | 0.758 | 0.911 | 0.381 | 0.316 | 0.316 | 0.237 | 0.684 | 0.500 | 0.789 |
| ig:llm/llm:sbert | 0.762 | 0.758 | 0.911 | 0.381 | 0.316 | 0.316 | 0.237 | 0.684 | 0.571 | 0.800 |
| ig:llm/llm:hybrid | 0.762 | 0.758 | 0.911 | 0.381 | 0.316 | 0.316 | 0.237 | 0.684 | 0.484 | 0.750 |
| ig:llm/llm:bm25+rnorm=minmax | 0.762 | 0.758 | 0.911 | 0.381 | 0.316 | 0.316 | 0.237 | 0.684 | 0.484 | 0.789 |
| ig:llm/llm:tfidf+rnorm=minmax | 0.762 | 0.758 | 0.911 | 0.381 | 0.316 | 0.316 | 0.237 | 0.684 | 0.500 | 0.789 |
| ig:llm/llm:sbert+rnorm=minmax | 0.762 | 0.758 | 0.911 | 0.381 | 0.316 | 0.316 | 0.237 | 0.684 | 0.571 | 0.800 |
| ig:llm/llm:hybrid+rnorm=minmax | 0.762 | 0.758 | 0.911 | 0.381 | 0.316 | 0.316 | 0.237 | 0.684 | 0.484 | 0.750 |
| ig:llm/index:bm25 | 0.762 | 0.758 | 0.911 | 0.762 | 0.737 | 0.421 | 0.509 | 0.263 | 0.544 | 0.698 |
| ig:gold/llm:bm25 | 1.000 | 1.000 | 1.000 | 0.905 | 0.895 | 0.895 | 0.895 | 0.105 | 0.580 | 0.797 |
| ig:llm/gold:bm25 | 0.762 | 0.758 | 0.911 | 0.286 | 0.210 | 0.210 | 0.184 | 0.789 | 0.556 | 0.625 |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ig:llm/llm:bm25 | 6207.3 / 6574.8 / 7556.3 | 12.7 / 12.8 / 20.5 | 2471.1 / 3006.6 / 4620.6 | 23.3 / 0.0 / 53.2 | 272.9 / 0.0 / 470.7 | 0.4 / 0.3 / 0.8 | 8975.9 / 8226.0 / 12403.7 | 26.942 |
| ig:llm/llm:tfidf | 3.5 / 3.2 / 4.2 | 13.1 / 13.0 / 14.1 | 1.6 / 1.8 / 3.1 | 8.7 / 0.0 / 33.5 | 200.9 / 0.0 / 497.7 | 0.4 / 0.3 / 0.8 | 215.8 / 7.4 / 543.0 | 3.017 |
| ig:llm/llm:sbert | 3.0 / 3.0 / 3.6 | 111.1 / 81.9 / 102.1 | 1.4 / 1.0 / 3.9 | 65.8 / 0.0 / 78.0 | 126.3 / 0.0 / 343.7 | 0.3 / 0.1 / 0.6 | 197.2 / 6.0 / 983.8 | 4.687 |
| ig:llm/llm:hybrid | 4.0 / 3.5 / 6.0 | 89.1 / 88.5 / 94.9 | 1.5 / 1.6 / 3.5 | 43.5 / 0.0 / 41.2 | 228.6 / 0.0 / 497.5 | 0.4 / 0.3 / 0.6 | 278.6 / 7.5 / 610.5 | 5.578 |
| ig:llm/llm:bm25+rnorm=minmax | 3.1 / 2.9 / 4.6 | 5.6 / 5.5 / 9.0 | 1.6 / 1.5 / 3.2 | 10.3 / 0.0 / 38.8 | 258.7 / 0.0 / 414.7 | 0.4 / 0.3 / 0.7 | 274.8 / 6.5 / 459.7 | 3.503 |
| ig:llm/llm:tfidf+rnorm=minmax | 3.9 / 4.1 / 5.3 | 10.9 / 11.2 / 13.2 | 1.6 / 1.3 / 3.4 | 9.0 / 0.0 / 35.6 | 173.1 / 0.0 / 485.3 | 0.4 / 0.3 / 1.0 | 188.6 / 6.7 / 532.7 | 2.686 |
| ig:llm/llm:sbert+rnorm=minmax | 3.4 / 3.2 / 4.8 | 82.0 / 80.7 / 86.2 | 2.0 / 1.1 / 5.0 | 8.2 / 0.0 / 30.0 | 120.9 / 0.0 / 322.4 | 0.3 / 0.1 / 0.7 | 135.2 / 7.0 / 350.9 | 3.287 |
| ig:llm/llm:hybrid+rnorm=minmax | 4.1 / 3.6 / 5.9 | 121.0 / 77.7 / 189.2 | 1.6 / 1.6 / 3.1 | 11.3 / 0.0 / 40.1 | 223.8 / 0.0 / 514.9 | 0.4 / 0.3 / 0.7 | 242.0 / 6.4 / 565.0 | 5.856 |
| ig:llm/index:bm25 | 3.8 / 3.5 / 4.7 | 13.2 / 13.5 / 22.2 | 1.9 / 0.6 / 5.2 | 28.9 / 40.2 / 51.5 | 382.6 / 244.6 / 770.0 | 0.3 / 0.3 / 0.3 | 419.2 / 291.3 / 834.6 | 5.788 |
| ig:gold/llm:bm25 | 0.1 / 0.1 / 0.1 | 12.1 / 10.3 / 20.0 | 2666.8 / 2988.9 / 3511.9 | 34.5 / 40.4 / 49.2 | 731.7 / 251.7 / 1480.3 | 0.3 / 0.3 / 0.4 | 3435.6 / 3370.9 / 4928.0 | 23.911 |
| ig:llm/gold:bm25 | 3.0 / 2.7 / 4.0 | 13.4 / 13.3 / 23.1 | 0.4 / 0.2 / 1.2 | 7.8 / 0.0 / 37.7 | 263.7 / 0.0 / 272.0 | 0.5 / 0.3 / 0.9 | 276.0 / 4.2 / 322.1 | 4.592 |
| ctx:bm25 | – | 17.3 / 19.3 / 22.5 | – | – | – | – | 17.8 / 19.9 / 23.1 | 0.378 |
| ctx:tfidf | – | 6.8 / 6.2 / 6.6 | – | – | – | – | 7.0 / 6.4 / 6.9 | 0.148 |
| ctx:sbert | – | 112.8 / 114.5 / 119.7 | – | – | – | – | 112.9 / 114.6 / 119.8 | 2.373 |
| ctx:hybrid | – | 104.0 / 95.3 / 141.7 | – | – | – | – | 104.3 / 95.5 / 142.2 | 2.191 |

Context index build (one-off, ms): bm25: 133 (cached), hybrid: 20147 (cached), sbert: 1154 (cached), tfidf: 27 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:llm/llm:hybrid+rnorm=minmax | ctx:hybrid | ndcg@10 | -0.012 | [-0.037, +0.010] | 0.265 | 2/7 |
| ig:llm/llm:hybrid+rnorm=minmax | ctx:hybrid | mrr | -0.042 | [-0.117, +0.000] | 0.501 | 0/2 |
| ig:llm/llm:hybrid+rnorm=minmax | ctx:hybrid | useful@1 | -0.050 | [-0.150, +0.000] | 1.000 | 0/1 |
| ig:llm/index:bm25 | ctx:bm25 | ndcg@10 | -0.007 | [-0.056, +0.036] | 0.768 | 7/5 |
| ig:llm/index:bm25 | ctx:bm25 | mrr | -0.025 | [-0.150, +0.100] | 0.940 | 2/3 |
| ig:llm/index:bm25 | ctx:bm25 | useful@1 | -0.050 | [-0.250, +0.150] | 1.000 | 2/3 |
| ig:llm/llm:bm25+rnorm=minmax | ctx:bm25 | ndcg@10 | -0.005 | [-0.025, +0.009] | 0.745 | 3/5 |
| ig:llm/llm:bm25+rnorm=minmax | ctx:bm25 | mrr | -0.033 | [-0.100, +0.000] | 1.000 | 0/1 |
| ig:llm/llm:bm25+rnorm=minmax | ctx:bm25 | useful@1 | -0.050 | [-0.150, +0.000] | 1.000 | 0/1 |
| ig:llm/llm:bm25 | ctx:bm25 | ndcg@10 | -0.008 | [-0.029, +0.008] | 0.529 | 3/5 |
| ig:llm/llm:bm25 | ctx:bm25 | mrr | -0.033 | [-0.100, +0.000] | 1.000 | 0/1 |
| ig:llm/llm:bm25 | ctx:bm25 | useful@1 | -0.050 | [-0.150, +0.000] | 1.000 | 0/1 |
| ig:llm/llm:hybrid | ctx:hybrid | ndcg@10 | -0.030 | [-0.069, -0.003] | 0.086 | 2/8 |
| ig:llm/llm:hybrid | ctx:hybrid | mrr | -0.067 | [-0.150, +0.000] | 0.255 | 0/3 |
| ig:llm/llm:hybrid | ctx:hybrid | useful@1 | -0.100 | [-0.250, +0.000] | 0.505 | 0/2 |
| ig:llm/llm:tfidf+rnorm=minmax | ctx:tfidf | ndcg@10 | -0.007 | [-0.030, +0.009] | 0.618 | 3/5 |
| ig:llm/llm:tfidf+rnorm=minmax | ctx:tfidf | mrr | -0.016 | [-0.127, +0.075] | 1.000 | 2/1 |
| ig:llm/llm:tfidf+rnorm=minmax | ctx:tfidf | useful@1 | +0.000 | [-0.150, +0.150] | 1.000 | 1/1 |
| ig:llm/llm:tfidf | ctx:tfidf | ndcg@10 | +0.002 | [-0.015, +0.017] | 0.838 | 4/5 |
| ig:llm/llm:tfidf | ctx:tfidf | mrr | -0.013 | [-0.118, +0.075] | 1.000 | 2/1 |
| ig:llm/llm:tfidf | ctx:tfidf | useful@1 | +0.000 | [-0.150, +0.150] | 1.000 | 1/1 |
| ig:llm/gold:bm25 | ctx:bm25 | ndcg@10 | -0.015 | [-0.061, +0.014] | 0.744 | 4/4 |
| ig:llm/gold:bm25 | ctx:bm25 | mrr | -0.037 | [-0.113, +0.000] | 1.000 | 0/1 |
| ig:llm/gold:bm25 | ctx:bm25 | useful@1 | -0.050 | [-0.150, +0.000] | 1.000 | 0/1 |
| ig:llm/llm:sbert+rnorm=minmax | ctx:sbert | ndcg@10 | +0.014 | [-0.036, +0.057] | 0.570 | 7/5 |
| ig:llm/llm:sbert+rnorm=minmax | ctx:sbert | mrr | -0.055 | [-0.150, +0.000] | 0.496 | 0/2 |
| ig:llm/llm:sbert+rnorm=minmax | ctx:sbert | useful@1 | -0.050 | [-0.150, +0.000] | 1.000 | 0/1 |
| ig:llm/llm:sbert | ctx:sbert | ndcg@10 | +0.010 | [-0.064, +0.074] | 0.791 | 7/6 |
| ig:llm/llm:sbert | ctx:sbert | mrr | -0.080 | [-0.193, +0.008] | 0.248 | 1/3 |
| ig:llm/llm:sbert | ctx:sbert | useful@1 | -0.100 | [-0.250, +0.000] | 0.503 | 0/2 |
| ig:gold/llm:bm25 | ctx:bm25 | ndcg@10 | +0.021 | [-0.022, +0.062] | 0.365 | 10/6 |
| ig:gold/llm:bm25 | ctx:bm25 | mrr | +0.058 | [-0.042, +0.175] | 0.498 | 3/1 |
| ig:gold/llm:bm25 | ctx:bm25 | useful@1 | +0.100 | [-0.100, +0.300] | 0.625 | 3/1 |
