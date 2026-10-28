# IGBench results (20261025T110203Z_plan_igb-test_hybrid)

Benchmark `igbench-v1-test` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:hybrid | 0.845 | 0.560 | 0.335 | 0.907 | 0.950 | 0.900 | 0.050 |
| ig:rule/index:hybrid | 0.828 | 0.570 | 0.350 | 0.944 | 0.925 | 0.850 | 0.050 |
| ig:rule/index:hybrid+rnorm=minmax | 0.852 | 0.560 | 0.355 | 0.948 | 0.925 | 0.850 | 0.050 |
| ig:rule/index:hybrid+align=0 | 0.842 | 0.540 | 0.340 | 0.924 | 0.892 | 0.800 | 0.100 |
| ig:gold/gold:hybrid | 0.842 | 0.570 | 0.350 | 0.944 | 0.950 | 0.900 | 0.000 |
| ig:gold/gold:hybrid+rnorm=minmax | 0.878 | 0.560 | 0.355 | 0.948 | 0.975 | 0.950 | 0.000 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:hybrid | 0.839 | 0.547 | 0.947 | 0.895 |
| ig:rule/index:hybrid | 0.821 | 0.558 | 0.921 | 0.842 |
| ig:rule/index:hybrid+rnorm=minmax | 0.846 | 0.547 | 0.921 | 0.842 |
| ig:rule/index:hybrid+align=0 | 0.836 | 0.526 | 0.886 | 0.789 |
| ig:gold/gold:hybrid | 0.835 | 0.558 | 0.947 | 0.895 |
| ig:gold/gold:hybrid+rnorm=minmax | 0.874 | 0.547 | 0.974 | 0.947 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:hybrid | 0.424 | 0.833 | 0.907 |
| ig:rule/index:hybrid | 0.295 | 0.839 | 0.944 |
| ig:rule/index:hybrid+rnorm=minmax | 0.335 | 0.829 | 0.948 |
| ig:rule/index:hybrid+align=0 | 0.389 | 0.798 | 0.924 |
| ig:gold/gold:hybrid | 0.345 | 0.843 | 0.944 |
| ig:gold/gold:hybrid+rnorm=minmax | 0.395 | 0.833 | 0.948 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | compare (n=8) | explain (n=3) | monitor (n=5) | predict (n=4) |
|---|---|---|---|---|
| ctx:hybrid | 0.847 | 0.763 | 0.809 | 0.918 |
| ig:rule/index:hybrid | 0.812 | 0.821 | 0.785 | 0.858 |
| ig:rule/index:hybrid+rnorm=minmax | 0.824 | 0.792 | 0.871 | 0.869 |
| ig:rule/index:hybrid+align=0 | 0.835 | 0.765 | 0.791 | 0.918 |
| ig:gold/gold:hybrid | 0.811 | 0.841 | 0.801 | 0.893 |
| ig:gold/gold:hybrid+rnorm=minmax | 0.823 | 0.839 | 0.913 | 0.916 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:hybrid | 0.860 |
| ig:rule/index:hybrid | 0.882 |
| ig:rule/index:hybrid+rnorm=minmax | 0.882 |
| ig:rule/index:hybrid+align=0 | 0.847 |
| ig:gold/gold:hybrid | 0.882 |
| ig:gold/gold:hybrid+rnorm=minmax | 0.882 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:rule/index:hybrid | 1.000 | 0.815 | 0.950 | 1.000 | 1.000 | 0.947 | 0.807 | 0.000 | 0.542 | 0.643 |
| ig:rule/index:hybrid+rnorm=minmax | 1.000 | 0.815 | 0.950 | 1.000 | 1.000 | 0.947 | 0.807 | 0.000 | 0.542 | 0.643 |
| ig:rule/index:hybrid+align=0 | 1.000 | 0.815 | 0.950 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | – | – |
| ig:gold/gold:hybrid | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.570 | 0.757 |
| ig:gold/gold:hybrid+rnorm=minmax | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.570 | 0.757 |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:hybrid | – | 112.2 / 91.5 / 99.6 | – | – | – | – | 112.4 / 91.7 / 99.7 | 2.36 |
| ig:rule/index:hybrid | 1.0 / 0.4 / 2.0 | 89.5 / 90.1 / 95.1 | 2.0 / 0.3 / 6.9 | 22.9 / 22.5 / 31.2 | 251.9 / 158.5 / 383.3 | 0.1 / 0.1 / 0.1 | 278.9 / 198.7 / 409.1 | 5.374 |
| ig:rule/index:hybrid+rnorm=minmax | 0.4 / 0.4 / 0.5 | 91.9 / 90.5 / 96.9 | 2.1 / 0.3 / 7.1 | 82.4 / 23.2 / 340.5 | 273.4 / 153.8 / 653.5 | 0.1 / 0.1 / 0.1 | 359.3 / 245.9 / 717.3 | 5.773 |
| ig:rule/index:hybrid+align=0 | 0.4 / 0.4 / 0.4 | 91.3 / 91.1 / 99.1 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.7 / 0.5 / 1.2 | 1.1 / 0.9 / 1.7 | 2.316 |
| ig:gold/gold:hybrid | 0.1 / 0.1 / 0.1 | 87.0 / 86.5 / 93.3 | 0.7 / 0.2 / 2.2 | 24.0 / 23.1 / 42.8 | 251.9 / 147.4 / 472.5 | 0.1 / 0.1 / 0.1 | 278.0 / 175.5 / 493.0 | 5.06 |
| ig:gold/gold:hybrid+rnorm=minmax | 0.1 / 0.1 / 0.1 | 91.7 / 90.9 / 95.9 | 0.9 / 0.2 / 2.8 | 23.9 / 21.7 / 38.8 | 250.8 / 153.0 / 461.1 | 0.1 / 0.1 / 0.1 | 276.9 / 184.2 / 480.2 | 5.178 |

