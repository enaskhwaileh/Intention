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

During AB-M1, the three requested canonical proposal files were absent. The root
JSON was initially untracked; the specification and example cards appeared during
implementation and were read as they became available. They were preserved without
being committed in AB-M1. That historical absence no longer describes availability:
the focused proposal follow-up commits authoritative, corrected copies at:

- `docs/ab_proposal/AB-Specification-v0.1.md`
- `docs/ab_proposal/action-base-v0.1.json`
- `docs/ab_proposal/grounded-card-examples-v0.1.json`

These paths are relative to `intention_grounding`. Root copies remain unchanged,
untracked historical source drafts, not authoritative alternatives. No competing
local copies were found. The proposal is research design data, not the active AB,
an executable AB-M1 schema, an empirically validated taxonomy, or live model output.

The follow-up corrects the trajectory card's former use of `fixture_literal_v1` to
map “every year” to `complete_grid`. Literal extraction is now separate from
`derive_explicit_group_time_grid_v1`, a declarative grounding derivation. It requires
resolved groups, a finite temporal domain, explicit grain, exhaustive temporal
coverage, and unambiguous scope over every requested group. The example cites all
five kinds of evidence and explicitly says “each of France and Spain” and an
inclusive range. `available_observations` remains a separately registered proposal
system policy, never user evidence. Neither rule is imported into the interpreter;
its two normalization rules and schema are unchanged.

The original “between 2019 and 2021” card assumed endpoints and year grain. It is
now a non-grounded ambiguity case. Positive time comparison instead explicitly
contrasts annual observations in 2019 versus 2021. All positive examples now state
annual granularity rather than silently inferring cadence from year labels. A date
range or “annual” alone does not imply a complete grid. The preserved root copies
record the pre-correction assumptions; the canonical specification, catalogue and
cards agree on the corrected semantics.

Still unresolved for later work: authorized external context (the interpreter
currently accepts exact-input evidence only), semantic scope/entailment review,
range disambiguation, and operationalizing the draft's binding and inheritance
rules. The Compare route's inference/transformation exclusions do not narrow the
interpreter's general analytical scope. Historical generic statistical thresholds
are not imported into the descriptive proposal.

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


## Proposal follow-up verification

Entry state: `feat/ab-m1-interpreter-contract` at
`9dad49297da1b7f5db1be53c8044ad2a331a1b6c`, with only the three untracked root proposal
files. No applicable AGENTS.md was found. Follow-up branch:
`fix/ab-proposal-coverage`, based on fetched `origin/main` at
`ec2a4e444da51b1ec60e701cb464fdcb0033519c` (same file contents as the entry commit).
Runtime KB, interpreter code/schema/rules, and historical results are untouched.

The standard-library consistency check parses both canonical JSON files and checks
parent cycles/references, predicates, templates, rule references, source spans,
propagated evidence, and the complete-grid rule's declared structure. It validates
manual activation certificates, rejects missing evidence or unresolved conditions,
and checks five underspecified coverage annotations. It does not execute grounding
or prove that manual semantic annotations are correct. Existing CI discovers these
tests without a workflow change.

Commands from the repository root:

```sh
.venv/bin/python -m unittest discover -s tests -p test_ab_proposal.py -v
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m intention_grounding.interpreter.demo
git diff --check
```

Observed on Python 3.13: the focused proposal check passed all 4 test methods;
the complete suite passed all 15 methods (11 existing interpreter tests run once);
the standalone demo matched all 13 expected outcomes. The existing interpreter
network-isolation test also runs its own temporary replay demo. A trailing blank
line found by diff --check was removed before commit. No live LLM calls, dataset
downloads, new grounding implementation, or scientific validation occurred.
