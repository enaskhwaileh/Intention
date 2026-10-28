# IGBench results (20261025T091633Z_srv_target_bird-validation_taberta)

Benchmark `target-bird-validation` on corpus `target-bird-validation` (75 tables), IL 1.0.0, labels: **established_benchmark_gold**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:taberta | 0.060 | 0.020 | 0.022 | 0.113 | 0.085 | 0.020 | 0.000 |
| ig:rule/index:taberta | 0.074 | 0.026 | 0.025 | 0.128 | 0.104 | 0.035 | 0.000 |
| ig:rule/index:taberta+rnorm=minmax | 0.069 | 0.024 | 0.024 | 0.122 | 0.097 | 0.029 | 0.000 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:taberta | – | – | – | – |
| ig:rule/index:taberta | – | – | – | – |
| ig:rule/index:taberta+rnorm=minmax | – | – | – | – |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:taberta | 0.010 | 0.049 | 0.113 |
| ig:rule/index:taberta | 0.017 | 0.065 | 0.128 |
| ig:rule/index:taberta+rnorm=minmax | 0.014 | 0.058 | 0.122 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | extreme (n=235) | lookup (n=655) | mean (n=55) | total_or_count (n=588) |
|---|---|---|---|---|
| ctx:taberta | 0.043 | 0.068 | 0.033 | 0.061 |
| ig:rule/index:taberta | 0.054 | 0.071 | 0.047 | 0.089 |
| ig:rule/index:taberta+rnorm=minmax | 0.051 | 0.067 | 0.036 | 0.080 |

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
| ctx:taberta | – | 9.2 / 7.5 / 17.3 | – | – | – | – | 9.2 / 7.5 / 17.3 | 14.184 |
| ig:rule/index:taberta | 0.3 / 0.3 / 0.5 | 7.3 / 7.3 / 7.6 | 0.1 / 0.0 / 0.4 | 4.1 / 0.0 / 0.0 | 7.7 / 0.0 / 0.0 | 0.1 / 0.1 / 0.2 | 12.4 / 0.4 / 7.4 | 14.182 |
| ig:rule/index:taberta+rnorm=minmax | 0.5 / 0.3 / 0.5 | 7.6 / 7.6 / 7.7 | 0.1 / 0.0 / 0.3 | 1.2 / 0.0 / 0.0 | 6.6 / 0.0 / 0.0 | 0.1 / 0.1 / 0.2 | 8.5 / 0.4 / 7.7 | 14.166 |

Context index build (one-off, ms): taberta: 9694

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:rule/index:taberta+rnorm=minmax | ctx:taberta | ndcg@10 | +0.008 | [+0.003, +0.015] | 0.007 | 189/142 |
| ig:rule/index:taberta+rnorm=minmax | ctx:taberta | mrr | +0.011 | [+0.004, +0.020] | 0.004 | 586/500 |
| ig:rule/index:taberta+rnorm=minmax | ctx:taberta | useful@1 | +0.009 | [+0.000, +0.019] | 0.067 | 33/19 |
| ig:rule/index:taberta | ctx:taberta | ndcg@10 | +0.014 | [+0.007, +0.021] | 0.000 | 201/142 |
| ig:rule/index:taberta | ctx:taberta | mrr | +0.018 | [+0.010, +0.027] | 0.000 | 589/499 |
| ig:rule/index:taberta | ctx:taberta | useful@1 | +0.015 | [+0.005, +0.025] | 0.003 | 42/19 |
