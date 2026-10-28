# IGBench results (20261025T105833Z_plan_igb-test_e5)

Benchmark `igbench-v1-test` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:sbert | 0.778 | 0.490 | 0.305 | 0.880 | 0.950 | 0.900 | 0.000 |
| ig:rule/index:sbert | 0.727 | 0.500 | 0.325 | 0.874 | 0.847 | 0.800 | 0.050 |
| ig:rule/index:sbert+rnorm=minmax | 0.806 | 0.550 | 0.330 | 0.916 | 0.917 | 0.850 | 0.050 |
| ig:rule/index:sbert+align=0 | 0.789 | 0.500 | 0.310 | 0.887 | 0.950 | 0.900 | 0.000 |
| ig:gold/gold:sbert | 0.781 | 0.550 | 0.335 | 0.928 | 0.908 | 0.850 | 0.000 |
| ig:gold/gold:sbert+rnorm=minmax | 0.819 | 0.570 | 0.330 | 0.916 | 0.942 | 0.900 | 0.000 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:sbert | 0.775 | 0.474 | 0.947 | 0.895 |
| ig:rule/index:sbert | 0.721 | 0.484 | 0.839 | 0.789 |
| ig:rule/index:sbert+rnorm=minmax | 0.803 | 0.537 | 0.912 | 0.842 |
| ig:rule/index:sbert+align=0 | 0.786 | 0.484 | 0.947 | 0.895 |
| ig:gold/gold:sbert | 0.778 | 0.537 | 0.903 | 0.842 |
| ig:gold/gold:sbert+rnorm=minmax | 0.818 | 0.558 | 0.939 | 0.895 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:sbert | 0.390 | 0.778 | 0.880 |
| ig:rule/index:sbert | 0.290 | 0.709 | 0.874 |
| ig:rule/index:sbert+rnorm=minmax | 0.340 | 0.836 | 0.916 |
| ig:rule/index:sbert+align=0 | 0.390 | 0.784 | 0.887 |
| ig:gold/gold:sbert | 0.340 | 0.800 | 0.928 |
| ig:gold/gold:sbert+rnorm=minmax | 0.390 | 0.855 | 0.916 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | compare (n=8) | explain (n=3) | monitor (n=5) | predict (n=4) |
|---|---|---|---|---|
| ctx:sbert | 0.731 | 0.783 | 0.755 | 0.853 |
| ig:rule/index:sbert | 0.715 | 0.846 | 0.685 | 0.613 |
| ig:rule/index:sbert+rnorm=minmax | 0.720 | 0.877 | 0.819 | 0.805 |
| ig:rule/index:sbert+align=0 | 0.718 | 0.811 | 0.755 | 0.857 |
| ig:gold/gold:sbert | 0.717 | 0.863 | 0.704 | 0.845 |
| ig:gold/gold:sbert+rnorm=minmax | 0.713 | 0.869 | 0.827 | 0.885 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:sbert | 0.875 |
| ig:rule/index:sbert | 0.920 |
| ig:rule/index:sbert+rnorm=minmax | 0.882 |
| ig:rule/index:sbert+align=0 | 0.859 |
| ig:gold/gold:sbert | 0.862 |
| ig:gold/gold:sbert+rnorm=minmax | 0.863 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:rule/index:sbert | 1.000 | 0.815 | 0.950 | 1.000 | 1.000 | 0.947 | 0.807 | 0.000 | 0.575 | 0.648 |
| ig:rule/index:sbert+rnorm=minmax | 1.000 | 0.815 | 0.950 | 1.000 | 1.000 | 0.947 | 0.807 | 0.000 | 0.575 | 0.648 |
| ig:rule/index:sbert+align=0 | 1.000 | 0.815 | 0.950 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | – | – |
| ig:gold/gold:sbert | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.628 | 0.761 |
| ig:gold/gold:sbert+rnorm=minmax | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.628 | 0.761 |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:sbert | – | 110.5 / 92.0 / 99.3 | – | – | – | – | 110.5 / 92.0 / 99.3 | 2.321 |
| ig:rule/index:sbert | 1.0 / 0.3 / 2.1 | 93.3 / 92.6 / 98.7 | 2.0 / 0.3 / 7.0 | 23.1 / 23.8 / 33.2 | 329.6 / 188.6 / 1104.5 | 0.1 / 0.1 / 0.1 | 356.9 / 229.4 / 1125.8 | 5.355 |
| ig:rule/index:sbert+rnorm=minmax | 0.4 / 0.4 / 0.4 | 91.5 / 91.3 / 96.4 | 1.9 / 0.3 / 5.8 | 36.1 / 21.2 / 32.7 | 374.2 / 188.9 / 1163.9 | 0.1 / 0.1 / 0.1 | 413.7 / 217.6 / 1185.9 | 5.626 |
| ig:rule/index:sbert+align=0 | 0.3 / 0.3 / 0.4 | 95.7 / 95.1 / 102.2 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.4 / 0.4 / 0.7 | 0.8 / 0.8 / 1.2 | 2.383 |
| ig:gold/gold:sbert | 0.1 / 0.1 / 0.1 | 96.1 / 95.6 / 99.2 | 0.8 / 0.2 / 2.3 | 110.9 / 24.7 / 341.3 | 313.7 / 200.0 / 823.6 | 0.1 / 0.1 / 0.1 | 426.6 / 286.6 / 1122.2 | 5.368 |
| ig:gold/gold:sbert+rnorm=minmax | 0.1 / 0.1 / 0.1 | 94.6 / 94.4 / 97.5 | 0.7 / 0.2 / 1.9 | 22.0 / 21.5 / 30.6 | 313.2 / 199.2 / 816.7 | 0.1 / 0.1 / 0.1 | 337.1 / 228.8 / 838.1 | 5.013 |

