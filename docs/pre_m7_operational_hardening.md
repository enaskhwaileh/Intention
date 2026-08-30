# Pre-Milestone-7 operational hardening

This stage makes the learned retrieval/storage boundaries executable without
selecting a final encoder or producing a paper result. The frozen scientific
architecture and alignment equations are unchanged.

## Corrected provider contracts

The Gemini Embedding 2 record now follows Google's current asymmetric search
format: queries are `task: search result | query: {content}` and documents are
`title: {title} | text: {content}`, using `none` when a title is absent. The
model is `gemini-embedding-2`, accepts 8,192 input tokens and output dimensions
128–3072, and automatically normalizes reduced-dimensional output. It does not
support the old `task_type` request parameter. Multiple parts in one Content
are aggregated, so distinct batch items require distinct Content objects or the
Batch API. The adapter calls the official `count_tokens` method with the exact
model and complete formatted string before embedding. Counts above 8,192,
invalid counts, and counting failures stop before `embed_content`; no
approximate tokenizer or silent truncation is allowed. Google documents that
the provider otherwise silently truncates overflow. The stable API alias has no
immutable checkpoint revision and remains blocked without credentials. These
facts were rechecked 2026-08-30 in the
[official embedding guide](https://ai.google.dev/gemini-api/docs/embeddings).

Gemini `gemini-3.7-flash` remains the structured-output candidate. Google's
current migration guide says `temperature`, `top_p`, and `top_k` are deprecated
for this model and should be removed. The registry now distinguishes supported,
deprecated, configured, and provider-default values; the adapter sends none of
those sampling fields and retains the provider default. It sends only the
supported default `thinking_level=medium` plus the structured response schema.
See the official [3.7 Flash guide](https://ai.google.dev/gemini-api/docs/latest-model)
and [structured-output documentation](https://ai.google.dev/gemini-api/docs/structured-output).

## Operational components

- `HuggingFaceEmbeddingProvider` is a reusable revision-pinned adapter with
  tokenizer pinning, query/document formatting, batching, device/dimension
  selection, fail-on-overflow token validation, L2 normalization, finite-vector
  validation, timing, and explicit unavailable/OOM failures. Normal CI injects
  mocks and downloads nothing.
- `Qwen/Qwen3-Embedding-0.6B` at model/tokenizer revision
  `e692b5a16e45607c7e85d81c53e944ac90e6260a` is designated only as the
  `operational_smoke_encoder`. Its official Apache-2.0 model card supports
  instruction-aware queries, unprompted documents, dimensions 32–1024, and a
  32k context. It requires no remote-code trust. It remains blocked because its
  pinned weights are absent. This is not final encoder selection.
- `QdrantVectorStore` uses the official client shape: named `topical_dense`
  vectors, deterministic UUID point IDs, payloads, batch upsert, retrieval,
  nearest-neighbor query, deterministic post-query tie ordering, deletion and
  rebuild. A reserved identity point binds encoder, serializer, dataset,
  profile, dimension, metric, and collection version. `topical_sparse` remains
  reserved for future work. Qdrant is a rebuildable index only.
- `ParquetDuckDBTableStore` is the authoritative normalized table store. It
  writes and validates Parquet plus immutable metadata/checksums and exposes
  DuckDB analytical queries. Missing optional dependencies fail explicitly.
  Versioned JSON profiles and immutable manifest revisions remain outside
  Qdrant.
- `OfflineTableIndexer` connects authoritative storage, leakage-safe neural
  serialization, document encoding, vector upsert, deterministic profiling,
  profile persistence, and artifact manifests. Matching build identities are
  reusable; changed identities create new derived manifest state.
- `OnlineSemanticPipeline` preserves the intended action downstream while
  sending only interpreted `q_u` to the query encoder.
- `GeminiStructuredOutputClient` plugs into `ExternalStructuredProvider`, keeps
  raw and structured artifacts separate, and relies on all existing schema,
  normalization, provenance, grounding, and missing-argument validation.

## Relevance calibration

Native Qdrant cosine similarity is preserved unchanged as `raw_score`.
`CosineEngineeringMapping` provides the bounded label-free `(cosine+1)/2`
plumbing value used as `relevance`. Its identity declares
`calibration_status: development_fit_pending` and `fit_scope:
no_labels_engineering_default`. It is not final paper calibration. Any learned
mapping must be fitted on development data only; test labels remain forbidden.

## Smoke and blockers

`PYTHONPATH=src python -m intention operational-smoke` is a read-only readiness
harness. Structured checks are derived from the pinned encoder registry, local
Hugging Face cache, dependencies, `INTENTION_EMBEDDING_DEVICE`,
`INTENTION_ARTIFACT_ROOT`, `INTENTION_QDRANT_URL`, and expected collection. A
configured Qdrant service may be probed with `get_collections`; the harness
never downloads weights, starts services, calls paid APIs, or substitutes a
backend. It transitions to `ready` only when every required component is ready.

No IA-WikiTables annotation or pool freeze, encoder bake-off, test evaluation,
prompt/K/fusion tuning, or paper-result generation occurs here. Future
conditions remain BM25, Dense, Hybrid, Dense + Intended-Action Alignment, and
Hybrid + Intended-Action Alignment.
