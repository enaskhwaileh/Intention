# IGBench results (20261025T154945Z_plan_bird_taberta_q14)

Benchmark `target-bird-validation` on corpus `target-bird-validation` (75 tables), IL 1.0.0, labels: **established_benchmark_gold**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:taberta | 0.840 | 0.330 | 0.181 | 0.947 | 0.866 | 0.772 | 0.000 |
| ig:llm/llm:taberta | 0.839 | 0.329 | 0.180 | 0.946 | 0.868 | 0.775 | 0.000 |
| ig:llm/llm:taberta+repair=1 | 0.838 | 0.329 | 0.180 | 0.944 | 0.865 | 0.771 | 0.000 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | 0.838 | 0.329 | 0.180 | 0.944 | 0.866 | 0.772 | 0.000 |
| ig:llm/llm:taberta+repair=1+align=0 | 0.836 | 0.328 | 0.180 | 0.944 | 0.863 | 0.768 | 0.000 |

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
| ctx:taberta | 0.457 | 0.879 | 0.947 |
| ig:llm/llm:taberta | 0.459 | 0.876 | 0.946 |
| ig:llm/llm:taberta+repair=1 | 0.457 | 0.875 | 0.944 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | 0.457 | 0.875 | 0.944 |
| ig:llm/llm:taberta+repair=1+align=0 | 0.455 | 0.874 | 0.944 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | extreme (n=235) | lookup (n=655) | mean (n=55) | total_or_count (n=588) |
|---|---|---|---|---|
| ctx:taberta | 0.838 | 0.825 | 0.772 | 0.864 |
| ig:llm/llm:taberta | 0.832 | 0.822 | 0.773 | 0.868 |
| ig:llm/llm:taberta+repair=1 | 0.831 | 0.822 | 0.784 | 0.864 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | 0.830 | 0.821 | 0.785 | 0.866 |
| ig:llm/llm:taberta+repair=1+align=0 | 0.831 | 0.821 | 0.774 | 0.861 |

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
| ctx:taberta | – | 12.9 / 11.6 / 17.0 | – | – | – | – | 12.9 / 11.6 / 17.0 | 19.84 |
| ig:llm/llm:taberta | 13.8 / 12.6 / 27.2 | 14.0 / 14.3 / 17.5 | 0.8 / 0.9 / 1.9 | 13.2 / 0.0 / 32.1 | 34.3 / 0.0 / 133.7 | 0.1 / 0.1 / 0.3 | 62.4 / 13.9 / 362.5 | 27.921 |
| ig:llm/llm:taberta+repair=1 | 6.6 / 5.1 / 16.4 | 12.6 / 10.9 / 17.1 | 1.3 / 1.1 / 3.3 | 14.3 / 0.0 / 34.3 | 40.0 / 0.0 / 377.6 | 0.1 / 0.1 / 0.3 | 62.5 / 7.4 / 455.7 | 25.631 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | 18.9 / 15.9 / 43.6 | 12.8 / 12.4 / 17.0 | 1.1 / 1.0 / 3.0 | 3.4 / 0.0 / 32.3 | 29.0 / 0.0 / 328.6 | 0.1 / 0.1 / 0.3 | 52.7 / 19.0 / 380.2 | 26.755 |
| ig:llm/llm:taberta+repair=1+align=0 | 22.6 / 16.1 / 41.5 | 13.9 / 14.5 / 17.1 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.1 / 0.1 / 0.2 | 22.8 / 16.3 / 41.9 | 26.023 |

Context index build (one-off, ms): taberta: 10563 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:llm/llm:taberta+repair=1 | ctx:taberta | ndcg@10 | -0.002 | [-0.008, +0.004] | 0.539 | 290/267 |
| ig:llm/llm:taberta+repair=1 | ctx:taberta | mrr | -0.001 | [-0.009, +0.009] | 0.884 | 116/111 |
| ig:llm/llm:taberta+repair=1 | ctx:taberta | useful@1 | -0.001 | [-0.016, +0.016] | 0.939 | 78/80 |
| ig:llm/llm:taberta+repair=1+align=0 | ctx:taberta | ndcg@10 | -0.004 | [-0.009, +0.002] | 0.220 | 277/269 |
| ig:llm/llm:taberta+repair=1+align=0 | ctx:taberta | mrr | -0.003 | [-0.011, +0.006] | 0.571 | 108/108 |
| ig:llm/llm:taberta+repair=1+align=0 | ctx:taberta | useful@1 | -0.004 | [-0.018, +0.012] | 0.685 | 69/75 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | ctx:taberta | ndcg@10 | -0.002 | [-0.007, +0.004] | 0.592 | 291/262 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | ctx:taberta | mrr | -0.000 | [-0.009, +0.009] | 0.951 | 116/107 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | ctx:taberta | useful@1 | -0.001 | [-0.016, +0.016] | 1.000 | 76/77 |
| ig:llm/llm:taberta | ctx:taberta | ndcg@10 | -0.001 | [-0.005, +0.004] | 0.852 | 210/189 |
| ig:llm/llm:taberta | ctx:taberta | mrr | +0.002 | [-0.006, +0.010] | 0.606 | 85/76 |
| ig:llm/llm:taberta | ctx:taberta | useful@1 | +0.003 | [-0.010, +0.017] | 0.776 | 58/54 |
