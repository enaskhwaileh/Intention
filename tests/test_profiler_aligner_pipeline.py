import unittest

from common import fig1_manifest, tmpdir

from intention_grounding import aligner, il, profiler
from intention_grounding.context import ContextMatcher
from intention_grounding.grounder import IndexResolver, ground
from intention_grounding.interpreter import RuleInterpreter, interpret
from intention_grounding.pipeline import Pipeline, combine_linear, combine_product

L = il.load()
M = fig1_manifest()
T = {t["table_id"]: t for t in M["tables"]}
CACHE = tmpdir()


def prof(tid):
    return profiler.profile(T[tid], cache_dir=CACHE)


def grounded(u):
    r = interpret(u, RuleInterpreter(), L["vocabulary"]).to_dict()
    g = ground(r, L, IndexResolver(L))
    assert g["status"] == "grounded", g["diagnostics"]
    return g


class ProfilerTests(unittest.TestCase):
    def test_types_geography_kinds(self):
        p = prof("fig1.country_rates")
        cols = {c["name"]: c for c in p["columns"]}
        self.assertEqual(cols["country"]["geo"]["level"], "country")
        self.assertEqual(cols["mild_side_effect_rate"]["measure_kind"]["kind"], "rate")
        self.assertEqual(cols["vaccinated_population"]["type"], "numeric")
        r = prof("fig1.regional_summary")
        self.assertEqual({c["name"]: c for c in r["columns"]}["region"]["geo"]["level"], "continent")
        lg = prof("fig1.vaccine_logistics")
        self.assertEqual({c["name"]: c for c in lg["columns"]}["delivery_date"]["temporal"]["grain"], "day")
        self.assertIn("shipment_id", lg["structure"]["identifiers"])

    def test_cache_and_full_scan(self):
        a = profiler.profile(T["fig1.patient_records"], cache_dir=CACHE)
        b = profiler.profile(T["fig1.patient_records"], cache_dir=CACHE)
        self.assertTrue(b["cache_hit"])
        self.assertEqual(a["rows"], 240)
        self.assertTrue(a["scan"]["complete"])


class AlignerTests(unittest.TestCase):
    def test_compare_country_rates(self):
        """Figure 1: comparing country-level rates prefers B; A loses the country distinction."""
        g = grounded("Compare mild side effect rates across countries in Europe")
        self.assertEqual(g["g_u"]["variant_id"], "compare.observed_values")
        b = aligner.assess(T["fig1.country_rates"], prof("fig1.country_rates"), g)
        a = aligner.assess(T["fig1.regional_summary"], prof("fig1.regional_summary"), g)
        d = aligner.assess(T["fig1.vaccine_logistics"], prof("fig1.vaccine_logistics"), g)
        self.assertEqual(b["state"], "supported")
        self.assertEqual(a["state"], "violated")
        self.assertGreater(b["A"], d["A"])
        verdict = next(v for v in a["procedures"][0]["requirements"] if v["verdict"] == "violated")
        self.assertIn("geographic", str(verdict["evidence"]))

    def test_predict_individual_outcome(self):
        """Figure 1: predicting an individual's side-effect type prefers patient records C."""
        g = grounded("Predict the side effect type of a patient from age, dose and prior condition")
        self.assertEqual(g["g_u"]["variant_id"], "predict.classification")
        c = aligner.assess(T["fig1.patient_records"], prof("fig1.patient_records"), g)
        b = aligner.assess(T["fig1.country_rates"], prof("fig1.country_rates"), g)
        self.assertEqual(c["state"], "supported")
        self.assertNotEqual(b["state"], "supported")

    def test_raw_mean_rejects_existing_rates_and_group_means_need_valid_values(self):
        g = grounded("Compare the average severity score across countries")
        c = aligner.assess(T["fig1.patient_records"], prof("fig1.patient_records"), g)
        self.assertEqual(c["procedures"][0]["procedure_id"], "means.raw")
        self.assertEqual(c["procedures"][0]["state"], "supported")
        g2 = grounded("Compare the average mild side effect rate across countries")
        b = aligner.assess(T["fig1.country_rates"], prof("fig1.country_rates"), g2)
        raw = next(p for p in b["procedures"] if p["procedure_id"] == "means.raw")
        self.assertEqual(raw["state"], "violated")  # unweighted average of existing rates is not implicit

    def test_absence_is_unresolved_not_violated(self):
        g = grounded("Compare the average hospital stay across countries")
        d = aligner.assess(T["fig1.vaccine_logistics"], prof("fig1.vaccine_logistics"), g)
        concept = next(v for v in d["procedures"][0]["requirements"] if v["id"].endswith("compare.common.concept"))
        self.assertEqual(concept["verdict"], "unresolved")


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.matcher = ContextMatcher(M, "bm25", cache_dir=None)

    def pipe(self, **kw):
        return Pipeline(M, library=L, interpreter=RuleInterpreter(), resolver=IndexResolver(L), matcher=self.matcher,
                        k_candidates=4, profile_cache=CACHE, **kw)

    def test_ranking_changes_with_intention(self):
        compare = self.pipe().run("Compare COVID-19 vaccine mild side effect rates across countries in Europe")
        predict = self.pipe().run("Predict the side effect type of a COVID-19 vaccine patient from age, dose and prior condition")
        self.assertEqual(compare["top_k"][0], "fig1.country_rates")
        self.assertEqual(predict["top_k"][0], "fig1.patient_records")
        for stage in ("interpreter_ms", "context_matching_ms", "grounder_ms", "profiler_ms", "aligner_ms", "ranking_ms", "total_ms"):
            self.assertIn(stage, compare["timing"])

    def test_no_intention_uses_context_only(self):
        rep = self.pipe().run("COVID-19 vaccine side effects data")
        self.assertEqual(rep["mode"], "context_only_fallback")
        self.assertTrue(all(x["U"] == x["r"] for x in rep["ranking"]))
        self.assertEqual(rep["timing"]["profiled_tables"], 0)

    def test_combination_functions_are_monotone(self):
        grid = [i / 10 for i in range(11)]
        for f in (combine_linear, combine_product):
            for r in grid:
                vals = [f(r, a) for a in grid]
                self.assertEqual(vals, sorted(vals))
                self.assertTrue(all(0 <= v <= 1 for v in vals))


if __name__ == "__main__":
    unittest.main()
