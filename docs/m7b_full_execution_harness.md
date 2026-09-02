# M7B full-corpus execution harness

This is an engineering execution layer for the frozen M7B development-only
topical encoder bakeoff. It is not a new scientific protocol and produces no
paper result by itself. The corrected 10K A100 pilot gate is merged; full-corpus
encoding and development effectiveness measurement have not run.

## Identity and ordering

The versioned operational contract is
`configs/benchmarks/m7b_full_execution.yaml`. Before model loading, preflight
reads only the normalized index and verifies 1,652,771 unique table IDs, all 256
shard values, every logical checksum, and the canonical M7A corpus digest. It
uses the same canonical M7A digest implementation rather than defining another
corpus hash.

Execution order is `normalized_shard_then_table_id_v1`: source shards 0 through
255, with canonical table IDs sorted ascending inside each shard. One SHA-256
is accumulated over each ordered UTF-8 table ID followed by a newline. Every
model identity and shard manifest binds that execution-order identity, full
table-ID digest, corpus digest, and frozen serialization identity.

Every record passes through `runtime_table_from_normalized_record()` and
`NeuralTableSerializer`. Structural schema checks reject benchmark/action/qrel
objects before serialization. Natural table content is not substring-blocked;
ordinary text such as “requirements” remains valid source evidence.

## Encoding artifacts and resume behavior

Each model has 256 independently resumable directories. A shard contains
`table_ids.txt`, a row-aligned two-dimensional `vectors.npy`, and
`shard-manifest.json`. Model inference is native unquantized BF16; persisted
vectors are normalized NumPy float32. The manifest records all corpus, model,
tokenizer, dimension, serialization, batch, checksum, validation, and timing
identities.

Files are flushed, closed, checksummed, validated in a temporary shard
directory, and atomically promoted. Resume revalidates every complete identity,
file checksum, row mapping, dimension, finite/nonzero status, and L2 norm before
skipping. A mismatch fails closed. Incomplete temporary directories are
discarded and restarted. CUDA OOM retries the same records at half the batch;
batch size one OOM returns a structured failure without substitution,
quantization, dropped records, or skipped records.

`raw_vector_payload_bytes` is rows × dimension × four bytes.
`physical_index_bytes` is the actual byte size of all 256 `vectors.npy` files
plus all 256 `table_ids.txt` mappings. Reports, manifests, query vectors, and
logs are excluded from this winner-rule tie-break.

## Exact development retrieval

The local selection index is sharded dense data, not Qdrant or another ANN.
The evaluator verifies all 256 complete shards, recomputes their global table-ID
sequence digest, encodes only the 30 canonical topical development queries, and
persists normalized float32 query vectors. It performs shard-by-shard
`torch.float32` matrix multiplication with TF32 explicitly disabled. Per-shard
and final merges use score descending then table ID ascending, yielding a
stable unique top 100 after searching all 1,652,771 tables.

The canonical query and qrel files must match their pinned SHA-256 hashes. For
qrels, the query ID is parsed first and holdout rows are skipped before table ID
or label materialization. Reports record `holdout_qrels_materialized: false`.
The evaluator reuses `require_exact_search()` and
`evaluate_development_rankings()`; provisional selection requires all three
local candidates and reuses `select_encoder()` and
`select_candidate_depth()`. It does not update the tracked encoder or K.

## Future commands

Metadata-only preflight (no model inference):

```bash
PYTHONPATH=src python -m intention m7b-full-preflight \
  --data-root data --artifact-root <ARTIFACT_ROOT>
```

Full encoding is deliberately guarded and must only be launched after review:

```bash
PYTHONPATH=src python -m intention m7b-full-encode \
  --model <MODEL> --data-root data --device cuda \
  --artifact-root <ARTIFACT_ROOT> --confirm-full-corpus
```

After a model's complete index validates:

```bash
PYTHONPATH=src python -m intention m7b-exact-dev-evaluate \
  --model <MODEL> --source-root <PINNED_WWW2018_REPO> \
  --artifact-root <ARTIFACT_ROOT> --device cuda
```

After all three development evaluations validate:

```bash
PYTHONPATH=src python -m intention m7b-provisional-select \
  --artifact-root <ARTIFACT_ROOT>
```

Gemini and Voyage have no execution route here. External calls remain zero,
actual external API spend is USD 0, holdout evaluation is forbidden, and M7C
has not started.
