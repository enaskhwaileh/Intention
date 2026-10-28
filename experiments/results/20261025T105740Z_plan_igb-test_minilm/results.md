# IGBench results (20261025T105740Z_plan_igb-test_minilm)

Benchmark `igbench-v1-test` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:sbert | 0.690 | 0.340 | 0.270 | 0.780 | 0.814 | 0.700 | 0.150 |
| ig:rule/index:sbert | 0.747 | 0.490 | 0.325 | 0.901 | 0.879 | 0.800 | 0.100 |
| ig:rule/index:sbert+rnorm=minmax | 0.737 | 0.450 | 0.295 | 0.828 | 0.867 | 0.750 | 0.100 |
| ig:rule/index:sbert+align=0 | 0.642 | 0.360 | 0.265 | 0.768 | 0.615 | 0.400 | 0.300 |
| ig:gold/gold:sbert | 0.786 | 0.540 | 0.330 | 0.908 | 0.929 | 0.900 | 0.000 |
| ig:gold/gold:sbert+rnorm=minmax | 0.769 | 0.470 | 0.310 | 0.869 | 0.917 | 0.850 | 0.000 |
| rerank:ce:sbert | 0.825 | 0.530 | 0.325 | 0.890 | 1.000 | 1.000 | 0.000 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:sbert | 0.680 | 0.316 | 0.804 | 0.684 |
| ig:rule/index:sbert | 0.739 | 0.474 | 0.873 | 0.789 |
| ig:rule/index:sbert+rnorm=minmax | 0.728 | 0.432 | 0.860 | 0.737 |
| ig:rule/index:sbert+align=0 | 0.629 | 0.337 | 0.594 | 0.368 |
| ig:gold/gold:sbert | 0.780 | 0.526 | 0.925 | 0.895 |
| ig:gold/gold:sbert+rnorm=minmax | 0.763 | 0.453 | 0.912 | 0.842 |
| rerank:ce:sbert | 0.821 | 0.516 | 1.000 | 1.000 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:sbert | 0.352 | 0.591 | 0.780 |
| ig:rule/index:sbert | 0.282 | 0.766 | 0.901 |
| ig:rule/index:sbert+rnorm=minmax | 0.299 | 0.709 | 0.828 |
| ig:rule/index:sbert+align=0 | 0.248 | 0.598 | 0.768 |
| ig:gold/gold:sbert | 0.345 | 0.820 | 0.908 |
| ig:gold/gold:sbert+rnorm=minmax | 0.362 | 0.727 | 0.869 |
| rerank:ce:sbert | 0.445 | 0.804 | 0.890 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | compare (n=8) | explain (n=3) | monitor (n=5) | predict (n=4) |
|---|---|---|---|---|
| ctx:sbert | 0.665 | 0.675 | 0.683 | 0.756 |
| ig:rule/index:sbert | 0.784 | 0.871 | 0.635 | 0.728 |
| ig:rule/index:sbert+rnorm=minmax | 0.742 | 0.732 | 0.715 | 0.764 |
| ig:rule/index:sbert+align=0 | 0.627 | 0.582 | 0.595 | 0.786 |
| ig:gold/gold:sbert | 0.781 | 0.877 | 0.702 | 0.842 |
| ig:gold/gold:sbert+rnorm=minmax | 0.740 | 0.759 | 0.747 | 0.871 |
| rerank:ce:sbert | 0.845 | 0.773 | 0.761 | 0.895 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:sbert | 0.824 |
| ig:rule/index:sbert | 0.940 |
| ig:rule/index:sbert+rnorm=minmax | 0.900 |
| ig:rule/index:sbert+align=0 | 0.842 |
| ig:gold/gold:sbert | 0.942 |
| ig:gold/gold:sbert+rnorm=minmax | 0.916 |
| rerank:ce:sbert | 0.890 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:rule/index:sbert | 1.000 | 0.815 | 0.950 | 1.000 | 1.000 | 0.947 | 0.807 | 0.000 | 0.608 | 0.652 |
| ig:rule/index:sbert+rnorm=minmax | 1.000 | 0.815 | 0.950 | 1.000 | 1.000 | 0.947 | 0.807 | 0.000 | 0.608 | 0.652 |
| ig:rule/index:sbert+align=0 | 1.000 | 0.815 | 0.950 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | – | – |
| ig:gold/gold:sbert | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.639 | 0.768 |
| ig:gold/gold:sbert+rnorm=minmax | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.639 | 0.768 |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:sbert | – | 110.8 / 91.2 / 100.9 | – | – | – | – | 110.8 / 91.2 / 100.9 | 2.327 |
| ig:rule/index:sbert | 1.0 / 0.4 / 2.1 | 91.1 / 91.1 / 93.0 | 2.0 / 0.3 / 6.7 | 22.2 / 22.5 / 31.5 | 247.0 / 127.2 / 868.3 | 0.1 / 0.1 / 0.1 | 273.4 / 149.8 / 889.1 | 5.04 |
| ig:rule/index:sbert+rnorm=minmax | 0.4 / 0.4 / 0.4 | 87.2 / 87.0 / 92.0 | 2.0 / 0.4 / 7.1 | 34.2 / 21.2 / 27.8 | 262.8 / 126.7 / 843.4 | 0.1 / 0.1 / 0.1 | 300.4 / 148.6 / 865.4 | 5.234 |
| ig:rule/index:sbert+align=0 | 0.4 / 0.4 / 0.4 | 84.0 / 82.2 / 93.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.4 / 0.4 / 0.7 | 0.9 / 0.8 / 1.2 | 2.135 |
| ig:gold/gold:sbert | 0.1 / 0.1 / 0.1 | 84.2 / 83.5 / 91.5 | 0.7 / 0.2 / 2.0 | 49.0 / 20.1 / 31.4 | 280.9 / 134.7 / 862.0 | 0.1 / 0.1 / 0.1 | 331.7 / 230.6 / 884.0 | 4.818 |
| ig:gold/gold:sbert+rnorm=minmax | 0.1 / 0.1 / 0.2 | 87.2 / 86.7 / 92.5 | 0.7 / 0.2 / 2.2 | 19.9 / 19.6 / 28.5 | 236.6 / 128.0 / 770.1 | 0.1 / 0.1 / 0.1 | 258.4 / 154.1 / 803.2 | 4.624 |
| rerank:ce:sbert | – | 978.4 / 975.1 / 1195.8 | – | – | – | – | 5180.6 / 6205.9 / 6494.8 | 8.129 |

