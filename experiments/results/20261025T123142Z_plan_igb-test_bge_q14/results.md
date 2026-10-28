# IGBench results (20261025T123142Z_plan_igb-test_bge_q14)

Benchmark `igbench-v1-test` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:sbert | 0.808 | 0.510 | 0.305 | 0.879 | 0.975 | 0.950 | 0.000 |
| ig:llm/llm:sbert | 0.757 | 0.520 | 0.310 | 0.873 | 0.929 | 0.900 | 0.000 |
| ig:llm/llm:sbert+repair=1 | 0.727 | 0.500 | 0.310 | 0.832 | 0.917 | 0.900 | 0.000 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.816 | 0.540 | 0.320 | 0.886 | 0.975 | 0.950 | 0.000 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.798 | 0.520 | 0.305 | 0.871 | 0.942 | 0.900 | 0.050 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:sbert | 0.804 | 0.495 | 0.974 | 0.947 |
| ig:llm/llm:sbert | 0.759 | 0.516 | 0.925 | 0.895 |
| ig:llm/llm:sbert+repair=1 | 0.728 | 0.495 | 0.913 | 0.895 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.822 | 0.537 | 0.974 | 0.947 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.803 | 0.516 | 0.939 | 0.895 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:sbert | 0.437 | 0.797 | 0.879 |
| ig:llm/llm:sbert | 0.387 | 0.797 | 0.873 |
| ig:llm/llm:sbert+repair=1 | 0.345 | 0.739 | 0.832 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.437 | 0.818 | 0.886 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.412 | 0.808 | 0.871 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | compare (n=8) | explain (n=3) | monitor (n=5) | predict (n=4) |
|---|---|---|---|---|
| ctx:sbert | 0.794 | 0.763 | 0.799 | 0.867 |
| ig:llm/llm:sbert | 0.725 | 0.726 | 0.783 | 0.829 |
| ig:llm/llm:sbert+repair=1 | 0.759 | 0.726 | 0.610 | 0.829 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.794 | 0.751 | 0.820 | 0.921 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.766 | 0.760 | 0.796 | 0.911 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:sbert | 0.871 |
| ig:llm/llm:sbert | 0.900 |
| ig:llm/llm:sbert+repair=1 | 0.900 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.881 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.868 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:llm/llm:sbert | 0.857 | 0.774 | 0.980 | 0.714 | 0.684 | 0.684 | 0.588 | 0.316 | 0.633 | 0.775 |
| ig:llm/llm:sbert+repair=1 | 1.000 | 0.788 | 0.933 | 0.905 | 0.895 | 0.895 | 0.781 | 0.105 | 0.608 | 0.692 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 1.000 | 0.788 | 0.933 | 0.905 | 0.895 | 0.895 | 0.781 | 0.105 | 0.608 | 0.692 |
| ig:llm/llm:sbert+repair=1+align=0 | 1.000 | 0.788 | 0.933 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | – | – |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:sbert | – | 106.8 / 83.5 / 106.9 | – | – | – | – | 106.8 / 83.5 / 106.9 | 2.243 |
| ig:llm/llm:sbert | 2.5 / 2.1 / 3.1 | 94.2 / 91.4 / 106.9 | 1.8 / 1.2 / 4.8 | 18.7 / 25.2 / 33.4 | 182.5 / 83.7 / 413.2 | 0.1 / 0.1 / 0.2 | 206.4 / 120.4 / 444.2 | 4.883 |
| ig:llm/llm:sbert+repair=1 | 3.5 / 3.0 / 5.2 | 117.0 / 118.2 / 123.6 | 2.7 / 2.4 / 4.2 | 33.8 / 34.5 / 56.2 | 403.7 / 241.4 / 1348.8 | 0.2 / 0.2 / 0.2 | 445.4 / 302.2 / 1428.0 | 6.748 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 5.2 / 4.6 / 7.9 | 90.1 / 90.9 / 93.8 | 2.3 / 1.2 / 5.9 | 35.8 / 20.7 / 38.1 | 324.5 / 134.1 / 1106.0 | 0.1 / 0.1 / 0.1 | 368.8 / 162.2 / 1131.4 | 5.106 |
| ig:llm/llm:sbert+repair=1+align=0 | 6.1 / 5.2 / 10.0 | 90.2 / 89.6 / 98.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.5 / 0.4 / 0.7 | 6.6 / 5.6 / 10.4 | 2.283 |

Context index build (one-off, ms): sbert: 10645 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:llm/llm:sbert+repair=1+align=0 | ctx:sbert | ndcg@10 | -0.012 | [-0.041, +0.014] | 0.340 | 6/9 |
| ig:llm/llm:sbert+repair=1+align=0 | ctx:sbert | mrr | -0.033 | [-0.100, +0.000] | 0.500 | 0/2 |
| ig:llm/llm:sbert+repair=1+align=0 | ctx:sbert | useful@1 | -0.050 | [-0.150, +0.000] | 1.000 | 0/1 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | ndcg@10 | +0.005 | [-0.027, +0.038] | 0.774 | 7/9 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | mrr | +0.000 | [+0.000, +0.000] | 1.000 | 0/0 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | useful@1 | +0.000 | [+0.000, +0.000] | 1.000 | 0/0 |
| ig:llm/llm:sbert | ctx:sbert | ndcg@10 | -0.051 | [-0.105, -0.004] | 0.049 | 6/10 |
| ig:llm/llm:sbert | ctx:sbert | mrr | -0.046 | [-0.129, +0.000] | 0.502 | 0/2 |
| ig:llm/llm:sbert | ctx:sbert | useful@1 | -0.050 | [-0.150, +0.000] | 1.000 | 0/1 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | ndcg@10 | -0.080 | [-0.175, -0.006] | 0.072 | 8/11 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | mrr | -0.058 | [-0.188, +0.050] | 0.499 | 1/2 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | useful@1 | -0.050 | [-0.200, +0.100] | 1.000 | 1/2 |
