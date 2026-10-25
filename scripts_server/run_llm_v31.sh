#!/bin/bash
# LLM configuration with prompts v3.1 (with and without one validator-guided repair), then TARGET.
source /datastore-beast/servers/Enas/intention/env.sh
export PYTHONUNBUFFERED=1 IG_LLM_BASE_URL=http://127.0.0.1:8765/v1 IG_LLM_API_KEY=EMPTY IG_LLM_MODEL=Qwen/Qwen2.5-14B-Instruct-AWQ IG_LLM_TIMEOUT=300
python -m unittest discover -s tests 2>&1 | tail -1
X="python -m intention_grounding.experiments --allow-live --vector-store chroma --workers 16"
SYS=ctx:bm25,ctx:tfidf,ctx:sbert,ctx:hybrid
for M in bm25 tfidf sbert hybrid; do SYS=$SYS,ig:llm/llm:$M,ig:llm/llm:$M+rnorm=minmax,ig:llm/llm:$M+repair=1,ig:llm/llm:$M+repair=1+rnorm=minmax; done
SYS=$SYS,ig:gold/llm:bm25,ig:llm/index:bm25,ig:gold/llm:bm25+repair=1,ig:llm/index:bm25+repair=1
for SPLIT in dev test; do
  B=""; [ $SPLIT = test ] && B="--benchmark benchmarks/igbench_v1/test_queries.json"
  echo "=== [$(date '+%H:%M:%S')] IGBench $SPLIT, LLM v3.1"
  $X $B --context bm25,tfidf,sbert,hybrid --systems $SYS --tag srv_${SPLIT}_llm31
  for M in intfloat/e5-base-v2 BAAI/bge-base-en-v1.5; do
    $X $B --context sbert --sbert-model $M --systems ctx:sbert,ig:llm/llm:sbert,ig:llm/llm:sbert+rnorm=minmax,ig:llm/llm:sbert+repair=1,ig:llm/llm:sbert+repair=1+rnorm=minmax --tag srv_${SPLIT}_llm31_$(basename $M)
  done
done
for DS in bird-validation spider-test; do
  while [ ! -s benchmarks/target/$DS.json ]; do sleep 60; done
  echo "=== [$(date '+%H:%M:%S')] TARGET $DS, LLM v3.1"
  python -m intention_grounding.experiments --allow-live --vector-store faiss --workers 32 --corpus data/corpus/target-$DS/manifest.json --benchmark benchmarks/target/$DS.json --context bm25,sbert --tag srv_target_${DS}_llm31 \
     --systems ctx:bm25,ctx:sbert,ig:llm/llm:bm25+repair=1,ig:llm/llm:sbert+repair=1,ig:llm/llm:bm25+repair=1+rnorm=minmax,ig:llm/llm:sbert+repair=1+rnorm=minmax
done
echo "=== DONE llm v3.1"
