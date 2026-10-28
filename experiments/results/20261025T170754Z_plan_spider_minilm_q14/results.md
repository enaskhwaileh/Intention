# IGBench results (20261025T170754Z_plan_spider_minilm_q14)

Benchmark `target-spider-test` on corpus `target-spider-test` (180 tables), IL 1.0.0, labels: **established_benchmark_gold**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:sbert | 0.870 | 0.277 | 0.148 | 0.963 | 0.871 | 0.790 | 0.000 |
| ig:llm/llm:sbert | 0.869 | 0.277 | 0.148 | 0.962 | 0.868 | 0.788 | 0.000 |
| ig:llm/llm:sbert+repair=1 | 0.868 | 0.277 | 0.148 | 0.964 | 0.866 | 0.785 | 0.000 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.868 | 0.277 | 0.148 | 0.964 | 0.867 | 0.786 | 0.000 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.868 | 0.277 | 0.148 | 0.964 | 0.867 | 0.785 | 0.000 |
| rerank:llm:sbert | 0.925 | 0.289 | 0.150 | 0.971 | 0.935 | 0.894 | 0.000 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:sbert | – | – | – | – |
| ig:llm/llm:sbert | – | – | – | – |
| ig:llm/llm:sbert+repair=1 | – | – | – | – |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | – | – | – | – |
| ig:llm/llm:sbert+repair=1+align=0 | – | – | – | – |
| rerank:llm:sbert | – | – | – | – |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:sbert | 0.603 | 0.922 | 0.963 |
| ig:llm/llm:sbert | 0.601 | 0.921 | 0.962 |
| ig:llm/llm:sbert+repair=1 | 0.599 | 0.921 | 0.964 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.600 | 0.921 | 0.964 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.600 | 0.921 | 0.964 |
| rerank:llm:sbert | 0.684 | 0.948 | 0.971 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | extreme (n=201) | lookup (n=971) | mean (n=162) | total_or_count (n=813) |
|---|---|---|---|---|
| ctx:sbert | 0.931 | 0.872 | 0.916 | 0.844 |
| ig:llm/llm:sbert | 0.929 | 0.872 | 0.918 | 0.841 |
| ig:llm/llm:sbert+repair=1 | 0.925 | 0.869 | 0.918 | 0.842 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.925 | 0.869 | 0.918 | 0.844 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.923 | 0.869 | 0.910 | 0.846 |
| rerank:llm:sbert | 0.974 | 0.924 | 0.957 | 0.908 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:sbert | – |
| ig:llm/llm:sbert | – |
| ig:llm/llm:sbert+repair=1 | – |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | – |
| ig:llm/llm:sbert+repair=1+align=0 | – |
| rerank:llm:sbert | – |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:sbert | – | 10.0 / 9.5 / 16.3 | – | – | – | – | 10.0 / 9.6 / 16.3 | 21.513 |
| ig:llm/llm:sbert | 4.9 / 4.6 / 9.5 | 8.8 / 6.6 / 15.4 | 0.8 / 0.9 / 1.9 | 2.1 / 0.0 / 19.1 | 6.9 / 0.0 / 38.9 | 0.1 / 0.1 / 0.3 | 15.0 / 5.9 / 67.9 | 21.856 |
| ig:llm/llm:sbert+repair=1 | 12.7 / 10.6 / 29.6 | 9.1 / 9.1 / 16.3 | 1.1 / 0.9 / 2.7 | 2.1 / 0.0 / 19.3 | 6.4 / 0.0 / 47.6 | 0.1 / 0.1 / 0.3 | 22.5 / 13.1 / 85.3 | 23.884 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 14.1 / 12.5 / 30.1 | 14.2 / 14.6 / 24.5 | 1.2 / 0.9 / 2.9 | 2.1 / 0.0 / 19.8 | 6.6 / 0.0 / 51.0 | 0.1 / 0.1 / 0.3 | 24.2 / 15.0 / 89.8 | 34.438 |
| ig:llm/llm:sbert+repair=1+align=0 | 15.3 / 13.8 / 31.3 | 14.5 / 14.6 / 24.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.1 / 0.1 / 0.2 | 15.5 / 14.0 / 31.4 | 33.975 |
| rerank:llm:sbert | – | 22.8 / 20.1 / 37.9 | – | – | – | – | 16713.3 / 16381.7 / 20319.2 | 2245.872 |

Context index build (one-off, ms): sbert: 8985 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:llm/llm:sbert+repair=1+align=0 | ctx:sbert | ndcg@10 | -0.002 | [-0.006, +0.003] | 0.456 | 222/255 |
| ig:llm/llm:sbert+repair=1+align=0 | ctx:sbert | mrr | -0.004 | [-0.010, +0.002] | 0.203 | 124/149 |
| ig:llm/llm:sbert+repair=1+align=0 | ctx:sbert | useful@1 | -0.006 | [-0.016, +0.004] | 0.323 | 55/67 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | ndcg@10 | -0.002 | [-0.006, +0.003] | 0.484 | 234/259 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | mrr | -0.004 | [-0.010, +0.003] | 0.262 | 127/155 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | useful@1 | -0.005 | [-0.015, +0.005] | 0.437 | 63/73 |
| ig:llm/llm:sbert | ctx:sbert | ndcg@10 | -0.001 | [-0.006, +0.003] | 0.582 | 191/210 |
| ig:llm/llm:sbert | ctx:sbert | mrr | -0.002 | [-0.008, +0.003] | 0.433 | 107/126 |
| ig:llm/llm:sbert | ctx:sbert | useful@1 | -0.003 | [-0.012, +0.007] | 0.639 | 53/59 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | ndcg@10 | -0.002 | [-0.007, +0.002] | 0.356 | 232/261 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | mrr | -0.004 | [-0.011, +0.002] | 0.196 | 125/157 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | useful@1 | -0.006 | [-0.016, +0.005] | 0.347 | 63/75 |
