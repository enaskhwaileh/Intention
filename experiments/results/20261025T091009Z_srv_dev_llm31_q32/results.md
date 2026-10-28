# IGBench results (20261025T091009Z_srv_dev_llm31_q32)

Benchmark `igbench-v1` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:bm25 | 0.768 | 0.486 | 0.323 | 0.851 | 0.895 | 0.800 | 0.143 |
| ctx:tfidf | 0.730 | 0.469 | 0.314 | 0.832 | 0.795 | 0.657 | 0.200 |
| ctx:sbert | 0.769 | 0.474 | 0.297 | 0.840 | 0.838 | 0.743 | 0.143 |
| ctx:hybrid | 0.814 | 0.543 | 0.334 | 0.884 | 0.876 | 0.771 | 0.143 |
| ig:llm/llm:bm25 | 0.773 | 0.509 | 0.331 | 0.870 | 0.874 | 0.771 | 0.143 |
| ig:llm/llm:bm25+repair=1 | 0.780 | 0.537 | 0.334 | 0.873 | 0.874 | 0.771 | 0.143 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.792 | 0.537 | 0.340 | 0.885 | 0.895 | 0.800 | 0.143 |
| ig:llm/llm:tfidf | 0.756 | 0.480 | 0.334 | 0.872 | 0.800 | 0.657 | 0.200 |
| ig:llm/llm:tfidf+repair=1 | 0.762 | 0.497 | 0.337 | 0.875 | 0.800 | 0.657 | 0.200 |
| ig:llm/llm:tfidf+repair=1+rnorm=minmax | 0.757 | 0.497 | 0.329 | 0.851 | 0.814 | 0.686 | 0.171 |
| ig:llm/llm:sbert | 0.777 | 0.497 | 0.317 | 0.863 | 0.835 | 0.771 | 0.171 |
| ig:llm/llm:sbert+repair=1 | 0.785 | 0.514 | 0.329 | 0.877 | 0.838 | 0.771 | 0.143 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.784 | 0.514 | 0.309 | 0.857 | 0.841 | 0.771 | 0.143 |
| ig:llm/llm:hybrid | 0.805 | 0.531 | 0.337 | 0.888 | 0.850 | 0.743 | 0.171 |
| ig:llm/llm:hybrid+repair=1 | 0.810 | 0.537 | 0.340 | 0.891 | 0.855 | 0.743 | 0.171 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | 0.819 | 0.543 | 0.334 | 0.886 | 0.876 | 0.771 | 0.143 |
| ig:gold/llm:bm25 | 0.788 | 0.531 | 0.334 | 0.882 | 0.869 | 0.771 | 0.143 |
| ig:llm/index:bm25+repair=1 | 0.779 | 0.531 | 0.331 | 0.866 | 0.879 | 0.771 | 0.143 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:bm25 | 0.779 | 0.469 | 0.917 | 0.844 |
| ctx:tfidf | 0.739 | 0.463 | 0.807 | 0.688 |
| ctx:sbert | 0.768 | 0.450 | 0.823 | 0.719 |
| ctx:hybrid | 0.821 | 0.525 | 0.896 | 0.812 |
| ig:llm/llm:bm25 | 0.784 | 0.494 | 0.893 | 0.812 |
| ig:llm/llm:bm25+repair=1 | 0.792 | 0.525 | 0.893 | 0.812 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.805 | 0.525 | 0.917 | 0.844 |
| ig:llm/llm:tfidf | 0.767 | 0.475 | 0.812 | 0.688 |
| ig:llm/llm:tfidf+repair=1 | 0.774 | 0.494 | 0.812 | 0.688 |
| ig:llm/llm:tfidf+repair=1+rnorm=minmax | 0.769 | 0.494 | 0.828 | 0.719 |
| ig:llm/llm:sbert | 0.777 | 0.475 | 0.820 | 0.750 |
| ig:llm/llm:sbert+repair=1 | 0.786 | 0.494 | 0.822 | 0.750 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.784 | 0.494 | 0.826 | 0.750 |
| ig:llm/llm:hybrid | 0.811 | 0.512 | 0.867 | 0.781 |
| ig:llm/llm:hybrid+repair=1 | 0.817 | 0.519 | 0.872 | 0.781 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | 0.827 | 0.525 | 0.896 | 0.812 |
| ig:gold/llm:bm25 | 0.800 | 0.519 | 0.888 | 0.812 |
| ig:llm/index:bm25+repair=1 | 0.791 | 0.519 | 0.898 | 0.812 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:bm25 | 0.306 | 0.711 | 0.851 |
| ctx:tfidf | 0.228 | 0.684 | 0.832 |
| ctx:sbert | 0.286 | 0.728 | 0.840 |
| ctx:hybrid | 0.312 | 0.789 | 0.884 |
| ig:llm/llm:bm25 | 0.302 | 0.745 | 0.870 |
| ig:llm/llm:bm25+repair=1 | 0.302 | 0.781 | 0.873 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.306 | 0.772 | 0.885 |
| ig:llm/llm:tfidf | 0.251 | 0.683 | 0.872 |
| ig:llm/llm:tfidf+repair=1 | 0.251 | 0.704 | 0.875 |
| ig:llm/llm:tfidf+repair=1+rnorm=minmax | 0.256 | 0.704 | 0.851 |
| ig:llm/llm:sbert | 0.286 | 0.724 | 0.863 |
| ig:llm/llm:sbert+repair=1 | 0.286 | 0.742 | 0.877 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.298 | 0.755 | 0.857 |
| ig:llm/llm:hybrid | 0.308 | 0.779 | 0.888 |
| ig:llm/llm:hybrid+repair=1 | 0.297 | 0.784 | 0.891 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | 0.302 | 0.789 | 0.886 |
| ig:gold/llm:bm25 | 0.311 | 0.772 | 0.882 |
| ig:llm/index:bm25+repair=1 | 0.302 | 0.774 | 0.866 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | aggregate (n=3) | compare (n=10) | explain (n=7) | monitor (n=5) | predict (n=8) |
|---|---|---|---|---|---|
| ctx:bm25 | 0.939 | 0.804 | 0.775 | 0.668 | 0.773 |
| ctx:tfidf | 0.940 | 0.736 | 0.738 | 0.649 | 0.734 |
| ctx:sbert | 0.966 | 0.762 | 0.808 | 0.673 | 0.730 |
| ctx:hybrid | 0.984 | 0.853 | 0.831 | 0.714 | 0.789 |
| ig:llm/llm:bm25 | 0.939 | 0.806 | 0.799 | 0.718 | 0.739 |
| ig:llm/llm:bm25+repair=1 | 0.939 | 0.813 | 0.818 | 0.726 | 0.739 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.939 | 0.815 | 0.822 | 0.717 | 0.792 |
| ig:llm/llm:tfidf | 0.918 | 0.760 | 0.789 | 0.688 | 0.758 |
| ig:llm/llm:tfidf+repair=1 | 0.918 | 0.765 | 0.804 | 0.695 | 0.758 |
| ig:llm/llm:tfidf+repair=1+rnorm=minmax | 0.918 | 0.762 | 0.787 | 0.653 | 0.783 |
| ig:llm/llm:sbert | 0.983 | 0.821 | 0.837 | 0.675 | 0.662 |
| ig:llm/llm:sbert+repair=1 | 0.983 | 0.824 | 0.846 | 0.712 | 0.662 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.983 | 0.787 | 0.843 | 0.664 | 0.735 |
| ig:llm/llm:hybrid | 0.984 | 0.874 | 0.832 | 0.718 | 0.721 |
| ig:llm/llm:hybrid+repair=1 | 0.984 | 0.880 | 0.830 | 0.746 | 0.721 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | 0.984 | 0.860 | 0.828 | 0.735 | 0.793 |
| ig:gold/llm:bm25 | 0.964 | 0.838 | 0.827 | 0.730 | 0.724 |
| ig:llm/index:bm25+repair=1 | 0.939 | 0.821 | 0.791 | 0.715 | 0.756 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:bm25 | 0.803 |
| ctx:tfidf | 0.799 |
| ctx:sbert | 0.772 |
| ctx:hybrid | 0.808 |
| ig:llm/llm:bm25 | 0.806 |
| ig:llm/llm:bm25+repair=1 | 0.817 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.813 |
| ig:llm/llm:tfidf | 0.798 |
| ig:llm/llm:tfidf+repair=1 | 0.796 |
| ig:llm/llm:tfidf+repair=1+rnorm=minmax | 0.795 |
| ig:llm/llm:sbert | 0.785 |
| ig:llm/llm:sbert+repair=1 | 0.796 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.763 |
| ig:llm/llm:hybrid | 0.809 |
| ig:llm/llm:hybrid+repair=1 | 0.816 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | 0.812 |
| ig:gold/llm:bm25 | 0.830 |
| ig:llm/index:bm25+repair=1 | 0.837 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:llm/llm:bm25 | 0.750 | 0.853 | 0.958 | 0.556 | 0.531 | 0.500 | 0.516 | 0.469 | 0.537 | 0.689 |
| ig:llm/llm:bm25+repair=1 | 0.861 | 0.819 | 0.893 | 0.694 | 0.656 | 0.625 | 0.599 | 0.344 | 0.553 | 0.663 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.861 | 0.819 | 0.893 | 0.694 | 0.656 | 0.625 | 0.599 | 0.344 | 0.553 | 0.663 |
| ig:llm/llm:tfidf | 0.750 | 0.853 | 0.958 | 0.556 | 0.531 | 0.500 | 0.516 | 0.469 | 0.559 | 0.712 |
| ig:llm/llm:tfidf+repair=1 | 0.861 | 0.819 | 0.893 | 0.694 | 0.656 | 0.625 | 0.599 | 0.344 | 0.574 | 0.682 |
| ig:llm/llm:tfidf+repair=1+rnorm=minmax | 0.861 | 0.819 | 0.893 | 0.694 | 0.656 | 0.625 | 0.599 | 0.344 | 0.574 | 0.682 |
| ig:llm/llm:sbert | 0.750 | 0.853 | 0.958 | 0.556 | 0.531 | 0.500 | 0.516 | 0.469 | 0.500 | 0.651 |
| ig:llm/llm:sbert+repair=1 | 0.861 | 0.819 | 0.893 | 0.694 | 0.656 | 0.625 | 0.599 | 0.344 | 0.520 | 0.634 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.861 | 0.819 | 0.893 | 0.694 | 0.656 | 0.625 | 0.599 | 0.344 | 0.520 | 0.634 |
| ig:llm/llm:hybrid | 0.750 | 0.853 | 0.958 | 0.556 | 0.531 | 0.500 | 0.516 | 0.469 | 0.520 | 0.693 |
| ig:llm/llm:hybrid+repair=1 | 0.861 | 0.819 | 0.893 | 0.694 | 0.656 | 0.625 | 0.599 | 0.344 | 0.531 | 0.670 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | 0.861 | 0.819 | 0.893 | 0.694 | 0.656 | 0.625 | 0.599 | 0.344 | 0.531 | 0.670 |
| ig:gold/llm:bm25 | 1.000 | 1.000 | 1.000 | 0.889 | 0.906 | 0.875 | 0.906 | 0.094 | 0.494 | 0.763 |
| ig:llm/index:bm25+repair=1 | 0.861 | 0.819 | 0.893 | 0.639 | 0.594 | 0.594 | 0.568 | 0.406 | 0.500 | 0.653 |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:bm25 | – | 5.1 / 5.3 / 7.6 | – | – | – | – | 5.2 / 5.4 / 7.7 | 0.189 |
| ctx:tfidf | – | 4.7 / 4.2 / 4.7 | – | – | – | – | 4.8 / 4.3 / 4.8 | 0.175 |
| ctx:sbert | – | 94.5 / 87.6 / 92.3 | – | – | – | – | 94.5 / 87.6 / 92.4 | 3.404 |
| ctx:hybrid | – | 95.4 / 95.6 / 101.6 | – | – | – | – | 95.5 / 95.7 / 101.8 | 3.439 |
| ig:llm/llm:bm25 | 16831.4 / 17034.2 / 27272.8 | 4.9 / 4.6 / 7.5 | 8508.3 / 8878.0 / 17956.4 | 24.6 / 0.0 / 41.7 | 884.0 / 0.0 / 3958.6 | 0.3 / 0.1 / 0.9 | 26249.3 / 26236.1 / 40318.5 | 88.649 |
| ig:llm/llm:bm25+repair=1 | 2921.7 / 8.2 / 11962.2 | 4.8 / 4.4 / 7.6 | 2868.4 / 2.0 / 11963.8 | 34.7 / 17.6 / 94.2 | 1018.3 / 81.7 / 4248.6 | 0.3 / 0.1 / 1.1 | 6844.1 / 3748.0 / 21949.1 | 50.801 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 10.4 / 9.1 / 18.1 | 4.9 / 4.4 / 7.6 | 2.3 / 1.8 / 5.8 | 13.8 / 18.4 / 28.4 | 964.4 / 85.1 / 3909.4 | 0.2 / 0.1 / 0.8 | 992.0 / 117.2 / 3948.6 | 14.93 |
| ig:llm/llm:tfidf | 8.8 / 8.0 / 16.9 | 4.3 / 4.2 / 5.3 | 1.8 / 1.1 / 4.7 | 10.8 / 0.0 / 28.2 | 828.9 / 0.0 / 3903.5 | 0.3 / 0.1 / 1.2 | 851.3 / 24.2 / 3942.3 | 16.508 |
| ig:llm/llm:tfidf+repair=1 | 7.4 / 6.7 / 14.0 | 4.3 / 4.0 / 5.7 | 1.8 / 1.3 / 4.4 | 32.2 / 17.9 / 35.7 | 976.5 / 83.7 / 4071.5 | 0.2 / 0.1 / 1.2 | 1018.9 / 118.2 / 4104.4 | 16.418 |
| ig:llm/llm:tfidf+repair=1+rnorm=minmax | 8.7 / 7.3 / 18.3 | 4.4 / 4.1 / 5.0 | 2.1 / 1.5 / 6.1 | 12.8 / 17.0 / 28.0 | 952.2 / 87.1 / 3925.7 | 0.2 / 0.1 / 1.1 | 976.7 / 117.9 / 3972.3 | 16.559 |
| ig:llm/llm:sbert | 6.5 / 5.1 / 17.2 | 85.7 / 84.1 / 93.3 | 1.6 / 1.0 / 4.3 | 14.4 / 0.0 / 36.6 | 815.1 / 0.0 / 4098.9 | 0.2 / 0.1 / 0.7 | 838.5 / 19.0 / 4151.3 | 19.759 |
| ig:llm/llm:sbert+repair=1 | 10.1 / 8.0 / 22.5 | 87.2 / 87.1 / 92.9 | 2.0 / 1.5 / 6.1 | 47.0 / 20.0 / 48.6 | 952.2 / 84.0 / 4070.6 | 0.2 / 0.1 / 0.6 | 1012.2 / 122.6 / 4118.2 | 19.555 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 9.0 / 7.5 / 24.3 | 82.5 / 81.5 / 90.9 | 2.0 / 1.3 / 5.9 | 61.3 / 19.7 / 393.0 | 1011.9 / 85.1 / 4014.5 | 0.2 / 0.1 / 0.7 | 1085.2 / 113.0 / 4794.9 | 19.779 |
| ig:llm/llm:hybrid | 6.7 / 5.7 / 14.2 | 89.5 / 89.3 / 102.1 | 1.8 / 1.1 / 4.7 | 14.2 / 0.0 / 33.7 | 964.3 / 0.0 / 3945.7 | 0.3 / 0.1 / 1.0 | 988.0 / 15.2 / 3985.2 | 22.004 |
| ig:llm/llm:hybrid+repair=1 | 13.4 / 12.5 / 24.0 | 105.1 / 85.5 / 179.8 | 2.6 / 1.6 / 8.4 | 15.7 / 19.9 / 35.0 | 1052.4 / 95.2 / 4003.1 | 0.3 / 0.1 / 1.3 | 1085.2 / 145.6 / 4054.9 | 20.665 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | 9.1 / 8.4 / 19.8 | 80.3 / 79.6 / 84.6 | 2.0 / 1.5 / 5.3 | 54.3 / 19.0 / 397.5 | 1074.0 / 136.0 / 4044.6 | 0.2 / 0.1 / 0.9 | 1140.5 / 272.8 / 4077.5 | 19.711 |
| ig:gold/llm:bm25 | 0.1 / 0.1 / 0.2 | 4.1 / 3.5 / 6.6 | 9774.1 / 9898.5 / 19620.3 | 24.6 / 29.0 / 39.9 | 1162.0 / 311.4 / 3802.0 | 0.1 / 0.1 / 0.3 | 10962.0 / 11316.4 / 20772.7 | 62.37 |
| ig:llm/index:bm25+repair=1 | 11.1 / 10.3 / 21.5 | 4.8 / 4.5 / 7.6 | 1.9 / 0.3 / 7.4 | 13.3 / 17.4 / 30.2 | 724.9 / 86.7 / 3869.8 | 0.2 / 0.1 / 0.9 | 752.2 / 124.8 / 3914.6 | 12.595 |

