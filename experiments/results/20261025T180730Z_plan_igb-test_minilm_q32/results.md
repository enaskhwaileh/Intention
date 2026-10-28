# IGBench results (20261025T180730Z_plan_igb-test_minilm_q32)

Benchmark `igbench-v1-test` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:sbert | 0.690 | 0.340 | 0.270 | 0.780 | 0.814 | 0.700 | 0.150 |
| ig:llm/llm:sbert | 0.699 | 0.430 | 0.280 | 0.801 | 0.852 | 0.750 | 0.050 |
| ig:llm/llm:sbert+repair=1 | 0.741 | 0.490 | 0.300 | 0.846 | 0.877 | 0.800 | 0.050 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.740 | 0.420 | 0.285 | 0.821 | 0.910 | 0.850 | 0.050 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.654 | 0.340 | 0.250 | 0.736 | 0.734 | 0.600 | 0.250 |
| rerank:llm:sbert | 0.823 | 0.550 | 0.310 | 0.873 | 1.000 | 1.000 | 0.000 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:sbert | 0.680 | 0.316 | 0.804 | 0.684 |
| ig:llm/llm:sbert | 0.710 | 0.432 | 0.870 | 0.789 |
| ig:llm/llm:sbert+repair=1 | 0.755 | 0.495 | 0.896 | 0.842 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.753 | 0.421 | 0.932 | 0.895 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.663 | 0.337 | 0.747 | 0.632 |
| rerank:llm:sbert | 0.820 | 0.537 | 1.000 | 1.000 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:sbert | 0.352 | 0.591 | 0.780 |
| ig:llm/llm:sbert | 0.312 | 0.701 | 0.801 |
| ig:llm/llm:sbert+repair=1 | 0.324 | 0.768 | 0.846 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.399 | 0.676 | 0.821 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.327 | 0.584 | 0.736 |
| rerank:llm:sbert | 0.445 | 0.830 | 0.873 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | compare (n=8) | explain (n=3) | monitor (n=5) | predict (n=4) |
|---|---|---|---|---|
| ctx:sbert | 0.665 | 0.675 | 0.683 | 0.756 |
| ig:llm/llm:sbert | 0.701 | 0.675 | 0.697 | 0.825 |
| ig:llm/llm:sbert+repair=1 | 0.758 | 0.815 | 0.691 | 0.825 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.750 | 0.714 | 0.734 | 0.856 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.673 | 0.681 | 0.614 | 0.756 |
| rerank:llm:sbert | 0.839 | 0.780 | 0.800 | 0.865 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:sbert | 0.824 |
| ig:llm/llm:sbert | 0.869 |
| ig:llm/llm:sbert+repair=1 | 0.919 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.896 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.826 |
| rerank:llm:sbert | 0.892 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:llm/llm:sbert | 0.762 | 0.931 | 0.911 | 0.714 | 0.684 | 0.684 | 0.623 | 0.316 | 0.673 | 0.805 |
| ig:llm/llm:sbert+repair=1 | 0.952 | 0.840 | 0.930 | 0.905 | 0.895 | 0.895 | 0.728 | 0.105 | 0.708 | 0.793 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.952 | 0.840 | 0.930 | 0.905 | 0.895 | 0.895 | 0.728 | 0.105 | 0.708 | 0.793 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.952 | 0.840 | 0.930 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | – | – |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:sbert | – | 89.4 / 68.4 / 81.5 | – | – | – | – | 89.5 / 68.4 / 81.5 | 1.879 |
| ig:llm/llm:sbert | 4.3 / 4.1 / 5.9 | 71.8 / 70.2 / 76.8 | 2.0 / 1.2 / 6.3 | 18.2 / 20.9 / 35.7 | 142.3 / 88.2 / 293.5 | 0.1 / 0.1 / 0.1 | 167.7 / 130.8 / 325.6 | 2.963 |
| ig:llm/llm:sbert+repair=1 | 5.4 / 4.3 / 9.8 | 72.4 / 69.6 / 77.9 | 2.0 / 1.1 / 5.6 | 17.3 / 19.7 / 25.7 | 261.4 / 118.0 / 797.4 | 0.1 / 0.1 / 0.1 | 287.2 / 150.6 / 829.1 | 4.754 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 7.2 / 3.5 / 16.6 | 96.5 / 95.0 / 114.1 | 1.9 / 1.0 / 5.6 | 62.5 / 20.7 / 330.7 | 275.2 / 118.2 / 835.5 | 0.1 / 0.1 / 0.1 | 347.9 / 230.6 / 883.4 | 5.203 |
| ig:llm/llm:sbert+repair=1+align=0 | 6.2 / 5.8 / 9.2 | 72.6 / 70.5 / 78.3 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.4 / 0.4 / 0.6 | 6.7 / 6.1 / 9.7 | 1.947 |
| rerank:llm:sbert | – | 644.4 / 824.4 / 874.5 | – | – | – | – | 46461.6 / 49056.3 / 65454.9 | 74.743 |

Context index build (one-off, ms): sbert: 10481 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:llm/llm:sbert+repair=1+align=0 | ctx:sbert | ndcg@10 | -0.032 | [-0.092, +0.010] | 0.334 | 5/9 |
| ig:llm/llm:sbert+repair=1+align=0 | ctx:sbert | mrr | -0.080 | [-0.185, +0.000] | 0.251 | 0/3 |
| ig:llm/llm:sbert+repair=1+align=0 | ctx:sbert | useful@1 | -0.100 | [-0.250, +0.000] | 0.501 | 0/2 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | ndcg@10 | +0.050 | [-0.015, +0.106] | 0.135 | 11/5 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | mrr | +0.096 | [-0.017, +0.217] | 0.244 | 4/1 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | useful@1 | +0.150 | [-0.050, +0.350] | 0.370 | 4/1 |
| ig:llm/llm:sbert | ctx:sbert | ndcg@10 | +0.011 | [-0.068, +0.082] | 0.791 | 11/3 |
| ig:llm/llm:sbert | ctx:sbert | mrr | +0.037 | [-0.108, +0.192] | 0.705 | 4/3 |
| ig:llm/llm:sbert | ctx:sbert | useful@1 | +0.050 | [-0.200, +0.300] | 1.000 | 4/3 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | ndcg@10 | +0.051 | [-0.045, +0.141] | 0.309 | 14/4 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | mrr | +0.062 | [-0.092, +0.225] | 0.519 | 5/3 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | useful@1 | +0.100 | [-0.150, +0.400] | 0.725 | 5/3 |
