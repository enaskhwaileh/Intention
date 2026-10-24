# IGBench results (20261024T213340Z_srv_dev_rnorm)

Benchmark `igbench-v1` on corpus `igbench-v1` (3300 tables), IL 1.0.0, labels: **draft_author_labels_unreviewed**.
Python 3.11.17 on Linux-5.15.0-151-generic-x86_64-with-glibc2.35. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ig:gold/gold:bm25+rnorm=minmax | 0.798 | 0.537 | 0.337 | 0.884 | 0.881 | 0.771 | 0.143 |
| ig:rule/index:bm25+rnorm=minmax | 0.797 | 0.526 | 0.337 | 0.884 | 0.906 | 0.829 | 0.114 |
| ig:gold/gold:tfidf+rnorm=minmax | 0.789 | 0.514 | 0.329 | 0.863 | 0.862 | 0.743 | 0.171 |
| ig:rule/index:tfidf+rnorm=minmax | 0.755 | 0.503 | 0.317 | 0.826 | 0.835 | 0.714 | 0.143 |
| ig:gold/gold:sbert+rnorm=minmax | 0.812 | 0.520 | 0.311 | 0.832 | 0.905 | 0.857 | 0.114 |
| ig:rule/index:sbert+rnorm=minmax | 0.789 | 0.520 | 0.311 | 0.855 | 0.860 | 0.800 | 0.143 |
| ig:gold/gold:hybrid+rnorm=minmax | 0.820 | 0.549 | 0.331 | 0.878 | 0.876 | 0.771 | 0.143 |
| ig:rule/index:hybrid+rnorm=minmax | 0.822 | 0.554 | 0.334 | 0.886 | 0.881 | 0.771 | 0.114 |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ig:gold/gold:bm25+rnorm=minmax | 0.812 | 0.525 | 0.901 | 0.812 |
| ig:rule/index:bm25+rnorm=minmax | 0.810 | 0.512 | 0.928 | 0.875 |
| ig:gold/gold:tfidf+rnorm=minmax | 0.803 | 0.512 | 0.880 | 0.781 |
| ig:rule/index:tfidf+rnorm=minmax | 0.766 | 0.500 | 0.850 | 0.750 |
| ig:gold/gold:sbert+rnorm=minmax | 0.815 | 0.500 | 0.897 | 0.844 |
| ig:rule/index:sbert+rnorm=minmax | 0.790 | 0.500 | 0.847 | 0.781 |
| ig:gold/gold:hybrid+rnorm=minmax | 0.828 | 0.531 | 0.896 | 0.812 |
| ig:rule/index:hybrid+rnorm=minmax | 0.830 | 0.537 | 0.901 | 0.812 |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ig:gold/gold:bm25+rnorm=minmax | 0.311 | 0.772 | 0.884 |
| ig:rule/index:bm25+rnorm=minmax | 0.321 | 0.767 | 0.884 |
| ig:gold/gold:tfidf+rnorm=minmax | 0.308 | 0.743 | 0.863 |
| ig:rule/index:tfidf+rnorm=minmax | 0.270 | 0.706 | 0.826 |
| ig:gold/gold:sbert+rnorm=minmax | 0.334 | 0.754 | 0.832 |
| ig:rule/index:sbert+rnorm=minmax | 0.301 | 0.757 | 0.855 |
| ig:gold/gold:hybrid+rnorm=minmax | 0.311 | 0.792 | 0.878 |
| ig:rule/index:hybrid+rnorm=minmax | 0.313 | 0.801 | 0.886 |

nDCG@10 by analytical operation / intention family (n = queries):

| System | aggregate (n=3) | compare (n=10) | explain (n=7) | monitor (n=5) | predict (n=8) |
|---|---|---|---|---|---|
| ig:gold/gold:bm25+rnorm=minmax | 0.964 | 0.848 | 0.831 | 0.728 | 0.754 |
| ig:rule/index:bm25+rnorm=minmax | 0.965 | 0.833 | 0.812 | 0.694 | 0.804 |
| ig:gold/gold:tfidf+rnorm=minmax | 0.937 | 0.843 | 0.815 | 0.708 | 0.754 |
| ig:rule/index:tfidf+rnorm=minmax | 0.937 | 0.760 | 0.790 | 0.645 | 0.770 |
| ig:gold/gold:sbert+rnorm=minmax | 0.984 | 0.826 | 0.865 | 0.714 | 0.759 |
| ig:rule/index:sbert+rnorm=minmax | 0.984 | 0.796 | 0.842 | 0.669 | 0.743 |
| ig:gold/gold:hybrid+rnorm=minmax | 0.984 | 0.862 | 0.845 | 0.748 | 0.774 |
| ig:rule/index:hybrid+rnorm=minmax | 0.984 | 0.866 | 0.839 | 0.717 | 0.801 |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ig:gold/gold:bm25+rnorm=minmax | 0.861 |
| ig:rule/index:bm25+rnorm=minmax | 0.823 |
| ig:gold/gold:tfidf+rnorm=minmax | 0.812 |
| ig:rule/index:tfidf+rnorm=minmax | 0.807 |
| ig:gold/gold:sbert+rnorm=minmax | 0.753 |
| ig:rule/index:sbert+rnorm=minmax | 0.777 |
| ig:gold/gold:hybrid+rnorm=minmax | 0.828 |
| ig:rule/index:hybrid+rnorm=minmax | 0.839 |

