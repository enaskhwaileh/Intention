# Milestone 7B topical encoder bakeoff

## Purpose and boundary

Milestone 7B freezes a development-only comparison of topical first-stage
retrievers over the verified 1,652,771-table WikiTables corpus. It selects an
open semantic encoder using canonical topical queries and historical topical
qrels only. It does not use intended actions, action arguments, requirements,
capability profiles, or usefulness labels. This is model selection, not a
final paper effectiveness result. Milestone 7C has not started.

The canonical qrels contain 3,120 judgments for 2,932 unique tables with labels
0/1/2. They are historically pooled and incomplete. `KnownRelevantRecall`
therefore means recall of known tables with label at least 1, never exhaustive
corpus recall; unjudged tables remain unjudged.

## Frozen candidates and evidence

All dense conditions consume `neural_table_evidence_v1` and the canonical
topical query only.

| Condition | Exact identity | Dimension | Role |
|---|---|---:|---|
| Qwen 0.6B | `Qwen/Qwen3-Embedding-0.6B@97b0c614be4d77ee51c0cef4e5f07c00f9eb65b3` | 1024 | eligible open model |
| Qwen 4B | `Qwen/Qwen3-Embedding-4B@5cf2132abc99cad020ac570b19d031efec650f2b` | 2560 | eligible open model |
| Nemotron 1B | `nvidia/Nemotron-3-Embed-1B-BF16@f880174635613cff04033875fc6a69296cb72006` | 2048 | eligible open model |
| BM25 | frozen repository adapter | — | lexical reference, ineligible |
| Gemini | `gemini-embedding-2` alias | 1536 | proprietary ceiling, ineligible |
| Voyage | `voyage-4-large` alias | 1024 | proprietary ceiling, ineligible |

Qwen uses the frozen table-discovery query wrapper, no document instruction,
model-defined SentenceTransformers pooling, and L2 normalization. Nemotron
uses only `query: ` and `passage: `, model-defined average pooling and
normalization, and its OpenMDW-1.1 license. All local adapters require
`trust_remote_code=false`; quantization, fine-tuning, prompt tuning, and
dimension tuning are forbidden. Qwen 8B, Cohere, and substitutes are excluded.
API aliases cannot win because they do not identify immutable checkpoints.

## Split, metrics, and selection

`m7b-topic-split-v1` sorts
`SHA256("m7b-topic-split-v1|" + query_id)` independently in QS1 (1–30) and QS2
(31–60), assigning the first 15 of each stratum to development. Development:

`1, 3, 5, 6, 8, 11, 13, 15, 16, 17, 19, 27, 28, 29, 30, 32, 34, 37, 39, 41, 43, 44, 45, 48, 49, 52, 53, 57, 58, 60`.

Locked holdout:

`2, 4, 7, 9, 10, 12, 14, 18, 20, 21, 22, 23, 24, 25, 26, 31, 33, 35, 36, 38, 40, 42, 46, 47, 50, 51, 54, 55, 56, 59`.

The evaluator rejects locked IDs. Selection requires exact full-corpus cosine
top-100 retrieval. Approximate HNSW may be timed separately but cannot select
the model. Primary is macro KnownRelevantRecall@100; sensitivity depths are
5/10/20/50/100. Secondary diagnostics are graded nDCG@10, MRR@10 at topical
label at least 2, bpref at label at least 1, judged/unjudged counts and rates,
QS1/QS2 macros, and diagnostic 95% paired topic-bootstrap intervals.

The only winner rule is Recall@100 when the top-two absolute gap exceeds 0.01;
otherwise bpref when its gap exceeds 0.01; otherwise lower embedding wall time;
if times are within 10%, smaller physical index. K is then the smallest frozen
depth reaching 98% of the winner's development Recall@100. Only after both
freezes may RRF (`k=60`) run as a diagnostic; it cannot change the encoder.

## Corrected bpref and zero-spend boundary

