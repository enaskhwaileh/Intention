import json
import math
from pathlib import Path
import tempfile
import unittest
from intention_grounding.evaluation import request_metrics, annotation_template, evaluate
from intention_grounding.profiler import sha256


class EvaluationTests(unittest.TestCase):
    def test_hand_calculated_metrics(self):
        labels={'a':'useful','b':'not_useful','c':'useful'}
        r=request_metrics(['b','a'],['a','b'],labels)
        self.assertAlmostEqual((1/math.log2(3))/(1+1/math.log2(3)),r['ndcg_at_10'])
        self.assertEqual(0,r['success_at_1']);self.assertEqual(.5,r['recall_at_10']);self.assertEqual(.5,r['candidate_recall'])
        r=request_metrics([],[],labels)
        self.assertEqual(0,r['ndcg_at_10']);self.assertEqual(0,r['recall_at_10'])

    def test_unjudged_unresolved_no_positive_and_duplicates(self):
        for state in ['unresolved','unjudged']:
            r=request_metrics(['a'],['a'],{'a':'useful','b':state})
            self.assertFalse(r['eligible']);self.assertIsNone(r['ndcg_at_10'])
        self.assertEqual('fully_judged_no_positive',request_metrics(['a'],['a'],{'a':'not_useful'})['reason'])
        with self.assertRaises(ValueError):request_metrics(['a','a'],['a'],{'a':'useful'})

    def test_no_generated_gold_and_immutable_predictions(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'predictions.json';j=Path(d)/'judgments.json'
            report={'corpus_sha256':'corpus','request_sha256':'request','request':{'request_id':'test'}}
            p.write_text(json.dumps(report));(p.parent/'predictions.sha256').write_text(sha256(p))
            template=annotation_template(report,['a','b']);j.write_text(json.dumps(template))
            self.assertFalse(template['independently_reviewed'])
            self.assertEqual('pending_independent_review',evaluate(p,j,['a','b'])['status'])
            p.write_text('{}')
            with self.assertRaisesRegex(ValueError,'IMMUTABLE'):evaluate(p,j,['a','b'])
