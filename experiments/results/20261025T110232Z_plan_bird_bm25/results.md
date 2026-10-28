# IGBench results (20261025T110232Z_plan_bird_bm25)

Benchmark `target-bird-validation` on corpus `target-bird-validation` (75 tables), IL 1.0.0, labels: **established_benchmark_gold**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:bm25 | 0.762 | 0.283 | 0.164 | 0.875 | 0.810 | 0.720 | 0.000 |
| ig:rule/index:bm25 | 0.791 | 0.300 | 0.167 | 0.893 | 0.836 | 0.747 | 0.000 |
| ig:rule/index:bm25+rnorm=minmax | 0.791 | 0.300 | 0.167 | 0.893 | 0.836 | 0.747 | 0.000 |
| ig:rule/index:bm25+align=0 | 0.791 | 0.299 | 0.167 | 0.893 | 0.837 | 0.748 | 0.000 |
| rerank:ce:bm25 | 0.820 | 0.326 | 0.174 | 0.922 | 0.845 | 0.749 | 0.000 |

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
| ctx:bm25 | 0.426 | 0.773 | 0.875 |
| ig:rule/index:bm25 | 0.443 | 0.814 | 0.893 |
| ig:rule/index:bm25+rnorm=minmax | 0.443 | 0.814 | 0.893 |
| ig:rule/index:bm25+align=0 | 0.444 | 0.813 | 0.893 |
| rerank:ce:bm25 | 0.436 | 0.868 | 0.922 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | extreme (n=235) | lookup (n=655) | mean (n=55) | total_or_count (n=588) |
|---|---|---|---|---|
| ctx:bm25 | 0.770 | 0.787 | 0.703 | 0.735 |
| ig:rule/index:bm25 | 0.782 | 0.805 | 0.735 | 0.784 |
| ig:rule/index:bm25+rnorm=minmax | 0.782 | 0.805 | 0.735 | 0.783 |
| ig:rule/index:bm25+align=0 | 0.782 | 0.805 | 0.735 | 0.783 |
| rerank:ce:bm25 | 0.848 | 0.854 | 0.712 | 0.780 |

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
| ctx:bm25 | – | 0.1 / 0.1 / 0.2 | – | – | – | – | 0.1 / 0.1 / 0.2 | 0.225 |
| ig:rule/index:bm25 | 0.5 / 0.3 / 0.5 | 0.1 / 0.1 / 0.2 | 0.2 / 0.0 / 0.5 | 3.5 / 0.0 / 0.0 | 26.2 / 0.0 / 0.0 | 0.1 / 0.1 / 0.2 | 30.7 / 0.5 / 21.2 | 2.95 |
| ig:rule/index:bm25+rnorm=minmax | 0.5 / 0.3 / 0.5 | 0.2 / 0.1 / 0.2 | 0.2 / 0.0 / 0.5 | 3.5 / 0.0 / 0.0 | 29.2 / 0.0 / 0.0 | 0.1 / 0.1 / 0.2 | 33.6 / 0.4 / 47.2 | 3.138 |
| ig:rule/index:bm25+align=0 | 0.4 / 0.3 / 0.5 | 0.1 / 0.1 / 0.2 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.2 / 0.2 / 0.3 | 0.6 / 0.5 / 0.8 | 1.263 |
| rerank:ce:bm25 | – | 0.3 / 0.2 / 0.8 | – | – | – | – | 6634.8 / 6597.0 / 7679.0 | 637.245 |

Context index build (one-off, ms): bm25: 3 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:rule/index:bm25+align=0 | ctx:bm25 | ndcg@10 | +0.029 | [+0.024, +0.034] | 0.000 | 433/97 |
| ig:rule/index:bm25+align=0 | ctx:bm25 | mrr | +0.026 | [+0.018, +0.034] | 0.000 | 198/48 |
| ig:rule/index:bm25+align=0 | ctx:bm25 | useful@1 | +0.029 | [+0.017, +0.040] | 0.000 | 64/20 |
| ig:rule/index:bm25+rnorm=minmax | ctx:bm25 | ndcg@10 | +0.029 | [+0.024, +0.034] | 0.000 | 437/95 |
| ig:rule/index:bm25+rnorm=minmax | ctx:bm25 | mrr | +0.026 | [+0.018, +0.034] | 0.000 | 199/48 |
| ig:rule/index:bm25+rnorm=minmax | ctx:bm25 | useful@1 | +0.027 | [+0.015, +0.040] | 0.000 | 63/21 |
| ig:rule/index:bm25 | ctx:bm25 | ndcg@10 | +0.029 | [+0.024, +0.034] | 0.000 | 437/95 |
| ig:rule/index:bm25 | ctx:bm25 | mrr | +0.026 | [+0.018, +0.034] | 0.000 | 199/48 |
| ig:rule/index:bm25 | ctx:bm25 | useful@1 | +0.027 | [+0.015, +0.040] | 0.000 | 63/21 |
