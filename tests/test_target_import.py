import json
import unittest
from pathlib import Path

from common import tmpdir

from intention_grounding import corpus, experiments
from intention_grounding.target_import import import_dataset, sql_operation

FIX = Path(__file__).parent / "fixtures" / "target"


class TargetImportTests(unittest.TestCase):
    def test_sql_operation(self):
        self.assertEqual(sql_operation("SELECT a, AVG(b) FROM t GROUP BY a"), {"sql_operation": "mean", "grouped": True})
        self.assertEqual(sql_operation("SELECT COUNT(*) FROM t")["sql_operation"], "total_or_count")
        self.assertEqual(sql_operation("SELECT name FROM t ORDER BY x DESC LIMIT 1")["sql_operation"], "extreme")

    def test_import_and_run_experiment(self):
        out = tmpdir()
        m, b = import_dataset("bird-mock", corpus_path=str(FIX / "corpus.jsonl"), queries_path=str(FIX / "queries.jsonl"),
                              out_corpus=out / "corpus", out_bench=out / "bench.json")
        self.assertEqual(m["table_count"], 4)
        self.assertEqual(len(b["queries"]), 4)
        self.assertEqual(b["queries"][0]["labels"], {"school/students": 2})
        self.assertEqual(b["queries"][0]["sql_operation"], "mean")
        manifest = corpus.load_manifest(out / "corpus" / "manifest.json")
        self.assertTrue(Path(manifest["tables"][0]["abs_path"]).exists())
        experiments.main(["--corpus", str(out / "corpus" / "manifest.json"), "--benchmark", str(out / "bench.json"),
                          "--systems", "target", "--context", "bm25", "--out", str(out / "results")])
        run = next((out / "results").iterdir())
        summary = json.loads((run / "summary.json").read_text())
        names = [s["system"] for s in summary["systems"]]
        self.assertEqual(names, ["ctx:bm25", "ig:rule/index:bm25"])
        self.assertIn("by_operation", summary["systems"][1])
        self.assertIn("R@5", (run / "results.md").read_text())


if __name__ == "__main__":
    unittest.main()
