#!/bin/bash
# TARGET with the LLM configuration (prompts v3.1, one repair). Waits for the vLLM endpoint.
source /datastore-beast/servers/Enas/intention/env.sh
export PYTHONUNBUFFERED=1 IG_LLM_BASE_URL=http://127.0.0.1:8765/v1 IG_LLM_API_KEY=EMPTY IG_LLM_MODEL=Qwen/Qwen2.5-14B-Instruct-AWQ IG_LLM_TIMEOUT=300
until curl -s localhost:8765/v1/models >/dev/null; do sleep 10; done
for DS in bird-validation spider-test; do
  echo "=== [$(date '+%H:%M:%S')] TARGET $DS, LLM v3.1"
  python -m intention_grounding.experiments --allow-live --vector-store faiss --workers 32 --corpus data/corpus/target-$DS/manifest.json --benchmark benchmarks/target/$DS.json --context bm25,sbert --tag srv_target_${DS}_llm31 \
     --systems ctx:bm25,ctx:sbert,ig:llm/llm:bm25+repair=1,ig:llm/llm:sbert+repair=1,ig:llm/llm:bm25+repair=1+rnorm=minmax,ig:llm/llm:sbert+repair=1+rnorm=minmax
done
echo "=== DONE llm target"
