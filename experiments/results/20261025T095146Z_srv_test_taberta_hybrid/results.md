# IGBench results (20261025T095146Z_srv_test_taberta_hybrid)

Benchmark `igbench-v1-test` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:taberta | 0.018 | 0.020 | 0.015 | 0.029 | 0.027 | 0.000 | 0.000 |
| ig:gold/gold:taberta | 0.099 | 0.040 | 0.035 | 0.068 | 0.125 | 0.100 | 0.100 |
| ig:rule/index:taberta | 0.079 | 0.030 | 0.030 | 0.058 | 0.075 | 0.050 | 0.100 |
| ig:gold/gold:taberta+rnorm=minmax | 0.078 | 0.040 | 0.025 | 0.052 | 0.092 | 0.050 | 0.100 |
| ig:rule/index:taberta+rnorm=minmax | 0.056 | 0.020 | 0.015 | 0.029 | 0.035 | 0.000 | 0.150 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:taberta | 0.019 | 0.021 | 0.029 | 0.000 |
| ig:gold/gold:taberta | 0.104 | 0.042 | 0.132 | 0.105 |
| ig:rule/index:taberta | 0.083 | 0.032 | 0.079 | 0.053 |
| ig:gold/gold:taberta+rnorm=minmax | 0.082 | 0.042 | 0.097 | 0.053 |
| ig:rule/index:taberta+rnorm=minmax | 0.059 | 0.021 | 0.037 | 0.000 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:taberta | 0.000 | 0.021 | 0.029 |
| ig:gold/gold:taberta | 0.022 | 0.043 | 0.068 |
| ig:rule/index:taberta | 0.013 | 0.033 | 0.058 |
| ig:gold/gold:taberta+rnorm=minmax | 0.010 | 0.043 | 0.052 |
| ig:rule/index:taberta+rnorm=minmax | 0.000 | 0.021 | 0.029 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | compare (n=8) | explain (n=3) | monitor (n=5) | predict (n=4) |
|---|---|---|---|---|
| ctx:taberta | 0.025 | 0.055 | 0.000 | 0.000 |
| ig:gold/gold:taberta | 0.110 | 0.338 | 0.000 | 0.023 |
| ig:rule/index:taberta | 0.098 | 0.267 | 0.000 | 0.000 |
| ig:gold/gold:taberta+rnorm=minmax | 0.071 | 0.277 | 0.013 | 0.023 |
| ig:rule/index:taberta+rnorm=minmax | 0.071 | 0.162 | 0.012 | 0.000 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:taberta | 0.514 |
| ig:gold/gold:taberta | 0.504 |
| ig:rule/index:taberta | 0.474 |
| ig:gold/gold:taberta+rnorm=minmax | 0.508 |
| ig:rule/index:taberta+rnorm=minmax | 0.469 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:gold/gold:taberta | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.667 | 0.286 |
| ig:rule/index:taberta | 1.000 | 0.815 | 0.950 | 1.000 | 1.000 | 0.947 | 0.807 | 0.000 | 0.200 | 0.167 |
| ig:gold/gold:taberta+rnorm=minmax | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.667 | 0.286 |
| ig:rule/index:taberta+rnorm=minmax | 1.000 | 0.815 | 0.950 | 1.000 | 1.000 | 0.947 | 0.807 | 0.000 | 0.200 | 0.167 |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:taberta | – | 31.8 / 29.2 / 36.2 | – | – | – | – | 31.8 / 29.2 / 36.3 | 0.669 |
| ig:gold/gold:taberta | 0.1 / 0.1 / 0.1 | 30.1 / 29.5 / 32.4 | 0.2 / 0.2 / 0.3 | 62.2 / 21.7 / 190.1 | 97.5 / 35.5 / 311.6 | 0.1 / 0.1 / 0.1 | 190.9 / 178.2 / 397.1 | 4.021 |
| ig:rule/index:taberta | 0.7 / 0.2 / 0.6 | 30.1 / 29.4 / 32.7 | 0.3 / 0.3 / 0.4 | 36.3 / 19.3 / 22.1 | 153.5 / 35.3 / 206.3 | 0.1 / 0.1 / 0.1 | 222.4 / 87.1 / 355.0 | 4.678 |
| ig:gold/gold:taberta+rnorm=minmax | 0.1 / 0.1 / 0.1 | 29.8 / 29.1 / 31.1 | 0.2 / 0.2 / 0.3 | 17.3 / 18.5 / 20.9 | 96.0 / 33.6 / 298.2 | 0.1 / 0.1 / 0.1 | 144.2 / 83.8 / 348.7 | 3.047 |
| ig:rule/index:taberta+rnorm=minmax | 0.2 / 0.2 / 0.2 | 30.2 / 29.1 / 34.6 | 0.3 / 0.3 / 0.3 | 36.1 / 18.5 / 38.5 | 154.3 / 35.1 / 202.7 | 0.1 / 0.1 / 0.1 | 222.0 / 94.0 / 263.5 | 4.681 |

Context index build (one-off, ms): taberta: 8429 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:rule/index:taberta+rnorm=minmax | ctx:taberta | ndcg@10 | +0.036 | [+0.010, +0.067] | 0.033 | 6/0 |
| ig:rule/index:taberta+rnorm=minmax | ctx:taberta | mrr | +0.008 | [-0.010, +0.035] | 1.000 | 1/2 |
| ig:rule/index:taberta+rnorm=minmax | ctx:taberta | useful@1 | +0.000 | [+0.000, +0.000] | 1.000 | 0/0 |
| ig:gold/gold:taberta+rnorm=minmax | ctx:taberta | ndcg@10 | +0.057 | [+0.018, +0.102] | 0.015 | 7/0 |
| ig:gold/gold:taberta+rnorm=minmax | ctx:taberta | mrr | +0.064 | [-0.002, +0.174] | 0.246 | 3/1 |
| ig:gold/gold:taberta+rnorm=minmax | ctx:taberta | useful@1 | +0.050 | [+0.000, +0.150] | 1.000 | 1/0 |
| ig:gold/gold:taberta | ctx:taberta | ndcg@10 | +0.077 | [+0.025, +0.135] | 0.016 | 7/0 |
| ig:gold/gold:taberta | ctx:taberta | mrr | +0.098 | [+0.000, +0.235] | 0.246 | 3/1 |
| ig:gold/gold:taberta | ctx:taberta | useful@1 | +0.100 | [+0.000, +0.250] | 0.499 | 2/0 |
| ig:rule/index:taberta | ctx:taberta | ndcg@10 | +0.058 | [+0.012, +0.111] | 0.063 | 5/0 |
| ig:rule/index:taberta | ctx:taberta | mrr | +0.048 | [-0.004, +0.135] | 0.500 | 2/1 |
| ig:rule/index:taberta | ctx:taberta | useful@1 | +0.050 | [+0.000, +0.150] | 1.000 | 1/0 |
