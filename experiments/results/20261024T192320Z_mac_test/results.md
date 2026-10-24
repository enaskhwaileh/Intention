# IGBench results (20261024T192320Z_mac_test)

Benchmark `igbench-v1-test` on corpus `igbench-v1` (3301 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.12.3 on macOS-15.7.9-x86_64-i386-64bit. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:bm25 | 0.828 | 0.530 | 0.345 | 0.935 | 0.917 | 0.850 | 0.100 |
| ctx:tfidf | 0.775 | 0.460 | 0.315 | 0.882 | 0.765 | 0.600 | 0.300 |
| ctx:sbert | 0.690 | 0.340 | 0.270 | 0.780 | 0.814 | 0.700 | 0.150 |
| ctx:hybrid | 0.845 | 0.560 | 0.335 | 0.907 | 0.950 | 0.900 | 0.050 |
| ig:gold/gold:bm25 | 0.857 | 0.550 | 0.355 | 0.948 | 0.975 | 0.950 | 0.000 |
| ig:rule/index:bm25 | 0.826 | 0.540 | 0.355 | 0.948 | 0.900 | 0.800 | 0.050 |
| ig:gold/gold:sbert | 0.786 | 0.540 | 0.330 | 0.908 | 0.929 | 0.900 | 0.000 |
| ig:rule/index:sbert | 0.747 | 0.490 | 0.325 | 0.901 | 0.879 | 0.800 | 0.100 |
| ig:gold/gold:hybrid | 0.842 | 0.570 | 0.350 | 0.944 | 0.950 | 0.900 | 0.000 |
| ig:rule/index:hybrid | 0.828 | 0.570 | 0.350 | 0.944 | 0.925 | 0.850 | 0.050 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:bm25 | 0.823 | 0.516 | 0.912 | 0.842 |
| ctx:tfidf | 0.770 | 0.442 | 0.752 | 0.579 |
| ctx:sbert | 0.680 | 0.316 | 0.804 | 0.684 |
| ctx:hybrid | 0.839 | 0.547 | 0.947 | 0.895 |
| ig:gold/gold:bm25 | 0.854 | 0.537 | 0.974 | 0.947 |
| ig:rule/index:bm25 | 0.821 | 0.526 | 0.895 | 0.789 |
| ig:gold/gold:sbert | 0.780 | 0.526 | 0.925 | 0.895 |
| ig:rule/index:sbert | 0.739 | 0.474 | 0.873 | 0.789 |
| ig:gold/gold:hybrid | 0.835 | 0.558 | 0.947 | 0.895 |
| ig:rule/index:hybrid | 0.821 | 0.558 | 0.921 | 0.842 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:bm25 | 0.414 | 0.810 | 0.935 |
| ctx:tfidf | 0.340 | 0.736 | 0.882 |
| ctx:sbert | 0.352 | 0.591 | 0.780 |
| ctx:hybrid | 0.424 | 0.833 | 0.907 |
| ig:gold/gold:bm25 | 0.395 | 0.829 | 0.948 |
| ig:rule/index:bm25 | 0.327 | 0.817 | 0.948 |
| ig:gold/gold:sbert | 0.345 | 0.820 | 0.908 |
| ig:rule/index:sbert | 0.282 | 0.766 | 0.901 |
| ig:gold/gold:hybrid | 0.345 | 0.843 | 0.944 |
| ig:rule/index:hybrid | 0.295 | 0.839 | 0.944 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | compare (n=8) | explain (n=3) | monitor (n=5) | predict (n=4) |
|---|---|---|---|---|
| ctx:bm25 | 0.812 | 0.800 | 0.750 | 0.909 |
| ctx:tfidf | 0.738 | 0.729 | 0.772 | 0.864 |
| ctx:sbert | 0.665 | 0.675 | 0.683 | 0.756 |
| ctx:hybrid | 0.847 | 0.763 | 0.809 | 0.918 |
| ig:gold/gold:bm25 | 0.805 | 0.833 | 0.849 | 0.918 |
| ig:rule/index:bm25 | 0.798 | 0.788 | 0.807 | 0.861 |
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
| ctx:sbert | 0.824 |
| ctx:hybrid | 0.860 |
| ig:gold/gold:bm25 | 0.882 |
| ig:rule/index:bm25 | 0.882 |
| ig:gold/gold:sbert | 0.942 |
| ig:rule/index:sbert | 0.940 |
| ig:gold/gold:hybrid | 0.882 |
| ig:rule/index:hybrid | 0.882 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:gold/gold:bm25 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.576 | 0.747 |
| ig:rule/index:bm25 | 1.000 | 0.815 | 0.950 | 1.000 | 1.000 | 0.947 | 0.807 | 0.000 | 0.549 | 0.634 |
| ig:gold/gold:sbert | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.639 | 0.768 |
| ig:rule/index:sbert | 1.000 | 0.815 | 0.950 | 1.000 | 1.000 | 0.947 | 0.807 | 0.000 | 0.608 | 0.652 |
| ig:gold/gold:hybrid | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.570 | 0.757 |
| ig:rule/index:hybrid | 1.000 | 0.815 | 0.950 | 1.000 | 1.000 | 0.947 | 0.807 | 0.000 | 0.542 | 0.643 |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:bm25 | – | 9.3 / 9.2 / 12.7 | – | – | – | – | 9.5 / 9.6 / 12.9 | 0.201 |
| ctx:tfidf | – | 5.8 / 6.0 / 6.9 | – | – | – | – | 6.1 / 6.3 / 7.2 | 0.128 |
| ctx:sbert | – | 65.1 / 61.5 / 82.0 | – | – | – | – | 65.2 / 61.5 / 82.1 | 1.37 |
| ctx:hybrid | – | 73.0 / 73.4 / 78.7 | – | – | – | – | 73.3 / 73.6 / 79.2 | 1.539 |
| ig:gold/gold:bm25 | 0.1 / 0.1 / 0.1 | 7.0 / 6.7 / 11.4 | 0.2 / 0.2 / 0.3 | 2066.2 / 1763.7 / 3111.8 | 1141.1 / 156.7 / 733.7 | 0.1 / 0.1 / 0.1 | 3216.1 / 2022.5 / 5316.4 | 67.561 |
| ig:rule/index:bm25 | 0.5 / 0.2 / 0.8 | 6.9 / 7.7 / 10.5 | 0.4 / 0.3 / 0.4 | 127.1 / 42.0 / 297.9 | 1182.5 / 196.3 / 458.6 | 0.1 / 0.1 / 0.1 | 1319.1 / 331.5 / 633.4 | 27.719 |
| ig:gold/gold:sbert | 0.1 / 0.1 / 0.1 | 63.8 / 62.7 / 70.1 | 0.2 / 0.2 / 0.2 | 1344.8 / 777.8 / 2717.2 | 273.7 / 155.8 / 597.9 | 0.1 / 0.1 / 0.1 | 1683.8 / 1340.9 / 3356.6 | 35.389 |
| ig:rule/index:sbert | 0.2 / 0.2 / 0.2 | 61.7 / 61.4 / 63.2 | 0.3 / 0.3 / 0.4 | 104.6 / 29.8 / 258.3 | 274.5 / 156.5 / 691.1 | 0.1 / 0.1 / 0.1 | 442.5 / 366.0 / 905.7 | 9.318 |
| ig:gold/gold:hybrid | 0.1 / 0.1 / 0.1 | 68.8 / 68.2 / 74.0 | 0.2 / 0.2 / 0.3 | 69.0 / 33.9 / 164.5 | 1209.6 / 248.0 / 1029.7 | 0.1 / 0.1 / 0.1 | 1349.0 / 430.4 / 1114.4 | 28.356 |
| ig:rule/index:hybrid | 0.2 / 0.2 / 0.2 | 69.1 / 68.2 / 73.9 | 0.3 / 0.3 / 0.4 | 22.7 / 19.1 / 28.6 | 1180.2 / 241.7 / 1047.9 | 0.1 / 0.1 / 0.1 | 1274.0 / 339.6 / 1142.0 | 26.78 |

Context index build (one-off, ms): bm25: 508, hybrid: 197719, sbert: 1399 (cached), tfidf: 797

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:gold/gold:bm25 | ctx:bm25 | ndcg@10 | +0.027 | [-0.018, +0.067] | 0.247 | 11/5 |
| ig:gold/gold:bm25 | ctx:bm25 | mrr | +0.058 | [-0.042, +0.175] | 0.498 | 3/1 |
| ig:gold/gold:bm25 | ctx:bm25 | useful@1 | +0.100 | [-0.100, +0.300] | 0.625 | 3/1 |
| ig:gold/gold:hybrid | ctx:hybrid | ndcg@10 | -0.009 | [-0.066, +0.043] | 0.756 | 7/10 |
| ig:gold/gold:hybrid | ctx:hybrid | mrr | +0.000 | [-0.100, +0.100] | 1.000 | 2/2 |
| ig:gold/gold:hybrid | ctx:hybrid | useful@1 | +0.000 | [-0.200, +0.200] | 1.000 | 2/2 |
| ig:gold/gold:sbert | ctx:sbert | ndcg@10 | +0.094 | [-0.004, +0.183] | 0.076 | 15/3 |
| ig:gold/gold:sbert | ctx:sbert | mrr | +0.115 | [-0.054, +0.292] | 0.248 | 6/2 |
| ig:gold/gold:sbert | ctx:sbert | useful@1 | +0.200 | [-0.050, +0.450] | 0.286 | 6/2 |
| ig:rule/index:hybrid | ctx:hybrid | ndcg@10 | -0.022 | [-0.079, +0.032] | 0.465 | 8/9 |
| ig:rule/index:hybrid | ctx:hybrid | mrr | -0.025 | [-0.125, +0.075] | 1.000 | 2/3 |
| ig:rule/index:hybrid | ctx:hybrid | useful@1 | -0.050 | [-0.250, +0.150] | 1.000 | 2/3 |
| ig:rule/index:bm25 | ctx:bm25 | ndcg@10 | -0.003 | [-0.045, +0.036] | 0.922 | 9/6 |
| ig:rule/index:bm25 | ctx:bm25 | mrr | -0.017 | [-0.142, +0.100] | 1.000 | 2/3 |
| ig:rule/index:bm25 | ctx:bm25 | useful@1 | -0.050 | [-0.300, +0.150] | 1.000 | 2/3 |
| ig:rule/index:sbert | ctx:sbert | ndcg@10 | +0.057 | [-0.038, +0.149] | 0.289 | 13/6 |
| ig:rule/index:sbert | ctx:sbert | mrr | +0.065 | [-0.104, +0.242] | 0.512 | 6/3 |
| ig:rule/index:sbert | ctx:sbert | useful@1 | +0.100 | [-0.150, +0.400] | 0.725 | 5/3 |
