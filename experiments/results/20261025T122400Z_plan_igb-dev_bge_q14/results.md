# IGBench results (20261025T122400Z_plan_igb-dev_bge_q14)

Benchmark `igbench-v1` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:sbert | 0.806 | 0.531 | 0.337 | 0.886 | 0.858 | 0.743 | 0.143 |
| ig:llm/llm:sbert | 0.789 | 0.549 | 0.329 | 0.868 | 0.894 | 0.829 | 0.057 |
| ig:llm/llm:sbert+repair=1 | 0.790 | 0.554 | 0.337 | 0.878 | 0.917 | 0.857 | 0.057 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.845 | 0.554 | 0.349 | 0.905 | 0.936 | 0.886 | 0.057 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.811 | 0.520 | 0.334 | 0.883 | 0.876 | 0.771 | 0.143 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:sbert | 0.808 | 0.525 | 0.845 | 0.719 |
| ig:llm/llm:sbert | 0.789 | 0.544 | 0.884 | 0.812 |
| ig:llm/llm:sbert+repair=1 | 0.791 | 0.550 | 0.909 | 0.844 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.851 | 0.550 | 0.930 | 0.875 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.814 | 0.512 | 0.865 | 0.750 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:sbert | 0.294 | 0.777 | 0.886 |
| ig:llm/llm:sbert | 0.341 | 0.798 | 0.868 |
| ig:llm/llm:sbert+repair=1 | 0.346 | 0.803 | 0.878 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.356 | 0.797 | 0.905 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.306 | 0.771 | 0.883 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | aggregate (n=3) | compare (n=10) | explain (n=7) | monitor (n=5) | predict (n=8) |
|---|---|---|---|---|---|
| ctx:sbert | 0.986 | 0.825 | 0.831 | 0.716 | 0.771 |
| ig:llm/llm:sbert | 0.919 | 0.851 | 0.832 | 0.716 | 0.680 |
| ig:llm/llm:sbert+repair=1 | 0.919 | 0.851 | 0.837 | 0.717 | 0.680 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.984 | 0.872 | 0.877 | 0.743 | 0.817 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.999 | 0.821 | 0.831 | 0.744 | 0.770 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:sbert | 0.842 |
| ig:llm/llm:sbert | 0.827 |
| ig:llm/llm:sbert+repair=1 | 0.845 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.834 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.810 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:llm/llm:sbert | 0.778 | 0.779 | 0.920 | 0.639 | 0.594 | 0.594 | 0.578 | 0.406 | 0.488 | 0.744 |
| ig:llm/llm:sbert+repair=1 | 1.000 | 0.746 | 0.909 | 0.806 | 0.781 | 0.781 | 0.703 | 0.219 | 0.479 | 0.762 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 1.000 | 0.746 | 0.909 | 0.806 | 0.781 | 0.781 | 0.703 | 0.219 | 0.479 | 0.762 |
| ig:llm/llm:sbert+repair=1+align=0 | 1.000 | 0.746 | 0.909 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | – | – |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:sbert | – | 102.0 / 89.6 / 113.9 | – | – | – | – | 102.1 / 89.6 / 114.0 | 3.675 |
| ig:llm/llm:sbert | 15.6 / 3.8 / 74.5 | 108.8 / 111.0 / 133.5 | 1.9 / 1.4 / 5.8 | 19.3 / 21.2 / 52.3 | 936.6 / 56.1 / 4182.4 | 0.2 / 0.1 / 0.6 | 974.5 / 97.1 / 4218.8 | 15.574 |
| ig:llm/llm:sbert+repair=1 | 9.2 / 5.8 / 23.4 | 100.0 / 93.1 / 135.1 | 2.3 / 1.5 / 6.1 | 38.9 / 23.4 / 46.6 | 1107.2 / 222.4 / 4416.8 | 0.1 / 0.1 / 0.3 | 1158.8 / 328.9 / 4451.5 | 17.224 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 8.6 / 8.0 / 16.6 | 92.0 / 91.9 / 102.0 | 2.1 / 1.4 / 5.9 | 20.2 / 23.8 / 40.2 | 1092.0 / 194.7 / 4576.1 | 0.1 / 0.1 / 0.2 | 1124.0 / 233.4 / 4609.4 | 17.545 |
| ig:llm/llm:sbert+repair=1+align=0 | 5.8 / 5.1 / 11.7 | 85.9 / 85.3 / 95.5 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.4 / 0.4 / 0.7 | 6.3 / 5.5 / 12.1 | 3.543 |

Context index build (one-off, ms): sbert: 12122 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:llm/llm:sbert+repair=1+align=0 | ctx:sbert | ndcg@10 | +0.004 | [-0.011, +0.019] | 0.652 | 13/13 |
| ig:llm/llm:sbert+repair=1+align=0 | ctx:sbert | mrr | +0.018 | [-0.029, +0.065] | 0.624 | 3/1 |
| ig:llm/llm:sbert+repair=1+align=0 | ctx:sbert | useful@1 | +0.029 | [-0.057, +0.114] | 1.000 | 2/1 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | ndcg@10 | +0.036 | [+0.010, +0.065] | 0.015 | 18/9 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | mrr | +0.078 | [+0.014, +0.145] | 0.030 | 6/1 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | useful@1 | +0.143 | [+0.029, +0.257] | 0.067 | 5/0 |
| ig:llm/llm:sbert | ctx:sbert | ndcg@10 | -0.018 | [-0.071, +0.025] | 0.573 | 9/13 |
| ig:llm/llm:sbert | ctx:sbert | mrr | +0.036 | [-0.017, +0.098] | 0.256 | 3/1 |
| ig:llm/llm:sbert | ctx:sbert | useful@1 | +0.086 | [+0.000, +0.200] | 0.256 | 3/0 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | ndcg@10 | -0.017 | [-0.071, +0.030] | 0.594 | 13/16 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | mrr | +0.059 | [-0.005, +0.125] | 0.097 | 5/1 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | useful@1 | +0.114 | [+0.029, +0.229] | 0.133 | 4/0 |
