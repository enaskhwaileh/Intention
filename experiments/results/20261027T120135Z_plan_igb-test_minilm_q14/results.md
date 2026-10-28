# IGBench results (20261027T120135Z_plan_igb-test_minilm_q14)

Benchmark `igbench-v1-test` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:sbert | 0.690 | 0.340 | 0.270 | 0.780 | 0.814 | 0.700 | 0.150 |
| ig:llm/llm:sbert | 0.744 | 0.460 | 0.300 | 0.846 | 0.910 | 0.850 | 0.050 |
| ig:llm/llm:sbert+repair=1 | 0.742 | 0.490 | 0.310 | 0.863 | 0.917 | 0.850 | 0.050 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.743 | 0.460 | 0.290 | 0.830 | 0.917 | 0.850 | 0.050 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.654 | 0.340 | 0.250 | 0.736 | 0.734 | 0.600 | 0.250 |
| rerank:llm:sbert | 0.809 | 0.520 | 0.305 | 0.861 | 0.975 | 0.950 | 0.050 |
| rerank:llmig:sbert | 0.784 | 0.490 | 0.315 | 0.875 | 0.960 | 0.950 | 0.000 |
| rerank:llmgold:sbert | 0.792 | 0.510 | 0.325 | 0.900 | 0.958 | 0.950 | 0.000 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:sbert | 0.680 | 0.316 | 0.804 | 0.684 |
| ig:llm/llm:sbert | 0.758 | 0.463 | 0.932 | 0.895 |
| ig:llm/llm:sbert+repair=1 | 0.756 | 0.495 | 0.939 | 0.895 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.756 | 0.463 | 0.939 | 0.895 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.663 | 0.337 | 0.747 | 0.632 |
| rerank:llm:sbert | 0.804 | 0.505 | 0.974 | 0.947 |
| rerank:llmig:sbert | 0.794 | 0.495 | 0.958 | 0.947 |
| rerank:llmgold:sbert | 0.786 | 0.495 | 0.956 | 0.947 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:sbert | 0.352 | 0.591 | 0.780 |
| ig:llm/llm:sbert | 0.374 | 0.731 | 0.846 |
| ig:llm/llm:sbert+repair=1 | 0.333 | 0.760 | 0.863 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.399 | 0.712 | 0.830 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.327 | 0.584 | 0.736 |
| rerank:llm:sbert | 0.432 | 0.803 | 0.861 |
| rerank:llmig:sbert | 0.395 | 0.760 | 0.875 |
| rerank:llmgold:sbert | 0.395 | 0.750 | 0.900 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | compare (n=8) | explain (n=3) | monitor (n=5) | predict (n=4) |
|---|---|---|---|---|
| ctx:sbert | 0.665 | 0.675 | 0.683 | 0.756 |
| ig:llm/llm:sbert | 0.758 | 0.743 | 0.747 | 0.825 |
| ig:llm/llm:sbert+repair=1 | 0.806 | 0.743 | 0.662 | 0.825 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.766 | 0.693 | 0.732 | 0.856 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.673 | 0.680 | 0.614 | 0.756 |
| rerank:llm:sbert | 0.838 | 0.773 | 0.794 | 0.822 |
| rerank:llmig:sbert | 0.789 | 0.757 | 0.804 | 0.855 |
| rerank:llmgold:sbert | 0.783 | 0.753 | 0.773 | 0.872 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:sbert | 0.824 |
| ig:llm/llm:sbert | 0.938 |
| ig:llm/llm:sbert+repair=1 | 0.942 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.905 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.829 |
| rerank:llm:sbert | 0.890 |
| rerank:llmig:sbert | 0.942 |
| rerank:llmgold:sbert | 0.942 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:llm/llm:sbert | 0.857 | 0.774 | 0.980 | 0.714 | 0.684 | 0.684 | 0.588 | 0.316 | 0.623 | 0.775 |
| ig:llm/llm:sbert+repair=1 | 1.000 | 0.788 | 0.933 | 0.905 | 0.895 | 0.895 | 0.781 | 0.105 | 0.616 | 0.703 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 1.000 | 0.788 | 0.933 | 0.905 | 0.895 | 0.895 | 0.781 | 0.105 | 0.616 | 0.703 |
| ig:llm/llm:sbert+repair=1+align=0 | 1.000 | 0.788 | 0.933 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | – | – |
| rerank:llmig:sbert | 1.000 | 0.788 | 0.933 | 0.905 | 0.895 | 0.895 | 0.781 | 0.000 | – | – |
| rerank:llmgold:sbert | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | – | – |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:sbert | – | 97.1 / 78.0 / 86.5 | – | – | – | – | 97.1 / 78.0 / 86.6 | 2.04 |
| ig:llm/llm:sbert | 4.3 / 4.6 / 5.9 | 76.8 / 76.6 / 80.6 | 1.8 / 1.3 / 4.1 | 17.2 / 21.3 / 35.7 | 163.3 / 80.1 / 291.8 | 0.1 / 0.1 / 0.2 | 187.6 / 108.6 / 320.9 | 4.315 |
| ig:llm/llm:sbert+repair=1 | 5.6 / 5.5 / 9.2 | 69.2 / 69.5 / 72.9 | 2.2 / 1.1 / 5.5 | 18.0 / 20.4 / 26.8 | 183.6 / 103.1 / 289.1 | 0.1 / 0.1 / 0.1 | 210.5 / 132.2 / 313.5 | 4.374 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 4.2 / 3.4 / 5.9 | 77.8 / 76.3 / 80.6 | 2.2 / 1.3 / 5.7 | 74.4 / 22.3 / 357.4 | 227.0 / 100.5 / 630.8 | 0.1 / 0.1 / 0.1 | 308.8 / 149.9 / 733.7 | 4.964 |
| ig:llm/llm:sbert+repair=1+align=0 | 4.9 / 4.2 / 7.4 | 80.1 / 78.8 / 85.1 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.4 / 0.4 / 0.5 | 5.3 / 5.0 / 8.2 | 2.191 |
| rerank:llm:sbert | – | 803.2 / 912.1 / 1093.4 | – | – | – | – | 808.7 / 915.2 / 1100.4 | 1.232 |
| rerank:llmig:sbert | 16.1 / 15.3 / 31.9 | 667.6 / 801.3 / 912.8 | 7.8 / 4.4 / 18.4 | 535.2 / 198.1 / 1213.7 | 1514.4 / 1034.1 / 3842.0 | 0.1 / 0.1 / 0.3 | 30436.5 / 31888.4 / 40692.5 | 53.576 |
| rerank:llmgold:sbert | 0.2 / 0.2 / 0.2 | 830.1 / 777.5 / 1202.7 | 0.2 / 0.2 / 0.3 | 899.4 / 1151.6 / 1509.4 | 4450.7 / 5124.0 / 8641.3 | 0.2 / 0.1 / 0.3 | 31587.2 / 29372.5 / 45996.9 | 52.922 |

