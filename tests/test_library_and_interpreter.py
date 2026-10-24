import json
import unittest

from intention_grounding import aligner, il
from intention_grounding.interpreter import (RuleInterpreter, ReplayInterpreter, interpret, validate_extraction,
                                             STATUS_EXTRACTED, STATUS_FAILURE, STATUS_NO_INTENTION)
from intention_grounding.interpreter.core import ExtractionError

L = il.load()
VOC = L["vocabulary"]


class IntentionLibraryTests(unittest.TestCase):
    def test_registration_has_no_problems_and_all_predicates_exist(self):
        self.assertEqual(il.registration_problems(L, predicates=set(aligner.PREDICATES)), [])

    def test_structure_matches_paper(self):
        self.assertEqual(set(L["axes"]), {"sem", "str", "cov", "qual", "aff"})
        self.assertEqual(L["variants"]["compare.group_means"]["procedures"], ["means.raw", "means.stored"])
        for pid, p in L["procedures"].items():
            self.assertTrue(p["hard"], pid)

    def test_definitions_exclude_requirements(self):
        d = json.dumps(il.definitions(L))
        self.assertNotIn("evidence_rule", d)
        self.assertNotIn("predicate", d)

    def test_registration_detects_broken_reference(self):
        broken = json.loads(json.dumps({k: v for k, v in L.items() if not k.startswith("_")}))
        broken["procedures"]["means.raw"]["hard"].append("no.such.requirement")
        self.assertTrue(any("no.such.requirement" in p for p in il.registration_problems(broken)))


def z(**kw):
    base = {"context_query": "salaries across departments", "intention_expression": "Compare",
            "arguments": [{"id": "a1", "label": "measure", "value": "salaries", "spans": ["salaries"]}], "scope": []}
    base.update(kw)
    return base


class InterpreterValidationTests(unittest.TestCase):
    U = "Compare average salaries across departments"

    def test_valid_extraction(self):
        self.assertTrue(validate_extraction(z(), self.U, VOC))

    def test_span_not_in_input_rejected(self):
        bad = z(arguments=[{"id": "a1", "label": "measure", "value": "wages", "spans": ["wages"]}])
        with self.assertRaises(ExtractionError):
            validate_extraction(bad, self.U, VOC)

    def test_unknown_label_and_duplicate_id_rejected(self):
        with self.assertRaises(ExtractionError):
            validate_extraction(z(arguments=[{"id": "a1", "label": "dimension", "value": "x", "spans": ["salaries"]}]), self.U, VOC)
        dup = [{"id": "a1", "label": "measure", "value": "s", "spans": ["salaries"]}, {"id": "a1", "label": "group_dimension", "value": "d", "spans": ["departments"]}]
        with self.assertRaises(ExtractionError):
            validate_extraction(z(arguments=dup), self.U, VOC)

    def test_statuses_and_fallback(self):
        ok = interpret(self.U, ReplayInterpreter({self.U: z()}), VOC)
        self.assertEqual(ok.status, STATUS_EXTRACTED)
        none = interpret(self.U, ReplayInterpreter({self.U: z(intention_expression=None, arguments=[])}), VOC)
        self.assertEqual((none.status, none.intention), (STATUS_NO_INTENTION, None))
        failed = interpret(self.U, ReplayInterpreter({}), VOC)  # provider failure
        self.assertEqual((failed.status, failed.context_query), (STATUS_FAILURE, self.U))
        malformed = interpret(self.U, ReplayInterpreter({self.U: {"context_query": "x"}}), VOC)
        self.assertEqual(malformed.status, STATUS_FAILURE)
        self.assertTrue(malformed.failure.startswith("INVALID_EXTRACTION"))

    def test_rule_interpreter(self):
        r = interpret("Compare mean COVID-19 vaccine side-effect severity scores across age groups in Europe", RuleInterpreter(), VOC)
        labels = {(a["label"], a["value"]) for a in r.intention["arguments"]}
        self.assertIn(("group_dimension", "age groups"), labels)
        self.assertIn(("statistic", "mean"), labels)
        self.assertEqual(r.intention["scope"][0]["value"], "Europe")
        self.assertEqual(interpret("COVID-19 vaccination data for Europe", RuleInterpreter(), VOC).status, STATUS_NO_INTENTION)
        p = interpret("Compare people fully vaccinated per hundred across countries", RuleInterpreter(), VOC)
        self.assertIn(("group_dimension", "countries"), {(a["label"], a["value"]) for a in p.intention["arguments"]})


if __name__ == "__main__":
    unittest.main()
