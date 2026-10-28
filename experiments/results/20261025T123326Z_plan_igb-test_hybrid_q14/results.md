# IGBench results (20261025T123326Z_plan_igb-test_hybrid_q14)

Benchmark `igbench-v1-test` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:hybrid | 0.845 | 0.560 | 0.335 | 0.907 | 0.950 | 0.900 | 0.050 |
| ig:llm/llm:hybrid | 0.819 | 0.540 | 0.335 | 0.913 | 0.900 | 0.800 | 0.100 |
| ig:llm/llm:hybrid+repair=1 | 0.822 | 0.550 | 0.340 | 0.921 | 0.925 | 0.850 | 0.050 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | 0.862 | 0.540 | 0.345 | 0.926 | 0.975 | 0.950 | 0.050 |
| ig:llm/llm:hybrid+repair=1+align=0 | 0.835 | 0.540 | 0.335 | 0.905 | 0.917 | 0.850 | 0.100 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:hybrid | 0.839 | 0.547 | 0.947 | 0.895 |
| ig:llm/llm:hybrid | 0.826 | 0.537 | 0.921 | 0.842 |
| ig:llm/llm:hybrid+repair=1 | 0.829 | 0.547 | 0.947 | 0.895 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | 0.872 | 0.537 | 1.000 | 1.000 |
| ig:llm/llm:hybrid+repair=1+align=0 | 0.843 | 0.537 | 0.939 | 0.895 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:hybrid | 0.424 | 0.833 | 0.907 |
| ig:llm/llm:hybrid | 0.362 | 0.812 | 0.913 |
| ig:llm/llm:hybrid+repair=1 | 0.333 | 0.820 | 0.921 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | 0.432 | 0.810 | 0.926 |
| ig:llm/llm:hybrid+repair=1+align=0 | 0.412 | 0.811 | 0.905 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | compare (n=8) | explain (n=3) | monitor (n=5) | predict (n=4) |
|---|---|---|---|---|
| ctx:hybrid | 0.847 | 0.763 | 0.809 | 0.918 |
| ig:llm/llm:hybrid | 0.793 | 0.782 | 0.820 | 0.906 |
| ig:llm/llm:hybrid+repair=1 | 0.822 | 0.782 | 0.785 | 0.906 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | 0.867 | 0.801 | 0.854 | 0.917 |
| ig:llm/llm:hybrid+repair=1+align=0 | 0.826 | 0.802 | 0.800 | 0.928 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:hybrid | 0.860 |
| ig:llm/llm:hybrid | 0.879 |
| ig:llm/llm:hybrid+repair=1 | 0.882 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | 0.882 |
| ig:llm/llm:hybrid+repair=1+align=0 | 0.860 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:llm/llm:hybrid | 0.857 | 0.774 | 0.980 | 0.714 | 0.684 | 0.684 | 0.588 | 0.316 | 0.594 | 0.775 |
| ig:llm/llm:hybrid+repair=1 | 1.000 | 0.788 | 0.933 | 0.905 | 0.895 | 0.895 | 0.781 | 0.105 | 0.592 | 0.692 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | 1.000 | 0.788 | 0.933 | 0.905 | 0.895 | 0.895 | 0.781 | 0.105 | 0.592 | 0.692 |
| ig:llm/llm:hybrid+repair=1+align=0 | 1.000 | 0.788 | 0.933 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | – | – |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:hybrid | – | 104.0 / 84.8 / 91.0 | – | – | – | – | 104.1 / 85.0 / 91.1 | 2.186 |
| ig:llm/llm:hybrid | 4.6 / 4.7 / 6.1 | 84.9 / 85.3 / 89.5 | 2.1 / 1.1 / 6.2 | 14.7 / 18.4 / 28.9 | 196.9 / 93.9 / 555.5 | 0.2 / 0.1 / 0.4 | 219.3 / 128.2 / 579.6 | 4.823 |
| ig:llm/llm:hybrid+repair=1 | 2.2 / 1.9 / 3.7 | 81.8 / 82.1 / 96.1 | 1.9 / 1.3 / 4.2 | 56.0 / 27.3 / 42.2 | 324.8 / 157.5 / 916.0 | 0.1 / 0.1 / 0.2 | 386.1 / 230.9 / 948.2 | 6.006 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | 5.5 / 4.4 / 10.4 | 105.7 / 103.1 / 118.7 | 2.5 / 1.7 / 4.3 | 29.6 / 32.7 / 49.6 | 336.5 / 214.4 / 1002.0 | 0.2 / 0.2 / 0.2 | 375.6 / 275.9 / 1041.6 | 5.925 |
| ig:llm/llm:hybrid+repair=1+align=0 | 4.5 / 3.7 / 7.3 | 91.5 / 92.6 / 98.8 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 1.0 / 0.8 / 1.2 | 5.5 / 4.9 / 8.2 | 2.434 |

Context index build (one-off, ms): hybrid: 9693 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:llm/llm:hybrid+repair=1+align=0 | ctx:hybrid | ndcg@10 | -0.016 | [-0.050, +0.009] | 0.371 | 5/7 |
| ig:llm/llm:hybrid+repair=1+align=0 | ctx:hybrid | mrr | -0.033 | [-0.092, +0.000] | 0.501 | 0/2 |
| ig:llm/llm:hybrid+repair=1+align=0 | ctx:hybrid | useful@1 | -0.050 | [-0.150, +0.000] | 1.000 | 0/1 |
| ig:llm/llm:hybrid+repair=1 | ctx:hybrid | ndcg@10 | -0.028 | [-0.086, +0.027] | 0.361 | 8/10 |
| ig:llm/llm:hybrid+repair=1 | ctx:hybrid | mrr | -0.025 | [-0.125, +0.075] | 1.000 | 2/3 |
| ig:llm/llm:hybrid+repair=1 | ctx:hybrid | useful@1 | -0.050 | [-0.250, +0.150] | 1.000 | 2/3 |
| ig:llm/llm:hybrid | ctx:hybrid | ndcg@10 | -0.031 | [-0.076, +0.011] | 0.207 | 6/9 |
| ig:llm/llm:hybrid | ctx:hybrid | mrr | -0.050 | [-0.125, +0.000] | 0.500 | 0/2 |
| ig:llm/llm:hybrid | ctx:hybrid | useful@1 | -0.100 | [-0.250, +0.000] | 0.500 | 0/2 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | ctx:hybrid | ndcg@10 | +0.010 | [-0.034, +0.047] | 0.642 | 6/8 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | ctx:hybrid | mrr | +0.025 | [-0.050, +0.100] | 1.000 | 2/1 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | ctx:hybrid | useful@1 | +0.050 | [-0.100, +0.200] | 1.000 | 2/1 |
