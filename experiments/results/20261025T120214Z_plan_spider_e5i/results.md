# IGBench results (20261025T120214Z_plan_spider_e5i)

Benchmark `target-spider-test` on corpus `target-spider-test` (180 tables), IL 1.0.0, labels: **established_benchmark_gold**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:sbert | 0.894 | 0.284 | 0.150 | 0.971 | 0.897 | 0.826 | 0.000 |
| ig:rule/index:sbert | 0.892 | 0.286 | 0.149 | 0.969 | 0.896 | 0.825 | 0.000 |
| ig:rule/index:sbert+rnorm=minmax | 0.895 | 0.287 | 0.150 | 0.971 | 0.899 | 0.830 | 0.000 |
| ig:rule/index:sbert+align=0 | 0.896 | 0.287 | 0.150 | 0.971 | 0.900 | 0.830 | 0.000 |

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
| ctx:sbert | 0.629 | 0.939 | 0.971 |
| ig:rule/index:sbert | 0.629 | 0.942 | 0.969 |
| ig:rule/index:sbert+rnorm=minmax | 0.632 | 0.945 | 0.971 |
| ig:rule/index:sbert+align=0 | 0.632 | 0.945 | 0.971 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | extreme (n=201) | lookup (n=971) | mean (n=162) | total_or_count (n=813) |
|---|---|---|---|---|
| ctx:sbert | 0.950 | 0.894 | 0.911 | 0.876 |
| ig:rule/index:sbert | 0.951 | 0.895 | 0.919 | 0.870 |
| ig:rule/index:sbert+rnorm=minmax | 0.951 | 0.897 | 0.919 | 0.875 |
| ig:rule/index:sbert+align=0 | 0.951 | 0.897 | 0.919 | 0.876 |

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
| ctx:sbert | – | 18.1 / 17.1 / 24.4 | – | – | – | – | 18.1 / 17.1 / 24.4 | 38.967 |
| ig:rule/index:sbert | 0.2 / 0.2 / 0.4 | 16.2 / 15.1 / 20.1 | 0.1 / 0.0 / 0.5 | 0.9 / 0.0 / 0.0 | 1.3 / 0.0 / 0.0 | 0.2 / 0.1 / 0.3 | 2.8 / 0.4 / 2.8 | 36.858 |
| ig:rule/index:sbert+rnorm=minmax | 1.5 / 0.1 / 0.3 | 16.9 / 15.1 / 24.0 | 0.2 / 0.0 / 0.5 | 0.8 / 0.0 / 0.0 | 1.3 / 0.0 / 0.0 | 0.2 / 0.2 / 0.3 | 4.0 / 0.3 / 17.9 | 38.457 |
| ig:rule/index:sbert+align=0 | 0.3 / 0.3 / 0.4 | 16.5 / 15.1 / 21.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.1 / 0.1 / 0.3 | 0.4 / 0.4 / 0.7 | 37.317 |

Context index build (one-off, ms): sbert: 11763 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:rule/index:sbert+rnorm=minmax | ctx:sbert | ndcg@10 | +0.002 | [-0.002, +0.005] | 0.304 | 203/162 |
| ig:rule/index:sbert+rnorm=minmax | ctx:sbert | mrr | +0.002 | [-0.002, +0.007] | 0.288 | 85/76 |
| ig:rule/index:sbert+rnorm=minmax | ctx:sbert | useful@1 | +0.004 | [-0.005, +0.012] | 0.428 | 44/36 |
| ig:rule/index:sbert | ctx:sbert | ndcg@10 | -0.002 | [-0.005, +0.002] | 0.344 | 197/181 |
| ig:rule/index:sbert | ctx:sbert | mrr | -0.001 | [-0.006, +0.004] | 0.725 | 85/86 |
| ig:rule/index:sbert | ctx:sbert | useful@1 | -0.001 | [-0.010, +0.007] | 0.917 | 44/46 |
| ig:rule/index:sbert+align=0 | ctx:sbert | ndcg@10 | +0.002 | [-0.001, +0.005] | 0.227 | 203/156 |
| ig:rule/index:sbert+align=0 | ctx:sbert | mrr | +0.003 | [-0.002, +0.007] | 0.244 | 85/75 |
| ig:rule/index:sbert+align=0 | ctx:sbert | useful@1 | +0.004 | [-0.004, +0.013] | 0.363 | 44/35 |
