#!/bin/bash
# TARGET benchmarks on beauty, intention-grounding systems parallelised over 32 worker processes.
source /datastore-beast/servers/Enas/intention/env.sh
export PYTHONUNBUFFERED=1
X="python -m intention_grounding.experiments --vector-store faiss --workers 32"
echo "=== [$(date '+%H:%M:%S')] equivalence check: IGBench test, gold/gold:bm25 with 16 workers (expect nDCG 0.8569)"
$X --workers 16 --benchmark benchmarks/igbench_v1/test_queries.json --context bm25 --systems ig:gold/gold:bm25 --tag srv_check_workers
for DS in bird-validation spider-test; do
  [ -s benchmarks/target/$DS.json ] || python -m intention_grounding.target_import --dataset $DS --max-rows 2000 || continue
  echo "=== [$(date '+%H:%M:%S')] TARGET $DS"
  $X --corpus data/corpus/target-$DS/manifest.json --benchmark benchmarks/target/$DS.json --context bm25,sbert --tag srv_target_$DS \
     --systems ctx:bm25,ctx:sbert,ig:rule/index:bm25,ig:rule/index:sbert,ig:rule/index:bm25+rnorm=minmax,ig:rule/index:sbert+rnorm=minmax
done
echo "=== DONE target"
