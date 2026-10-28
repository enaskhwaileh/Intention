# IGBench results (20261025T105714Z_plan_igb-test_tfidf)

Benchmark `igbench-v1-test` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:tfidf | 0.775 | 0.460 | 0.315 | 0.882 | 0.765 | 0.600 | 0.300 |
| ig:rule/index:tfidf | 0.823 | 0.500 | 0.340 | 0.927 | 0.917 | 0.850 | 0.000 |
| ig:rule/index:tfidf+rnorm=minmax | 0.813 | 0.500 | 0.335 | 0.917 | 0.887 | 0.800 | 0.050 |
| ig:rule/index:tfidf+align=0 | 0.773 | 0.460 | 0.310 | 0.876 | 0.775 | 0.650 | 0.250 |
| ig:gold/gold:tfidf | 0.834 | 0.510 | 0.345 | 0.935 | 0.917 | 0.850 | 0.000 |
| ig:gold/gold:tfidf+rnorm=minmax | 0.828 | 0.520 | 0.340 | 0.925 | 0.912 | 0.850 | 0.000 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:tfidf | 0.770 | 0.442 | 0.752 | 0.579 |
| ig:rule/index:tfidf | 0.821 | 0.484 | 0.912 | 0.842 |
| ig:rule/index:tfidf+rnorm=minmax | 0.810 | 0.484 | 0.882 | 0.789 |
| ig:rule/index:tfidf+align=0 | 0.768 | 0.442 | 0.763 | 0.632 |
| ig:gold/gold:tfidf | 0.833 | 0.495 | 0.912 | 0.842 |
| ig:gold/gold:tfidf+rnorm=minmax | 0.826 | 0.505 | 0.908 | 0.842 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:tfidf | 0.340 | 0.736 | 0.882 |
| ig:rule/index:tfidf | 0.377 | 0.775 | 0.927 |
| ig:rule/index:tfidf+rnorm=minmax | 0.368 | 0.779 | 0.917 |
| ig:rule/index:tfidf+align=0 | 0.349 | 0.740 | 0.876 |
| ig:gold/gold:tfidf | 0.377 | 0.788 | 0.935 |
| ig:gold/gold:tfidf+rnorm=minmax | 0.377 | 0.800 | 0.925 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | compare (n=8) | explain (n=3) | monitor (n=5) | predict (n=4) |
|---|---|---|---|---|
| ctx:tfidf | 0.738 | 0.729 | 0.772 | 0.864 |
| ig:rule/index:tfidf | 0.774 | 0.795 | 0.857 | 0.876 |
| ig:rule/index:tfidf+rnorm=minmax | 0.771 | 0.759 | 0.842 | 0.878 |
| ig:rule/index:tfidf+align=0 | 0.748 | 0.728 | 0.760 | 0.850 |
| ig:gold/gold:tfidf | 0.780 | 0.797 | 0.873 | 0.900 |
| ig:gold/gold:tfidf+rnorm=minmax | 0.774 | 0.759 | 0.885 | 0.892 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:tfidf | 0.862 |
| ig:rule/index:tfidf | 0.882 |
| ig:rule/index:tfidf+rnorm=minmax | 0.882 |
| ig:rule/index:tfidf+align=0 | 0.849 |
| ig:gold/gold:tfidf | 0.882 |
| ig:gold/gold:tfidf+rnorm=minmax | 0.882 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:rule/index:tfidf | 1.000 | 0.815 | 0.950 | 1.000 | 1.000 | 0.947 | 0.807 | 0.000 | 0.562 | 0.634 |
| ig:rule/index:tfidf+rnorm=minmax | 1.000 | 0.815 | 0.950 | 1.000 | 1.000 | 0.947 | 0.807 | 0.000 | 0.562 | 0.634 |
| ig:rule/index:tfidf+align=0 | 1.000 | 0.815 | 0.950 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | – | – |
| ig:gold/gold:tfidf | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.589 | 0.747 |
| ig:gold/gold:tfidf+rnorm=minmax | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.589 | 0.747 |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:tfidf | – | 4.8 / 4.2 / 4.5 | – | – | – | – | 4.9 / 4.4 / 4.7 | 0.103 |
| ig:rule/index:tfidf | 1.0 / 0.4 / 2.1 | 4.1 / 3.9 / 4.6 | 2.0 / 0.3 / 6.6 | 33.5 / 21.9 / 95.2 | 212.0 / 99.4 / 316.3 | 0.1 / 0.1 / 0.1 | 249.6 / 162.0 / 334.3 | 3.012 |
| ig:rule/index:tfidf+rnorm=minmax | 0.4 / 0.3 / 0.4 | 5.2 / 4.0 / 8.6 | 2.6 / 0.3 / 8.1 | 39.0 / 22.5 / 113.5 | 223.8 / 109.9 / 318.9 | 0.1 / 0.1 / 0.1 | 266.7 / 179.0 / 434.3 | 3.078 |
| ig:rule/index:tfidf+align=0 | 0.3 / 0.3 / 0.4 | 4.0 / 3.7 / 4.7 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.8 / 0.6 / 1.3 | 1.2 / 1.0 / 1.9 | 0.18 |
| ig:gold/gold:tfidf | 0.1 / 0.1 / 0.1 | 3.8 / 3.6 / 4.6 | 0.8 / 0.2 / 3.1 | 23.9 / 19.0 / 36.1 | 229.8 / 114.4 / 541.6 | 0.1 / 0.1 / 0.1 | 255.8 / 148.6 / 559.7 | 2.877 |
| ig:gold/gold:tfidf+rnorm=minmax | 0.1 / 0.1 / 0.1 | 3.9 / 3.7 / 4.7 | 0.8 / 0.2 / 3.1 | 23.5 / 18.4 / 29.6 | 220.4 / 114.9 / 533.0 | 0.1 / 0.1 / 0.1 | 245.9 / 147.6 / 550.9 | 2.794 |