Context index build (one-off, ms): sbert: 11961 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:rule/index:sbert+rnorm=minmax | ctx:sbert | ndcg@10 | +0.047 | [-0.011, +0.105] | 0.139 | 14/4 |
| ig:rule/index:sbert+rnorm=minmax | ctx:sbert | mrr | +0.052 | [-0.062, +0.177] | 0.449 | 5/2 |
| ig:rule/index:sbert+rnorm=minmax | ctx:sbert | useful@1 | +0.050 | [-0.150, +0.250] | 1.000 | 3/2 |
| ig:rule/index:sbert | ctx:sbert | ndcg@10 | +0.057 | [-0.038, +0.149] | 0.289 | 13/6 |
| ig:rule/index:sbert | ctx:sbert | mrr | +0.065 | [-0.104, +0.242] | 0.512 | 6/3 |
| ig:rule/index:sbert | ctx:sbert | useful@1 | +0.100 | [-0.150, +0.400] | 0.725 | 5/3 |
| ig:rule/index:sbert+align=0 | ctx:sbert | ndcg@10 | -0.043 | [-0.091, +0.002] | 0.086 | 4/12 |
| ig:rule/index:sbert+align=0 | ctx:sbert | mrr | -0.200 | [-0.325, -0.093] | 0.003 | 0/9 |
| ig:rule/index:sbert+align=0 | ctx:sbert | useful@1 | -0.300 | [-0.500, -0.100] | 0.031 | 0/6 |
| ig:gold/gold:sbert+rnorm=minmax | ctx:sbert | ndcg@10 | +0.078 | [+0.018, +0.133] | 0.017 | 15/2 |
| ig:gold/gold:sbert+rnorm=minmax | ctx:sbert | mrr | +0.102 | [-0.006, +0.233] | 0.155 | 5/1 |
| ig:gold/gold:sbert+rnorm=minmax | ctx:sbert | useful@1 | +0.150 | [-0.050, +0.350] | 0.366 | 4/1 |
| ig:gold/gold:sbert | ctx:sbert | ndcg@10 | +0.094 | [-0.004, +0.183] | 0.076 | 15/3 |
| ig:gold/gold:sbert | ctx:sbert | mrr | +0.115 | [-0.054, +0.292] | 0.248 | 6/2 |
| ig:gold/gold:sbert | ctx:sbert | useful@1 | +0.200 | [-0.050, +0.450] | 0.286 | 6/2 |
