#!/bin/bash
# LLM configuration (paper's main system): LLM Interpreter + LLM Grounder, served locally by vLLM (serve_llm.sh).
source /datastore-beast/servers/Enas/intention/env.sh
export PYTHONUNBUFFERED=1 IG_LLM_BASE_URL=http://127.0.0.1:8765/v1 IG_LLM_API_KEY=EMPTY IG_LLM_MODEL=Qwen/Qwen2.5-14B-Instruct-AWQ IG_LLM_TIMEOUT=300
X="python -m intention_grounding.experiments --allow-live --vector-store chroma --workers 16"
SYS=ig:llm/llm:bm25,ig:llm/llm:tfidf,ig:llm/llm:sbert,ig:llm/llm:hybrid,ig:llm/llm:bm25+rnorm=minmax,ig:llm/llm:tfidf+rnorm=minmax,ig:llm/llm:sbert+rnorm=minmax,ig:llm/llm:hybrid+rnorm=minmax,ig:llm/index:bm25,ig:gold/llm:bm25,ig:llm/gold:bm25,ctx:bm25,ctx:tfidf,ctx:sbert,ctx:hybrid
for SPLIT in test dev; do
  B=""; [ $SPLIT = test ] && B="--benchmark benchmarks/igbench_v1/test_queries.json"
  echo "=== [$(date '+%H:%M:%S')] IGBench $SPLIT, LLM"
  $X $B --context bm25,tfidf,sbert,hybrid --systems $SYS --tag srv_${SPLIT}_llm
  for M in intfloat/e5-base-v2 BAAI/bge-base-en-v1.5; do
    $X $B --context sbert --sbert-model $M --systems ctx:sbert,ig:llm/llm:sbert,ig:llm/llm:sbert+rnorm=minmax --tag srv_${SPLIT}_llm_$(basename $M)
  done
done
for DS in bird-validation spider-test; do
  while [ ! -s benchmarks/target/$DS.json ]; do sleep 60; done
  echo "=== [$(date '+%H:%M:%S')] TARGET $DS, LLM"
  $X --vector-store faiss --workers 32 --corpus data/corpus/target-$DS/manifest.json --benchmark benchmarks/target/$DS.json --context bm25,sbert --tag srv_target_${DS}_llm \
     --systems ctx:bm25,ctx:sbert,ig:llm/llm:bm25,ig:llm/llm:sbert,ig:llm/llm:bm25+rnorm=minmax,ig:llm/llm:sbert+rnorm=minmax
done
echo "=== DONE llm"