## RQ3 – interpretation, grounding and assessment accuracy

| System | Intention presence | Argument F1 | Scope F1 | Grounding status | Family | Variant | Binding acc. | Fallback rate | Assessment P | Assessment R |
|---|---|---|---|---|---|---|---|---|---|---|
| ig:gold/gold:bm25+rnorm=minmax | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.497 | 0.789 |
| ig:rule/index:bm25+rnorm=minmax | 1.000 | 0.825 | 0.970 | 0.833 | 0.812 | 0.812 | 0.688 | 0.188 | 0.482 | 0.784 |
| ig:gold/gold:tfidf+rnorm=minmax | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.538 | 0.803 |
| ig:rule/index:tfidf+rnorm=minmax | 1.000 | 0.825 | 0.970 | 0.833 | 0.812 | 0.812 | 0.688 | 0.188 | 0.497 | 0.802 |
| ig:gold/gold:sbert+rnorm=minmax | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.535 | 0.771 |
| ig:rule/index:sbert+rnorm=minmax | 1.000 | 0.825 | 0.970 | 0.833 | 0.812 | 0.812 | 0.688 | 0.188 | 0.479 | 0.753 |
| ig:gold/gold:hybrid+rnorm=minmax | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.507 | 0.795 |
| ig:rule/index:hybrid+rnorm=minmax | 1.000 | 0.825 | 0.970 | 0.833 | 0.812 | 0.812 | 0.688 | 0.188 | 0.474 | 0.788 |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ig:gold/gold:bm25+rnorm=minmax | 0.1 / 0.1 / 0.1 | 4.7 / 4.6 / 7.0 | 0.1 / 0.1 / 0.2 | 27.0 / 21.7 / 27.6 | 967.7 / 353.7 / 3925.4 | 0.1 / 0.1 / 0.1 | 1000.8 / 420.7 / 3957.2 | 36.059 |
| ig:rule/index:bm25+rnorm=minmax | 0.4 / 0.2 / 0.7 | 4.8 / 5.0 / 7.8 | 0.2 / 0.2 / 0.4 | 21.6 / 18.1 / 26.8 | 865.9 / 148.3 / 3781.4 | 0.1 / 0.1 / 0.1 | 894.1 / 171.0 / 3809.9 | 32.222 |
| ig:gold/gold:tfidf+rnorm=minmax | 0.1 / 0.1 / 0.1 | 6.1 / 5.3 / 7.1 | 0.1 / 0.1 / 0.2 | 15.9 / 17.5 / 21.3 | 890.9 / 250.2 / 3902.6 | 0.1 / 0.1 / 0.1 | 914.1 / 276.8 / 3930.6 | 32.948 |
| ig:rule/index:tfidf+rnorm=minmax | 0.2 / 0.2 / 0.2 | 19.8 / 5.1 / 10.1 | 0.2 / 0.2 / 0.3 | 12.9 / 16.6 / 21.0 | 763.8 / 121.7 / 3704.9 | 0.1 / 0.1 / 0.1 | 797.9 / 178.2 / 3731.3 | 28.76 |
| ig:gold/gold:sbert+rnorm=minmax | 0.1 / 0.1 / 0.1 | 83.7 / 76.2 / 85.0 | 0.2 / 0.2 / 0.2 | 27.3 / 20.8 / 37.7 | 854.5 / 252.1 / 4001.0 | 0.1 / 0.1 / 0.1 | 966.7 / 351.7 / 4101.5 | 34.859 |
| ig:rule/index:sbert+rnorm=minmax | 0.2 / 0.2 / 0.2 | 77.7 / 77.0 / 84.5 | 0.2 / 0.2 / 0.3 | 30.0 / 19.0 / 37.5 | 791.9 / 165.5 / 4087.3 | 0.1 / 0.1 / 0.1 | 901.0 / 260.4 / 4193.5 | 32.487 |
| ig:gold/gold:hybrid+rnorm=minmax | 0.1 / 0.1 / 0.1 | 84.9 / 84.5 / 92.1 | 0.2 / 0.2 / 0.2 | 34.1 / 19.5 / 38.8 | 991.4 / 284.9 / 4214.2 | 0.1 / 0.1 / 0.1 | 1111.8 / 414.5 / 4338.2 | 40.076 |
| ig:rule/index:hybrid+rnorm=minmax | 0.2 / 0.2 / 0.2 | 90.9 / 83.1 / 93.0 | 0.2 / 0.3 / 0.3 | 22.0 / 18.1 / 34.9 | 918.2 / 184.4 / 3923.5 | 0.1 / 0.1 / 0.1 | 1032.5 / 369.7 / 4022.2 | 37.214 |

Context index build (one-off, ms): bm25: 60 (cached), hybrid: 10638 (cached), sbert: 1047 (cached), tfidf: 16 (cached)

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
