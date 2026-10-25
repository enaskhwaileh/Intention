# IGBench results (20261024T213828Z_srv_dev_rnorm_e5-base-v2)

Benchmark `igbench-v1` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ig:gold/gold:sbert+rnorm=minmax | 0.836 | 0.566 | 0.349 | 0.908 | 0.922 | 0.886 | 0.057 |
| ig:rule/index:sbert+rnorm=minmax | 0.811 | 0.566 | 0.340 | 0.897 | 0.898 | 0.829 | 0.086 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ig:gold/gold:sbert+rnorm=minmax | 0.843 | 0.544 | 0.936 | 0.906 |
| ig:rule/index:sbert+rnorm=minmax | 0.816 | 0.544 | 0.909 | 0.844 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ig:gold/gold:sbert+rnorm=minmax | 0.336 | 0.780 | 0.908 |
| ig:rule/index:sbert+rnorm=minmax | 0.353 | 0.811 | 0.897 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | aggregate (n=3) | compare (n=10) | explain (n=7) | monitor (n=5) | predict (n=8) |
|---|---|---|---|---|---|
| ig:gold/gold:sbert+rnorm=minmax | 0.925 | 0.844 | 0.855 | 0.782 | 0.827 |
| ig:rule/index:sbert+rnorm=minmax | 0.926 | 0.853 | 0.817 | 0.733 | 0.771 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ig:gold/gold:sbert+rnorm=minmax | 0.833 |
| ig:rule/index:sbert+rnorm=minmax | 0.835 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:gold/gold:sbert+rnorm=minmax | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.520 | 0.792 |
| ig:rule/index:sbert+rnorm=minmax | 1.000 | 0.825 | 0.970 | 0.833 | 0.812 | 0.812 | 0.688 | 0.188 | 0.494 | 0.783 |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ig:gold/gold:sbert+rnorm=minmax | 0.1 / 0.1 / 0.1 | 97.4 / 84.6 / 100.2 | 0.2 / 0.2 / 0.3 | 33.7 / 21.7 / 36.6 | 890.5 / 310.0 / 3870.4 | 0.1 / 0.1 / 0.1 | 1023.1 / 427.5 / 3981.6 | 36.874 |
| ig:rule/index:sbert+rnorm=minmax | 0.4 / 0.2 / 0.7 | 85.5 / 84.6 / 92.6 | 0.3 / 0.3 / 0.3 | 24.5 / 20.2 / 36.6 | 661.2 / 241.2 / 2581.8 | 0.1 / 0.1 / 0.1 | 773.1 / 353.7 / 2714.2 | 27.873 |

Context index build (one-off, ms): sbert: 10774 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
