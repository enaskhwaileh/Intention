# IGBench results (20261025T113938Z_plan_spider_bm25)

Benchmark `target-spider-test` on corpus `target-spider-test` (180 tables), IL 1.0.0, labels: **established_benchmark_gold**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:bm25 | 0.840 | 0.269 | 0.146 | 0.952 | 0.841 | 0.744 | 0.000 |
| ig:rule/index:bm25 | 0.882 | 0.277 | 0.146 | 0.955 | 0.895 | 0.828 | 0.000 |
| ig:rule/index:bm25+rnorm=minmax | 0.882 | 0.277 | 0.146 | 0.955 | 0.895 | 0.828 | 0.000 |
| ig:rule/index:bm25+align=0 | 0.882 | 0.277 | 0.146 | 0.955 | 0.894 | 0.828 | 0.000 |
| rerank:ce:bm25 | 0.859 | 0.267 | 0.145 | 0.947 | 0.872 | 0.805 | 0.000 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:bm25 | – | – | – | – |
| ig:rule/index:bm25 | – | – | – | – |
| ig:rule/index:bm25+rnorm=minmax | – | – | – | – |
| ig:rule/index:bm25+align=0 | – | – | – | – |
| rerank:ce:bm25 | – | – | – | – |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:bm25 | 0.564 | 0.902 | 0.952 |
| ig:rule/index:bm25 | 0.635 | 0.918 | 0.955 |
| ig:rule/index:bm25+rnorm=minmax | 0.635 | 0.918 | 0.955 |
| ig:rule/index:bm25+align=0 | 0.635 | 0.919 | 0.955 |
| rerank:ce:bm25 | 0.606 | 0.891 | 0.947 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | extreme (n=201) | lookup (n=971) | mean (n=162) | total_or_count (n=813) |
|---|---|---|---|---|
| ctx:bm25 | 0.864 | 0.842 | 0.931 | 0.815 |
| ig:rule/index:bm25 | 0.923 | 0.880 | 0.950 | 0.862 |
| ig:rule/index:bm25+rnorm=minmax | 0.923 | 0.880 | 0.950 | 0.862 |
| ig:rule/index:bm25+align=0 | 0.923 | 0.880 | 0.950 | 0.862 |
| rerank:ce:bm25 | 0.917 | 0.885 | 0.929 | 0.800 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:bm25 | – |
| ig:rule/index:bm25 | – |
| ig:rule/index:bm25+rnorm=minmax | – |
| ig:rule/index:bm25+align=0 | – |
| rerank:ce:bm25 | – |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:bm25 | – | 0.1 / 0.1 / 0.2 | – | – | – | – | 0.1 / 0.1 / 0.2 | 0.258 |
| ig:rule/index:bm25 | 0.3 / 0.3 / 0.4 | 0.1 / 0.1 / 0.2 | 0.1 / 0.0 / 0.5 | 3.2 / 0.0 / 0.0 | 14.4 / 0.0 / 0.0 | 0.2 / 0.2 / 0.3 | 18.2 / 0.5 / 4.5 | 2.822 |
| ig:rule/index:bm25+rnorm=minmax | 0.6 / 0.3 / 0.4 | 0.2 / 0.1 / 0.3 | 0.1 / 0.0 / 0.5 | 1.3 / 0.0 / 0.0 | 17.1 / 0.0 / 0.0 | 0.1 / 0.1 / 0.3 | 19.3 / 0.4 / 5.6 | 3.041 |
| ig:rule/index:bm25+align=0 | 0.8 / 0.1 / 0.3 | 0.1 / 0.1 / 0.2 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.2 / 0.2 / 0.3 | 1.0 / 0.3 / 0.6 | 0.904 |
| rerank:ce:bm25 | – | 0.3 / 0.2 / 0.6 | – | – | – | – | 4656.8 / 4876.0 / 6438.2 | 626.049 |

Context index build (one-off, ms): bm25: 2 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:rule/index:bm25+align=0 | ctx:bm25 | ndcg@10 | +0.042 | [+0.037, +0.047] | 0.000 | 587/21 |
| ig:rule/index:bm25+align=0 | ctx:bm25 | mrr | +0.054 | [+0.047, +0.060] | 0.000 | 347/8 |
| ig:rule/index:bm25+align=0 | ctx:bm25 | useful@1 | +0.084 | [+0.072, +0.096] | 0.000 | 185/5 |
| ig:rule/index:bm25+rnorm=minmax | ctx:bm25 | ndcg@10 | +0.042 | [+0.037, +0.047] | 0.000 | 588/24 |
| ig:rule/index:bm25+rnorm=minmax | ctx:bm25 | mrr | +0.054 | [+0.048, +0.060] | 0.000 | 347/8 |
| ig:rule/index:bm25+rnorm=minmax | ctx:bm25 | useful@1 | +0.084 | [+0.073, +0.096] | 0.000 | 186/5 |
| ig:rule/index:bm25 | ctx:bm25 | ndcg@10 | +0.042 | [+0.037, +0.047] | 0.000 | 588/25 |
| ig:rule/index:bm25 | ctx:bm25 | mrr | +0.054 | [+0.048, +0.060] | 0.000 | 347/8 |
| ig:rule/index:bm25 | ctx:bm25 | useful@1 | +0.084 | [+0.073, +0.096] | 0.000 | 186/5 |
