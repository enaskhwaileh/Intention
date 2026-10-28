# IGBench results (20261025T115107Z_plan_spider_minilm)

Benchmark `target-spider-test` on corpus `target-spider-test` (180 tables), IL 1.0.0, labels: **established_benchmark_gold**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:sbert | 0.870 | 0.277 | 0.148 | 0.963 | 0.871 | 0.790 | 0.000 |
| ig:rule/index:sbert | 0.875 | 0.278 | 0.149 | 0.968 | 0.874 | 0.797 | 0.000 |
| ig:rule/index:sbert+rnorm=minmax | 0.875 | 0.279 | 0.149 | 0.968 | 0.874 | 0.797 | 0.000 |
| ig:rule/index:sbert+align=0 | 0.875 | 0.278 | 0.149 | 0.968 | 0.874 | 0.797 | 0.000 |
| rerank:ce:sbert | 0.859 | 0.268 | 0.146 | 0.955 | 0.869 | 0.795 | 0.000 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:sbert | – | – | – | – |
| ig:rule/index:sbert | – | – | – | – |
| ig:rule/index:sbert+rnorm=minmax | – | – | – | – |
| ig:rule/index:sbert+align=0 | – | – | – | – |
| rerank:ce:sbert | – | – | – | – |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:sbert | 0.603 | 0.922 | 0.963 |
| ig:rule/index:sbert | 0.607 | 0.925 | 0.968 |
| ig:rule/index:sbert+rnorm=minmax | 0.607 | 0.925 | 0.968 |
| ig:rule/index:sbert+align=0 | 0.607 | 0.925 | 0.968 |
| rerank:ce:sbert | 0.598 | 0.892 | 0.955 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | extreme (n=201) | lookup (n=971) | mean (n=162) | total_or_count (n=813) |
|---|---|---|---|---|
| ctx:sbert | 0.931 | 0.872 | 0.916 | 0.844 |
| ig:rule/index:sbert | 0.931 | 0.876 | 0.923 | 0.851 |
| ig:rule/index:sbert+rnorm=minmax | 0.931 | 0.876 | 0.923 | 0.851 |
| ig:rule/index:sbert+align=0 | 0.931 | 0.876 | 0.923 | 0.850 |
| rerank:ce:sbert | 0.930 | 0.893 | 0.926 | 0.787 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:sbert | – |
| ig:rule/index:sbert | – |
| ig:rule/index:sbert+rnorm=minmax | – |
| ig:rule/index:sbert+align=0 | – |
| rerank:ce:sbert | – |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:sbert | – | 9.2 / 9.1 / 13.6 | – | – | – | – | 9.2 / 9.1 / 13.6 | 19.703 |
| ig:rule/index:sbert | 0.2 / 0.1 / 0.3 | 7.3 / 7.9 / 11.5 | 0.1 / 0.0 / 0.5 | 0.8 / 0.0 / 0.0 | 1.4 / 0.0 / 0.0 | 0.2 / 0.1 / 0.3 | 2.7 / 0.3 / 2.7 | 17.542 |
| ig:rule/index:sbert+rnorm=minmax | 0.4 / 0.3 / 0.4 | 7.5 / 6.0 / 13.4 | 0.1 / 0.0 / 0.4 | 0.8 / 0.0 / 0.0 | 1.5 / 0.0 / 0.0 | 0.1 / 0.1 / 0.3 | 3.0 / 0.4 / 4.5 | 18.27 |
| ig:rule/index:sbert+align=0 | 0.2 / 0.2 / 0.4 | 9.8 / 9.5 / 14.2 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.2 / 0.2 / 0.4 | 0.5 / 0.4 / 0.7 | 22.344 |
| rerank:ce:sbert | – | 936.4 / 903.0 / 1561.7 | – | – | – | – | 3990.4 / 3981.2 / 5363.1 | 536.345 |

Context index build (one-off, ms): sbert: 10513 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:rule/index:sbert+rnorm=minmax | ctx:sbert | ndcg@10 | +0.005 | [+0.001, +0.009] | 0.016 | 265/204 |
| ig:rule/index:sbert+rnorm=minmax | ctx:sbert | mrr | +0.003 | [-0.002, +0.009] | 0.215 | 131/115 |
| ig:rule/index:sbert+rnorm=minmax | ctx:sbert | useful@1 | +0.007 | [-0.002, +0.016] | 0.182 | 63/48 |
| ig:rule/index:sbert | ctx:sbert | ndcg@10 | +0.005 | [+0.001, +0.009] | 0.016 | 265/204 |
| ig:rule/index:sbert | ctx:sbert | mrr | +0.003 | [-0.002, +0.008] | 0.254 | 130/115 |
| ig:rule/index:sbert | ctx:sbert | useful@1 | +0.006 | [-0.003, +0.016] | 0.212 | 62/48 |
| ig:rule/index:sbert+align=0 | ctx:sbert | ndcg@10 | +0.005 | [+0.001, +0.008] | 0.018 | 265/205 |
| ig:rule/index:sbert+align=0 | ctx:sbert | mrr | +0.003 | [-0.002, +0.008] | 0.252 | 130/114 |
| ig:rule/index:sbert+align=0 | ctx:sbert | useful@1 | +0.006 | [-0.003, +0.016] | 0.207 | 61/47 |
