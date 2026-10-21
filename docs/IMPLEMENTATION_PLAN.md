# Implementation status and next checkpoints

The [README](../README.md) is the authoritative architecture, setup, demonstration and limitations guide. This replaces the superseded pre-implementation plan; Git preserves that plan's history.

| Checkpoint | Delivered | Verification / acceptance |
| --- | --- | --- |
| 1. Establish state | Clean starting tree, baseline 53 tests, remote main and dedicated branch verified. | Recovery SHA and remote relationship in [progress log](PROGRESS.md). |
| 2. Canonical terminology | Interpreter schema v2, IL v0.3, distinct instance/type references, current fixtures/prompts/API/CLI/UI migrated; explicit legacy readers. | Current contracts pass; terminology check runs in CI; frozen inputs unchanged. |
| 3. Ingestion | Local/unknown provenance, empty-header and boolean fixes, explicit parsing/missingness/full scans, content/config/version cache. | Regression tests cover malformed tables, missing metadata and cache invalidation. |
| 4. Real data | Official UCI 275/560, three inspected tables, immutable originals, deterministic normalization and complete small manifest. | Offline reconstruction matches hashes; family relationships and documentation conflicts recorded. |
| 5. Compare | Direct documented values and explicitly requested means; request grounding separate from table binding; safe SQL and execution gate. | Independent Decimal arithmetic agrees with actual SQLite results; unsupported cases never execute. |
| 6. Discovery | Full-request BM25, per-procedure evidence verdicts, deterministic versioned ranking, explicit ties and abstention. | Real successful, incompatible, unresolved, ambiguous and unsupported examples; no calibrated-score claim. |
| 7. Evaluation readiness | Versioned requests/corpus/judgments/splits; evaluator-only gold; immutable prediction hash checks; metrics and unjudged annotation template. | Hand-checkable metrics and gold-isolation tests. Independent judgments are not available, so no effectiveness result. |
| 8. Demonstration | Existing dashboard shows real data, exact input mode, grounding, candidates, bindings, verdicts/evidence, ranking, SQL and results. | Browser verification and exported actual reports. |
| 9. Delivery | Full offline checks, source-only commits, branch push, no merge or force push. | Final verification/commit IDs in delivery and progress log. |

## Next scientific milestone: independent pilot review

**Purpose:** assess usefulness with judgments not produced by the framework under test.

**Dependencies:** review source-to-concept mappings, fix operation policy for observed interval counts, assign independent reviewers, and accept ranking/abstention conventions. Current corpus remains development-only.

**Affected files:** annotation records outside runtime bundles; `evaluation.py` and its schemas/tests if reviewer feedback changes the protocol; new versioned source/topic manifests before claiming disjoint evaluation.

**Deliverables:** independently reviewed topical/usefulness labels with evidence and adjudication, frozen requests and corpus identity, declared eligibility/denominators, faithful baseline integration plan with exact model resources.

**Verification:** `python -m unittest discover -s tests -v`; `python -m intention_grounding.verify_demo`; evaluate immutable predictions using the separate evaluator only after real review.

**Acceptance:** no generated gold; independent reviewers and decisions auditable; no unresolved labels made negative; source families/topics do not leak across claimed partitions; no test-driven prompt/policy selection. Report a development pilot, not publication-ready superiority.

Later: integrate faithful dense/reranking/semantic matching/TABERTA/direct-LLM baselines, expand independent families, validate language interpretation, implement narrow Predict diagnostics with prediction-time information and separate row splits, then freeze held-out evaluation. Do not treat broad IL definitions as runtime support.
