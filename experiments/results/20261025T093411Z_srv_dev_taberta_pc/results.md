# IGBench results (20261025T093411Z_srv_dev_taberta_pc)

Benchmark `igbench-v1` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:taberta | 0.615 | 0.354 | 0.240 | 0.692 | 0.640 | 0.486 | 0.400 |
| ig:gold/gold:taberta | 0.748 | 0.463 | 0.314 | 0.836 | 0.837 | 0.743 | 0.143 |
| ig:rule/index:taberta | 0.735 | 0.480 | 0.314 | 0.858 | 0.832 | 0.714 | 0.200 |
| ig:gold/gold:taberta+rnorm=minmax | 0.710 | 0.423 | 0.289 | 0.788 | 0.770 | 0.657 | 0.257 |
| ig:rule/index:taberta+rnorm=minmax | 0.703 | 0.423 | 0.291 | 0.820 | 0.776 | 0.657 | 0.229 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:taberta | 0.606 | 0.325 | 0.623 | 0.469 |
| ig:gold/gold:taberta | 0.752 | 0.444 | 0.838 | 0.750 |
| ig:rule/index:taberta | 0.737 | 0.463 | 0.831 | 0.719 |
| ig:gold/gold:taberta+rnorm=minmax | 0.710 | 0.400 | 0.764 | 0.656 |
| ig:rule/index:taberta+rnorm=minmax | 0.703 | 0.400 | 0.770 | 0.656 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:taberta | 0.207 | 0.538 | 0.692 |
| ig:gold/gold:taberta | 0.312 | 0.686 | 0.836 |
| ig:rule/index:taberta | 0.291 | 0.704 | 0.858 |
| ig:gold/gold:taberta+rnorm=minmax | 0.267 | 0.625 | 0.788 |
| ig:rule/index:taberta+rnorm=minmax | 0.253 | 0.625 | 0.820 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | aggregate (n=3) | compare (n=10) | explain (n=7) | monitor (n=5) | predict (n=8) |
|---|---|---|---|---|---|
| ctx:taberta | 0.883 | 0.584 | 0.580 | 0.672 | 0.531 |
| ig:gold/gold:taberta | 0.879 | 0.763 | 0.823 | 0.676 | 0.687 |
| ig:rule/index:taberta | 0.878 | 0.714 | 0.842 | 0.680 | 0.669 |
| ig:gold/gold:taberta+rnorm=minmax | 0.901 | 0.667 | 0.770 | 0.709 | 0.657 |
| ig:rule/index:taberta+rnorm=minmax | 0.900 | 0.664 | 0.775 | 0.703 | 0.631 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:taberta | 0.665 |
| ig:gold/gold:taberta | 0.708 |
| ig:rule/index:taberta | 0.753 |
| ig:gold/gold:taberta+rnorm=minmax | 0.673 |
| ig:rule/index:taberta+rnorm=minmax | 0.718 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:gold/gold:taberta | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.593 | 0.762 |
| ig:rule/index:taberta | 1.000 | 0.825 | 0.970 | 0.833 | 0.812 | 0.812 | 0.688 | 0.188 | 0.547 | 0.736 |
| ig:gold/gold:taberta+rnorm=minmax | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.593 | 0.762 |
| ig:rule/index:taberta+rnorm=minmax | 1.000 | 0.825 | 0.970 | 0.833 | 0.812 | 0.812 | 0.688 | 0.188 | 0.547 | 0.736 |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:taberta | – | 31.9 / 29.3 / 38.1 | – | – | – | – | 32.0 / 29.3 / 38.2 | 1.153 |
| ig:gold/gold:taberta | 0.1 / 0.1 / 0.1 | 30.9 / 29.6 / 39.4 | 0.2 / 0.2 / 0.3 | 96.5 / 28.0 / 267.9 | 786.2 / 165.4 / 3859.2 | 0.1 / 0.1 / 0.1 | 914.9 / 283.8 / 3938.1 | 32.97 |
| ig:rule/index:taberta | 0.4 / 0.2 / 0.7 | 31.0 / 29.4 / 40.0 | 0.3 / 0.3 / 0.4 | 28.8 / 19.3 / 38.6 | 717.5 / 109.7 / 3984.7 | 0.1 / 0.1 / 0.1 | 779.1 / 169.8 / 4057.8 | 28.073 |
| ig:gold/gold:taberta+rnorm=minmax | 0.1 / 0.1 / 0.1 | 36.9 / 30.4 / 40.0 | 0.2 / 0.2 / 0.2 | 30.2 / 20.6 / 35.1 | 780.0 / 143.2 / 3894.3 | 0.1 / 0.1 / 0.1 | 848.3 / 215.3 / 3950.5 | 30.581 |
| ig:rule/index:taberta+rnorm=minmax | 0.2 / 0.2 / 0.2 | 45.2 / 32.4 / 45.0 | 0.3 / 0.3 / 0.3 | 22.0 / 18.7 / 30.2 | 729.9 / 111.2 / 3973.1 | 0.1 / 0.1 / 0.1 | 798.5 / 194.2 / 4143.8 | 28.779 |

Context index build (one-off, ms): taberta: 402208

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
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
