"""Context matching: r(q_u, T) in [0, 1] and top-k candidate retrieval.

Each table is serialised from its documentation and schema (title, description,
attribute names and descriptions, a few categorical values). Methods:
  bm25        lexical BM25 (Robertson/Sparck Jones), r = score / max score for q
  tfidf       TF-IDF cosine (scikit-learn)
  lsa         latent semantic analysis (TF-IDF + truncated SVD) cosine
  sbert       Sentence-BERT embeddings of tables (chunked) and queries, stored in a vector
              database (ChromaDB by default; FAISS or exact numpy); r = max chunk cosine
  hybrid      0.5 * bm25 + 0.5 * sbert
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


def table_chunks(table, columns_per_chunk=12, max_chunks=25, desc_chars=600, col_desc_chars=140):
    """Passages for dense embedding: one for title + description, then groups of attributes
    (name and documentation), each prefixed by the table title so every chunk carries its context.
    Chunking keeps wide tables within the encoder's token limit."""
    title = table.get("title", "") or table["table_id"]
    chunks = [f"{title}. {(table.get('description') or '')[:desc_chars]}".strip()]
    cols = [c for c in table.get("columns", []) if c["name"].casefold() != "rownames"]
    for s in range(0, len(cols), columns_per_chunk):
        group = cols[s:s + columns_per_chunk]
        body = "; ".join(f"{c['name']}" + (f" ({c['description'][:col_desc_chars]})" if c.get("description") else "") for c in group)
        chunks.append(f"{title}. Columns: {body}")
        if len(chunks) >= max_chunks:
            break
    return chunks


TABERTA_ROWS = 10
TABERTA_DEFAULT_MODEL = "/datastore-beast/servers/Enas/enas/tabert/TABERTA_OWL/models/PC_pairwise_contrastive"


def taberta_chunks(table, rows=TABERTA_ROWS, view=None):
    """TABERTA's table serializations (paper Section 3.1), one passage per table, first 10 rows:
      full   [DB]<db> [TABLE]<t> [SCHEMA]<c1>,<c2>,... [ROWS]<r1 values>|<r2 values>|...
      row    [TABLE]<t> [ROWS][ROW] c1:v11 | c2:v12 [ROW] c1:v21 | ...      (PC model)
      schema [TABLE]<t> [SCHEMA]<c1>,<c2>,...
    The encoder truncates at its token limit (256). IG_TABERTA_VIEW selects the view (default full)."""
    import csv as _csv
    import os
    view = view or os.environ.get("IG_TABERTA_VIEW", "full")
    src = table.get("source") or {}
    db = src.get("database_id") or table.get("source_family") or ""
    name = src.get("table_id") or table.get("title") or table["table_id"]
    cols = [c["name"] for c in table.get("columns", [])]
    body = []
    path = table.get("abs_path") or table.get("path")
    if path and view != "schema":
        try:
            with open(path, newline="", encoding="utf-8", errors="replace") as f:
                reader = _csv.reader(f)
                header = next(reader, [])
                cols = cols or header
                for n, row in enumerate(reader):
                    if n >= rows:
                        break
                    body.append(row)
        except OSError:
            pass
    if view == "schema":
        return [f"[TABLE]{name} [SCHEMA]{','.join(cols)}"]
    if view == "row":
        return [f"[TABLE]{name} [ROWS]" + " ".join("[ROW] " + " | ".join(f"{c}:{v}" for c, v in zip(cols, r)) for r in body)]
    return [f"[DB]{db} [TABLE]{name} [SCHEMA]{','.join(cols)} [ROWS]{'|'.join(','.join(r) for r in body) or 'N/A'}"]


