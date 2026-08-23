# MVP implementation status

## Repository inspection

The current `main` branch begins from intentional cleanup commit `5a9fdd7`, which
removed the previous implementation. The immediately preceding commit (`030fe82`)
was inspected through Git history. It contained:

- Pydantic models for queries, grounded intentions, operational profiles, and
  table profiles;
- YAML-based intended-action and predicate definitions;
- grounding, profile instantiation, profile validation, and Boolean ranking;
- a separate deterministic capability-extraction package and tests.

## Reuse

Because the current branch deliberately removed those files, no source file was
restored. The MVP reuses their useful architectural boundaries: typed domain
objects, configuration-driven action templates, explicit validation, separate
matching/ranking stages, and deterministic tests.

## Missing components at the clean baseline

The clean baseline had no package, configuration, fixtures, tests, demo, or
documentation. It also had no weighted requirement matching, required-evidence
gate, action-conditioned usefulness score, fallback, or provenance-grounded
explanation.

## MVP assumptions

- Actions and capability profiles are manually supplied, with confidence `1.0`
  unless a fixture explicitly represents partial evidence.
- The provisional operational axes are `content`, `structure`, `analysis`,
  `scope`, `relation`, and `quality`; `relation` is defined but inactive.
- String containment and set overlap are sufficient transparent value rules for
  this fixture. There is no semantic model.
- Patient records can partially support country comparison because their country
  field permits aggregation; they do not directly contain precomputed rates.
- Failed required evidence demotes rather than removes a candidate.
- The standard library is sufficient; dataclasses avoid adding a validation
  framework to the intentionally clean repository.
