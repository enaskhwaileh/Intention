#!/bin/bash
# Full experiment suite on beauty (GPU). Usage: bash run_server.sh igbench|target
source /datastore-beast/servers/Enas/intention/env.sh
step(){ echo; echo "=== [$(date '+%H:%M:%S')] $*"; }
X="python -m intention_grounding.experiments --vector-store ${VS:-chroma}"
if [ "$1" = igbench ]; then
  step "corpus"; python -m intention_grounding.acquire --offline || python -m intention_grounding.acquire
  python -m intention_grounding.corpus fetch && python -m intention_grounding.corpus build
  step "tests"; python -m unittest discover -s tests 2>&1 | tail -3
  SYS=ctx:bm25,ctx:tfidf,ctx:lsa,ctx:sbert,ctx:hybrid,ig:gold/gold:bm25,ig:rule/index:bm25,ig:gold/gold:tfidf,ig:rule/index:tfidf,ig:gold/gold:sbert,ig:rule/index:sbert,ig:gold/gold:hybrid,ig:rule/index:hybrid
  step "IGBench test"; $X --context bm25,tfidf,lsa,sbert,hybrid --benchmark benchmarks/igbench_v1/test_queries.json --systems $SYS --tag srv_test
  step "IGBench dev";  $X --context bm25,tfidf,lsa,sbert,hybrid --systems $SYS --tag srv_dev
  for M in intfloat/e5-base-v2 BAAI/bge-base-en-v1.5; do
    T=$(basename $M)
    step "IGBench test, encoder $M"; $X --context sbert --sbert-model $M --benchmark benchmarks/igbench_v1/test_queries.json --systems ctx:sbert,ig:gold/gold:sbert,ig:rule/index:sbert --tag srv_test_$T
    step "IGBench dev, encoder $M";  $X --context sbert --sbert-model $M --systems ctx:sbert,ig:gold/gold:sbert,ig:rule/index:sbert --tag srv_dev_$T
  done
  step "ablations"; $X --systems ablations --benchmark benchmarks/igbench_v1/test_queries.json --tag srv_test_ablations
  $X --systems ablations --tag srv_dev_ablations
  step "scaling"; python -m intention_grounding.scaling --sample 300 --seed 7
else
  for DS in bird-validation spider-test; do
    step "TARGET $DS import"; python -m intention_grounding.target_import --dataset $DS --max-rows 2000 || continue
    step "TARGET $DS run"; $X --corpus data/corpus/target-$DS/manifest.json --benchmark benchmarks/target/$DS.json --systems target --context bm25,sbert --tag srv_target_$DS
  done
fi
step "DONE $1"
