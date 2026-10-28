# IGBench results (20261025T111403Z_plan_bird_minilm)

Benchmark `target-bird-validation` on corpus `target-bird-validation` (75 tables), IL 1.0.0, labels: **established_benchmark_gold**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:sbert | 0.863 | 0.329 | 0.184 | 0.963 | 0.893 | 0.821 | 0.000 |
| ig:rule/index:sbert | 0.862 | 0.330 | 0.183 | 0.960 | 0.894 | 0.825 | 0.000 |
| ig:rule/index:sbert+rnorm=minmax | 0.863 | 0.330 | 0.184 | 0.960 | 0.894 | 0.825 | 0.000 |
| ig:rule/index:sbert+align=0 | 0.862 | 0.330 | 0.184 | 0.960 | 0.893 | 0.824 | 0.000 |
| rerank:ce:sbert | 0.839 | 0.331 | 0.184 | 0.962 | 0.849 | 0.751 | 0.000 |

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
| ctx:sbert | 0.486 | 0.877 | 0.963 |
| ig:rule/index:sbert | 0.487 | 0.878 | 0.960 |
| ig:rule/index:sbert+rnorm=minmax | 0.487 | 0.878 | 0.960 |
| ig:rule/index:sbert+align=0 | 0.487 | 0.878 | 0.960 |
| rerank:ce:sbert | 0.438 | 0.879 | 0.962 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | extreme (n=235) | lookup (n=655) | mean (n=55) | total_or_count (n=588) |
|---|---|---|---|---|
| ctx:sbert | 0.860 | 0.845 | 0.827 | 0.887 |
| ig:rule/index:sbert | 0.852 | 0.847 | 0.841 | 0.886 |
| ig:rule/index:sbert+rnorm=minmax | 0.851 | 0.847 | 0.841 | 0.886 |
| ig:rule/index:sbert+align=0 | 0.851 | 0.847 | 0.841 | 0.885 |
| rerank:ce:sbert | 0.858 | 0.869 | 0.755 | 0.806 |

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
| ctx:sbert | – | 5.2 / 5.0 / 5.2 | – | – | – | – | 5.2 / 5.1 / 5.3 | 8.047 |
| ig:rule/index:sbert | 1.0 / 0.2 / 0.5 | 4.2 / 4.2 / 4.4 | 0.2 / 0.0 / 0.5 | 2.1 / 0.0 / 0.0 | 9.0 / 0.0 / 0.0 | 0.1 / 0.1 / 0.3 | 12.5 / 0.4 / 79.6 | 8.775 |
| ig:rule/index:sbert+rnorm=minmax | 0.5 / 0.3 / 0.5 | 4.3 / 4.3 / 4.4 | 0.2 / 0.0 / 0.5 | 1.7 / 0.0 / 0.0 | 9.3 / 0.0 / 0.0 | 0.1 / 0.1 / 0.3 | 11.9 / 0.5 / 7.5 | 9.3 |
| ig:rule/index:sbert+align=0 | 0.4 / 0.3 / 0.5 | 4.3 / 4.2 / 4.4 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.2 / 0.2 / 0.3 | 0.6 / 0.5 / 0.8 | 7.961 |
| rerank:ce:sbert | – | 2640.5 / 2369.1 / 5258.2 | – | – | – | – | 10383.1 / 10603.8 / 16760.4 | 998.52 |

Context index build (one-off, ms): sbert: 11251 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:rule/index:sbert+rnorm=minmax | ctx:sbert | ndcg@10 | -0.000 | [-0.004, +0.004] | 0.903 | 261/247 |
| ig:rule/index:sbert+rnorm=minmax | ctx:sbert | mrr | +0.001 | [-0.006, +0.007] | 0.811 | 78/84 |
| ig:rule/index:sbert+rnorm=minmax | ctx:sbert | useful@1 | +0.004 | [-0.009, +0.016] | 0.615 | 52/46 |
| ig:rule/index:sbert | ctx:sbert | ndcg@10 | -0.001 | [-0.005, +0.004] | 0.838 | 260/248 |
| ig:rule/index:sbert | ctx:sbert | mrr | +0.001 | [-0.006, +0.007] | 0.836 | 77/84 |
| ig:rule/index:sbert | ctx:sbert | useful@1 | +0.004 | [-0.009, +0.016] | 0.615 | 52/46 |
| ig:rule/index:sbert+align=0 | ctx:sbert | ndcg@10 | -0.001 | [-0.005, +0.004] | 0.743 | 260/249 |
| ig:rule/index:sbert+align=0 | ctx:sbert | mrr | +0.000 | [-0.007, +0.007] | 0.997 | 75/86 |
| ig:rule/index:sbert+align=0 | ctx:sbert | useful@1 | +0.003 | [-0.009, +0.016] | 0.686 | 51/46 |
