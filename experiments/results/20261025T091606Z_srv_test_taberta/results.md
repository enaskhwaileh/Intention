# IGBench results (20261025T091606Z_srv_test_taberta)

Benchmark `igbench-v1-test` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:taberta | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| ig:gold/gold:taberta | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| ig:rule/index:taberta | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| ig:gold/gold:taberta+rnorm=minmax | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| ig:rule/index:taberta+rnorm=minmax | 0.001 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:taberta | 0.000 | 0.000 | 0.000 | 0.000 |
| ig:gold/gold:taberta | 0.000 | 0.000 | 0.000 | 0.000 |
| ig:rule/index:taberta | 0.000 | 0.000 | 0.000 | 0.000 |
| ig:gold/gold:taberta+rnorm=minmax | 0.000 | 0.000 | 0.000 | 0.000 |
| ig:rule/index:taberta+rnorm=minmax | 0.002 | 0.000 | 0.000 | 0.000 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:taberta | 0.000 | 0.000 | 0.000 |
| ig:gold/gold:taberta | 0.000 | 0.000 | 0.000 |
| ig:rule/index:taberta | 0.000 | 0.000 | 0.000 |
| ig:gold/gold:taberta+rnorm=minmax | 0.000 | 0.000 | 0.000 |
| ig:rule/index:taberta+rnorm=minmax | 0.000 | 0.000 | 0.000 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | compare (n=8) | explain (n=3) | monitor (n=5) | predict (n=4) |
|---|---|---|---|---|
| ctx:taberta | 0.000 | 0.000 | 0.000 | 0.000 |
| ig:gold/gold:taberta | 0.000 | 0.000 | 0.000 | 0.000 |
| ig:rule/index:taberta | 0.000 | 0.000 | 0.000 | 0.000 |
| ig:gold/gold:taberta+rnorm=minmax | 0.000 | 0.000 | 0.000 | 0.000 |
| ig:rule/index:taberta+rnorm=minmax | 0.000 | 0.000 | 0.000 | 0.007 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:taberta | 0.500 |
| ig:gold/gold:taberta | 0.497 |
| ig:rule/index:taberta | 0.494 |
| ig:gold/gold:taberta+rnorm=minmax | 0.497 |
| ig:rule/index:taberta+rnorm=minmax | 0.494 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:gold/gold:taberta | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | – | – |
| ig:rule/index:taberta | 1.000 | 0.815 | 0.950 | 1.000 | 1.000 | 0.947 | 0.807 | 0.000 | – | – |
| ig:gold/gold:taberta+rnorm=minmax | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | – | – |
| ig:rule/index:taberta+rnorm=minmax | 1.000 | 0.815 | 0.950 | 1.000 | 1.000 | 0.947 | 0.807 | 0.000 | – | – |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:taberta | – | 32.6 / 18.3 / 23.8 | – | – | – | – | 32.6 / 18.4 / 23.9 | 0.686 |
| ig:gold/gold:taberta | 0.1 / 0.1 / 0.1 | 20.6 / 20.1 / 25.1 | 0.2 / 0.1 / 0.2 | 67.3 / 16.0 / 213.7 | 76.4 / 32.1 / 205.2 | 0.1 / 0.1 / 0.1 | 165.4 / 76.9 / 361.9 | 3.509 |
| ig:rule/index:taberta | 0.5 / 0.2 / 0.7 | 20.6 / 21.7 / 25.7 | 0.3 / 0.2 / 0.3 | 100.5 / 23.5 / 217.3 | 70.7 / 31.8 / 164.1 | 0.1 / 0.1 / 0.1 | 193.8 / 72.1 / 524.4 | 4.127 |
| ig:gold/gold:taberta+rnorm=minmax | 0.1 / 0.1 / 0.1 | 18.5 / 17.6 / 23.8 | 0.1 / 0.1 / 0.2 | 61.0 / 13.8 / 33.6 | 54.5 / 25.1 / 124.1 | 0.1 / 0.1 / 0.1 | 135.1 / 65.0 / 251.2 | 2.879 |
| ig:rule/index:taberta+rnorm=minmax | 0.2 / 0.2 / 0.2 | 21.3 / 22.7 / 25.1 | 0.2 / 0.2 / 0.3 | 90.0 / 15.2 / 212.5 | 78.3 / 32.5 / 233.9 | 0.1 / 0.1 / 0.1 | 190.8 / 71.5 / 500.2 | 4.076 |

Context index build (one-off, ms): taberta: 9932 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:rule/index:taberta+rnorm=minmax | ctx:taberta | ndcg@10 | +0.001 | [+0.000, +0.004] | 1.000 | 1/0 |
| ig:rule/index:taberta+rnorm=minmax | ctx:taberta | mrr | +0.000 | [+0.000, +0.000] | 1.000 | 0/0 |
| ig:rule/index:taberta+rnorm=minmax | ctx:taberta | useful@1 | +0.000 | [+0.000, +0.000] | 1.000 | 0/0 |
| ig:gold/gold:taberta+rnorm=minmax | ctx:taberta | ndcg@10 | +0.000 | [+0.000, +0.000] | 1.000 | 0/0 |
| ig:gold/gold:taberta+rnorm=minmax | ctx:taberta | mrr | +0.000 | [+0.000, +0.000] | 1.000 | 0/0 |
| ig:gold/gold:taberta+rnorm=minmax | ctx:taberta | useful@1 | +0.000 | [+0.000, +0.000] | 1.000 | 0/0 |
| ig:gold/gold:taberta | ctx:taberta | ndcg@10 | +0.000 | [+0.000, +0.000] | 1.000 | 0/0 |
| ig:gold/gold:taberta | ctx:taberta | mrr | +0.000 | [+0.000, +0.000] | 1.000 | 0/0 |
| ig:gold/gold:taberta | ctx:taberta | useful@1 | +0.000 | [+0.000, +0.000] | 1.000 | 0/0 |
| ig:rule/index:taberta | ctx:taberta | ndcg@10 | +0.000 | [+0.000, +0.000] | 1.000 | 0/0 |
| ig:rule/index:taberta | ctx:taberta | mrr | +0.000 | [+0.000, +0.000] | 1.000 | 0/0 |
| ig:rule/index:taberta | ctx:taberta | useful@1 | +0.000 | [+0.000, +0.000] | 1.000 | 0/0 |
