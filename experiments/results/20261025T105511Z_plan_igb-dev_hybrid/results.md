# IGBench results (20261025T105511Z_plan_igb-dev_hybrid)

Benchmark `igbench-v1` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:hybrid | 0.814 | 0.543 | 0.334 | 0.884 | 0.876 | 0.771 | 0.143 |
| ig:rule/index:hybrid | 0.811 | 0.549 | 0.337 | 0.891 | 0.886 | 0.771 | 0.114 |
| ig:rule/index:hybrid+rnorm=minmax | 0.822 | 0.554 | 0.334 | 0.886 | 0.881 | 0.771 | 0.114 |
| ig:rule/index:hybrid+align=0 | 0.792 | 0.509 | 0.323 | 0.874 | 0.833 | 0.714 | 0.171 |
| ig:gold/gold:hybrid | 0.821 | 0.531 | 0.340 | 0.891 | 0.900 | 0.829 | 0.114 |
| ig:gold/gold:hybrid+rnorm=minmax | 0.820 | 0.549 | 0.331 | 0.878 | 0.876 | 0.771 | 0.143 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:hybrid | 0.821 | 0.525 | 0.896 | 0.812 |
| ig:rule/index:hybrid | 0.818 | 0.531 | 0.906 | 0.812 |
| ig:rule/index:hybrid+rnorm=minmax | 0.830 | 0.537 | 0.901 | 0.812 |
| ig:rule/index:hybrid+align=0 | 0.797 | 0.487 | 0.848 | 0.750 |
| ig:gold/gold:hybrid | 0.829 | 0.512 | 0.922 | 0.875 |
| ig:gold/gold:hybrid+rnorm=minmax | 0.828 | 0.531 | 0.896 | 0.812 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:hybrid | 0.312 | 0.789 | 0.884 |
| ig:rule/index:hybrid | 0.318 | 0.796 | 0.891 |
| ig:rule/index:hybrid+rnorm=minmax | 0.313 | 0.801 | 0.886 |
| ig:rule/index:hybrid+align=0 | 0.295 | 0.744 | 0.874 |
| ig:gold/gold:hybrid | 0.349 | 0.778 | 0.891 |
| ig:gold/gold:hybrid+rnorm=minmax | 0.311 | 0.792 | 0.878 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | aggregate (n=3) | compare (n=10) | explain (n=7) | monitor (n=5) | predict (n=8) |
|---|---|---|---|---|---|
| ctx:hybrid | 0.984 | 0.853 | 0.831 | 0.714 | 0.789 |
| ig:rule/index:hybrid | 0.983 | 0.892 | 0.829 | 0.705 | 0.737 |
| ig:rule/index:hybrid+rnorm=minmax | 0.984 | 0.866 | 0.839 | 0.717 | 0.801 |
| ig:rule/index:hybrid+align=0 | 0.984 | 0.831 | 0.795 | 0.683 | 0.772 |
| ig:gold/gold:hybrid | 0.983 | 0.883 | 0.852 | 0.768 | 0.730 |
| ig:gold/gold:hybrid+rnorm=minmax | 0.984 | 0.862 | 0.845 | 0.748 | 0.774 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:hybrid | 0.808 |
| ig:rule/index:hybrid | 0.841 |
| ig:rule/index:hybrid+rnorm=minmax | 0.839 |
| ig:rule/index:hybrid+align=0 | 0.785 |
| ig:gold/gold:hybrid | 0.834 |
| ig:gold/gold:hybrid+rnorm=minmax | 0.828 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:rule/index:hybrid | 1.000 | 0.825 | 0.970 | 0.833 | 0.812 | 0.812 | 0.688 | 0.188 | 0.474 | 0.788 |
| ig:rule/index:hybrid+rnorm=minmax | 1.000 | 0.825 | 0.970 | 0.833 | 0.812 | 0.812 | 0.688 | 0.188 | 0.474 | 0.788 |
| ig:rule/index:hybrid+align=0 | 1.000 | 0.825 | 0.970 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | – | – |
| ig:gold/gold:hybrid | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.507 | 0.795 |
| ig:gold/gold:hybrid+rnorm=minmax | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.507 | 0.795 |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:hybrid | – | 105.5 / 94.2 / 102.8 | – | – | – | – | 105.7 / 94.4 / 103.0 | 3.804 |
| ig:rule/index:hybrid | 0.7 / 0.4 / 1.3 | 94.3 / 94.4 / 101.8 | 2.0 / 0.6 / 6.5 | 28.9 / 23.2 / 45.9 | 924.3 / 175.2 / 3860.6 | 0.1 / 0.1 / 0.2 | 957.1 / 256.9 / 3886.6 | 15.779 |
| ig:rule/index:hybrid+rnorm=minmax | 0.4 / 0.4 / 0.5 | 91.6 / 91.2 / 99.2 | 1.9 / 0.5 / 7.4 | 70.5 / 22.3 / 404.3 | 978.8 / 170.1 / 4042.2 | 0.1 / 0.1 / 0.2 | 1052.6 / 402.8 / 4085.6 | 16.434 |
| ig:rule/index:hybrid+align=0 | 0.4 / 0.4 / 0.6 | 86.7 / 87.1 / 93.8 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.6 / 0.5 / 1.1 | 1.0 / 1.0 / 1.6 | 3.527 |
| ig:gold/gold:hybrid | 0.1 / 0.1 / 0.2 | 86.6 / 86.3 / 93.6 | 0.6 / 0.3 / 1.7 | 24.6 / 22.9 / 44.7 | 989.8 / 329.4 / 4001.5 | 0.2 / 0.1 / 0.2 | 1016.5 / 359.2 / 4036.6 | 20.192 |
| ig:gold/gold:hybrid+rnorm=minmax | 0.1 / 0.1 / 0.2 | 91.1 / 91.2 / 97.7 | 0.5 / 0.2 / 1.6 | 63.9 / 23.2 / 46.9 | 1028.4 / 340.4 / 4099.9 | 0.1 / 0.1 / 0.2 | 1094.3 / 418.5 / 4123.2 | 20.751 |

