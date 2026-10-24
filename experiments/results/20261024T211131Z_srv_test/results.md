# IGBench results (20261024T211131Z_srv_test)

Benchmark `igbench-v1-test` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:bm25 | 0.828 | 0.530 | 0.345 | 0.935 | 0.917 | 0.850 | 0.100 |
| ctx:tfidf | 0.775 | 0.460 | 0.315 | 0.882 | 0.765 | 0.600 | 0.300 |
| ctx:lsa | 0.806 | 0.540 | 0.345 | 0.896 | 0.829 | 0.700 | 0.150 |
| ctx:sbert | 0.690 | 0.340 | 0.270 | 0.780 | 0.814 | 0.700 | 0.150 |
| ctx:hybrid | 0.845 | 0.560 | 0.335 | 0.907 | 0.950 | 0.900 | 0.050 |
| ig:gold/gold:bm25 | 0.857 | 0.550 | 0.355 | 0.948 | 0.975 | 0.950 | 0.000 |
| ig:rule/index:bm25 | 0.826 | 0.540 | 0.355 | 0.948 | 0.900 | 0.800 | 0.050 |
| ig:gold/gold:tfidf | 0.834 | 0.510 | 0.345 | 0.935 | 0.917 | 0.850 | 0.000 |
| ig:rule/index:tfidf | 0.823 | 0.500 | 0.340 | 0.927 | 0.917 | 0.850 | 0.000 |
| ig:gold/gold:sbert | 0.786 | 0.540 | 0.330 | 0.908 | 0.929 | 0.900 | 0.000 |
| ig:rule/index:sbert | 0.747 | 0.490 | 0.325 | 0.901 | 0.879 | 0.800 | 0.100 |
| ig:gold/gold:hybrid | 0.842 | 0.570 | 0.350 | 0.944 | 0.950 | 0.900 | 0.000 |
| ig:rule/index:hybrid | 0.828 | 0.570 | 0.350 | 0.944 | 0.925 | 0.850 | 0.050 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:bm25 | 0.823 | 0.516 | 0.912 | 0.842 |
| ctx:tfidf | 0.770 | 0.442 | 0.752 | 0.579 |
| ctx:lsa | 0.799 | 0.526 | 0.820 | 0.684 |
| ctx:sbert | 0.680 | 0.316 | 0.804 | 0.684 |
| ctx:hybrid | 0.839 | 0.547 | 0.947 | 0.895 |
| ig:gold/gold:bm25 | 0.854 | 0.537 | 0.974 | 0.947 |
| ig:rule/index:bm25 | 0.821 | 0.526 | 0.895 | 0.789 |
| ig:gold/gold:tfidf | 0.833 | 0.495 | 0.912 | 0.842 |
| ig:rule/index:tfidf | 0.821 | 0.484 | 0.912 | 0.842 |
| ig:gold/gold:sbert | 0.780 | 0.526 | 0.925 | 0.895 |
| ig:rule/index:sbert | 0.739 | 0.474 | 0.873 | 0.789 |
| ig:gold/gold:hybrid | 0.835 | 0.558 | 0.947 | 0.895 |
| ig:rule/index:hybrid | 0.821 | 0.558 | 0.921 | 0.842 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:bm25 | 0.414 | 0.810 | 0.935 |
| ctx:tfidf | 0.340 | 0.736 | 0.882 |
| ctx:lsa | 0.352 | 0.787 | 0.896 |
| ctx:sbert | 0.352 | 0.591 | 0.780 |
| ctx:hybrid | 0.424 | 0.833 | 0.907 |
| ig:gold/gold:bm25 | 0.395 | 0.829 | 0.948 |
| ig:rule/index:bm25 | 0.327 | 0.817 | 0.948 |
| ig:gold/gold:tfidf | 0.377 | 0.788 | 0.935 |
| ig:rule/index:tfidf | 0.377 | 0.775 | 0.927 |
| ig:gold/gold:sbert | 0.345 | 0.820 | 0.908 |
| ig:rule/index:sbert | 0.282 | 0.766 | 0.901 |
| ig:gold/gold:hybrid | 0.345 | 0.843 | 0.944 |
| ig:rule/index:hybrid | 0.295 | 0.839 | 0.944 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | compare (n=8) | explain (n=3) | monitor (n=5) | predict (n=4) |
|---|---|---|---|---|
| ctx:bm25 | 0.812 | 0.800 | 0.750 | 0.909 |
| ctx:tfidf | 0.738 | 0.729 | 0.772 | 0.864 |
| ctx:lsa | 0.836 | 0.797 | 0.675 | 0.873 |
| ctx:sbert | 0.665 | 0.675 | 0.683 | 0.756 |
| ctx:hybrid | 0.847 | 0.763 | 0.809 | 0.918 |
| ig:gold/gold:bm25 | 0.805 | 0.833 | 0.849 | 0.918 |
| ig:rule/index:bm25 | 0.798 | 0.788 | 0.807 | 0.861 |
| ig:gold/gold:tfidf | 0.780 | 0.797 | 0.873 | 0.900 |
| ig:rule/index:tfidf | 0.774 | 0.795 | 0.857 | 0.876 |
| ig:gold/gold:sbert | 0.781 | 0.877 | 0.702 | 0.842 |
| ig:rule/index:sbert | 0.784 | 0.871 | 0.635 | 0.728 |
| ig:gold/gold:hybrid | 0.811 | 0.841 | 0.801 | 0.893 |
| ig:rule/index:hybrid | 0.812 | 0.821 | 0.785 | 0.858 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:bm25 | 0.871 |
| ctx:tfidf | 0.862 |
| ctx:lsa | 0.863 |
| ctx:sbert | 0.824 |
| ctx:hybrid | 0.860 |
| ig:gold/gold:bm25 | 0.882 |
| ig:rule/index:bm25 | 0.882 |
| ig:gold/gold:tfidf | 0.882 |
| ig:rule/index:tfidf | 0.882 |
| ig:gold/gold:sbert | 0.942 |
| ig:rule/index:sbert | 0.940 |
| ig:gold/gold:hybrid | 0.882 |
| ig:rule/index:hybrid | 0.882 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:gold/gold:bm25 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.576 | 0.747 |
| ig:rule/index:bm25 | 1.000 | 0.815 | 0.950 | 1.000 | 1.000 | 0.947 | 0.807 | 0.000 | 0.549 | 0.634 |
| ig:gold/gold:tfidf | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.589 | 0.747 |
| ig:rule/index:tfidf | 1.000 | 0.815 | 0.950 | 1.000 | 1.000 | 0.947 | 0.807 | 0.000 | 0.562 | 0.634 |
| ig:gold/gold:sbert | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.639 | 0.768 |
| ig:rule/index:sbert | 1.000 | 0.815 | 0.950 | 1.000 | 1.000 | 0.947 | 0.807 | 0.000 | 0.608 | 0.652 |
| ig:gold/gold:hybrid | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.570 | 0.757 |
| ig:rule/index:hybrid | 1.000 | 0.815 | 0.950 | 1.000 | 1.000 | 0.947 | 0.807 | 0.000 | 0.542 | 0.643 |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:bm25 | – | 6.5 / 6.5 / 8.4 | – | – | – | – | 6.7 / 6.6 / 8.6 | 0.14 |
| ctx:tfidf | – | 4.4 / 4.5 / 4.9 | – | – | – | – | 4.6 / 4.6 / 5.1 | 0.097 |
| ctx:lsa | – | 25.0 / 21.7 / 30.5 | – | – | – | – | 25.3 / 21.9 / 30.9 | 0.532 |
| ctx:sbert | – | 87.3 / 80.6 / 88.2 | – | – | – | – | 87.3 / 80.6 / 88.2 | 1.834 |
| ctx:hybrid | – | 88.3 / 87.2 / 93.6 | – | – | – | – | 88.4 / 87.4 / 93.8 | 1.858 |
| ig:gold/gold:bm25 | 0.1 / 0.1 / 0.1 | 7.0 / 6.7 / 10.8 | 0.2 / 0.2 / 0.2 | 1402.4 / 1184.7 / 1889.0 | 323.6 / 120.2 / 548.3 | 0.1 / 0.1 / 0.1 | 1734.7 / 1435.8 / 2689.3 | 36.458 |
| ig:rule/index:bm25 | 0.4 / 0.2 / 0.7 | 5.8 / 6.1 / 9.7 | 0.3 / 0.2 / 0.4 | 115.9 / 39.0 / 251.8 | 320.7 / 154.9 / 451.9 | 0.1 / 0.1 / 0.1 | 444.5 / 254.3 / 790.5 | 9.362 |
| ig:gold/gold:tfidf | 0.1 / 0.1 / 0.1 | 5.4 / 5.0 / 6.7 | 0.2 / 0.1 / 0.2 | 220.6 / 78.4 / 227.1 | 218.2 / 119.1 / 551.6 | 0.1 / 0.1 / 0.1 | 445.5 / 259.7 / 718.4 | 9.385 |
| ig:rule/index:tfidf | 0.2 / 0.2 / 0.2 | 5.2 / 5.4 / 6.8 | 0.2 / 0.2 / 0.3 | 33.0 / 18.4 / 28.7 | 214.0 / 110.2 / 324.3 | 0.1 / 0.1 / 0.1 | 253.7 / 144.1 / 348.4 | 5.353 |
| ig:gold/gold:sbert | 0.1 / 0.1 / 0.1 | 79.3 / 78.3 / 84.4 | 0.2 / 0.2 / 0.2 | 920.2 / 599.0 / 1704.0 | 257.8 / 156.3 / 776.7 | 0.1 / 0.1 / 0.1 | 1258.6 / 997.3 / 2442.1 | 26.469 |
| ig:rule/index:sbert | 0.2 / 0.2 / 0.2 | 78.2 / 76.7 / 81.1 | 0.3 / 0.3 / 0.3 | 115.1 / 37.0 / 207.2 | 271.8 / 144.5 / 850.9 | 0.1 / 0.1 / 0.1 | 466.5 / 363.5 / 1220.8 | 9.827 |
| ig:gold/gold:hybrid | 0.1 / 0.1 / 0.1 | 83.2 / 82.2 / 87.6 | 0.2 / 0.2 / 0.2 | 64.9 / 22.1 / 152.3 | 346.5 / 141.9 / 916.6 | 0.1 / 0.1 / 0.1 | 495.8 / 293.8 / 1014.4 | 10.443 |
| ig:rule/index:hybrid | 0.2 / 0.2 / 0.2 | 82.5 / 82.3 / 89.4 | 0.3 / 0.3 / 0.3 | 33.0 / 18.2 / 51.8 | 342.1 / 166.0 / 1112.0 | 0.1 / 0.1 / 0.1 | 459.2 / 273.0 / 1212.0 | 9.674 |

