# IGBench results (20261025T123351Z_plan_bird_bm25_q14)

Benchmark `target-bird-validation` on corpus `target-bird-validation` (75 tables), IL 1.0.0, labels: **established_benchmark_gold**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:bm25 | 0.762 | 0.283 | 0.164 | 0.875 | 0.810 | 0.720 | 0.000 |
| ig:llm/llm:bm25 | 0.784 | 0.294 | 0.165 | 0.880 | 0.837 | 0.754 | 0.000 |
| ig:llm/llm:bm25+repair=1 | 0.793 | 0.298 | 0.166 | 0.884 | 0.847 | 0.765 | 0.000 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.793 | 0.298 | 0.166 | 0.883 | 0.847 | 0.765 | 0.000 |
| ig:llm/llm:bm25+repair=1+align=0 | 0.792 | 0.298 | 0.166 | 0.883 | 0.846 | 0.764 | 0.000 |
| rerank:llm:bm25 | 0.879 | 0.327 | 0.172 | 0.912 | 0.939 | 0.901 | 0.000 |

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
| ig:llm/llm:bm25 | 0.447 | 0.798 | 0.880 |
| ig:llm/llm:bm25+repair=1 | 0.454 | 0.809 | 0.884 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.454 | 0.809 | 0.883 |
| ig:llm/llm:bm25+repair=1+align=0 | 0.452 | 0.810 | 0.883 |
| rerank:llm:bm25 | 0.533 | 0.876 | 0.912 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | extreme (n=235) | lookup (n=655) | mean (n=55) | total_or_count (n=588) |
|---|---|---|---|---|
| ctx:bm25 | 0.770 | 0.787 | 0.703 | 0.735 |
| ig:llm/llm:bm25 | 0.783 | 0.802 | 0.721 | 0.770 |
| ig:llm/llm:bm25+repair=1 | 0.790 | 0.805 | 0.733 | 0.786 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 0.790 | 0.805 | 0.733 | 0.785 |
| ig:llm/llm:bm25+repair=1+align=0 | 0.788 | 0.805 | 0.732 | 0.784 |
| rerank:llm:bm25 | 0.879 | 0.887 | 0.820 | 0.875 |

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
| ctx:bm25 | – | 0.1 / 0.1 / 0.2 | – | – | – | – | 0.1 / 0.1 / 0.2 | 0.244 |
| ig:llm/llm:bm25 | 12.8 / 12.1 / 23.5 | 0.1 / 0.1 / 0.2 | 0.8 / 0.8 / 2.0 | 5.3 / 0.0 / 31.4 | 41.8 / 0.0 / 348.6 | 0.1 / 0.1 / 0.2 | 60.9 / 13.3 / 402.4 | 5.15 |
| ig:llm/llm:bm25+repair=1 | 4511.5 / 1.4 / 19628.6 | 0.1 / 0.1 / 0.2 | 24202.2 / 2.1 / 95216.6 | 5.1 / 0.0 / 38.5 | 39.1 / 0.0 / 341.2 | 0.2 / 0.2 / 0.3 | 28758.2 / 11718.1 / 111370.6 | 1656.61 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | 17.2 / 14.5 / 38.2 | 0.1 / 0.1 / 0.2 | 1.7 / 1.3 / 3.9 | 6.0 / 0.0 / 37.5 | 56.9 / 0.0 / 417.5 | 0.1 / 0.1 / 0.3 | 82.1 / 18.5 / 473.6 | 6.691 |
| ig:llm/llm:bm25+repair=1+align=0 | 18.2 / 15.8 / 40.2 | 0.1 / 0.1 / 0.2 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.2 / 0.2 / 0.3 | 18.4 / 16.0 / 40.4 | 2.353 |
| rerank:llm:bm25 | – | 0.4 / 0.4 / 0.7 | – | – | – | – | 50522.1 / 48776.3 / 66348.3 | 4858.583 |

Context index build (one-off, ms): bm25: 2 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:llm/llm:bm25+repair=1+align=0 | ctx:bm25 | ndcg@10 | +0.030 | [+0.023, +0.037] | 0.000 | 501/147 |
| ig:llm/llm:bm25+repair=1+align=0 | ctx:bm25 | mrr | +0.035 | [+0.025, +0.045] | 0.000 | 246/70 |
| ig:llm/llm:bm25+repair=1+align=0 | ctx:bm25 | useful@1 | +0.044 | [+0.029, +0.061] | 0.000 | 108/40 |
| ig:llm/llm:bm25 | ctx:bm25 | ndcg@10 | +0.022 | [+0.016, +0.029] | 0.000 | 363/113 |
| ig:llm/llm:bm25 | ctx:bm25 | mrr | +0.027 | [+0.018, +0.035] | 0.000 | 184/56 |
| ig:llm/llm:bm25 | ctx:bm25 | useful@1 | +0.035 | [+0.021, +0.049] | 0.000 | 85/32 |
| ig:llm/llm:bm25+repair=1 | ctx:bm25 | ndcg@10 | +0.031 | [+0.024, +0.038] | 0.000 | 500/148 |
| ig:llm/llm:bm25+repair=1 | ctx:bm25 | mrr | +0.036 | [+0.026, +0.046] | 0.000 | 249/72 |
| ig:llm/llm:bm25+repair=1 | ctx:bm25 | useful@1 | +0.046 | [+0.030, +0.062] | 0.000 | 111/41 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | ctx:bm25 | ndcg@10 | +0.031 | [+0.024, +0.038] | 0.000 | 500/148 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | ctx:bm25 | mrr | +0.036 | [+0.026, +0.046] | 0.000 | 249/71 |
| ig:llm/llm:bm25+repair=1+rnorm=minmax | ctx:bm25 | useful@1 | +0.046 | [+0.030, +0.062] | 0.000 | 111/41 |
