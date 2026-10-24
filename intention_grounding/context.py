"""Context matching: r(q_u, T) in [0, 1] and top-k candidate retrieval.

Each table is serialised from its documentation and schema (title, description,
attribute names and descriptions, a few categorical values). Methods:
  bm25        lexical BM25 (Robertson/Sparck Jones), r = score / max score for q
  tfidf       TF-IDF cosine (scikit-learn)
  lsa         latent semantic analysis (TF-IDF + truncated SVD) cosine
  sbert       Sentence-BERT cosine (optional; needs sentence-transformers)
  hybrid      0.5 * bm25 + 0.5 * dense (sbert if available else lsa)
Indexes are cached per corpus and method; build and query times are recorded.
"""
import hashlib
import json
import math
import pickle
import re
import time
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX_DIR = ROOT / "data" / "runtime" / "index"
SERIALIZATION = "title-description-columns-values-v1+plural-stem"
_TOKEN = re.compile(r"[a-z0-9]+")


def _stem(tok):
    """Minimal plural stemming (s/es/ies), standard for lexical retrieval baselines."""
    if len(tok) > 4 and tok.endswith("ies"):
        return tok[:-3] + "y"
    if len(tok) > 3 and tok.endswith("s") and not tok.endswith(("ss", "us", "is")):
        return tok[:-1]
    return tok


def tokenize(text):
    text = re.sub(r"([a-z])([A-Z])", r"\1 \2", text)
    return [_stem(t) for t in _TOKEN.findall(text.casefold().replace("_", " "))]


def serialize(table, profile=None, max_chars=4000):
    parts = [table.get("title", ""), table.get("description", "")]
    for c in table.get("columns", [])[:120]:
        parts.append(f"{c['name']}: {c.get('description', '')}")
    if profile:
        for c in profile.get("columns", []):
            if c.get("type") == "categorical" and c.get("top_values"):
                parts.append(" ".join(v for v, _ in c["top_values"][:8]))
    return " \n".join(p for p in parts if p)[:max_chars]


def corpus_key(manifest, method, extra=""):
    ids = json.dumps([(t["table_id"], t["sha256"]) for t in manifest["tables"]])
    return hashlib.sha256(f"{ids}|{method}|{SERIALIZATION}|{extra}".encode()).hexdigest()[:20]


class BM25:
    name = "bm25"

    def __init__(self, docs, k1=1.2, b=0.75):
        self.k1, self.b = k1, b
        self.doc_len, self.postings, self.df = [], defaultdict(list), Counter()
        for i, doc in enumerate(docs):
            toks = tokenize(doc)
            self.doc_len.append(len(toks))
            for term, f in Counter(toks).items():
                self.postings[term].append((i, f))
                self.df[term] += 1
        self.n = len(docs)
        self.avg = sum(self.doc_len) / max(1, self.n)

    def scores(self, query):
        out = defaultdict(float)
        for term in set(tokenize(query)):
            df = self.df.get(term)
            if not df:
                continue
            idf = math.log(1 + (self.n - df + 0.5) / (df + 0.5))
            for i, f in self.postings[term]:
                out[i] += idf * f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * self.doc_len[i] / self.avg))
        if not out:
            return {}
        top = max(out.values())
        return {i: s / top for i, s in out.items()} if top > 0 else {}


class Vector:
    def __init__(self, docs, method="tfidf", dims=256):
        from sklearn.feature_extraction.text import TfidfVectorizer
        self.name = method
        self.vectorizer = TfidfVectorizer(tokenizer=tokenize, lowercase=False, token_pattern=None, sublinear_tf=True, min_df=1)
        matrix = self.vectorizer.fit_transform(docs)
        self.svd = None
        if method == "lsa":
            from sklearn.decomposition import TruncatedSVD
            from sklearn.preprocessing import normalize
            self.svd = TruncatedSVD(n_components=min(dims, matrix.shape[1] - 1), random_state=0)
            self.matrix = normalize(self.svd.fit_transform(matrix))
        else:
            self.matrix = matrix

    def scores(self, query):
        import numpy as np
        q = self.vectorizer.transform([query])
        if self.svd is not None:
            from sklearn.preprocessing import normalize
            q = normalize(self.svd.transform(q))
            sims = self.matrix @ q[0]
        else:
            sims = (self.matrix @ q.T).toarray().ravel()
        sims = np.clip(sims, 0, 1)
        return {int(i): float(s) for i, s in enumerate(sims) if s > 0}


