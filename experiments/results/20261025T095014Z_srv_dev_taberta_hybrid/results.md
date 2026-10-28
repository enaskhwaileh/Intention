# IGBench results (20261025T095014Z_srv_dev_taberta_hybrid)

Benchmark `igbench-v1` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:taberta | 0.023 | 0.000 | 0.009 | 0.013 | 0.015 | 0.000 | 0.086 |
| ig:gold/gold:taberta | 0.043 | 0.023 | 0.014 | 0.059 | 0.104 | 0.086 | 0.029 |
| ig:rule/index:taberta | 0.032 | 0.023 | 0.011 | 0.019 | 0.087 | 0.057 | 0.029 |
| ig:gold/gold:taberta+rnorm=minmax | 0.027 | 0.006 | 0.011 | 0.057 | 0.043 | 0.029 | 0.057 |
| ig:rule/index:taberta+rnorm=minmax | 0.025 | 0.011 | 0.009 | 0.017 | 0.050 | 0.029 | 0.029 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:taberta | 0.025 | 0.000 | 0.017 | 0.000 |
| ig:gold/gold:taberta | 0.047 | 0.025 | 0.114 | 0.094 |
| ig:rule/index:taberta | 0.035 | 0.025 | 0.096 | 0.062 |
| ig:gold/gold:taberta+rnorm=minmax | 0.030 | 0.006 | 0.047 | 0.031 |
| ig:rule/index:taberta+rnorm=minmax | 0.027 | 0.013 | 0.054 | 0.031 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:taberta | 0.000 | 0.000 | 0.013 |
| ig:gold/gold:taberta | 0.042 | 0.044 | 0.059 |
| ig:rule/index:taberta | 0.013 | 0.019 | 0.019 |
| ig:gold/gold:taberta+rnorm=minmax | 0.004 | 0.004 | 0.057 |
| ig:rule/index:taberta+rnorm=minmax | 0.004 | 0.008 | 0.017 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | aggregate (n=3) | compare (n=10) | explain (n=7) | monitor (n=5) | predict (n=8) |
|---|---|---|---|---|---|
| ctx:taberta | 0.045 | 0.023 | 0.017 | 0.015 | 0.032 |
| ig:gold/gold:taberta | 0.089 | 0.061 | 0.009 | 0.092 | 0.015 |
| ig:rule/index:taberta | 0.056 | 0.058 | 0.000 | 0.048 | 0.015 |
| ig:gold/gold:taberta+rnorm=minmax | 0.089 | 0.033 | 0.028 | 0.031 | 0.000 |
| ig:rule/index:taberta+rnorm=minmax | 0.056 | 0.030 | 0.022 | 0.048 | 0.000 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:taberta | 0.512 |
| ig:gold/gold:taberta | 0.532 |
| ig:rule/index:taberta | 0.512 |
| ig:gold/gold:taberta+rnorm=minmax | 0.532 |
| ig:rule/index:taberta+rnorm=minmax | 0.512 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:gold/gold:taberta | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.429 | 0.500 |
| ig:rule/index:taberta | 1.000 | 0.825 | 0.970 | 0.833 | 0.812 | 0.812 | 0.688 | 0.188 | 0.222 | 0.500 |
| ig:gold/gold:taberta+rnorm=minmax | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.429 | 0.500 |
| ig:rule/index:taberta+rnorm=minmax | 1.000 | 0.825 | 0.970 | 0.833 | 0.812 | 0.812 | 0.688 | 0.188 | 0.222 | 0.500 |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:taberta | – | 37.8 / 27.5 / 37.2 | – | – | – | – | 37.9 / 27.6 / 37.3 | 1.365 |
| ig:gold/gold:taberta | 0.1 / 0.1 / 0.1 | 30.2 / 29.0 / 37.4 | 0.2 / 0.2 / 0.3 | 201.9 / 109.0 / 670.1 | 292.7 / 35.9 / 1262.1 | 0.1 / 0.1 / 0.1 | 526.4 / 242.2 / 1632.1 | 18.977 |
| ig:rule/index:taberta | 0.4 / 0.2 / 0.7 | 33.1 / 31.4 / 42.5 | 0.3 / 0.3 / 0.4 | 98.0 / 21.0 / 260.4 | 215.2 / 28.2 / 797.5 | 0.1 / 0.1 / 0.1 | 348.2 / 93.6 / 1426.4 | 12.571 |
| ig:gold/gold:taberta+rnorm=minmax | 0.1 / 0.1 / 0.1 | 39.5 / 31.5 / 44.0 | 0.2 / 0.2 / 0.3 | 391.4 / 27.1 / 1595.3 | 422.5 / 42.6 / 2464.6 | 0.1 / 0.1 / 0.2 | 855.0 / 205.3 / 3813.5 | 30.832 |
| ig:rule/index:taberta+rnorm=minmax | 0.2 / 0.2 / 0.2 | 33.3 / 32.1 / 42.3 | 0.3 / 0.3 / 0.4 | 155.7 / 210.2 / 256.8 | 250.9 / 39.9 / 1028.7 | 0.1 / 0.1 / 0.1 | 441.9 / 318.2 / 1323.7 | 15.955 |

Context index build (one-off, ms): taberta: 428687

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:rule/index:taberta+rnorm=minmax | ctx:taberta | ndcg@10 | +0.001 | [-0.017, +0.018] | 0.905 | 6/7 |
| ig:rule/index:taberta+rnorm=minmax | ctx:taberta | mrr | +0.034 | [-0.007, +0.097] | 0.325 | 5/3 |
| ig:rule/index:taberta+rnorm=minmax | ctx:taberta | useful@1 | +0.029 | [+0.000, +0.086] | 1.000 | 1/0 |
| ig:gold/gold:taberta+rnorm=minmax | ctx:taberta | ndcg@10 | +0.004 | [-0.018, +0.024] | 0.735 | 6/8 |
| ig:gold/gold:taberta+rnorm=minmax | ctx:taberta | mrr | +0.027 | [-0.010, +0.093] | 0.410 | 6/3 |
| ig:gold/gold:taberta+rnorm=minmax | ctx:taberta | useful@1 | +0.029 | [+0.000, +0.086] | 1.000 | 1/0 |
| ig:gold/gold:taberta | ctx:taberta | ndcg@10 | +0.019 | [-0.015, +0.060] | 0.339 | 7/8 |
| ig:gold/gold:taberta | ctx:taberta | mrr | +0.089 | [+0.008, +0.186] | 0.110 | 6/3 |
| ig:gold/gold:taberta | ctx:taberta | useful@1 | +0.086 | [+0.000, +0.200] | 0.256 | 3/0 |
| ig:rule/index:taberta | ctx:taberta | ndcg@10 | +0.008 | [-0.018, +0.039] | 0.609 | 6/7 |
| ig:rule/index:taberta | ctx:taberta | mrr | +0.072 | [+0.004, +0.159] | 0.118 | 5/3 |
| ig:rule/index:taberta | ctx:taberta | useful@1 | +0.057 | [+0.000, +0.143] | 0.499 | 2/0 |
