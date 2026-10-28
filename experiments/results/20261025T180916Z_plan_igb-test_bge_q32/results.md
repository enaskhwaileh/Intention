# IGBench results (20261025T180916Z_plan_igb-test_bge_q32)

Benchmark `igbench-v1-test` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:sbert | 0.808 | 0.510 | 0.305 | 0.879 | 0.975 | 0.950 | 0.000 |
| ig:llm/llm:sbert | 0.719 | 0.520 | 0.305 | 0.823 | 0.884 | 0.850 | 0.000 |
| ig:llm/llm:sbert+repair=1 | 0.721 | 0.520 | 0.315 | 0.843 | 0.884 | 0.850 | 0.000 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.817 | 0.540 | 0.325 | 0.896 | 0.967 | 0.950 | 0.000 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.798 | 0.530 | 0.305 | 0.871 | 0.942 | 0.900 | 0.050 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:sbert | 0.804 | 0.495 | 0.974 | 0.947 |
| ig:llm/llm:sbert | 0.720 | 0.516 | 0.878 | 0.842 |
| ig:llm/llm:sbert+repair=1 | 0.721 | 0.516 | 0.878 | 0.842 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.823 | 0.537 | 0.965 | 0.947 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.803 | 0.526 | 0.939 | 0.895 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:sbert | 0.437 | 0.797 | 0.879 |
| ig:llm/llm:sbert | 0.337 | 0.757 | 0.823 |
| ig:llm/llm:sbert+repair=1 | 0.337 | 0.757 | 0.843 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.437 | 0.820 | 0.896 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.412 | 0.818 | 0.871 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | compare (n=8) | explain (n=3) | monitor (n=5) | predict (n=4) |
|---|---|---|---|---|
| ctx:sbert | 0.794 | 0.763 | 0.799 | 0.867 |
| ig:llm/llm:sbert | 0.726 | 0.763 | 0.608 | 0.829 |
| ig:llm/llm:sbert+repair=1 | 0.725 | 0.790 | 0.599 | 0.829 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.783 | 0.780 | 0.826 | 0.921 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.766 | 0.761 | 0.796 | 0.911 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:sbert | 0.871 |
| ig:llm/llm:sbert | 0.897 |
| ig:llm/llm:sbert+repair=1 | 0.896 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.878 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.868 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:llm/llm:sbert | 0.762 | 0.931 | 0.911 | 0.714 | 0.684 | 0.684 | 0.623 | 0.316 | 0.667 | 0.809 |
| ig:llm/llm:sbert+repair=1 | 0.952 | 0.840 | 0.930 | 0.905 | 0.895 | 0.895 | 0.728 | 0.105 | 0.671 | 0.797 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.952 | 0.840 | 0.930 | 0.905 | 0.895 | 0.895 | 0.728 | 0.105 | 0.671 | 0.797 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.952 | 0.840 | 0.930 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | – | – |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:sbert | – | 101.5 / 79.5 / 97.0 | – | – | – | – | 101.6 / 79.5 / 97.1 | 2.133 |
| ig:llm/llm:sbert | 4.8 / 4.3 / 7.1 | 80.0 / 77.9 / 87.3 | 2.1 / 1.4 / 5.7 | 21.5 / 21.9 / 44.4 | 190.2 / 110.7 / 407.4 | 0.1 / 0.1 / 0.2 | 219.7 / 147.0 / 436.0 | 3.731 |
| ig:llm/llm:sbert+repair=1 | 5.8 / 5.1 / 9.6 | 79.2 / 77.5 / 86.1 | 2.1 / 1.3 / 5.6 | 46.4 / 19.6 / 40.9 | 302.1 / 132.6 / 921.1 | 0.1 / 0.1 / 0.1 | 357.6 / 164.1 / 959.8 | 4.96 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 6.0 / 5.3 / 9.7 | 80.0 / 79.4 / 82.8 | 2.0 / 1.0 / 5.7 | 63.8 / 21.5 / 321.4 | 353.1 / 136.1 / 1100.4 | 0.2 / 0.1 / 0.1 | 426.1 / 213.3 / 1130.7 | 5.023 |
| ig:llm/llm:sbert+repair=1+align=0 | 5.4 / 5.0 / 8.7 | 79.4 / 78.6 / 84.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.4 / 0.4 / 0.7 | 5.9 / 5.5 / 9.1 | 2.08 |

Context index build (one-off, ms): sbert: 11159 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:llm/llm:sbert+repair=1+align=0 | ctx:sbert | ndcg@10 | -0.012 | [-0.041, +0.014] | 0.348 | 6/8 |
| ig:llm/llm:sbert+repair=1+align=0 | ctx:sbert | mrr | -0.033 | [-0.100, +0.000] | 0.500 | 0/2 |
| ig:llm/llm:sbert+repair=1+align=0 | ctx:sbert | useful@1 | -0.050 | [-0.150, +0.000] | 1.000 | 0/1 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | ndcg@10 | +0.006 | [-0.029, +0.042] | 0.751 | 8/8 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | mrr | -0.008 | [-0.025, +0.000] | 1.000 | 0/1 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | useful@1 | +0.000 | [+0.000, +0.000] | 1.000 | 0/0 |
| ig:llm/llm:sbert | ctx:sbert | ndcg@10 | -0.087 | [-0.182, -0.015] | 0.034 | 6/9 |
| ig:llm/llm:sbert | ctx:sbert | mrr | -0.091 | [-0.220, +0.000] | 0.247 | 0/3 |
| ig:llm/llm:sbert | ctx:sbert | useful@1 | -0.100 | [-0.250, +0.000] | 0.499 | 0/2 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | ndcg@10 | -0.086 | [-0.181, -0.009] | 0.059 | 7/12 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | mrr | -0.091 | [-0.220, +0.000] | 0.247 | 0/3 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | useful@1 | -0.100 | [-0.250, +0.000] | 0.499 | 0/2 |
