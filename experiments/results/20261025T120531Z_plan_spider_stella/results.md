# IGBench results (20261025T120531Z_plan_spider_stella)

Benchmark `target-spider-test` on corpus `target-spider-test` (180 tables), IL 1.0.0, labels: **established_benchmark_gold**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:sbert | 0.916 | 0.290 | 0.151 | 0.976 | 0.922 | 0.867 | 0.000 |
| ig:rule/index:sbert | 0.914 | 0.289 | 0.151 | 0.977 | 0.920 | 0.864 | 0.000 |
| ig:rule/index:sbert+rnorm=minmax | 0.914 | 0.290 | 0.151 | 0.977 | 0.920 | 0.864 | 0.000 |
| ig:rule/index:sbert+align=0 | 0.914 | 0.290 | 0.151 | 0.977 | 0.920 | 0.864 | 0.000 |

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
| ctx:sbert | 0.659 | 0.953 | 0.976 |
| ig:rule/index:sbert | 0.654 | 0.949 | 0.977 |
| ig:rule/index:sbert+rnorm=minmax | 0.654 | 0.951 | 0.977 |
| ig:rule/index:sbert+align=0 | 0.654 | 0.951 | 0.977 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | extreme (n=201) | lookup (n=971) | mean (n=162) | total_or_count (n=813) |
|---|---|---|---|---|
| ctx:sbert | 0.961 | 0.915 | 0.957 | 0.898 |
| ig:rule/index:sbert | 0.962 | 0.915 | 0.957 | 0.892 |
| ig:rule/index:sbert+rnorm=minmax | 0.962 | 0.915 | 0.957 | 0.893 |
| ig:rule/index:sbert+align=0 | 0.962 | 0.915 | 0.957 | 0.893 |

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
| ctx:sbert | – | 25.8 / 27.1 / 29.1 | – | – | – | – | 25.8 / 27.1 / 29.1 | 55.425 |
| ig:rule/index:sbert | 0.3 / 0.3 / 0.4 | 27.6 / 27.3 / 32.5 | 0.1 / 0.0 / 0.5 | 0.9 / 0.0 / 0.0 | 1.6 / 0.0 / 0.0 | 0.2 / 0.1 / 0.3 | 3.2 / 0.5 / 2.7 | 61.398 |
| ig:rule/index:sbert+rnorm=minmax | 0.7 / 0.1 / 0.3 | 25.4 / 26.7 / 27.8 | 0.1 / 0.0 / 0.5 | 0.8 / 0.0 / 0.0 | 1.4 / 0.0 / 0.0 | 0.2 / 0.2 / 0.3 | 3.3 / 0.4 / 6.2 | 56.039 |
| ig:rule/index:sbert+align=0 | 0.4 / 0.3 / 0.4 | 23.8 / 23.9 / 29.2 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.2 / 0.2 / 0.3 | 0.6 / 0.4 / 0.7 | 52.767 |

Context index build (one-off, ms): sbert: 8638 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:rule/index:sbert+rnorm=minmax | ctx:sbert | ndcg@10 | -0.002 | [-0.004, +0.001] | 0.116 | 100/117 |
| ig:rule/index:sbert+rnorm=minmax | ctx:sbert | mrr | -0.002 | [-0.006, +0.002] | 0.303 | 39/56 |
| ig:rule/index:sbert+rnorm=minmax | ctx:sbert | useful@1 | -0.003 | [-0.010, +0.003] | 0.402 | 22/29 |
| ig:rule/index:sbert | ctx:sbert | ndcg@10 | -0.002 | [-0.005, +0.000] | 0.072 | 99/127 |
| ig:rule/index:sbert | ctx:sbert | mrr | -0.002 | [-0.006, +0.002] | 0.316 | 40/57 |
| ig:rule/index:sbert | ctx:sbert | useful@1 | -0.003 | [-0.010, +0.003] | 0.402 | 22/29 |
| ig:rule/index:sbert+align=0 | ctx:sbert | ndcg@10 | -0.002 | [-0.005, +0.001] | 0.104 | 97/115 |
| ig:rule/index:sbert+align=0 | ctx:sbert | mrr | -0.002 | [-0.006, +0.002] | 0.301 | 39/56 |
| ig:rule/index:sbert+align=0 | ctx:sbert | useful@1 | -0.003 | [-0.010, +0.003] | 0.403 | 22/29 |
