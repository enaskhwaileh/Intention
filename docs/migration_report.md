# Migration report

## Preserved

- Branch `mvp-restart` and checkpoint `1a8ac2915628a268a25eed94a2cc607a95af365d`.
- The complete `src/intention_mvp` deterministic implementation.
- Vaccine configuration, fixture, runner, documentation, and 12 regression
  tests.
- Historical implementation at commit `030fe82`, untouched in Git history.

## Added alongside the MVP

The new `src/intention` package establishes validated research contracts and a
versioned action/predicate registry. YAML configurations are new scientific
contracts; existing JSON configurations remain the authoritative inputs for the
preserved regression runner.

## Superseded but not removed

The MVP dataclasses and action catalogue are too narrow for the five-action
research system. They remain executable regression assets. New development
will target `src/intention`; specific MVP components may be translated only
after equivalent behavior and tests exist.

No file or directory was removed in Phases 0–2. No code from `030fe82` was
restored.
