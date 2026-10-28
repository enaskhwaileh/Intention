# IGBench results (20261025T181017Z_plan_igb-test_taberta_q32)

Benchmark `igbench-v1-test` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:taberta | 0.612 | 0.330 | 0.205 | 0.666 | 0.722 | 0.650 | 0.100 |
| ig:llm/llm:taberta | 0.620 | 0.360 | 0.220 | 0.679 | 0.718 | 0.650 | 0.050 |
| ig:llm/llm:taberta+repair=1 | 0.626 | 0.370 | 0.225 | 0.689 | 0.742 | 0.650 | 0.050 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | 0.589 | 0.330 | 0.190 | 0.633 | 0.687 | 0.600 | 0.050 |
| ig:llm/llm:taberta+repair=1+align=0 | 0.558 | 0.300 | 0.185 | 0.620 | 0.611 | 0.500 | 0.150 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:taberta | 0.600 | 0.305 | 0.708 | 0.632 |
| ig:llm/llm:taberta | 0.651 | 0.379 | 0.756 | 0.684 |
| ig:llm/llm:taberta+repair=1 | 0.657 | 0.390 | 0.781 | 0.684 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | 0.618 | 0.347 | 0.723 | 0.632 |
| ig:llm/llm:taberta+repair=1+align=0 | 0.585 | 0.316 | 0.643 | 0.526 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:taberta | 0.312 | 0.598 | 0.666 |
| ig:llm/llm:taberta | 0.327 | 0.612 | 0.679 |
| ig:llm/llm:taberta+repair=1 | 0.327 | 0.622 | 0.689 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | 0.302 | 0.579 | 0.633 |
| ig:llm/llm:taberta+repair=1+align=0 | 0.267 | 0.552 | 0.620 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | compare (n=8) | explain (n=3) | monitor (n=5) | predict (n=4) |
|---|---|---|---|---|
| ctx:taberta | 0.594 | 0.533 | 0.665 | 0.646 |
| ig:llm/llm:taberta | 0.664 | 0.533 | 0.691 | 0.711 |
| ig:llm/llm:taberta+repair=1 | 0.664 | 0.591 | 0.680 | 0.711 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | 0.585 | 0.535 | 0.694 | 0.707 |
| ig:llm/llm:taberta+repair=1+align=0 | 0.564 | 0.534 | 0.636 | 0.668 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:taberta | 0.795 |
| ig:llm/llm:taberta | 0.811 |
| ig:llm/llm:taberta+repair=1 | 0.811 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | 0.798 |
| ig:llm/llm:taberta+repair=1+align=0 | 0.770 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:llm/llm:taberta | 0.762 | 0.931 | 0.911 | 0.714 | 0.684 | 0.684 | 0.623 | 0.316 | 0.619 | 0.839 |
| ig:llm/llm:taberta+repair=1 | 0.952 | 0.840 | 0.930 | 0.905 | 0.895 | 0.895 | 0.728 | 0.105 | 0.641 | 0.809 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | 0.952 | 0.840 | 0.930 | 0.905 | 0.895 | 0.895 | 0.728 | 0.105 | 0.641 | 0.809 |
| ig:llm/llm:taberta+repair=1+align=0 | 0.952 | 0.840 | 0.930 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | – | – |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:taberta | – | 100.1 / 79.3 / 85.4 | – | – | – | – | 100.1 / 79.4 / 85.5 | 2.103 |
| ig:llm/llm:taberta | 4.5 / 4.2 / 6.4 | 78.6 / 77.8 / 84.8 | 1.7 / 0.9 / 4.8 | 15.6 / 18.2 / 30.6 | 115.7 / 79.0 / 251.9 | 0.1 / 0.1 / 0.1 | 138.4 / 109.3 / 282.5 | 3.103 |
| ig:llm/llm:taberta+repair=1 | 5.9 / 5.0 / 10.6 | 78.9 / 77.1 / 83.7 | 2.0 / 1.0 / 5.6 | 18.3 / 17.3 / 31.4 | 190.4 / 114.2 / 395.3 | 0.1 / 0.1 / 0.2 | 217.7 / 151.6 / 433.6 | 4.432 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | 5.5 / 4.5 / 10.1 | 73.3 / 73.8 / 78.2 | 1.8 / 1.0 / 4.2 | 59.6 / 19.7 / 304.4 | 197.8 / 123.0 / 342.1 | 0.1 / 0.1 / 0.2 | 265.8 / 163.2 / 565.3 | 4.817 |
| ig:llm/llm:taberta+repair=1+align=0 | 5.7 / 4.9 / 10.6 | 79.1 / 79.2 / 84.8 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.4 / 0.4 / 0.6 | 6.2 / 5.4 / 10.9 | 2.118 |

Context index build (one-off, ms): taberta: 9919 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:llm/llm:taberta+repair=1 | ctx:taberta | ndcg@10 | +0.012 | [-0.103, +0.108] | 0.842 | 6/8 |
| ig:llm/llm:taberta+repair=1 | ctx:taberta | mrr | +0.019 | [-0.129, +0.156] | 0.873 | 4/2 |
| ig:llm/llm:taberta+repair=1 | ctx:taberta | useful@1 | +0.000 | [-0.200, +0.200] | 1.000 | 2/2 |
| ig:llm/llm:taberta+repair=1+align=0 | ctx:taberta | ndcg@10 | -0.053 | [-0.150, +0.004] | 0.177 | 5/6 |
| ig:llm/llm:taberta+repair=1+align=0 | ctx:taberta | mrr | -0.112 | [-0.250, +0.001] | 0.188 | 1/4 |
| ig:llm/llm:taberta+repair=1+align=0 | ctx:taberta | useful@1 | -0.150 | [-0.300, +0.000] | 0.255 | 0/3 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | ctx:taberta | ndcg@10 | -0.023 | [-0.125, +0.046] | 0.769 | 7/5 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | ctx:taberta | mrr | -0.035 | [-0.169, +0.079] | 0.759 | 2/2 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | ctx:taberta | useful@1 | -0.050 | [-0.200, +0.100] | 1.000 | 1/2 |
| ig:llm/llm:taberta | ctx:taberta | ndcg@10 | +0.007 | [-0.107, +0.099] | 0.910 | 5/6 |
| ig:llm/llm:taberta | ctx:taberta | mrr | -0.004 | [-0.150, +0.122] | 1.000 | 3/2 |
| ig:llm/llm:taberta | ctx:taberta | useful@1 | +0.000 | [-0.200, +0.200] | 1.000 | 2/2 |
