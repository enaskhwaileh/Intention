# Pre-Milestone-7 system architecture freeze

This gate freezes interfaces and provenance before IA-WikiTables pooling. It
produces no benchmark annotations, model results, or paper evidence.

## Scientific pipeline

```text
user input u
  -> LLM interpreter
  -> topical query q_u + grounded action I_u + requirements Psi*(I_u)

offline table T
  -> authoritative normalized Parquet artifact (DuckDB access)
  -> neural_table_evidence_v1 serialization S(T)
  -> document encoder E_document
  -> Qdrant rebuildable vector index

offline table T
  -> deterministic capability profiler
  -> optional validated semantic enrichment (separately inferred)
  -> versioned Phi(T) profile artifact

online q_u
  -> query encoder E_query(q_u)
  -> dense or lexical+dense retrieval
  -> candidate table IDs
  -> authoritative capability-profile lookup
  -> intended-action alignment
  -> final usefulness ranking
```

The equations are `e_q = E_query(q_u)`, `e_T = E_document(S(T))`, and
`r(q_u,T) = similarity(e_q,e_T)`. Query and document modes, instructions,
dimension, normalization, similarity, truncation, tokenizer/model revisions,
device, timings, failure, and configuration hash are part of the embedding
identity. The provider-independent interface is `EmbeddingProvider`; no vendor
is the architectural contract.

First-stage semantic retrieval receives only `q_u`. The original action-bearing
request, grounded action, requirements, profiles, judgments, and gold artifacts
are unavailable to it. A system that embeds full input must be registered and
reported as a separate full-input baseline. Intended-action alignment operates
after dense or hybrid candidate generation.

## Encoder registry and selection

`configs/architecture/embeddings.yaml` is fail closed. The reviewed candidates
are Google `gemini-embedding-2`, Voyage `voyage-4-large`, Qwen
`Qwen3-Embedding-8B`, Qwen `Qwen3-Embedding-0.6B`, and Voyage
`voyage-4-nano`; BM25 is the available lexical reference. TABERTA is not in the
new primary architecture. API aliases remain blocked because providers do not
publish immutable checkpoint revisions and credentials are absent. Open-weight
entries pin exact Hugging Face revisions but remain blocked because weights and
validated hardware are absent.

The registry facts were checked against authoritative sources on 2026-08-29:

- [Gemini embedding documentation](https://ai.google.dev/gemini-api/docs/embeddings)
  and [pricing](https://ai.google.dev/gemini-api/docs/pricing);
- [Voyage embeddings](https://docs.voyageai.com/docs/embeddings) and
  [pricing](https://docs.voyageai.com/docs/pricing);
- official model cards for
  [Qwen3-Embedding-8B](https://huggingface.co/Qwen/Qwen3-Embedding-8B),
  [Qwen3-Embedding-0.6B](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B),
  and [voyage-4-nano](https://huggingface.co/voyageai/voyage-4-nano).

No model wins from an external leaderboard. The development-only bake-off uses
topical nDCG, candidate recall at frozen/sensitivity K, embedding and retrieval
latency, index size, reproducibility, availability/cost, and robustness to
serialization length. Final intended-action usefulness and all test labels are
forbidden selection signals. The final encoder remains pending real development
data and precedes final pool freezing.

## Serialization and storage authority

BM25 keeps immutable `title_description_schema_v1`. Neural retrieval uses the
separate canonical JSON `neural_table_evidence_v1`: title, caption, ordered
columns, deterministic basic types, stable-head representative rows, and
representative values. Sampling limits, seed, character budget, truncation,
version, policy hash, and output checksum are frozen. It excludes action,
arguments, requirements, profiles, topical/usefulness/benchmark labels, system
outputs, full input, and all gold information.

Parquet artifacts are the authoritative normalized tables, with DuckDB as the
local analytical engine. Versioned JSON/Parquet artifacts are authoritative for
capability profiles. Qdrant is only a rebuildable index. Its collection identity
binds dense dimension/metric, collection version, encoder hash, serialization
hash, dataset version, and profile version. Payload carries traceable references;
Qdrant supports future separately named sparse vectors. This design follows the
official [Qdrant collection](https://qdrant.tech/documentation/manage-data/collections/),
[point](https://qdrant.tech/documentation/concepts/points/), and
[payload](https://qdrant.tech/documentation/concepts/payload/) contracts.

Every table has a schema-validated artifact manifest linking source dataset and
version, normalized artifact and hash, serialization identity/hash, encoder
revision/hash, vector collection version/hash, and capability-profile
version/hash. Loss of Qdrant does not lose the authoritative table or profile.

## LLM and profiler boundaries

The deterministic interpreter remains the controlled reference. The learned
configuration uses the existing external structured-provider boundary plus the
versioned `configs/architecture/llm_registry.yaml`. The reviewed candidate is
stable `gemini-3.7-flash`, whose official documentation supports structured
JSON output; it remains blocked without credentials and an immutable checkpoint
revision. Its output must still pass the repository's Draft 2020-12 validation,
normalization, span support, grounding, supported-action, and missing-argument
checks. The LLM cannot add actions or predicates, change requirement semantics,
score rankings, or create judgments. See Google's official
[model list](https://ai.google.dev/gemini-api/docs/models) and
[structured-output guide](https://ai.google.dev/gemini-api/docs/structured-output).

Deterministic profiling stays authoritative for computable facts. Optional
`SemanticProfilerEnricher` output is limited to ambiguous semantic roles and
granularity, must be `state=inferred`, and carries confidence, model, prompt and
schema hashes, evidence, and source fields. Inferred output cannot silently
overwrite observed deterministic evidence.

## Retrieval and evaluation conditions

The frozen future conditions are BM25, Dense, Hybrid, Dense + Intended-Action
Alignment, and Hybrid + Intended-Action Alignment. Hybrid retrieval initially
uses deterministic reciprocal-rank fusion with `k=60`; it is an untuned
interface default, not a result or final hyperparameter claim.

`evaluate_paper_ranking` is the normative paper-evaluation entry point. It
requires scored table IDs, the complete qrels, and the declared universe. Older
label-list helpers remain only for controlled hand-computable regression tests
and must not be called by experiment orchestration.

## Blocked work

API credentials, model downloads, accelerator validation, Qdrant service,
Parquet/DuckDB runtime dependencies, IA-WikiTables source acquisition, human
annotations, and real development data are absent. Consequently there is no
encoder bake-off, index build, pool freeze, real retrieval run, or paper claim.
