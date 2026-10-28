# IGBench results (20261025T091517Z_srv_dev_taberta)

Benchmark `igbench-v1` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:taberta | 0.003 | 0.000 | 0.000 | 0.000 | 0.001 | 0.000 | 0.000 |
| ig:gold/gold:taberta | 0.002 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| ig:rule/index:taberta | 0.011 | 0.006 | 0.003 | 0.005 | 0.029 | 0.029 | 0.029 |
| ig:gold/gold:taberta+rnorm=minmax | 0.001 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| ig:rule/index:taberta+rnorm=minmax | 0.001 | 0.000 | 0.000 | 0.000 | 0.002 | 0.000 | 0.000 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:taberta | 0.003 | 0.000 | 0.001 | 0.000 |
| ig:gold/gold:taberta | 0.002 | 0.000 | 0.000 | 0.000 |
| ig:rule/index:taberta | 0.012 | 0.006 | 0.031 | 0.031 |
| ig:gold/gold:taberta+rnorm=minmax | 0.001 | 0.000 | 0.000 | 0.000 |
| ig:rule/index:taberta+rnorm=minmax | 0.001 | 0.000 | 0.003 | 0.000 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:taberta | 0.000 | 0.000 | 0.000 |
| ig:gold/gold:taberta | 0.000 | 0.000 | 0.000 |
| ig:rule/index:taberta | 0.005 | 0.005 | 0.005 |
| ig:gold/gold:taberta+rnorm=minmax | 0.000 | 0.000 | 0.000 |
| ig:rule/index:taberta+rnorm=minmax | 0.000 | 0.000 | 0.000 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | aggregate (n=3) | compare (n=10) | explain (n=7) | monitor (n=5) | predict (n=8) |
|---|---|---|---|---|---|
| ctx:taberta | 0.000 | 0.004 | 0.003 | 0.006 | 0.000 |
| ig:gold/gold:taberta | 0.000 | 0.005 | 0.004 | 0.000 | 0.000 |
| ig:rule/index:taberta | 0.000 | 0.005 | 0.011 | 0.000 | 0.034 |
| ig:gold/gold:taberta+rnorm=minmax | 0.000 | 0.002 | 0.000 | 0.005 | 0.000 |
| ig:rule/index:taberta+rnorm=minmax | 0.000 | 0.002 | 0.000 | 0.000 | 0.000 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:taberta | 0.540 |
| ig:gold/gold:taberta | 0.488 |
| ig:rule/index:taberta | 0.502 |
| ig:gold/gold:taberta+rnorm=minmax | 0.488 |
| ig:rule/index:taberta+rnorm=minmax | 0.502 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:gold/gold:taberta | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | – | – |
| ig:rule/index:taberta | 1.000 | 0.825 | 0.970 | 0.833 | 0.812 | 0.812 | 0.688 | 0.188 | – | 0.000 |
| ig:gold/gold:taberta+rnorm=minmax | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | – | – |
| ig:rule/index:taberta+rnorm=minmax | 1.000 | 0.825 | 0.970 | 0.833 | 0.812 | 0.812 | 0.688 | 0.188 | – | 0.000 |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:taberta | – | 11.3 / 10.7 / 13.1 | – | – | – | – | 11.4 / 10.8 / 13.2 | 0.411 |
| ig:gold/gold:taberta | 0.1 / 0.1 / 0.1 | 27.9 / 14.1 / 29.6 | 0.2 / 0.1 / 0.2 | 536.9 / 42.5 / 358.8 | 67.3 / 22.2 / 229.2 | 0.1 / 0.1 / 0.1 | 633.2 / 141.3 / 566.7 | 22.837 |
| ig:rule/index:taberta | 0.4 / 0.2 / 0.6 | 20.0 / 13.9 / 24.9 | 0.3 / 0.2 / 0.5 | 61.1 / 14.3 / 242.1 | 47.0 / 16.9 / 145.8 | 0.1 / 0.1 / 0.1 | 129.8 / 55.2 / 303.2 | 4.715 |
| ig:gold/gold:taberta+rnorm=minmax | 0.1 / 0.1 / 0.1 | 23.3 / 23.1 / 25.7 | 0.1 / 0.1 / 0.2 | 41.9 / 13.7 / 32.4 | 57.3 / 20.1 / 158.1 | 0.1 / 0.1 / 0.1 | 123.4 / 58.1 / 285.6 | 4.489 |
| ig:rule/index:taberta+rnorm=minmax | 0.1 / 0.1 / 0.2 | 23.1 / 23.0 / 25.2 | 0.2 / 0.2 / 0.3 | 38.6 / 13.4 / 201.6 | 52.5 / 17.5 / 145.6 | 0.1 / 0.1 / 0.1 | 115.2 / 56.6 / 293.8 | 4.188 |

Context index build (one-off, ms): taberta: 26029

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:rule/index:taberta+rnorm=minmax | ctx:taberta | ndcg@10 | -0.002 | [-0.006, +0.001] | 0.371 | 1/3 |
| ig:rule/index:taberta+rnorm=minmax | ctx:taberta | mrr | +0.002 | [-0.003, +0.007] | 1.000 | 1/1 |
| ig:rule/index:taberta+rnorm=minmax | ctx:taberta | useful@1 | +0.000 | [+0.000, +0.000] | 1.000 | 0/0 |
| ig:gold/gold:taberta+rnorm=minmax | ctx:taberta | ndcg@10 | -0.001 | [-0.005, +0.001] | 0.492 | 1/3 |
| ig:gold/gold:taberta+rnorm=minmax | ctx:taberta | mrr | -0.001 | [-0.003, +0.000] | 1.000 | 0/1 |
| ig:gold/gold:taberta+rnorm=minmax | ctx:taberta | useful@1 | +0.000 | [+0.000, +0.000] | 1.000 | 0/0 |
| ig:gold/gold:taberta | ctx:taberta | ndcg@10 | -0.001 | [-0.005, +0.003] | 1.000 | 2/2 |
| ig:gold/gold:taberta | ctx:taberta | mrr | -0.001 | [-0.003, +0.000] | 1.000 | 0/1 |
| ig:gold/gold:taberta | ctx:taberta | useful@1 | +0.000 | [+0.000, +0.000] | 1.000 | 0/0 |
| ig:rule/index:taberta | ctx:taberta | ndcg@10 | +0.008 | [-0.003, +0.026] | 0.378 | 3/2 |
| ig:rule/index:taberta | ctx:taberta | mrr | +0.028 | [-0.003, +0.086] | 1.000 | 1/1 |
| ig:rule/index:taberta | ctx:taberta | useful@1 | +0.029 | [+0.000, +0.086] | 1.000 | 1/0 |
