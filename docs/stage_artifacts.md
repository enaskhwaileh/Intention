# Stage artifact contract

The future orchestrator will expose serializable artifacts named:

```text
stage_00_input
stage_01_interpretation
stage_02_grounded_action
stage_03_requirement_profile
stage_04_table_capability_profiles
stage_05_topical_candidates
stage_06_requirement_matches
stage_07_feasibility
stage_08_alignment
stage_09_usefulness_ranking
stage_10_explanations
```

Phases 0–2 define shared types for these boundaries but do not generate the
artifacts. Later stages must validate their inputs and outputs, serialize
deterministically, and return meaningful errors.
