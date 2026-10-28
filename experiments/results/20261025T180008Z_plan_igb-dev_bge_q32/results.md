# IGBench results (20261025T180008Z_plan_igb-dev_bge_q32)

Benchmark `igbench-v1` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:sbert | 0.806 | 0.531 | 0.337 | 0.886 | 0.858 | 0.743 | 0.143 |
| ig:llm/llm:sbert | 0.786 | 0.537 | 0.331 | 0.871 | 0.858 | 0.771 | 0.086 |
| ig:llm/llm:sbert+repair=1 | 0.793 | 0.537 | 0.340 | 0.881 | 0.895 | 0.829 | 0.057 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.844 | 0.549 | 0.349 | 0.905 | 0.936 | 0.886 | 0.057 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.812 | 0.520 | 0.334 | 0.883 | 0.876 | 0.771 | 0.143 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:sbert | 0.808 | 0.525 | 0.845 | 0.719 |
| ig:llm/llm:sbert | 0.787 | 0.531 | 0.845 | 0.750 |
| ig:llm/llm:sbert+repair=1 | 0.794 | 0.531 | 0.885 | 0.812 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.850 | 0.544 | 0.930 | 0.875 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.815 | 0.512 | 0.865 | 0.750 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:sbert | 0.294 | 0.777 | 0.886 |
| ig:llm/llm:sbert | 0.313 | 0.776 | 0.871 |
| ig:llm/llm:sbert+repair=1 | 0.332 | 0.780 | 0.881 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.356 | 0.795 | 0.905 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.306 | 0.771 | 0.883 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | aggregate (n=3) | compare (n=10) | explain (n=7) | monitor (n=5) | predict (n=8) |
|---|---|---|---|---|---|
| ctx:sbert | 0.986 | 0.825 | 0.831 | 0.716 | 0.771 |
| ig:llm/llm:sbert | 0.999 | 0.856 | 0.821 | 0.739 | 0.629 |
| ig:llm/llm:sbert+repair=1 | 0.999 | 0.857 | 0.837 | 0.764 | 0.629 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.999 | 0.868 | 0.872 | 0.759 | 0.810 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.999 | 0.821 | 0.831 | 0.752 | 0.770 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:sbert | 0.842 |
| ig:llm/llm:sbert | 0.822 |
| ig:llm/llm:sbert+repair=1 | 0.840 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.829 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.810 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:llm/llm:sbert | 0.750 | 0.853 | 0.958 | 0.556 | 0.531 | 0.500 | 0.516 | 0.469 | 0.515 | 0.688 |
| ig:llm/llm:sbert+repair=1 | 0.944 | 0.774 | 0.935 | 0.750 | 0.719 | 0.688 | 0.630 | 0.281 | 0.558 | 0.727 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.944 | 0.774 | 0.935 | 0.750 | 0.719 | 0.688 | 0.630 | 0.281 | 0.558 | 0.727 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.944 | 0.774 | 0.935 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | – | – |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:sbert | – | 91.2 / 78.9 / 88.6 | – | – | – | – | 91.2 / 79.0 / 88.6 | 3.283 |
| ig:llm/llm:sbert | 6.8 / 7.1 / 11.3 | 82.8 / 81.2 / 91.4 | 1.6 / 1.2 / 4.1 | 15.9 / 0.0 / 51.8 | 1053.7 / 0.0 / 4779.2 | 0.2 / 0.1 / 0.6 | 1078.9 / 11.2 / 4822.0 | 18.848 |
| ig:llm/llm:sbert+repair=1 | 6.8 / 6.5 / 10.7 | 82.4 / 80.4 / 92.9 | 2.2 / 1.6 / 6.0 | 39.0 / 21.0 / 44.9 | 1234.8 / 114.1 / 4736.0 | 0.2 / 0.1 / 0.6 | 1283.8 / 163.6 / 4777.6 | 19.202 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 90.7 / 6.7 / 350.5 | 83.6 / 81.8 / 91.9 | 1.9 / 1.4 / 5.1 | 17.7 / 21.4 / 38.4 | 1193.0 / 100.5 / 4794.3 | 0.2 / 0.1 / 0.6 | 1304.3 / 287.4 / 4834.9 | 19.329 |
| ig:llm/llm:sbert+repair=1+align=0 | 8.1 / 7.2 / 18.0 | 83.3 / 81.0 / 97.9 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.4 / 0.4 / 0.7 | 8.6 / 7.5 / 18.6 | 3.524 |

Context index build (one-off, ms): sbert: 10534 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:llm/llm:sbert+repair=1+align=0 | ctx:sbert | ndcg@10 | +0.005 | [-0.010, +0.020] | 0.549 | 13/12 |
| ig:llm/llm:sbert+repair=1+align=0 | ctx:sbert | mrr | +0.018 | [-0.029, +0.065] | 0.624 | 3/1 |
| ig:llm/llm:sbert+repair=1+align=0 | ctx:sbert | useful@1 | +0.029 | [-0.057, +0.114] | 1.000 | 2/1 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | ndcg@10 | +0.036 | [+0.010, +0.064] | 0.015 | 16/11 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | mrr | +0.078 | [+0.014, +0.145] | 0.030 | 6/1 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | useful@1 | +0.143 | [+0.029, +0.257] | 0.067 | 5/0 |
| ig:llm/llm:sbert | ctx:sbert | ndcg@10 | -0.021 | [-0.078, +0.025] | 0.508 | 9/12 |
| ig:llm/llm:sbert | ctx:sbert | mrr | +0.000 | [-0.069, +0.067] | 1.000 | 2/2 |
| ig:llm/llm:sbert | ctx:sbert | useful@1 | +0.029 | [-0.057, +0.114] | 1.000 | 2/1 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | ndcg@10 | -0.014 | [-0.073, +0.036] | 0.663 | 13/15 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | mrr | +0.037 | [-0.046, +0.112] | 0.403 | 5/2 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | useful@1 | +0.086 | [-0.029, +0.200] | 0.389 | 4/1 |
