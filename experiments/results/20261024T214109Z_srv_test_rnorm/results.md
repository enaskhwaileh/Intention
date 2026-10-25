# IGBench results (20261024T214109Z_srv_test_rnorm)

Benchmark `igbench-v1-test` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ig:gold/gold:bm25+rnorm=minmax | 0.861 | 0.550 | 0.350 | 0.940 | 0.975 | 0.950 | 0.000 |
| ig:rule/index:bm25+rnorm=minmax | 0.825 | 0.540 | 0.350 | 0.940 | 0.900 | 0.800 | 0.050 |
| ig:gold/gold:tfidf+rnorm=minmax | 0.828 | 0.520 | 0.340 | 0.925 | 0.912 | 0.850 | 0.000 |
| ig:rule/index:tfidf+rnorm=minmax | 0.813 | 0.500 | 0.335 | 0.917 | 0.887 | 0.800 | 0.050 |
| ig:gold/gold:sbert+rnorm=minmax | 0.769 | 0.470 | 0.310 | 0.869 | 0.917 | 0.850 | 0.000 |
| ig:rule/index:sbert+rnorm=minmax | 0.737 | 0.450 | 0.295 | 0.828 | 0.867 | 0.750 | 0.100 |
| ig:gold/gold:hybrid+rnorm=minmax | 0.878 | 0.560 | 0.355 | 0.948 | 0.975 | 0.950 | 0.000 |
| ig:rule/index:hybrid+rnorm=minmax | 0.852 | 0.560 | 0.355 | 0.948 | 0.925 | 0.850 | 0.050 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ig:gold/gold:bm25+rnorm=minmax | 0.858 | 0.537 | 0.974 | 0.947 |
| ig:rule/index:bm25+rnorm=minmax | 0.820 | 0.526 | 0.895 | 0.789 |
| ig:gold/gold:tfidf+rnorm=minmax | 0.826 | 0.505 | 0.908 | 0.842 |
| ig:rule/index:tfidf+rnorm=minmax | 0.810 | 0.484 | 0.882 | 0.789 |
| ig:gold/gold:sbert+rnorm=minmax | 0.763 | 0.453 | 0.912 | 0.842 |
| ig:rule/index:sbert+rnorm=minmax | 0.728 | 0.432 | 0.860 | 0.737 |
| ig:gold/gold:hybrid+rnorm=minmax | 0.874 | 0.547 | 0.974 | 0.947 |
| ig:rule/index:hybrid+rnorm=minmax | 0.846 | 0.547 | 0.921 | 0.842 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ig:gold/gold:bm25+rnorm=minmax | 0.395 | 0.824 | 0.940 |
| ig:rule/index:bm25+rnorm=minmax | 0.327 | 0.812 | 0.940 |
| ig:gold/gold:tfidf+rnorm=minmax | 0.377 | 0.800 | 0.925 |
| ig:rule/index:tfidf+rnorm=minmax | 0.368 | 0.779 | 0.917 |
| ig:gold/gold:sbert+rnorm=minmax | 0.362 | 0.727 | 0.869 |
| ig:rule/index:sbert+rnorm=minmax | 0.299 | 0.709 | 0.828 |
| ig:gold/gold:hybrid+rnorm=minmax | 0.395 | 0.833 | 0.948 |
| ig:rule/index:hybrid+rnorm=minmax | 0.335 | 0.829 | 0.948 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | compare (n=8) | explain (n=3) | monitor (n=5) | predict (n=4) |
|---|---|---|---|---|
| ig:gold/gold:bm25+rnorm=minmax | 0.801 | 0.825 | 0.876 | 0.918 |
| ig:rule/index:bm25+rnorm=minmax | 0.795 | 0.789 | 0.809 | 0.861 |
| ig:gold/gold:tfidf+rnorm=minmax | 0.774 | 0.759 | 0.885 | 0.892 |
| ig:rule/index:tfidf+rnorm=minmax | 0.771 | 0.759 | 0.842 | 0.878 |
| ig:gold/gold:sbert+rnorm=minmax | 0.740 | 0.759 | 0.747 | 0.871 |
| ig:rule/index:sbert+rnorm=minmax | 0.742 | 0.732 | 0.715 | 0.764 |
| ig:gold/gold:hybrid+rnorm=minmax | 0.823 | 0.839 | 0.913 | 0.916 |
| ig:rule/index:hybrid+rnorm=minmax | 0.824 | 0.792 | 0.871 | 0.869 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ig:gold/gold:bm25+rnorm=minmax | 0.882 |
| ig:rule/index:bm25+rnorm=minmax | 0.882 |
| ig:gold/gold:tfidf+rnorm=minmax | 0.882 |
| ig:rule/index:tfidf+rnorm=minmax | 0.882 |
| ig:gold/gold:sbert+rnorm=minmax | 0.916 |
| ig:rule/index:sbert+rnorm=minmax | 0.900 |
| ig:gold/gold:hybrid+rnorm=minmax | 0.882 |
| ig:rule/index:hybrid+rnorm=minmax | 0.882 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:gold/gold:bm25+rnorm=minmax | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.576 | 0.747 |
| ig:rule/index:bm25+rnorm=minmax | 1.000 | 0.815 | 0.950 | 1.000 | 1.000 | 0.947 | 0.807 | 0.000 | 0.549 | 0.634 |
| ig:gold/gold:tfidf+rnorm=minmax | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.589 | 0.747 |
| ig:rule/index:tfidf+rnorm=minmax | 1.000 | 0.815 | 0.950 | 1.000 | 1.000 | 0.947 | 0.807 | 0.000 | 0.562 | 0.634 |
| ig:gold/gold:sbert+rnorm=minmax | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.639 | 0.768 |
| ig:rule/index:sbert+rnorm=minmax | 1.000 | 0.815 | 0.950 | 1.000 | 1.000 | 0.947 | 0.807 | 0.000 | 0.608 | 0.652 |
| ig:gold/gold:hybrid+rnorm=minmax | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.570 | 0.757 |
| ig:rule/index:hybrid+rnorm=minmax | 1.000 | 0.815 | 0.950 | 1.000 | 1.000 | 0.947 | 0.807 | 0.000 | 0.542 | 0.643 |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ig:gold/gold:bm25+rnorm=minmax | 0.1 / 0.1 / 0.1 | 14.7 / 4.6 / 7.2 | 0.2 / 0.1 / 0.2 | 29.2 / 20.8 / 23.3 | 290.9 / 115.6 / 557.0 | 0.1 / 0.1 / 0.1 | 336.1 / 161.8 / 582.1 | 7.074 |
| ig:rule/index:bm25+rnorm=minmax | 0.5 / 0.2 / 0.7 | 4.8 / 5.1 / 7.0 | 0.3 / 0.2 / 0.3 | 28.8 / 18.3 / 20.1 | 309.2 / 138.7 / 325.4 | 0.1 / 0.1 / 0.1 | 345.0 / 156.8 / 540.7 | 7.264 |
| ig:gold/gold:tfidf+rnorm=minmax | 0.1 / 0.1 / 0.1 | 5.7 / 5.0 / 6.5 | 0.1 / 0.1 / 0.2 | 28.7 / 16.6 / 18.9 | 216.2 / 103.3 / 548.7 | 0.1 / 0.1 / 0.1 | 251.8 / 142.9 / 570.9 | 5.313 |
| ig:rule/index:tfidf+rnorm=minmax | 0.2 / 0.2 / 0.2 | 17.7 / 5.2 / 6.9 | 0.2 / 0.2 / 0.4 | 15.5 / 16.2 / 18.4 | 207.6 / 109.2 / 324.7 | 0.1 / 0.1 / 0.1 | 242.3 / 138.8 / 347.4 | 5.107 |
| ig:gold/gold:sbert+rnorm=minmax | 0.1 / 0.1 / 0.1 | 90.9 / 78.4 / 89.1 | 0.2 / 0.2 / 0.2 | 29.8 / 19.8 / 23.5 | 249.2 / 155.7 / 777.4 | 0.1 / 0.1 / 0.1 | 371.0 / 276.9 / 877.7 | 7.817 |
| ig:rule/index:sbert+rnorm=minmax | 0.2 / 0.2 / 0.2 | 88.8 / 74.8 / 85.5 | 0.3 / 0.3 / 0.3 | 28.2 / 18.6 / 24.2 | 253.7 / 122.2 / 912.1 | 0.1 / 0.1 / 0.1 | 372.1 / 242.5 / 1013.2 | 7.838 |
| ig:gold/gold:hybrid+rnorm=minmax | 0.1 / 0.1 / 0.1 | 82.0 / 80.7 / 88.1 | 0.2 / 0.2 / 0.2 | 28.7 / 18.2 / 22.1 | 343.1 / 112.7 / 952.7 | 0.1 / 0.1 / 0.1 | 455.0 / 216.1 / 1050.4 | 9.584 |
| ig:rule/index:hybrid+rnorm=minmax | 0.2 / 0.2 / 0.2 | 81.4 / 81.3 / 86.6 | 0.3 / 0.3 / 0.3 | 28.0 / 17.7 / 22.4 | 369.6 / 203.5 / 1118.0 | 0.1 / 0.1 / 0.1 | 480.6 / 301.2 / 1337.4 | 10.122 |

Context index build (one-off, ms): bm25: 57 (cached), hybrid: 10546 (cached), sbert: 931 (cached), tfidf: 15 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
