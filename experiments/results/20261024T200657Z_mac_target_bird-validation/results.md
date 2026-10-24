# IGBench results (20261024T200657Z_mac_target_bird-validation)

Benchmark `target-bird-validation` on corpus `target-bird-validation` (1 tables), IL 1.0.0, labels: **established_benchmark_gold**.
Python 3.12.3 on macOS-15.7.9-x86_64-i386-64bit. Warm caches: False.

## RQ1 – usefulness ranking (queries with at least one useful table)

| System | nDCG@10 | P@5 | P@10 | R@10 | MRR | Useful@1 | Topical-only@1 |
|---|---|---|---|---|---|---|---|
| ctx:bm25 | – | – | – | – | – | – | – |
| ig:rule/index:bm25 | – | – | – | – | – | – | – |
| ctx:sbert | – | – | – | – | – | – | – |
| ig:rule/index:sbert | – | – | – | – | – | – | – |

Intention-bearing queries only (gold grounding = grounded):

| System | nDCG@10 | P@5 | MRR | Useful@1 |
|---|---|---|---|---|
| ctx:bm25 | – | – | – | – |
| ig:rule/index:bm25 | – | – | – | – |
| ctx:sbert | – | – | – | – |
| ig:rule/index:sbert | – | – | – | – |

Recall of gold/useful tables at k (TARGET's main retrieval metric):

| System | R@1 | R@5 | R@10 |
|---|---|---|---|
| ctx:bm25 | – | – | – |
| ig:rule/index:bm25 | – | – | – |
| ctx:sbert | – | – | – |
| ig:rule/index:sbert | – | – | – |

## RQ2 – response to a change of intention with a fixed topic

Pairwise intention-swap accuracy: a table useful only for intention *a* ranks above a table useful only for intention *b* in *a*'s ranking (0.5 = indifferent).

| System | Swap accuracy |
|---|---|
| ctx:bm25 | – |
| ig:rule/index:bm25 | – |
| ctx:sbert | – |
| ig:rule/index:sbert | – |

## RQ4 – running time per stage (ms per query: mean / median / p95)

| System | Interpreter | Context matching | Grounder | Profiler | Aligner | Ranking | Total | Wall (s) |
|---|---|---|---|---|---|---|---|---|
| ctx:bm25 | – | – | – | – | – | – | – | 0.0 |
| ig:rule/index:bm25 | – | – | – | – | – | – | – | 0.0 |
| ctx:sbert | – | – | – | – | – | – | – | 0.0 |
| ig:rule/index:sbert | – | – | – | – | – | – | – | 0.0 |

Context index build (one-off, ms): bm25: 4, sbert: 12386

## Significance (paired randomization test, 10,000 permutations; bootstrap 95% CI of the mean difference)

| System | vs | Metric | Δ mean | 95% CI | p | wins/losses |
|---|---|---|---|---|---|---|
