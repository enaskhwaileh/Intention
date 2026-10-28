# IGBench results (20261025T122627Z_plan_igb-dev_taberta_q14)

Benchmark `igbench-v1` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:taberta | 0.615 | 0.354 | 0.240 | 0.692 | 0.640 | 0.486 | 0.400 |
| ig:llm/llm:taberta | 0.709 | 0.434 | 0.283 | 0.792 | 0.828 | 0.743 | 0.229 |
| ig:llm/llm:taberta+repair=1 | 0.731 | 0.457 | 0.306 | 0.839 | 0.851 | 0.771 | 0.200 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | 0.686 | 0.411 | 0.274 | 0.768 | 0.773 | 0.686 | 0.200 |
| ig:llm/llm:taberta+repair=1+align=0 | 0.627 | 0.349 | 0.249 | 0.728 | 0.625 | 0.457 | 0.400 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:taberta | 0.606 | 0.325 | 0.623 | 0.469 |
| ig:llm/llm:taberta | 0.710 | 0.412 | 0.828 | 0.750 |
| ig:llm/llm:taberta+repair=1 | 0.733 | 0.438 | 0.852 | 0.781 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | 0.684 | 0.388 | 0.768 | 0.688 |
| ig:llm/llm:taberta+repair=1+align=0 | 0.620 | 0.319 | 0.606 | 0.438 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:taberta | 0.207 | 0.538 | 0.692 |
| ig:llm/llm:taberta | 0.294 | 0.663 | 0.792 |
| ig:llm/llm:taberta+repair=1 | 0.303 | 0.691 | 0.839 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | 0.264 | 0.608 | 0.768 |
| ig:llm/llm:taberta+repair=1+align=0 | 0.204 | 0.521 | 0.728 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | aggregate (n=3) | compare (n=10) | explain (n=7) | monitor (n=5) | predict (n=8) |
|---|---|---|---|---|---|
| ctx:taberta | 0.883 | 0.584 | 0.580 | 0.672 | 0.531 |
| ig:llm/llm:taberta | 0.855 | 0.723 | 0.716 | 0.672 | 0.671 |
| ig:llm/llm:taberta+repair=1 | 0.855 | 0.723 | 0.800 | 0.705 | 0.671 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | 0.899 | 0.680 | 0.685 | 0.730 | 0.598 |
| ig:llm/llm:taberta+repair=1+align=0 | 0.912 | 0.601 | 0.575 | 0.701 | 0.550 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:taberta | 0.665 |
| ig:llm/llm:taberta | 0.734 |
| ig:llm/llm:taberta+repair=1 | 0.738 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | 0.719 |
| ig:llm/llm:taberta+repair=1+align=0 | 0.679 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:llm/llm:taberta | 0.778 | 0.779 | 0.920 | 0.639 | 0.594 | 0.594 | 0.578 | 0.406 | 0.581 | 0.672 |
| ig:llm/llm:taberta+repair=1 | 1.000 | 0.746 | 0.909 | 0.806 | 0.781 | 0.781 | 0.703 | 0.219 | 0.584 | 0.720 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | 1.000 | 0.746 | 0.909 | 0.806 | 0.781 | 0.781 | 0.703 | 0.219 | 0.584 | 0.720 |
| ig:llm/llm:taberta+repair=1+align=0 | 1.000 | 0.746 | 0.909 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | – | – |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:taberta | – | 99.7 / 88.5 / 97.0 | – | – | – | – | 99.8 / 88.6 / 97.1 | 3.592 |
| ig:llm/llm:taberta | 6.4 / 6.2 / 11.4 | 89.9 / 89.4 / 99.2 | 1.7 / 1.0 / 4.4 | 18.1 / 17.5 / 51.6 | 597.7 / 44.0 / 3854.7 | 0.2 / 0.1 / 0.5 | 624.6 / 73.6 / 3879.6 | 12.225 |
| ig:llm/llm:taberta+repair=1 | 8.6 / 7.5 / 19.0 | 91.0 / 90.5 / 100.1 | 2.0 / 1.4 / 5.8 | 16.6 / 19.1 / 35.2 | 780.2 / 136.4 / 4041.7 | 0.1 / 0.1 / 0.2 | 808.5 / 167.8 / 4074.2 | 17.168 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | 4.6 / 4.2 / 9.6 | 114.8 / 114.9 / 122.4 | 2.1 / 1.5 / 4.6 | 21.6 / 19.9 / 50.1 | 838.3 / 115.6 / 3715.7 | 0.2 / 0.1 / 0.3 | 867.8 / 167.8 / 3739.9 | 17.129 |
| ig:llm/llm:taberta+repair=1+align=0 | 7.5 / 6.6 / 12.7 | 88.8 / 88.9 / 92.2 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.4 / 0.4 / 0.7 | 8.0 / 7.0 / 13.1 | 3.623 |

Context index build (one-off, ms): taberta: 11769 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:llm/llm:taberta+repair=1 | ctx:taberta | ndcg@10 | +0.115 | [+0.049, +0.182] | 0.001 | 23/8 |
| ig:llm/llm:taberta+repair=1 | ctx:taberta | mrr | +0.210 | [+0.107, +0.320] | 0.000 | 15/1 |
| ig:llm/llm:taberta+repair=1 | ctx:taberta | useful@1 | +0.286 | [+0.143, +0.457] | 0.002 | 10/0 |
| ig:llm/llm:taberta+repair=1+align=0 | ctx:taberta | ndcg@10 | +0.014 | [-0.007, +0.033] | 0.192 | 18/8 |
| ig:llm/llm:taberta+repair=1+align=0 | ctx:taberta | mrr | -0.015 | [-0.053, +0.013] | 0.483 | 7/5 |
| ig:llm/llm:taberta+repair=1+align=0 | ctx:taberta | useful@1 | -0.029 | [-0.086, +0.000] | 1.000 | 0/1 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | ctx:taberta | ndcg@10 | +0.071 | [+0.040, +0.105] | 0.000 | 25/4 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | ctx:taberta | mrr | +0.133 | [+0.060, +0.222] | 0.000 | 14/0 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | ctx:taberta | useful@1 | +0.200 | [+0.086, +0.343] | 0.015 | 7/0 |
| ig:llm/llm:taberta | ctx:taberta | ndcg@10 | +0.094 | [+0.034, +0.161] | 0.006 | 18/6 |
| ig:llm/llm:taberta | ctx:taberta | mrr | +0.188 | [+0.088, +0.294] | 0.000 | 13/1 |
| ig:llm/llm:taberta | ctx:taberta | useful@1 | +0.257 | [+0.114, +0.400] | 0.004 | 9/0 |
