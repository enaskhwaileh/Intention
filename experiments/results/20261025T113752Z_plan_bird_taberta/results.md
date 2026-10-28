# IGBench results (20261025T113752Z_plan_bird_taberta)

Benchmark `target-bird-validation` on corpus `target-bird-validation` (75 tables), IL 1.0.0, labels: **established_benchmark_gold**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:taberta | 0.840 | 0.330 | 0.181 | 0.947 | 0.866 | 0.772 | 0.000 |
| ig:rule/index:taberta | 0.845 | 0.332 | 0.181 | 0.950 | 0.871 | 0.779 | 0.000 |
| ig:rule/index:taberta+rnorm=minmax | 0.845 | 0.332 | 0.181 | 0.949 | 0.871 | 0.779 | 0.000 |
| ig:rule/index:taberta+align=0 | 0.844 | 0.332 | 0.181 | 0.949 | 0.870 | 0.778 | 0.000 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:taberta | – | – | – | – |
| ig:rule/index:taberta | – | – | – | – |
| ig:rule/index:taberta+rnorm=minmax | – | – | – | – |
| ig:rule/index:taberta+align=0 | – | – | – | – |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:taberta | 0.457 | 0.879 | 0.947 |
| ig:rule/index:taberta | 0.461 | 0.884 | 0.950 |
| ig:rule/index:taberta+rnorm=minmax | 0.461 | 0.885 | 0.949 |
| ig:rule/index:taberta+align=0 | 0.461 | 0.884 | 0.949 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | extreme (n=235) | lookup (n=655) | mean (n=55) | total_or_count (n=588) |
|---|---|---|---|---|
| ctx:taberta | 0.838 | 0.825 | 0.772 | 0.864 |
| ig:rule/index:taberta | 0.849 | 0.826 | 0.777 | 0.871 |
| ig:rule/index:taberta+rnorm=minmax | 0.848 | 0.826 | 0.777 | 0.871 |
| ig:rule/index:taberta+align=0 | 0.848 | 0.825 | 0.777 | 0.870 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:taberta | – |
| ig:rule/index:taberta | – |
| ig:rule/index:taberta+rnorm=minmax | – |
| ig:rule/index:taberta+align=0 | – |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:taberta | – | 10.1 / 8.5 / 14.9 | – | – | – | – | 10.1 / 8.5 / 14.9 | 15.487 |
| ig:rule/index:taberta | 0.3 / 0.3 / 0.5 | 13.2 / 14.7 / 15.4 | 0.2 / 0.0 / 0.6 | 3.3 / 0.0 / 0.0 | 11.0 / 0.0 / 0.0 | 0.1 / 0.1 / 0.3 | 15.0 / 0.5 / 8.3 | 23.333 |
| ig:rule/index:taberta+rnorm=minmax | 1.2 / 0.2 / 0.4 | 9.0 / 8.0 / 13.6 | 0.2 / 0.0 / 0.6 | 2.8 / 0.0 / 0.0 | 14.5 / 0.0 / 0.0 | 0.1 / 0.1 / 0.2 | 18.9 / 0.4 / 103.9 | 17.491 |
| ig:rule/index:taberta+align=0 | 0.7 / 0.1 / 0.2 | 14.1 / 14.9 / 17.3 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.2 / 0.2 / 0.3 | 1.0 / 0.4 / 0.6 | 22.682 |

Context index build (one-off, ms): taberta: 8447 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:rule/index:taberta+align=0 | ctx:taberta | ndcg@10 | +0.004 | [-0.001, +0.009] | 0.097 | 315/270 |
| ig:rule/index:taberta+align=0 | ctx:taberta | mrr | +0.004 | [-0.004, +0.012] | 0.303 | 125/102 |
| ig:rule/index:taberta+align=0 | ctx:taberta | useful@1 | +0.005 | [-0.009, +0.021] | 0.548 | 74/66 |
| ig:rule/index:taberta+rnorm=minmax | ctx:taberta | ndcg@10 | +0.005 | [-0.000, +0.010] | 0.064 | 318/270 |
| ig:rule/index:taberta+rnorm=minmax | ctx:taberta | mrr | +0.005 | [-0.003, +0.013] | 0.254 | 128/103 |
| ig:rule/index:taberta+rnorm=minmax | ctx:taberta | useful@1 | +0.006 | [-0.008, +0.022] | 0.454 | 77/67 |
| ig:rule/index:taberta | ctx:taberta | ndcg@10 | +0.005 | [+0.000, +0.010] | 0.053 | 320/269 |
| ig:rule/index:taberta | ctx:taberta | mrr | +0.005 | [-0.003, +0.013] | 0.247 | 128/103 |
| ig:rule/index:taberta | ctx:taberta | useful@1 | +0.007 | [-0.007, +0.023] | 0.406 | 78/67 |
