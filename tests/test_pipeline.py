import copy
import importlib.resources
import json
from pathlib import Path
import tempfile
import unittest

from intention_grounding.action_base import ActionBaseError, load_action_base, validate_action_base
from intention_grounding.aligner import compare_card
from intention_grounding.cli import main
from intention_grounding.grounder import ReplayGrounderProvider, ground
from intention_grounding.interpreter.core import interpret
from intention_grounding.interpreter.providers import ReplayProvider
from intention_grounding.profiler import profile_table


class PipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fixtures = json.loads(importlib.resources.files("intention_grounding.interpreter").joinpath("fixtures/replay.json").read_text())
        cls.case = fixtures[2]
        cls.interpreted = interpret(cls.case["input_id"], cls.case["input"], ReplayProvider(cls.case["raw_response"]))
        cls.ab = load_action_base()
        doc = cls.interpreted["interpretation"]
        cls.proposal = {"ab_version": cls.ab["ab_version"], "input_id": doc["input_id"],
                        "action_id": "compare.time", "bindings": {}, "evidence": []}
        for index, argument in enumerate(doc["actions"][0]["arguments"]):
            cls.proposal["bindings"].setdefault(argument["role"], []).append({"action_id": "a1", "argument_index": index})
            cls.proposal["evidence"].extend(argument["value"]["evidence"])
        cls.proposal["evidence"] = list(dict.fromkeys(cls.proposal["evidence"]))

    def run_proposal(self, proposal):
        return ground(self.interpreted, self.ab, ReplayGrounderProvider(json.dumps(proposal)), run_id="test-run")

    def test_valid_grounding_and_inheritance(self):
        result = self.run_proposal(self.proposal)
        self.assertEqual("grounded", result["status"])
        card = result["grounded_card"]
        self.assertEqual("0.1.0-draft", card["ab_version"])
        self.assertEqual("compare", card["selected_parent_action_id"])
        self.assertEqual("compare.time", card["selected_child_action_id"])
        self.assertEqual({"measure_semantics", "observation_binding", "usable_numeric_observations",
                          "comparable_measure_definition", "time_coverage"},
                         {r["id"] for r in card["requirements"]})
        self.assertTrue(card["deterministic_validation"]["valid"])

    def test_unknown_wrong_action_and_version(self):
        for field, value, reason in [("action_id", "COMPARE", "UNKNOWN_ACTION_ID"),
                                     ("ab_version", "9", "AB_VERSION_MISMATCH")]:
            proposal = copy.deepcopy(self.proposal); proposal[field] = value
            result = self.run_proposal(proposal)
            self.assertEqual("invalid_model_response", result["status"])
            self.assertIn(reason, result["reasons"][0])

    def test_malformed_missing_arguments_and_evidence(self):
        malformed = ground(self.interpreted, self.ab, ReplayGrounderProvider("{"), run_id="x")
        self.assertEqual("invalid_model_response", malformed["status"])
        for mutate in [lambda p: p["bindings"].pop("measure"), lambda p: p.update(evidence=[])]:
            proposal = copy.deepcopy(self.proposal); mutate(proposal)
            self.assertEqual("invalid_model_response", self.run_proposal(proposal)["status"])

    def test_non_grounded_interpreter_states_and_provider_error(self):
        fixtures = json.loads(importlib.resources.files("intention_grounding.interpreter").joinpath("fixtures/replay.json").read_text())
        for index, expected in [(6, "ambiguous"), (3, "insufficient_input"), (7, "unsupported")]:
            case = fixtures[index]
            envelope = interpret(case["input_id"], case["input"], ReplayProvider(case["raw_response"]))
            self.assertEqual(expected, ground(envelope, self.ab, ReplayGrounderProvider("{}"), run_id="x")["status"])
        class Broken:
            metadata = {"provider": "broken"}
            def invoke(self, *_): raise RuntimeError("secret")
        result = ground(self.interpreted, self.ab, Broken(), run_id="x")
        self.assertEqual("provider_failure", result["status"])
        self.assertNotIn("secret", json.dumps(result))

    def test_action_base_validation(self):
        ab = copy.deepcopy(self.ab); ab["actions"]["compare.time"]["parent"] = "missing"
        with self.assertRaises(ActionBaseError): validate_action_base(ab)
        with self.assertRaises(ActionBaseError): load_action_base(expected_version="9")

    def test_profile_and_unknown_alignment(self):
        path = Path(importlib.resources.files("intention_grounding").joinpath("fixtures/offline_table.csv"))
        profile = profile_table(path)
        self.assertEqual(4, profile["row_count"])
        self.assertTrue(all(column["evidence_ref"] for column in profile["columns"]))
        card = self.run_proposal(self.proposal)["grounded_card"]
        compared = compare_card(card, [profile])
        self.assertTrue(all(r["state"] == "unknown" for r in compared["tables"][0]["requirements"]))
        broken = copy.deepcopy(profile); broken["evidence"] = []
        compared = compare_card(card, [broken])
        self.assertTrue(all(r["reason"] == "PROFILE_MISSING_EVIDENCE" for r in compared["tables"][0]["requirements"]))

    def test_offline_cli_integration(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(0, main(["--output", directory]))
            runs = list(Path(directory).iterdir())
            self.assertEqual(1, len(runs))
            self.assertEqual({"run.json", "interpreter.raw.txt", "interpretation.json", "grounder.raw.txt",
                              "grounding.json", "table-profiles.json", "comparison.json"},
                             {path.name for path in runs[0].iterdir()})


if __name__ == "__main__":
    unittest.main()
