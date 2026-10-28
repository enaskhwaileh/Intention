# IGBench results (20261027T074641Z_plan_spider_minilm_q32)

Benchmark `target-spider-test` on corpus `target-spider-test` (180 tables), IL 1.0.0, labels: **established_benchmark_gold**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:sbert | 0.870 | 0.277 | 0.148 | 0.963 | 0.871 | 0.790 | 0.000 |
| ig:llm/llm:sbert | 0.869 | 0.278 | 0.148 | 0.962 | 0.867 | 0.785 | 0.000 |
| ig:llm/llm:sbert+repair=1 | 0.868 | 0.278 | 0.148 | 0.963 | 0.866 | 0.783 | 0.000 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.869 | 0.278 | 0.148 | 0.963 | 0.867 | 0.784 | 0.000 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.869 | 0.278 | 0.148 | 0.964 | 0.866 | 0.782 | 0.000 |
| rerank:llm:sbert | 0.937 | 0.294 | 0.152 | 0.978 | 0.944 | 0.904 | 0.000 |

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
| ig:llm/llm:sbert | 0.600 | 0.923 | 0.962 |
| ig:llm/llm:sbert+repair=1 | 0.598 | 0.923 | 0.963 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.600 | 0.923 | 0.963 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.598 | 0.922 | 0.964 |
| rerank:llm:sbert | 0.693 | 0.959 | 0.978 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | extreme (n=201) | lookup (n=971) | mean (n=162) | total_or_count (n=813) |
|---|---|---|---|---|
| ctx:sbert | 0.931 | 0.872 | 0.916 | 0.844 |
| ig:llm/llm:sbert | 0.926 | 0.868 | 0.910 | 0.847 |
| ig:llm/llm:sbert+repair=1 | 0.925 | 0.869 | 0.911 | 0.846 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.925 | 0.870 | 0.910 | 0.847 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.924 | 0.870 | 0.903 | 0.846 |
| rerank:llm:sbert | 0.977 | 0.937 | 0.967 | 0.920 |

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
| ctx:sbert | – | 4.9 / 4.8 / 5.0 | – | – | – | – | 4.9 / 4.8 / 5.0 | 10.598 |
| ig:llm/llm:sbert | 5.9 / 4.6 / 14.9 | 4.8 / 4.7 / 5.0 | 0.7 / 0.8 / 1.8 | 0.8 / 0.0 / 0.0 | 2.2 / 0.0 / 0.0 | 0.1 / 0.1 / 0.3 | 9.8 / 5.6 / 25.7 | 13.381 |
| ig:llm/llm:sbert+repair=1 | 7.8 / 6.7 / 15.8 | 4.7 / 4.7 / 4.9 | 1.1 / 0.9 / 2.8 | 1.1 / 0.0 / 15.2 | 3.4 / 0.0 / 18.4 | 0.1 / 0.1 / 0.2 | 13.6 / 8.3 / 46.7 | 14.291 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 7.9 / 6.9 / 15.6 | 4.8 / 4.8 / 5.0 | 1.1 / 0.9 / 2.5 | 1.2 / 0.0 / 15.6 | 3.4 / 0.0 / 17.2 | 0.1 / 0.1 / 0.3 | 13.7 / 8.4 / 46.1 | 14.453 |
| ig:llm/llm:sbert+repair=1+align=0 | 11.1 / 7.9 / 30.4 | 4.7 / 4.7 / 4.9 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.2 / 0.2 / 0.4 | 11.3 / 8.1 / 30.6 | 13.679 |
| rerank:llm:sbert | – | 270.3 / 280.0 / 331.8 | – | – | – | – | 21461.0 / 21645.9 / 23331.6 | 2882.24 |

Context index build (one-off, ms): sbert: 10777 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:llm/llm:sbert+repair=1+align=0 | ctx:sbert | ndcg@10 | -0.002 | [-0.006, +0.003] | 0.507 | 241/273 |
| ig:llm/llm:sbert+repair=1+align=0 | ctx:sbert | mrr | -0.005 | [-0.011, +0.002] | 0.135 | 129/158 |
| ig:llm/llm:sbert+repair=1+align=0 | ctx:sbert | useful@1 | -0.008 | [-0.019, +0.002] | 0.159 | 56/73 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | ndcg@10 | -0.001 | [-0.005, +0.004] | 0.760 | 242/269 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | mrr | -0.003 | [-0.009, +0.003] | 0.327 | 133/154 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | useful@1 | -0.006 | [-0.017, +0.004] | 0.302 | 60/73 |
| ig:llm/llm:sbert | ctx:sbert | ndcg@10 | -0.002 | [-0.005, +0.002] | 0.472 | 173/208 |
| ig:llm/llm:sbert | ctx:sbert | mrr | -0.003 | [-0.009, +0.002] | 0.228 | 102/128 |
| ig:llm/llm:sbert | ctx:sbert | useful@1 | -0.006 | [-0.015, +0.004] | 0.286 | 46/58 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | ndcg@10 | -0.002 | [-0.006, +0.003] | 0.483 | 242/278 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | mrr | -0.004 | [-0.011, +0.002] | 0.184 | 133/160 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | useful@1 | -0.007 | [-0.018, +0.003] | 0.201 | 60/76 |
