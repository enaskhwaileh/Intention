# IGBench results (20261024T225129Z_srv_dev_llm31)

Benchmark `igbench-v1` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:bm25 | 0.768 | 0.486 | 0.323 | 0.851 | 0.895 | 0.800 | 0.143 |
| ctx:tfidf | 0.730 | 0.469 | 0.314 | 0.832 | 0.795 | 0.657 | 0.200 |
| ctx:sbert | 0.769 | 0.474 | 0.297 | 0.840 | 0.838 | 0.743 | 0.143 |
| ctx:hybrid | 0.814 | 0.543 | 0.334 | 0.884 | 0.876 | 0.771 | 0.143 |
| ig:llm/llm:bm25 | 0.774 | 0.514 | 0.329 | 0.851 | 0.888 | 0.800 | 0.114 |
| ig:llm/llm:bm25+rnorm=minmax | 0.788 | 0.520 | 0.334 | 0.863 | 0.909 | 0.829 | 0.114 |
| ig:llm/llm:bm25+repair=1 | 0.781 | 0.520 | 0.331 | 0.866 | 0.888 | 0.800 | 0.114 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.794 | 0.520 | 0.337 | 0.878 | 0.909 | 0.829 | 0.114 |
| ig:llm/llm:tfidf | 0.766 | 0.503 | 0.331 | 0.851 | 0.838 | 0.714 | 0.171 |
| ig:llm/llm:tfidf+rnorm=minmax | 0.764 | 0.503 | 0.326 | 0.846 | 0.852 | 0.743 | 0.143 |
| ig:llm/llm:tfidf+repair=1 | 0.774 | 0.503 | 0.334 | 0.865 | 0.838 | 0.714 | 0.171 |
| ig:llm/llm:tfidf+repair=1+rnorm=minmax | 0.765 | 0.503 | 0.326 | 0.846 | 0.852 | 0.743 | 0.143 |
| ig:llm/llm:sbert | 0.787 | 0.497 | 0.317 | 0.858 | 0.859 | 0.800 | 0.143 |
| ig:llm/llm:sbert+rnorm=minmax | 0.786 | 0.497 | 0.303 | 0.847 | 0.844 | 0.771 | 0.143 |
| ig:llm/llm:sbert+repair=1 | 0.787 | 0.497 | 0.317 | 0.858 | 0.859 | 0.800 | 0.143 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.786 | 0.497 | 0.303 | 0.847 | 0.844 | 0.771 | 0.143 |
| ig:llm/llm:hybrid | 0.808 | 0.531 | 0.334 | 0.885 | 0.850 | 0.743 | 0.171 |
| ig:llm/llm:hybrid+rnorm=minmax | 0.820 | 0.537 | 0.334 | 0.886 | 0.871 | 0.771 | 0.143 |
| ig:llm/llm:hybrid+repair=1 | 0.807 | 0.531 | 0.334 | 0.885 | 0.850 | 0.743 | 0.171 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | 0.819 | 0.537 | 0.334 | 0.886 | 0.871 | 0.771 | 0.143 |
| ig:gold/llm:bm25 | 0.791 | 0.531 | 0.334 | 0.882 | 0.874 | 0.771 | 0.143 |
| ig:llm/index:bm25 | 0.772 | 0.520 | 0.329 | 0.851 | 0.879 | 0.771 | 0.143 |
| ig:gold/llm:bm25+repair=1 | 0.791 | 0.531 | 0.334 | 0.882 | 0.874 | 0.771 | 0.143 |
| ig:llm/index:bm25+repair=1 | 0.778 | 0.526 | 0.331 | 0.866 | 0.879 | 0.771 | 0.143 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:bm25 | 0.779 | 0.469 | 0.917 | 0.844 |
| ctx:tfidf | 0.739 | 0.463 | 0.807 | 0.688 |
| ctx:sbert | 0.768 | 0.450 | 0.823 | 0.719 |
| ctx:hybrid | 0.821 | 0.525 | 0.896 | 0.812 |
| ig:llm/llm:bm25 | 0.785 | 0.500 | 0.909 | 0.844 |
| ig:llm/llm:bm25+rnorm=minmax | 0.800 | 0.506 | 0.932 | 0.875 |
| ig:llm/llm:bm25+repair=1 | 0.793 | 0.506 | 0.909 | 0.844 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.807 | 0.506 | 0.932 | 0.875 |
| ig:llm/llm:tfidf | 0.779 | 0.500 | 0.854 | 0.750 |
| ig:llm/llm:tfidf+rnorm=minmax | 0.776 | 0.500 | 0.870 | 0.781 |
| ig:llm/llm:tfidf+repair=1 | 0.787 | 0.500 | 0.854 | 0.750 |
| ig:llm/llm:tfidf+repair=1+rnorm=minmax | 0.777 | 0.500 | 0.870 | 0.781 |
| ig:llm/llm:sbert | 0.788 | 0.475 | 0.846 | 0.781 |
| ig:llm/llm:sbert+rnorm=minmax | 0.787 | 0.475 | 0.829 | 0.750 |
| ig:llm/llm:sbert+repair=1 | 0.788 | 0.475 | 0.846 | 0.781 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.787 | 0.475 | 0.829 | 0.750 |
| ig:llm/llm:hybrid | 0.815 | 0.512 | 0.867 | 0.781 |
| ig:llm/llm:hybrid+rnorm=minmax | 0.827 | 0.519 | 0.891 | 0.812 |
| ig:llm/llm:hybrid+repair=1 | 0.814 | 0.512 | 0.867 | 0.781 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | 0.826 | 0.519 | 0.891 | 0.812 |
| ig:gold/llm:bm25 | 0.804 | 0.519 | 0.893 | 0.812 |
| ig:llm/index:bm25 | 0.783 | 0.506 | 0.898 | 0.812 |
| ig:gold/llm:bm25+repair=1 | 0.804 | 0.519 | 0.893 | 0.812 |
| ig:llm/index:bm25+repair=1 | 0.790 | 0.512 | 0.898 | 0.812 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:bm25 | 0.306 | 0.711 | 0.851 |
| ctx:tfidf | 0.228 | 0.684 | 0.832 |
| ctx:sbert | 0.286 | 0.728 | 0.840 |
| ctx:hybrid | 0.312 | 0.789 | 0.884 |
| ig:llm/llm:bm25 | 0.316 | 0.747 | 0.851 |
| ig:llm/llm:bm25+rnorm=minmax | 0.321 | 0.751 | 0.863 |
| ig:llm/llm:bm25+repair=1 | 0.316 | 0.761 | 0.866 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.321 | 0.751 | 0.878 |
| ig:llm/llm:tfidf | 0.280 | 0.720 | 0.851 |
| ig:llm/llm:tfidf+rnorm=minmax | 0.285 | 0.720 | 0.846 |
| ig:llm/llm:tfidf+repair=1 | 0.280 | 0.720 | 0.865 |
| ig:llm/llm:tfidf+repair=1+rnorm=minmax | 0.285 | 0.720 | 0.846 |
| ig:llm/llm:sbert | 0.301 | 0.728 | 0.858 |
| ig:llm/llm:sbert+rnorm=minmax | 0.298 | 0.733 | 0.847 |
| ig:llm/llm:sbert+repair=1 | 0.301 | 0.728 | 0.858 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.298 | 0.733 | 0.847 |
| ig:llm/llm:hybrid | 0.308 | 0.777 | 0.885 |
| ig:llm/llm:hybrid+rnorm=minmax | 0.312 | 0.782 | 0.886 |
| ig:llm/llm:hybrid+repair=1 | 0.308 | 0.777 | 0.885 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | 0.312 | 0.782 | 0.886 |
| ig:gold/llm:bm25 | 0.311 | 0.772 | 0.882 |
| ig:llm/index:bm25 | 0.302 | 0.756 | 0.851 |
| ig:gold/llm:bm25+repair=1 | 0.311 | 0.772 | 0.882 |
| ig:llm/index:bm25+repair=1 | 0.302 | 0.770 | 0.866 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | aggregate (n=3) | compare (n=10) | explain (n=7) | monitor (n=5) | predict (n=8) |
|---|---|---|---|---|---|
| ctx:bm25 | 0.939 | 0.804 | 0.775 | 0.668 | 0.773 |
| ctx:tfidf | 0.940 | 0.736 | 0.738 | 0.649 | 0.734 |
| ctx:sbert | 0.966 | 0.762 | 0.808 | 0.673 | 0.730 |
| ctx:hybrid | 0.984 | 0.853 | 0.831 | 0.714 | 0.789 |
| ig:llm/llm:bm25 | 0.937 | 0.814 | 0.809 | 0.668 | 0.756 |
| ig:llm/llm:bm25+rnorm=minmax | 0.938 | 0.821 | 0.814 | 0.668 | 0.805 |
| ig:llm/llm:bm25+repair=1 | 0.937 | 0.814 | 0.809 | 0.720 | 0.756 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.938 | 0.821 | 0.814 | 0.711 | 0.805 |
| ig:llm/llm:tfidf | 0.915 | 0.800 | 0.795 | 0.649 | 0.774 |
| ig:llm/llm:tfidf+rnorm=minmax | 0.916 | 0.787 | 0.781 | 0.649 | 0.789 |
| ig:llm/llm:tfidf+repair=1 | 0.915 | 0.800 | 0.795 | 0.700 | 0.774 |
| ig:llm/llm:tfidf+repair=1+rnorm=minmax | 0.916 | 0.787 | 0.781 | 0.657 | 0.789 |
| ig:llm/llm:sbert | 0.965 | 0.817 | 0.844 | 0.673 | 0.711 |
| ig:llm/llm:sbert+rnorm=minmax | 0.981 | 0.789 | 0.831 | 0.673 | 0.748 |
| ig:llm/llm:sbert+repair=1 | 0.965 | 0.817 | 0.844 | 0.675 | 0.711 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.981 | 0.789 | 0.831 | 0.675 | 0.748 |
| ig:llm/llm:hybrid | 0.980 | 0.875 | 0.838 | 0.714 | 0.733 |
| ig:llm/llm:hybrid+rnorm=minmax | 0.984 | 0.855 | 0.844 | 0.714 | 0.800 |
| ig:llm/llm:hybrid+repair=1 | 0.980 | 0.875 | 0.838 | 0.707 | 0.733 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | 0.984 | 0.855 | 0.844 | 0.707 | 0.800 |
| ig:gold/llm:bm25 | 0.964 | 0.838 | 0.827 | 0.728 | 0.741 |
| ig:llm/index:bm25 | 0.937 | 0.811 | 0.791 | 0.668 | 0.756 |
| ig:gold/llm:bm25+repair=1 | 0.964 | 0.838 | 0.827 | 0.728 | 0.741 |
| ig:llm/index:bm25+repair=1 | 0.937 | 0.811 | 0.791 | 0.710 | 0.756 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:bm25 | 0.803 |
| ctx:tfidf | 0.799 |
| ctx:sbert | 0.772 |
| ctx:hybrid | 0.808 |
| ig:llm/llm:bm25 | 0.820 |
| ig:llm/llm:bm25+rnorm=minmax | 0.815 |
| ig:llm/llm:bm25+repair=1 | 0.820 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.815 |
| ig:llm/llm:tfidf | 0.809 |
| ig:llm/llm:tfidf+rnorm=minmax | 0.802 |
| ig:llm/llm:tfidf+repair=1 | 0.809 |
| ig:llm/llm:tfidf+repair=1+rnorm=minmax | 0.802 |
| ig:llm/llm:sbert | 0.802 |
| ig:llm/llm:sbert+rnorm=minmax | 0.777 |
| ig:llm/llm:sbert+repair=1 | 0.802 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.777 |
| ig:llm/llm:hybrid | 0.820 |
| ig:llm/llm:hybrid+rnorm=minmax | 0.820 |
| ig:llm/llm:hybrid+repair=1 | 0.820 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | 0.820 |
| ig:gold/llm:bm25 | 0.840 |
| ig:llm/index:bm25 | 0.835 |
| ig:gold/llm:bm25+repair=1 | 0.840 |
| ig:llm/index:bm25+repair=1 | 0.835 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:llm/llm:bm25 | 0.778 | 0.779 | 0.920 | 0.639 | 0.594 | 0.594 | 0.578 | 0.406 | 0.512 | 0.747 |
| ig:llm/llm:bm25+rnorm=minmax | 0.778 | 0.779 | 0.920 | 0.639 | 0.594 | 0.594 | 0.578 | 0.406 | 0.512 | 0.747 |
| ig:llm/llm:bm25+repair=1 | 0.833 | 0.790 | 0.889 | 0.667 | 0.625 | 0.625 | 0.609 | 0.375 | 0.512 | 0.741 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.833 | 0.790 | 0.889 | 0.667 | 0.625 | 0.625 | 0.609 | 0.375 | 0.512 | 0.741 |
| ig:llm/llm:tfidf | 0.778 | 0.779 | 0.920 | 0.639 | 0.594 | 0.594 | 0.578 | 0.406 | 0.529 | 0.768 |
| ig:llm/llm:tfidf+rnorm=minmax | 0.778 | 0.779 | 0.920 | 0.639 | 0.594 | 0.594 | 0.578 | 0.406 | 0.529 | 0.768 |
| ig:llm/llm:tfidf+repair=1 | 0.833 | 0.790 | 0.889 | 0.667 | 0.625 | 0.625 | 0.609 | 0.375 | 0.529 | 0.762 |
| ig:llm/llm:tfidf+repair=1+rnorm=minmax | 0.833 | 0.790 | 0.889 | 0.667 | 0.625 | 0.625 | 0.609 | 0.375 | 0.529 | 0.762 |
| ig:llm/llm:sbert | 0.778 | 0.779 | 0.920 | 0.639 | 0.594 | 0.594 | 0.578 | 0.406 | 0.495 | 0.712 |
| ig:llm/llm:sbert+rnorm=minmax | 0.778 | 0.779 | 0.920 | 0.639 | 0.594 | 0.594 | 0.578 | 0.406 | 0.495 | 0.712 |
| ig:llm/llm:sbert+repair=1 | 0.833 | 0.790 | 0.889 | 0.667 | 0.625 | 0.625 | 0.609 | 0.375 | 0.495 | 0.707 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.833 | 0.790 | 0.889 | 0.667 | 0.625 | 0.625 | 0.609 | 0.375 | 0.495 | 0.707 |
| ig:llm/llm:hybrid | 0.778 | 0.779 | 0.920 | 0.639 | 0.594 | 0.594 | 0.578 | 0.406 | 0.496 | 0.750 |
| ig:llm/llm:hybrid+rnorm=minmax | 0.778 | 0.779 | 0.920 | 0.639 | 0.594 | 0.594 | 0.578 | 0.406 | 0.496 | 0.750 |
| ig:llm/llm:hybrid+repair=1 | 0.833 | 0.790 | 0.889 | 0.667 | 0.625 | 0.625 | 0.609 | 0.375 | 0.496 | 0.744 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | 0.833 | 0.790 | 0.889 | 0.667 | 0.625 | 0.625 | 0.609 | 0.375 | 0.496 | 0.744 |
| ig:gold/llm:bm25 | 1.000 | 1.000 | 1.000 | 0.917 | 0.938 | 0.938 | 0.938 | 0.062 | 0.492 | 0.781 |
| ig:llm/index:bm25 | 0.778 | 0.779 | 0.920 | 0.611 | 0.594 | 0.594 | 0.568 | 0.406 | 0.512 | 0.747 |
| ig:gold/llm:bm25+repair=1 | 1.000 | 1.000 | 1.000 | 0.917 | 0.938 | 0.938 | 0.938 | 0.062 | 0.492 | 0.781 |
| ig:llm/index:bm25+repair=1 | 0.833 | 0.790 | 0.889 | 0.667 | 0.656 | 0.656 | 0.630 | 0.344 | 0.516 | 0.747 |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:bm25 | – | 16.2 / 16.6 / 24.3 | – | – | – | – | 16.6 / 17.0 / 24.7 | 0.599 |
| ctx:tfidf | – | 13.2 / 13.1 / 14.6 | – | – | – | – | 13.6 / 13.6 / 15.1 | 0.492 |
| ctx:sbert | – | 138.7 / 126.4 / 142.9 | – | – | – | – | 138.8 / 126.6 / 143.0 | 5.0 |
| ctx:hybrid | – | 149.1 / 151.4 / 164.3 | – | – | – | – | 149.5 / 151.8 / 164.9 | 5.382 |
| ig:llm/llm:bm25 | 9760.4 / 9548.3 / 13252.5 | 15.1 / 16.4 / 22.0 | 4617.4 / 5064.9 / 9593.8 | 44.0 / 26.8 / 123.4 | 722.4 / 96.8 / 4637.6 | 0.3 / 0.2 / 0.8 | 15145.6 / 15229.6 / 22996.0 | 67.52 |
| ig:llm/llm:bm25+rnorm=minmax | 4.8 / 3.8 / 8.7 | 19.1 / 7.9 / 12.4 | 1.9 / 2.0 / 3.5 | 20.7 / 25.2 / 46.7 | 1018.0 / 177.9 / 5734.7 | 0.3 / 0.3 / 0.8 | 1047.1 / 223.4 / 5768.1 | 14.798 |
| ig:llm/llm:bm25+repair=1 | 1194.8 / 6.9 / 5544.5 | 14.6 / 15.9 / 22.1 | 1042.1 / 2.5 / 5232.8 | 22.4 / 27.2 / 48.3 | 1096.1 / 156.6 / 5831.0 | 0.3 / 0.2 / 0.7 | 3357.2 / 2605.5 / 7538.0 | 26.601 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 5.9 / 5.2 / 9.6 | 14.8 / 16.2 / 23.0 | 2.1 / 2.3 / 4.6 | 21.7 / 30.5 / 46.3 | 1181.1 / 182.5 / 4585.9 | 0.3 / 0.2 / 0.8 | 1212.6 / 225.7 / 4625.2 | 14.951 |
| ig:llm/llm:tfidf | 6.2 / 5.4 / 11.7 | 4.9 / 4.8 / 5.5 | 1.6 / 1.0 / 5.1 | 13.1 / 15.4 / 30.9 | 681.8 / 66.7 / 4198.5 | 0.2 / 0.1 / 0.8 | 703.8 / 97.9 / 4225.7 | 10.393 |
| ig:llm/llm:tfidf+rnorm=minmax | 4.2 / 4.0 / 7.6 | 5.6 / 5.6 / 6.4 | 1.4 / 1.2 / 3.0 | 15.3 / 14.5 / 39.0 | 781.7 / 80.7 / 4846.3 | 0.3 / 0.2 / 0.9 | 803.9 / 106.9 / 4872.6 | 11.219 |
| ig:llm/llm:tfidf+repair=1 | 6.4 / 5.1 / 14.1 | 12.2 / 12.6 / 14.2 | 2.0 / 1.8 / 4.2 | 20.9 / 31.8 / 43.7 | 1090.7 / 164.2 / 5620.9 | 0.3 / 0.3 / 0.7 | 1121.7 / 211.6 / 5671.1 | 15.493 |
| ig:llm/llm:tfidf+repair=1+rnorm=minmax | 5.7 / 5.2 / 10.1 | 12.6 / 13.4 / 14.6 | 2.1 / 2.0 / 4.2 | 38.7 / 21.8 / 50.7 | 1085.7 / 164.6 / 5134.9 | 0.3 / 0.2 / 0.8 | 1134.1 / 202.3 / 5165.6 | 13.655 |
| ig:llm/llm:sbert | 4.9 / 4.4 / 8.8 | 122.9 / 120.8 / 130.9 | 3.1 / 1.6 / 14.7 | 34.9 / 27.6 / 103.3 | 1107.7 / 114.7 / 6051.4 | 0.3 / 0.2 / 0.6 | 1152.5 / 164.4 / 6105.9 | 18.226 |
| ig:llm/llm:sbert+rnorm=minmax | 5.2 / 4.8 / 8.8 | 120.4 / 119.3 / 128.3 | 2.0 / 1.4 / 5.7 | 25.9 / 26.7 / 75.3 | 996.8 / 105.4 / 6229.4 | 0.3 / 0.2 / 0.7 | 1031.5 / 140.7 / 6296.6 | 17.335 |
| ig:llm/llm:sbert+repair=1 | 8.0 / 6.3 / 18.8 | 81.1 / 77.5 / 93.4 | 2.0 / 1.3 / 6.3 | 36.5 / 21.1 / 49.3 | 697.5 / 68.2 / 4149.0 | 0.2 / 0.1 / 0.6 | 745.0 / 107.2 / 4203.7 | 13.119 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 7.4 / 6.8 / 15.5 | 95.5 / 81.5 / 120.8 | 2.3 / 1.6 / 7.0 | 19.1 / 21.6 / 46.6 | 794.4 / 73.9 / 5153.6 | 0.2 / 0.2 / 0.6 | 824.5 / 111.5 / 5183.0 | 15.687 |
| ig:llm/llm:hybrid | 4.3 / 4.1 / 7.5 | 139.4 / 136.6 / 149.4 | 2.1 / 1.7 / 5.8 | 40.2 / 37.4 / 59.2 | 1171.9 / 132.5 / 6401.0 | 0.3 / 0.3 / 0.9 | 1220.5 / 181.4 / 6458.0 | 20.871 |
| ig:llm/llm:hybrid+rnorm=minmax | 4.4 / 4.1 / 7.2 | 140.8 / 139.7 / 154.2 | 1.9 / 1.5 / 5.1 | 39.0 / 25.1 / 56.8 | 1010.9 / 93.2 / 5510.6 | 0.3 / 0.2 / 0.9 | 1057.9 / 168.4 / 5576.2 | 19.888 |
| ig:llm/llm:hybrid+repair=1 | 6.6 / 5.7 / 13.0 | 135.5 / 137.1 / 148.2 | 2.2 / 1.8 / 4.5 | 65.3 / 24.5 / 53.0 | 1511.6 / 191.3 / 5417.1 | 0.3 / 0.3 / 0.8 | 1587.7 / 254.7 / 5486.2 | 19.188 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | 9.2 / 7.8 / 22.1 | 85.3 / 84.6 / 93.1 | 2.2 / 1.7 / 5.7 | 20.1 / 22.9 / 42.5 | 1030.9 / 153.9 / 4919.1 | 0.3 / 0.2 / 0.9 | 1064.0 / 219.6 / 4978.5 | 14.887 |
| ig:gold/llm:bm25 | 0.1 / 0.1 / 0.2 | 4.1 / 3.6 / 6.7 | 1879.7 / 2191.0 / 4132.9 | 36.6 / 40.4 / 54.1 | 1521.5 / 791.8 / 5162.1 | 0.3 / 0.2 / 0.4 | 3440.4 / 2988.4 / 8155.3 | 31.2 |
| ig:llm/index:bm25 | 5.1 / 4.9 / 7.7 | 15.0 / 15.8 / 22.2 | 1.6 / 0.5 / 5.5 | 23.2 / 23.7 / 45.9 | 1392.8 / 212.3 / 5637.4 | 0.3 / 0.2 / 0.9 | 1424.3 / 255.7 / 5780.6 | 18.67 |
| ig:gold/llm:bm25+repair=1 | 0.1 / 0.1 / 0.2 | 4.7 / 4.0 / 7.0 | 448.6 / 1.7 / 4866.4 | 24.2 / 24.0 / 45.6 | 1158.1 / 451.0 / 5425.1 | 0.2 / 0.2 / 0.3 | 1632.8 / 614.0 / 6065.6 | 22.616 |
| ig:llm/index:bm25+repair=1 | 8.3 / 7.1 / 15.1 | 5.1 / 5.2 / 8.1 | 2.0 / 0.5 / 7.3 | 15.4 / 22.5 / 29.3 | 1077.7 / 171.1 / 4101.5 | 0.2 / 0.1 / 0.7 | 1104.6 / 210.6 / 4143.6 | 16.318 |

