import json
import unittest

from common import tmpdir

from intention_grounding import il
from intention_grounding.experiments import query_metrics, swap_accuracy, entry_f1
from intention_grounding.grounder import LLMResolver, ground
from intention_grounding.interpreter import LLMInterpreter, interpret
from intention_grounding.llm import ChatClient, LLMUnavailable, parse_json_object

L = il.load()


class FakeClient(ChatClient):
    """Returns canned JSON for each prompt version; no network."""
    def __init__(self, responses, **kw):
        super().__init__(model="fake-model", cache_dir=tmpdir(), api_key="x", **kw)
        self.responses = responses

    def complete_json(self, messages, *, prompt_version):
        rec = {"cache_hit": False, "model": self.model, "usage": {"total_tokens": 10}, "latency_ms": 1.0}
        self.calls.append(rec)
        return json.dumps(self.responses[prompt_version]), rec


class LLMPathTests(unittest.TestCase):
    def test_llm_interpreter_and_resolver_contracts(self):
        u = "Predict whether a passenger survived from class and age"
        z = {"context_query": "passenger survival, class and age", "intention_expression": "Predict",
             "arguments": [{"id": "a1", "label": "target", "value": "survived", "spans": ["survived"]},
                           {"id": "a2", "label": "predictor", "value": "class", "spans": ["class"]},
                           {"id": "a3", "label": "predictor", "value": "age", "spans": ["age"]}], "scope": []}
        p = {"status": "proposed", "variant_id": "predict.classification", "bindings": {"target": ["a1"], "predictor": ["a2", "a3"]},
             "scope": [], "justification": "whether -> classification", "diagnostics": []}
        from intention_grounding.grounder import PROMPT_VERSION as GV
        from intention_grounding.interpreter.providers import PROMPT_VERSION as IV
        client = FakeClient({IV: z, GV: p})
        r = interpret(u, LLMInterpreter(client=client), L["vocabulary"]).to_dict()
        self.assertEqual(r["status"], "extracted")
        self.assertEqual(r["provider"]["model"], "fake-model")
        g = ground(r, L, LLMResolver(client=client))
        self.assertEqual((g["status"], g["g_u"]["variant_id"]), ("grounded", "predict.classification"))

    def test_validator_guided_repair(self):
        from intention_grounding.interpreter.providers import PROMPT_VERSION as IV
        u = "Predict whether a passenger survived"
        bad = {"context_query": "passenger survival", "intention_expression": "Predict ... survived",
               "arguments": [{"id": "a1", "label": "target", "value": "survived", "spans": ["survived"]}], "scope": []}
        good = dict(bad, intention_expression="Predict")

        class Seq(FakeClient):
            def complete_json(self, messages, *, prompt_version):
                rec = {"cache_hit": False, "model": "fake", "usage": None, "latency_ms": 1.0}
                return json.dumps(good if len(messages) > 2 else bad), rec
        self.assertEqual(interpret(u, LLMInterpreter(client=Seq({})), L["vocabulary"]).to_dict()["status"], "failure")
        r = interpret(u, LLMInterpreter(client=Seq({}), max_repairs=1), L["vocabulary"]).to_dict()
        self.assertEqual((r["status"], r["provider"]["repairs"]), ("extracted", 1))

    def test_messages_never_contain_tables(self):
        msgs = LLMInterpreter(client=FakeClient({})).messages("Compare wages", L["vocabulary"])
        self.assertNotIn("table_id", json.dumps(msgs))

    def test_cache_replay_and_live_guard(self):
        cache = tmpdir()
        client = ChatClient(model="m", cache_dir=cache, allow_live=False, api_key="")
        msgs = [{"role": "user", "content": "hi"}]
        with self.assertRaises(LLMUnavailable):
            client.complete_json(msgs, prompt_version="v")
        (cache / f"{client.key(msgs, 'v')}.json").write_text(json.dumps({"content": "{\"a\": 1}", "model": "m"}))
        raw, rec = client.complete_json(msgs, prompt_version="v")
        self.assertEqual(json.loads(raw), {"a": 1})
        self.assertTrue(rec["cache_hit"])

    def test_strict_json(self):
        with self.assertRaises(ValueError):
            parse_json_object('{"a": 1, "a": 2}')
        with self.assertRaises(ValueError):
            parse_json_object("[1]")
        self.assertEqual(parse_json_object('```json\n{"a": 1}\n```'), {"a": 1})


class MetricTests(unittest.TestCase):
    def test_hand_checked_metrics(self):
        labels = {"A": 2, "B": 1, "C": 2}
        m = query_metrics(["B", "A", "X", "C"], labels)
        self.assertAlmostEqual(m["mrr"], 0.5)
        self.assertAlmostEqual(m["p@5"], 0.4)
        self.assertAlmostEqual(m["r@10"], 1.0)
        self.assertEqual(m["useful@1"], 0.0)
        self.assertEqual(m["topical_only@1"], 1.0)
        ideal = query_metrics(["A", "C", "B"], labels)
        self.assertAlmostEqual(ideal["ndcg@10"], 1.0)

    def test_swap_accuracy(self):
        qs = [{"query_id": "q1", "pair_group": "t", "gold_grounding_status": "grounded", "labels": {"A": 2, "B": 0}},
              {"query_id": "q2", "pair_group": "t", "gold_grounding_status": "grounded", "labels": {"B": 2, "A": 1}}]
        perfect, _ = swap_accuracy({"q1": ["A", "B"], "q2": ["B", "A"]}, qs)
        indifferent, _ = swap_accuracy({"q1": ["A", "B"], "q2": ["A", "B"]}, qs)
        self.assertEqual(perfect, 1.0)
        self.assertEqual(indifferent, 0.5)

    def test_entry_f1(self):
        gold = [{"label": "measure", "value": "hourly wage"}]
        self.assertEqual(entry_f1([{"label": "measure", "value": "hourly wages"}], gold), 1.0)
        self.assertEqual(entry_f1([{"label": "target", "value": "hourly wage"}], gold), 0.0)


if __name__ == "__main__":
    unittest.main()
