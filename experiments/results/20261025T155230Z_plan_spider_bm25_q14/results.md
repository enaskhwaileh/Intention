# IGBench results (20261025T155230Z_plan_spider_bm25_q14)

Benchmark `target-spider-test` on corpus `target-spider-test` (180 tables), IL 1.0.0, labels: **established_benchmark_gold**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:bm25 | 0.840 | 0.269 | 0.146 | 0.952 | 0.841 | 0.744 | 0.000 |
| ig:llm/llm:bm25 | 0.857 | 0.272 | 0.146 | 0.954 | 0.862 | 0.776 | 0.000 |
| ig:llm/llm:bm25+repair=1 | 0.861 | 0.273 | 0.146 | 0.953 | 0.867 | 0.784 | 0.000 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.861 | 0.273 | 0.146 | 0.953 | 0.867 | 0.784 | 0.000 |
| ig:llm/llm:bm25+repair=1+align=0 | 0.862 | 0.273 | 0.146 | 0.953 | 0.868 | 0.786 | 0.000 |
| rerank:llm:bm25 | 0.915 | 0.286 | 0.148 | 0.961 | 0.927 | 0.881 | 0.000 |

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
| ig:llm/llm:bm25 | 0.591 | 0.908 | 0.954 |
| ig:llm/llm:bm25+repair=1 | 0.597 | 0.910 | 0.953 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.597 | 0.910 | 0.953 |
| ig:llm/llm:bm25+repair=1+align=0 | 0.599 | 0.910 | 0.953 |
| rerank:llm:bm25 | 0.673 | 0.942 | 0.961 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | extreme (n=201) | lookup (n=971) | mean (n=162) | total_or_count (n=813) |
|---|---|---|---|---|
| ctx:bm25 | 0.864 | 0.842 | 0.931 | 0.815 |
| ig:llm/llm:bm25 | 0.870 | 0.866 | 0.945 | 0.825 |
| ig:llm/llm:bm25+repair=1 | 0.874 | 0.869 | 0.947 | 0.830 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.874 | 0.869 | 0.947 | 0.830 |
| ig:llm/llm:bm25+repair=1+align=0 | 0.874 | 0.867 | 0.947 | 0.835 |
| rerank:llm:bm25 | 0.951 | 0.920 | 0.953 | 0.893 |

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
| ctx:bm25 | – | 0.1 / 0.1 / 0.2 | – | – | – | – | 0.1 / 0.1 / 0.2 | 0.256 |
| ig:llm/llm:bm25 | 4.3 / 3.3 / 9.2 | 0.2 / 0.2 / 0.3 | 1.2 / 1.2 / 2.6 | 1.9 / 0.0 / 18.4 | 20.3 / 0.0 / 51.1 | 0.1 / 0.1 / 0.2 | 27.9 / 4.9 / 81.3 | 4.028 |
| ig:llm/llm:bm25+repair=1 | 3360.7 / 0.9 / 18413.9 | 0.1 / 0.1 / 0.2 | 19066.3 / 1.6 / 62952.4 | 1.9 / 0.0 / 18.3 | 15.2 / 0.0 / 48.2 | 0.1 / 0.1 / 0.2 | 22444.3 / 35.3 / 69833.6 | 1764.394 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 7.0 / 5.9 / 14.5 | 0.1 / 0.1 / 0.2 | 1.9 / 1.3 / 4.8 | 3.6 / 0.0 / 25.3 | 23.8 / 0.0 / 86.1 | 0.1 / 0.1 / 0.2 | 36.5 / 8.6 / 122.6 | 5.296 |
| ig:llm/llm:bm25+repair=1+align=0 | 7.0 / 4.6 / 22.5 | 0.1 / 0.1 / 0.2 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.2 / 0.2 / 0.3 | 7.2 / 4.8 / 22.7 | 2.186 |
| rerank:llm:bm25 | – | 0.4 / 0.4 / 0.8 | – | – | – | – | 19784.4 / 20072.0 / 22388.5 | 2685.899 |

Context index build (one-off, ms): bm25: 2 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:llm/llm:bm25+repair=1+align=0 | ctx:bm25 | ndcg@10 | +0.021 | [+0.017, +0.026] | 0.000 | 383/74 |
| ig:llm/llm:bm25+repair=1+align=0 | ctx:bm25 | mrr | +0.028 | [+0.021, +0.034] | 0.000 | 255/43 |
| ig:llm/llm:bm25+repair=1+align=0 | ctx:bm25 | useful@1 | +0.042 | [+0.032, +0.053] | 0.000 | 119/29 |
| ig:llm/llm:bm25 | ctx:bm25 | ndcg@10 | +0.016 | [+0.012, +0.020] | 0.000 | 315/67 |
| ig:llm/llm:bm25 | ctx:bm25 | mrr | +0.021 | [+0.016, +0.027] | 0.000 | 213/43 |
| ig:llm/llm:bm25 | ctx:bm25 | useful@1 | +0.032 | [+0.022, +0.042] | 0.000 | 100/31 |
| ig:llm/llm:bm25+repair=1 | ctx:bm25 | ndcg@10 | +0.020 | [+0.016, +0.025] | 0.000 | 387/86 |
| ig:llm/llm:bm25+repair=1 | ctx:bm25 | mrr | +0.026 | [+0.020, +0.033] | 0.000 | 257/54 |
| ig:llm/llm:bm25+repair=1 | ctx:bm25 | useful@1 | +0.040 | [+0.029, +0.051] | 0.000 | 122/36 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | ctx:bm25 | ndcg@10 | +0.020 | [+0.016, +0.025] | 0.000 | 387/86 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | ctx:bm25 | mrr | +0.026 | [+0.020, +0.033] | 0.000 | 257/54 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | ctx:bm25 | useful@1 | +0.040 | [+0.029, +0.051] | 0.000 | 122/36 |