Context index build (one-off, ms): hybrid: 12803 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:rule/index:hybrid+align=0 | ctx:hybrid | ndcg@10 | -0.009 | [-0.029, +0.011] | 0.421 | 4/9 |
| ig:rule/index:hybrid+align=0 | ctx:hybrid | mrr | -0.058 | [-0.133, +0.000] | 0.244 | 0/3 |
| ig:rule/index:hybrid+align=0 | ctx:hybrid | useful@1 | -0.100 | [-0.250, +0.000] | 0.498 | 0/2 |
| ig:rule/index:hybrid | ctx:hybrid | ndcg@10 | -0.022 | [-0.079, +0.032] | 0.465 | 8/9 |
| ig:rule/index:hybrid | ctx:hybrid | mrr | -0.025 | [-0.125, +0.075] | 1.000 | 2/3 |
| ig:rule/index:hybrid | ctx:hybrid | useful@1 | -0.050 | [-0.250, +0.150] | 1.000 | 2/3 |
| ig:gold/gold:hybrid+rnorm=minmax | ctx:hybrid | ndcg@10 | +0.026 | [-0.023, +0.070] | 0.329 | 9/6 |
| ig:gold/gold:hybrid+rnorm=minmax | ctx:hybrid | mrr | +0.025 | [-0.050, +0.125] | 1.000 | 2/1 |
| ig:gold/gold:hybrid+rnorm=minmax | ctx:hybrid | useful@1 | +0.050 | [-0.100, +0.250] | 1.000 | 2/1 |
| ig:rule/index:hybrid+rnorm=minmax | ctx:hybrid | ndcg@10 | +0.001 | [-0.046, +0.044] | 0.979 | 9/6 |
| ig:rule/index:hybrid+rnorm=minmax | ctx:hybrid | mrr | -0.025 | [-0.125, +0.075] | 1.000 | 2/3 |
| ig:rule/index:hybrid+rnorm=minmax | ctx:hybrid | useful@1 | -0.050 | [-0.250, +0.150] | 1.000 | 2/3 |
| ig:gold/gold:hybrid | ctx:hybrid | ndcg@10 | -0.009 | [-0.066, +0.043] | 0.756 | 7/10 |
| ig:gold/gold:hybrid | ctx:hybrid | mrr | +0.000 | [-0.100, +0.100] | 1.000 | 2/2 |
| ig:gold/gold:hybrid | ctx:hybrid | useful@1 | +0.000 | [-0.200, +0.200] | 1.000 | 2/2 |
