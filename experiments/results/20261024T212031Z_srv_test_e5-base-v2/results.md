# IGBench results (20261024T212031Z_srv_test_e5-base-v2)

Benchmark `igbench-v1-test` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:sbert | 0.778 | 0.490 | 0.305 | 0.880 | 0.950 | 0.900 | 0.000 |
| ig:gold/gold:sbert | 0.781 | 0.550 | 0.335 | 0.928 | 0.908 | 0.850 | 0.000 |
| ig:rule/index:sbert | 0.727 | 0.500 | 0.325 | 0.874 | 0.847 | 0.800 | 0.050 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:sbert | 0.775 | 0.474 | 0.947 | 0.895 |
| ig:gold/gold:sbert | 0.778 | 0.537 | 0.903 | 0.842 |
| ig:rule/index:sbert | 0.721 | 0.484 | 0.839 | 0.789 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:sbert | 0.390 | 0.778 | 0.880 |
| ig:gold/gold:sbert | 0.340 | 0.800 | 0.928 |
| ig:rule/index:sbert | 0.290 | 0.709 | 0.874 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | compare (n=8) | explain (n=3) | monitor (n=5) | predict (n=4) |
|---|---|---|---|---|
| ctx:sbert | 0.731 | 0.783 | 0.755 | 0.853 |
| ig:gold/gold:sbert | 0.717 | 0.863 | 0.704 | 0.845 |
| ig:rule/index:sbert | 0.715 | 0.846 | 0.685 | 0.613 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:sbert | 0.875 |
| ig:gold/gold:sbert | 0.862 |
| ig:rule/index:sbert | 0.920 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:gold/gold:sbert | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.628 | 0.761 |
| ig:rule/index:sbert | 1.000 | 0.815 | 0.950 | 1.000 | 1.000 | 0.947 | 0.807 | 0.000 | 0.575 | 0.648 |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:sbert | – | 100.8 / 88.4 / 100.7 | – | – | – | – | 100.9 / 88.5 / 100.7 | 2.119 |
| ig:gold/gold:sbert | 0.1 / 0.1 / 0.1 | 91.4 / 93.1 / 99.4 | 0.2 / 0.2 / 0.3 | 130.6 / 67.3 / 335.3 | 334.5 / 230.3 / 804.9 | 0.1 / 0.1 / 0.1 | 557.9 / 448.4 / 1003.0 | 11.74 |
| ig:rule/index:sbert | 0.4 / 0.2 / 0.8 | 89.9 / 90.3 / 95.6 | 0.3 / 0.3 / 0.4 | 76.5 / 29.0 / 254.4 | 343.7 / 211.4 / 1105.7 | 0.1 / 0.1 / 0.1 | 512.3 / 418.1 / 1222.3 | 10.785 |

Context index build (one-off, ms): sbert: 63095

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
| ig:rule/index:sbert | ctx:sbert | ndcg@10 | -0.059 | [-0.148, +0.017] | 0.239 | 11/8 |
| ig:rule/index:sbert | ctx:sbert | mrr | -0.103 | [-0.236, +0.000] | 0.251 | 0/3 |
| ig:rule/index:sbert | ctx:sbert | useful@1 | -0.100 | [-0.250, +0.000] | 0.496 | 0/2 |
| ig:gold/gold:sbert | ctx:sbert | ndcg@10 | -0.008 | [-0.061, +0.042] | 0.779 | 11/8 |
| ig:gold/gold:sbert | ctx:sbert | mrr | -0.042 | [-0.108, +0.000] | 0.499 | 0/2 |
| ig:gold/gold:sbert | ctx:sbert | useful@1 | -0.050 | [-0.150, +0.000] | 1.000 | 0/1 |
