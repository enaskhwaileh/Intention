# Repository map (updated 21 October 2026)

## Confirmed current path

| Stage | Files | Role |
| --- | --- | --- |
| Entry point | `intention_grounding/cli.py`, `pyproject.toml` | Offline replay or opt-in Groq run; writes unique run artifact directories. |
| Interpret | `interpreter/core.py`, `providers.py`, `schema.json`, `fixtures/replay.json` | Provider response, closed-schema and evidence validation; replay responses are manually authored. |
| Intention Library | `docs/ab_proposal/action-base-v0.1.json`, `action_base.py` | Canonical `0.1.0-draft` IL: abstract Compare parent and three concrete Compare intentions; deterministic consistency checks. |
| Ground | `grounder.py` | Model proposal validation against the IL and interpreter evidence; deterministic grounded card. |
| Profile | `profiler.py`, `fixtures/offline_table.csv`, `fixtures/offline-source-metadata.json` | Full local scan of a synthetic four-row table with file-hash provenance. |
| Compare | `aligner.py` | Three-valued requirement results; current unsupported predicates are `unknown`. |
| Verify | `tests/test_interpreter.py`, `test_ab_proposal.py`, `test_pipeline.py`, `.github/workflows/` | Offline contracts and CI. |

`intention_grounding/docs/ab_proposal/AB-Specification-v0.1.md` and `grounded-card-examples-v0.1.json` preserve the frozen v0.1 Compare proposal; the broader IL extension remains separate uncommitted local work; the examples are proposal fixtures, not measured outputs. `notebooks/pipeline_walkthrough.ipynb` walks through the current APIs. Existing notebooks under `intention_grounding/_archive_2026-09-16/` are historical.

## Other files and review candidates

| Category | Files | Reason and review risk |
| --- | --- | --- |
| Legacy workflow | `intention_grounding/kb/`, `scripts/grounder_production.py`, `scripts/interpreter_production.py`, `scripts/grounder_action_verification_gate.py`, `intention_grounding/AB-M1.md` | Older knowledge base and scripts use different contracts. Keep until references and reproducibility needs are checked; `test_interpreter.py` still imports the legacy grounder. |
| Historical experiments | `scripts/_test_archive/`, `_archive_2026-09-16/` | Potentially useful provenance for prior work. Review before archiving elsewhere or deleting. |
| Asserted legacy data/results | `data/queries_input.json`, `data/dataset_tables.json`, `data/ground_truth_labels.json`, `results/interpreter_output.json`, `results/grounder_output.json` | Human/project assertions and older outputs, not verified empirical observations for the current pipeline. Retain pending provenance review. |
| Similar historical library files | `kb/action_base_v1.0.json`, `kb/action_base_v1.0-1.json`, `docs/ab_proposal/action-base-v0.1.json` | Names and versions can confuse; only the last is canonical for current CLI. Check historic consumers before changing names. |
| Generated local state | `outputs/`, `intention_grounding.egg-info/`, `__pycache__/`, `.DS_Store` | Ignored or build artifacts; `outputs/` contains prior run evidence, so review before any removal. |
| Environments | `./.venv`, `../.venv` | Both ignored by the root `.gitignore` (`.venv/` pattern); M0 found the repository environment absent and the parent on Python 3.9. Use a supported Python >=3.10 environment and leave the parent intact. |

Two redundant tracked files were removed: the retired print-only test placeholder and the identical `_working` trace copy. See the cleanup manifest in [the M0 audit](REPOSITORY_AUDIT_M0.md). No data, annotations or results were removed. `.env` and `.env.*` are ignored except `.env.example`; nested `intention_grounding/.gitignore` also ignores `.env`. No credential values are needed for the offline path.

## Open questions

- Whether legacy labels/results have independent review or provenance suitable for any evaluation claim.
- Which historical scripts and notebooks must remain available for reproducibility.
- Where and under what acquisition record real WikiDBs files will be kept if added later.
