# Experiment status — 2026-10-28 16:40

## Progress

| Part | Done |
|---|---|
| Current run (all except Groq) | 68 / 68 ✅ |
|   IGBench, no LLM | 22 / 22 ✅ |
|   IGBench, Qwen-14B / 32B | 24 / 24 ✅ |
|   BIRD + Spider, no LLM | 10 / 10 ✅ |
|   BIRD + Spider, Qwen-14B | 6 / 6 ✅ |
|   BIRD + Spider, Qwen-32B | 6 / 6 ✅ |
| Next run: Groq | 0 / 18  |

## What is happening now

- Current run: not running
- Groq run: [2026-10-28 11:48] smoke test failed; not starting the full Groq run 
- Groq key on the server: **no** — add intention_grounding/.env
- GPU (free, used, utilisation): 17408 MiB, 23037 MiB, 100 %
- Our LLM server: off

## Last 10 events

```
== LLM profile q32: started (attempt 1)
== [20:07:13] run igb-dev.bm25.q32: 10 systems
   -> ok 619s
== [20:17:31] run igb-dev.minilm.q32: 8 systems
   -> ok 738s
== [20:29:49] run igb-test.bm25.q32: 10 systems
   -> ok 410s
== [20:36:39] run igb-test.minilm.q32: 8 systems
   -> ok 407s
== summary
```

## Cells needing attention

none

## Paper tables

experiments/paper/tables.md, updated 2026-10-27 20:52
