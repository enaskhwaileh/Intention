# IGBench results (20261025T104158Z_plan_igb-dev_bm25)

Benchmark `igbench-v1` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:bm25 | 0.768 | 0.486 | 0.323 | 0.851 | 0.895 | 0.800 | 0.143 |
| ig:rule/index:bm25 | 0.788 | 0.531 | 0.331 | 0.875 | 0.909 | 0.829 | 0.114 |
| ig:rule/index:bm25+rnorm=minmax | 0.797 | 0.526 | 0.337 | 0.884 | 0.906 | 0.829 | 0.114 |
| ig:rule/index:bm25+align=0 | 0.777 | 0.491 | 0.326 | 0.865 | 0.884 | 0.800 | 0.143 |
| ig:gold/gold:bm25 | 0.796 | 0.537 | 0.334 | 0.882 | 0.879 | 0.771 | 0.143 |
| ig:gold/gold:bm25+rnorm=minmax | 0.798 | 0.537 | 0.337 | 0.884 | 0.881 | 0.771 | 0.143 |
| rerank:ce:bm25 | 0.808 | 0.566 | 0.346 | 0.897 | 0.894 | 0.829 | 0.143 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:bm25 | 0.779 | 0.469 | 0.917 | 0.844 |
| ig:rule/index:bm25 | 0.801 | 0.519 | 0.932 | 0.875 |
| ig:rule/index:bm25+rnorm=minmax | 0.810 | 0.512 | 0.928 | 0.875 |
| ig:rule/index:bm25+align=0 | 0.789 | 0.475 | 0.904 | 0.844 |
| ig:gold/gold:bm25 | 0.809 | 0.525 | 0.898 | 0.812 |
| ig:gold/gold:bm25+rnorm=minmax | 0.812 | 0.525 | 0.901 | 0.812 |
| rerank:ce:bm25 | 0.815 | 0.556 | 0.907 | 0.844 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:bm25 | 0.306 | 0.711 | 0.851 |
| ig:rule/index:bm25 | 0.321 | 0.782 | 0.875 |
| ig:rule/index:bm25+rnorm=minmax | 0.321 | 0.767 | 0.884 |
| ig:rule/index:bm25+align=0 | 0.306 | 0.702 | 0.865 |
| ig:gold/gold:bm25 | 0.311 | 0.781 | 0.882 |
| ig:gold/gold:bm25+rnorm=minmax | 0.311 | 0.772 | 0.884 |
| rerank:ce:bm25 | 0.328 | 0.808 | 0.897 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | aggregate (n=3) | compare (n=10) | explain (n=7) | monitor (n=5) | predict (n=8) |
|---|---|---|---|---|---|
| ctx:bm25 | 0.939 | 0.804 | 0.775 | 0.668 | 0.773 |
| ig:rule/index:bm25 | 0.964 | 0.831 | 0.807 | 0.699 | 0.770 |
| ig:rule/index:bm25+rnorm=minmax | 0.965 | 0.833 | 0.812 | 0.694 | 0.804 |
| ig:rule/index:bm25+align=0 | 0.979 | 0.808 | 0.778 | 0.672 | 0.787 |
| ig:gold/gold:bm25 | 0.964 | 0.855 | 0.827 | 0.728 | 0.741 |
| ig:gold/gold:bm25+rnorm=minmax | 0.964 | 0.848 | 0.831 | 0.728 | 0.754 |
| rerank:ce:bm25 | 0.917 | 0.809 | 0.834 | 0.689 | 0.856 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:bm25 | 0.803 |
| ig:rule/index:bm25 | 0.843 |
| ig:rule/index:bm25+rnorm=minmax | 0.823 |
| ig:rule/index:bm25+align=0 | 0.795 |
| ig:gold/gold:bm25 | 0.860 |
| ig:gold/gold:bm25+rnorm=minmax | 0.861 |
| rerank:ce:bm25 | 0.843 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:rule/index:bm25 | 1.000 | 0.825 | 0.970 | 0.833 | 0.812 | 0.812 | 0.688 | 0.188 | 0.482 | 0.784 |
| ig:rule/index:bm25+rnorm=minmax | 1.000 | 0.825 | 0.970 | 0.833 | 0.812 | 0.812 | 0.688 | 0.188 | 0.482 | 0.784 |
| ig:rule/index:bm25+align=0 | 1.000 | 0.825 | 0.970 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | – | – |
| ig:gold/gold:bm25 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.497 | 0.789 |
| ig:gold/gold:bm25+rnorm=minmax | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.497 | 0.789 |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:bm25 | – | 5.9 / 5.4 / 8.2 | – | – | – | – | 6.0 / 5.5 / 8.3 | 0.217 |
| ig:rule/index:bm25 | 0.7 / 0.4 / 1.7 | 5.8 / 5.0 / 11.5 | 1.8 / 0.6 / 6.3 | 20.8 / 20.1 / 54.7 | 1030.8 / 220.4 / 3859.5 | 0.1 / 0.1 / 0.2 | 1055.1 / 258.5 / 3883.8 | 12.506 |
| ig:rule/index:bm25+rnorm=minmax | 0.4 / 0.4 / 0.5 | 4.9 / 3.9 / 6.4 | 1.9 / 0.6 / 6.7 | 15.7 / 18.0 / 28.9 | 1034.0 / 251.4 / 3926.0 | 0.1 / 0.1 / 0.2 | 1053.1 / 270.0 / 3950.9 | 12.832 |
| ig:rule/index:bm25+align=0 | 0.4 / 0.4 / 0.5 | 3.9 / 3.9 / 5.8 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.7 / 0.6 / 1.2 | 1.1 / 1.0 / 1.9 | 0.227 |
| ig:gold/gold:bm25 | 0.1 / 0.1 / 0.2 | 3.6 / 3.2 / 6.2 | 0.6 / 0.3 / 1.5 | 23.5 / 23.9 / 52.9 | 1087.6 / 383.0 / 4605.5 | 0.1 / 0.1 / 0.2 | 1113.1 / 408.5 / 4640.0 | 17.265 |
| ig:gold/gold:bm25+rnorm=minmax | 0.1 / 0.1 / 0.2 | 5.2 / 3.3 / 6.7 | 0.6 / 0.2 / 1.5 | 24.6 / 21.3 / 32.0 | 1126.4 / 455.2 / 4554.8 | 0.1 / 0.1 / 0.2 | 1153.0 / 481.4 / 4586.5 | 17.44 |
| rerank:ce:bm25 | – | 40.2 / 25.2 / 113.0 | – | – | – | – | 9480.0 / 9045.0 / 12441.1 | 23.966 |

