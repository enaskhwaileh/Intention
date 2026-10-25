# IGBench results (20261024T233214Z_srv_target_spider-test)

Benchmark `target-spider-test` on corpus `target-spider-test` (180 tables), IL 1.0.0, labels: **established_benchmark_gold**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:bm25 | 0.860 | 0.275 | 0.142 | 0.973 | 0.840 | 0.733 | 0.000 |
| ctx:sbert | 0.890 | 0.277 | 0.145 | 0.988 | 0.876 | 0.793 | 0.000 |
| ig:rule/index:bm25 | 0.908 | 0.279 | 0.142 | 0.972 | 0.906 | 0.843 | 0.000 |
| ig:rule/index:sbert | 0.888 | 0.277 | 0.145 | 0.989 | 0.870 | 0.786 | 0.000 |
| ig:rule/index:bm25+rnorm=minmax | 0.908 | 0.279 | 0.142 | 0.972 | 0.906 | 0.843 | 0.000 |
| ig:rule/index:sbert+rnorm=minmax | 0.888 | 0.277 | 0.145 | 0.989 | 0.870 | 0.786 | 0.000 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:bm25 | – | – | – | – |
| ctx:sbert | – | – | – | – |
| ig:rule/index:bm25 | – | – | – | – |
| ig:rule/index:sbert | – | – | – | – |
| ig:rule/index:bm25+rnorm=minmax | – | – | – | – |
| ig:rule/index:sbert+rnorm=minmax | – | – | – | – |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:bm25 | 0.578 | 0.950 | 0.973 |
| ctx:sbert | 0.634 | 0.957 | 0.988 |
| ig:rule/index:bm25 | 0.673 | 0.957 | 0.972 |
| ig:rule/index:sbert | 0.626 | 0.956 | 0.989 |
| ig:rule/index:bm25+rnorm=minmax | 0.673 | 0.957 | 0.972 |
| ig:rule/index:sbert+rnorm=minmax | 0.626 | 0.956 | 0.989 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | extreme (n=89) | lookup (n=356) | mean (n=72) | total_or_count (n=258) |
|---|---|---|---|---|
| ctx:bm25 | 0.860 | 0.849 | 0.928 | 0.856 |
| ctx:sbert | 0.911 | 0.901 | 0.927 | 0.858 |
| ig:rule/index:bm25 | 0.906 | 0.903 | 0.950 | 0.903 |
| ig:rule/index:sbert | 0.905 | 0.892 | 0.941 | 0.861 |
| ig:rule/index:bm25+rnorm=minmax | 0.906 | 0.903 | 0.950 | 0.903 |
| ig:rule/index:sbert+rnorm=minmax | 0.905 | 0.892 | 0.941 | 0.861 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:bm25 | – |
| ctx:sbert | – |
| ig:rule/index:bm25 | – |
| ig:rule/index:sbert | – |
| ig:rule/index:bm25+rnorm=minmax | – |
| ig:rule/index:sbert+rnorm=minmax | – |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:bm25 | – | 0.2 / 0.1 / 0.3 | – | – | – | – | 0.2 / 0.1 / 0.3 | 0.144 |
| ctx:sbert | – | 8.8 / 8.2 / 12.3 | – | – | – | – | 8.8 / 8.3 / 12.3 | 6.863 |
| ig:rule/index:bm25 | 0.4 / 0.1 / 0.3 | 0.3 / 0.2 / 0.4 | 0.2 / 0.0 / 1.4 | 12.3 / 0.0 / 0.0 | 2.0 / 0.0 / 0.0 | 0.2 / 0.2 / 0.4 | 15.1 / 0.3 / 5.5 | 2.788 |
| ig:rule/index:sbert | 0.2 / 0.2 / 0.2 | 8.9 / 7.9 / 14.2 | 0.2 / 0.0 / 1.4 | 3.3 / 0.0 / 0.0 | 1.9 / 0.0 / 0.0 | 0.2 / 0.2 / 0.3 | 5.9 / 0.4 / 4.6 | 8.786 |
| ig:rule/index:bm25+rnorm=minmax | 0.8 / 0.1 / 0.3 | 0.1 / 0.1 / 0.3 | 0.2 / 0.0 / 1.3 | 0.6 / 0.0 / 0.0 | 1.9 / 0.0 / 0.0 | 0.2 / 0.1 / 0.4 | 3.7 / 0.3 / 9.2 | 1.529 |
| ig:rule/index:sbert+rnorm=minmax | 0.2 / 0.1 / 0.2 | 8.1 / 8.0 / 10.6 | 0.2 / 0.0 / 1.2 | 2.2 / 0.0 / 0.0 | 2.1 / 0.0 / 0.0 | 0.2 / 0.2 / 0.4 | 5.0 / 0.4 / 4.8 | 8.796 |

Context index build (one-off, ms): bm25: 10, sbert: 11891

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:rule/index:sbert+rnorm=minmax | ctx:sbert | ndcg@10 | -0.003 | [-0.009, +0.003] | 0.425 | 82/76 |
| ig:rule/index:sbert+rnorm=minmax | ctx:sbert | mrr | -0.006 | [-0.015, +0.002] | 0.163 | 38/52 |
| ig:rule/index:sbert+rnorm=minmax | ctx:sbert | useful@1 | -0.008 | [-0.025, +0.008] | 0.445 | 19/25 |
| ig:rule/index:sbert | ctx:sbert | ndcg@10 | -0.003 | [-0.009, +0.003] | 0.416 | 82/76 |
| ig:rule/index:sbert | ctx:sbert | mrr | -0.006 | [-0.015, +0.002] | 0.163 | 38/52 |
| ig:rule/index:sbert | ctx:sbert | useful@1 | -0.008 | [-0.025, +0.008] | 0.445 | 19/25 |
| ig:rule/index:bm25+rnorm=minmax | ctx:bm25 | ndcg@10 | +0.048 | [+0.039, +0.056] | 0.000 | 200/5 |
| ig:rule/index:bm25+rnorm=minmax | ctx:bm25 | mrr | +0.066 | [+0.054, +0.077] | 0.000 | 145/3 |
| ig:rule/index:bm25+rnorm=minmax | ctx:bm25 | useful@1 | +0.110 | [+0.088, +0.132] | 0.000 | 86/1 |
| ig:rule/index:bm25 | ctx:bm25 | ndcg@10 | +0.048 | [+0.039, +0.056] | 0.000 | 200/5 |
| ig:rule/index:bm25 | ctx:bm25 | mrr | +0.066 | [+0.054, +0.077] | 0.000 | 145/3 |
| ig:rule/index:bm25 | ctx:bm25 | useful@1 | +0.110 | [+0.088, +0.132] | 0.000 | 86/1 |