Context index build (one-off, ms): bm25: 61 (cached), hybrid: 13489 (cached), sbert: 1056 (cached), tfidf: 21 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:llm/llm:hybrid+repair=1 | ctx:hybrid | ndcg@10 | -0.004 | [-0.029, +0.019] | 0.810 | 13/9 |
| ig:llm/llm:hybrid+repair=1 | ctx:hybrid | mrr | -0.021 | [-0.090, +0.038] | 0.619 | 1/3 |
| ig:llm/llm:hybrid+repair=1 | ctx:hybrid | useful@1 | -0.029 | [-0.143, +0.057] | 1.000 | 1/2 |
| ig:llm/llm:bm25 | ctx:bm25 | ndcg@10 | +0.004 | [-0.018, +0.027] | 0.708 | 8/7 |
| ig:llm/llm:bm25 | ctx:bm25 | mrr | -0.021 | [-0.064, +0.000] | 1.000 | 0/1 |
| ig:llm/llm:bm25 | ctx:bm25 | useful@1 | -0.029 | [-0.086, +0.000] | 1.000 | 0/1 |
| ig:llm/llm:hybrid | ctx:hybrid | ndcg@10 | -0.009 | [-0.032, +0.009] | 0.525 | 10/6 |
| ig:llm/llm:hybrid | ctx:hybrid | mrr | -0.026 | [-0.074, +0.000] | 0.504 | 0/2 |
| ig:llm/llm:hybrid | ctx:hybrid | useful@1 | -0.029 | [-0.086, +0.000] | 1.000 | 0/1 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | ndcg@10 | +0.015 | [-0.007, +0.039] | 0.225 | 16/11 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | mrr | +0.003 | [-0.056, +0.062] | 0.943 | 5/5 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | useful@1 | +0.029 | [-0.057, +0.114] | 1.000 | 2/1 |
| ig:llm/llm:tfidf | ctx:tfidf | ndcg@10 | +0.025 | [+0.005, +0.050] | 0.025 | 13/4 |
| ig:llm/llm:tfidf | ctx:tfidf | mrr | +0.005 | [-0.038, +0.043] | 1.000 | 2/1 |
| ig:llm/llm:tfidf | ctx:tfidf | useful@1 | +0.000 | [-0.086, +0.086] | 1.000 | 1/1 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | ctx:hybrid | ndcg@10 | +0.005 | [-0.006, +0.017] | 0.431 | 10/11 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | ctx:hybrid | mrr | +0.000 | [-0.043, +0.052] | 1.000 | 1/2 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | ctx:hybrid | useful@1 | +0.000 | [-0.086, +0.086] | 1.000 | 1/1 |
| ig:llm/index:bm25+repair=1 | ctx:bm25 | ndcg@10 | +0.011 | [-0.012, +0.033] | 0.412 | 13/7 |
| ig:llm/index:bm25+repair=1 | ctx:bm25 | mrr | -0.017 | [-0.064, +0.014] | 1.000 | 1/1 |
| ig:llm/index:bm25+repair=1 | ctx:bm25 | useful@1 | -0.029 | [-0.086, +0.000] | 1.000 | 0/1 |
| ig:llm/llm:sbert | ctx:sbert | ndcg@10 | +0.009 | [-0.034, +0.051] | 0.707 | 13/7 |
| ig:llm/llm:sbert | ctx:sbert | mrr | -0.003 | [-0.093, +0.088] | 0.948 | 4/6 |
| ig:llm/llm:sbert | ctx:sbert | useful@1 | +0.029 | [-0.114, +0.171] | 1.000 | 3/2 |
| ig:llm/llm:tfidf+repair=1 | ctx:tfidf | ndcg@10 | +0.031 | [+0.011, +0.055] | 0.006 | 17/5 |
| ig:llm/llm:tfidf+repair=1 | ctx:tfidf | mrr | +0.005 | [-0.038, +0.043] | 1.000 | 2/1 |
| ig:llm/llm:tfidf+repair=1 | ctx:tfidf | useful@1 | +0.000 | [-0.086, +0.086] | 1.000 | 1/1 |
| ig:llm/llm:bm25+repair=1 | ctx:bm25 | ndcg@10 | +0.011 | [-0.011, +0.035] | 0.378 | 13/8 |
| ig:llm/llm:bm25+repair=1 | ctx:bm25 | mrr | -0.021 | [-0.064, +0.000] | 1.000 | 0/1 |
| ig:llm/llm:bm25+repair=1 | ctx:bm25 | useful@1 | -0.029 | [-0.086, +0.000] | 1.000 | 0/1 |
| ig:gold/llm:bm25 | ctx:bm25 | ndcg@10 | +0.019 | [-0.004, +0.044] | 0.138 | 19/10 |
| ig:gold/llm:bm25 | ctx:bm25 | mrr | -0.026 | [-0.090, +0.029] | 0.503 | 1/3 |
| ig:gold/llm:bm25 | ctx:bm25 | useful@1 | -0.029 | [-0.143, +0.057] | 1.000 | 1/2 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | ndcg@10 | +0.016 | [-0.029, +0.058] | 0.482 | 18/9 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | mrr | -0.001 | [-0.092, +0.090] | 0.987 | 5/6 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | useful@1 | +0.029 | [-0.114, +0.171] | 1.000 | 3/2 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | ctx:bm25 | ndcg@10 | +0.023 | [+0.010, +0.040] | 0.001 | 14/7 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | ctx:bm25 | mrr | +0.000 | [+0.000, +0.000] | 1.000 | 0/0 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | ctx:bm25 | useful@1 | +0.000 | [+0.000, +0.000] | 1.000 | 0/0 |
| ig:llm/llm:tfidf+repair=1+rnorm=minmax | ctx:tfidf | ndcg@10 | +0.026 | [+0.011, +0.045] | 0.002 | 17/3 |
| ig:llm/llm:tfidf+repair=1+rnorm=minmax | ctx:tfidf | mrr | +0.019 | [+0.000, +0.052] | 0.507 | 2/0 |
| ig:llm/llm:tfidf+repair=1+rnorm=minmax | ctx:tfidf | useful@1 | +0.029 | [+0.000, +0.086] | 1.000 | 1/0 |
