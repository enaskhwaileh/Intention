#!/bin/bash
# Score calibration check: context score r rescaled over the candidate list (rnorm=minmax) before F(r, A).
source /datastore-beast/servers/Enas/intention/env.sh
while pgrep -f "run_server.sh igbench" >/dev/null; do sleep 30; done
X="python -m intention_grounding.experiments --vector-store chroma"
for SPLIT in dev test; do
  B=""; [ $SPLIT = test ] && B="--benchmark benchmarks/igbench_v1/test_queries.json"
  echo "=== [$(date '+%H:%M:%S')] $SPLIT MiniLM / BM25 / TF-IDF / hybrid"
  $X $B --context bm25,tfidf,sbert,hybrid --tag srv_${SPLIT}_rnorm --systems \
ig:gold/gold:bm25+rnorm=minmax,ig:rule/index:bm25+rnorm=minmax,ig:gold/gold:tfidf+rnorm=minmax,ig:rule/index:tfidf+rnorm=minmax,ig:gold/gold:sbert+rnorm=minmax,ig:rule/index:sbert+rnorm=minmax,ig:gold/gold:hybrid+rnorm=minmax,ig:rule/index:hybrid+rnorm=minmax
  for M in intfloat/e5-base-v2 BAAI/bge-base-en-v1.5; do
    echo "=== [$(date '+%H:%M:%S')] $SPLIT $M"
    $X $B --context sbert --sbert-model $M --tag srv_${SPLIT}_rnorm_$(basename $M) --systems ig:gold/gold:sbert+rnorm=minmax,ig:rule/index:sbert+rnorm=minmax
  done
done
echo "=== DONE calibration"
