#!/bin/bash
# After the profiler fix (derived-series cache outside df.attrs): equivalence check, TARGET LLM, then timing reruns.
source /datastore-beast/servers/Enas/intention/env.sh
export PYTHONUNBUFFERED=1 IG_LLM_BASE_URL=http://127.0.0.1:8765/v1 IG_LLM_API_KEY=EMPTY IG_LLM_MODEL=Qwen/Qwen2.5-14B-Instruct-AWQ IG_LLM_TIMEOUT=300
X="python -m intention_grounding.experiments"
echo "=== [$(date '+%H:%M:%S')] equivalence: IGBench test (expect 0.8569 / 0.8256)"
$X --vector-store chroma --benchmark benchmarks/igbench_v1/test_queries.json --context bm25 --systems ig:gold/gold:bm25,ig:rule/index:bm25 --tag srv_check_fix
for DS in bird-validation spider-test; do
  echo "=== [$(date '+%H:%M:%S')] TARGET $DS, LLM v3.1"
  $X --allow-live --vector-store faiss --workers 32 --corpus data/corpus/target-$DS/manifest.json --benchmark benchmarks/target/$DS.json --context bm25,sbert --tag srv_target_${DS}_llm31 \
     --systems ctx:bm25,ctx:sbert,ig:llm/llm:bm25+repair=1,ig:llm/llm:sbert+repair=1,ig:llm/llm:bm25+repair=1+rnorm=minmax,ig:llm/llm:sbert+repair=1+rnorm=minmax
done
echo "=== [$(date '+%H:%M:%S')] timing reruns, one process (no workers), after the fix"
$X --vector-store faiss --corpus data/corpus/target-bird-validation/manifest.json --benchmark benchmarks/target/bird-validation.json --context bm25,sbert --tag srv_target_bird-validation_timing --systems ctx:bm25,ctx:sbert,ig:rule/index:bm25,ig:rule/index:sbert
$X --vector-store chroma --benchmark benchmarks/igbench_v1/test_queries.json --tag srv_test_timing --context bm25,tfidf,lsa,sbert,hybrid \
   --systems ctx:bm25,ctx:sbert,ig:gold/gold:bm25,ig:rule/index:bm25,ig:gold/gold:sbert,ig:rule/index:sbert
python -m intention_grounding.scaling --sample 300 --seed 7
echo "=== DONE after fix"
