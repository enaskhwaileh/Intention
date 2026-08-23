# Reproducibility

## Current deterministic checkpoint

```bash
python3 -m pip install -e ".[dev]"
pytest -q
python3 scripts/run_vaccine_mvp.py
```

The core test suite must remain offline. YAML registry configuration is loaded
from the repository and validated before use.

## Not yet reproducible

No external benchmark, model checkpoint, baseline run, ablation, statistical
test, paper figure, or result table has been produced. Future runs must record
the Git commit, configuration version, benchmark version, seed, commands, and
raw measured outputs.
