# Milestone 5 retrieval contract

This contract freezes the first-stage retrieval boundary before any external
model is installed. It is an interface and observability milestone, not a
real-benchmark experiment.

## Input boundary

The proposed system and every proposed first-stage retriever receive only the
validated topical query `q_u`. The action cue, grounded action, arguments,
requirements, and full user input are unavailable to first-stage retrieval.
The historical Milestone 5 registry contains `TABERTA-Hybrid` with
`input_scope: topical_only`, but the Pre-Milestone-7 architecture decision
removes TABERTA from the planned primary encoder architecture.

`TABERTA-FullInput` is a separately named baseline with
`input_scope: full_input_baseline`. Its results must never be reported as the
topical-only historical TABERTA condition. The main pipeline always constructs a
`topical_only` request; an adapter registered for full input fails that request.

## Common result

`Retriever.retrieve(RetrievalRequest, tables)` returns one
`RetrievalResult`, validated by the Draft 2020-12 schema at
`configs/retrieval/result_schema.json`. A successful result contains:

- native `raw_score`, normalized relevance in `[0,1]`, and contiguous rank;
- normalization method/version, fit scope, and retrieval-config hash;
- model/checkpoint, adapter, serialization, registry, and config provenance;
- serialization, inference, and total milliseconds plus clock identity;
- an explicit `success` state and no failure object.

A failed result contains no candidates and includes a stable failure code,
message, and retryability. Provider absence, serialization errors, invalid
requests, and provider errors are distinct. No adapter may substitute BM25 or
another available system after failure.

## Evidence access and model serialization

`retrieval_table_evidence_v1` is the shared access boundary. It permits title,
description, column names, row structure, and cell values, while forbidding metadata,
capability/action artifacts, full user input, and gold/usefulness labels.
Permitted evidence is not a universal serialization.

`title_description_schema_v1` is the BM25 serialization. It exposes:

1. table title;
2. table description;
3. ordered column names from the first row.

It excludes rows, cell values, metadata, capability profiles, grounded action,
action arguments, and full user input. The ordered space-joined representation and its
SHA-256 checksum are produced by `TableSerializer`. Any future serialization
gets a new identifier and version; it does not mutate this contract. External
retrievers currently have `serialization: null` and remain blocked until their
exact published/model-required serialization is independently registered and
shown to be a subset of the common evidence-access policy.

## Candidate depth

The current deterministic default is `K=20`, not a final paper choice.
Development diagnostics may use `K ∈ {5,10,20,50}`; the frozen M7B selection
depths are `K ∈ {5,10,20,50,100}`. Choose the smallest K whose development
KnownRelevantRecall@K is at least 0.98 times development
KnownRelevantRecall@100; otherwise choose 100. This is the single authoritative
M7B depth rule. Test labels are forbidden.

## Registry and availability gate

`configs/baselines/registry.yaml` records, for every retriever, model,
checkpoint and revision, adapter revision, serialization, input scope, prompt/instruction,
embedding dimension, hardware, dependencies, latency fields, availability, and
failure reason. Unknown external identities remain null and blocked. An
external adapter can become available only when its implementation, model, and
exact revisions are present and the remaining model-specific fields are pinned.
Each result carries the registry hash and retrieval-config hash.

No large model was downloaded and no real benchmark was run in this stage.

The modern dense architecture, neural table serializer, vector index, and
development-only encoder-selection gate are frozen separately in
`docs/system_architecture_freeze.md`.