Context index build (one-off, ms): sbert: 11020 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:llm/llm:sbert+repair=1+align=0 | ctx:sbert | ndcg@10 | -0.032 | [-0.092, +0.010] | 0.334 | 5/10 |
| ig:llm/llm:sbert+repair=1+align=0 | ctx:sbert | mrr | -0.080 | [-0.185, +0.000] | 0.251 | 0/3 |
| ig:llm/llm:sbert+repair=1+align=0 | ctx:sbert | useful@1 | -0.100 | [-0.250, +0.000] | 0.501 | 0/2 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | ndcg@10 | +0.053 | [-0.015, +0.111] | 0.113 | 11/6 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | mrr | +0.102 | [-0.007, +0.226] | 0.153 | 5/1 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | ctx:sbert | useful@1 | +0.150 | [-0.050, +0.350] | 0.370 | 4/1 |
| ig:llm/llm:sbert | ctx:sbert | ndcg@10 | +0.054 | [-0.026, +0.131] | 0.191 | 13/3 |
| ig:llm/llm:sbert | ctx:sbert | mrr | +0.096 | [-0.037, +0.242] | 0.279 | 5/2 |
| ig:llm/llm:sbert | ctx:sbert | useful@1 | +0.150 | [-0.100, +0.400] | 0.451 | 5/2 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | ndcg@10 | +0.052 | [-0.044, +0.141] | 0.294 | 14/5 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | mrr | +0.102 | [-0.064, +0.281] | 0.294 | 6/3 |
| ig:llm/llm:sbert+repair=1 | ctx:sbert | useful@1 | +0.150 | [-0.150, +0.450] | 0.511 | 6/3 |
