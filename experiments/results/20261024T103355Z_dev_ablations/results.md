# IGBench results (20261024T103355Z_dev_ablations)

Benchmark `igbench-v1` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.13.17 on Linux-6.18.44-fc-v153-x86_64-with-glibc2.39. Warm caches: False.

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
| ig:gold/gold:bm25+comb=linear | 0.1 / 0.1 / 0.2 | 5.5 / 5.6 / 8.8 | 0.2 / 0.2 / 0.3 | 12.3 / 9.2 / 20.3 | 909.0 / 401.4 / 3527.0 | 0.1 / 0.1 / 0.2 | 928.5 / 423.7 / 3550.4 | 33.465 |
| ig:gold/gold:bm25+comb=lexicographic | 0.1 / 0.1 / 0.1 | 6.5 / 6.2 / 12.3 | 0.2 / 0.2 / 0.3 | 14.6 / 10.6 / 23.9 | 1011.8 / 366.0 / 3732.2 | 0.1 / 0.1 / 0.2 | 1034.7 / 386.8 / 3766.8 | 37.309 |
| ig:gold/gold:bm25+soft=0 | 0.1 / 0.1 / 0.2 | 11.9 / 6.3 / 12.0 | 0.2 / 0.2 / 0.3 | 14.4 / 10.7 / 17.4 | 943.7 / 379.2 / 3416.9 | 0.1 / 0.1 / 0.2 | 971.8 / 393.9 / 3436.4 | 35.049 |
| ig:gold/gold:bm25+alpha=0.25 | 0.1 / 0.1 / 0.2 | 7.4 / 7.5 / 12.2 | 0.2 / 0.2 / 0.4 | 12.1 / 12.5 / 20.5 | 1045.5 / 422.6 / 3655.1 | 0.1 / 0.1 / 0.2 | 1067.0 / 446.7 / 3680.4 | 38.482 |
| ig:gold/gold:bm25+alpha=0.75 | 0.1 / 0.1 / 0.2 | 6.5 / 5.9 / 12.3 | 0.2 / 0.2 / 0.3 | 15.8 / 11.8 / 18.8 | 1071.0 / 437.9 / 4419.5 | 0.1 / 0.1 / 0.2 | 1095.2 / 450.9 / 4442.3 | 39.49 |
| ig:gold/gold:bm25+alpha=1.0 | 0.1 / 0.1 / 0.2 | 6.7 / 6.4 / 11.8 | 0.2 / 0.2 / 0.3 | 18.0 / 11.4 / 25.3 | 989.2 / 373.0 / 3940.6 | 0.1 / 0.1 / 0.2 | 1015.8 / 396.0 / 3974.8 | 36.638 |
| ig:gold/gold:bm25+k=20 | 0.1 / 0.1 / 0.1 | 5.5 / 5.3 / 11.3 | 0.2 / 0.2 / 0.3 | 4.1 / 3.6 / 7.4 | 767.8 / 71.4 / 3748.3 | 0.1 / 0.0 / 0.1 | 778.5 / 82.0 / 3767.2 | 28.06 |
| ig:gold/gold:bm25+k=100 | 0.1 / 0.1 / 0.2 | 6.6 / 6.1 / 13.0 | 0.2 / 0.2 / 0.3 | 730.1 / 347.9 / 2277.4 | 1614.8 / 781.5 / 4047.2 | 0.3 / 0.3 / 0.4 | 2354.6 / 1455.0 / 6625.4 | 84.875 |
| ig:gold/gold:bm25+bind=0.7 | 0.1 / 0.1 / 0.2 | 6.7 / 6.8 / 12.3 | 0.2 / 0.2 / 0.4 | 16.8 / 11.7 / 19.0 | 992.3 / 371.2 / 3780.3 | 0.1 / 0.1 / 0.2 | 1017.6 / 394.6 / 3800.0 | 36.724 |
| ig:gold/index:bm25 | 0.1 / 0.1 / 0.1 | 6.9 / 6.3 / 12.9 | 0.4 / 0.4 / 0.6 | 17.7 / 12.4 / 18.7 | 1078.8 / 454.7 / 3984.8 | 0.1 / 0.1 / 0.2 | 1105.5 / 472.7 / 4015.1 | 39.872 |
| ig:rule/gold:bm25 | 0.4 / 0.2 / 1.1 | 6.9 / 7.4 / 11.5 | 0.2 / 0.2 / 0.3 | 5.3 / 0.0 / 18.7 | 223.1 / 0.0 / 844.3 | 0.1 / 0.1 / 0.2 | 237.3 / 9.9 / 871.0 | 8.567 |

Context index build (one-off, ms): bm25: 46 (cached), lsa: 1076 (cached), tfidf: 9 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
