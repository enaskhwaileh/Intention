# IGBench results (20261025T113159Z_plan_bird_e5i)

Benchmark `target-bird-validation` on corpus `target-bird-validation` (75 tables), IL 1.0.0, labels: **established_benchmark_gold**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:sbert | 0.889 | 0.345 | 0.186 | 0.974 | 0.913 | 0.853 | 0.000 |
| ig:rule/index:sbert | 0.884 | 0.344 | 0.185 | 0.971 | 0.910 | 0.845 | 0.000 |
| ig:rule/index:sbert+rnorm=minmax | 0.887 | 0.344 | 0.186 | 0.972 | 0.913 | 0.849 | 0.000 |
| ig:rule/index:sbert+align=0 | 0.886 | 0.344 | 0.186 | 0.973 | 0.912 | 0.847 | 0.000 |

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
| ctx:sbert | 0.504 | 0.916 | 0.974 |
| ig:rule/index:sbert | 0.502 | 0.913 | 0.971 |
| ig:rule/index:sbert+rnorm=minmax | 0.505 | 0.915 | 0.972 |
| ig:rule/index:sbert+align=0 | 0.504 | 0.915 | 0.973 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | extreme (n=235) | lookup (n=655) | mean (n=55) | total_or_count (n=588) |
|---|---|---|---|---|
| ctx:sbert | 0.898 | 0.881 | 0.842 | 0.898 |
| ig:rule/index:sbert | 0.886 | 0.877 | 0.837 | 0.896 |
| ig:rule/index:sbert+rnorm=minmax | 0.886 | 0.878 | 0.837 | 0.902 |
| ig:rule/index:sbert+align=0 | 0.886 | 0.878 | 0.842 | 0.899 |

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
| ctx:sbert | – | 18.2 / 18.4 / 22.1 | – | – | – | – | 18.2 / 18.4 / 22.1 | 27.942 |
| ig:rule/index:sbert | 0.2 / 0.2 / 0.4 | 18.5 / 19.6 / 22.4 | 0.2 / 0.0 / 0.4 | 1.8 / 0.0 / 0.0 | 11.5 / 0.0 / 0.0 | 0.1 / 0.1 / 0.2 | 14.0 / 0.4 / 6.7 | 31.07 |
| ig:rule/index:sbert+rnorm=minmax | 0.9 / 0.2 / 0.5 | 18.4 / 19.5 / 22.2 | 0.2 / 0.0 / 0.6 | 9.3 / 0.0 / 0.0 | 17.8 / 0.0 / 0.0 | 0.2 / 0.2 / 0.3 | 28.5 / 0.4 / 72.0 | 32.388 |
| ig:rule/index:sbert+align=0 | 0.4 / 0.2 / 0.4 | 19.4 / 20.2 / 26.3 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.2 / 0.2 / 0.4 | 0.7 / 0.4 / 0.7 | 31.655 |

Context index build (one-off, ms): sbert: 11834 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:rule/index:sbert+rnorm=minmax | ctx:sbert | ndcg@10 | -0.002 | [-0.006, +0.002] | 0.330 | 180/225 |
| ig:rule/index:sbert+rnorm=minmax | ctx:sbert | mrr | -0.001 | [-0.007, +0.006] | 0.808 | 64/58 |
| ig:rule/index:sbert+rnorm=minmax | ctx:sbert | useful@1 | -0.005 | [-0.017, +0.008] | 0.514 | 40/47 |
| ig:rule/index:sbert | ctx:sbert | ndcg@10 | -0.005 | [-0.009, -0.001] | 0.035 | 179/240 |
| ig:rule/index:sbert | ctx:sbert | mrr | -0.004 | [-0.011, +0.003] | 0.292 | 63/66 |
| ig:rule/index:sbert | ctx:sbert | useful@1 | -0.009 | [-0.021, +0.004] | 0.211 | 40/53 |
| ig:rule/index:sbert+align=0 | ctx:sbert | ndcg@10 | -0.003 | [-0.006, +0.001] | 0.197 | 175/223 |
| ig:rule/index:sbert+align=0 | ctx:sbert | mrr | -0.002 | [-0.008, +0.005] | 0.581 | 59/55 |
| ig:rule/index:sbert+align=0 | ctx:sbert | useful@1 | -0.006 | [-0.017, +0.006] | 0.365 | 35/44 |
