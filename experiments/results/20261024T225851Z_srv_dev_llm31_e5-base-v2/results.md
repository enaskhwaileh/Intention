# IGBench results (20261024T225851Z_srv_dev_llm31_e5-base-v2)

Benchmark `igbench-v1` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:sbert | 0.820 | 0.543 | 0.337 | 0.894 | 0.929 | 0.886 | 0.057 |
| ig:llm/llm:sbert | 0.764 | 0.543 | 0.320 | 0.849 | 0.903 | 0.857 | 0.057 |
| ig:llm/llm:sbert+rnorm=minmax | 0.827 | 0.566 | 0.343 | 0.899 | 0.929 | 0.886 | 0.057 |
| ig:llm/llm:sbert+repair=1 | 0.762 | 0.543 | 0.320 | 0.849 | 0.903 | 0.857 | 0.057 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.825 | 0.566 | 0.343 | 0.899 | 0.929 | 0.886 | 0.057 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:sbert | 0.826 | 0.519 | 0.943 | 0.906 |
| ig:llm/llm:sbert | 0.765 | 0.519 | 0.914 | 0.875 |
| ig:llm/llm:sbert+rnorm=minmax | 0.834 | 0.544 | 0.943 | 0.906 |
| ig:llm/llm:sbert+repair=1 | 0.763 | 0.519 | 0.914 | 0.875 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.832 | 0.544 | 0.943 | 0.906 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:sbert | 0.361 | 0.780 | 0.894 |
| ig:llm/llm:sbert | 0.356 | 0.785 | 0.849 |
| ig:llm/llm:sbert+rnorm=minmax | 0.361 | 0.809 | 0.899 |
| ig:llm/llm:sbert+repair=1 | 0.356 | 0.785 | 0.849 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.361 | 0.809 | 0.899 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | aggregate (n=3) | compare (n=10) | explain (n=7) | monitor (n=5) | predict (n=8) |
|---|---|---|---|---|---|
| ctx:sbert | 0.948 | 0.829 | 0.835 | 0.773 | 0.798 |
| ig:llm/llm:sbert | 0.858 | 0.796 | 0.798 | 0.773 | 0.654 |
| ig:llm/llm:sbert+rnorm=minmax | 0.946 | 0.857 | 0.832 | 0.773 | 0.791 |
| ig:llm/llm:sbert+repair=1 | 0.858 | 0.796 | 0.799 | 0.758 | 0.654 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.946 | 0.857 | 0.833 | 0.758 | 0.791 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:sbert | 0.834 |
| ig:llm/llm:sbert | 0.841 |
| ig:llm/llm:sbert+rnorm=minmax | 0.833 |
| ig:llm/llm:sbert+repair=1 | 0.841 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.833 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:llm/llm:sbert | 0.778 | 0.779 | 0.920 | 0.639 | 0.594 | 0.594 | 0.578 | 0.406 | 0.496 | 0.744 |
| ig:llm/llm:sbert+rnorm=minmax | 0.778 | 0.779 | 0.920 | 0.639 | 0.594 | 0.594 | 0.578 | 0.406 | 0.496 | 0.744 |
| ig:llm/llm:sbert+repair=1 | 0.833 | 0.790 | 0.889 | 0.667 | 0.625 | 0.625 | 0.609 | 0.375 | 0.496 | 0.739 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.833 | 0.790 | 0.889 | 0.667 | 0.625 | 0.625 | 0.609 | 0.375 | 0.496 | 0.739 |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:sbert | – | 127.0 / 111.2 / 132.2 | – | – | – | – | 127.0 / 111.3 / 132.3 | 4.574 |
| ig:llm/llm:sbert | 5.4 / 4.8 / 9.4 | 112.4 / 101.6 / 143.8 | 1.9 / 1.9 / 3.9 | 37.0 / 34.7 / 93.3 | 1165.8 / 180.8 / 5079.2 | 0.3 / 0.2 / 0.5 | 1212.0 / 262.5 / 5154.6 | 16.789 |
| ig:llm/llm:sbert+rnorm=minmax | 4.9 / 4.6 / 7.3 | 138.3 / 137.5 / 146.3 | 1.6 / 1.6 / 4.0 | 79.4 / 21.0 / 83.9 | 1062.8 / 205.2 / 5021.2 | 0.3 / 0.2 / 0.5 | 1150.5 / 323.5 / 5109.9 | 15.629 |
| ig:llm/llm:sbert+repair=1 | 5.3 / 4.8 / 9.6 | 148.7 / 133.4 / 148.6 | 2.2 / 1.5 / 5.9 | 20.7 / 22.6 / 56.5 | 683.4 / 130.9 / 2584.9 | 0.2 / 0.1 / 0.8 | 712.9 / 161.2 / 2668.9 | 13.294 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 8.4 / 7.2 / 18.3 | 145.1 / 129.1 / 266.7 | 1.9 / 1.4 / 5.4 | 21.8 / 23.4 / 65.6 | 744.8 / 128.3 / 2868.7 | 0.2 / 0.1 / 0.6 | 778.4 / 163.8 / 2903.2 | 14.45 |

Context index build (one-off, ms): sbert: 18068 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | ndcg@10 | +0.004 | [-0.008, +0.016] | 0.585 | 11/12 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | mrr | +0.000 | [+0.000, +0.000] | 1.000 | 0/0 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | useful@1 | +0.000 | [+0.000, +0.000] | 1.000 | 0/0 |
| ig:llm/llm:sbert+rnorm=minmax | ctx:sbert | ndcg@10 | +0.005 | [-0.006, +0.018] | 0.381 | 10/11 |
| ig:llm/llm:sbert+rnorm=minmax | ctx:sbert | mrr | +0.000 | [+0.000, +0.000] | 1.000 | 0/0 |
| ig:llm/llm:sbert+rnorm=minmax | ctx:sbert | useful@1 | +0.000 | [+0.000, +0.000] | 1.000 | 0/0 |
| ig:llm/llm:sbert | ctx:sbert | ndcg@10 | -0.056 | [-0.113, -0.009] | 0.019 | 5/18 |
| ig:llm/llm:sbert | ctx:sbert | mrr | -0.026 | [-0.078, +0.000] | 1.000 | 0/1 |
| ig:llm/llm:sbert | ctx:sbert | useful@1 | -0.029 | [-0.086, +0.000] | 1.000 | 0/1 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | ndcg@10 | -0.058 | [-0.115, -0.012] | 0.015 | 6/19 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | mrr | -0.026 | [-0.078, +0.000] | 1.000 | 0/1 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | useful@1 | -0.029 | [-0.086, +0.000] | 1.000 | 0/1 |