Context index build (one-off, ms): tfidf: 1632 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:rule/index:tfidf+rnorm=minmax | ctx:tfidf | ndcg@10 | +0.036 | [-0.013, +0.080] | 0.161 | 10/4 |
| ig:rule/index:tfidf+rnorm=minmax | ctx:tfidf | mrr | +0.123 | [+0.015, +0.242] | 0.070 | 7/1 |
| ig:rule/index:tfidf+rnorm=minmax | ctx:tfidf | useful@1 | +0.200 | [+0.000, +0.450] | 0.223 | 5/1 |
| ig:gold/gold:tfidf+rnorm=minmax | ctx:tfidf | ndcg@10 | +0.050 | [+0.001, +0.096] | 0.069 | 11/4 |
| ig:gold/gold:tfidf+rnorm=minmax | ctx:tfidf | mrr | +0.148 | [+0.031, +0.269] | 0.038 | 8/1 |
| ig:gold/gold:tfidf+rnorm=minmax | ctx:tfidf | useful@1 | +0.250 | [+0.000, +0.500] | 0.127 | 6/1 |
| ig:rule/index:tfidf | ctx:tfidf | ndcg@10 | +0.046 | [-0.003, +0.090] | 0.086 | 12/4 |
| ig:rule/index:tfidf | ctx:tfidf | mrr | +0.152 | [+0.035, +0.275] | 0.038 | 8/1 |
| ig:rule/index:tfidf | ctx:tfidf | useful@1 | +0.250 | [+0.000, +0.500] | 0.127 | 6/1 |
| ig:rule/index:tfidf+align=0 | ctx:tfidf | ndcg@10 | -0.002 | [-0.018, +0.014] | 0.834 | 4/7 |
| ig:rule/index:tfidf+align=0 | ctx:tfidf | mrr | +0.010 | [-0.033, +0.069] | 0.876 | 2/2 |
| ig:rule/index:tfidf+align=0 | ctx:tfidf | useful@1 | +0.050 | [+0.000, +0.150] | 1.000 | 1/0 |
| ig:gold/gold:tfidf | ctx:tfidf | ndcg@10 | +0.057 | [+0.006, +0.103] | 0.046 | 12/4 |
| ig:gold/gold:tfidf | ctx:tfidf | mrr | +0.152 | [+0.035, +0.275] | 0.038 | 8/1 |
| ig:gold/gold:tfidf | ctx:tfidf | useful@1 | +0.250 | [+0.000, +0.500] | 0.127 | 6/1 |
