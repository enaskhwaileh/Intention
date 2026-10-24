# IGBench results (20261024T213945Z_srv_dev_rnorm_bge-base-en-v1.5)

Benchmark `igbench-v1` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ig:gold/gold:sbert+rnorm=minmax | 0.842 | 0.571 | 0.349 | 0.906 | 0.938 | 0.886 | 0.029 |
| ig:rule/index:sbert+rnorm=minmax | 0.837 | 0.560 | 0.349 | 0.905 | 0.929 | 0.886 | 0.029 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ig:gold/gold:sbert+rnorm=minmax | 0.848 | 0.569 | 0.932 | 0.875 |
| ig:rule/index:sbert+rnorm=minmax | 0.842 | 0.556 | 0.922 | 0.875 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ig:gold/gold:sbert+rnorm=minmax | 0.331 | 0.812 | 0.906 |
| ig:rule/index:sbert+rnorm=minmax | 0.356 | 0.808 | 0.905 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | aggregate (n=3) | compare (n=10) | explain (n=7) | monitor (n=5) | predict (n=8) |
|---|---|---|---|---|---|
| ig:gold/gold:sbert+rnorm=minmax | 0.999 | 0.845 | 0.869 | 0.794 | 0.811 |
| ig:rule/index:sbert+rnorm=minmax | 0.999 | 0.857 | 0.874 | 0.723 | 0.810 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ig:gold/gold:sbert+rnorm=minmax | 0.840 |
| ig:rule/index:sbert+rnorm=minmax | 0.840 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:gold/gold:sbert+rnorm=minmax | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.505 | 0.783 |
| ig:rule/index:sbert+rnorm=minmax | 1.000 | 0.825 | 0.970 | 0.833 | 0.812 | 0.812 | 0.688 | 0.188 | 0.480 | 0.778 |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ig:gold/gold:sbert+rnorm=minmax | 0.1 / 0.1 / 0.1 | 104.0 / 85.2 / 101.6 | 0.2 / 0.2 / 0.3 | 37.3 / 21.1 / 216.1 | 880.7 / 271.9 / 4136.4 | 0.1 / 0.1 / 0.1 | 1023.3 / 431.1 / 4467.9 | 36.876 |
| ig:rule/index:sbert+rnorm=minmax | 0.4 / 0.2 / 0.7 | 83.7 / 83.3 / 91.2 | 0.3 / 0.3 / 0.3 | 31.1 / 19.6 / 34.8 | 797.1 / 154.1 / 4190.9 | 0.1 / 0.1 / 0.1 | 913.8 / 277.2 / 4307.5 | 32.936 |

Context index build (one-off, ms): sbert: 10479 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
