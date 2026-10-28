# IGBench results (20261027T005708Z_plan_bird_bm25_q32)

Benchmark `target-bird-validation` on corpus `target-bird-validation` (75 tables), IL 1.0.0, labels: **established_benchmark_gold**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:bm25 | 0.762 | 0.283 | 0.164 | 0.875 | 0.810 | 0.720 | 0.000 |
| ig:llm/llm:bm25 | 0.787 | 0.293 | 0.166 | 0.887 | 0.839 | 0.759 | 0.000 |
| ig:llm/llm:bm25+repair=1 | 0.802 | 0.303 | 0.168 | 0.896 | 0.851 | 0.770 | 0.000 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.802 | 0.303 | 0.168 | 0.896 | 0.851 | 0.771 | 0.000 |
| ig:llm/llm:bm25+repair=1+align=0 | 0.802 | 0.303 | 0.168 | 0.896 | 0.851 | 0.770 | 0.000 |
| rerank:llm:bm25 | 0.899 | 0.337 | 0.174 | 0.921 | 0.951 | 0.920 | 0.000 |

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
| ctx:bm25 | 0.426 | 0.773 | 0.875 |
| ig:llm/llm:bm25 | 0.449 | 0.799 | 0.887 |
| ig:llm/llm:bm25+repair=1 | 0.456 | 0.822 | 0.896 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.456 | 0.821 | 0.896 |
| ig:llm/llm:bm25+repair=1+align=0 | 0.456 | 0.821 | 0.896 |
| rerank:llm:bm25 | 0.548 | 0.898 | 0.921 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | extreme (n=235) | lookup (n=655) | mean (n=55) | total_or_count (n=588) |
|---|---|---|---|---|
| ctx:bm25 | 0.770 | 0.787 | 0.703 | 0.735 |
| ig:llm/llm:bm25 | 0.794 | 0.810 | 0.737 | 0.764 |
| ig:llm/llm:bm25+repair=1 | 0.802 | 0.820 | 0.732 | 0.788 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.802 | 0.821 | 0.732 | 0.789 |
| ig:llm/llm:bm25+repair=1+align=0 | 0.804 | 0.821 | 0.729 | 0.788 |
| rerank:llm:bm25 | 0.901 | 0.908 | 0.837 | 0.892 |

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
| ctx:bm25 | – | 0.1 / 0.1 / 0.2 | – | – | – | – | 0.1 / 0.1 / 0.2 | 0.233 |
| ig:llm/llm:bm25 | 8.1 / 5.4 / 19.0 | 0.1 / 0.1 / 0.2 | 1.2 / 0.0 / 3.9 | 2.9 / 0.0 / 0.0 | 29.8 / 0.0 / 0.0 | 0.1 / 0.1 / 0.2 | 42.2 / 7.6 / 27.8 | 3.854 |
| ig:llm/llm:bm25+repair=1 | 18.3 / 15.8 / 40.2 | 0.2 / 0.1 / 0.2 | 29529.0 / 2.2 / 114551.3 | 4.3 / 0.0 / 34.4 | 40.7 / 0.0 / 293.0 | 0.1 / 0.1 / 0.2 | 29592.6 / 34.3 / 114586.8 | 1452.599 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 11.2 / 8.6 / 27.4 | 0.1 / 0.1 / 0.2 | 2.2 / 1.4 / 5.9 | 5.0 / 0.0 / 34.2 | 48.3 / 0.0 / 346.3 | 0.1 / 0.1 / 0.2 | 67.0 / 11.2 / 390.9 | 6.152 |
| ig:llm/llm:bm25+repair=1+align=0 | 19.6 / 16.6 / 41.0 | 0.1 / 0.1 / 0.2 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.2 / 0.2 / 0.3 | 19.9 / 16.9 / 41.2 | 2.493 |
| rerank:llm:bm25 | – | 0.5 / 0.5 / 0.8 | – | – | – | – | 73186.2 / 72805.5 / 87590.0 | 7033.445 |

Context index build (one-off, ms): bm25: 2 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:llm/llm:bm25+repair=1+align=0 | ctx:bm25 | ndcg@10 | +0.041 | [+0.034, +0.047] | 0.000 | 556/134 |
| ig:llm/llm:bm25+repair=1+align=0 | ctx:bm25 | mrr | +0.041 | [+0.031, +0.051] | 0.000 | 254/63 |
| ig:llm/llm:bm25+repair=1+align=0 | ctx:bm25 | useful@1 | +0.051 | [+0.035, +0.067] | 0.000 | 112/34 |
| ig:llm/llm:bm25 | ctx:bm25 | ndcg@10 | +0.026 | [+0.020, +0.032] | 0.000 | 351/95 |
| ig:llm/llm:bm25 | ctx:bm25 | mrr | +0.029 | [+0.021, +0.037] | 0.000 | 175/46 |
| ig:llm/llm:bm25 | ctx:bm25 | useful@1 | +0.040 | [+0.027, +0.053] | 0.000 | 82/21 |
| ig:llm/llm:bm25+repair=1 | ctx:bm25 | ndcg@10 | +0.040 | [+0.034, +0.047] | 0.000 | 558/139 |
| ig:llm/llm:bm25+repair=1 | ctx:bm25 | mrr | +0.041 | [+0.031, +0.051] | 0.000 | 257/67 |
| ig:llm/llm:bm25+repair=1 | ctx:bm25 | useful@1 | +0.051 | [+0.035, +0.067] | 0.000 | 114/36 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | ctx:bm25 | ndcg@10 | +0.041 | [+0.034, +0.048] | 0.000 | 558/138 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | ctx:bm25 | mrr | +0.041 | [+0.031, +0.051] | 0.000 | 256/66 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | ctx:bm25 | useful@1 | +0.051 | [+0.036, +0.068] | 0.000 | 114/35 |
