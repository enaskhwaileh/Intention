# IGBench results (20261027T031930Z_plan_bird_minilm_q32)

Benchmark `target-bird-validation` on corpus `target-bird-validation` (75 tables), IL 1.0.0, labels: **established_benchmark_gold**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:sbert | 0.863 | 0.329 | 0.184 | 0.963 | 0.893 | 0.821 | 0.000 |
| ig:llm/llm:sbert | 0.860 | 0.329 | 0.184 | 0.962 | 0.890 | 0.818 | 0.000 |
| ig:llm/llm:sbert+repair=1 | 0.861 | 0.330 | 0.184 | 0.962 | 0.892 | 0.820 | 0.000 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.861 | 0.329 | 0.184 | 0.962 | 0.892 | 0.821 | 0.000 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.860 | 0.329 | 0.184 | 0.962 | 0.892 | 0.821 | 0.000 |
| rerank:llm:sbert | 0.938 | 0.360 | 0.187 | 0.977 | 0.964 | 0.936 | 0.000 |

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
| ig:llm/llm:sbert | 0.484 | 0.877 | 0.962 |
| ig:llm/llm:sbert+repair=1 | 0.484 | 0.878 | 0.962 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.485 | 0.878 | 0.962 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.485 | 0.877 | 0.962 |
| rerank:llm:sbert | 0.559 | 0.948 | 0.977 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | extreme (n=235) | lookup (n=655) | mean (n=55) | total_or_count (n=588) |
|---|---|---|---|---|
| ctx:sbert | 0.860 | 0.845 | 0.827 | 0.887 |
| ig:llm/llm:sbert | 0.858 | 0.843 | 0.817 | 0.884 |
| ig:llm/llm:sbert+repair=1 | 0.855 | 0.845 | 0.814 | 0.885 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.857 | 0.845 | 0.814 | 0.885 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.856 | 0.845 | 0.809 | 0.884 |
| rerank:llm:sbert | 0.933 | 0.936 | 0.900 | 0.946 |

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
| ctx:sbert | – | 4.7 / 4.6 / 4.7 | – | – | – | – | 4.7 / 4.6 / 4.8 | 7.274 |
| ig:llm/llm:sbert | 14.6 / 13.0 / 29.4 | 4.5 / 4.5 / 4.7 | 0.6 / 0.0 / 1.9 | 2.6 / 0.0 / 0.0 | 12.1 / 0.0 / 0.0 | 0.1 / 0.1 / 0.3 | 30.1 / 14.2 / 39.0 | 10.329 |
| ig:llm/llm:sbert+repair=1 | 19.3 / 16.9 / 41.5 | 4.7 / 4.5 / 4.7 | 1.1 / 1.0 / 2.5 | 2.9 / 0.0 / 32.1 | 26.7 / 0.0 / 242.5 | 0.1 / 0.1 / 0.2 | 50.4 / 19.7 / 298.6 | 12.09 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 11.6 / 8.7 / 30.6 | 4.4 / 4.4 / 4.6 | 1.2 / 1.1 / 3.0 | 8.5 / 0.0 / 36.2 | 29.1 / 0.0 / 274.5 | 0.1 / 0.1 / 0.3 | 50.7 / 10.9 / 389.4 | 12.648 |
| ig:llm/llm:sbert+repair=1+align=0 | 19.9 / 17.3 / 44.5 | 4.7 / 4.5 / 4.7 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.2 / 0.2 / 0.3 | 20.1 / 17.6 / 44.8 | 9.951 |
| rerank:llm:sbert | – | 26.2 / 21.9 / 37.0 | – | – | – | – | 63469.8 / 63781.3 / 74955.4 | 6096.411 |

Context index build (one-off, ms): sbert: 10494 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:llm/llm:sbert+repair=1+align=0 | ctx:sbert | ndcg@10 | -0.002 | [-0.007, +0.002] | 0.325 | 267/267 |
| ig:llm/llm:sbert+repair=1+align=0 | ctx:sbert | mrr | -0.001 | [-0.009, +0.006] | 0.810 | 91/91 |
| ig:llm/llm:sbert+repair=1+align=0 | ctx:sbert | useful@1 | +0.000 | [-0.014, +0.013] | 1.000 | 58/58 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | ndcg@10 | -0.002 | [-0.007, +0.003] | 0.430 | 276/269 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | mrr | -0.001 | [-0.009, +0.006] | 0.795 | 93/95 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | useful@1 | +0.000 | [-0.014, +0.014] | 1.000 | 59/59 |
| ig:llm/llm:sbert | ctx:sbert | ndcg@10 | -0.003 | [-0.007, +0.001] | 0.160 | 173/179 |
| ig:llm/llm:sbert | ctx:sbert | mrr | -0.003 | [-0.009, +0.004] | 0.413 | 59/68 |
| ig:llm/llm:sbert | ctx:sbert | useful@1 | -0.003 | [-0.014, +0.009] | 0.733 | 37/41 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | ndcg@10 | -0.002 | [-0.007, +0.003] | 0.394 | 277/269 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | mrr | -0.001 | [-0.009, +0.006] | 0.730 | 93/96 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | useful@1 | -0.001 | [-0.015, +0.012] | 1.000 | 59/60 |
