# IGBench results (20261024T215231Z_srv_target_bird-validation)

Benchmark `target-bird-validation` on corpus `target-bird-validation` (75 tables), IL 1.0.0, labels: **established_benchmark_gold**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:bm25 | 0.762 | 0.283 | 0.164 | 0.875 | 0.810 | 0.720 | 0.000 |
| ctx:sbert | 0.863 | 0.329 | 0.184 | 0.963 | 0.893 | 0.821 | 0.000 |
| ig:rule/index:bm25 | 0.791 | 0.300 | 0.167 | 0.893 | 0.836 | 0.747 | 0.000 |
| ig:rule/index:sbert | 0.862 | 0.330 | 0.183 | 0.960 | 0.894 | 0.825 | 0.000 |
| ig:rule/index:bm25+rnorm=minmax | 0.791 | 0.300 | 0.167 | 0.893 | 0.836 | 0.747 | 0.000 |
| ig:rule/index:sbert+rnorm=minmax | 0.863 | 0.330 | 0.184 | 0.960 | 0.894 | 0.825 | 0.000 |

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
| ctx:bm25 | 0.426 | 0.773 | 0.875 |
| ctx:sbert | 0.486 | 0.877 | 0.963 |
| ig:rule/index:bm25 | 0.443 | 0.814 | 0.893 |
| ig:rule/index:sbert | 0.487 | 0.878 | 0.960 |
| ig:rule/index:bm25+rnorm=minmax | 0.443 | 0.814 | 0.893 |
| ig:rule/index:sbert+rnorm=minmax | 0.487 | 0.878 | 0.960 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | extreme (n=235) | lookup (n=655) | mean (n=55) | total_or_count (n=588) |
|---|---|---|---|---|
| ctx:bm25 | 0.770 | 0.787 | 0.703 | 0.735 |
| ctx:sbert | 0.860 | 0.845 | 0.827 | 0.887 |
| ig:rule/index:bm25 | 0.782 | 0.805 | 0.735 | 0.784 |
| ig:rule/index:sbert | 0.852 | 0.847 | 0.841 | 0.886 |
| ig:rule/index:bm25+rnorm=minmax | 0.782 | 0.805 | 0.735 | 0.783 |
| ig:rule/index:sbert+rnorm=minmax | 0.851 | 0.847 | 0.841 | 0.886 |

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
| ctx:bm25 | – | 0.1 / 0.1 / 0.2 | – | – | – | – | 0.1 / 0.1 / 0.2 | 0.239 |
| ctx:sbert | – | 5.4 / 5.2 / 5.8 | – | – | – | – | 5.4 / 5.2 / 5.8 | 8.323 |
| ig:rule/index:bm25 | 0.1 / 0.1 / 0.1 | 0.1 / 0.1 / 0.2 | 0.2 / 0.0 / 0.5 | 1.7 / 0.0 / 0.0 | 2663.7 / 0.0 / 0.0 | 0.1 / 0.1 / 0.2 | 2666.0 / 0.3 / 7.8 | 1391.301 |
| ig:rule/index:sbert | 0.2 / 0.2 / 0.4 | 10.8 / 7.8 / 19.0 | 0.2 / 0.0 / 0.7 | 13.5 / 0.0 / 0.0 | 3166.5 / 0.0 / 0.0 | 0.2 / 0.2 / 0.3 | 3180.7 / 0.4 / 7.3 | 1454.75 |
| ig:rule/index:bm25+rnorm=minmax | 0.1 / 0.1 / 0.1 | 0.1 / 0.1 / 0.2 | 0.2 / 0.0 / 0.6 | 18.3 / 0.0 / 0.0 | 2814.1 / 0.0 / 0.0 | 0.1 / 0.1 / 0.3 | 2833.0 / 0.2 / 7.1 | 1453.443 |
| ig:rule/index:sbert+rnorm=minmax | 0.2 / 0.2 / 0.3 | 9.3 / 8.6 / 19.4 | 0.2 / 0.0 / 0.7 | 2.7 / 0.0 / 0.0 | 3327.1 / 0.0 / 0.0 | 0.2 / 0.2 / 0.3 | 3330.6 / 0.4 / 8.3 | 1616.874 |

Context index build (one-off, ms): bm25: 2 (cached), sbert: 8636 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:rule/index:sbert+rnorm=minmax | ctx:sbert | ndcg@10 | -0.000 | [-0.004, +0.004] | 0.903 | 261/247 |
| ig:rule/index:sbert+rnorm=minmax | ctx:sbert | mrr | +0.001 | [-0.006, +0.007] | 0.811 | 78/84 |
| ig:rule/index:sbert+rnorm=minmax | ctx:sbert | useful@1 | +0.004 | [-0.009, +0.016] | 0.615 | 52/46 |
| ig:rule/index:sbert | ctx:sbert | ndcg@10 | -0.001 | [-0.005, +0.004] | 0.838 | 260/248 |
| ig:rule/index:sbert | ctx:sbert | mrr | +0.001 | [-0.006, +0.007] | 0.836 | 77/84 |
| ig:rule/index:sbert | ctx:sbert | useful@1 | +0.004 | [-0.009, +0.016] | 0.615 | 52/46 |
| ig:rule/index:bm25+rnorm=minmax | ctx:bm25 | ndcg@10 | +0.029 | [+0.024, +0.034] | 0.000 | 437/95 |
| ig:rule/index:bm25+rnorm=minmax | ctx:bm25 | mrr | +0.026 | [+0.018, +0.034] | 0.000 | 199/48 |
| ig:rule/index:bm25+rnorm=minmax | ctx:bm25 | useful@1 | +0.027 | [+0.015, +0.040] | 0.000 | 63/21 |
| ig:rule/index:bm25 | ctx:bm25 | ndcg@10 | +0.029 | [+0.024, +0.034] | 0.000 | 437/95 |
| ig:rule/index:bm25 | ctx:bm25 | mrr | +0.026 | [+0.018, +0.034] | 0.000 | 199/48 |
| ig:rule/index:bm25 | ctx:bm25 | useful@1 | +0.027 | [+0.015, +0.040] | 0.000 | 63/21 |
