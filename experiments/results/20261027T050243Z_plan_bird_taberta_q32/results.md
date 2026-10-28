# IGBench results (20261027T050243Z_plan_bird_taberta_q32)

Benchmark `target-bird-validation` on corpus `target-bird-validation` (75 tables), IL 1.0.0, labels: **established_benchmark_gold**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:taberta | 0.840 | 0.330 | 0.181 | 0.947 | 0.866 | 0.772 | 0.000 |
| ig:llm/llm:taberta | 0.845 | 0.331 | 0.180 | 0.947 | 0.872 | 0.783 | 0.000 |
| ig:llm/llm:taberta+repair=1 | 0.844 | 0.332 | 0.181 | 0.947 | 0.870 | 0.776 | 0.000 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | 0.844 | 0.332 | 0.180 | 0.947 | 0.871 | 0.778 | 0.000 |
| ig:llm/llm:taberta+repair=1+align=0 | 0.843 | 0.332 | 0.180 | 0.947 | 0.868 | 0.772 | 0.000 |

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
| ig:llm/llm:taberta | 0.466 | 0.881 | 0.947 |
| ig:llm/llm:taberta+repair=1 | 0.460 | 0.885 | 0.947 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | 0.460 | 0.884 | 0.947 |
| ig:llm/llm:taberta+repair=1+align=0 | 0.459 | 0.884 | 0.947 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | extreme (n=235) | lookup (n=655) | mean (n=55) | total_or_count (n=588) |
|---|---|---|---|---|
| ctx:taberta | 0.838 | 0.825 | 0.772 | 0.864 |
| ig:llm/llm:taberta | 0.846 | 0.828 | 0.778 | 0.870 |
| ig:llm/llm:taberta+repair=1 | 0.847 | 0.827 | 0.770 | 0.869 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | 0.849 | 0.828 | 0.770 | 0.868 |
| ig:llm/llm:taberta+repair=1+align=0 | 0.846 | 0.827 | 0.763 | 0.867 |

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
| ctx:taberta | – | 8.2 / 8.0 / 8.3 | – | – | – | – | 8.3 / 8.0 / 8.3 | 12.666 |
| ig:llm/llm:taberta | 11.2 / 9.1 / 26.2 | 7.9 / 7.9 / 8.1 | 0.7 / 0.0 / 1.9 | 4.0 / 0.0 / 0.0 | 12.8 / 0.0 / 0.0 | 0.1 / 0.1 / 0.3 | 28.9 / 10.6 / 34.1 | 16.31 |
| ig:llm/llm:taberta+repair=1 | 10.3 / 8.1 / 17.9 | 8.0 / 7.9 / 8.2 | 1.2 / 1.1 / 2.7 | 2.8 / 0.0 / 31.2 | 25.9 / 0.0 / 224.9 | 0.1 / 0.1 / 0.2 | 40.5 / 10.1 / 278.2 | 17.576 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | 20.0 / 17.1 / 44.7 | 8.0 / 8.0 / 8.2 | 1.1 / 1.0 / 2.8 | 4.1 / 0.0 / 32.1 | 25.3 / 0.0 / 232.7 | 0.1 / 0.1 / 0.2 | 50.7 / 20.0 / 288.2 | 17.46 |
| ig:llm/llm:taberta+repair=1+align=0 | 20.1 / 17.9 / 43.5 | 8.3 / 8.0 / 8.3 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.2 / 0.2 / 0.4 | 20.4 / 18.2 / 43.7 | 15.536 |

Context index build (one-off, ms): taberta: 9938 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:llm/llm:taberta+repair=1 | ctx:taberta | ndcg@10 | +0.004 | [-0.001, +0.010] | 0.126 | 322/269 |
| ig:llm/llm:taberta+repair=1 | ctx:taberta | mrr | +0.004 | [-0.005, +0.013] | 0.378 | 128/106 |
| ig:llm/llm:taberta+repair=1 | ctx:taberta | useful@1 | +0.004 | [-0.012, +0.021] | 0.696 | 81/75 |
| ig:llm/llm:taberta+repair=1+align=0 | ctx:taberta | ndcg@10 | +0.003 | [-0.002, +0.009] | 0.267 | 311/270 |
| ig:llm/llm:taberta+repair=1+align=0 | ctx:taberta | mrr | +0.002 | [-0.007, +0.011] | 0.670 | 124/108 |
| ig:llm/llm:taberta+repair=1+align=0 | ctx:taberta | useful@1 | +0.000 | [-0.016, +0.017] | 1.000 | 75/75 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | ctx:taberta | ndcg@10 | +0.005 | [-0.001, +0.011] | 0.098 | 317/263 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | ctx:taberta | mrr | +0.005 | [-0.004, +0.014] | 0.269 | 128/103 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | ctx:taberta | useful@1 | +0.005 | [-0.010, +0.021] | 0.575 | 80/72 |
| ig:llm/llm:taberta | ctx:taberta | ndcg@10 | +0.005 | [+0.001, +0.010] | 0.019 | 206/161 |
| ig:llm/llm:taberta | ctx:taberta | mrr | +0.006 | [-0.001, +0.014] | 0.076 | 86/63 |
| ig:llm/llm:taberta | ctx:taberta | useful@1 | +0.010 | [-0.003, +0.024] | 0.134 | 58/42 |
