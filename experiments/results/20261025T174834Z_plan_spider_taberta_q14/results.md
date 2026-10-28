# IGBench results (20261025T174834Z_plan_spider_taberta_q14)

Benchmark `target-spider-test` on corpus `target-spider-test` (180 tables), IL 1.0.0, labels: **established_benchmark_gold**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:taberta | 0.783 | 0.255 | 0.142 | 0.933 | 0.777 | 0.661 | 0.000 |
| ig:llm/llm:taberta | 0.790 | 0.257 | 0.143 | 0.935 | 0.785 | 0.673 | 0.000 |
| ig:llm/llm:taberta+repair=1 | 0.790 | 0.256 | 0.142 | 0.935 | 0.784 | 0.673 | 0.000 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | 0.791 | 0.256 | 0.142 | 0.935 | 0.785 | 0.675 | 0.000 |
| ig:llm/llm:taberta+repair=1+align=0 | 0.787 | 0.256 | 0.142 | 0.934 | 0.780 | 0.667 | 0.000 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:taberta | – | – | – | – |
| ig:llm/llm:taberta | – | – | – | – |
| ig:llm/llm:taberta+repair=1 | – | – | – | – |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | – | – | – | – |
| ig:llm/llm:taberta+repair=1+align=0 | – | – | – | – |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:taberta | 0.487 | 0.855 | 0.933 |
| ig:llm/llm:taberta | 0.498 | 0.861 | 0.935 |
| ig:llm/llm:taberta+repair=1 | 0.498 | 0.860 | 0.935 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | 0.501 | 0.859 | 0.935 |
| ig:llm/llm:taberta+repair=1+align=0 | 0.494 | 0.857 | 0.934 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | extreme (n=201) | lookup (n=971) | mean (n=162) | total_or_count (n=813) |
|---|---|---|---|---|
| ctx:taberta | 0.808 | 0.791 | 0.763 | 0.772 |
| ig:llm/llm:taberta | 0.816 | 0.797 | 0.784 | 0.778 |
| ig:llm/llm:taberta+repair=1 | 0.822 | 0.795 | 0.795 | 0.774 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | 0.822 | 0.796 | 0.792 | 0.776 |
| ig:llm/llm:taberta+repair=1+align=0 | 0.821 | 0.795 | 0.770 | 0.771 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:taberta | – |
| ig:llm/llm:taberta | – |
| ig:llm/llm:taberta+repair=1 | – |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | – |
| ig:llm/llm:taberta+repair=1+align=0 | – |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:taberta | – | 9.4 / 8.7 / 14.9 | – | – | – | – | 9.4 / 8.7 / 14.9 | 20.119 |
| ig:llm/llm:taberta | 11.4 / 10.7 / 20.6 | 9.2 / 8.8 / 14.8 | 0.9 / 1.0 / 2.0 | 1.5 / 0.0 / 17.3 | 5.5 / 0.0 / 33.4 | 0.1 / 0.1 / 0.3 | 19.6 / 12.3 / 65.8 | 23.287 |
| ig:llm/llm:taberta+repair=1 | 15.0 / 13.2 / 31.2 | 9.2 / 8.7 / 14.6 | 1.2 / 0.9 / 3.0 | 2.0 / 0.0 / 19.3 | 6.1 / 0.0 / 44.4 | 0.1 / 0.1 / 0.3 | 24.6 / 16.1 / 80.7 | 24.089 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | 7.1 / 5.4 / 16.3 | 9.3 / 8.7 / 14.8 | 1.1 / 0.9 / 2.7 | 2.0 / 0.0 / 19.1 | 6.3 / 0.0 / 43.5 | 0.1 / 0.1 / 0.2 | 16.7 / 7.3 / 72.8 | 24.353 |
| ig:llm/llm:taberta+repair=1+align=0 | 15.2 / 13.2 / 33.5 | 9.2 / 8.7 / 14.8 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.2 / 0.2 / 0.4 | 15.5 / 13.5 / 33.8 | 22.723 |

Context index build (one-off, ms): taberta: 8220 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:llm/llm:taberta+repair=1 | ctx:taberta | ndcg@10 | +0.007 | [+0.001, +0.012] | 0.020 | 402/332 |
| ig:llm/llm:taberta+repair=1 | ctx:taberta | mrr | +0.007 | [-0.001, +0.015] | 0.088 | 271/215 |
| ig:llm/llm:taberta+repair=1 | ctx:taberta | useful@1 | +0.012 | [-0.001, +0.026] | 0.087 | 118/92 |
| ig:llm/llm:taberta+repair=1+align=0 | ctx:taberta | ndcg@10 | +0.004 | [-0.002, +0.009] | 0.166 | 379/330 |
| ig:llm/llm:taberta+repair=1+align=0 | ctx:taberta | mrr | +0.003 | [-0.005, +0.010] | 0.477 | 251/214 |
| ig:llm/llm:taberta+repair=1+align=0 | ctx:taberta | useful@1 | +0.006 | [-0.006, +0.018] | 0.387 | 101/88 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | ctx:taberta | ndcg@10 | +0.008 | [+0.002, +0.013] | 0.006 | 399/325 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | ctx:taberta | mrr | +0.008 | [+0.000, +0.015] | 0.043 | 268/208 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | ctx:taberta | useful@1 | +0.014 | [+0.001, +0.026] | 0.041 | 115/85 |
| ig:llm/llm:taberta | ctx:taberta | ndcg@10 | +0.007 | [+0.003, +0.012] | 0.003 | 332/251 |
| ig:llm/llm:taberta | ctx:taberta | mrr | +0.008 | [+0.001, +0.014] | 0.028 | 224/160 |
| ig:llm/llm:taberta | ctx:taberta | useful@1 | +0.012 | [+0.000, +0.023] | 0.054 | 95/69 |
