"""Persistent vector stores for table embeddings.

All stores hold unit-length vectors with string ids and metadata, support
incremental upsert/delete, and return cosine similarity for a query vector.

  chroma   ChromaDB persistent collection (HNSW, cosine space)  - pip install chromadb
  faiss    FAISS exact inner-product index over stored vectors  - pip install faiss-cpu
  numpy    exact search with numpy (no extra dependency)

Data lives under data/runtime/vectordb/<backend>/<collection>.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VECTOR_DIR = ROOT / "data" / "runtime" / "vectordb"


class NumpyStore:
    backend = "numpy"

    def __init__(self, collection, root=VECTOR_DIR):
        import numpy as np
        self.np = np
        self.dir = Path(root) / self.backend / collection
        self.dir.mkdir(parents=True, exist_ok=True)
        self.ids, self.meta, self.vectors = [], {}, None
        if (self.dir / "ids.json").exists():
            self.ids = json.loads((self.dir / "ids.json").read_text())
            self.meta = json.loads((self.dir / "meta.json").read_text())
            self.vectors = np.load(self.dir / "vectors.npy")
        self._rebuild()

    def _rebuild(self):
        self.pos = {i: n for n, i in enumerate(self.ids)}

    def _save(self):
        self.np.save(self.dir / "vectors.npy", self.vectors if self.vectors is not None else self.np.zeros((0, 1), "float32"))
        (self.dir / "ids.json").write_text(json.dumps(self.ids))
        (self.dir / "meta.json").write_text(json.dumps(self.meta))

    def count(self):
        return len(self.ids)

    def metadata(self):
        return dict(self.meta)

    def upsert(self, ids, vectors, metadatas):
        np = self.np
        vectors = np.asarray(vectors, dtype="float32")
        new_rows = []
        for i, v, m in zip(ids, vectors, metadatas):
            if i in self.pos:
                self.vectors[self.pos[i]] = v
            else:
                self.ids.append(i)
                new_rows.append(v)
            self.meta[i] = m
        if new_rows:
            stacked = np.vstack(new_rows)
            self.vectors = stacked if self.vectors is None or self.vectors.size == 0 else np.vstack([self.vectors, stacked])
        self._rebuild()
        self._after_change()
        self._save()

    def delete(self, ids):
        drop = set(ids)
        if not drop:
            return
        keep = [n for n, i in enumerate(self.ids) if i not in drop]
        self.vectors = self.vectors[keep] if self.vectors is not None else None
        self.ids = [self.ids[n] for n in keep]
        for i in drop:
            self.meta.pop(i, None)
        self._rebuild()
        self._after_change()
        self._save()

    def _after_change(self):
        pass

    def query(self, vector, n):
        np = self.np
        if not self.ids:
            return []
        sims = self.vectors @ np.asarray(vector, dtype="float32")
        n = min(n, len(self.ids))
        top = np.argpartition(-sims, n - 1)[:n]
        top = top[np.argsort(-sims[top], kind="stable")]
        return [(self.ids[t], float(sims[t]), self.meta[self.ids[t]]) for t in top]


class FaissStore(NumpyStore):
    backend = "faiss"

    def _after_change(self):
        import faiss
        self.index = faiss.IndexFlatIP(self.vectors.shape[1]) if self.vectors is not None and len(self.vectors) else None
        if self.index is not None:
            self.index.add(self.vectors)

    def __init__(self, collection, root=VECTOR_DIR):
        super().__init__(collection, root)
        self._after_change()

    def query(self, vector, n):
        if not self.ids or self.index is None:
            return []
        scores, idx = self.index.search(self.np.asarray([vector], dtype="float32"), min(n, len(self.ids)))
        return [(self.ids[i], float(s), self.meta[self.ids[i]]) for s, i in zip(scores[0], idx[0]) if i >= 0]


class ChromaStore:
    backend = "chroma"
    BATCH = 4000

    def __init__(self, collection, root=VECTOR_DIR):
        import chromadb
        path = Path(root) / self.backend
        path.mkdir(parents=True, exist_ok=True)
        self.client = chromadb.PersistentClient(path=str(path))
        self.col = self.client.get_or_create_collection(name=collection, metadata={"hnsw:space": "cosine"})

    def count(self):
        return self.col.count()

    def metadata(self):
        out, offset = {}, 0
        while True:
            page = self.col.get(include=["metadatas"], limit=self.BATCH, offset=offset)
            for i, m in zip(page["ids"], page["metadatas"]):
                out[i] = m
            if len(page["ids"]) < self.BATCH:
                return out
            offset += self.BATCH

    def upsert(self, ids, vectors, metadatas):
        vectors = [list(map(float, v)) for v in vectors]
        for s in range(0, len(ids), self.BATCH):
            self.col.upsert(ids=ids[s:s + self.BATCH], embeddings=vectors[s:s + self.BATCH], metadatas=metadatas[s:s + self.BATCH])

    def delete(self, ids):
        ids = list(ids)
        for s in range(0, len(ids), self.BATCH):
            self.col.delete(ids=ids[s:s + self.BATCH])

    def query(self, vector, n):
        n = min(n, self.count())
        if not n:
            return []
        res = self.col.query(query_embeddings=[list(map(float, vector))], n_results=n, include=["distances", "metadatas"])
        return [(i, 1.0 - float(d), m) for i, d, m in zip(res["ids"][0], res["distances"][0], res["metadatas"][0])]


BACKENDS = {"chroma": ChromaStore, "faiss": FaissStore, "numpy": NumpyStore}


def open_store(backend, collection, root=VECTOR_DIR):
    if backend not in BACKENDS:
        raise ValueError("UNKNOWN_VECTOR_STORE:" + backend)
    return BACKENDS[backend](collection, root)
