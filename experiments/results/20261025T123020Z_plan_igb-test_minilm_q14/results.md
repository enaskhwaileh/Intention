# IGBench results (20261025T123020Z_plan_igb-test_minilm_q14)

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

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:sbert | 0.680 | 0.316 | 0.804 | 0.684 |
| ig:llm/llm:sbert | 0.758 | 0.463 | 0.932 | 0.895 |
| ig:llm/llm:sbert+repair=1 | 0.756 | 0.495 | 0.939 | 0.895 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.756 | 0.463 | 0.939 | 0.895 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.663 | 0.337 | 0.747 | 0.632 |
| rerank:llm:sbert | 0.804 | 0.505 | 0.974 | 0.947 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:sbert | 0.352 | 0.591 | 0.780 |
| ig:llm/llm:sbert | 0.374 | 0.731 | 0.846 |
| ig:llm/llm:sbert+repair=1 | 0.333 | 0.760 | 0.863 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.399 | 0.712 | 0.830 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.327 | 0.584 | 0.736 |
| rerank:llm:sbert | 0.432 | 0.803 | 0.861 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | compare (n=8) | explain (n=3) | monitor (n=5) | predict (n=4) |
|---|---|---|---|---|
| ctx:sbert | 0.665 | 0.675 | 0.683 | 0.756 |
| ig:llm/llm:sbert | 0.758 | 0.743 | 0.747 | 0.825 |
| ig:llm/llm:sbert+repair=1 | 0.806 | 0.743 | 0.662 | 0.825 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 0.766 | 0.693 | 0.732 | 0.856 |
| ig:llm/llm:sbert+repair=1+align=0 | 0.673 | 0.680 | 0.614 | 0.756 |
| rerank:llm:sbert | 0.838 | 0.773 | 0.794 | 0.822 |

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

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:llm/llm:sbert | 0.857 | 0.774 | 0.980 | 0.714 | 0.684 | 0.684 | 0.588 | 0.316 | 0.623 | 0.775 |
| ig:llm/llm:sbert+repair=1 | 1.000 | 0.788 | 0.933 | 0.905 | 0.895 | 0.895 | 0.781 | 0.105 | 0.616 | 0.703 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 1.000 | 0.788 | 0.933 | 0.905 | 0.895 | 0.895 | 0.781 | 0.105 | 0.616 | 0.703 |
| ig:llm/llm:sbert+repair=1+align=0 | 1.000 | 0.788 | 0.933 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | – | – |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:sbert | – | 99.1 / 82.1 / 85.7 | – | – | – | – | 99.2 / 82.1 / 85.7 | 2.083 |
| ig:llm/llm:sbert | 4.5 / 3.9 / 6.2 | 78.9 / 79.1 / 87.9 | 1.7 / 1.2 / 3.9 | 18.9 / 22.4 / 36.6 | 188.7 / 89.6 / 345.3 | 0.2 / 0.1 / 0.2 | 214.7 / 116.0 / 377.6 | 4.54 |
| ig:llm/llm:sbert+repair=1 | 4.7 / 4.6 / 6.9 | 69.7 / 69.0 / 74.2 | 2.2 / 1.2 / 5.6 | 18.9 / 20.7 / 28.6 | 199.5 / 129.9 / 331.6 | 0.1 / 0.1 / 0.2 | 226.4 / 166.6 / 353.9 | 4.424 |
| ig:llm/llm:sbert+repair=1+rnorm=minmax | 4.1 / 3.6 / 6.8 | 73.2 / 72.8 / 82.8 | 1.9 / 1.1 / 5.3 | 61.8 / 20.9 / 321.0 | 210.9 / 107.1 / 533.7 | 0.1 / 0.1 / 0.1 | 279.6 / 144.2 / 611.3 | 4.584 |
| ig:llm/llm:sbert+repair=1+align=0 | 6.2 / 6.1 / 9.1 | 74.3 / 72.5 / 82.4 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.4 / 0.4 / 0.6 | 6.7 / 6.8 / 9.6 | 1.974 |
| rerank:llm:sbert | – | 783.8 / 985.5 / 1065.4 | – | – | – | – | 31616.6 / 31239.7 / 43467.4 | 50.365 |

Context index build (one-off, ms): sbert: 12083 (cached)

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
