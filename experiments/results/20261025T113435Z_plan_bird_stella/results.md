# IGBench results (20261025T113435Z_plan_bird_stella)

Benchmark `target-bird-validation` on corpus `target-bird-validation` (75 tables), IL 1.0.0, labels: **established_benchmark_gold**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:sbert | 0.913 | 0.350 | 0.187 | 0.975 | 0.945 | 0.905 | 0.000 |
| ig:rule/index:sbert | 0.912 | 0.350 | 0.186 | 0.974 | 0.943 | 0.902 | 0.000 |
| ig:rule/index:sbert+rnorm=minmax | 0.912 | 0.350 | 0.187 | 0.975 | 0.944 | 0.903 | 0.000 |
| ig:rule/index:sbert+align=0 | 0.912 | 0.350 | 0.187 | 0.975 | 0.943 | 0.901 | 0.000 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:sbert | – | – | – | – |
| ig:rule/index:sbert | – | – | – | – |
| ig:rule/index:sbert+rnorm=minmax | – | – | – | – |
| ig:rule/index:sbert+align=0 | – | – | – | – |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:sbert | 0.537 | 0.925 | 0.975 |
| ig:rule/index:sbert | 0.536 | 0.926 | 0.974 |
| ig:rule/index:sbert+rnorm=minmax | 0.536 | 0.925 | 0.975 |
| ig:rule/index:sbert+align=0 | 0.536 | 0.925 | 0.975 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | extreme (n=235) | lookup (n=655) | mean (n=55) | total_or_count (n=588) |
|---|---|---|---|---|
| ctx:sbert | 0.911 | 0.911 | 0.855 | 0.922 |
| ig:rule/index:sbert | 0.912 | 0.907 | 0.868 | 0.920 |
| ig:rule/index:sbert+rnorm=minmax | 0.912 | 0.908 | 0.868 | 0.921 |
| ig:rule/index:sbert+align=0 | 0.913 | 0.908 | 0.868 | 0.920 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:sbert | – |
| ig:rule/index:sbert | – |
| ig:rule/index:sbert+rnorm=minmax | – |
| ig:rule/index:sbert+align=0 | – |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:sbert | – | 29.6 / 29.8 / 33.4 | – | – | – | – | 29.6 / 29.8 / 33.4 | 45.403 |
| ig:rule/index:sbert | 0.3 / 0.3 / 0.5 | 29.0 / 29.6 / 37.4 | 0.2 / 0.0 / 0.5 | 5.0 / 0.0 / 0.0 | 10.1 / 0.0 / 0.0 | 0.1 / 0.1 / 0.2 | 15.8 / 0.5 / 7.3 | 47.359 |
| ig:rule/index:sbert+rnorm=minmax | 0.4 / 0.3 / 0.5 | 22.2 / 21.1 / 27.6 | 0.2 / 0.0 / 0.5 | 1.7 / 0.0 / 0.0 | 8.7 / 0.0 / 0.0 | 0.1 / 0.1 / 0.3 | 11.2 / 0.5 / 16.8 | 36.415 |
| ig:rule/index:sbert+align=0 | 1.6 / 0.2 / 0.4 | 23.5 / 23.7 / 30.9 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.1 / 0.1 / 0.2 | 1.7 / 0.3 / 0.9 | 37.41 |

Context index build (one-off, ms): sbert: 8719 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:rule/index:sbert+rnorm=minmax | ctx:sbert | ndcg@10 | -0.001 | [-0.004, +0.001] | 0.342 | 105/114 |
| ig:rule/index:sbert+rnorm=minmax | ctx:sbert | mrr | -0.001 | [-0.005, +0.002] | 0.510 | 22/27 |
| ig:rule/index:sbert+rnorm=minmax | ctx:sbert | useful@1 | -0.002 | [-0.009, +0.005] | 0.742 | 15/18 |
| ig:rule/index:sbert | ctx:sbert | ndcg@10 | -0.002 | [-0.004, +0.001] | 0.216 | 105/121 |
| ig:rule/index:sbert | ctx:sbert | mrr | -0.002 | [-0.006, +0.002] | 0.438 | 23/29 |
| ig:rule/index:sbert | ctx:sbert | useful@1 | -0.003 | [-0.010, +0.005] | 0.629 | 16/20 |
| ig:rule/index:sbert+align=0 | ctx:sbert | ndcg@10 | -0.002 | [-0.004, +0.001] | 0.211 | 102/114 |
| ig:rule/index:sbert+align=0 | ctx:sbert | mrr | -0.002 | [-0.006, +0.001] | 0.219 | 19/28 |
| ig:rule/index:sbert+align=0 | ctx:sbert | useful@1 | -0.003 | [-0.010, +0.003] | 0.459 | 12/17 |
