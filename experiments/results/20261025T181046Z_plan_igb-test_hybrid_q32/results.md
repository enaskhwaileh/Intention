# IGBench results (20261025T181046Z_plan_igb-test_hybrid_q32)

Benchmark `igbench-v1-test` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:hybrid | 0.845 | 0.560 | 0.335 | 0.907 | 0.950 | 0.900 | 0.050 |
| ig:llm/llm:hybrid | 0.820 | 0.550 | 0.325 | 0.890 | 0.925 | 0.850 | 0.050 |
| ig:llm/llm:hybrid+repair=1 | 0.828 | 0.550 | 0.335 | 0.913 | 0.925 | 0.850 | 0.050 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | 0.858 | 0.540 | 0.340 | 0.917 | 0.950 | 0.900 | 0.050 |
| ig:llm/llm:hybrid+repair=1+align=0 | 0.829 | 0.550 | 0.330 | 0.895 | 0.917 | 0.850 | 0.100 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:hybrid | 0.839 | 0.547 | 0.947 | 0.895 |
| ig:llm/llm:hybrid | 0.827 | 0.547 | 0.947 | 0.895 |
| ig:llm/llm:hybrid+repair=1 | 0.835 | 0.547 | 0.947 | 0.895 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | 0.867 | 0.537 | 0.974 | 0.947 |
| ig:llm/llm:hybrid+repair=1+align=0 | 0.837 | 0.547 | 0.939 | 0.895 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:hybrid | 0.424 | 0.833 | 0.907 |
| ig:llm/llm:hybrid | 0.374 | 0.824 | 0.890 |
| ig:llm/llm:hybrid+repair=1 | 0.374 | 0.822 | 0.913 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | 0.424 | 0.812 | 0.917 |
| ig:llm/llm:hybrid+repair=1+align=0 | 0.412 | 0.821 | 0.895 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | compare (n=8) | explain (n=3) | monitor (n=5) | predict (n=4) |
|---|---|---|---|---|
| ctx:hybrid | 0.847 | 0.763 | 0.809 | 0.918 |
| ig:llm/llm:hybrid | 0.778 | 0.763 | 0.861 | 0.906 |
| ig:llm/llm:hybrid+repair=1 | 0.793 | 0.782 | 0.854 | 0.906 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | 0.840 | 0.802 | 0.882 | 0.917 |
| ig:llm/llm:hybrid+repair=1+align=0 | 0.826 | 0.767 | 0.800 | 0.928 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:hybrid | 0.860 |
| ig:llm/llm:hybrid | 0.879 |
| ig:llm/llm:hybrid+repair=1 | 0.879 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | 0.879 |
| ig:llm/llm:hybrid+repair=1+align=0 | 0.860 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:llm/llm:hybrid | 0.762 | 0.931 | 0.911 | 0.714 | 0.684 | 0.684 | 0.623 | 0.316 | 0.630 | 0.829 |
| ig:llm/llm:hybrid+repair=1 | 0.952 | 0.840 | 0.930 | 0.905 | 0.895 | 0.895 | 0.728 | 0.105 | 0.639 | 0.780 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | 0.952 | 0.840 | 0.930 | 0.905 | 0.895 | 0.895 | 0.728 | 0.105 | 0.639 | 0.780 |
| ig:llm/llm:hybrid+repair=1+align=0 | 0.952 | 0.840 | 0.930 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | – | – |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:hybrid | – | 103.6 / 81.3 / 92.1 | – | – | – | – | 103.7 / 81.4 / 92.3 | 2.178 |
| ig:llm/llm:hybrid | 4.0 / 3.7 / 5.9 | 85.7 / 84.0 / 95.7 | 1.8 / 0.9 / 5.6 | 14.0 / 17.4 / 27.1 | 194.9 / 97.4 / 614.8 | 0.2 / 0.1 / 0.1 | 215.5 / 137.9 / 639.5 | 3.65 |
| ig:llm/llm:hybrid+repair=1 | 5.5 / 4.9 / 8.6 | 82.1 / 80.3 / 86.8 | 2.0 / 1.0 / 5.2 | 31.8 / 18.8 / 29.6 | 326.5 / 170.4 / 999.5 | 0.1 / 0.1 / 0.1 | 367.0 / 208.1 / 1039.7 | 5.263 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | 123.5 / 9.5 / 256.0 | 81.9 / 81.7 / 87.4 | 1.8 / 1.1 / 5.1 | 16.8 / 18.9 / 24.6 | 283.0 / 137.9 / 1014.1 | 0.2 / 0.1 / 0.2 | 426.3 / 376.1 / 1044.3 | 5.123 |
| ig:llm/llm:hybrid+repair=1+align=0 | 5.3 / 4.7 / 9.1 | 82.3 / 77.6 / 95.2 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.7 / 0.5 / 1.3 | 6.1 / 5.9 / 9.6 | 2.18 |

Context index build (one-off, ms): hybrid: 10292 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:llm/llm:hybrid+repair=1+align=0 | ctx:hybrid | ndcg@10 | -0.021 | [-0.056, +0.001] | 0.168 | 4/7 |
| ig:llm/llm:hybrid+repair=1+align=0 | ctx:hybrid | mrr | -0.033 | [-0.092, +0.000] | 0.501 | 0/2 |
| ig:llm/llm:hybrid+repair=1+align=0 | ctx:hybrid | useful@1 | -0.050 | [-0.150, +0.000] | 1.000 | 0/1 |
| ig:llm/llm:hybrid+repair=1 | ctx:hybrid | ndcg@10 | -0.023 | [-0.071, +0.021] | 0.366 | 7/10 |
| ig:llm/llm:hybrid+repair=1 | ctx:hybrid | mrr | -0.025 | [-0.100, +0.050] | 1.000 | 1/2 |
| ig:llm/llm:hybrid+repair=1 | ctx:hybrid | useful@1 | -0.050 | [-0.200, +0.100] | 1.000 | 1/2 |
| ig:llm/llm:hybrid | ctx:hybrid | ndcg@10 | -0.030 | [-0.073, +0.008] | 0.212 | 5/8 |
| ig:llm/llm:hybrid | ctx:hybrid | mrr | -0.025 | [-0.100, +0.050] | 1.000 | 1/2 |
| ig:llm/llm:hybrid | ctx:hybrid | useful@1 | -0.050 | [-0.200, +0.100] | 1.000 | 1/2 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | ctx:hybrid | ndcg@10 | +0.007 | [-0.036, +0.043] | 0.766 | 5/9 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | ctx:hybrid | mrr | +0.000 | [-0.075, +0.075] | 1.000 | 1/1 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | ctx:hybrid | useful@1 | +0.000 | [-0.150, +0.150] | 1.000 | 1/1 |
