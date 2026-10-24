#!/bin/bash
# TARGET benchmark import + experiments. Log: experiments/run_target_log.txt
cd "$(dirname "$0")"
exec > >(tee -a experiments/run_target_log.txt) 2>&1
step(){ echo; echo "=== [$(date '+%H:%M:%S')] $*"; }
PY=./.venv-sbert/bin/python
STORE=chroma; $PY -c "import chromadb" 2>/dev/null || STORE=numpy
step "TARGET datasets on the hub"
# (hub listing done)
for DS in bird-validation spider-test; do
  step "TARGET $DS: import"
  if $PY -m intention_grounding.target_import --dataset $DS --max-rows 2000 && [ -s benchmarks/target/$DS.json ]; then
    step "TARGET $DS: experiments"
    $PY -m intention_grounding.experiments --vector-store $STORE --corpus data/corpus/target-$DS/manifest.json \
      --benchmark benchmarks/target/$DS.json --systems target --context bm25,sbert --tag mac_target_$DS
  else echo "WARN: import of $DS failed"; fi
done
step "ALL DONE $(date)"
