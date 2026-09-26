# AB-M1: interpreter foundation

Starting state: branch `main`, commit `80c8b0c25595156eaa781b89d0b1d7471044d74a`.
Working tree contained only untracked `action-base-v0.1.json`; it remains untouched
and is excluded from this milestone commit. No applicable AGENTS.md was found.
Implementation branch: `feat/ab-m1-interpreter-contract`.

## Inspection and compatibility

The old `scripts/interpreter_production.py` imported dotenv and Groq, checked the
key at import time, selected one of seven labels, and returned model-reported
confidence. Its companion test printed a handwritten dictionary without assertions.
The new entry point requires an explicit provider and input ID, returns an execution
envelope, and makes no automatic provider calls. Old callers must migrate; there is
no compatibility conversion to the old label/confidence output.

`grounder_production.py` actively loads `kb/action_base_v1.0.json`: eight actions,
flat `conditions`, including DETECT_ANOMALIES. Its label lookup copies conditions;
it does not bind query arguments. `action_base_v1.0-1.json` has seven actions, axes,
hard constraints, soft predicates, weights, and promotion metadata; it has no
`conditions` lists and is not a drop-in replacement. For COMPARE the active file
requires two categorical columns, a numeric column, and 1,000 rows. The alternate
file adds group cardinality and balance language and scoring weights. These are
historical assertions, not scientific claims endorsed by this implementation.
Both files are preserved. The legacy grounder still accepts old dictionaries, but
explicitly rejects versioned interpretations and execution envelopes.

All three requested proposal files are absent:

- `docs/ab_proposal/AB-Specification-v0.1.md`
- `docs/ab_proposal/action-base-v0.1.json`
- `docs/ab_proposal/grounded-card-examples-v0.1.json`

Paths above are relative to `intention_grounding`. The untracked root JSON was read
as a partial draft reference, not copied into runtime or committed. Conformance to
the missing specification/examples cannot be claimed. That draft describes Compare
specializations, additive inheritance, role binding, and explicit complete-grid
activation. Its global requirement for time grain alongside time points is stricter
than extraction of a bare year; extraction preserves the year without inventing a
grain. Its `available_observations` default and complete-grid activation are future
grounder policy, not interpreter defaults. A time filter does not select trajectories;
a range implies neither endpoints only nor complete annual coverage. The draft's
descriptive scope differs from legacy generic statistical thresholds. None of these
scientific or policy questions is silently reconciled.

## Contract and validation

`interpreter/schema.json` is a closed JSON Schema (Draft 2020-12), version `1.0`.
`core.validate` adds deterministic cross-record and provenance validation. All nested
objects reject unknown keys. An interpretation contains exact original input and ID,
query topics/entities/measures/constraints, evidence, action expressions, arguments,
missing roles, candidate readings, relationships, status, and diagnostic codes.

Extracted values have `literal`, `evidence`, and nullable `normalized`. Literal text
must exactly match each referenced evidence span. Normalization catalogue `1.0` has
only `casefold-v1` (Python Unicode casefold) and `annual-v1` (case-insensitive
annual/annually/yearly → year). Both require the original evidence and verify the
actual transformation. No system defaults are admitted in this version. Relative
time remains literal; ranges remain ranges. Multiple values use repeated role
records, avoiding implicit concatenation. General role `other` preserves additional
source values without expanding an AB taxonomy.

Candidate labels are source expressions, optionally normalized, and provisional.
Candidate `reading.description` is explicitly a semantic hypothesis with evidence,
not a literal extraction or a normalization operation. Candidate-specific arguments
preserve alternative bindings. No final AB action IDs, confidence, requirements, or
suitability fields are accepted. A provenance check cannot detect arbitrary false
claims embedded in natural-language hypothesis descriptions; those need reviewed
semantic evaluation.

Relationships refer to action IDs for `single`, `joint`, and `accepted_alternatives`;
`competing_interpretations` refers to candidate IDs of one action mention. Joint
means both requested, accepted alternatives means either explicitly acceptable,
and competing means unresolved readings. All actions must be covered and competing
candidates must be represented. This small version does not model nested Boolean
goal expressions or conflicts among combinations of several action mentions.

Scope is extraction of English analytical requests for dataset discovery, including
recognizable non-Compare actions. `unsupported` means outside that scope (e.g. poem
writing), never merely outside the draft Compare branch. `insufficient` means
missing/unresolved arguments; `ambiguous` preserves competing readings (and takes
precedence if missing information also exists); `unambiguous` has no missing roles
or diagnostic codes. These statuses describe the interpretation, not execution.
Scope decisions, completeness of extraction, and semantic correctness remain model
judgments, not facts proved by deterministic validation.

