# Milestone 5 retrieval contract

This contract freezes the first-stage retrieval boundary before any external
model is installed. It is an interface and observability milestone, not a
real-benchmark experiment.

## Input boundary

The proposed system and every proposed first-stage retriever receive only the
validated topical query `q_u`. The action cue, grounded action, arguments,
requirements, and full user input are unavailable to first-stage retrieval.
`TABERTA-Hybrid` is registered with `input_scope: topical_only`.

`TABERTA-FullInput` is a separately named baseline with
`input_scope: full_input_baseline`. Its results must never be reported as the
topical-only TABERTA-Hybrid condition. The main pipeline always constructs a
`topical_only` request; an adapter registered for full input fails that request.

## Common result

`Retriever.retrieve(RetrievalRequest, tables)` returns one
`RetrievalResult`, validated by the Draft 2020-12 schema at
`configs/retrieval/result_schema.json`. A successful result contains:

- normalized relevance in `[0,1]` and contiguous one-based rank;
- retriever name and exact adapter revision;
- serialization identity and input scope;
- serialization, inference, and total milliseconds plus clock identity;
- an explicit `success` state and no failure object.

A failed result contains no candidates and includes a stable failure code,
message, and retryability. Provider absence, serialization errors, invalid
requests, and provider errors are distinct. No adapter may substitute BM25 or
another available system after failure.

## Table serialization

`title_description_schema_v1` is the primary frozen serialization. It exposes:

1. table title;
2. table description;
3. ordered column names from the first row.

It excludes rows, cell values, metadata, capability profiles, grounded action,
action arguments, and full user input. The ordered space-joined representation and its
SHA-256 checksum are produced by `TableSerializer`. Any future serialization
gets a new identifier and version; it does not mutate this contract.

## Candidate depth

The frozen primary depth is `K=20`. Development diagnostics may use
`K ∈ {5,10,20,50}`; sensitivity analysis may use
`K ∈ {5,10,20,50,100}`. These values were fixed before real evaluation.

## Registry and availability gate

`configs/baselines/registry.yaml` records, for every retriever, model,
checkpoint, revision, serialization, input scope, prompt/instruction,
embedding dimension, hardware, dependencies, latency fields, availability, and
failure reason. Unknown external identities remain null and blocked. An
external adapter can become available only when its implementation, model, and
exact revision are present and the remaining model-specific fields are pinned.

No large model was downloaded and no real benchmark was run in this stage.
