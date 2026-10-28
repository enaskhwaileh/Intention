# IGBench results (20261025T110127Z_plan_igb-test_taberta)

Benchmark `igbench-v1-test` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:taberta | 0.612 | 0.330 | 0.205 | 0.666 | 0.722 | 0.650 | 0.100 |
| ig:rule/index:taberta | 0.639 | 0.390 | 0.250 | 0.741 | 0.755 | 0.650 | 0.100 |
| ig:rule/index:taberta+rnorm=minmax | 0.624 | 0.360 | 0.210 | 0.680 | 0.733 | 0.650 | 0.050 |
| ig:rule/index:taberta+align=0 | 0.594 | 0.340 | 0.210 | 0.680 | 0.669 | 0.550 | 0.150 |
| ig:gold/gold:taberta | 0.671 | 0.410 | 0.270 | 0.790 | 0.783 | 0.700 | 0.050 |
| ig:gold/gold:taberta+rnorm=minmax | 0.625 | 0.360 | 0.210 | 0.680 | 0.735 | 0.650 | 0.050 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:taberta | 0.600 | 0.305 | 0.708 | 0.632 |
| ig:rule/index:taberta | 0.628 | 0.368 | 0.742 | 0.632 |
| ig:rule/index:taberta+rnorm=minmax | 0.612 | 0.337 | 0.719 | 0.632 |
| ig:rule/index:taberta+align=0 | 0.581 | 0.316 | 0.652 | 0.526 |
| ig:gold/gold:taberta | 0.662 | 0.390 | 0.772 | 0.684 |
| ig:gold/gold:taberta+rnorm=minmax | 0.613 | 0.337 | 0.721 | 0.632 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:taberta | 0.312 | 0.598 | 0.666 |
| ig:rule/index:taberta | 0.247 | 0.649 | 0.741 |
| ig:rule/index:taberta+rnorm=minmax | 0.314 | 0.622 | 0.680 |
| ig:rule/index:taberta+align=0 | 0.279 | 0.602 | 0.680 |
| ig:gold/gold:taberta | 0.297 | 0.671 | 0.790 |
| ig:gold/gold:taberta+rnorm=minmax | 0.314 | 0.622 | 0.680 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | compare (n=8) | explain (n=3) | monitor (n=5) | predict (n=4) |
|---|---|---|---|---|
| ctx:taberta | 0.594 | 0.533 | 0.665 | 0.646 |
| ig:rule/index:taberta | 0.650 | 0.645 | 0.661 | 0.583 |
| ig:rule/index:taberta+rnorm=minmax | 0.584 | 0.557 | 0.694 | 0.663 |
| ig:rule/index:taberta+align=0 | 0.561 | 0.550 | 0.624 | 0.654 |
| ig:gold/gold:taberta | 0.646 | 0.648 | 0.670 | 0.737 |
| ig:gold/gold:taberta+rnorm=minmax | 0.580 | 0.568 | 0.678 | 0.690 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:taberta | 0.795 |
| ig:rule/index:taberta | 0.838 |
| ig:rule/index:taberta+rnorm=minmax | 0.815 |
| ig:rule/index:taberta+align=0 | 0.779 |
| ig:gold/gold:taberta | 0.845 |
| ig:gold/gold:taberta+rnorm=minmax | 0.814 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:rule/index:taberta | 1.000 | 0.815 | 0.950 | 1.000 | 1.000 | 0.947 | 0.807 | 0.000 | 0.581 | 0.667 |
| ig:rule/index:taberta+rnorm=minmax | 1.000 | 0.815 | 0.950 | 1.000 | 1.000 | 0.947 | 0.807 | 0.000 | 0.581 | 0.667 |
| ig:rule/index:taberta+align=0 | 1.000 | 0.815 | 0.950 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | – | – |
| ig:gold/gold:taberta | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.586 | 0.774 |
| ig:gold/gold:taberta+rnorm=minmax | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.586 | 0.774 |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:taberta | – | 120.9 / 99.7 / 103.5 | – | – | – | – | 120.9 / 99.8 / 103.6 | 2.54 |
| ig:rule/index:taberta | 1.0 / 0.4 / 2.1 | 98.3 / 97.5 / 103.3 | 2.3 / 0.3 / 7.2 | 22.3 / 22.2 / 32.6 | 148.8 / 84.4 / 337.5 | 0.1 / 0.1 / 0.1 | 175.5 / 105.3 / 371.7 | 4.308 |
| ig:rule/index:taberta+rnorm=minmax | 0.4 / 0.4 / 0.5 | 96.2 / 94.8 / 102.1 | 2.1 / 0.3 / 7.3 | 20.3 / 19.7 / 33.2 | 139.8 / 84.1 / 332.3 | 0.1 / 0.1 / 0.1 | 163.7 / 101.5 / 364.6 | 4.069 |
| ig:rule/index:taberta+align=0 | 0.4 / 0.4 / 0.4 | 98.0 / 97.4 / 101.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.4 / 0.4 / 0.7 | 0.9 / 0.8 / 1.2 | 2.46 |
| ig:gold/gold:taberta | 0.1 / 0.1 / 0.1 | 99.8 / 100.5 / 103.3 | 0.8 / 0.2 / 3.0 | 65.0 / 21.5 / 326.1 | 190.0 / 116.5 / 414.8 | 0.1 / 0.1 / 0.1 | 257.0 / 145.3 / 482.4 | 4.032 |
| ig:gold/gold:taberta+rnorm=minmax | 0.1 / 0.1 / 0.1 | 93.6 / 94.1 / 97.6 | 0.7 / 0.2 / 2.6 | 22.5 / 23.3 / 36.1 | 147.3 / 92.3 / 354.3 | 0.1 / 0.1 / 0.1 | 171.8 / 122.2 / 390.8 | 3.688 |

Context index build (one-off, ms): taberta: 13701 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:rule/index:taberta+align=0 | ctx:taberta | ndcg@10 | -0.018 | [-0.050, +0.011] | 0.316 | 6/6 |
| ig:rule/index:taberta+align=0 | ctx:taberta | mrr | -0.053 | [-0.158, +0.017] | 0.500 | 3/2 |
| ig:rule/index:taberta+align=0 | ctx:taberta | useful@1 | -0.100 | [-0.250, +0.000] | 0.500 | 0/2 |
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
