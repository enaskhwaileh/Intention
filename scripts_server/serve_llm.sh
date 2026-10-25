#!/bin/bash
# OpenAI-compatible LLM endpoint on the A100 for the Interpreter and Grounder (port 8765, this machine only).
E=/datastore-beast/servers/Enas/intention
export HF_HOME=$E/cache/huggingface
export VLLM_USE_V1=0
exec $E/venvs/vllm/bin/vllm serve Qwen/Qwen2.5-14B-Instruct-AWQ --host 127.0.0.1 --port 8765 \
  --gpu-memory-utilization 0.68 --max-model-len 12288 --max-num-seqs 32 --seed 0 --enforce-eager --served-model-name Qwen/Qwen2.5-14B-Instruct-AWQ
