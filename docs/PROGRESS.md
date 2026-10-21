# Real-table Compare implementation checkpoints

Starting recovery commit: `dc7b48cbf1749c76ffe56bfe6f6462ddd1af91ad`. Remote main verified as `cd4f7235cd4a2dae1a7a31d0806f50aecfc4a665`, identical tree. Dedicated branch: `implementation/real-table-compare`. No applicable AGENTS.md found. Baseline: 53 offline tests passed; no user modifications present.

1. Verified incorrect WikiDBs fallback, unknown-only aligner, missing retrieval/ranking/evaluation, catalog/runtime gap and conflicting documentation.
2. Migration inventory: extracted `actions` becomes `intentions`; instance `id` stays an instance ID, binding references become `intention_instance_id`; catalog `action_id` becomes `intention_id`; library identity becomes `il_version`/`il_path`; `grounded_card` becomes `grounded_intention`; verdict `unknown` becomes `unresolved`. External argparse `action=` stays unchanged. Frozen proposals and historical outputs remain unchanged; explicit legacy readers migrate old inputs. No manuscript is available to verify paper consistency.

Scope change authorized by the researcher: direct documented-value comparison AND explicit group-mean comparison. This supersedes the old direct-observation-only policy; no causal interpretation or automatic averaging of precomputed means.

Checkpoints 2–3: canonical interpreter schema v2 and IL v0.3, explicit frozen-input readers, separate instance/type references, corrected local provenance, boolean/header handling, explicit parsing and full scans, content/config/version caches. 56 tests passed. Maintained documentation reconciliation is completed in checkpoint 9.

Checkpoint 4: downloaded UCI 275 (279,992-byte ZIP) and 560 (604,298-byte ZIP); inspected original contents and official license pages. Normalized 731 daily and 17,379 hourly DC observations, plus 8,760 hourly Seoul observations. Both CC BY 4.0; exact hashes and source documents retained. DC daily/hourly share a source family. Source temperature/season conflicts excluded from semantic binding. No held-out split claim. Hardware: Intel i5-8257U, 16 GiB RAM, approximately 542 GiB free; no torch/transformers installed. Qwen remains unavailable in this environment; BM25 is the complete baseline, no substituted encoder.
