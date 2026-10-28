# IGBench results (20261025T142330Z_plan_bird_minilm_q14)

Benchmark `target-bird-validation` on corpus `target-bird-validation` (75 tables), IL 1.0.0, labels: **established_benchmark_gold**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:sbert | 0.863 | 0.329 | 0.184 | 0.963 | 0.893 | 0.821 | 0.000 |
| ig:llm/llm:sbert | 0.858 | 0.328 | 0.184 | 0.960 | 0.890 | 0.817 | 0.000 |
| ig:llm/llm:sbert+repair=1 | 0.856 | 0.326 | 0.183 | 0.958 | 0.889 | 0.815 | 0.000 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.856 | 0.326 | 0.183 | 0.958 | 0.889 | 0.816 | 0.000 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.856 | 0.327 | 0.183 | 0.957 | 0.889 | 0.816 | 0.000 |
| rerank:llm:sbert | 0.927 | 0.352 | 0.187 | 0.975 | 0.958 | 0.928 | 0.000 |

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
| ctx:sbert | 0.486 | 0.877 | 0.963 |
| ig:llm/llm:sbert | 0.484 | 0.874 | 0.960 |
| ig:llm/llm:sbert+repair=1 | 0.483 | 0.871 | 0.958 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.483 | 0.871 | 0.958 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.483 | 0.871 | 0.957 |
| rerank:llm:sbert | 0.551 | 0.931 | 0.975 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | extreme (n=235) | lookup (n=655) | mean (n=55) | total_or_count (n=588) |
|---|---|---|---|---|
| ctx:sbert | 0.860 | 0.845 | 0.827 | 0.887 |
| ig:llm/llm:sbert | 0.855 | 0.841 | 0.823 | 0.882 |
| ig:llm/llm:sbert+repair=1 | 0.846 | 0.841 | 0.824 | 0.878 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.847 | 0.841 | 0.824 | 0.879 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.849 | 0.840 | 0.817 | 0.879 |
| rerank:llm:sbert | 0.930 | 0.922 | 0.894 | 0.934 |

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
| ctx:sbert | – | 10.1 / 7.5 / 15.1 | – | – | – | – | 10.1 / 7.5 / 15.2 | 15.431 |
| ig:llm/llm:sbert | 9.5 / 7.0 / 22.8 | 10.6 / 10.0 / 15.2 | 0.9 / 1.0 / 2.2 | 10.5 / 0.0 / 31.1 | 32.4 / 0.0 / 156.2 | 0.1 / 0.1 / 0.2 | 53.6 / 8.6 / 359.1 | 21.535 |
| ig:llm/llm:sbert+repair=1 | 19.1 / 16.0 / 43.2 | 9.5 / 9.1 / 14.7 | 1.4 / 1.2 / 3.4 | 12.6 / 0.0 / 34.8 | 42.2 / 0.0 / 400.6 | 0.1 / 0.1 / 0.3 | 75.7 / 19.8 / 475.2 | 22.198 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 19.1 / 15.9 / 45.0 | 10.5 / 9.5 / 14.9 | 1.1 / 1.0 / 2.8 | 6.9 / 0.0 / 35.8 | 35.7 / 0.0 / 362.8 | 0.1 / 0.1 / 0.3 | 63.2 / 19.6 / 450.5 | 23.63 |
| ig:llm/llm:sbert+repair=1+align=0 | 8.9 / 7.2 / 20.2 | 11.3 / 11.0 / 15.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.2 / 0.2 / 0.3 | 9.2 / 7.5 / 20.6 | 19.294 |
| rerank:llm:sbert | – | 27.0 / 24.9 / 44.3 | – | – | – | – | 52317.6 / 52277.2 / 63122.8 | 5022.889 |

Context index build (one-off, ms): sbert: 13035 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:llm/llm:sbert+repair=1+align=0 | ctx:sbert | ndcg@10 | -0.007 | [-0.012, -0.003] | 0.002 | 232/276 |
| ig:llm/llm:sbert+repair=1+align=0 | ctx:sbert | mrr | -0.004 | [-0.011, +0.003] | 0.287 | 80/93 |
| ig:llm/llm:sbert+repair=1+align=0 | ctx:sbert | useful@1 | -0.005 | [-0.018, +0.008] | 0.558 | 50/57 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | ndcg@10 | -0.007 | [-0.012, -0.002] | 0.003 | 240/281 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | mrr | -0.004 | [-0.011, +0.003] | 0.309 | 86/96 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | useful@1 | -0.005 | [-0.018, +0.009] | 0.567 | 52/59 |
| ig:llm/llm:sbert | ctx:sbert | ndcg@10 | -0.004 | [-0.009, -0.000] | 0.030 | 185/201 |
| ig:llm/llm:sbert | ctx:sbert | mrr | -0.003 | [-0.010, +0.002] | 0.264 | 59/65 |
| ig:llm/llm:sbert | ctx:sbert | useful@1 | -0.004 | [-0.014, +0.007] | 0.552 | 32/38 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | ndcg@10 | -0.007 | [-0.012, -0.003] | 0.003 | 241/284 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | mrr | -0.004 | [-0.012, +0.003] | 0.268 | 87/99 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | useful@1 | -0.005 | [-0.019, +0.009] | 0.511 | 54/62 |
