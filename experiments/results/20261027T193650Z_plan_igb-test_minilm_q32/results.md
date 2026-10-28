# IGBench results (20261027T193650Z_plan_igb-test_minilm_q32)

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
| rerank:llmig:sbert | 0.788 | 0.530 | 0.320 | 0.885 | 0.960 | 0.950 | 0.000 |
| rerank:llmgold:sbert | 0.802 | 0.520 | 0.330 | 0.910 | 0.958 | 0.950 | 0.000 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:sbert | 0.680 | 0.316 | 0.804 | 0.684 |
| ig:llm/llm:sbert | 0.710 | 0.432 | 0.870 | 0.789 |
| ig:llm/llm:sbert+repair=1 | 0.755 | 0.495 | 0.896 | 0.842 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.753 | 0.421 | 0.932 | 0.895 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.663 | 0.337 | 0.747 | 0.632 |
| rerank:llm:sbert | 0.820 | 0.537 | 1.000 | 1.000 |
| rerank:llmig:sbert | 0.798 | 0.537 | 0.958 | 0.947 |
| rerank:llmgold:sbert | 0.797 | 0.505 | 0.956 | 0.947 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:sbert | 0.352 | 0.591 | 0.780 |
| ig:llm/llm:sbert | 0.312 | 0.701 | 0.801 |
| ig:llm/llm:sbert+repair=1 | 0.324 | 0.768 | 0.846 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.399 | 0.676 | 0.821 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.327 | 0.584 | 0.736 |
| rerank:llm:sbert | 0.445 | 0.830 | 0.873 |
| rerank:llmig:sbert | 0.395 | 0.794 | 0.885 |
| rerank:llmgold:sbert | 0.395 | 0.760 | 0.910 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | compare (n=8) | explain (n=3) | monitor (n=5) | predict (n=4) |
|---|---|---|---|---|
| ctx:sbert | 0.665 | 0.675 | 0.683 | 0.756 |
| ig:llm/llm:sbert | 0.701 | 0.675 | 0.697 | 0.825 |
| ig:llm/llm:sbert+repair=1 | 0.758 | 0.815 | 0.691 | 0.825 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.750 | 0.714 | 0.734 | 0.856 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.673 | 0.681 | 0.614 | 0.756 |
| rerank:llm:sbert | 0.839 | 0.780 | 0.800 | 0.865 |
| rerank:llmig:sbert | 0.802 | 0.844 | 0.743 | 0.859 |
| rerank:llmgold:sbert | 0.789 | 0.803 | 0.758 | 0.893 |

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
| rerank:llmig:sbert | 0.930 |
| rerank:llmgold:sbert | 0.942 |

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
| ctx:sbert | – | 94.6 / 74.4 / 82.0 | – | – | – | – | 94.6 / 74.4 / 82.0 | 1.987 |
| ig:llm/llm:sbert | 2.5 / 2.5 / 3.0 | 74.6 / 74.3 / 76.8 | 1.3 / 1.1 / 3.5 | 15.7 / 20.3 / 32.5 | 137.9 / 85.4 / 289.7 | 0.1 / 0.1 / 0.1 | 158.2 / 112.2 / 317.2 | 2.755 |
| ig:llm/llm:sbert+repair=1 | 3.1 / 2.6 / 5.4 | 79.7 / 80.7 / 82.6 | 1.4 / 1.0 / 2.7 | 30.5 / 18.5 / 25.5 | 245.8 / 108.1 / 810.8 | 0.1 / 0.1 / 0.1 | 281.6 / 151.5 / 846.7 | 4.21 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 2.3 / 2.1 / 4.2 | 72.7 / 71.4 / 77.0 | 1.3 / 1.0 / 2.5 | 45.9 / 19.0 / 27.7 | 274.2 / 108.5 / 827.9 | 0.1 / 0.1 / 0.1 | 324.5 / 151.9 / 862.1 | 4.363 |
| ig:llm/llm:sbert+repair=1+align=0 | 3.1 / 2.4 / 5.2 | 76.2 / 73.8 / 81.8 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.2 / 0.2 / 0.4 | 3.3 / 2.7 / 5.4 | 1.759 |
| rerank:llm:sbert | – | 158.8 / 145.3 / 207.0 | – | – | – | – | 162.0 / 148.5 / 208.1 | 0.899 |
| rerank:llmig:sbert | 2.9 / 1.6 / 5.8 | 115.5 / 96.6 / 203.9 | 1.8 / 1.1 / 1.9 | 19.7 / 21.8 / 30.0 | 270.4 / 123.0 / 831.2 | 0.1 / 0.1 / 0.1 | 32874.4 / 34510.3 / 42865.5 | 186.821 |
| rerank:llmgold:sbert | 0.2 / 0.2 / 0.2 | 124.6 / 98.8 / 212.0 | 0.2 / 0.2 / 0.3 | 77.9 / 23.8 / 264.2 | 276.6 / 199.5 / 749.9 | 0.1 / 0.1 / 0.1 | 33431.8 / 33265.9 / 43471.3 | 191.976 |

Context index build (one-off, ms): sbert: 10220 (cached)

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
