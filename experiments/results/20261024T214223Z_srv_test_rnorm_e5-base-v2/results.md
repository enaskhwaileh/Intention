# IGBench results (20261024T214223Z_srv_test_rnorm_e5-base-v2)

Benchmark `igbench-v1-test` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ig:gold/gold:sbert+rnorm=minmax | 0.819 | 0.570 | 0.330 | 0.916 | 0.942 | 0.900 | 0.000 |
| ig:rule/index:sbert+rnorm=minmax | 0.806 | 0.550 | 0.330 | 0.916 | 0.917 | 0.850 | 0.050 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ig:gold/gold:sbert+rnorm=minmax | 0.818 | 0.558 | 0.939 | 0.895 |
| ig:rule/index:sbert+rnorm=minmax | 0.803 | 0.537 | 0.912 | 0.842 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ig:gold/gold:sbert+rnorm=minmax | 0.390 | 0.855 | 0.916 |
| ig:rule/index:sbert+rnorm=minmax | 0.340 | 0.836 | 0.916 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | compare (n=8) | explain (n=3) | monitor (n=5) | predict (n=4) |
|---|---|---|---|---|
| ig:gold/gold:sbert+rnorm=minmax | 0.713 | 0.869 | 0.827 | 0.885 |
| ig:rule/index:sbert+rnorm=minmax | 0.720 | 0.877 | 0.819 | 0.805 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ig:gold/gold:sbert+rnorm=minmax | 0.863 |
| ig:rule/index:sbert+rnorm=minmax | 0.882 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:gold/gold:sbert+rnorm=minmax | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.628 | 0.761 |
| ig:rule/index:sbert+rnorm=minmax | 1.000 | 0.815 | 0.950 | 1.000 | 1.000 | 0.947 | 0.807 | 0.000 | 0.575 | 0.648 |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ig:gold/gold:sbert+rnorm=minmax | 0.1 / 0.1 / 0.1 | 109.8 / 90.0 / 98.2 | 0.2 / 0.2 / 0.3 | 35.5 / 23.3 / 38.2 | 326.4 / 206.7 / 835.7 | 0.1 / 0.1 / 0.1 | 472.9 / 359.1 / 953.9 | 9.951 |
| ig:rule/index:sbert+rnorm=minmax | 0.5 / 0.2 / 0.7 | 88.3 / 87.4 / 94.9 | 0.3 / 0.3 / 0.4 | 44.3 / 20.3 / 48.0 | 327.6 / 198.2 / 1113.9 | 0.1 / 0.1 / 0.1 | 462.6 / 301.3 / 1231.6 | 9.74 |

Context index build (one-off, ms): sbert: 11072 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
