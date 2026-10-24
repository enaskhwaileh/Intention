import unittest

from intention_grounding import il
from intention_grounding.grounder import IndexResolver, ReplayResolver, ground
from intention_grounding.interpreter import ReplayInterpreter, RuleInterpreter, interpret

L = il.load()
U = "Compare mean severity scores across age groups in Europe"
Z = {"context_query": "severity scores across age groups in Europe", "intention_expression": "Compare",
     "arguments": [{"id": "a1", "label": "statistic", "value": "mean", "spans": ["mean"]},
                   {"id": "a2", "label": "measure", "value": "severity scores", "spans": ["severity scores"]},
                   {"id": "a3", "label": "group_dimension", "value": "age groups", "spans": ["age groups"]}],
     "scope": [{"id": "s1", "label": "geography", "value": "Europe", "spans": ["in Europe"]}]}


def interp(u=U, z=Z):
    return interpret(u, ReplayInterpreter({u: z}), L["vocabulary"]).to_dict()


def proposal(**kw):
    p = {"status": "proposed", "variant_id": "compare.group_means",
         "bindings": {"statistic": ["a1"], "measure": ["a2"], "group_dimension": ["a3"]},
         "scope": ["s1"], "justification": "", "diagnostics": []}
    p.update(kw)
    return p


class GrounderTests(unittest.TestCase):
    def test_paper_example_grounds_both_mean_procedures(self):
        g = ground(interp(), L, ReplayResolver({U: proposal()}))
        self.assertEqual(g["status"], "grounded")
        self.assertEqual([p["procedure_id"] for p in g["psi_u"]], ["means.raw", "means.stored"])
        valid = next(r for r in g["psi_u"][0]["hard"] if r["requirement_id"] == "means.raw.valid")
        self.assertEqual(valid["id"], "means.raw/means.raw.valid")
        self.assertEqual(g["g_u"]["theta"]["measure"], "severity scores")
        scope = next(r for r in g["psi_u"][0]["hard"] if r["requirement_id"] == "compare.common.scope")
        self.assertEqual(scope["params"]["scope"], [{"label": "geography", "value": "Europe"}])
        self.assertEqual(valid["provenance"]["il_version"], "1.0.0")

    def test_index_resolver_matches_gold(self):
        g = ground(interp(), L, IndexResolver(L))
        self.assertEqual((g["status"], g["g_u"]["variant_id"]), ("grounded", "compare.group_means"))

    def test_shorter_input_is_insufficient(self):
        u = "Compare COVID-19 vaccine side effects in Europe"
        r = interpret(u, RuleInterpreter(), L["vocabulary"]).to_dict()
        g = ground(r, L, IndexResolver(L))
        self.assertEqual(g["status"], "insufficient")
        self.assertEqual(g["psi_u"], [])

    def test_contract_violations_fail(self):
        for bad in (proposal(variant_id="compare.median"), proposal(bindings={"statistic": ["a1"], "measure": ["a9"], "group_dimension": ["a3"]}),
                    proposal(bindings={"statistic": ["a1"], "measure": ["a3"], "group_dimension": ["a2"]}) | {"variant_id": "monitor.trend"},
                    proposal(scope=[])):
            g = ground(interp(), L, ReplayResolver({U: bad}))
            self.assertEqual(g["status"], "failure", bad)
            self.assertTrue(g["diagnostics"][0]["code"].startswith("CONTRACT_INVALID"))

    def test_missing_required_role_is_insufficient(self):
        g = ground(interp(), L, ReplayResolver({U: proposal(bindings={"measure": ["a2"], "group_dimension": ["a3"]})}))
        self.assertEqual(g["status"], "insufficient")

    def test_inadmissible_statistic_is_unsupported(self):
        z = dict(Z, arguments=[dict(Z["arguments"][0], value="median", spans=["mean"])] + Z["arguments"][1:])
        g = ground(interp(z=z), L, ReplayResolver({U: proposal()}))
        self.assertEqual(g["status"], "unsupported")

    def test_applicability_excludes_raw_procedure_for_reported_means(self):
        u = "Compare reported mean severity scores across age groups in Europe"
        z = dict(Z, arguments=[{"id": "a1", "label": "statistic", "value": "reported mean", "spans": ["reported mean"]}] + Z["arguments"][1:])
        g = ground(interp(u, z), L, ReplayResolver({u: proposal()}))
        self.assertEqual([p["procedure_id"] for p in g["psi_u"]], ["means.stored"])
        self.assertEqual(g["g_u"]["procedure_decisions"]["means.raw"], "excluded")

    def test_no_intention_is_not_attempted(self):
        u = "vaccination data"
        z = {"context_query": u, "intention_expression": None, "arguments": [], "scope": []}
        self.assertEqual(ground(interp(u, z), L, IndexResolver(L))["status"], "not_attempted")


if __name__ == "__main__":
    unittest.main()
