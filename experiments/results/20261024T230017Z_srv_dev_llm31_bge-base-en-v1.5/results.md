# IGBench results (20261024T230017Z_srv_dev_llm31_bge-base-en-v1.5)

Benchmark `igbench-v1` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:sbert | 0.806 | 0.531 | 0.337 | 0.886 | 0.858 | 0.743 | 0.143 |
| ig:llm/llm:sbert | 0.789 | 0.549 | 0.329 | 0.868 | 0.894 | 0.829 | 0.057 |
| ig:llm/llm:sbert+rnorm=minmax | 0.835 | 0.549 | 0.346 | 0.902 | 0.913 | 0.857 | 0.057 |
| ig:llm/llm:sbert+repair=1 | 0.787 | 0.549 | 0.329 | 0.868 | 0.894 | 0.829 | 0.057 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.834 | 0.549 | 0.346 | 0.902 | 0.913 | 0.857 | 0.057 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:sbert | 0.808 | 0.525 | 0.845 | 0.719 |
| ig:llm/llm:sbert | 0.789 | 0.544 | 0.884 | 0.812 |
| ig:llm/llm:sbert+rnorm=minmax | 0.840 | 0.544 | 0.905 | 0.844 |
| ig:llm/llm:sbert+repair=1 | 0.788 | 0.544 | 0.884 | 0.812 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.839 | 0.544 | 0.905 | 0.844 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:sbert | 0.294 | 0.777 | 0.886 |
| ig:llm/llm:sbert | 0.341 | 0.798 | 0.868 |
| ig:llm/llm:sbert+rnorm=minmax | 0.351 | 0.793 | 0.902 |
| ig:llm/llm:sbert+repair=1 | 0.341 | 0.798 | 0.868 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.351 | 0.793 | 0.902 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | aggregate (n=3) | compare (n=10) | explain (n=7) | monitor (n=5) | predict (n=8) |
|---|---|---|---|---|---|
| ctx:sbert | 0.986 | 0.825 | 0.831 | 0.716 | 0.771 |
| ig:llm/llm:sbert | 0.919 | 0.851 | 0.832 | 0.716 | 0.680 |
| ig:llm/llm:sbert+rnorm=minmax | 0.984 | 0.872 | 0.849 | 0.716 | 0.817 |
| ig:llm/llm:sbert+repair=1 | 0.919 | 0.851 | 0.828 | 0.711 | 0.680 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.984 | 0.872 | 0.846 | 0.711 | 0.817 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:sbert | 0.842 |
| ig:llm/llm:sbert | 0.827 |
| ig:llm/llm:sbert+rnorm=minmax | 0.826 |
| ig:llm/llm:sbert+repair=1 | 0.827 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.826 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:llm/llm:sbert | 0.778 | 0.779 | 0.920 | 0.639 | 0.594 | 0.594 | 0.578 | 0.406 | 0.488 | 0.744 |
| ig:llm/llm:sbert+rnorm=minmax | 0.778 | 0.779 | 0.920 | 0.639 | 0.594 | 0.594 | 0.578 | 0.406 | 0.488 | 0.744 |
| ig:llm/llm:sbert+repair=1 | 0.833 | 0.790 | 0.889 | 0.667 | 0.625 | 0.625 | 0.609 | 0.375 | 0.489 | 0.739 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.833 | 0.790 | 0.889 | 0.667 | 0.625 | 0.625 | 0.609 | 0.375 | 0.489 | 0.739 |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:sbert | – | 132.6 / 119.6 / 137.5 | – | – | – | – | 132.7 / 119.7 / 137.6 | 4.778 |
| ig:llm/llm:sbert | 5.1 / 5.0 / 8.0 | 138.2 / 137.2 / 148.7 | 1.6 / 1.2 / 3.2 | 111.6 / 23.0 / 69.3 | 1333.2 / 76.9 / 6148.3 | 0.2 / 0.1 / 0.5 | 1453.0 / 108.7 / 6673.3 | 20.221 |
| ig:llm/llm:sbert+rnorm=minmax | 5.2 / 4.8 / 8.7 | 137.1 / 136.3 / 147.0 | 1.6 / 1.4 / 3.8 | 74.7 / 25.3 / 382.7 | 1375.4 / 97.7 / 6048.0 | 0.2 / 0.2 / 0.5 | 1458.5 / 217.4 / 6392.9 | 21.606 |
| ig:llm/llm:sbert+repair=1 | 6.8 / 5.8 / 13.8 | 82.8 / 81.6 / 88.6 | 2.1 / 1.2 / 5.8 | 17.0 / 19.7 / 41.3 | 1047.5 / 80.5 / 5009.4 | 0.2 / 0.1 / 0.6 | 1074.4 / 108.6 / 5051.9 | 15.317 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 7.4 / 6.9 / 15.5 | 90.1 / 87.9 / 104.4 | 1.8 / 1.5 / 5.3 | 17.2 / 20.0 / 42.4 | 1374.3 / 93.3 / 7606.6 | 0.2 / 0.1 / 0.6 | 1402.1 / 124.6 / 7649.4 | 18.625 |

Context index build (one-off, ms): sbert: 17133 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | ndcg@10 | +0.025 | [+0.001, +0.052] | 0.070 | 14/9 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | mrr | +0.055 | [+0.000, +0.119] | 0.127 | 4/1 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | useful@1 | +0.114 | [+0.029, +0.229] | 0.127 | 4/0 |
| ig:llm/llm:sbert+rnorm=minmax | ctx:sbert | ndcg@10 | +0.027 | [+0.003, +0.053] | 0.055 | 13/7 |
| ig:llm/llm:sbert+rnorm=minmax | ctx:sbert | mrr | +0.055 | [+0.000, +0.119] | 0.127 | 4/1 |
| ig:llm/llm:sbert+rnorm=minmax | ctx:sbert | useful@1 | +0.114 | [+0.029, +0.229] | 0.127 | 4/0 |
| ig:llm/llm:sbert | ctx:sbert | ndcg@10 | -0.018 | [-0.071, +0.025] | 0.573 | 9/13 |
| ig:llm/llm:sbert | ctx:sbert | mrr | +0.036 | [-0.017, +0.098] | 0.256 | 3/1 |
| ig:llm/llm:sbert | ctx:sbert | useful@1 | +0.086 | [+0.000, +0.200] | 0.256 | 3/0 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | ndcg@10 | -0.020 | [-0.072, +0.022] | 0.537 | 10/15 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | mrr | +0.036 | [-0.017, +0.098] | 0.256 | 3/1 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | useful@1 | +0.086 | [+0.000, +0.200] | 0.256 | 3/0 |
