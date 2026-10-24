# IGBench results (20261024T212649Z_srv_dev_ablations)

Benchmark `igbench-v1` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ig:gold/gold:bm25+comb=linear | 0.762 | 0.531 | 0.314 | 0.844 | 0.902 | 0.829 | 0.114 |
| ig:gold/gold:bm25+comb=lexicographic | 0.687 | 0.509 | 0.300 | 0.809 | 0.801 | 0.686 | 0.143 |
| ig:gold/gold:bm25+soft=0 | 0.800 | 0.537 | 0.337 | 0.884 | 0.893 | 0.800 | 0.143 |
| ig:gold/gold:bm25+alpha=0.25 | 0.802 | 0.526 | 0.337 | 0.887 | 0.886 | 0.771 | 0.143 |
| ig:gold/gold:bm25+alpha=0.75 | 0.762 | 0.520 | 0.317 | 0.854 | 0.887 | 0.800 | 0.143 |
| ig:gold/gold:bm25+alpha=1.0 | 0.735 | 0.526 | 0.309 | 0.824 | 0.901 | 0.829 | 0.114 |
| ig:gold/gold:bm25+k=20 | 0.794 | 0.537 | 0.334 | 0.882 | 0.879 | 0.771 | 0.143 |
| ig:gold/gold:bm25+k=100 | 0.796 | 0.537 | 0.334 | 0.882 | 0.879 | 0.771 | 0.143 |
| ig:gold/gold:bm25+bind=0.7 | 0.796 | 0.543 | 0.343 | 0.882 | 0.879 | 0.771 | 0.143 |
| ig:gold/index:bm25 | 0.796 | 0.537 | 0.334 | 0.882 | 0.879 | 0.771 | 0.143 |
| ig:rule/gold:bm25 | 0.781 | 0.503 | 0.329 | 0.865 | 0.898 | 0.829 | 0.114 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ig:gold/gold:bm25+comb=linear | 0.772 | 0.519 | 0.924 | 0.875 |
| ig:gold/gold:bm25+comb=lexicographic | 0.690 | 0.494 | 0.813 | 0.719 |
| ig:gold/gold:bm25+soft=0 | 0.814 | 0.525 | 0.914 | 0.844 |
| ig:gold/gold:bm25+alpha=0.25 | 0.816 | 0.512 | 0.906 | 0.812 |
| ig:gold/gold:bm25+alpha=0.75 | 0.772 | 0.506 | 0.908 | 0.844 |
| ig:gold/gold:bm25+alpha=1.0 | 0.742 | 0.512 | 0.923 | 0.875 |
| ig:gold/gold:bm25+k=20 | 0.807 | 0.525 | 0.898 | 0.812 |
| ig:gold/gold:bm25+k=100 | 0.809 | 0.525 | 0.898 | 0.812 |
| ig:gold/gold:bm25+bind=0.7 | 0.809 | 0.531 | 0.898 | 0.812 |
| ig:gold/index:bm25 | 0.809 | 0.525 | 0.898 | 0.812 |
| ig:rule/gold:bm25 | 0.792 | 0.487 | 0.920 | 0.875 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ig:gold/gold:bm25+comb=linear | 0.349 | 0.781 | 0.844 |
| ig:gold/gold:bm25+comb=lexicographic | 0.316 | 0.748 | 0.809 |
| ig:gold/gold:bm25+soft=0 | 0.316 | 0.781 | 0.884 |
| ig:gold/gold:bm25+alpha=0.25 | 0.311 | 0.756 | 0.887 |
| ig:gold/gold:bm25+alpha=0.75 | 0.340 | 0.757 | 0.854 |
| ig:gold/gold:bm25+alpha=1.0 | 0.349 | 0.767 | 0.824 |
| ig:gold/gold:bm25+k=20 | 0.311 | 0.781 | 0.882 |
| ig:gold/gold:bm25+k=100 | 0.311 | 0.781 | 0.882 |
| ig:gold/gold:bm25+bind=0.7 | 0.311 | 0.781 | 0.882 |
| ig:gold/index:bm25 | 0.311 | 0.781 | 0.882 |
| ig:rule/gold:bm25 | 0.321 | 0.716 | 0.865 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | aggregate (n=3) | compare (n=10) | explain (n=7) | monitor (n=5) | predict (n=8) |
|---|---|---|---|---|---|
| ig:gold/gold:bm25+comb=linear | 0.919 | 0.848 | 0.810 | 0.708 | 0.644 |
| ig:gold/gold:bm25+comb=lexicographic | 0.783 | 0.756 | 0.735 | 0.701 | 0.549 |
| ig:gold/gold:bm25+soft=0 | 0.964 | 0.859 | 0.827 | 0.728 | 0.753 |
| ig:gold/gold:bm25+alpha=0.25 | 0.964 | 0.856 | 0.831 | 0.727 | 0.762 |
| ig:gold/gold:bm25+alpha=0.75 | 0.943 | 0.829 | 0.826 | 0.712 | 0.642 |
| ig:gold/gold:bm25+alpha=1.0 | 0.810 | 0.795 | 0.805 | 0.701 | 0.639 |
| ig:gold/gold:bm25+k=20 | 0.964 | 0.855 | 0.827 | 0.724 | 0.733 |
| ig:gold/gold:bm25+k=100 | 0.964 | 0.855 | 0.827 | 0.728 | 0.741 |
| ig:gold/gold:bm25+bind=0.7 | 0.979 | 0.833 | 0.831 | 0.734 | 0.755 |
| ig:gold/index:bm25 | 0.964 | 0.855 | 0.827 | 0.728 | 0.741 |
| ig:rule/gold:bm25 | 0.979 | 0.808 | 0.802 | 0.672 | 0.780 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ig:gold/gold:bm25+comb=linear | 0.829 |
| ig:gold/gold:bm25+comb=lexicographic | 0.839 |
| ig:gold/gold:bm25+soft=0 | 0.861 |
| ig:gold/gold:bm25+alpha=0.25 | 0.851 |
| ig:gold/gold:bm25+alpha=0.75 | 0.859 |
| ig:gold/gold:bm25+alpha=1.0 | 0.859 |
| ig:gold/gold:bm25+k=20 | 0.863 |
| ig:gold/gold:bm25+k=100 | 0.873 |
| ig:gold/gold:bm25+bind=0.7 | 0.862 |
| ig:gold/index:bm25 | 0.860 |
| ig:rule/gold:bm25 | 0.800 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:gold/gold:bm25+comb=linear | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.497 | 0.789 |
| ig:gold/gold:bm25+comb=lexicographic | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.497 | 0.789 |
| ig:gold/gold:bm25+soft=0 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.497 | 0.789 |
| ig:gold/gold:bm25+alpha=0.25 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.497 | 0.789 |
| ig:gold/gold:bm25+alpha=0.75 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.497 | 0.789 |
| ig:gold/gold:bm25+alpha=1.0 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.497 | 0.789 |
| ig:gold/gold:bm25+k=20 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.603 | 0.784 |
| ig:gold/gold:bm25+k=100 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.453 | 0.797 |
| ig:gold/gold:bm25+bind=0.7 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.623 | 0.740 |
| ig:gold/index:bm25 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.497 | 0.789 |
| ig:rule/gold:bm25 | 1.000 | 0.825 | 0.970 | 0.417 | 0.344 | 0.344 | 0.328 | 0.656 | 0.423 | 0.815 |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ig:gold/gold:bm25+comb=linear | 0.1 / 0.1 / 0.2 | 4.7 / 4.7 / 7.0 | 0.2 / 0.1 / 0.2 | 24.7 / 20.7 / 78.4 | 936.4 / 341.9 / 3828.4 | 0.1 / 0.1 / 0.1 | 967.2 / 396.9 / 3856.0 | 34.852 |
| ig:gold/gold:bm25+comb=lexicographic | 0.1 / 0.1 / 0.1 | 5.2 / 4.9 / 7.4 | 0.1 / 0.1 / 0.2 | 28.5 / 18.0 / 115.9 | 919.2 / 342.6 / 3749.8 | 0.1 / 0.1 / 0.1 | 954.2 / 374.6 / 3776.8 | 34.404 |
| ig:gold/gold:bm25+soft=0 | 0.1 / 0.1 / 0.1 | 5.0 / 4.8 / 7.6 | 0.1 / 0.1 / 0.2 | 25.2 / 18.0 / 107.2 | 926.2 / 346.3 / 3864.7 | 0.1 / 0.1 / 0.1 | 957.6 / 379.4 / 3921.7 | 34.523 |
| ig:gold/gold:bm25+alpha=0.25 | 0.1 / 0.1 / 0.1 | 7.8 / 4.6 / 7.6 | 0.1 / 0.1 / 0.2 | 22.7 / 17.9 / 35.7 | 928.8 / 344.3 / 3750.7 | 0.1 / 0.1 / 0.1 | 960.7 / 378.6 / 3776.6 | 34.636 |
| ig:gold/gold:bm25+alpha=0.75 | 0.1 / 0.1 / 0.1 | 8.2 / 4.7 / 7.8 | 0.1 / 0.1 / 0.2 | 30.8 / 17.9 / 124.7 | 916.2 / 343.7 / 3740.7 | 0.1 / 0.1 / 0.1 | 956.6 / 382.5 / 3817.8 | 34.488 |
| ig:gold/gold:bm25+alpha=1.0 | 0.1 / 0.1 / 0.1 | 8.3 / 4.9 / 8.4 | 0.1 / 0.1 / 0.2 | 33.3 / 18.1 / 130.9 | 932.7 / 364.0 / 3849.5 | 0.1 / 0.1 / 0.1 | 975.7 / 395.9 / 3967.1 | 35.178 |
| ig:gold/gold:bm25+k=20 | 0.1 / 0.1 / 0.1 | 10.5 / 4.9 / 16.4 | 0.1 / 0.1 / 0.2 | 6.8 / 7.2 / 10.3 | 401.1 / 69.7 / 1965.8 | 0.0 / 0.0 / 0.1 | 419.3 / 91.7 / 1978.6 | 15.126 |
| ig:gold/gold:bm25+k=100 | 0.1 / 0.1 / 0.1 | 5.0 / 5.0 / 8.0 | 0.1 / 0.1 / 0.2 | 225.4 / 140.4 / 647.5 | 1319.2 / 618.6 / 4145.5 | 0.2 / 0.2 / 0.2 | 1551.7 / 874.0 / 5162.6 | 55.95 |
| ig:gold/gold:bm25+bind=0.7 | 0.1 / 0.1 / 0.1 | 12.2 / 4.7 / 13.9 | 0.1 / 0.1 / 0.2 | 16.9 / 18.0 / 22.8 | 903.6 / 283.2 / 3817.1 | 0.1 / 0.1 / 0.1 | 933.9 / 314.9 / 3922.9 | 33.682 |
| ig:gold/index:bm25 | 0.1 / 0.1 / 0.1 | 7.8 / 4.5 / 8.2 | 0.3 / 0.2 / 0.3 | 17.0 / 17.8 / 27.6 | 937.8 / 393.7 / 3717.9 | 0.1 / 0.1 / 0.1 | 963.9 / 419.5 / 3745.0 | 34.752 |
| ig:rule/gold:bm25 | 0.4 / 0.1 / 0.7 | 7.2 / 4.3 / 8.5 | 0.1 / 0.1 / 0.1 | 9.0 / 0.0 / 22.0 | 193.3 / 0.0 / 454.7 | 0.1 / 0.1 / 0.1 | 210.8 / 6.2 / 477.5 | 7.604 |

Context index build (one-off, ms): bm25: 64 (cached), lsa: 1700 (cached), tfidf: 11 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
