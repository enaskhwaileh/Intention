# IGBench results (20261025T093706Z_srv_target_bird-validation_taberta_pc)

Benchmark `target-bird-validation` on corpus `target-bird-validation` (75 tables), IL 1.0.0, labels: **established_benchmark_gold**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:taberta | 0.840 | 0.330 | 0.181 | 0.947 | 0.866 | 0.772 | 0.000 |
| ig:rule/index:taberta | 0.845 | 0.332 | 0.181 | 0.950 | 0.871 | 0.779 | 0.000 |
| ig:rule/index:taberta+rnorm=minmax | 0.845 | 0.332 | 0.181 | 0.949 | 0.871 | 0.779 | 0.000 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:taberta | – | – | – | – |
| ig:rule/index:taberta | – | – | – | – |
| ig:rule/index:taberta+rnorm=minmax | – | – | – | – |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:taberta | 0.457 | 0.879 | 0.947 |
| ig:rule/index:taberta | 0.461 | 0.884 | 0.950 |
| ig:rule/index:taberta+rnorm=minmax | 0.461 | 0.885 | 0.949 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | extreme (n=235) | lookup (n=655) | mean (n=55) | total_or_count (n=588) |
|---|---|---|---|---|
| ctx:taberta | 0.838 | 0.825 | 0.772 | 0.864 |
| ig:rule/index:taberta | 0.849 | 0.826 | 0.777 | 0.871 |
| ig:rule/index:taberta+rnorm=minmax | 0.848 | 0.826 | 0.777 | 0.871 |

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
| ctx:taberta | – | 27.6 / 28.9 / 32.1 | – | – | – | – | 27.6 / 28.9 / 32.1 | 42.305 |
| ig:rule/index:taberta | 0.5 / 0.3 / 0.5 | 25.6 / 23.3 / 31.2 | 0.1 / 0.0 / 0.3 | 2.5 / 0.0 / 0.0 | 9.7 / 0.0 / 0.0 | 0.1 / 0.1 / 0.2 | 13.0 / 0.4 / 29.0 | 42.095 |
| ig:rule/index:taberta+rnorm=minmax | 0.4 / 0.3 / 0.5 | 24.9 / 22.6 / 30.3 | 0.1 / 0.0 / 0.3 | 1.3 / 0.0 / 0.0 | 7.0 / 0.0 / 0.0 | 0.1 / 0.1 / 0.2 | 9.0 / 0.4 / 11.5 | 41.064 |

Context index build (one-off, ms): taberta: 19147

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:rule/index:taberta+rnorm=minmax | ctx:taberta | ndcg@10 | +0.005 | [-0.000, +0.010] | 0.064 | 318/270 |
| ig:rule/index:taberta+rnorm=minmax | ctx:taberta | mrr | +0.005 | [-0.003, +0.013] | 0.254 | 128/103 |
| ig:rule/index:taberta+rnorm=minmax | ctx:taberta | useful@1 | +0.006 | [-0.008, +0.022] | 0.454 | 77/67 |
| ig:rule/index:taberta | ctx:taberta | ndcg@10 | +0.005 | [+0.000, +0.010] | 0.053 | 320/269 |
| ig:rule/index:taberta | ctx:taberta | mrr | +0.005 | [-0.003, +0.013] | 0.247 | 128/103 |
| ig:rule/index:taberta | ctx:taberta | useful@1 | +0.007 | [-0.007, +0.023] | 0.406 | 78/67 |