Context index build (one-off, ms): sbert: 14072 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:rule/index:sbert+rnorm=minmax | ctx:sbert | ndcg@10 | +0.015 | [-0.032, +0.059] | 0.531 | 9/9 |
| ig:rule/index:sbert+rnorm=minmax | ctx:sbert | mrr | -0.033 | [-0.092, +0.000] | 0.507 | 0/2 |
| ig:rule/index:sbert+rnorm=minmax | ctx:sbert | useful@1 | -0.050 | [-0.150, +0.000] | 1.000 | 0/1 |
| ig:rule/index:sbert | ctx:sbert | ndcg@10 | -0.059 | [-0.148, +0.017] | 0.239 | 11/8 |
| ig:rule/index:sbert | ctx:sbert | mrr | -0.103 | [-0.236, +0.000] | 0.251 | 0/3 |
| ig:rule/index:sbert | ctx:sbert | useful@1 | -0.100 | [-0.250, +0.000] | 0.496 | 0/2 |
| ig:rule/index:sbert+align=0 | ctx:sbert | ndcg@10 | -0.000 | [-0.033, +0.028] | 0.983 | 8/8 |
| ig:rule/index:sbert+align=0 | ctx:sbert | mrr | +0.000 | [+0.000, +0.000] | 1.000 | 0/0 |
| ig:rule/index:sbert+align=0 | ctx:sbert | useful@1 | +0.000 | [+0.000, +0.000] | 1.000 | 0/0 |
| ig:gold/gold:sbert+rnorm=minmax | ctx:sbert | ndcg@10 | +0.028 | [-0.015, +0.066] | 0.189 | 12/5 |
| ig:gold/gold:sbert+rnorm=minmax | ctx:sbert | mrr | -0.008 | [-0.025, +0.000] | 1.000 | 0/1 |
| ig:gold/gold:sbert+rnorm=minmax | ctx:sbert | useful@1 | +0.000 | [+0.000, +0.000] | 1.000 | 0/0 |
| ig:gold/gold:sbert | ctx:sbert | ndcg@10 | -0.008 | [-0.061, +0.042] | 0.779 | 11/8 |
| ig:gold/gold:sbert | ctx:sbert | mrr | -0.042 | [-0.108, +0.000] | 0.499 | 0/2 |
| ig:gold/gold:sbert | ctx:sbert | useful@1 | -0.050 | [-0.150, +0.000] | 1.000 | 0/1 |
