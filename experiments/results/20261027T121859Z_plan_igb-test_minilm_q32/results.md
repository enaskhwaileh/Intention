# IGBench results (20261027T121859Z_plan_igb-test_minilm_q32)

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
| rerank:llmig:sbert | 0.740 | 0.420 | 0.285 | 0.821 | 0.910 | 0.850 | 0.050 |
| rerank:llmgold:sbert | 0.769 | 0.470 | 0.310 | 0.869 | 0.917 | 0.850 | 0.000 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:sbert | 0.680 | 0.316 | 0.804 | 0.684 |
| ig:llm/llm:sbert | 0.710 | 0.432 | 0.870 | 0.789 |
| ig:llm/llm:sbert+repair=1 | 0.755 | 0.495 | 0.896 | 0.842 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.753 | 0.421 | 0.932 | 0.895 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.663 | 0.337 | 0.747 | 0.632 |
| rerank:llm:sbert | 0.820 | 0.537 | 1.000 | 1.000 |
| rerank:llmig:sbert | 0.753 | 0.421 | 0.932 | 0.895 |
| rerank:llmgold:sbert | 0.763 | 0.453 | 0.912 | 0.842 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:sbert | 0.352 | 0.591 | 0.780 |
| ig:llm/llm:sbert | 0.312 | 0.701 | 0.801 |
| ig:llm/llm:sbert+repair=1 | 0.324 | 0.768 | 0.846 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.399 | 0.676 | 0.821 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.327 | 0.584 | 0.736 |
| rerank:llm:sbert | 0.445 | 0.830 | 0.873 |
| rerank:llmig:sbert | 0.399 | 0.676 | 0.821 |
| rerank:llmgold:sbert | 0.362 | 0.727 | 0.869 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | compare (n=8) | explain (n=3) | monitor (n=5) | predict (n=4) |
|---|---|---|---|---|
| ctx:sbert | 0.665 | 0.675 | 0.683 | 0.756 |
| ig:llm/llm:sbert | 0.701 | 0.675 | 0.697 | 0.825 |
| ig:llm/llm:sbert+repair=1 | 0.758 | 0.815 | 0.691 | 0.825 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.750 | 0.714 | 0.734 | 0.856 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.673 | 0.681 | 0.614 | 0.756 |
| rerank:llm:sbert | 0.839 | 0.780 | 0.800 | 0.865 |
| rerank:llmig:sbert | 0.750 | 0.714 | 0.734 | 0.856 |
| rerank:llmgold:sbert | 0.740 | 0.759 | 0.747 | 0.871 |

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
| rerank:llmig:sbert | 0.896 |
| rerank:llmgold:sbert | 0.916 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:llm/llm:sbert | 0.762 | 0.931 | 0.911 | 0.714 | 0.684 | 0.684 | 0.623 | 0.316 | 0.673 | 0.805 |
| ig:llm/llm:sbert+repair=1 | 0.952 | 0.840 | 0.930 | 0.905 | 0.895 | 0.895 | 0.728 | 0.105 | 0.708 | 0.793 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.952 | 0.840 | 0.930 | 0.905 | 0.895 | 0.895 | 0.728 | 0.105 | 0.708 | 0.793 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.952 | 0.840 | 0.930 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | – | – |
| rerank:llmig:sbert | 0.952 | 0.840 | 0.930 | 0.905 | 0.895 | 0.895 | 0.728 | 0.000 | – | – |
| rerank:llmgold:sbert | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | – | – |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:sbert | – | 121.3 / 97.5 / 106.9 | – | – | – | – | 121.4 / 97.6 / 107.0 | 2.549 |
| ig:llm/llm:sbert | 4.5 / 4.4 / 6.3 | 93.2 / 93.0 / 103.6 | 2.1 / 1.4 / 5.9 | 18.4 / 23.5 / 34.7 | 176.4 / 112.2 / 380.2 | 0.2 / 0.2 / 0.2 | 202.7 / 154.0 / 410.0 | 3.903 |
| ig:llm/llm:sbert+repair=1 | 6.9 / 6.1 / 11.7 | 100.3 / 99.8 / 108.5 | 2.3 / 1.6 / 5.6 | 20.9 / 23.7 / 31.4 | 322.6 / 164.7 / 973.3 | 0.2 / 0.2 / 0.3 | 354.6 / 198.2 / 1019.0 | 5.81 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 6.5 / 5.8 / 11.0 | 87.2 / 83.9 / 101.5 | 2.7 / 1.6 / 6.6 | 101.1 / 24.6 / 573.6 | 358.8 / 145.2 / 1001.9 | 0.2 / 0.1 / 0.3 | 470.8 / 272.6 / 1030.8 | 5.926 |
| ig:llm/llm:sbert+repair=1+align=0 | 6.6 / 5.9 / 12.0 | 98.8 / 98.0 / 105.8 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.5 / 0.5 / 0.8 | 7.2 / 6.5 / 12.5 | 2.741 |
| rerank:llm:sbert | – | 982.8 / 1094.0 / 1330.6 | – | – | – | – | 993.0 / 1121.9 / 1342.3 | 1.514 |
| rerank:llmig:sbert | 23.8 / 22.0 / 51.8 | 777.2 / 962.7 / 1093.1 | 39.8 / 31.0 / 106.3 | 703.6 / 291.8 / 1537.0 | 3264.9 / 1047.1 / 8104.6 | 0.3 / 0.2 / 0.3 | 34875.6 / 33323.6 / 40695.9 | 62.564 |
| rerank:llmgold:sbert | 0.2 / 0.2 / 0.3 | 1303.2 / 1734.5 / 1865.0 | 0.8 / 0.3 / 0.8 | 662.6 / 986.6 / 1139.8 | 3629.3 / 3909.1 / 7424.7 | 0.2 / 0.2 / 0.3 | 35649.6 / 36804.8 / 40293.2 | 66.694 |

Context index build (one-off, ms): sbert: 14533 (cached)

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
