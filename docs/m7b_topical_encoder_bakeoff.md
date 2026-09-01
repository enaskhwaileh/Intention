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

## Execution evidence

No CUDA accelerator or working NVIDIA driver is available on the current host.
None of the three native, unquantized local candidates could therefore satisfy
the common-accelerator 10,000-table pilot gate. No weights were downloaded, no
CPU/alternate model was substituted, no full embeddings or indexes were built,
and no development effectiveness metrics were computed. Efficiency values
remain missing rather than estimated.

Paid execution was not authorized because
`INTENTION_ALLOW_PAID_EMBEDDING_BAKEOFF=1` was absent. Gemini and Voyage made no
calls and incurred zero known cost. Authorized execution would additionally
require an estimate and is blocked above USD 75 per provider.

The outcome is explicitly blocked: no winner or K is selected and hybrid is
not executed. The holdout was neither loaded nor evaluated. Regenerate the
small structured report with `PYTHONPATH=src python3 -m intention
m7b-bakeoff-preflight`.
