# IGBench results (20261025T104340Z_plan_igb-dev_tfidf)

Benchmark `igbench-v1` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:tfidf | 0.730 | 0.469 | 0.314 | 0.832 | 0.795 | 0.657 | 0.200 |
| ig:rule/index:tfidf | 0.762 | 0.520 | 0.323 | 0.842 | 0.841 | 0.714 | 0.143 |
| ig:rule/index:tfidf+rnorm=minmax | 0.755 | 0.503 | 0.317 | 0.826 | 0.835 | 0.714 | 0.143 |
| ig:rule/index:tfidf+align=0 | 0.705 | 0.457 | 0.303 | 0.789 | 0.738 | 0.571 | 0.257 |
| ig:gold/gold:tfidf | 0.801 | 0.520 | 0.337 | 0.875 | 0.876 | 0.771 | 0.171 |
| ig:gold/gold:tfidf+rnorm=minmax | 0.789 | 0.514 | 0.329 | 0.863 | 0.862 | 0.743 | 0.171 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:tfidf | 0.739 | 0.463 | 0.807 | 0.688 |
| ig:rule/index:tfidf | 0.774 | 0.519 | 0.857 | 0.750 |
| ig:rule/index:tfidf+rnorm=minmax | 0.766 | 0.500 | 0.850 | 0.750 |
| ig:rule/index:tfidf+align=0 | 0.711 | 0.450 | 0.745 | 0.594 |
| ig:gold/gold:tfidf | 0.816 | 0.519 | 0.896 | 0.812 |
| ig:gold/gold:tfidf+rnorm=minmax | 0.803 | 0.512 | 0.880 | 0.781 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:tfidf | 0.228 | 0.684 | 0.832 |
| ig:rule/index:tfidf | 0.270 | 0.746 | 0.842 |
| ig:rule/index:tfidf+rnorm=minmax | 0.270 | 0.706 | 0.826 |
| ig:rule/index:tfidf+align=0 | 0.201 | 0.655 | 0.789 |
| ig:gold/gold:tfidf | 0.337 | 0.740 | 0.875 |
| ig:gold/gold:tfidf+rnorm=minmax | 0.308 | 0.743 | 0.863 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | aggregate (n=3) | compare (n=10) | explain (n=7) | monitor (n=5) | predict (n=8) |
|---|---|---|---|---|---|
| ctx:tfidf | 0.940 | 0.736 | 0.738 | 0.649 | 0.734 |
| ig:rule/index:tfidf | 0.938 | 0.769 | 0.791 | 0.690 | 0.762 |
| ig:rule/index:tfidf+rnorm=minmax | 0.937 | 0.760 | 0.790 | 0.645 | 0.770 |
| ig:rule/index:tfidf+align=0 | 0.933 | 0.711 | 0.723 | 0.610 | 0.695 |
| ig:gold/gold:tfidf | 0.938 | 0.852 | 0.843 | 0.747 | 0.747 |
| ig:gold/gold:tfidf+rnorm=minmax | 0.937 | 0.843 | 0.815 | 0.708 | 0.754 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:tfidf | 0.799 |
| ig:rule/index:tfidf | 0.825 |
| ig:rule/index:tfidf+rnorm=minmax | 0.807 |
| ig:rule/index:tfidf+align=0 | 0.760 |
| ig:gold/gold:tfidf | 0.819 |
| ig:gold/gold:tfidf+rnorm=minmax | 0.812 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:rule/index:tfidf | 1.000 | 0.825 | 0.970 | 0.833 | 0.812 | 0.812 | 0.688 | 0.188 | 0.497 | 0.802 |
| ig:rule/index:tfidf+rnorm=minmax | 1.000 | 0.825 | 0.970 | 0.833 | 0.812 | 0.812 | 0.688 | 0.188 | 0.497 | 0.802 |
| ig:rule/index:tfidf+align=0 | 1.000 | 0.825 | 0.970 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | – | – |
| ig:gold/gold:tfidf | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.538 | 0.803 |
| ig:gold/gold:tfidf+rnorm=minmax | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.538 | 0.803 |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:tfidf | – | 5.2 / 4.3 / 9.2 | – | – | – | – | 5.4 / 4.4 / 9.4 | 0.195 |
| ig:rule/index:tfidf | 0.7 / 0.3 / 1.7 | 3.9 / 3.8 / 4.6 | 1.8 / 0.5 / 6.5 | 30.5 / 18.5 / 111.3 | 832.2 / 170.4 / 3854.7 | 0.1 / 0.1 / 0.2 | 866.2 / 205.5 / 4070.5 | 12.324 |
| ig:rule/index:tfidf+rnorm=minmax | 0.4 / 0.4 / 0.5 | 5.8 / 3.9 / 5.4 | 1.8 / 0.5 / 6.3 | 15.0 / 17.5 / 27.1 | 826.5 / 167.1 / 3841.5 | 0.1 / 0.1 / 0.2 | 844.7 / 187.5 / 3868.4 | 12.163 |
| ig:rule/index:tfidf+align=0 | 0.4 / 0.4 / 0.5 | 4.0 / 3.9 / 4.9 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.6 / 0.5 / 1.1 | 1.1 / 1.0 / 1.7 | 0.26 |
| ig:gold/gold:tfidf | 0.1 / 0.1 / 0.2 | 3.8 / 3.7 / 4.6 | 0.6 / 0.2 / 1.8 | 20.1 / 19.2 / 29.9 | 885.5 / 259.5 / 3919.7 | 0.1 / 0.1 / 0.2 | 907.6 / 287.9 / 3950.6 | 16.363 |
| ig:gold/gold:tfidf+rnorm=minmax | 0.1 / 0.1 / 0.2 | 4.1 / 3.8 / 4.9 | 0.6 / 0.2 / 1.5 | 25.1 / 18.2 / 35.4 | 882.6 / 256.3 / 4024.5 | 0.1 / 0.1 / 0.2 | 909.8 / 277.1 / 4052.1 | 16.299 |

