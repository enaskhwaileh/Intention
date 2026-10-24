import unittest

from common import fig1_manifest, tmpdir

from intention_grounding.context import ContextMatcher, table_chunks
from intention_grounding.embedding import HashEncoder
from intention_grounding.vectorstore import NumpyStore

M = fig1_manifest()


class DenseContextTests(unittest.TestCase):
    def test_chunks_carry_title_and_cover_all_columns(self):
        t = M["tables"][2]
        chunks = table_chunks(t, columns_per_chunk=3)
        self.assertTrue(all(c.startswith(t["title"]) for c in chunks))
        self.assertEqual(len(chunks), 1 + 3)  # 8 columns in groups of 3

    def test_vector_store_retrieval_and_incremental_sync(self):
        root = tmpdir()
        m = ContextMatcher(M, "sbert", encoder=HashEncoder(), vector_store="numpy", vector_root=root)
        self.assertEqual(m.dense_stats["embedded"], m.dense_stats["chunks"])
        ranked, _ = m.retrieve("patient records with observed side effect and severity score", k=4)
        self.assertEqual(ranked[0][0], "fig1.patient_records")
        self.assertTrue(0 < ranked[0][1] <= 1)
        self.assertIn("embed_query_ms", m.last_timing)
        again = ContextMatcher(M, "sbert", encoder=HashEncoder(), vector_store="numpy", vector_root=root)
        self.assertEqual(again.dense_stats["embedded"], 0)  # nothing re-embedded
        changed = {**M, "tables": [dict(M["tables"][0], title="Changed title")] + M["tables"][1:]}
        third = ContextMatcher(changed, "sbert", encoder=HashEncoder(), vector_store="numpy", vector_root=root)
        self.assertGreater(third.dense_stats["embedded"], 0)
        self.assertLess(third.dense_stats["embedded"], third.dense_stats["chunks"])

    def test_hybrid_combines_lexical_and_dense(self):
        m = ContextMatcher(M, "hybrid", encoder=HashEncoder(), vector_store="numpy", vector_root=tmpdir(), cache_dir=None)
        ranked, _ = m.retrieve("vaccine shipments and storage temperature", k=4)
        self.assertEqual(ranked[0][0], "fig1.vaccine_logistics")

    def test_numpy_store_delete(self):
        s = NumpyStore("t", tmpdir())
        s.upsert(["a", "b"], [[1, 0], [0, 1]], [{"table_id": "A"}, {"table_id": "B"}])
        s.delete(["a"])
        self.assertEqual([h[0] for h in s.query([1, 0], 5)], ["b"])

    @unittest.skipUnless(__import__("importlib").util.find_spec("chromadb"), "chromadb not installed")
    def test_chroma_backend(self):
        m = ContextMatcher(M, "sbert", encoder=HashEncoder(), vector_store="chroma", vector_root=tmpdir())
        ranked, _ = m.retrieve("country side effect rates", k=4)
        self.assertEqual(len(ranked), 4)


if __name__ == "__main__":
    unittest.main()
