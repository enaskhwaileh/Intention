# IGBench results (20261025T123216Z_plan_igb-test_stella_q14)

Benchmark `igbench-v1-test` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:sbert | 0.827 | 0.520 | 0.340 | 0.923 | 0.950 | 0.900 | 0.000 |
| ig:llm/llm:sbert | 0.789 | 0.570 | 0.340 | 0.919 | 0.906 | 0.850 | 0.000 |
| ig:llm/llm:sbert+repair=1 | 0.790 | 0.560 | 0.355 | 0.952 | 0.919 | 0.900 | 0.000 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.829 | 0.570 | 0.340 | 0.917 | 0.975 | 0.950 | 0.000 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.789 | 0.540 | 0.330 | 0.903 | 0.875 | 0.750 | 0.050 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:sbert | 0.824 | 0.505 | 0.947 | 0.895 |
| ig:llm/llm:sbert | 0.792 | 0.568 | 0.901 | 0.842 |
| ig:llm/llm:sbert+repair=1 | 0.793 | 0.558 | 0.914 | 0.895 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.833 | 0.568 | 0.974 | 0.947 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.792 | 0.537 | 0.868 | 0.737 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:sbert | 0.407 | 0.796 | 0.923 |
| ig:llm/llm:sbert | 0.374 | 0.799 | 0.919 |
| ig:llm/llm:sbert+repair=1 | 0.345 | 0.795 | 0.952 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.395 | 0.837 | 0.917 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.324 | 0.804 | 0.903 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | compare (n=8) | explain (n=3) | monitor (n=5) | predict (n=4) |
|---|---|---|---|---|
| ctx:sbert | 0.854 | 0.776 | 0.765 | 0.899 |
| ig:llm/llm:sbert | 0.765 | 0.791 | 0.762 | 0.900 |
| ig:llm/llm:sbert+repair=1 | 0.787 | 0.791 | 0.732 | 0.900 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.829 | 0.784 | 0.796 | 0.934 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.779 | 0.800 | 0.734 | 0.903 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:sbert | 0.850 |
| ig:llm/llm:sbert | 0.862 |
| ig:llm/llm:sbert+repair=1 | 0.865 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.862 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.842 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:llm/llm:sbert | 0.857 | 0.774 | 0.980 | 0.714 | 0.684 | 0.684 | 0.588 | 0.316 | 0.603 | 0.760 |
| ig:llm/llm:sbert+repair=1 | 1.000 | 0.788 | 0.933 | 0.905 | 0.895 | 0.895 | 0.781 | 0.105 | 0.600 | 0.672 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 1.000 | 0.788 | 0.933 | 0.905 | 0.895 | 0.895 | 0.781 | 0.105 | 0.600 | 0.672 |
| ig:llm/llm:sbert+repair=1+align=0 | 1.000 | 0.788 | 0.933 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | – | – |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:sbert | – | 151.2 / 134.3 / 148.6 | – | – | – | – | 151.3 / 134.4 / 148.7 | 3.177 |
| ig:llm/llm:sbert | 5.8 / 2.4 / 17.0 | 130.1 / 137.7 / 154.6 | 1.8 / 0.9 / 5.8 | 15.8 / 18.7 / 29.4 | 160.9 / 87.7 / 314.7 | 0.1 / 0.1 / 0.2 | 185.2 / 120.0 / 338.6 | 5.24 |
| ig:llm/llm:sbert+repair=1 | 4.9 / 4.7 / 6.8 | 99.9 / 98.8 / 101.8 | 1.8 / 1.0 / 4.4 | 16.6 / 18.2 / 24.7 | 225.7 / 114.5 / 732.9 | 0.1 / 0.1 / 0.1 | 249.9 / 151.0 / 765.3 | 4.81 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 4.8 / 3.8 / 6.9 | 97.4 / 97.6 / 102.3 | 2.1 / 1.2 / 5.6 | 108.6 / 21.9 / 305.7 | 229.0 / 115.5 / 738.9 | 0.1 / 0.1 / 0.1 | 345.5 / 223.5 / 873.1 | 5.595 |
| ig:llm/llm:sbert+repair=1+align=0 | 5.4 / 5.4 / 8.5 | 101.9 / 101.0 / 110.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.3 / 0.4 / 0.5 | 5.8 / 6.0 / 8.8 | 2.586 |

Context index build (one-off, ms): sbert: 10095 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:llm/llm:sbert+repair=1+align=0 | ctx:sbert | ndcg@10 | -0.039 | [-0.081, -0.003] | 0.071 | 7/9 |
| ig:llm/llm:sbert+repair=1+align=0 | ctx:sbert | mrr | -0.075 | [-0.150, +0.000] | 0.253 | 0/3 |
| ig:llm/llm:sbert+repair=1+align=0 | ctx:sbert | useful@1 | -0.150 | [-0.300, +0.000] | 0.253 | 0/3 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | ndcg@10 | -0.002 | [-0.043, +0.034] | 0.936 | 11/7 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | mrr | +0.025 | [-0.050, +0.100] | 1.000 | 2/1 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | useful@1 | +0.050 | [-0.100, +0.200] | 1.000 | 2/1 |
| ig:llm/llm:sbert | ctx:sbert | ndcg@10 | -0.039 | [-0.104, +0.013] | 0.251 | 9/7 |
| ig:llm/llm:sbert | ctx:sbert | mrr | -0.044 | [-0.156, +0.050] | 0.751 | 1/2 |
| ig:llm/llm:sbert | ctx:sbert | useful@1 | -0.050 | [-0.200, +0.100] | 1.000 | 1/2 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | ndcg@10 | -0.038 | [-0.117, +0.036] | 0.363 | 10/9 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | mrr | -0.031 | [-0.175, +0.100] | 0.747 | 2/2 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | useful@1 | +0.000 | [-0.200, +0.200] | 1.000 | 2/2 |