Context index build (one-off, ms): tfidf: 1573 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:rule/index:tfidf+rnorm=minmax | ctx:tfidf | ndcg@10 | +0.024 | [+0.006, +0.044] | 0.016 | 19/6 |
| ig:rule/index:tfidf+rnorm=minmax | ctx:tfidf | mrr | +0.039 | [-0.002, +0.094] | 0.158 | 4/2 |
| ig:rule/index:tfidf+rnorm=minmax | ctx:tfidf | useful@1 | +0.057 | [+0.000, +0.143] | 0.505 | 2/0 |
| ig:gold/gold:tfidf+rnorm=minmax | ctx:tfidf | ndcg@10 | +0.057 | [+0.026, +0.093] | 0.000 | 21/5 |
| ig:gold/gold:tfidf+rnorm=minmax | ctx:tfidf | mrr | +0.067 | [-0.012, +0.145] | 0.120 | 7/1 |
| ig:gold/gold:tfidf+rnorm=minmax | ctx:tfidf | useful@1 | +0.086 | [-0.029, +0.200] | 0.374 | 4/1 |
| ig:rule/index:tfidf | ctx:tfidf | ndcg@10 | +0.032 | [+0.011, +0.054] | 0.005 | 19/5 |
| ig:rule/index:tfidf | ctx:tfidf | mrr | +0.045 | [+0.002, +0.098] | 0.094 | 5/1 |
| ig:rule/index:tfidf | ctx:tfidf | useful@1 | +0.057 | [+0.000, +0.143] | 0.505 | 2/0 |
| ig:rule/index:tfidf+align=0 | ctx:tfidf | ndcg@10 | -0.025 | [-0.049, -0.003] | 0.039 | 6/14 |
| ig:rule/index:tfidf+align=0 | ctx:tfidf | mrr | -0.057 | [-0.107, -0.014] | 0.016 | 0/7 |
| ig:rule/index:tfidf+align=0 | ctx:tfidf | useful@1 | -0.086 | [-0.200, +0.000] | 0.256 | 0/3 |
| ig:gold/gold:tfidf | ctx:tfidf | ndcg@10 | +0.069 | [+0.035, +0.106] | 0.000 | 23/5 |
| ig:gold/gold:tfidf | ctx:tfidf | mrr | +0.081 | [-0.005, +0.167] | 0.088 | 7/1 |
| ig:gold/gold:tfidf | ctx:tfidf | useful@1 | +0.114 | [-0.029, +0.257] | 0.223 | 5/1 |
