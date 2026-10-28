# IGBench results (20261025T122734Z_plan_igb-dev_hybrid_q14)

Benchmark `igbench-v1` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:hybrid | 0.814 | 0.543 | 0.334 | 0.884 | 0.876 | 0.771 | 0.143 |
| ig:llm/llm:hybrid | 0.808 | 0.531 | 0.334 | 0.885 | 0.850 | 0.743 | 0.171 |
| ig:llm/llm:hybrid+repair=1 | 0.811 | 0.531 | 0.337 | 0.889 | 0.869 | 0.771 | 0.143 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | 0.823 | 0.537 | 0.334 | 0.886 | 0.890 | 0.800 | 0.114 |
| ig:llm/llm:hybrid+repair=1+align=0 | 0.808 | 0.543 | 0.331 | 0.881 | 0.852 | 0.743 | 0.171 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:hybrid | 0.821 | 0.525 | 0.896 | 0.812 |
| ig:llm/llm:hybrid | 0.815 | 0.512 | 0.867 | 0.781 |
| ig:llm/llm:hybrid+repair=1 | 0.818 | 0.512 | 0.888 | 0.812 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | 0.831 | 0.519 | 0.911 | 0.844 |
| ig:llm/llm:hybrid+repair=1+align=0 | 0.814 | 0.525 | 0.870 | 0.781 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:hybrid | 0.312 | 0.789 | 0.884 |
| ig:llm/llm:hybrid | 0.308 | 0.777 | 0.885 |
| ig:llm/llm:hybrid+repair=1 | 0.311 | 0.777 | 0.889 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | 0.316 | 0.782 | 0.886 |
| ig:llm/llm:hybrid+repair=1+align=0 | 0.298 | 0.787 | 0.881 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | aggregate (n=3) | compare (n=10) | explain (n=7) | monitor (n=5) | predict (n=8) |
|---|---|---|---|---|---|
| ctx:hybrid | 0.984 | 0.853 | 0.831 | 0.714 | 0.789 |
| ig:llm/llm:hybrid | 0.980 | 0.875 | 0.838 | 0.714 | 0.733 |
| ig:llm/llm:hybrid+repair=1 | 0.980 | 0.875 | 0.843 | 0.726 | 0.733 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | 0.984 | 0.855 | 0.855 | 0.724 | 0.800 |
| ig:llm/llm:hybrid+repair=1+align=0 | 0.984 | 0.856 | 0.818 | 0.711 | 0.773 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:hybrid | 0.808 |
| ig:llm/llm:hybrid | 0.820 |
| ig:llm/llm:hybrid+repair=1 | 0.821 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | 0.818 |
| ig:llm/llm:hybrid+repair=1+align=0 | 0.808 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:llm/llm:hybrid | 0.778 | 0.779 | 0.920 | 0.639 | 0.594 | 0.594 | 0.578 | 0.406 | 0.496 | 0.750 |
| ig:llm/llm:hybrid+repair=1 | 1.000 | 0.746 | 0.909 | 0.806 | 0.781 | 0.781 | 0.703 | 0.219 | 0.494 | 0.774 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | 1.000 | 0.746 | 0.909 | 0.806 | 0.781 | 0.781 | 0.703 | 0.219 | 0.494 | 0.774 |
| ig:llm/llm:hybrid+repair=1+align=0 | 1.000 | 0.746 | 0.909 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | – | – |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:hybrid | – | 112.4 / 102.7 / 126.3 | – | – | – | – | 112.6 / 102.9 / 126.7 | 4.054 |
| ig:llm/llm:hybrid | 6.7 / 2.8 / 42.1 | 91.9 / 84.2 / 118.3 | 1.9 / 1.1 / 4.7 | 15.3 / 18.4 / 43.5 | 649.9 / 59.3 / 3890.8 | 0.2 / 0.1 / 0.7 | 674.8 / 108.8 / 3918.3 | 12.432 |
| ig:llm/llm:hybrid+repair=1 | 7.0 / 6.6 / 14.4 | 83.0 / 80.6 / 93.2 | 3.1 / 1.9 / 7.5 | 131.1 / 37.0 / 744.9 | 1164.1 / 459.2 / 4540.2 | 0.2 / 0.2 / 0.4 | 1306.9 / 686.1 / 4577.3 | 18.111 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | 6.3 / 5.3 / 12.0 | 84.0 / 82.4 / 92.4 | 2.2 / 1.5 / 6.2 | 20.6 / 24.1 / 43.7 | 1020.1 / 200.7 / 4198.6 | 0.2 / 0.2 / 0.2 | 1050.5 / 236.7 / 4227.9 | 17.441 |
| ig:llm/llm:hybrid+repair=1+align=0 | 7.1 / 4.2 / 21.9 | 98.9 / 91.7 / 139.6 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.6 / 0.5 / 1.1 | 7.8 / 4.7 / 22.5 | 4.08 |

Context index build (one-off, ms): hybrid: 11149 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:llm/llm:hybrid+repair=1+align=0 | ctx:hybrid | ndcg@10 | -0.006 | [-0.014, +0.001] | 0.120 | 6/11 |
| ig:llm/llm:hybrid+repair=1+align=0 | ctx:hybrid | mrr | -0.024 | [-0.062, +0.000] | 0.247 | 0/3 |
| ig:llm/llm:hybrid+repair=1+align=0 | ctx:hybrid | useful@1 | -0.029 | [-0.086, +0.000] | 1.000 | 0/1 |
| ig:llm/llm:hybrid+repair=1 | ctx:hybrid | ndcg@10 | -0.003 | [-0.028, +0.020] | 0.853 | 13/13 |
| ig:llm/llm:hybrid+repair=1 | ctx:hybrid | mrr | -0.007 | [-0.069, +0.050] | 0.748 | 1/2 |
| ig:llm/llm:hybrid+repair=1 | ctx:hybrid | useful@1 | +0.000 | [-0.086, +0.086] | 1.000 | 1/1 |
| ig:llm/llm:hybrid | ctx:hybrid | ndcg@10 | -0.005 | [-0.028, +0.014] | 0.734 | 9/10 |
| ig:llm/llm:hybrid | ctx:hybrid | mrr | -0.026 | [-0.074, +0.000] | 0.504 | 0/2 |
| ig:llm/llm:hybrid | ctx:hybrid | useful@1 | -0.029 | [-0.086, +0.000] | 1.000 | 0/1 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | ctx:hybrid | ndcg@10 | +0.009 | [-0.003, +0.023] | 0.170 | 13/11 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | ctx:hybrid | mrr | +0.014 | [-0.014, +0.057] | 1.000 | 1/1 |
| ig:llm/llm:hybrid+repair=1+rnorm=minmax | ctx:hybrid | useful@1 | +0.029 | [+0.000, +0.086] | 1.000 | 1/0 |
