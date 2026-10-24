"""Text encoders for dense context matching.

SBERTEncoder wraps sentence-transformers. Queries and tables (passages) can use
different prefixes, as required by instruction-tuned retrieval models:

  sentence-transformers/all-MiniLM-L6-v2   no prefixes (default; 384 dims, 256 tokens)
  intfloat/e5-base-v2                      "query: " / "passage: "
  BAAI/bge-small-en-v1.5                   query instruction, no passage prefix

HashEncoder is a deterministic bag-of-words encoder used in tests and as an
offline stand-in; it is not a semantic model.
"""
import hashlib
import re
import time

PREFIXES = {
    "e5": ("query: ", "passage: "),
    "bge": ("Represent this sentence for searching relevant passages: ", ""),
}
DEFAULT_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def prefixes_for(model):
    name = model.lower()
    for key, pair in PREFIXES.items():
        if key in name:
            return pair
    return ("", "")


class SBERTEncoder:
    def __init__(self, model=DEFAULT_MODEL, *, device="cpu", batch_size=64, query_prefix=None, passage_prefix=None):
        from sentence_transformers import SentenceTransformer
        self.model_name = model
        self.model = SentenceTransformer(model, device=device)
        qp, pp = prefixes_for(model)
        self.query_prefix = qp if query_prefix is None else query_prefix
        self.passage_prefix = pp if passage_prefix is None else passage_prefix
        self.batch_size = batch_size
        self.dim = self.model.get_sentence_embedding_dimension()
        self.max_tokens = getattr(self.model, "max_seq_length", None)

    @property
    def identity(self):
        return {"encoder": "sbert", "model": self.model_name, "dim": self.dim, "max_tokens": self.max_tokens,
                "query_prefix": self.query_prefix, "passage_prefix": self.passage_prefix}

    def encode(self, texts, kind="passage"):
        prefix = self.query_prefix if kind == "query" else self.passage_prefix
        return self.model.encode([prefix + t for t in texts], batch_size=self.batch_size,
                                 normalize_embeddings=True, show_progress_bar=False, convert_to_numpy=True)


class HashEncoder:
    """Deterministic hashed bag-of-words vectors (unit length). Offline tests only."""
    def __init__(self, dim=256):
        self.dim, self.model_name = dim, f"hash-bow-{dim}"

    @property
    def identity(self):
        return {"encoder": "hash", "model": self.model_name, "dim": self.dim}

    def encode(self, texts, kind="passage"):
        import numpy as np
        out = np.zeros((len(texts), self.dim), dtype="float32")
        for i, text in enumerate(texts):
            for tok in re.findall(r"[a-z0-9]+", text.lower()):
                tok = tok[:-1] if len(tok) > 3 and tok.endswith("s") else tok
                out[i, int(hashlib.md5(tok.encode()).hexdigest(), 16) % self.dim] += 1.0
            norm = float((out[i] ** 2).sum()) ** 0.5
            if norm:
                out[i] /= norm
        return out


def timed_encode(encoder, texts, kind):
    start = time.perf_counter()
    vectors = encoder.encode(texts, kind=kind)
    return vectors, round((time.perf_counter() - start) * 1000, 3)
