# IGBench results (20261027T083646Z_plan_spider_taberta_q32)

Benchmark `target-spider-test` on corpus `target-spider-test` (180 tables), IL 1.0.0, labels: **established_benchmark_gold**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:taberta | 0.783 | 0.255 | 0.142 | 0.933 | 0.777 | 0.661 | 0.000 |
| ig:llm/llm:taberta | 0.790 | 0.256 | 0.143 | 0.937 | 0.784 | 0.671 | 0.000 |
| ig:llm/llm:taberta+repair=1 | 0.793 | 0.256 | 0.143 | 0.938 | 0.785 | 0.674 | 0.000 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | 0.793 | 0.256 | 0.143 | 0.938 | 0.786 | 0.675 | 0.000 |
| ig:llm/llm:taberta+repair=1+align=0 | 0.791 | 0.256 | 0.143 | 0.938 | 0.784 | 0.672 | 0.000 |

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
| ig:llm/llm:taberta | 0.498 | 0.858 | 0.937 |
| ig:llm/llm:taberta+repair=1 | 0.502 | 0.859 | 0.938 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | 0.502 | 0.859 | 0.938 |
| ig:llm/llm:taberta+repair=1+align=0 | 0.499 | 0.858 | 0.938 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | extreme (n=201) | lookup (n=971) | mean (n=162) | total_or_count (n=813) |
|---|---|---|---|---|
| ctx:taberta | 0.808 | 0.791 | 0.763 | 0.772 |
| ig:llm/llm:taberta | 0.826 | 0.794 | 0.790 | 0.776 |
| ig:llm/llm:taberta+repair=1 | 0.832 | 0.798 | 0.799 | 0.775 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | 0.832 | 0.798 | 0.794 | 0.777 |
| ig:llm/llm:taberta+repair=1+align=0 | 0.834 | 0.798 | 0.782 | 0.775 |

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
| ctx:taberta | – | 8.2 / 8.1 / 8.4 | – | – | – | – | 8.3 / 8.1 / 8.4 | 17.736 |
| ig:llm/llm:taberta | 11.6 / 9.6 / 26.7 | 8.1 / 8.1 / 8.3 | 0.7 / 0.8 / 1.8 | 0.8 / 0.0 / 0.0 | 2.2 / 0.0 / 0.0 | 0.1 / 0.1 / 0.3 | 15.5 / 11.0 / 36.5 | 20.637 |
| ig:llm/llm:taberta+repair=1 | 18.0 / 15.4 / 40.8 | 8.0 / 8.0 / 8.2 | 1.0 / 0.8 / 2.6 | 1.1 / 0.0 / 15.1 | 3.3 / 0.0 / 17.4 | 0.1 / 0.1 / 0.2 | 23.6 / 17.5 / 57.7 | 21.119 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | 16.9 / 14.6 / 38.1 | 7.9 / 7.9 / 8.2 | 1.0 / 0.9 / 2.4 | 1.2 / 0.0 / 15.8 | 3.1 / 0.0 / 18.1 | 0.1 / 0.1 / 0.2 | 22.4 / 16.5 / 56.4 | 20.828 |
| ig:llm/llm:taberta+repair=1+align=0 | 17.8 / 15.7 / 39.1 | 8.0 / 7.9 / 8.2 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.2 / 0.2 / 0.3 | 18.1 / 16.0 / 39.3 | 20.573 |

Context index build (one-off, ms): taberta: 9897 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:llm/llm:taberta+repair=1 | ctx:taberta | ndcg@10 | +0.010 | [+0.004, +0.015] | 0.000 | 422/320 |
| ig:llm/llm:taberta+repair=1 | ctx:taberta | mrr | +0.008 | [+0.000, +0.015] | 0.035 | 269/205 |
| ig:llm/llm:taberta+repair=1 | ctx:taberta | useful@1 | +0.013 | [+0.001, +0.026] | 0.043 | 111/82 |
| ig:llm/llm:taberta+repair=1+align=0 | ctx:taberta | ndcg@10 | +0.008 | [+0.003, +0.013] | 0.001 | 414/318 |
| ig:llm/llm:taberta+repair=1+align=0 | ctx:taberta | mrr | +0.006 | [-0.002, +0.013] | 0.104 | 261/205 |
| ig:llm/llm:taberta+repair=1+align=0 | ctx:taberta | useful@1 | +0.011 | [-0.002, +0.023] | 0.111 | 105/82 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | ctx:taberta | ndcg@10 | +0.010 | [+0.005, +0.015] | 0.000 | 421/317 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | ctx:taberta | mrr | +0.008 | [+0.001, +0.016] | 0.023 | 269/202 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | ctx:taberta | useful@1 | +0.014 | [+0.001, +0.026] | 0.033 | 109/79 |
| ig:llm/llm:taberta | ctx:taberta | ndcg@10 | +0.007 | [+0.002, +0.012] | 0.002 | 300/222 |
| ig:llm/llm:taberta | ctx:taberta | mrr | +0.006 | [-0.000, +0.013] | 0.053 | 198/154 |
| ig:llm/llm:taberta | ctx:taberta | useful@1 | +0.010 | [-0.001, +0.021] | 0.074 | 80/58 |
