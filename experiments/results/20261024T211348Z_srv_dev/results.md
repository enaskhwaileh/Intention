# IGBench results (20261024T211348Z_srv_dev)

Benchmark `igbench-v1` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:bm25 | 0.768 | 0.486 | 0.323 | 0.851 | 0.895 | 0.800 | 0.143 |
| ctx:tfidf | 0.730 | 0.469 | 0.314 | 0.832 | 0.795 | 0.657 | 0.200 |
| ctx:lsa | 0.743 | 0.486 | 0.320 | 0.851 | 0.849 | 0.743 | 0.143 |
| ctx:sbert | 0.769 | 0.474 | 0.297 | 0.840 | 0.838 | 0.743 | 0.143 |
| ctx:hybrid | 0.814 | 0.543 | 0.334 | 0.884 | 0.876 | 0.771 | 0.143 |
| ig:gold/gold:bm25 | 0.796 | 0.537 | 0.334 | 0.882 | 0.879 | 0.771 | 0.143 |
| ig:rule/index:bm25 | 0.788 | 0.531 | 0.331 | 0.875 | 0.909 | 0.829 | 0.114 |
| ig:gold/gold:tfidf | 0.801 | 0.520 | 0.337 | 0.875 | 0.876 | 0.771 | 0.171 |
| ig:rule/index:tfidf | 0.762 | 0.520 | 0.323 | 0.842 | 0.841 | 0.714 | 0.143 |
| ig:gold/gold:sbert | 0.815 | 0.526 | 0.326 | 0.875 | 0.927 | 0.886 | 0.086 |
| ig:rule/index:sbert | 0.784 | 0.531 | 0.323 | 0.871 | 0.868 | 0.829 | 0.143 |
| ig:gold/gold:hybrid | 0.821 | 0.531 | 0.340 | 0.891 | 0.900 | 0.829 | 0.114 |
| ig:rule/index:hybrid | 0.811 | 0.549 | 0.337 | 0.891 | 0.886 | 0.771 | 0.114 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:bm25 | 0.779 | 0.469 | 0.917 | 0.844 |
| ctx:tfidf | 0.739 | 0.463 | 0.807 | 0.688 |
| ctx:lsa | 0.744 | 0.463 | 0.850 | 0.750 |
| ctx:sbert | 0.768 | 0.450 | 0.823 | 0.719 |
| ctx:hybrid | 0.821 | 0.525 | 0.896 | 0.812 |
| ig:gold/gold:bm25 | 0.809 | 0.525 | 0.898 | 0.812 |
| ig:rule/index:bm25 | 0.801 | 0.519 | 0.932 | 0.875 |
| ig:gold/gold:tfidf | 0.816 | 0.519 | 0.896 | 0.812 |
| ig:rule/index:tfidf | 0.774 | 0.519 | 0.857 | 0.750 |
| ig:gold/gold:sbert | 0.818 | 0.506 | 0.921 | 0.875 |
| ig:rule/index:sbert | 0.784 | 0.512 | 0.856 | 0.812 |
| ig:gold/gold:hybrid | 0.829 | 0.512 | 0.922 | 0.875 |
| ig:rule/index:hybrid | 0.818 | 0.531 | 0.906 | 0.812 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:bm25 | 0.306 | 0.711 | 0.851 |
| ctx:tfidf | 0.228 | 0.684 | 0.832 |
| ctx:lsa | 0.276 | 0.713 | 0.851 |
| ctx:sbert | 0.286 | 0.728 | 0.840 |
| ctx:hybrid | 0.312 | 0.789 | 0.884 |
| ig:gold/gold:bm25 | 0.311 | 0.781 | 0.882 |
| ig:rule/index:bm25 | 0.321 | 0.782 | 0.875 |
| ig:gold/gold:tfidf | 0.337 | 0.740 | 0.875 |
| ig:rule/index:tfidf | 0.270 | 0.746 | 0.842 |
| ig:gold/gold:sbert | 0.362 | 0.776 | 0.875 |
| ig:rule/index:sbert | 0.329 | 0.758 | 0.871 |
| ig:gold/gold:hybrid | 0.349 | 0.778 | 0.891 |
| ig:rule/index:hybrid | 0.318 | 0.796 | 0.891 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | aggregate (n=3) | compare (n=10) | explain (n=7) | monitor (n=5) | predict (n=8) |
|---|---|---|---|---|---|
| ctx:bm25 | 0.939 | 0.804 | 0.775 | 0.668 | 0.773 |
| ctx:tfidf | 0.940 | 0.736 | 0.738 | 0.649 | 0.734 |
| ctx:lsa | 0.936 | 0.815 | 0.732 | 0.612 | 0.693 |
| ctx:sbert | 0.966 | 0.762 | 0.808 | 0.673 | 0.730 |
| ctx:hybrid | 0.984 | 0.853 | 0.831 | 0.714 | 0.789 |
| ig:gold/gold:bm25 | 0.964 | 0.855 | 0.827 | 0.728 | 0.741 |
| ig:rule/index:bm25 | 0.964 | 0.831 | 0.807 | 0.699 | 0.770 |
| ig:gold/gold:tfidf | 0.938 | 0.852 | 0.843 | 0.747 | 0.747 |
| ig:rule/index:tfidf | 0.938 | 0.769 | 0.791 | 0.690 | 0.762 |
| ig:gold/gold:sbert | 0.983 | 0.874 | 0.878 | 0.720 | 0.696 |
| ig:rule/index:sbert | 0.983 | 0.817 | 0.844 | 0.678 | 0.686 |
| ig:gold/gold:hybrid | 0.983 | 0.883 | 0.852 | 0.768 | 0.730 |
| ig:rule/index:hybrid | 0.983 | 0.892 | 0.829 | 0.705 | 0.737 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:bm25 | 0.803 |
| ctx:tfidf | 0.799 |
| ctx:lsa | 0.822 |
| ctx:sbert | 0.772 |
| ctx:hybrid | 0.808 |
| ig:gold/gold:bm25 | 0.860 |
| ig:rule/index:bm25 | 0.843 |
| ig:gold/gold:tfidf | 0.819 |
| ig:rule/index:tfidf | 0.825 |
| ig:gold/gold:sbert | 0.823 |
| ig:rule/index:sbert | 0.799 |
| ig:gold/gold:hybrid | 0.834 |
| ig:rule/index:hybrid | 0.841 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:gold/gold:bm25 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.497 | 0.789 |
| ig:rule/index:bm25 | 1.000 | 0.825 | 0.970 | 0.833 | 0.812 | 0.812 | 0.688 | 0.188 | 0.482 | 0.784 |
| ig:gold/gold:tfidf | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.538 | 0.803 |
| ig:rule/index:tfidf | 1.000 | 0.825 | 0.970 | 0.833 | 0.812 | 0.812 | 0.688 | 0.188 | 0.497 | 0.802 |
| ig:gold/gold:sbert | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.535 | 0.771 |
| ig:rule/index:sbert | 1.000 | 0.825 | 0.970 | 0.833 | 0.812 | 0.812 | 0.688 | 0.188 | 0.479 | 0.753 |
| ig:gold/gold:hybrid | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.507 | 0.795 |
| ig:rule/index:hybrid | 1.000 | 0.825 | 0.970 | 0.833 | 0.812 | 0.812 | 0.688 | 0.188 | 0.474 | 0.788 |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:bm25 | – | 4.9 / 5.0 / 7.4 | – | – | – | – | 5.1 / 5.1 / 7.5 | 0.182 |
| ctx:tfidf | – | 4.2 / 4.0 / 4.5 | – | – | – | – | 4.3 / 4.2 / 4.7 | 0.155 |
| ctx:lsa | – | 26.1 / 25.9 / 27.9 | – | – | – | – | 26.3 / 26.1 / 28.1 | 0.946 |
| ctx:sbert | – | 82.4 / 73.3 / 81.0 | – | – | – | – | 82.5 / 73.3 / 81.0 | 2.97 |
| ctx:hybrid | – | 79.0 / 79.0 / 83.9 | – | – | – | – | 79.1 / 79.1 / 84.1 | 2.849 |
| ig:gold/gold:bm25 | 0.1 / 0.1 / 0.1 | 5.0 / 4.9 / 7.8 | 0.2 / 0.1 / 0.3 | 958.4 / 445.4 / 2662.1 | 980.3 / 385.0 / 3952.5 | 0.1 / 0.1 / 0.1 | 1945.3 / 1310.2 / 5547.6 | 70.078 |
| ig:rule/index:bm25 | 0.4 / 0.2 / 0.7 | 4.9 / 5.0 / 7.6 | 0.3 / 0.2 / 0.4 | 109.6 / 26.3 / 342.5 | 878.7 / 139.9 / 3917.3 | 0.1 / 0.1 / 0.1 | 995.3 / 317.3 / 4054.4 | 35.868 |
| ig:gold/gold:tfidf | 0.1 / 0.1 / 0.1 | 13.1 / 5.3 / 11.8 | 0.1 / 0.1 / 0.2 | 62.3 / 41.1 / 201.1 | 882.7 / 238.3 / 3876.8 | 0.1 / 0.1 / 0.1 | 959.5 / 318.0 / 3978.9 | 34.587 |
| ig:rule/index:tfidf | 0.2 / 0.2 / 0.2 | 5.2 / 5.2 / 7.4 | 0.2 / 0.2 / 0.3 | 37.0 / 18.8 / 85.6 | 762.1 / 119.0 / 3751.7 | 0.1 / 0.1 / 0.1 | 805.7 / 186.4 / 3781.4 | 29.043 |
| ig:gold/gold:sbert | 0.1 / 0.1 / 0.1 | 92.0 / 84.5 / 92.6 | 0.2 / 0.2 / 0.2 | 390.3 / 190.9 / 1021.0 | 846.4 / 252.6 / 3946.6 | 0.1 / 0.1 / 0.1 | 1330.0 / 686.6 / 4865.0 | 47.945 |
| ig:rule/index:sbert | 0.2 / 0.2 / 0.2 | 83.2 / 82.8 / 94.3 | 0.2 / 0.3 / 0.3 | 48.2 / 20.8 / 124.3 | 797.3 / 198.1 / 4013.0 | 0.1 / 0.1 / 0.1 | 930.1 / 316.2 / 4128.9 | 33.533 |
| ig:gold/gold:hybrid | 0.1 / 0.1 / 0.1 | 95.7 / 88.8 / 100.7 | 0.2 / 0.2 / 0.3 | 41.5 / 19.5 / 149.5 | 972.9 / 293.5 / 3964.4 | 0.1 / 0.1 / 0.1 | 1111.5 / 433.9 / 4079.7 | 40.071 |
| ig:rule/index:hybrid | 0.2 / 0.2 / 0.2 | 87.2 / 86.9 / 96.3 | 0.3 / 0.3 / 0.3 | 32.1 / 18.4 / 47.9 | 912.5 / 152.1 / 4088.4 | 0.1 / 0.1 / 0.1 | 1033.3 / 283.3 / 4190.3 | 37.246 |

