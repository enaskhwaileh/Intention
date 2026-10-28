# IGBench results (20261025T105333Z_plan_igb-dev_taberta)

Benchmark `igbench-v1` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:taberta | 0.615 | 0.354 | 0.240 | 0.692 | 0.640 | 0.486 | 0.400 |
| ig:rule/index:taberta | 0.735 | 0.480 | 0.314 | 0.858 | 0.832 | 0.714 | 0.200 |
| ig:rule/index:taberta+rnorm=minmax | 0.703 | 0.423 | 0.291 | 0.820 | 0.776 | 0.657 | 0.229 |
| ig:rule/index:taberta+align=0 | 0.645 | 0.371 | 0.271 | 0.759 | 0.616 | 0.429 | 0.429 |
| ig:gold/gold:taberta | 0.748 | 0.463 | 0.314 | 0.836 | 0.837 | 0.743 | 0.143 |
| ig:gold/gold:taberta+rnorm=minmax | 0.710 | 0.423 | 0.289 | 0.788 | 0.770 | 0.657 | 0.257 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:taberta | 0.606 | 0.325 | 0.623 | 0.469 |
| ig:rule/index:taberta | 0.737 | 0.463 | 0.831 | 0.719 |
| ig:rule/index:taberta+rnorm=minmax | 0.703 | 0.400 | 0.770 | 0.656 |
| ig:rule/index:taberta+align=0 | 0.639 | 0.344 | 0.596 | 0.406 |
| ig:gold/gold:taberta | 0.752 | 0.444 | 0.838 | 0.750 |
| ig:gold/gold:taberta+rnorm=minmax | 0.710 | 0.400 | 0.764 | 0.656 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:taberta | 0.207 | 0.538 | 0.692 |
| ig:rule/index:taberta | 0.291 | 0.704 | 0.858 |
| ig:rule/index:taberta+rnorm=minmax | 0.253 | 0.625 | 0.820 |
| ig:rule/index:taberta+align=0 | 0.189 | 0.543 | 0.759 |
| ig:gold/gold:taberta | 0.312 | 0.686 | 0.836 |
| ig:gold/gold:taberta+rnorm=minmax | 0.267 | 0.625 | 0.788 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | aggregate (n=3) | compare (n=10) | explain (n=7) | monitor (n=5) | predict (n=8) |
|---|---|---|---|---|---|
| ctx:taberta | 0.883 | 0.584 | 0.580 | 0.672 | 0.531 |
| ig:rule/index:taberta | 0.878 | 0.714 | 0.842 | 0.680 | 0.669 |
| ig:rule/index:taberta+rnorm=minmax | 0.900 | 0.664 | 0.775 | 0.703 | 0.631 |
| ig:rule/index:taberta+align=0 | 0.913 | 0.605 | 0.688 | 0.657 | 0.551 |
| ig:gold/gold:taberta | 0.879 | 0.763 | 0.823 | 0.676 | 0.687 |
| ig:gold/gold:taberta+rnorm=minmax | 0.901 | 0.667 | 0.770 | 0.709 | 0.657 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:taberta | 0.665 |
| ig:rule/index:taberta | 0.753 |
| ig:rule/index:taberta+rnorm=minmax | 0.718 |
| ig:rule/index:taberta+align=0 | 0.671 |
| ig:gold/gold:taberta | 0.708 |
| ig:gold/gold:taberta+rnorm=minmax | 0.673 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:rule/index:taberta | 1.000 | 0.825 | 0.970 | 0.833 | 0.812 | 0.812 | 0.688 | 0.188 | 0.547 | 0.736 |
| ig:rule/index:taberta+rnorm=minmax | 1.000 | 0.825 | 0.970 | 0.833 | 0.812 | 0.812 | 0.688 | 0.188 | 0.547 | 0.736 |
| ig:rule/index:taberta+align=0 | 1.000 | 0.825 | 0.970 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | – | – |
| ig:gold/gold:taberta | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.593 | 0.762 |
| ig:gold/gold:taberta+rnorm=minmax | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.593 | 0.762 |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:taberta | – | 110.2 / 99.0 / 107.4 | – | – | – | – | 110.2 / 99.0 / 107.5 | 3.968 |
| ig:rule/index:taberta | 0.7 / 0.4 / 0.9 | 95.4 / 94.8 / 101.7 | 1.9 / 0.6 / 7.2 | 18.1 / 20.2 / 36.0 | 752.8 / 124.2 / 3942.4 | 0.1 / 0.1 / 0.2 | 774.4 / 157.3 / 3967.5 | 15.751 |
| ig:rule/index:taberta+rnorm=minmax | 0.4 / 0.4 / 0.5 | 97.7 / 98.1 / 102.5 | 2.0 / 0.6 / 6.6 | 45.7 / 20.5 / 319.2 | 768.7 / 157.6 / 3772.2 | 0.1 / 0.1 / 0.2 | 817.8 / 221.8 / 4094.0 | 15.98 |
| ig:rule/index:taberta+align=0 | 0.4 / 0.4 / 0.5 | 96.1 / 95.1 / 102.4 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.4 / 0.3 / 0.7 | 0.8 / 0.7 / 1.3 | 3.863 |
| ig:gold/gold:taberta | 0.1 / 0.1 / 0.2 | 94.0 / 93.3 / 99.4 | 0.6 / 0.2 / 1.7 | 22.7 / 20.7 / 40.6 | 828.3 / 158.8 / 3995.3 | 0.1 / 0.1 / 0.1 | 853.0 / 181.0 / 4040.6 | 20.266 |
| ig:gold/gold:taberta+rnorm=minmax | 0.1 / 0.1 / 0.2 | 96.0 / 95.2 / 102.6 | 0.6 / 0.2 / 1.6 | 53.2 / 20.4 / 44.3 | 824.5 / 157.4 / 3986.7 | 0.1 / 0.1 / 0.2 | 879.6 / 180.5 / 4072.5 | 20.633 |