Context index build (one-off, ms): bm25: 90 (cached), hybrid: 17282 (cached), sbert: 1282 (cached), tfidf: 39 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:llm/llm:hybrid+rnorm=minmax | ctx:hybrid | ndcg@10 | +0.005 | [-0.004, +0.016] | 0.304 | 9/8 |
| ig:llm/llm:hybrid+rnorm=minmax | ctx:hybrid | mrr | -0.005 | [-0.014, +0.000] | 1.000 | 0/1 |
| ig:llm/llm:hybrid+rnorm=minmax | ctx:hybrid | useful@1 | +0.000 | [+0.000, +0.000] | 1.000 | 0/0 |
| ig:llm/index:bm25 | ctx:bm25 | ndcg@10 | +0.001 | [-0.019, +0.019] | 0.923 | 12/7 |
| ig:llm/index:bm25 | ctx:bm25 | mrr | -0.017 | [-0.064, +0.014] | 1.000 | 1/1 |
| ig:llm/index:bm25 | ctx:bm25 | useful@1 | -0.029 | [-0.086, +0.000] | 1.000 | 0/1 |
| ig:llm/llm:bm25+rnorm=minmax | ctx:bm25 | ndcg@10 | +0.019 | [+0.008, +0.033] | 0.002 | 12/6 |
| ig:llm/llm:bm25+rnorm=minmax | ctx:bm25 | mrr | +0.014 | [+0.000, +0.043] | 1.000 | 1/0 |
| ig:llm/llm:bm25+rnorm=minmax | ctx:bm25 | useful@1 | +0.029 | [+0.000, +0.086] | 1.000 | 1/0 |
| ig:llm/llm:hybrid+repair=1 | ctx:hybrid | ndcg@10 | -0.006 | [-0.030, +0.013] | 0.681 | 10/11 |
| ig:llm/llm:hybrid+repair=1 | ctx:hybrid | mrr | -0.026 | [-0.074, +0.000] | 0.504 | 0/2 |
| ig:llm/llm:hybrid+repair=1 | ctx:hybrid | useful@1 | -0.029 | [-0.086, +0.000] | 1.000 | 0/1 |
| ig:llm/llm:bm25 | ctx:bm25 | ndcg@10 | +0.005 | [-0.015, +0.023] | 0.636 | 11/7 |
| ig:llm/llm:bm25 | ctx:bm25 | mrr | -0.007 | [-0.064, +0.043] | 1.000 | 1/1 |
| ig:llm/llm:bm25 | ctx:bm25 | useful@1 | +0.000 | [-0.086, +0.086] | 1.000 | 1/1 |
| ig:llm/llm:hybrid | ctx:hybrid | ndcg@10 | -0.005 | [-0.028, +0.014] | 0.734 | 9/10 |
| ig:llm/llm:hybrid | ctx:hybrid | mrr | -0.026 | [-0.074, +0.000] | 0.504 | 0/2 |
| ig:llm/llm:hybrid | ctx:hybrid | useful@1 | -0.029 | [-0.086, +0.000] | 1.000 | 0/1 |
| ig:llm/llm:tfidf+rnorm=minmax | ctx:tfidf | ndcg@10 | +0.033 | [+0.015, +0.053] | 0.001 | 17/3 |
| ig:llm/llm:tfidf+rnorm=minmax | ctx:tfidf | mrr | +0.057 | [+0.005, +0.124] | 0.131 | 4/0 |
| ig:llm/llm:tfidf+rnorm=minmax | ctx:tfidf | useful@1 | +0.086 | [+0.000, +0.171] | 0.255 | 3/0 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | ndcg@10 | +0.017 | [-0.005, +0.040] | 0.158 | 16/9 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | mrr | +0.005 | [-0.055, +0.064] | 0.896 | 4/4 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | useful@1 | +0.029 | [-0.057, +0.114] | 1.000 | 2/1 |
| ig:llm/llm:tfidf | ctx:tfidf | ndcg@10 | +0.035 | [+0.013, +0.063] | 0.004 | 16/4 |
| ig:llm/llm:tfidf | ctx:tfidf | mrr | +0.043 | [-0.019, +0.110] | 0.254 | 4/1 |
| ig:llm/llm:tfidf | ctx:tfidf | useful@1 | +0.057 | [-0.057, +0.171] | 0.622 | 3/1 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | ctx:hybrid | ndcg@10 | +0.005 | [-0.005, +0.015] | 0.409 | 10/9 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | ctx:hybrid | mrr | -0.005 | [-0.014, +0.000] | 1.000 | 0/1 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | ctx:hybrid | useful@1 | +0.000 | [+0.000, +0.000] | 1.000 | 0/0 |
| ig:llm/index:bm25+repair=1 | ctx:bm25 | ndcg@10 | +0.007 | [-0.016, +0.029] | 0.577 | 13/8 |
| ig:llm/index:bm25+repair=1 | ctx:bm25 | mrr | -0.017 | [-0.064, +0.014] | 1.000 | 1/1 |
| ig:llm/index:bm25+repair=1 | ctx:bm25 | useful@1 | -0.029 | [-0.086, +0.000] | 1.000 | 0/1 |
| ig:llm/llm:sbert+rnorm=minmax | ctx:sbert | ndcg@10 | +0.017 | [-0.006, +0.040] | 0.166 | 15/8 |
| ig:llm/llm:sbert+rnorm=minmax | ctx:sbert | mrr | +0.005 | [-0.055, +0.064] | 0.896 | 4/4 |
| ig:llm/llm:sbert+rnorm=minmax | ctx:sbert | useful@1 | +0.029 | [-0.057, +0.114] | 1.000 | 2/1 |
| ig:llm/llm:sbert | ctx:sbert | ndcg@10 | +0.018 | [-0.016, +0.054] | 0.348 | 13/10 |
| ig:llm/llm:sbert | ctx:sbert | mrr | +0.021 | [-0.058, +0.105] | 0.645 | 4/4 |
| ig:llm/llm:sbert | ctx:sbert | useful@1 | +0.057 | [-0.057, +0.171] | 0.626 | 3/1 |
| ig:llm/llm:tfidf+repair=1 | ctx:tfidf | ndcg@10 | +0.043 | [+0.017, +0.071] | 0.001 | 18/4 |
| ig:llm/llm:tfidf+repair=1 | ctx:tfidf | mrr | +0.043 | [-0.019, +0.110] | 0.254 | 4/1 |
| ig:llm/llm:tfidf+repair=1 | ctx:tfidf | useful@1 | +0.057 | [-0.057, +0.171] | 0.622 | 3/1 |
| ig:gold/llm:bm25+repair=1 | ctx:bm25 | ndcg@10 | +0.023 | [-0.002, +0.048] | 0.086 | 20/9 |
| ig:gold/llm:bm25+repair=1 | ctx:bm25 | mrr | -0.021 | [-0.086, +0.029] | 0.750 | 1/2 |
| ig:gold/llm:bm25+repair=1 | ctx:bm25 | useful@1 | -0.029 | [-0.143, +0.057] | 1.000 | 1/2 |
| ig:llm/llm:bm25+repair=1 | ctx:bm25 | ndcg@10 | +0.013 | [-0.011, +0.035] | 0.319 | 13/7 |
| ig:llm/llm:bm25+repair=1 | ctx:bm25 | mrr | -0.007 | [-0.064, +0.043] | 1.000 | 1/1 |
| ig:llm/llm:bm25+repair=1 | ctx:bm25 | useful@1 | +0.000 | [-0.086, +0.086] | 1.000 | 1/1 |
| ig:gold/llm:bm25 | ctx:bm25 | ndcg@10 | +0.023 | [-0.002, +0.048] | 0.086 | 20/9 |
| ig:gold/llm:bm25 | ctx:bm25 | mrr | -0.021 | [-0.086, +0.029] | 0.750 | 1/2 |
| ig:gold/llm:bm25 | ctx:bm25 | useful@1 | -0.029 | [-0.143, +0.057] | 1.000 | 1/2 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | ndcg@10 | +0.018 | [-0.016, +0.054] | 0.340 | 14/11 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | mrr | +0.021 | [-0.058, +0.105] | 0.645 | 4/4 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | useful@1 | +0.057 | [-0.057, +0.171] | 0.626 | 3/1 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | ctx:bm25 | ndcg@10 | +0.025 | [+0.011, +0.042] | 0.001 | 14/6 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | ctx:bm25 | mrr | +0.014 | [+0.000, +0.043] | 1.000 | 1/0 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | ctx:bm25 | useful@1 | +0.029 | [+0.000, +0.086] | 1.000 | 1/0 |
| ig:llm/llm:tfidf+repair=1+rnorm=minmax | ctx:tfidf | ndcg@10 | +0.034 | [+0.016, +0.055] | 0.000 | 18/3 |
| ig:llm/llm:tfidf+repair=1+rnorm=minmax | ctx:tfidf | mrr | +0.057 | [+0.005, +0.124] | 0.131 | 4/0 |
| ig:llm/llm:tfidf+repair=1+rnorm=minmax | ctx:tfidf | useful@1 | +0.086 | [+0.000, +0.171] | 0.255 | 3/0 |