Context index build (one-off, ms): bm25: 58 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:gold/gold:bm25+rnorm=minmax | ctx:bm25 | ndcg@10 | +0.029 | [+0.009, +0.050] | 0.009 | 21/9 |
| ig:gold/gold:bm25+rnorm=minmax | ctx:bm25 | mrr | -0.014 | [-0.076, +0.038] | 0.874 | 2/2 |
| ig:gold/gold:bm25+rnorm=minmax | ctx:bm25 | useful@1 | -0.029 | [-0.143, +0.057] | 1.000 | 1/2 |
| ig:rule/index:bm25+align=0 | ctx:bm25 | ndcg@10 | +0.009 | [-0.003, +0.022] | 0.168 | 13/6 |
| ig:rule/index:bm25+align=0 | ctx:bm25 | mrr | -0.011 | [-0.033, +0.000] | 1.000 | 0/1 |
| ig:rule/index:bm25+align=0 | ctx:bm25 | useful@1 | +0.000 | [+0.000, +0.000] | 1.000 | 0/0 |
| ig:rule/index:bm25+rnorm=minmax | ctx:bm25 | ndcg@10 | +0.028 | [+0.011, +0.047] | 0.003 | 19/6 |
| ig:rule/index:bm25+rnorm=minmax | ctx:bm25 | mrr | +0.011 | [-0.017, +0.049] | 0.751 | 2/1 |
| ig:rule/index:bm25+rnorm=minmax | ctx:bm25 | useful@1 | +0.029 | [+0.000, +0.086] | 1.000 | 1/0 |
| ig:rule/index:bm25 | ctx:bm25 | ndcg@10 | +0.019 | [-0.000, +0.041] | 0.069 | 16/8 |
| ig:rule/index:bm25 | ctx:bm25 | mrr | +0.014 | [-0.009, +0.052] | 0.751 | 2/1 |
| ig:rule/index:bm25 | ctx:bm25 | useful@1 | +0.029 | [+0.000, +0.086] | 1.000 | 1/0 |
| ig:gold/gold:bm25 | ctx:bm25 | ndcg@10 | +0.027 | [+0.003, +0.053] | 0.047 | 21/8 |
| ig:gold/gold:bm25 | ctx:bm25 | mrr | -0.017 | [-0.081, +0.038] | 0.750 | 2/2 |
| ig:gold/gold:bm25 | ctx:bm25 | useful@1 | -0.029 | [-0.143, +0.057] | 1.000 | 1/2 |