class SBERT:
    name = "sbert"

    def __init__(self, docs, model="sentence-transformers/all-MiniLM-L6-v2", query_prefix=""):
        from sentence_transformers import SentenceTransformer
        self.model_name, self.query_prefix = model, query_prefix
        self.model = SentenceTransformer(model, device="cpu")
        self.matrix = self.model.encode(docs, normalize_embeddings=True, batch_size=64, show_progress_bar=False)

    def __getstate__(self):
        state = dict(self.__dict__)
        state.pop("model", None)
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        from sentence_transformers import SentenceTransformer
        self.model = SentenceTransformer(self.model_name, device="cpu")

    def scores(self, query):
        import numpy as np
        q = self.model.encode([self.query_prefix + query], normalize_embeddings=True)[0]
        sims = np.clip(self.matrix @ q, 0, 1)
        return {int(i): float(s) for i, s in enumerate(sims) if s > 0}


class Hybrid:
    def __init__(self, parts, weights):
        self.parts, self.weights, self.name = parts, weights, "hybrid"

    def scores(self, query):
        out = defaultdict(float)
        for part, w in zip(self.parts, self.weights):
            for i, s in part.scores(query).items():
                out[i] += w * s
        return dict(out)


class ContextMatcher:
    """Index over a corpus manifest; retrieve(q, k) -> [(table_id, r)] with timing."""

    def __init__(self, manifest, method="bm25", *, cache_dir=INDEX_DIR, sbert_model=None):
        self.manifest, self.method = manifest, method
        self.ids = [t["table_id"] for t in manifest["tables"]]
        start = time.perf_counter()
        extra = sbert_model or ""
        key = corpus_key(manifest, method, extra)
        path = Path(cache_dir) / f"{method}-{key}.pkl" if cache_dir else None
        self.cache_hit = False
        if path and path.exists():
            with open(path, "rb") as f:
                self.index = pickle.load(f)
            self.cache_hit = True
        else:
            docs = [serialize(t) for t in manifest["tables"]]
            self.index = self._build(method, docs, sbert_model)
            if path:
                path.parent.mkdir(parents=True, exist_ok=True)
                with open(path, "wb") as f:
                    pickle.dump(self.index, f)
        self.build_ms = round((time.perf_counter() - start) * 1000, 3)

    def _build(self, method, docs, sbert_model):
        if method == "bm25":
            return BM25(docs)
        if method in ("tfidf", "lsa"):
            return Vector(docs, method)
        if method == "sbert":
            return SBERT(docs, sbert_model or "sentence-transformers/all-MiniLM-L6-v2")
        if method == "hybrid":
            try:
                dense = SBERT(docs, sbert_model or "sentence-transformers/all-MiniLM-L6-v2")
            except ImportError:
                dense = Vector(docs, "lsa")
            return Hybrid([BM25(docs), dense], [0.5, 0.5])
        raise ValueError("UNKNOWN_CONTEXT_METHOD:" + method)

    def retrieve(self, query, k=50):
        start = time.perf_counter()
        scores = self.index.scores(query)
        ranked = sorted(((self.ids[i], round(s, 6)) for i, s in scores.items()), key=lambda x: (-x[1], x[0]))
        if len(ranked) < k:  # pad deterministically so k candidates are always returned
            seen = {t for t, _ in ranked}
            ranked += [(t, 0.0) for t in sorted(self.ids) if t not in seen][: k - len(ranked)]
        return ranked[:k], round((time.perf_counter() - start) * 1000, 3)

    def score_all(self, query):
        scores = self.index.scores(query)
        return {self.ids[i]: s for i, s in scores.items()}
