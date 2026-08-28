# Online interpretation and grounding protocol

## Artifact boundary

Every provider returns a `ProviderArtifact` containing provider, model, revision,
schema version, validated-content candidate, and untouched raw response. Raw
responses and validated interpretations are separate objects. External provider
configuration requires raw retention and prohibits silent deterministic fallback.

## Structured output

`configs/interpretation/output_schema.json` is the provider-facing JSON Schema.
It permits only a supported action or `unknown`, argument fields, topical fields,
exact source spans, and ambiguity metadata. Unknown root fields—including model
self-confidence—are rejected. Span text must equal the corresponding substring
of the original request.

Validation then checks the action-specific argument schema from the knowledge
layer. Invented arguments, missing required values, unsupported actions,
ambiguous actions, malformed spans, and invalid schema versions cannot ground.
Existential `*` is inserted only for fields explicitly authorized by the action.

## Ambiguity policy

- `unambiguous`: exactly one supported action cue; grounding may proceed.
- `ambiguous`: multiple supported actions; action becomes `unknown`, no guessing.
- `insufficient`: no supported action; relevance-only fallback.

A recognized action with missing required arguments retains the extracted action
for diagnostic evaluation but produces no grounding or requirements.

## Normalization

`configs/interpretation/normalization.yaml` versions action aliases, argument
aliases, and deterministic value aliases. Providers cannot create aliases.
Normalization occurs after schema validation and never fills an undeclared
required value.

## External providers

`ExternalStructuredProvider` is a callable boundary for SDK-specific adapters.
It passes the complete JSON Schema to the configured client and retains the raw
response. Without a client it raises an availability error. No external model,
prompt, checkpoint, or accuracy result is claimed in Milestone 4.
