# IGBench results (20261024T234532Z_srv_target_spider-test_full)

Benchmark `target-spider-test` on corpus `target-spider-test` (180 tables), IL 1.0.0, labels: **established_benchmark_gold**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:bm25 | 0.840 | 0.269 | 0.146 | 0.952 | 0.841 | 0.744 | 0.000 |
| ctx:sbert | 0.870 | 0.277 | 0.148 | 0.963 | 0.871 | 0.790 | 0.000 |
| ig:rule/index:bm25 | 0.882 | 0.277 | 0.146 | 0.955 | 0.895 | 0.828 | 0.000 |
| ig:rule/index:sbert | 0.875 | 0.278 | 0.149 | 0.968 | 0.874 | 0.797 | 0.000 |
| ig:rule/index:bm25+rnorm=minmax | 0.882 | 0.277 | 0.146 | 0.955 | 0.895 | 0.828 | 0.000 |
| ig:rule/index:sbert+rnorm=minmax | 0.875 | 0.279 | 0.149 | 0.968 | 0.874 | 0.797 | 0.000 |

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
| ctx:bm25 | 0.564 | 0.902 | 0.952 |
| ctx:sbert | 0.603 | 0.922 | 0.963 |
| ig:rule/index:bm25 | 0.635 | 0.918 | 0.955 |
| ig:rule/index:sbert | 0.607 | 0.925 | 0.968 |
| ig:rule/index:bm25+rnorm=minmax | 0.635 | 0.918 | 0.955 |
| ig:rule/index:sbert+rnorm=minmax | 0.607 | 0.925 | 0.968 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | extreme (n=201) | lookup (n=971) | mean (n=162) | total_or_count (n=813) |
|---|---|---|---|---|
| ctx:bm25 | 0.864 | 0.842 | 0.931 | 0.815 |
| ctx:sbert | 0.931 | 0.872 | 0.916 | 0.844 |
| ig:rule/index:bm25 | 0.923 | 0.880 | 0.950 | 0.862 |
| ig:rule/index:sbert | 0.931 | 0.876 | 0.923 | 0.851 |
| ig:rule/index:bm25+rnorm=minmax | 0.923 | 0.880 | 0.950 | 0.862 |
| ig:rule/index:sbert+rnorm=minmax | 0.931 | 0.876 | 0.923 | 0.851 |

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
| ctx:bm25 | – | 0.2 / 0.2 / 0.4 | – | – | – | – | 0.2 / 0.2 / 0.4 | 0.479 |
| ctx:sbert | – | 11.6 / 11.0 / 16.5 | – | – | – | – | 11.6 / 11.0 / 16.5 | 24.998 |
| ig:rule/index:bm25 | 0.2 / 0.2 / 0.3 | 0.3 / 0.2 / 0.6 | 0.2 / 0.0 / 0.6 | 1.3 / 0.0 / 0.0 | 2.8 / 0.0 / 0.0 | 0.2 / 0.1 / 0.3 | 4.7 / 0.4 / 4.6 | 4.578 |
| ig:rule/index:sbert | 0.6 / 0.1 / 0.3 | 10.8 / 10.8 / 13.9 | 0.1 / 0.0 / 0.5 | 0.9 / 0.0 / 0.0 | 1.8 / 0.0 / 0.0 | 0.2 / 0.2 / 0.3 | 3.7 / 0.4 / 6.2 | 25.81 |
| ig:rule/index:bm25+rnorm=minmax | 1.2 / 0.1 / 0.3 | 0.3 / 0.2 / 0.6 | 0.2 / 0.0 / 0.7 | 1.1 / 0.0 / 0.0 | 3.0 / 0.0 / 0.0 | 0.2 / 0.2 / 0.3 | 5.7 / 0.3 / 31.7 | 5.013 |
| ig:rule/index:sbert+rnorm=minmax | 0.2 / 0.2 / 0.4 | 11.9 / 10.7 / 20.0 | 0.2 / 0.0 / 0.8 | 1.2 / 0.0 / 0.0 | 2.8 / 0.0 / 0.0 | 0.2 / 0.2 / 0.4 | 4.8 / 0.5 / 3.8 | 29.33 |

Context index build (one-off, ms): bm25: 3 (cached), sbert: 16444 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:rule/index:sbert+rnorm=minmax | ctx:sbert | ndcg@10 | +0.005 | [+0.001, +0.009] | 0.016 | 265/204 |
| ig:rule/index:sbert+rnorm=minmax | ctx:sbert | mrr | +0.003 | [-0.002, +0.009] | 0.215 | 131/115 |
| ig:rule/index:sbert+rnorm=minmax | ctx:sbert | useful@1 | +0.007 | [-0.002, +0.016] | 0.182 | 63/48 |
| ig:rule/index:sbert | ctx:sbert | ndcg@10 | +0.005 | [+0.001, +0.009] | 0.016 | 265/204 |
| ig:rule/index:sbert | ctx:sbert | mrr | +0.003 | [-0.002, +0.008] | 0.254 | 130/115 |
| ig:rule/index:sbert | ctx:sbert | useful@1 | +0.006 | [-0.003, +0.016] | 0.212 | 62/48 |
| ig:rule/index:bm25+rnorm=minmax | ctx:bm25 | ndcg@10 | +0.042 | [+0.037, +0.047] | 0.000 | 588/24 |
| ig:rule/index:bm25+rnorm=minmax | ctx:bm25 | mrr | +0.054 | [+0.048, +0.060] | 0.000 | 347/8 |
| ig:rule/index:bm25+rnorm=minmax | ctx:bm25 | useful@1 | +0.084 | [+0.073, +0.096] | 0.000 | 186/5 |
| ig:rule/index:bm25 | ctx:bm25 | ndcg@10 | +0.042 | [+0.037, +0.047] | 0.000 | 588/25 |
| ig:rule/index:bm25 | ctx:bm25 | mrr | +0.054 | [+0.048, +0.060] | 0.000 | 347/8 |
| ig:rule/index:bm25 | ctx:bm25 | useful@1 | +0.084 | [+0.073, +0.096] | 0.000 | 186/5 |
