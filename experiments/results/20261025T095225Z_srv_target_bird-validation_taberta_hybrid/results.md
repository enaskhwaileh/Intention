# IGBench results (20261025T095225Z_srv_target_bird-validation_taberta_hybrid)

Benchmark `target-bird-validation` on corpus `target-bird-validation` (75 tables), IL 1.0.0, labels: **established_benchmark_gold**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:taberta | 0.258 | 0.099 | 0.082 | 0.422 | 0.251 | 0.126 | 0.000 |
| ig:rule/index:taberta | 0.247 | 0.095 | 0.078 | 0.397 | 0.245 | 0.129 | 0.000 |
| ig:rule/index:taberta+rnorm=minmax | 0.247 | 0.095 | 0.078 | 0.397 | 0.245 | 0.129 | 0.000 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:taberta | – | – | – | – |
| ig:rule/index:taberta | – | – | – | – |
| ig:rule/index:taberta+rnorm=minmax | – | – | – | – |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:taberta | 0.063 | 0.254 | 0.422 |
| ig:rule/index:taberta | 0.066 | 0.242 | 0.397 |
| ig:rule/index:taberta+rnorm=minmax | 0.066 | 0.242 | 0.397 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | extreme (n=235) | lookup (n=655) | mean (n=55) | total_or_count (n=588) |
|---|---|---|---|---|
| ctx:taberta | 0.301 | 0.241 | 0.315 | 0.255 |
| ig:rule/index:taberta | 0.272 | 0.219 | 0.275 | 0.266 |
| ig:rule/index:taberta+rnorm=minmax | 0.272 | 0.219 | 0.275 | 0.265 |

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
| ctx:taberta | – | 28.8 / 29.7 / 34.3 | – | – | – | – | 28.8 / 29.7 / 34.3 | 44.241 |
| ig:rule/index:taberta | 0.3 / 0.3 / 0.5 | 26.6 / 27.5 / 32.2 | 0.1 / 0.0 / 0.4 | 4.1 / 0.0 / 0.0 | 9.4 / 0.0 / 0.0 | 0.1 / 0.1 / 0.2 | 14.2 / 0.4 / 7.4 | 43.484 |
| ig:rule/index:taberta+rnorm=minmax | 0.4 / 0.3 / 0.5 | 26.7 / 27.9 / 33.0 | 0.1 / 0.0 / 0.3 | 1.4 / 0.0 / 0.0 | 7.3 / 0.0 / 0.0 | 0.1 / 0.1 / 0.2 | 9.4 / 0.4 / 16.8 | 43.45 |

Context index build (one-off, ms): taberta: 20578

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:rule/index:taberta+rnorm=minmax | ctx:taberta | ndcg@10 | -0.011 | [-0.022, -0.000] | 0.049 | 286/366 |
| ig:rule/index:taberta+rnorm=minmax | ctx:taberta | mrr | -0.007 | [-0.020, +0.008] | 0.348 | 320/403 |
| ig:rule/index:taberta+rnorm=minmax | ctx:taberta | useful@1 | +0.003 | [-0.014, +0.020] | 0.825 | 96/92 |
| ig:rule/index:taberta | ctx:taberta | ndcg@10 | -0.011 | [-0.022, -0.000] | 0.050 | 287/366 |
| ig:rule/index:taberta | ctx:taberta | mrr | -0.006 | [-0.020, +0.008] | 0.357 | 321/403 |
| ig:rule/index:taberta | ctx:taberta | useful@1 | +0.003 | [-0.014, +0.020] | 0.825 | 96/92 |
