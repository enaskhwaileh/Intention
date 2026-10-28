import json
import unittest

from common import fig1_manifest

from intention_grounding import il
from intention_grounding.context import ContextMatcher
from intention_grounding.grounder import IndexResolver
from intention_grounding.interpreter import RuleInterpreter
from intention_grounding.llm import ChatClient
from intention_grounding.pipeline import Pipeline
from intention_grounding.rerank import LLMReranker


class Fake(ChatClient):
    def __init__(self):
        super().__init__(model="fake", cache_dir=None, api_key="x")

    def complete_json(self, messages, *, prompt_version):
        cands = json.loads(messages[-1]["content"])["candidates"]
        # prefer the last candidate, to show the reranker reorders
        return json.dumps({"scores": {c["id"]: (3 if i == len(cands) - 1 else 0) for i, c in enumerate(cands)}}), {"cache_hit": False}


class BaselineTests(unittest.TestCase):
    def test_llm_reranker_reorders_head(self):
        m = fig1_manifest()
        matcher = ContextMatcher(m, "bm25", cache_dir=None)
        rr = LLMReranker(m, matcher, k=3, client=Fake())
        base = [t for t, _ in matcher.retrieve("vaccination rate by country", 3)[0]]
        out = rr.rank("vaccination rate by country")
        self.assertEqual(out["ranking"][0]["table_id"], base[-1])
        self.assertEqual(out["status"], "ok")

    def test_query_rewrite_control_never_aligns(self):
        m, lib = fig1_manifest(), il.load()
        p = Pipeline(m, library=lib, interpreter=RuleInterpreter(), resolver=IndexResolver(lib),
                     matcher=ContextMatcher(m, "bm25", cache_dir=None), align=False)
        rep = p.run("Compare the average vaccination rate across countries")
        self.assertEqual(rep["grounding"]["status"], "disabled")
        self.assertTrue(all(x["A"] is None for x in rep["ranking"]))


if __name__ == "__main__":
    unittest.main()


class CombinedTests(unittest.TestCase):
    def test_ig_llm_reranker_passes_verdicts(self):
        from intention_grounding.rerank import IGLLMReranker
        m, lib = fig1_manifest(), il.load()
        seen = {}

        class Spy(Fake):
            def complete_json(self, messages, *, prompt_version):
                seen["cands"] = json.loads(messages[-1]["content"])["candidates"]
                return super().complete_json(messages, prompt_version=prompt_version)

        p = Pipeline(m, library=lib, interpreter=RuleInterpreter(), resolver=IndexResolver(lib),
                     matcher=ContextMatcher(m, "bm25", cache_dir=None))
        out = IGLLMReranker(m, p, k=3, client=Spy()).rank("Compare the average vaccination rate across countries")
        self.assertEqual(out["status"], "ok")
        self.assertTrue(any("framework_check" in c for c in seen["cands"]))
        chk = next(c["framework_check"] for c in seen["cands"] if "framework_check" in c)
        self.assertIn(chk["overall"], ("supported", "violated", "unresolved"))