Context index build (one-off, ms): taberta: 14589 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:rule/index:taberta+align=0 | ctx:taberta | ndcg@10 | +0.032 | [-0.002, +0.072] | 0.101 | 23/5 |
| ig:rule/index:taberta+align=0 | ctx:taberta | mrr | -0.024 | [-0.084, +0.023] | 0.414 | 8/5 |
| ig:rule/index:taberta+align=0 | ctx:taberta | useful@1 | -0.057 | [-0.143, +0.000] | 0.498 | 0/2 |
| ig:rule/index:taberta+rnorm=minmax | ctx:taberta | ndcg@10 | +0.088 | [+0.042, +0.137] | 0.000 | 26/4 |
| ig:rule/index:taberta+rnorm=minmax | ctx:taberta | mrr | +0.135 | [+0.029, +0.246] | 0.018 | 15/3 |
| ig:rule/index:taberta+rnorm=minmax | ctx:taberta | useful@1 | +0.171 | [+0.000, +0.343] | 0.111 | 8/2 |
| ig:gold/gold:taberta+rnorm=minmax | ctx:taberta | ndcg@10 | +0.095 | [+0.047, +0.146] | 0.001 | 25/4 |
| ig:gold/gold:taberta+rnorm=minmax | ctx:taberta | mrr | +0.129 | [+0.033, +0.237] | 0.016 | 13/3 |
| ig:gold/gold:taberta+rnorm=minmax | ctx:taberta | useful@1 | +0.171 | [+0.029, +0.314] | 0.070 | 7/1 |
| ig:gold/gold:taberta | ctx:taberta | ndcg@10 | +0.132 | [+0.067, +0.199] | 0.000 | 24/7 |
| ig:gold/gold:taberta | ctx:taberta | mrr | +0.197 | [+0.088, +0.314] | 0.001 | 13/3 |
| ig:gold/gold:taberta | ctx:taberta | useful@1 | +0.257 | [+0.086, +0.429] | 0.010 | 10/1 |
| ig:rule/index:taberta | ctx:taberta | ndcg@10 | +0.118 | [+0.048, +0.193] | 0.002 | 23/8 |
| ig:rule/index:taberta | ctx:taberta | mrr | +0.191 | [+0.075, +0.312] | 0.004 | 14/3 |
| ig:rule/index:taberta | ctx:taberta | useful@1 | +0.229 | [+0.057, +0.400] | 0.037 | 10/2 |
