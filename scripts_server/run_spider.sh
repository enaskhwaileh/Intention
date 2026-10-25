#!/bin/bash
source /datastore-beast/servers/Enas/intention/env.sh; export PYTHONUNBUFFERED=1
python -m intention_grounding.experiments --vector-store faiss --workers 32 --corpus data/corpus/target-spider-test/manifest.json --benchmark benchmarks/target/spider-test.json --context bm25,sbert --tag srv_target_spider-test_full \
  --systems ctx:bm25,ctx:sbert,ig:rule/index:bm25,ig:rule/index:sbert,ig:rule/index:bm25+rnorm=minmax,ig:rule/index:sbert+rnorm=minmax
echo "=== DONE spider"
