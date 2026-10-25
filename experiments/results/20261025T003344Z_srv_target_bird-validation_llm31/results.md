# IGBench results (20261025T003344Z_srv_target_bird-validation_llm31)

Benchmark `target-bird-validation` on corpus `target-bird-validation` (75 tables), IL 1.0.0, labels: **established_benchmark_gold**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:bm25 | 0.762 | 0.283 | 0.164 | 0.875 | 0.810 | 0.720 | 0.000 |
| ctx:sbert | 0.863 | 0.329 | 0.184 | 0.963 | 0.893 | 0.821 | 0.000 |
| ig:llm/llm:bm25+repair=1 | 0.787 | 0.295 | 0.165 | 0.880 | 0.841 | 0.760 | 0.000 |
| ig:llm/llm:sbert+repair=1 | 0.857 | 0.328 | 0.184 | 0.960 | 0.888 | 0.814 | 0.000 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.787 | 0.295 | 0.165 | 0.880 | 0.841 | 0.760 | 0.000 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.857 | 0.328 | 0.184 | 0.960 | 0.888 | 0.815 | 0.000 |

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
| ctx:bm25 | 0.426 | 0.773 | 0.875 |
| ctx:sbert | 0.486 | 0.877 | 0.963 |
| ig:llm/llm:bm25+repair=1 | 0.451 | 0.800 | 0.880 |
| ig:llm/llm:sbert+repair=1 | 0.483 | 0.875 | 0.960 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.451 | 0.800 | 0.880 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.483 | 0.875 | 0.960 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | extreme (n=235) | lookup (n=655) | mean (n=55) | total_or_count (n=588) |
|---|---|---|---|---|
| ctx:bm25 | 0.770 | 0.787 | 0.703 | 0.735 |
| ctx:sbert | 0.860 | 0.845 | 0.827 | 0.887 |
| ig:llm/llm:bm25+repair=1 | 0.787 | 0.804 | 0.725 | 0.773 |
| ig:llm/llm:sbert+repair=1 | 0.852 | 0.840 | 0.827 | 0.881 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.787 | 0.804 | 0.725 | 0.773 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.853 | 0.840 | 0.828 | 0.881 |

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
| ctx:bm25 | – | 0.4 / 0.4 / 0.5 | – | – | – | – | 0.4 / 0.4 / 0.5 | 0.651 |
| ctx:sbert | – | 12.7 / 11.5 / 20.6 | – | – | – | – | 12.7 / 11.5 / 20.7 | 19.494 |
| ig:llm/llm:bm25+repair=1 | 2499.1 / 10.8 / 21092.6 | 0.3 / 0.2 / 0.5 | 42017.4 / 30971.0 / 128370.0 | 12.1 / 0.0 / 69.4 | 54.2 / 0.0 / 526.4 | 0.2 / 0.2 / 0.3 | 44583.2 / 32825.3 / 129330.1 | 2339.08 |
| ig:llm/llm:sbert+repair=1 | 17.3 / 14.6 / 35.6 | 12.6 / 11.3 / 20.7 | 1.9 / 1.9 / 4.6 | 5.9 / 0.0 / 63.5 | 60.9 / 0.0 / 529.8 | 0.3 / 0.2 / 0.5 | 86.7 / 18.8 / 620.9 | 27.565 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 8.2 / 5.9 / 20.5 | 0.2 / 0.2 / 0.4 | 1.4 / 1.5 / 3.6 | 5.5 / 0.0 / 59.8 | 57.0 / 0.0 / 497.5 | 0.2 / 0.2 / 0.3 | 72.6 / 8.4 / 579.6 | 9.61 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 14.1 / 11.7 / 29.8 | 12.0 / 11.3 / 18.6 | 1.8 / 1.7 / 4.6 | 6.4 / 0.0 / 62.4 | 64.2 / 0.0 / 542.8 | 0.3 / 0.2 / 0.5 | 87.2 / 15.0 / 619.7 | 26.634 |

Context index build (one-off, ms): bm25: 3 (cached), sbert: 16204 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | ndcg@10 | -0.005 | [-0.010, -0.002] | 0.009 | 197/218 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | mrr | -0.004 | [-0.011, +0.002] | 0.161 | 64/73 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | useful@1 | -0.006 | [-0.017, +0.005] | 0.361 | 34/43 |
| ig:llm/llm:bm25+repair=1 | ctx:bm25 | ndcg@10 | +0.025 | [+0.019, +0.032] | 0.000 | 400/123 |
| ig:llm/llm:bm25+repair=1 | ctx:bm25 | mrr | +0.030 | [+0.021, +0.039] | 0.000 | 199/61 |
| ig:llm/llm:bm25+repair=1 | ctx:bm25 | useful@1 | +0.040 | [+0.025, +0.055] | 0.000 | 95/33 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | ndcg@10 | -0.006 | [-0.010, -0.002] | 0.008 | 198/220 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | mrr | -0.005 | [-0.012, +0.001] | 0.138 | 65/75 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | useful@1 | -0.006 | [-0.018, +0.005] | 0.313 | 35/45 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | ctx:bm25 | ndcg@10 | +0.025 | [+0.019, +0.032] | 0.000 | 400/123 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | ctx:bm25 | mrr | +0.030 | [+0.021, +0.039] | 0.000 | 199/60 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | ctx:bm25 | useful@1 | +0.040 | [+0.025, +0.055] | 0.000 | 95/33 |