Context index build (one-off, ms): hybrid: 13780 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:rule/index:hybrid+align=0 | ctx:hybrid | ndcg@10 | -0.021 | [-0.039, -0.007] | 0.004 | 4/14 |
| ig:rule/index:hybrid+align=0 | ctx:hybrid | mrr | -0.043 | [-0.092, -0.005] | 0.124 | 0/4 |
| ig:rule/index:hybrid+align=0 | ctx:hybrid | useful@1 | -0.057 | [-0.143, +0.000] | 0.500 | 0/2 |
| ig:rule/index:hybrid | ctx:hybrid | ndcg@10 | -0.003 | [-0.029, +0.022] | 0.843 | 13/12 |
| ig:rule/index:hybrid | ctx:hybrid | mrr | +0.009 | [-0.052, +0.081] | 0.751 | 2/2 |
| ig:rule/index:hybrid | ctx:hybrid | useful@1 | +0.000 | [-0.114, +0.114] | 1.000 | 2/2 |
| ig:gold/gold:hybrid+rnorm=minmax | ctx:hybrid | ndcg@10 | +0.006 | [-0.009, +0.022] | 0.457 | 15/11 |
| ig:gold/gold:hybrid+rnorm=minmax | ctx:hybrid | mrr | +0.000 | [-0.057, +0.052] | 1.000 | 2/2 |
| ig:gold/gold:hybrid+rnorm=minmax | ctx:hybrid | useful@1 | +0.000 | [-0.086, +0.086] | 1.000 | 1/1 |
| ig:rule/index:hybrid+rnorm=minmax | ctx:hybrid | ndcg@10 | +0.008 | [-0.005, +0.022] | 0.263 | 13/11 |
| ig:rule/index:hybrid+rnorm=minmax | ctx:hybrid | mrr | +0.005 | [-0.043, +0.057] | 1.000 | 2/2 |
| ig:rule/index:hybrid+rnorm=minmax | ctx:hybrid | useful@1 | +0.000 | [-0.086, +0.086] | 1.000 | 1/1 |
| ig:gold/gold:hybrid | ctx:hybrid | ndcg@10 | +0.006 | [-0.025, +0.035] | 0.726 | 16/11 |
| ig:gold/gold:hybrid | ctx:hybrid | mrr | +0.024 | [-0.052, +0.100] | 0.626 | 3/2 |
| ig:gold/gold:hybrid | ctx:hybrid | useful@1 | +0.057 | [-0.057, +0.171] | 0.626 | 3/1 |