Context index build (one-off, ms): bm25: 59 (cached), hybrid: 10090 (cached), lsa: 116 (cached), sbert: 942 (cached), tfidf: 8 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:rule/index:tfidf | ctx:tfidf | ndcg@10 | +0.032 | [+0.011, +0.054] | 0.005 | 19/5 |
| ig:rule/index:tfidf | ctx:tfidf | mrr | +0.045 | [+0.002, +0.098] | 0.094 | 5/1 |
| ig:rule/index:tfidf | ctx:tfidf | useful@1 | +0.057 | [+0.000, +0.143] | 0.505 | 2/0 |
| ig:gold/gold:tfidf | ctx:tfidf | ndcg@10 | +0.069 | [+0.035, +0.106] | 0.000 | 23/5 |
| ig:gold/gold:tfidf | ctx:tfidf | mrr | +0.081 | [-0.005, +0.167] | 0.088 | 7/1 |
| ig:gold/gold:tfidf | ctx:tfidf | useful@1 | +0.114 | [-0.029, +0.257] | 0.223 | 5/1 |
| ig:rule/index:sbert | ctx:sbert | ndcg@10 | +0.015 | [-0.027, +0.058] | 0.535 | 17/12 |
| ig:rule/index:sbert | ctx:sbert | mrr | +0.030 | [-0.052, +0.117] | 0.495 | 5/5 |
| ig:rule/index:sbert | ctx:sbert | useful@1 | +0.086 | [-0.029, +0.229] | 0.369 | 4/1 |
| ig:rule/index:hybrid | ctx:hybrid | ndcg@10 | -0.003 | [-0.029, +0.022] | 0.843 | 13/12 |
| ig:rule/index:hybrid | ctx:hybrid | mrr | +0.009 | [-0.052, +0.081] | 0.751 | 2/2 |
| ig:rule/index:hybrid | ctx:hybrid | useful@1 | +0.000 | [-0.114, +0.114] | 1.000 | 2/2 |
| ig:rule/index:bm25 | ctx:bm25 | ndcg@10 | +0.019 | [-0.000, +0.041] | 0.069 | 16/8 |
| ig:rule/index:bm25 | ctx:bm25 | mrr | +0.014 | [-0.009, +0.052] | 0.751 | 2/1 |
| ig:rule/index:bm25 | ctx:bm25 | useful@1 | +0.029 | [+0.000, +0.086] | 1.000 | 1/0 |
| ig:gold/gold:bm25 | ctx:bm25 | ndcg@10 | +0.027 | [+0.003, +0.053] | 0.047 | 21/8 |
| ig:gold/gold:bm25 | ctx:bm25 | mrr | -0.017 | [-0.081, +0.038] | 0.750 | 2/2 |
| ig:gold/gold:bm25 | ctx:bm25 | useful@1 | -0.029 | [-0.143, +0.057] | 1.000 | 1/2 |
| ig:gold/gold:hybrid | ctx:hybrid | ndcg@10 | +0.006 | [-0.025, +0.035] | 0.726 | 16/11 |
| ig:gold/gold:hybrid | ctx:hybrid | mrr | +0.024 | [-0.052, +0.100] | 0.626 | 3/2 |
| ig:gold/gold:hybrid | ctx:hybrid | useful@1 | +0.057 | [-0.057, +0.171] | 0.626 | 3/1 |
| ig:gold/gold:sbert | ctx:sbert | ndcg@10 | +0.045 | [-0.007, +0.095] | 0.112 | 23/7 |
| ig:gold/gold:sbert | ctx:sbert | mrr | +0.089 | [-0.015, +0.200] | 0.101 | 7/2 |
| ig:gold/gold:sbert | ctx:sbert | useful@1 | +0.143 | [+0.000, +0.286] | 0.117 | 6/1 |