For bpref, `R` is the judged-relevant count, `N` the judged-nonrelevant count,
and the penalty denominator is `min(R,N)`. Each judged relevant contributes
`1 - min(nonrelevant_before, min(R,N)) / min(R,N)`. Unjudged documents are
ignored; `R=0` returns 0. When `N=0`, bpref is the fraction of all judged
relevant documents actually retrieved. Hand-computable tests cover all three
`R`/`N` orderings, partial/complete/empty retrieval with `N=0`, and `R=0`.

Gemini and Voyage are estimate-only external ceilings. Full API execution is
forbidden in this stage and requires future explicit user approval. Neither
provider was called, no quota was intentionally consumed, and actual spend is
USD 0. There is no environment-variable authorization path.

## Semantic-header repair and corrected A100 pilots

Independent review of commit `5c49bedf2ecc80d3391eed3d8c2d3abb4d977670`
found that the initial pilots exposed internal `cXXXX` identifiers instead of
canonical semantic column headers. The normalized corpus was correct and was
not changed. One canonical normalized-record adapter now preserves positional
internal IDs plus ordered `header_text` metadata. Both neural and lexical
serializers consume that metadata; duplicate, empty, and null headers remain
positional, representative rows are arrays, and missing normalized metadata
fails closed. The original 77.216/84.157/281.580-second measurements and policy
hash `06fe970a...072905` are superseded and are not current evidence.

Pilots ran sequentially in the isolated M7B environment: Python 3.10.12,
PyTorch 2.5.1+cu121 (CUDA 12.1), Transformers 5.2.0,
SentenceTransformers 5.4.1, Hugging Face Hub 1.29.0, qdrant-client 1.15.1,
pyarrow 23.0.1, and DuckDB 1.2.2. The detected device was one NVIDIA
A100-PCIE-40GB (42,409,000,960 bytes nominal VRAM), compute capability 8.0,
with BF16 support.

`m7b-pilot-table-id-order-v1` selects the first 10,000 unique IDs in canonical
`table_id` order from the complete normalized index. Its ordered-ID SHA-256 is
`5a8ee854f5bb6d94438d5043dda2625e1ae3044518f0417c9940e86ee1f5e16c`.
Every corrected run used this population and `neural_table_evidence_v1`
version 1.1.0 (policy hash
`1b37ffbfb3b0a47ea053f315d064427a0c61bdcac2ec8413bdd593ee46507290`).
All 10,000 tables passed semantic-header validation. Serialized lengths were
75/765/1,797/4,095 characters at min/median/p95/max.

| Model | Batch | OOM | Seconds | Tables/s | Peak allocated | Peak reserved | Projected hours | Gate |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Qwen 0.6B | 64 | 0 | 66.669 | 149.994 | 16,577,182,208 | 36,068,917,248 | 3.061 | pass |
| Nemotron 1B | 128 | 0 | 78.218 | 127.847 | 30,146,498,048 | 35,932,602,368 | 3.591 | pass |
| Qwen 4B | 32 | 1 at batch 64 | 241.566 median | 41.397 | 20,637,003,776 | 30,654,070,784 | 11.090 | pass |

Calibration used the longest real pilot inputs in the bounded sequence
4/8/16/32/64/128 and retained an 85% VRAM safety margin. All outputs had the
expected dimensions, finite/nonzero values, BF16-tolerant L2 norms, exact
model/tokenizer revisions, zero truncation violations, and the correct isolated
model-defined pooling (Qwen last-token; Nemotron mean). Qwen 4B handled its OOM
and returned to batch 32; it was not quantized or substituted. Because its
first projection was within 10% of 12 hours, the boundary-stability timings
were 243.758, 241.566, and 241.221 seconds without reload or recalibration; the
median determined its gate result.

These are transparent projections from 10K pilots, not full-corpus timings.
No full-corpus embedding/index, exact development retrieval, effectiveness
metric, encoder selection, K selection, hybrid run, or holdout evaluation has
occurred. M7C remains unstarted. Runtime reports, weights, and caches remain
outside Git.
