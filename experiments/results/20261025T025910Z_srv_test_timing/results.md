# IGBench results (20261025T025910Z_srv_test_timing)

Benchmark `igbench-v1-test` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:bm25 | 0.828 | 0.530 | 0.345 | 0.935 | 0.917 | 0.850 | 0.100 |
| ctx:sbert | 0.690 | 0.340 | 0.270 | 0.780 | 0.814 | 0.700 | 0.150 |
| ig:gold/gold:bm25 | 0.857 | 0.550 | 0.355 | 0.948 | 0.975 | 0.950 | 0.000 |
| ig:rule/index:bm25 | 0.826 | 0.540 | 0.355 | 0.948 | 0.900 | 0.800 | 0.050 |
| ig:gold/gold:sbert | 0.786 | 0.540 | 0.330 | 0.908 | 0.929 | 0.900 | 0.000 |
| ig:rule/index:sbert | 0.747 | 0.490 | 0.325 | 0.901 | 0.879 | 0.800 | 0.100 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:bm25 | 0.823 | 0.516 | 0.912 | 0.842 |
| ctx:sbert | 0.680 | 0.316 | 0.804 | 0.684 |
| ig:gold/gold:bm25 | 0.854 | 0.537 | 0.974 | 0.947 |
| ig:rule/index:bm25 | 0.821 | 0.526 | 0.895 | 0.789 |
| ig:gold/gold:sbert | 0.780 | 0.526 | 0.925 | 0.895 |
| ig:rule/index:sbert | 0.739 | 0.474 | 0.873 | 0.789 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:bm25 | 0.414 | 0.810 | 0.935 |
| ctx:sbert | 0.352 | 0.591 | 0.780 |
| ig:gold/gold:bm25 | 0.395 | 0.829 | 0.948 |
| ig:rule/index:bm25 | 0.327 | 0.817 | 0.948 |
| ig:gold/gold:sbert | 0.345 | 0.820 | 0.908 |
| ig:rule/index:sbert | 0.282 | 0.766 | 0.901 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | compare (n=8) | explain (n=3) | monitor (n=5) | predict (n=4) |
|---|---|---|---|---|
| ctx:bm25 | 0.812 | 0.800 | 0.750 | 0.909 |
| ctx:sbert | 0.665 | 0.675 | 0.683 | 0.756 |
| ig:gold/gold:bm25 | 0.805 | 0.833 | 0.849 | 0.918 |
| ig:rule/index:bm25 | 0.798 | 0.788 | 0.807 | 0.861 |
| ig:gold/gold:sbert | 0.781 | 0.877 | 0.702 | 0.842 |
| ig:rule/index:sbert | 0.784 | 0.871 | 0.635 | 0.728 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:bm25 | 0.871 |
| ctx:sbert | 0.824 |
| ig:gold/gold:bm25 | 0.882 |
| ig:rule/index:bm25 | 0.882 |
| ig:gold/gold:sbert | 0.942 |
| ig:rule/index:sbert | 0.940 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:gold/gold:bm25 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.576 | 0.747 |
| ig:rule/index:bm25 | 1.000 | 0.815 | 0.950 | 1.000 | 1.000 | 0.947 | 0.807 | 0.000 | 0.549 | 0.634 |
| ig:gold/gold:sbert | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.639 | 0.768 |
| ig:rule/index:sbert | 1.000 | 0.815 | 0.950 | 1.000 | 1.000 | 0.947 | 0.807 | 0.000 | 0.608 | 0.652 |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:bm25 | – | 7.7 / 7.9 / 10.3 | – | – | – | – | 7.9 / 8.2 / 10.6 | 0.167 |
| ctx:sbert | – | 140.3 / 121.5 / 151.7 | – | – | – | – | 140.4 / 121.6 / 152.0 | 2.95 |
| ig:gold/gold:bm25 | 0.3 / 0.3 / 0.4 | 9.3 / 9.6 / 13.7 | 0.5 / 0.5 / 0.7 | 81.8 / 36.6 / 68.2 | 428.8 / 329.9 / 1151.4 | 0.2 / 0.2 / 0.2 | 523.8 / 393.1 / 1230.1 | 11.034 |
| ig:rule/index:bm25 | 0.9 / 0.4 / 1.4 | 8.2 / 7.9 / 12.5 | 0.7 / 0.5 / 1.0 | 30.9 / 31.1 / 43.8 | 434.6 / 267.4 / 1009.4 | 0.2 / 0.2 / 0.2 | 478.6 / 294.9 / 1054.7 | 10.083 |
| ig:gold/gold:sbert | 0.2 / 0.2 / 0.3 | 125.3 / 117.6 / 153.1 | 0.4 / 0.3 / 0.6 | 56.6 / 31.3 / 64.8 | 501.5 / 277.3 / 1116.2 | 0.2 / 0.1 / 0.3 | 686.6 / 428.2 / 1253.6 | 14.466 |
| ig:rule/index:sbert | 0.4 / 0.4 / 0.5 | 114.9 / 112.0 / 141.5 | 0.6 / 0.5 / 0.9 | 29.8 / 32.6 / 36.4 | 478.3 / 208.8 / 1100.6 | 0.1 / 0.1 / 0.2 | 626.4 / 339.3 / 1259.4 | 13.196 |

Context index build (one-off, ms): bm25: 129 (cached), hybrid: 19232 (cached), lsa: 295 (cached), sbert: 1181 (cached), tfidf: 15 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:rule/index:sbert | ctx:sbert | ndcg@10 | +0.057 | [-0.038, +0.149] | 0.289 | 13/6 |
| ig:rule/index:sbert | ctx:sbert | mrr | +0.065 | [-0.104, +0.242] | 0.512 | 6/3 |
| ig:rule/index:sbert | ctx:sbert | useful@1 | +0.100 | [-0.150, +0.400] | 0.725 | 5/3 |
| ig:rule/index:bm25 | ctx:bm25 | ndcg@10 | -0.003 | [-0.045, +0.036] | 0.922 | 9/6 |
| ig:rule/index:bm25 | ctx:bm25 | mrr | -0.017 | [-0.142, +0.100] | 1.000 | 2/3 |
| ig:rule/index:bm25 | ctx:bm25 | useful@1 | -0.050 | [-0.300, +0.150] | 1.000 | 2/3 |
| ig:gold/gold:bm25 | ctx:bm25 | ndcg@10 | +0.027 | [-0.018, +0.067] | 0.247 | 11/5 |
| ig:gold/gold:bm25 | ctx:bm25 | mrr | +0.058 | [-0.042, +0.175] | 0.498 | 3/1 |
| ig:gold/gold:bm25 | ctx:bm25 | useful@1 | +0.100 | [-0.100, +0.300] | 0.625 | 3/1 |
| ig:gold/gold:sbert | ctx:sbert | ndcg@10 | +0.094 | [-0.004, +0.183] | 0.076 | 15/3 |
| ig:gold/gold:sbert | ctx:sbert | mrr | +0.115 | [-0.054, +0.292] | 0.248 | 6/2 |
| ig:gold/gold:sbert | ctx:sbert | useful@1 | +0.200 | [-0.050, +0.450] | 0.286 | 6/2 |