Context index build (one-off, ms): bm25: 378, hybrid: 24572, lsa: 4298, sbert: 1035 (cached), tfidf: 325

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:rule/index:tfidf | ctx:tfidf | ndcg@10 | +0.046 | [-0.003, +0.090] | 0.086 | 12/4 |
| ig:rule/index:tfidf | ctx:tfidf | mrr | +0.152 | [+0.035, +0.275] | 0.038 | 8/1 |
| ig:rule/index:tfidf | ctx:tfidf | useful@1 | +0.250 | [+0.000, +0.500] | 0.127 | 6/1 |
| ig:gold/gold:tfidf | ctx:tfidf | ndcg@10 | +0.057 | [+0.006, +0.103] | 0.046 | 12/4 |
| ig:gold/gold:tfidf | ctx:tfidf | mrr | +0.152 | [+0.035, +0.275] | 0.038 | 8/1 |
| ig:gold/gold:tfidf | ctx:tfidf | useful@1 | +0.250 | [+0.000, +0.500] | 0.127 | 6/1 |
| ig:rule/index:sbert | ctx:sbert | ndcg@10 | +0.057 | [-0.038, +0.149] | 0.289 | 13/6 |
| ig:rule/index:sbert | ctx:sbert | mrr | +0.065 | [-0.104, +0.242] | 0.512 | 6/3 |
| ig:rule/index:sbert | ctx:sbert | useful@1 | +0.100 | [-0.150, +0.400] | 0.725 | 5/3 |
| ig:rule/index:hybrid | ctx:hybrid | ndcg@10 | -0.022 | [-0.079, +0.032] | 0.465 | 8/9 |
| ig:rule/index:hybrid | ctx:hybrid | mrr | -0.025 | [-0.125, +0.075] | 1.000 | 2/3 |
| ig:rule/index:hybrid | ctx:hybrid | useful@1 | -0.050 | [-0.250, +0.150] | 1.000 | 2/3 |
| ig:rule/index:bm25 | ctx:bm25 | ndcg@10 | -0.003 | [-0.045, +0.036] | 0.922 | 9/6 |
| ig:rule/index:bm25 | ctx:bm25 | mrr | -0.017 | [-0.142, +0.100] | 1.000 | 2/3 |
| ig:rule/index:bm25 | ctx:bm25 | useful@1 | -0.050 | [-0.300, +0.150] | 1.000 | 2/3 |
| ig:gold/gold:bm25 | ctx:bm25 | ndcg@10 | +0.027 | [-0.018, +0.067] | 0.247 | 11/5 |
| ig:gold/gold:bm25 | ctx:bm25 | mrr | +0.058 | [-0.042, +0.175] | 0.498 | 3/1 |
| ig:gold/gold:bm25 | ctx:bm25 | useful@1 | +0.100 | [-0.100, +0.300] | 0.625 | 3/1 |
| ig:gold/gold:hybrid | ctx:hybrid | ndcg@10 | -0.009 | [-0.066, +0.043] | 0.756 | 7/10 |
| ig:gold/gold:hybrid | ctx:hybrid | mrr | +0.000 | [-0.100, +0.100] | 1.000 | 2/2 |
| ig:gold/gold:hybrid | ctx:hybrid | useful@1 | +0.000 | [-0.200, +0.200] | 1.000 | 2/2 |
| ig:gold/gold:sbert | ctx:sbert | ndcg@10 | +0.094 | [-0.004, +0.183] | 0.076 | 15/3 |
| ig:gold/gold:sbert | ctx:sbert | mrr | +0.115 | [-0.054, +0.292] | 0.248 | 6/2 |
| ig:gold/gold:sbert | ctx:sbert | useful@1 | +0.200 | [-0.050, +0.450] | 0.286 | 6/2 |
