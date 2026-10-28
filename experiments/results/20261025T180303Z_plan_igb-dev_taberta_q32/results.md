# IGBench results (20261025T180303Z_plan_igb-dev_taberta_q32)

Benchmark `igbench-v1` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:taberta | 0.615 | 0.354 | 0.240 | 0.692 | 0.640 | 0.486 | 0.400 |
| ig:llm/llm:taberta | 0.677 | 0.406 | 0.271 | 0.751 | 0.777 | 0.686 | 0.257 |
| ig:llm/llm:taberta+repair=1 | 0.715 | 0.440 | 0.297 | 0.811 | 0.838 | 0.771 | 0.171 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | 0.678 | 0.394 | 0.277 | 0.775 | 0.767 | 0.686 | 0.200 |
| ig:llm/llm:taberta+repair=1+align=0 | 0.625 | 0.349 | 0.249 | 0.728 | 0.625 | 0.457 | 0.400 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:taberta | 0.606 | 0.325 | 0.623 | 0.469 |
| ig:llm/llm:taberta | 0.674 | 0.381 | 0.771 | 0.688 |
| ig:llm/llm:taberta+repair=1 | 0.716 | 0.419 | 0.839 | 0.781 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | 0.675 | 0.369 | 0.761 | 0.688 |
| ig:llm/llm:taberta+repair=1+align=0 | 0.618 | 0.319 | 0.606 | 0.438 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:taberta | 0.207 | 0.538 | 0.692 |
| ig:llm/llm:taberta | 0.274 | 0.607 | 0.751 |
| ig:llm/llm:taberta+repair=1 | 0.303 | 0.664 | 0.811 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | 0.264 | 0.577 | 0.775 |
| ig:llm/llm:taberta+repair=1+align=0 | 0.204 | 0.521 | 0.728 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | aggregate (n=3) | compare (n=10) | explain (n=7) | monitor (n=5) | predict (n=8) |
|---|---|---|---|---|---|
| ctx:taberta | 0.883 | 0.584 | 0.580 | 0.672 | 0.531 |
| ig:llm/llm:taberta | 0.912 | 0.689 | 0.641 | 0.693 | 0.601 |
| ig:llm/llm:taberta+repair=1 | 0.912 | 0.702 | 0.787 | 0.731 | 0.601 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | 0.912 | 0.667 | 0.687 | 0.714 | 0.582 |
| ig:llm/llm:taberta+repair=1+align=0 | 0.912 | 0.601 | 0.575 | 0.685 | 0.550 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:taberta | 0.665 |
| ig:llm/llm:taberta | 0.700 |
| ig:llm/llm:taberta+repair=1 | 0.743 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | 0.724 |
| ig:llm/llm:taberta+repair=1+align=0 | 0.679 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:llm/llm:taberta | 0.750 | 0.853 | 0.958 | 0.556 | 0.531 | 0.500 | 0.516 | 0.469 | 0.562 | 0.610 |
| ig:llm/llm:taberta+repair=1 | 0.944 | 0.774 | 0.935 | 0.750 | 0.719 | 0.688 | 0.630 | 0.281 | 0.604 | 0.688 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | 0.944 | 0.774 | 0.935 | 0.750 | 0.719 | 0.688 | 0.630 | 0.281 | 0.604 | 0.688 |
| ig:llm/llm:taberta+repair=1+align=0 | 0.944 | 0.774 | 0.935 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | – | – |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:taberta | – | 93.5 / 81.6 / 90.5 | – | – | – | – | 93.5 / 81.7 / 90.6 | 3.367 |
| ig:llm/llm:taberta | 5.4 / 5.2 / 9.6 | 83.4 / 81.9 / 90.8 | 1.6 / 0.9 / 4.0 | 12.8 / 0.0 / 34.3 | 822.5 / 0.0 / 3823.3 | 0.2 / 0.1 / 0.6 | 843.1 / 8.9 / 3862.5 | 20.183 |
| ig:llm/llm:taberta+repair=1 | 9.5 / 8.6 / 16.6 | 84.3 / 83.8 / 88.7 | 1.9 / 1.5 / 4.3 | 16.1 / 18.5 / 32.6 | 941.1 / 77.0 / 3897.0 | 0.1 / 0.1 / 0.4 | 969.5 / 113.7 / 3933.7 | 19.753 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | 7.9 / 6.4 / 16.8 | 84.0 / 82.9 / 95.7 | 1.8 / 1.3 / 5.1 | 65.7 / 18.2 / 395.1 | 976.6 / 73.8 / 3853.7 | 0.2 / 0.1 / 0.6 | 1053.1 / 98.4 / 4256.0 | 19.856 |
| ig:llm/llm:taberta+repair=1+align=0 | 7.8 / 7.1 / 14.5 | 83.5 / 82.1 / 89.1 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.4 / 0.4 / 0.7 | 8.3 / 7.7 / 14.8 | 3.545 |

Context index build (one-off, ms): taberta: 10969 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:llm/llm:taberta+repair=1 | ctx:taberta | ndcg@10 | +0.099 | [+0.023, +0.173] | 0.013 | 23/7 |
| ig:llm/llm:taberta+repair=1 | ctx:taberta | mrr | +0.198 | [+0.091, +0.310] | 0.000 | 14/2 |
| ig:llm/llm:taberta+repair=1 | ctx:taberta | useful@1 | +0.286 | [+0.143, +0.457] | 0.002 | 10/0 |
| ig:llm/llm:taberta+repair=1+align=0 | ctx:taberta | ndcg@10 | +0.012 | [-0.009, +0.031] | 0.258 | 17/8 |
| ig:llm/llm:taberta+repair=1+align=0 | ctx:taberta | mrr | -0.015 | [-0.053, +0.013] | 0.483 | 7/5 |
| ig:llm/llm:taberta+repair=1+align=0 | ctx:taberta | useful@1 | -0.029 | [-0.086, +0.000] | 1.000 | 0/1 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | ctx:taberta | ndcg@10 | +0.064 | [+0.032, +0.097] | 0.001 | 23/6 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | ctx:taberta | mrr | +0.127 | [+0.049, +0.219] | 0.002 | 14/1 |
| ig:llm/llm:taberta+repair=1+rnorm=minmax | ctx:taberta | useful@1 | +0.200 | [+0.086, +0.343] | 0.015 | 7/0 |
| ig:llm/llm:taberta | ctx:taberta | ndcg@10 | +0.062 | [-0.006, +0.134] | 0.089 | 18/5 |
| ig:llm/llm:taberta | ctx:taberta | mrr | +0.136 | [+0.045, +0.237] | 0.006 | 10/2 |
| ig:llm/llm:taberta | ctx:taberta | useful@1 | +0.200 | [+0.086, +0.343] | 0.016 | 7/0 |
