# IGBench results (20261025T180945Z_plan_igb-test_stella_q32)

Benchmark `igbench-v1-test` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:sbert | 0.827 | 0.520 | 0.340 | 0.923 | 0.950 | 0.900 | 0.000 |
| ig:llm/llm:sbert | 0.784 | 0.550 | 0.345 | 0.934 | 0.898 | 0.850 | 0.000 |
| ig:llm/llm:sbert+repair=1 | 0.794 | 0.560 | 0.355 | 0.954 | 0.898 | 0.850 | 0.000 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.825 | 0.560 | 0.340 | 0.919 | 0.950 | 0.900 | 0.000 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.789 | 0.540 | 0.330 | 0.903 | 0.875 | 0.750 | 0.050 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:sbert | 0.824 | 0.505 | 0.947 | 0.895 |
| ig:llm/llm:sbert | 0.786 | 0.547 | 0.892 | 0.842 |
| ig:llm/llm:sbert+repair=1 | 0.797 | 0.558 | 0.892 | 0.842 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.830 | 0.558 | 0.947 | 0.895 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.792 | 0.537 | 0.868 | 0.737 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:sbert | 0.407 | 0.796 | 0.923 |
| ig:llm/llm:sbert | 0.337 | 0.779 | 0.934 |
| ig:llm/llm:sbert+repair=1 | 0.337 | 0.791 | 0.954 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.387 | 0.829 | 0.919 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.324 | 0.804 | 0.903 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | compare (n=8) | explain (n=3) | monitor (n=5) | predict (n=4) |
|---|---|---|---|---|
| ctx:sbert | 0.854 | 0.776 | 0.765 | 0.899 |
| ig:llm/llm:sbert | 0.761 | 0.776 | 0.765 | 0.891 |
| ig:llm/llm:sbert+repair=1 | 0.765 | 0.852 | 0.752 | 0.891 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.801 | 0.819 | 0.806 | 0.934 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.779 | 0.798 | 0.734 | 0.903 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:sbert | 0.850 |
| ig:llm/llm:sbert | 0.855 |
| ig:llm/llm:sbert+repair=1 | 0.855 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.855 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.846 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:llm/llm:sbert | 0.762 | 0.931 | 0.911 | 0.714 | 0.684 | 0.684 | 0.623 | 0.316 | 0.630 | 0.791 |
| ig:llm/llm:sbert+repair=1 | 0.952 | 0.840 | 0.930 | 0.905 | 0.895 | 0.895 | 0.728 | 0.105 | 0.644 | 0.758 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.952 | 0.840 | 0.930 | 0.905 | 0.895 | 0.895 | 0.728 | 0.105 | 0.644 | 0.758 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.952 | 0.840 | 0.930 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | – | – |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:sbert | – | 115.4 / 93.7 / 105.5 | – | – | – | – | 115.4 / 93.7 / 105.6 | 2.424 |
| ig:llm/llm:sbert | 4.3 / 4.2 / 5.7 | 96.2 / 94.4 / 104.3 | 1.8 / 1.0 / 5.3 | 15.7 / 18.6 / 29.0 | 163.0 / 85.4 / 321.0 | 0.1 / 0.1 / 0.1 | 185.7 / 118.6 / 348.2 | 3.775 |
| ig:llm/llm:sbert+repair=1 | 5.4 / 5.5 / 9.1 | 90.7 / 90.7 / 95.9 | 2.0 / 1.1 / 5.3 | 17.3 / 17.8 / 28.3 | 268.5 / 121.7 / 848.6 | 0.1 / 0.1 / 0.1 | 294.3 / 156.4 / 878.9 | 4.652 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 6.6 / 5.5 / 10.8 | 94.2 / 92.0 / 98.9 | 2.0 / 0.9 / 5.2 | 30.6 / 19.0 / 28.6 | 328.2 / 161.6 / 1087.7 | 0.1 / 0.1 / 0.1 | 368.5 / 188.7 / 1133.3 | 5.355 |
| ig:llm/llm:sbert+repair=1+align=0 | 5.7 / 4.9 / 9.9 | 94.9 / 93.7 / 97.5 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.4 / 0.4 / 0.7 | 6.2 / 5.4 / 10.2 | 2.444 |

Context index build (one-off, ms): sbert: 9734 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:llm/llm:sbert+repair=1+align=0 | ctx:sbert | ndcg@10 | -0.039 | [-0.081, -0.004] | 0.067 | 6/9 |
| ig:llm/llm:sbert+repair=1+align=0 | ctx:sbert | mrr | -0.075 | [-0.150, +0.000] | 0.253 | 0/3 |
| ig:llm/llm:sbert+repair=1+align=0 | ctx:sbert | useful@1 | -0.150 | [-0.300, +0.000] | 0.253 | 0/3 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | ndcg@10 | -0.005 | [-0.052, +0.040] | 0.850 | 11/6 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | mrr | +0.000 | [-0.100, +0.100] | 1.000 | 2/2 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | useful@1 | +0.000 | [-0.200, +0.200] | 1.000 | 2/2 |
| ig:llm/llm:sbert | ctx:sbert | ndcg@10 | -0.044 | [-0.121, +0.031] | 0.311 | 7/8 |
| ig:llm/llm:sbert | ctx:sbert | mrr | -0.052 | [-0.198, +0.075] | 0.557 | 2/3 |
| ig:llm/llm:sbert | ctx:sbert | useful@1 | -0.050 | [-0.300, +0.150] | 1.000 | 2/3 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | ndcg@10 | -0.035 | [-0.116, +0.045] | 0.448 | 10/9 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | mrr | -0.052 | [-0.198, +0.075] | 0.557 | 2/3 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | useful@1 | -0.050 | [-0.300, +0.150] | 1.000 | 2/3 |
