#!/bin/bash
# Runs the full experiment suite on this Mac. Log: experiments/run_log.txt
cd "$(dirname "$0")"
LOG=experiments/run_log.txt
mkdir -p experiments
exec > >(tee -a "$LOG") 2>&1
step(){ echo; echo "=== [$(date '+%H:%M:%S')] $*"; }
step "START $(date)"
PY=./.venv-sbert/bin/python
if [ ! -x "$PY" ]; then step "creating .venv-sbert"; python3.12 -m venv .venv-sbert || python3 -m venv .venv-sbert; fi
step "installing dependencies into .venv-sbert (torch / numpy pinned to the versions that work on this Mac)"
printf 'numpy==1.26.4\ntorch==2.2.2\npyarrow<20\ndatasets<4\n' > /tmp/ig-constraints.txt
UV=""
for c in "$(command -v uv)" "$HOME/.local/bin/uv" "$HOME/.cargo/bin/uv" /usr/local/bin/uv /opt/homebrew/bin/uv; do [ -n "$c" ] && [ -x "$c" ] && UV="$c" && break; done
if [ -n "$UV" ]; then echo "using $UV"; INSTALL() { "$UV" pip install --python "$PY" -c /tmp/ig-constraints.txt "$@"; }
else $PY -m ensurepip --upgrade >/dev/null 2>&1; INSTALL() { $PY -m pip install -q -c /tmp/ig-constraints.txt "$@"; }; fi
INSTALL "pandas<2.3" python-dotenv "datasets<4" "pyarrow<20" || echo "WARN: pandas/datasets install had errors"
INSTALL -e . --no-deps
STORE=numpy
if INSTALL chromadb && $PY -c "import chromadb" 2>/dev/null; then STORE=chroma
elif INSTALL faiss-cpu && $PY -c "import faiss" 2>/dev/null; then STORE=faiss; fi
echo "vector store: $STORE"
$PY -c "import sentence_transformers, torch, pandas, sklearn; print('sbert', sentence_transformers.__version__, 'torch', torch.__version__, 'pandas', pandas.__version__)" || { echo "FATAL: required packages missing"; exit 1; }
step "building the IGBench corpus (git downloads OWID + Rdatasets once)"
$PY -m intention_grounding.acquire --offline || $PY -m intention_grounding.acquire
$PY -m intention_grounding.corpus fetch
$PY -m intention_grounding.corpus build
step "unit tests"
$PY -m unittest discover -s tests 2>&1 | tail -4
step "IGBench held-out test: BM25, TF-IDF, SBERT, hybrid (+ intention grounding on each)"
$PY -m intention_grounding.experiments --vector-store $STORE --context bm25,tfidf,sbert,hybrid --benchmark benchmarks/igbench_v1/test_queries.json --tag mac_test \
  --systems ctx:bm25,ctx:tfidf,ctx:sbert,ctx:hybrid,ig:gold/gold:bm25,ig:rule/index:bm25,ig:gold/gold:sbert,ig:rule/index:sbert,ig:gold/gold:hybrid,ig:rule/index:hybrid
step "IGBench development set"
$PY -m intention_grounding.experiments --vector-store $STORE --context bm25,tfidf,sbert,hybrid --tag mac_dev \
  --systems ctx:bm25,ctx:tfidf,ctx:sbert,ctx:hybrid,ig:gold/gold:bm25,ig:rule/index:bm25,ig:gold/gold:sbert,ig:rule/index:sbert,ig:gold/gold:hybrid,ig:rule/index:hybrid
step "IGBench ablations (held-out test)"
$PY -m intention_grounding.experiments --vector-store $STORE --systems ablations --benchmark benchmarks/igbench_v1/test_queries.json --tag mac_test_ablations
step "scalability"
$PY -m intention_grounding.scaling --sample 300 --seed 7
for DS in bird-validation infiagentda spider-test; do
  step "TARGET $DS: import"
  if $PY -m intention_grounding.target_import --dataset $DS --max-rows 2000; then
    step "TARGET $DS: experiments"
    $PY -m intention_grounding.experiments --vector-store $STORE --corpus data/corpus/target-$DS/manifest.json \
      --benchmark benchmarks/target/$DS.json --systems target --context bm25,sbert --tag mac_target_$DS
  else echo "WARN: import of $DS failed"; fi
done
step "ALL DONE $(date)"
echo "You can close this window."
