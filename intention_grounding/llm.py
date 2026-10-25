"""Minimal OpenAI-compatible chat client with a content-addressed response cache.

Works with Groq (default), OpenAI, or any OpenAI-compatible server (e.g. a local
Ollama/vLLM endpoint) through plain HTTPS, so no SDK is required.

Configuration (environment or intention_grounding/.env):
  IG_LLM_BASE_URL  default https://api.groq.com/openai/v1
  IG_LLM_API_KEY   falls back to GROQ_API_KEY
  IG_LLM_MODEL     falls back to GROQ_MODEL_ID
  IG_LLM_TIMEOUT   seconds per call (default 120)

A local server works the same way, e.g. vLLM on a GPU:
  IG_LLM_BASE_URL=http://localhost:8765/v1 IG_LLM_API_KEY=EMPTY IG_LLM_MODEL=Qwen/Qwen2.5-14B-Instruct-AWQ

Every call is cached under data/runtime/llm-cache/<sha256>.json, keyed by the
model, prompt version and messages. Re-running an experiment therefore replays
identical responses and costs nothing; `allow_live=False` forbids new calls.
"""
import hashlib
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = Path(__file__).resolve().parent / ".env"
DEFAULT_CACHE = ROOT / "data" / "runtime" / "llm-cache"


class LLMUnavailable(RuntimeError):
    """No credentials/model, live calls disabled and no cached response."""


def _load_env():
    if ENV_PATH.is_file():
        try:
            from dotenv import load_dotenv
            load_dotenv(ENV_PATH, override=False, interpolate=False)
        except ImportError:  # minimal parser fallback
            for line in ENV_PATH.read_text().splitlines():
                if "=" in line and not line.lstrip().startswith("#"):
                    key, value = line.split("=", 1)
                    os.environ.setdefault(key.strip(), value.strip())


def config():
    _load_env()
    return {
        "base_url": os.environ.get("IG_LLM_BASE_URL", "https://api.groq.com/openai/v1").rstrip("/"),
        "api_key": os.environ.get("IG_LLM_API_KEY") or os.environ.get("GROQ_API_KEY") or "",
        "model": os.environ.get("IG_LLM_MODEL") or os.environ.get("GROQ_MODEL_ID") or "",
    }


class ChatClient:
    def __init__(self, *, model=None, temperature=0.0, max_tokens=2048, timeout=None,
                 cache_dir=DEFAULT_CACHE, allow_live=True, base_url=None, api_key=None):
        cfg = config()
        self.model = model or cfg["model"]
        self.base_url = (base_url or cfg["base_url"]).rstrip("/")
        self._api_key = api_key if api_key is not None else cfg["api_key"]
        self.temperature, self.max_tokens = temperature, max_tokens
        self.timeout = float(timeout if timeout is not None else os.environ.get("IG_LLM_TIMEOUT", 120))
        self.cache_dir = Path(cache_dir) if cache_dir else None
        self.allow_live = allow_live
        self.calls = []  # per-call records: cache hit, latency, usage

    def key(self, messages, prompt_version):
        payload = {"model": self.model, "temperature": self.temperature, "max_tokens": self.max_tokens,
                   "prompt_version": prompt_version, "messages": messages}
        return hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode()).hexdigest()

    def complete_json(self, messages, *, prompt_version):
        """Return (raw_text, record). Raises LLMUnavailable when no response can be produced."""
        key = self.key(messages, prompt_version)
        path = self.cache_dir / f"{key}.json" if self.cache_dir else None
        start = time.perf_counter()
        if path and path.exists():
            stored = json.loads(path.read_text(encoding="utf-8"))
            record = {"cache_hit": True, "cache_key": key, "model": stored.get("model"),
                      "usage": stored.get("usage"), "latency_ms": round((time.perf_counter() - start) * 1000, 3),
                      "original_latency_ms": stored.get("latency_ms")}
            self.calls.append(record)
            return stored["content"], record
        if not self.allow_live:
            raise LLMUnavailable("LIVE_CALLS_DISABLED_AND_NOT_CACHED")
        if not self._api_key or not self.model:
            raise LLMUnavailable("MISSING_LLM_CREDENTIALS_OR_MODEL")
        body = json.dumps({"model": self.model, "temperature": self.temperature, "max_tokens": self.max_tokens,
                           "response_format": {"type": "json_object"}, "messages": messages}).encode()
        request = urllib.request.Request(self.base_url + "/chat/completions", data=body, method="POST",
                                         headers={"Content-Type": "application/json",
                                                  "Authorization": "Bearer " + self._api_key})
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                data = json.loads(response.read().decode())
        except urllib.error.HTTPError as exc:
            raise LLMUnavailable(f"HTTP_{exc.code}") from None
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            raise LLMUnavailable("CONNECTION_FAILED:" + type(exc).__name__) from None
        latency = round((time.perf_counter() - start) * 1000, 3)
        content = data["choices"][0]["message"]["content"]
        usage = data.get("usage")
        if path:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps({"model": data.get("model", self.model), "requested_model": self.model,
                                        "prompt_version": prompt_version, "messages": messages,
                                        "content": content, "usage": usage, "latency_ms": latency},
                                       ensure_ascii=False, indent=1), encoding="utf-8")
        record = {"cache_hit": False, "cache_key": key, "model": data.get("model", self.model),
                  "usage": usage, "latency_ms": latency}
        self.calls.append(record)
        return content, record


def parse_json_object(raw):
    """Strict JSON object parsing: no duplicate keys, no NaN/Infinity, object at top level."""
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError("DUPLICATE_KEY")
            result[key] = value
        return result

    def constant(_):
        raise ValueError("NON_JSON_CONSTANT")

    if not isinstance(raw, str):
        raise ValueError("NON_TEXT_RESPONSE")
    text = raw.strip()
    if text.startswith("```"):
        text = text.strip("`")
        text = text[text.find("{"):]
    value = json.loads(text, object_pairs_hook=pairs, parse_constant=constant)
    if not isinstance(value, dict):
        raise ValueError("NOT_AN_OBJECT")
    return value
