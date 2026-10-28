# IGBench results (20261025T091740Z_srv_target_spider-test_taberta)

Benchmark `target-spider-test` on corpus `target-spider-test` (180 tables), IL 1.0.0, labels: **established_benchmark_gold**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:taberta | 0.022 | 0.009 | 0.008 | 0.038 | 0.032 | 0.009 | 0.000 |
| ig:rule/index:taberta | 0.026 | 0.010 | 0.009 | 0.044 | 0.037 | 0.012 | 0.000 |
| ig:rule/index:taberta+rnorm=minmax | 0.025 | 0.009 | 0.009 | 0.043 | 0.036 | 0.012 | 0.000 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:taberta | – | – | – | – |
| ig:rule/index:taberta | – | – | – | – |
| ig:rule/index:taberta+rnorm=minmax | – | – | – | – |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:taberta | 0.004 | 0.021 | 0.038 |
| ig:rule/index:taberta | 0.006 | 0.025 | 0.044 |
| ig:rule/index:taberta+rnorm=minmax | 0.005 | 0.025 | 0.043 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | extreme (n=201) | lookup (n=971) | mean (n=162) | total_or_count (n=813) |
|---|---|---|---|---|
| ctx:taberta | 0.006 | 0.025 | 0.008 | 0.025 |
| ig:rule/index:taberta | 0.013 | 0.026 | 0.013 | 0.032 |
| ig:rule/index:taberta+rnorm=minmax | 0.013 | 0.026 | 0.013 | 0.030 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:taberta | – |
| ig:rule/index:taberta | – |
| ig:rule/index:taberta+rnorm=minmax | – |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:taberta | – | 14.6 / 16.4 / 18.4 | – | – | – | – | 14.6 / 16.4 / 18.4 | 31.441 |
| ig:rule/index:taberta | 0.3 / 0.3 / 0.4 | 14.2 / 14.2 / 18.3 | 0.1 / 0.0 / 0.3 | 0.6 / 0.0 / 0.0 | 0.8 / 0.0 / 0.0 | 0.1 / 0.1 / 0.2 | 2.0 / 0.4 / 1.3 | 32.315 |
| ig:rule/index:taberta+rnorm=minmax | 0.3 / 0.3 / 0.4 | 9.2 / 7.7 / 17.3 | 0.1 / 0.0 / 0.4 | 0.7 / 0.0 / 0.0 | 0.9 / 0.0 / 0.0 | 0.1 / 0.1 / 0.2 | 2.2 / 0.4 / 1.4 | 21.917 |

Context index build (one-off, ms): taberta: 9241

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:rule/index:taberta+rnorm=minmax | ctx:taberta | ndcg@10 | +0.004 | [-0.000, +0.007] | 0.064 | 101/75 |
| ig:rule/index:taberta+rnorm=minmax | ctx:taberta | mrr | +0.004 | [-0.001, +0.009] | 0.110 | 362/331 |
| ig:rule/index:taberta+rnorm=minmax | ctx:taberta | useful@1 | +0.003 | [-0.002, +0.008] | 0.379 | 19/13 |
| ig:rule/index:taberta | ctx:taberta | ndcg@10 | +0.004 | [+0.000, +0.008] | 0.030 | 103/77 |
| ig:rule/index:taberta | ctx:taberta | mrr | +0.004 | [-0.001, +0.009] | 0.084 | 361/333 |
| ig:rule/index:taberta | ctx:taberta | useful@1 | +0.003 | [-0.003, +0.008] | 0.411 | 21/15 |