class DenseIndex:
    """Dense context matching: tables embedded with an encoder and stored in a vector database.

    Each table contributes several chunk vectors (see table_chunks); the table score is the
    maximum cosine similarity of its chunks to the query embedding, clipped to [0, 1].
    The store is synchronised incrementally: only new or changed chunks are embedded."""
    name = "sbert"
    CHUNKING = "title-description+column-groups-12-v1"

    def __init__(self, manifest, ids, encoder, backend="chroma", root=None, batch=256, chunker=None, chunking=None):
        from . import vectorstore
        self.ids, self.encoder = ids, encoder
        self.chunker = chunker or table_chunks
        self.CHUNKING = chunking or self.CHUNKING
        self.pos = {t: i for i, t in enumerate(ids)}
        ident = encoder.identity
        slug = re.sub(r"[^A-Za-z0-9]+", "-", ident["model"]).strip("-")[-30:]
        key = hashlib.sha256(json.dumps([manifest.get("corpus_id"), ident, self.CHUNKING], sort_keys=True).encode()).hexdigest()[:10]
        self.collection = f"ig-{slug}-{key}"
        self.store = vectorstore.open_store(backend, self.collection, **({"root": root} if root else {}))
        self.backend = backend
        self.stats = self._sync(manifest, batch)

    def _sync(self, manifest, batch):
        start = time.perf_counter()
        wanted = {}
        for t in manifest["tables"]:
            for n, text in enumerate(self.chunker(t)):
                h = hashlib.sha256(text.encode()).hexdigest()[:16]
                wanted[f"{t['table_id']}::{n}"] = (t["table_id"], text, h)
        existing = self.store.metadata()
        stale = [i for i in existing if i not in wanted]
        todo = [i for i, (_, _, h) in wanted.items() if existing.get(i, {}).get("hash") != h]
        if stale:
            self.store.delete(stale)
        embed_ms = 0.0
        for s in range(0, len(todo), batch):
            part = todo[s:s + batch]
            t0 = time.perf_counter()
            vectors = self.encoder.encode([wanted[i][1] for i in part], kind="passage")
            embed_ms += (time.perf_counter() - t0) * 1000
            self.store.upsert(part, vectors, [{"table_id": wanted[i][0], "hash": wanted[i][2]} for i in part])
        return {"chunks": len(wanted), "embedded": len(todo), "reused": len(wanted) - len(todo), "deleted": len(stale),
                "embed_ms": round(embed_ms, 3), "sync_ms": round((time.perf_counter() - start) * 1000, 3),
                "backend": self.backend, "collection": self.collection, **self.encoder.identity}

    def scores(self, query, n_chunks=None):
        t0 = time.perf_counter()
        vector = self.encoder.encode([query], kind="query")[0]
        t1 = time.perf_counter()
        hits = self.store.query(vector, n_chunks or 2000)
        t2 = time.perf_counter()
        self.last_timing = {"embed_query_ms": round((t1 - t0) * 1000, 3), "vector_search_ms": round((t2 - t1) * 1000, 3)}
        out = {}
        for _, sim, meta in hits:
            i = self.pos.get(meta["table_id"])
            if i is not None and sim > out.get(i, 0.0):
                out[i] = min(1.0, sim)
        return {i: s for i, s in out.items() if s > 0}


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
    """Index over a corpus manifest; retrieve(q, k) -> [(table_id, r)] with timing.

    Dense methods (sbert, hybrid) keep their table embeddings in a vector database
    (`vector_store`: chroma | faiss | numpy) instead of the pickle cache."""

    def __init__(self, manifest, method="bm25", *, cache_dir=INDEX_DIR, sbert_model=None, vector_store="chroma",
                 encoder=None, vector_root=None):
        self.manifest, self.method = manifest, method
        self.ids = [t["table_id"] for t in manifest["tables"]]
        self.last_timing = {}
        self.dense_stats = None
        start = time.perf_counter()
        self.cache_hit = False
        if method == "taberta":  # TABERTA (structure-aware table embeddings; default: PC model, IG_TABERTA_MODEL overrides)
            import os
            if encoder is None:
                from .embedding import SBERTEncoder
                encoder = SBERTEncoder(os.environ.get("IG_TABERTA_MODEL", TABERTA_DEFAULT_MODEL))
            dense = DenseIndex(manifest, self.ids, encoder, backend=vector_store, root=vector_root,
                               chunker=taberta_chunks, chunking=f"taberta-{os.environ.get('IG_TABERTA_VIEW', 'full')}-rows{TABERTA_ROWS}-v2")
            self.dense_stats = dense.stats
            self.cache_hit = dense.stats["embedded"] == 0
            self.index = dense
        elif method in ("sbert", "hybrid"):
            if encoder is None:
                from .embedding import DEFAULT_MODEL, SBERTEncoder
                encoder = SBERTEncoder(sbert_model or DEFAULT_MODEL)
            dense = DenseIndex(manifest, self.ids, encoder, backend=vector_store, root=vector_root)
            self.dense_stats = dense.stats
            self.cache_hit = dense.stats["embedded"] == 0
            if method == "sbert":
                self.index = dense
            else:
                lexical = ContextMatcher(manifest, "bm25", cache_dir=cache_dir).index
                self.index = Hybrid([lexical, dense], [0.5, 0.5])
        else:
            key = corpus_key(manifest, method)
            path = Path(cache_dir) / f"{method}-{key}.pkl" if cache_dir else None
            if path and path.exists():
                with open(path, "rb") as f:
                    self.index = pickle.load(f)
                self.cache_hit = True
            else:
                docs = [serialize(t) for t in manifest["tables"]]
                self.index = BM25(docs) if method == "bm25" else Vector(docs, method) if method in ("tfidf", "lsa") else None
                if self.index is None:
                    raise ValueError("UNKNOWN_CONTEXT_METHOD:" + method)
                if path:
                    path.parent.mkdir(parents=True, exist_ok=True)
                    with open(path, "wb") as f:
                        pickle.dump(self.index, f)
        self.build_ms = round((time.perf_counter() - start) * 1000, 3)

    def _dense_timing(self):
        parts = self.index.parts if isinstance(self.index, Hybrid) else [self.index]
        return next((p.last_timing for p in parts if hasattr(p, "last_timing")), {})

    def retrieve(self, query, k=50):
        start = time.perf_counter()
        scores = self.index.scores(query)
        ranked = sorted(((self.ids[i], round(s, 6)) for i, s in scores.items()), key=lambda x: (-x[1], x[0]))
        if len(ranked) < k:  # pad deterministically so k candidates are always returned
            seen = {t for t, _ in ranked}
            ranked += [(t, 0.0) for t in sorted(self.ids) if t not in seen][: k - len(ranked)]
        self.last_timing = self._dense_timing()
        return ranked[:k], round((time.perf_counter() - start) * 1000, 3)

    def score_all(self, query):
        scores = self.index.scores(query)
        return {self.ids[i]: s for i, s in scores.items()}
