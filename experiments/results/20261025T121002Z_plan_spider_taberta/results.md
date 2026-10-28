# IGBench results (20261025T121002Z_plan_spider_taberta)

Benchmark `target-spider-test` on corpus `target-spider-test` (180 tables), IL 1.0.0, labels: **established_benchmark_gold**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:taberta | 0.783 | 0.255 | 0.142 | 0.933 | 0.777 | 0.661 | 0.000 |
| ig:rule/index:taberta | 0.784 | 0.255 | 0.142 | 0.935 | 0.777 | 0.663 | 0.000 |
| ig:rule/index:taberta+rnorm=minmax | 0.784 | 0.255 | 0.142 | 0.935 | 0.777 | 0.663 | 0.000 |
| ig:rule/index:taberta+align=0 | 0.783 | 0.255 | 0.142 | 0.935 | 0.776 | 0.661 | 0.000 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:taberta | – | – | – | – |
| ig:rule/index:taberta | – | – | – | – |
| ig:rule/index:taberta+rnorm=minmax | – | – | – | – |
| ig:rule/index:taberta+align=0 | – | – | – | – |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:taberta | 0.487 | 0.855 | 0.933 |
| ig:rule/index:taberta | 0.488 | 0.855 | 0.935 |
| ig:rule/index:taberta+rnorm=minmax | 0.488 | 0.855 | 0.935 |
| ig:rule/index:taberta+align=0 | 0.486 | 0.854 | 0.935 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | extreme (n=201) | lookup (n=971) | mean (n=162) | total_or_count (n=813) |
|---|---|---|---|---|
| ctx:taberta | 0.808 | 0.791 | 0.763 | 0.772 |
| ig:rule/index:taberta | 0.825 | 0.784 | 0.774 | 0.774 |
| ig:rule/index:taberta+rnorm=minmax | 0.825 | 0.784 | 0.774 | 0.775 |
| ig:rule/index:taberta+align=0 | 0.825 | 0.784 | 0.774 | 0.773 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:taberta | – |
| ig:rule/index:taberta | – |
| ig:rule/index:taberta+rnorm=minmax | – |
| ig:rule/index:taberta+align=0 | – |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:taberta | – | 11.8 / 11.5 / 15.3 | – | – | – | – | 11.8 / 11.5 / 15.3 | 25.372 |
| ig:rule/index:taberta | 0.2 / 0.2 / 0.4 | 12.2 / 12.5 / 15.4 | 0.1 / 0.0 / 0.5 | 0.8 / 0.0 / 0.0 | 1.4 / 0.0 / 0.0 | 0.2 / 0.2 / 0.4 | 2.9 / 0.4 / 3.6 | 28.581 |
| ig:rule/index:taberta+rnorm=minmax | 0.3 / 0.2 / 0.4 | 9.7 / 8.9 / 12.7 | 0.2 / 0.0 / 0.5 | 0.8 / 0.0 / 0.0 | 1.2 / 0.0 / 0.0 | 0.2 / 0.2 / 0.3 | 2.8 / 0.5 / 5.7 | 22.93 |
| ig:rule/index:taberta+align=0 | 0.2 / 0.1 / 0.2 | 10.2 / 9.6 / 12.8 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.2 / 0.2 / 0.3 | 0.4 / 0.3 / 0.6 | 23.085 |

Context index build (one-off, ms): taberta: 10422 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:rule/index:taberta+align=0 | ctx:taberta | ndcg@10 | -0.000 | [-0.005, +0.005] | 0.949 | 374/373 |
| ig:rule/index:taberta+align=0 | ctx:taberta | mrr | -0.001 | [-0.008, +0.005] | 0.734 | 237/240 |
| ig:rule/index:taberta+align=0 | ctx:taberta | useful@1 | +0.000 | [-0.013, +0.012] | 1.000 | 91/91 |
| ig:rule/index:taberta+rnorm=minmax | ctx:taberta | ndcg@10 | +0.001 | [-0.004, +0.005] | 0.848 | 379/370 |
| ig:rule/index:taberta+rnorm=minmax | ctx:taberta | mrr | -0.000 | [-0.007, +0.006] | 0.956 | 240/237 |
| ig:rule/index:taberta+rnorm=minmax | ctx:taberta | useful@1 | +0.002 | [-0.011, +0.014] | 0.831 | 92/88 |
| ig:rule/index:taberta | ctx:taberta | ndcg@10 | +0.001 | [-0.005, +0.005] | 0.851 | 380/376 |
| ig:rule/index:taberta | ctx:taberta | mrr | -0.000 | [-0.007, +0.007] | 0.987 | 241/237 |
| ig:rule/index:taberta | ctx:taberta | useful@1 | +0.002 | [-0.011, +0.014] | 0.830 | 93/89 |
