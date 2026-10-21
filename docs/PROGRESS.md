# Real-table Compare implementation checkpoints

Starting recovery commit: `dc7b48cbf1749c76ffe56bfe6f6462ddd1af91ad`. Remote main verified as `cd4f7235cd4a2dae1a7a31d0806f50aecfc4a665`, identical tree. Dedicated branch: `implementation/real-table-compare`. No applicable AGENTS.md found. Baseline: 53 offline tests passed; no user modifications present.

1. Verified incorrect WikiDBs fallback, unknown-only aligner, missing retrieval/ranking/evaluation, catalog/runtime gap and conflicting documentation.
2. Migration inventory: extracted `actions` becomes `intentions`; instance `id` stays an instance ID, binding references become `intention_instance_id`; catalog `action_id` becomes `intention_id`; library identity becomes `il_version`/`il_path`; `grounded_card` becomes `grounded_intention`; verdict `unknown` becomes `unresolved`. External argparse `action=` stays unchanged. Frozen proposals and historical outputs remain unchanged; explicit legacy readers migrate old inputs. No manuscript is available to verify paper consistency.

Scope change authorized by the researcher: direct documented-value comparison AND explicit group-mean comparison. This supersedes the old direct-observation-only policy; no causal interpretation or automatic averaging of precomputed means.
