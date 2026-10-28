# IGBench results (20261027T050435Z_plan_spider_bm25_q32)

Benchmark `target-spider-test` on corpus `target-spider-test` (180 tables), IL 1.0.0, labels: **established_benchmark_gold**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:bm25 | 0.840 | 0.269 | 0.146 | 0.952 | 0.841 | 0.744 | 0.000 |
| ig:llm/llm:bm25 | 0.861 | 0.273 | 0.146 | 0.953 | 0.868 | 0.785 | 0.000 |
| ig:llm/llm:bm25+repair=1 | 0.867 | 0.273 | 0.146 | 0.953 | 0.876 | 0.796 | 0.000 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.867 | 0.273 | 0.146 | 0.953 | 0.876 | 0.796 | 0.000 |
| ig:llm/llm:bm25+repair=1+align=0 | 0.866 | 0.273 | 0.146 | 0.953 | 0.875 | 0.795 | 0.000 |
| rerank:llm:bm25 | 0.930 | 0.292 | 0.148 | 0.963 | 0.942 | 0.904 | 0.000 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:bm25 | – | – | – | – |
| ig:llm/llm:bm25 | – | – | – | – |
| ig:llm/llm:bm25+repair=1 | – | – | – | – |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | – | – | – | – |
| ig:llm/llm:bm25+repair=1+align=0 | – | – | – | – |
| rerank:llm:bm25 | – | – | – | – |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:bm25 | 0.564 | 0.902 | 0.952 |
| ig:llm/llm:bm25 | 0.598 | 0.912 | 0.953 |
| ig:llm/llm:bm25+repair=1 | 0.608 | 0.913 | 0.953 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.608 | 0.913 | 0.953 |
| ig:llm/llm:bm25+repair=1+align=0 | 0.607 | 0.913 | 0.953 |
| rerank:llm:bm25 | 0.695 | 0.954 | 0.963 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | extreme (n=201) | lookup (n=971) | mean (n=162) | total_or_count (n=813) |
|---|---|---|---|---|
| ctx:bm25 | 0.864 | 0.842 | 0.931 | 0.815 |
| ig:llm/llm:bm25 | 0.879 | 0.864 | 0.938 | 0.838 |
| ig:llm/llm:bm25+repair=1 | 0.885 | 0.873 | 0.942 | 0.839 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.885 | 0.873 | 0.942 | 0.839 |
| ig:llm/llm:bm25+repair=1+align=0 | 0.884 | 0.873 | 0.944 | 0.838 |
| rerank:llm:bm25 | 0.959 | 0.931 | 0.974 | 0.914 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:bm25 | – |
| ig:llm/llm:bm25 | – |
| ig:llm/llm:bm25+repair=1 | – |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | – |
| ig:llm/llm:bm25+repair=1+align=0 | – |
| rerank:llm:bm25 | – |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:bm25 | – | 0.1 / 0.1 / 0.2 | – | – | – | – | 0.1 / 0.1 / 0.2 | 0.253 |
| ig:llm/llm:bm25 | 16963.7 / 16610.4 / 25091.7 | 0.1 / 0.1 / 0.2 | 28276.2 / 45332.9 / 57717.5 | 1.2 / 0.0 / 0.0 | 10.0 / 0.0 / 0.0 | 0.2 / 0.2 / 0.2 | 45251.3 / 58157.2 / 79119.9 | 4208.556 |
| ig:llm/llm:bm25+repair=1 | 5487.4 / 1.2 / 22873.7 | 0.1 / 0.1 / 0.2 | 26723.1 / 2.0 / 101683.9 | 1.3 / 0.0 / 17.8 | 12.5 / 0.0 / 16.9 | 0.2 / 0.2 / 0.2 | 32224.5 / 16761.0 / 118076.4 | 2573.24 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 18.3 / 15.6 / 37.8 | 0.1 / 0.1 / 0.2 | 2.2 / 1.3 / 8.7 | 1.7 / 0.0 / 16.4 | 20.9 / 0.0 / 21.9 | 0.1 / 0.1 / 0.2 | 43.2 / 18.9 / 65.6 | 5.539 |
| ig:llm/llm:bm25+repair=1+align=0 | 11.6 / 8.1 / 32.5 | 0.1 / 0.1 / 0.2 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.2 / 0.2 / 0.3 | 11.9 / 8.3 / 32.6 | 3.024 |
| rerank:llm:bm25 | – | 0.5 / 0.4 / 0.8 | – | – | – | – | 21423.4 / 21315.7 / 23216.7 | 2878.18 |

Context index build (one-off, ms): bm25: 3 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:llm/llm:bm25+repair=1+align=0 | ctx:bm25 | ndcg@10 | +0.025 | [+0.021, +0.030] | 0.000 | 396/55 |
| ig:llm/llm:bm25+repair=1+align=0 | ctx:bm25 | mrr | +0.034 | [+0.028, +0.040] | 0.000 | 263/27 |
| ig:llm/llm:bm25+repair=1+align=0 | ctx:bm25 | useful@1 | +0.051 | [+0.041, +0.062] | 0.000 | 125/15 |
| ig:llm/llm:bm25 | ctx:bm25 | ndcg@10 | +0.021 | [+0.017, +0.025] | 0.000 | 293/41 |
| ig:llm/llm:bm25 | ctx:bm25 | mrr | +0.028 | [+0.022, +0.033] | 0.000 | 212/21 |
| ig:llm/llm:bm25 | ctx:bm25 | useful@1 | +0.041 | [+0.032, +0.051] | 0.000 | 99/11 |
| ig:llm/llm:bm25+repair=1 | ctx:bm25 | ndcg@10 | +0.026 | [+0.022, +0.031] | 0.000 | 401/56 |
| ig:llm/llm:bm25+repair=1 | ctx:bm25 | mrr | +0.035 | [+0.029, +0.041] | 0.000 | 268/28 |
| ig:llm/llm:bm25+repair=1 | ctx:bm25 | useful@1 | +0.053 | [+0.042, +0.064] | 0.000 | 128/15 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | ctx:bm25 | ndcg@10 | +0.026 | [+0.022, +0.031] | 0.000 | 402/56 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | ctx:bm25 | mrr | +0.035 | [+0.029, +0.041] | 0.000 | 268/28 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | ctx:bm25 | useful@1 | +0.053 | [+0.042, +0.064] | 0.000 | 128/15 |
