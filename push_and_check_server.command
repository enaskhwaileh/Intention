#!/bin/bash
# Commit + push the current work, then check that the GPU server "beauty" is reachable without a password prompt.
cd "$(dirname "$0")"
exec > >(tee experiments/push_and_server_log.txt) 2>&1
echo "=== git"
git add -A
git commit -q -F - <<'MSG' || echo "(nothing new to commit)"
SBERT/ChromaDB context matching, TARGET importer (BIRD, Spider), Mac experiment runs

- IGBench test/dev runs with BM25, TF-IDF, SBERT and hybrid, with intention grounding on each
- ablations and scaling re-run on macOS
- TARGET importer reads hub files directly and uses BIRD column documentation
- launcher scripts for the full suite and the TARGET benchmarks

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01GUB4sFF8rBgY7k6twk516m
MSG
git log --oneline -1
git push -u origin "$(git branch --show-current)" && echo "PUSH_OK"
echo "=== ssh beauty"
ssh -o BatchMode=yes -o ConnectTimeout=15 beauty 'echo SSH_OK; hostname; whoami; uname -a; nvidia-smi --query-gpu=name,memory.total,memory.used --format=csv 2>&1 | head -5; which python3 conda uv git 2>/dev/null; python3 --version; df -h ~ | tail -1; nproc; free -g | head -2'
echo "=== done (exit $?)"
