# Milestone demo snapshots

These JSON files are deterministic observability artifacts, not experimental
or paper results. Each snapshot uses the same synthetic input and records the
actual structured outputs of the implementation at the named milestone commit.

Directories older than `CURRENT_MILESTONE` in
`src/intention/demonstrator.py` are immutable. Never regenerate, reformat, or
edit them in place. A new milestone adds a new numbered directory. The envelope
is intentionally API-friendly:

- `snapshot_schema_version` identifies the transport contract.
- `milestone`, `classification`, and `provenance` identify the artifact.
- `stage_order` gives presentation order without coupling clients to keys.
- `stages` contains typed JSON artifacts for every pipeline boundary.
- `stage_digest` verifies the canonical stage payload.

`manifest.json` pins the full-file SHA-256 of every historical snapshot; the
test suite fails if an immutable archive is changed.

Regenerate the current snapshot:

```bash
PYTHONPATH=src python3 -m intention demo-snapshot
```

Verify it without writing:

```bash
PYTHONPATH=src python3 -m intention demo-snapshot --check
```
