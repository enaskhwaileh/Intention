import copy
import importlib.resources
import json
from pathlib import Path
import tempfile
import unittest
import contextlib
import io
import os
from unittest.mock import patch

from intention_grounding.intention_library import IntentionLibraryError, load_intention_library, validate_intention_library
from intention_grounding.aligner import compare_card
from intention_grounding.cli import main
from intention_grounding.grounder import GroqGrounderProvider, ReplayGrounderProvider, ground
from intention_grounding.interpreter.core import interpret
from intention_grounding.interpreter.providers import ReplayProvider
from intention_grounding.profiler import profile_table


class PipelineTests(unittest.TestCase):
    def setUp(self):
        env_dir = tempfile.TemporaryDirectory()
        self.addCleanup(env_dir.cleanup)
        env_patch = patch('intention_grounding.groq_config.ENV_PATH', Path(env_dir.name) / '.env')
        env_patch.start()
        self.addCleanup(env_patch.stop)

    @classmethod
    def setUpClass(cls):
        fixtures = json.loads(importlib.resources.files("intention_grounding.interpreter").joinpath("fixtures/replay.json").read_text())
        cls.case = fixtures[2]
        cls.interpreted = interpret(cls.case["input_id"], cls.case["input"], ReplayProvider(cls.case["raw_response"]))
        cls.il = load_intention_library()
        doc = cls.interpreted["interpretation"]
        cls.proposal = {"il_version": cls.il["il_version"], "input_id": doc["input_id"],
                        "intention_id": "compare.time", "bindings": {}, "evidence": []}
        for index, argument in enumerate(doc["intentions"][0]["arguments"]):
            cls.proposal["bindings"].setdefault(argument["role"], []).append({"intention_instance_id": "a1", "argument_index": index})
            cls.proposal["evidence"].extend(argument["value"]["evidence"])
        cls.proposal["evidence"] = list(dict.fromkeys(cls.proposal["evidence"]))

    def run_proposal(self, proposal):
        return ground(self.interpreted, self.il, ReplayGrounderProvider(json.dumps(proposal)), run_id="test-run")

    def test_valid_grounding_and_inheritance(self):
        result = self.run_proposal(self.proposal)
        self.assertEqual("grounded", result["status"])
        card = result["grounded_intention"]
        self.assertEqual(self.il["il_version"], card["il_version"])
        self.assertEqual("compare", card["parent_intention_id"])
        self.assertEqual("compare.time", card["intention_id"])
        self.assertEqual({"measure_semantics", "observation_binding", "usable_numeric_observations",
                          "comparable_measure_definition", "time_coverage"},
                         {r["id"] for r in card["requirements"]})
        self.assertTrue(card["deterministic_validation"]["valid"])

    def test_unknown_wrong_intention_and_version(self):
        for field, value, reason in [("intention_id", "COMPARE", "UNKNOWN_INTENTION_ID"),
                                     ("il_version", "9", "IL_VERSION_MISMATCH")]:
            proposal = copy.deepcopy(self.proposal); proposal[field] = value
            result = self.run_proposal(proposal)
            self.assertEqual("invalid_model_response", result["status"])
            self.assertIn(reason, result["reasons"][0])

    def test_malformed_missing_arguments_and_evidence(self):
        malformed = ground(self.interpreted, self.il, ReplayGrounderProvider("{"), run_id="x")
        self.assertEqual("invalid_model_response", malformed["status"])
        for mutate in [lambda p: p["bindings"].pop("measure"), lambda p: p.update(evidence=[])]:
            proposal = copy.deepcopy(self.proposal); mutate(proposal)
            self.assertEqual("invalid_model_response", self.run_proposal(proposal)["status"])

    def test_non_grounded_interpreter_states_and_provider_error(self):
        fixtures = json.loads(importlib.resources.files("intention_grounding.interpreter").joinpath("fixtures/replay.json").read_text())
        for index, expected in [(6, "ambiguous"), (3, "insufficient_input"), (7, "unsupported")]:
            case = fixtures[index]
            envelope = interpret(case["input_id"], case["input"], ReplayProvider(case["raw_response"]))
            self.assertEqual(expected, ground(envelope, self.il, ReplayGrounderProvider("{}"), run_id="x")["status"])
        class Broken:
            metadata = {"provider": "broken"}
            def invoke(self, *_): raise RuntimeError("secret")
        result = ground(self.interpreted, self.il, Broken(), run_id="x")
        self.assertEqual("provider_failure", result["status"])
        self.assertNotIn("secret", json.dumps(result))
        self.assertEqual({"exception_type": "RuntimeError"}, result["provider_error"])

    def test_grounder_provider_status_is_sanitized(self):
        with self.assertRaisesRegex(RuntimeError, "GROQ_MODEL_ID"):
            GroqGrounderProvider(model="")
        class FailingProvider:
            metadata = {"provider": "mock"}
            def invoke(self, *_):
                error = RuntimeError("secret-value in request headers")
                error.status_code = 403
                error.code = "untrusted-secret-value"
                raise error
        result = ground(self.interpreted, self.il, FailingProvider(), run_id="x")
        self.assertEqual("provider_failure", result["status"])
        self.assertEqual({"exception_type": "RuntimeError", "http_status": 403},
                         result["provider_error"])
        self.assertNotIn("secret-value", json.dumps(result))
        with patch.dict(os.environ, {}, clear=True):
            missing = ground(self.interpreted, self.il,
                             GroqGrounderProvider(model="explicit-test-model"), run_id="x")
        self.assertEqual({"exception_type": "MissingGroqCredentialError",
                          "error_code": "MISSING_GROQ_API_KEY"}, missing["provider_error"])

    def test_intention_library_validation(self):
        il = copy.deepcopy(self.il); il["intentions"]["compare.time"]["parent"] = "missing"
        with self.assertRaises(IntentionLibraryError): validate_intention_library(il)
        with self.assertRaises(IntentionLibraryError): load_intention_library(expected_version="9")

    def test_profile_and_unknown_alignment(self):
        path = Path(importlib.resources.files("intention_grounding").joinpath("fixtures/offline_table.csv"))
        profile = profile_table(path)
        self.assertEqual(4, profile["row_count"])
        self.assertTrue(all(column["evidence_ref"] for column in profile["columns"]))
        card = self.run_proposal(self.proposal)["grounded_intention"]
        compared = compare_card(card, [profile])
        self.assertTrue(all(r["state"] == "unresolved" for r in compared["tables"][0]["requirements"]))
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

    def test_live_cli_requires_model_and_sanitizes_provider_failure(self):
        stream = io.StringIO()
        with patch.dict(os.environ, {}, clear=True), contextlib.redirect_stdout(stream):
            self.assertEqual(2, main(["--mode", "groq", "--input", "Compare income."]))
        self.assertEqual("configuration_error=MISSING_GROQ_MODEL_ID", stream.getvalue().strip())

        class FailingProvider:
            metadata = {"provider": "mock", "model": "explicit-test-model"}
            def invoke(self, *_):
                error = RuntimeError("secret-value Authorization: Bearer secret-value")
                error.status_code = 429
                error.code = "rate_limit_exceeded"
                raise error

        with tempfile.TemporaryDirectory() as directory:
            stream = io.StringIO()
            with patch("intention_grounding.cli.GroqProvider", return_value=FailingProvider()), \
                 patch("intention_grounding.cli.GroqGrounderProvider", return_value=FailingProvider()), \
                 patch.dict(os.environ, {"GROQ_API_KEY": "secret-value"}), \
                 contextlib.redirect_stdout(stream):
                exit_code = main(["--mode", "groq", "--model", "explicit-test-model",
                                  "--input", "Compare income.", "--output", directory])
            self.assertEqual(2, exit_code)
            run = next(Path(directory).iterdir())
            interpretation = json.loads((run / "interpretation.json").read_text())
            grounding = json.loads((run / "grounding.json").read_text())
            self.assertEqual({"exception_type": "RuntimeError", "http_status": 429,
                              "error_code": "rate_limit_exceeded"}, interpretation["provider_error"])
            self.assertEqual("invalid_interpretation", grounding["status"])
            self.assertNotIn("secret-value", stream.getvalue())
            for path in run.iterdir():
                self.assertNotIn("secret-value", path.read_text())

    def test_model_list_cli_is_safe_and_offline_when_mocked(self):
        stream = io.StringIO()
        with patch("intention_grounding.cli.list_available_models", return_value=["a/model", "b-model"]) as mocked, \
             contextlib.redirect_stdout(stream):
            self.assertEqual(0, main(["--list-models"]))
        mocked.assert_called_once_with()
        self.assertEqual(["a/model", "b-model"], stream.getvalue().splitlines())

    def test_missing_key_stays_in_safe_artifact_and_model_preflight(self):
        with tempfile.TemporaryDirectory() as directory:
            stream = io.StringIO()
            with patch.dict(os.environ, {}, clear=True), contextlib.redirect_stdout(stream):
                self.assertEqual(2, main(["--mode", "groq", "--model", "explicit-test-model",
                                          "--input", "Compare income.", "--output", directory]))
            run = next(Path(directory).iterdir())
            interpretation = json.loads((run / "interpretation.json").read_text())
            self.assertEqual({"exception_type": "MissingGroqCredentialError",
                              "error_code": "MISSING_GROQ_API_KEY"}, interpretation["provider_error"])
            self.assertIn("MISSING_GROQ_API_KEY", stream.getvalue())
            self.assertNotIn("Authorization", (run / "interpretation.json").read_text())
        stream = io.StringIO()
        with patch.dict(os.environ, {}, clear=True), contextlib.redirect_stdout(stream):
            self.assertEqual(2, main(["--list-models"]))
        self.assertEqual("model_list_error=MISSING_GROQ_API_KEY", stream.getvalue().strip())

    def test_notebook_live_cell_preflights_environment_without_calls(self):
        notebook = json.loads((Path(__file__).parents[1] / "notebooks/pipeline_walkthrough.ipynb").read_text())
        source = "".join(notebook["cells"][-1]["source"])
        self.assertIn("RUN_LIVE_GROQ = False", source)
        live_source = source.replace("RUN_LIVE_GROQ = False", "RUN_LIVE_GROQ = True", 1)
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(RuntimeError, "GROQ_MODEL_ID"):
                exec(live_source, {})
        with patch.dict(os.environ, {"GROQ_API_KEY": "test-only-key"}, clear=True):
            with self.assertRaisesRegex(RuntimeError, "GROQ_MODEL_ID"):
                exec(live_source, {})
        with patch.dict(os.environ, {"GROQ_MODEL_ID": "test-model"}, clear=True):
            with self.assertRaisesRegex(RuntimeError, "GROQ_API_KEY"):
                exec(live_source, {})


if __name__ == "__main__":
    unittest.main()
