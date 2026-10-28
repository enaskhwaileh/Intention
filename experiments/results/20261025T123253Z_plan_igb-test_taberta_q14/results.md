# IGBench results (20261025T123253Z_plan_igb-test_taberta_q14)

Benchmark `igbench-v1-test` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:taberta | 0.612 | 0.330 | 0.205 | 0.666 | 0.722 | 0.650 | 0.100 |
| ig:llm/llm:taberta | 0.623 | 0.380 | 0.220 | 0.676 | 0.718 | 0.650 | 0.050 |
| ig:llm/llm:taberta+repair=1 | 0.630 | 0.370 | 0.230 | 0.693 | 0.743 | 0.700 | 0.050 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | 0.592 | 0.340 | 0.195 | 0.643 | 0.686 | 0.600 | 0.050 |
| ig:llm/llm:taberta+repair=1+align=0 | 0.557 | 0.300 | 0.185 | 0.620 | 0.611 | 0.500 | 0.150 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:taberta | 0.600 | 0.305 | 0.708 | 0.632 |
| ig:llm/llm:taberta | 0.654 | 0.400 | 0.756 | 0.684 |
| ig:llm/llm:taberta+repair=1 | 0.661 | 0.390 | 0.782 | 0.737 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | 0.622 | 0.358 | 0.723 | 0.632 |
| ig:llm/llm:taberta+repair=1+align=0 | 0.585 | 0.316 | 0.643 | 0.526 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:taberta | 0.312 | 0.598 | 0.666 |
| ig:llm/llm:taberta | 0.327 | 0.632 | 0.676 |
| ig:llm/llm:taberta+repair=1 | 0.335 | 0.624 | 0.693 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | 0.302 | 0.589 | 0.643 |
| ig:llm/llm:taberta+repair=1+align=0 | 0.267 | 0.552 | 0.620 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | compare (n=8) | explain (n=3) | monitor (n=5) | predict (n=4) |
|---|---|---|---|---|
| ctx:taberta | 0.594 | 0.533 | 0.665 | 0.646 |
| ig:llm/llm:taberta | 0.664 | 0.549 | 0.691 | 0.711 |
| ig:llm/llm:taberta+repair=1 | 0.689 | 0.549 | 0.680 | 0.711 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | 0.585 | 0.557 | 0.694 | 0.707 |
| ig:llm/llm:taberta+repair=1+align=0 | 0.564 | 0.532 | 0.636 | 0.668 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:taberta | 0.795 |
| ig:llm/llm:taberta | 0.818 |
| ig:llm/llm:taberta+repair=1 | 0.841 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | 0.810 |
| ig:llm/llm:taberta+repair=1+align=0 | 0.770 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:llm/llm:taberta | 0.857 | 0.774 | 0.980 | 0.714 | 0.684 | 0.684 | 0.588 | 0.316 | 0.585 | 0.816 |
| ig:llm/llm:taberta+repair=1 | 1.000 | 0.788 | 0.933 | 0.905 | 0.895 | 0.895 | 0.781 | 0.105 | 0.603 | 0.745 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | 1.000 | 0.788 | 0.933 | 0.905 | 0.895 | 0.895 | 0.781 | 0.105 | 0.603 | 0.745 |
| ig:llm/llm:taberta+repair=1+align=0 | 1.000 | 0.788 | 0.933 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | – | – |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:taberta | – | 109.4 / 88.7 / 93.2 | – | – | – | – | 109.5 / 88.7 / 93.2 | 2.3 |
| ig:llm/llm:taberta | 3.8 / 3.4 / 5.0 | 87.6 / 87.3 / 93.2 | 1.4 / 1.0 / 3.4 | 17.7 / 17.8 / 31.8 | 144.1 / 77.6 / 266.1 | 0.1 / 0.1 / 0.2 | 167.8 / 105.1 / 299.7 | 4.342 |
| ig:llm/llm:taberta+repair=1 | 4.2 / 4.0 / 6.6 | 87.7 / 86.0 / 91.9 | 2.3 / 1.0 / 6.3 | 17.9 / 17.5 / 30.0 | 161.7 / 92.0 / 255.1 | 0.1 / 0.1 / 0.1 | 187.1 / 126.7 / 292.0 | 4.523 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | 5.4 / 4.5 / 8.8 | 100.2 / 104.2 / 112.7 | 2.0 / 1.1 / 4.4 | 131.5 / 24.4 / 399.3 | 266.3 / 157.7 / 1025.5 | 0.1 / 0.1 / 0.2 | 406.4 / 226.5 / 1061.4 | 5.766 |
| ig:llm/llm:taberta+repair=1+align=0 | 5.5 / 5.2 / 7.3 | 88.1 / 84.6 / 101.5 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.3 / 0.2 / 0.4 | 5.8 / 5.4 / 7.9 | 2.433 |

Context index build (one-off, ms): taberta: 12694 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:llm/llm:taberta+repair=1 | ctx:taberta | ndcg@10 | +0.016 | [-0.098, +0.106] | 0.799 | 6/8 |
| ig:llm/llm:taberta+repair=1 | ctx:taberta | mrr | +0.021 | [-0.125, +0.146] | 0.875 | 3/2 |
| ig:llm/llm:taberta+repair=1 | ctx:taberta | useful@1 | +0.050 | [-0.100, +0.200] | 1.000 | 2/1 |
| ig:llm/llm:taberta+repair=1+align=0 | ctx:taberta | ndcg@10 | -0.053 | [-0.150, +0.004] | 0.172 | 5/7 |
| ig:llm/llm:taberta+repair=1+align=0 | ctx:taberta | mrr | -0.112 | [-0.250, +0.001] | 0.188 | 1/4 |
| ig:llm/llm:taberta+repair=1+align=0 | ctx:taberta | useful@1 | -0.150 | [-0.300, +0.000] | 0.255 | 0/3 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | ctx:taberta | ndcg@10 | -0.020 | [-0.120, +0.049] | 0.798 | 8/5 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | ctx:taberta | mrr | -0.036 | [-0.169, +0.079] | 0.694 | 2/3 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | ctx:taberta | useful@1 | -0.050 | [-0.200, +0.100] | 1.000 | 1/2 |
| ig:llm/llm:taberta | ctx:taberta | ndcg@10 | +0.009 | [-0.107, +0.102] | 0.888 | 6/7 |
| ig:llm/llm:taberta | ctx:taberta | mrr | -0.004 | [-0.150, +0.122] | 0.939 | 3/3 |
| ig:llm/llm:taberta | ctx:taberta | useful@1 | +0.000 | [-0.200, +0.200] | 1.000 | 2/2 |
