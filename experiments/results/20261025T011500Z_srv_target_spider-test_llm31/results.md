# IGBench results (20261025T011500Z_srv_target_spider-test_llm31)

Benchmark `target-spider-test` on corpus `target-spider-test` (180 tables), IL 1.0.0, labels: **established_benchmark_gold**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:bm25 | 0.840 | 0.269 | 0.146 | 0.952 | 0.841 | 0.744 | 0.000 |
| ctx:sbert | 0.870 | 0.277 | 0.148 | 0.963 | 0.871 | 0.790 | 0.000 |
| ig:llm/llm:bm25+repair=1 | 0.858 | 0.273 | 0.146 | 0.953 | 0.864 | 0.778 | 0.000 |
| ig:llm/llm:sbert+repair=1 | 0.869 | 0.277 | 0.148 | 0.963 | 0.868 | 0.788 | 0.000 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.858 | 0.273 | 0.146 | 0.953 | 0.864 | 0.778 | 0.000 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.869 | 0.277 | 0.148 | 0.963 | 0.869 | 0.789 | 0.000 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:bm25 | – | – | – | – |
| ctx:sbert | – | – | – | – |
| ig:llm/llm:bm25+repair=1 | – | – | – | – |
| ig:llm/llm:sbert+repair=1 | – | – | – | – |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | – | – | – | – |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | – | – | – | – |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:bm25 | 0.564 | 0.902 | 0.952 |
| ctx:sbert | 0.603 | 0.922 | 0.963 |
| ig:llm/llm:bm25+repair=1 | 0.593 | 0.910 | 0.953 |
| ig:llm/llm:sbert+repair=1 | 0.600 | 0.922 | 0.963 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.593 | 0.910 | 0.953 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.601 | 0.922 | 0.963 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | extreme (n=201) | lookup (n=971) | mean (n=162) | total_or_count (n=813) |
|---|---|---|---|---|
| ctx:bm25 | 0.864 | 0.842 | 0.931 | 0.815 |
| ctx:sbert | 0.931 | 0.872 | 0.916 | 0.844 |
| ig:llm/llm:bm25+repair=1 | 0.871 | 0.867 | 0.947 | 0.827 |
| ig:llm/llm:sbert+repair=1 | 0.926 | 0.871 | 0.918 | 0.842 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.871 | 0.867 | 0.947 | 0.827 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.926 | 0.871 | 0.918 | 0.844 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:bm25 | – |
| ctx:sbert | – |
| ig:llm/llm:bm25+repair=1 | – |
| ig:llm/llm:sbert+repair=1 | – |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | – |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | – |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:bm25 | – | 0.3 / 0.3 / 0.6 | – | – | – | – | 0.3 / 0.3 / 0.6 | 0.714 |
| ctx:sbert | – | 10.1 / 9.4 / 15.9 | – | – | – | – | 10.2 / 9.4 / 16.0 | 21.873 |
| ig:llm/llm:bm25+repair=1 | 22017.3 / 18565.2 / 43469.7 | 0.2 / 0.1 / 0.3 | 43579.2 / 32933.7 / 127179.0 | 8.5 / 0.0 / 30.4 | 18.9 / 0.0 / 85.7 | 0.5 / 0.2 / 0.3 | 65624.8 / 52120.5 / 146645.1 | 5956.098 |
| ig:llm/llm:sbert+repair=1 | 14.2 / 12.2 / 27.4 | 11.0 / 10.9 / 13.9 | 1.6 / 1.5 / 3.4 | 2.3 / 0.0 / 23.6 | 8.6 / 0.0 / 58.1 | 0.2 / 0.1 / 0.3 | 27.0 / 15.3 / 99.2 | 28.682 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 11.7 / 10.2 / 22.7 | 0.3 / 0.2 / 0.6 | 1.7 / 1.7 / 3.9 | 13.9 / 0.0 / 30.3 | 29.9 / 0.0 / 102.0 | 0.2 / 0.2 / 0.4 | 57.8 / 13.3 / 161.0 | 9.59 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 13.4 / 11.5 / 28.3 | 11.6 / 10.7 / 20.4 | 1.7 / 1.7 / 3.9 | 3.1 / 0.0 / 29.9 | 13.7 / 0.0 / 86.6 | 0.3 / 0.2 / 0.5 | 32.6 / 14.8 / 147.0 | 32.265 |

Context index build (one-off, ms): bm25: 2 (cached), sbert: 12091 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | ndcg@10 | -0.001 | [-0.005, +0.004] | 0.772 | 205/224 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | mrr | -0.002 | [-0.008, +0.004] | 0.610 | 116/134 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | useful@1 | -0.001 | [-0.012, +0.008] | 0.856 | 59/62 |
| ig:llm/llm:bm25+repair=1 | ctx:bm25 | ndcg@10 | +0.018 | [+0.014, +0.022] | 0.000 | 343/75 |
| ig:llm/llm:bm25+repair=1 | ctx:bm25 | mrr | +0.023 | [+0.017, +0.029] | 0.000 | 231/50 |
| ig:llm/llm:bm25+repair=1 | ctx:bm25 | useful@1 | +0.035 | [+0.024, +0.045] | 0.000 | 109/35 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | ndcg@10 | -0.001 | [-0.006, +0.003] | 0.570 | 204/227 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | mrr | -0.002 | [-0.008, +0.003] | 0.443 | 114/137 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | useful@1 | -0.003 | [-0.013, +0.007] | 0.656 | 59/65 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | ctx:bm25 | ndcg@10 | +0.018 | [+0.014, +0.022] | 0.000 | 343/75 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | ctx:bm25 | mrr | +0.023 | [+0.017, +0.029] | 0.000 | 231/50 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | ctx:bm25 | useful@1 | +0.035 | [+0.024, +0.045] | 0.000 | 109/35 |
