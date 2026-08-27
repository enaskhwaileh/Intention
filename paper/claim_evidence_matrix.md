# Claim-evidence matrix

| Candidate claim | Required evidence | Current status | Required experiment | Available result | Limitation |
| --- | --- | --- | --- | --- | --- |
| Intended action can change a ranking for a fixed topic and pool | Executed action-switch example | implemented regression | preserve fixtures | three topic pairs and all five actions pass | handcrafted scenarios |
| Action-aware ranking improves suitability | Independent judgments and baselines | unsupported | benchmark reranking evaluation | none | no benchmark or annotations |
| Five actions are supported end to end | Tests and traces for all five | synthetic support verified | real benchmark integration | six controlled cases | no real-corpus evidence |
| Capability profiles can be extracted offline | Extraction annotations and tests | synthetic heuristics implemented | profiler gold evaluation | deterministic fixture profiles | no independent extraction labels |
| Explanations are provenance grounded | Trace audit or judgment | component traces implemented | broader explanation evaluation | synthetic traces | no user evaluation |
| The approach is novel relative to prior work | Verified literature comparison | unsupported | related-work review | none | broad first-work claim rejected |

Existing placeholder result tables must remain labeled placeholders or be
removed from a submission; they must never be filled with invented values.
