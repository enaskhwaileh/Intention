# IGBench results (20261025T093625Z_srv_test_taberta_pc)

Benchmark `igbench-v1-test` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:taberta | 0.612 | 0.330 | 0.205 | 0.666 | 0.722 | 0.650 | 0.100 |
| ig:gold/gold:taberta | 0.671 | 0.410 | 0.270 | 0.790 | 0.783 | 0.700 | 0.050 |
| ig:rule/index:taberta | 0.639 | 0.390 | 0.250 | 0.741 | 0.755 | 0.650 | 0.100 |
| ig:gold/gold:taberta+rnorm=minmax | 0.625 | 0.360 | 0.210 | 0.680 | 0.735 | 0.650 | 0.050 |
| ig:rule/index:taberta+rnorm=minmax | 0.624 | 0.360 | 0.210 | 0.680 | 0.733 | 0.650 | 0.050 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:taberta | 0.600 | 0.305 | 0.708 | 0.632 |
| ig:gold/gold:taberta | 0.662 | 0.390 | 0.772 | 0.684 |
| ig:rule/index:taberta | 0.628 | 0.368 | 0.742 | 0.632 |
| ig:gold/gold:taberta+rnorm=minmax | 0.613 | 0.337 | 0.721 | 0.632 |
| ig:rule/index:taberta+rnorm=minmax | 0.612 | 0.337 | 0.719 | 0.632 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:taberta | 0.312 | 0.598 | 0.666 |
| ig:gold/gold:taberta | 0.297 | 0.671 | 0.790 |
| ig:rule/index:taberta | 0.247 | 0.649 | 0.741 |
| ig:gold/gold:taberta+rnorm=minmax | 0.314 | 0.622 | 0.680 |
| ig:rule/index:taberta+rnorm=minmax | 0.314 | 0.622 | 0.680 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | compare (n=8) | explain (n=3) | monitor (n=5) | predict (n=4) |
|---|---|---|---|---|
| ctx:taberta | 0.594 | 0.533 | 0.665 | 0.646 |
| ig:gold/gold:taberta | 0.646 | 0.648 | 0.670 | 0.737 |
| ig:rule/index:taberta | 0.650 | 0.645 | 0.661 | 0.583 |
| ig:gold/gold:taberta+rnorm=minmax | 0.580 | 0.568 | 0.678 | 0.690 |
| ig:rule/index:taberta+rnorm=minmax | 0.584 | 0.557 | 0.694 | 0.663 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:taberta | 0.795 |
| ig:gold/gold:taberta | 0.845 |
| ig:rule/index:taberta | 0.838 |
| ig:gold/gold:taberta+rnorm=minmax | 0.814 |
| ig:rule/index:taberta+rnorm=minmax | 0.815 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:gold/gold:taberta | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.586 | 0.774 |
| ig:rule/index:taberta | 1.000 | 0.815 | 0.950 | 1.000 | 1.000 | 0.947 | 0.807 | 0.000 | 0.581 | 0.667 |
| ig:gold/gold:taberta+rnorm=minmax | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.586 | 0.774 |
| ig:rule/index:taberta+rnorm=minmax | 1.000 | 0.815 | 0.950 | 1.000 | 1.000 | 0.947 | 0.807 | 0.000 | 0.581 | 0.667 |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:taberta | – | 31.7 / 29.6 / 33.9 | – | – | – | – | 31.8 / 29.6 / 34.0 | 0.668 |
| ig:gold/gold:taberta | 0.1 / 0.1 / 0.1 | 29.4 / 29.2 / 32.0 | 0.2 / 0.2 / 0.3 | 66.6 / 23.0 / 234.6 | 155.0 / 92.0 / 450.9 | 0.1 / 0.1 / 0.1 | 252.2 / 232.3 / 528.1 | 5.311 |
| ig:rule/index:taberta | 0.5 / 0.2 / 0.6 | 30.7 / 30.6 / 34.1 | 0.3 / 0.3 / 0.4 | 41.9 / 19.9 / 122.5 | 141.5 / 83.4 / 342.8 | 0.1 / 0.1 / 0.1 | 216.3 / 159.4 / 392.9 | 4.555 |
| ig:gold/gold:taberta+rnorm=minmax | 0.1 / 0.1 / 0.1 | 43.4 / 33.4 / 39.3 | 0.2 / 0.2 / 0.3 | 26.8 / 19.8 / 27.1 | 148.5 / 90.6 / 340.1 | 0.1 / 0.1 / 0.1 | 220.0 / 150.3 / 399.9 | 4.64 |
| ig:rule/index:taberta+rnorm=minmax | 0.2 / 0.2 / 0.2 | 29.7 / 28.7 / 32.9 | 0.3 / 0.3 / 0.3 | 27.4 / 18.8 / 26.5 | 146.0 / 78.0 / 309.1 | 0.1 / 0.1 / 0.1 | 204.6 / 129.4 / 390.3 | 4.315 |

Context index build (one-off, ms): taberta: 9335 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:rule/index:taberta+rnorm=minmax | ctx:taberta | ndcg@10 | +0.010 | [-0.023, +0.038] | 0.579 | 7/4 |
| ig:rule/index:taberta+rnorm=minmax | ctx:taberta | mrr | +0.011 | [-0.069, +0.100] | 0.620 | 3/1 |
| ig:rule/index:taberta+rnorm=minmax | ctx:taberta | useful@1 | +0.000 | [-0.150, +0.150] | 1.000 | 1/1 |
| ig:gold/gold:taberta+rnorm=minmax | ctx:taberta | ndcg@10 | +0.011 | [-0.023, +0.042] | 0.536 | 8/4 |
| ig:gold/gold:taberta+rnorm=minmax | ctx:taberta | mrr | +0.013 | [-0.066, +0.100] | 0.745 | 2/1 |
| ig:gold/gold:taberta+rnorm=minmax | ctx:taberta | useful@1 | +0.000 | [-0.150, +0.150] | 1.000 | 1/1 |
| ig:gold/gold:taberta | ctx:taberta | ndcg@10 | +0.055 | [-0.010, +0.127] | 0.151 | 9/6 |
| ig:gold/gold:taberta | ctx:taberta | mrr | +0.061 | [-0.035, +0.164] | 0.316 | 4/1 |
| ig:gold/gold:taberta | ctx:taberta | useful@1 | +0.050 | [-0.100, +0.200] | 1.000 | 2/1 |
| ig:rule/index:taberta | ctx:taberta | ndcg@10 | +0.024 | [-0.035, +0.088] | 0.466 | 8/7 |
| ig:rule/index:taberta | ctx:taberta | mrr | +0.033 | [-0.077, +0.148] | 0.659 | 4/2 |
| ig:rule/index:taberta | ctx:taberta | useful@1 | +0.000 | [-0.200, +0.200] | 1.000 | 2/2 |