Evidence spans are nonempty, half-open Python/Unicode code-point offsets into the
unmodified input. Booleans and floats are not valid indices. Bounds, substring
identity, unique IDs, evidence resolution, normalizations, relationship membership,
and status consistency are checked. A valid span proves textual provenance, not
semantic entailment; even the wrong occurrence of identical text cannot always be
detected. No validation here establishes table suitability or model calibration.

The execution envelope separates `raw_response`, validated `interpretation`, safe
`failure` code, and metadata. INVALID_INPUT, PROVIDER_FAILURE, MALFORMED_JSON, and
schema/provenance codes never become UNKNOWN interpretations. JSON duplicate keys,
non-JSON constants, and markdown-wrapped JSON fail. Provider exception text is not
returned. Raw response artifacts contain provider content and should be treated as
such; the adapter never adds credentials to logs or metadata.

## Installation, tests, and demo

From the repository root (Python >=3.10):

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -e '.[dev]'
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m intention_grounding.interpreter.demo
```

Runtime uses jsonschema 4.23.0; tests use standard-library unittest. Groq is optional
(`pip install -e '.[groq]'`), absent from default installation/tests. Core imports
need neither credentials nor optional SDKs. An explicitly invoked `GroqProvider`
requires an explicit model, loads the key only at invocation, sets temperature,
token limit and JSON response format, bounds timeout to 120 seconds and retries to
2, and has no model substitution or heuristic fallback. The default is zero retries
and 30 seconds. Adapter tests inject a mocked client; live provider compatibility
and model support for the requested JSON format remain unverified.

The demo executes stored input → replay response → parsing → validation and creates
a unique `outputs/ab-m1/manual-replay-*` directory each time. Each case has separate
`.raw.txt` and `.result.json` files. Use `--output-root PATH` to change the parent.
Thirteen manually authored cases include malformed JSON and bad evidence spans;
expected rejections are demo success, unexpected outcomes produce a nonzero exit.
Replay metadata identifies manual origin; no model or prompt version is invented.
Live adapter metadata records configured model, prompt `ab-m1-v1`, and settings.
Replay fixtures and their outputs are not live model predictions or scientific
evaluation results. No keyword classifier is implemented.

CI now installs the current package, runs unittest, compiles the relevant current
files, and runs the offline demo on Python 3.10, 3.11, and 3.13. Removed obsolete
checks referenced missing `src`, `configs/retrieval/result_schema.json`, and the
absent `intention` CLI (smoke, synthetic benchmark, profiler/interpreter/controlled
and operational evaluations, WikiTables audit/preflight/acquisition, snapshot).
No replacement profiler/retrieval/corpus acquisition was created. Archived research
scripts and historical result files are preserved and are not an offline test suite.

## Verification and next milestone

Local targeted checks passed after correcting a test network stub that interfered
with SSL imports. Delivery verification on Python 3.13: all 11 unittest methods passed (including
parameterized rejection cases); all 13 demo outcomes matched their expectations;
compileall and git diff --check passed. CI versions 3.10/3.11 were not run locally. Tests
include independently specified fixture expectations and rejection mutations, a
mocked Groq success/failure path, legacy compatibility, and a subprocess that blocks
optional imports/network connections while running the entire offline demo.
Installation required approved network access after sandbox DNS failed; this only
installed software dependencies. No live LLM calls or dataset/model-weight downloads
were performed, and no accuracy, argument F1, or scientific evaluation is claimed.

Next: validate an executable AB schema, inheritance expansion, action resolution,
and argument binding. A later AB-constrained LLM may propose IDs/bindings; whether
a second LLM call is needed remains undecided. AB loading/validation, inheritance,
requirement-template instantiation, and grounded-card validation must remain
deterministic regardless of resolver choice. No new grounder, profiler, retrieval,
or ranking is implemented here.

Later interpreter evaluation needs natural-language requests with independently
reviewed action, argument, ambiguity, and evidence annotations. End-to-end evaluation
separately needs real tables with provenance, requests, and reviewed action-specific
requirement-satisfaction judgments. Relevance labels are not automatically intended-
action usefulness labels. Existing labels need a provenance audit before use as
trusted ground truth. Dataset choice and acquisition remain a subsequent milestone;
none is chosen or prepared by AB-M1.
