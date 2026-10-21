"""Hand-checkable fixtures test mechanics, never independent usefulness labels."""
import copy
import json
from pathlib import Path
import tempfile
import unittest

from intention_grounding.contracts import validate_splits
from intention_grounding.discovery import run
from intention_grounding.grounder import ground_request
from intention_grounding.profiler import sha256
from intention_grounding.procedures import quote_identifier
from intention_grounding.retrieval import retrieve


class DiscoveryTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        (self.root/'observations.csv').write_text('date,group,count\n2011-01-01,A,2\n2011-01-02,A,4\n2011-01-01,B,4\n2011-01-02,B,6\n')
        (self.root/'documentation.txt').write_text('Test fixture: interval counts for test system, daily rows; groups A/B. No real-world provenance claim.')
        doc={'path':'documentation.txt','sha256':sha256(self.root/'documentation.txt'),'locator':'entire test fixture specification'}
        table={'table_id':'fixture','source_family':'test_fixture','topic':'test','path':'observations.csv','normalized_sha256':sha256(self.root/'observations.csv'),
               'retrieval_text':'count daily group test system', 'semantics':{'population':'test_system','measure_concept':'count','unit':'count','grain':'day','measure_kind':'interval_count',
               'columns':{'measure':'count','date':'date','group':'group'},'source_document':doc}}
        self.corpus={'schema_version':'1.0','corpus_id':'test','partition':'development_only','sources':[],'tables':[table],'independent_usefulness_judgments':False}
        self.manifest=self.root/'manifest.json';self.write_corpus()
        self.request={'schema_version':'1.0','request_id':'test','text':'Compare mean daily count for groups A and B in the test system.',
                      'input_mode':'authored_structured_request','status':'ready','intention_type':'compare','topic':'test',
                      'roles':{'population':'test_system','measure_concept':'count','unit':'count','grain':'day','group_role':'group','groups':['A','B'],'period':['2011-01-01','2011-01-02'],'statistic':'mean'}}

    def write_corpus(self):self.manifest.write_text(json.dumps(self.corpus))
    def execute(self, **kwargs):return run(self.request,root=self.root,manifest_path=self.manifest,**kwargs)

    def test_means_agree_with_hand_calculation_and_evidence_resolves(self):
        result=self.execute();p=result['ranking'][0]['procedures'][0]
        self.assertEqual('supported',p['outcome'])
        self.assertEqual([3.,5.],[r['value'] for r in p['execution']['rows']])
        self.assertEqual(2.,p['execution']['difference_second_minus_first'])
        self.assertIn('AVG(',p['execution']['parameterized_sql'])
        self.assertEqual(['2011-01-01','2011-01-02','A','B'],p['execution']['parameters'])
        evidence={e['id'] for e in p['evidence']}
        self.assertTrue(all(v['evidence_refs'] and set(v['evidence_refs'])<=evidence for v in p['requirements']))
        self.assertIsNone(result['effectiveness']['metrics'])

    def test_direct_values_reject_duplicates_and_never_implicitly_average(self):
        self.request['roles']['statistic']='documented'
        p=self.execute()['ranking'][0]['procedures'][0]
        self.assertEqual('violated',p['outcome']);self.assertEqual('not_executed',p['execution']['status'])
        self.request['roles']['period']=['2011-01-01','2011-01-01']
        p=self.execute()['ranking'][0]['procedures'][0]
        self.assertEqual([2.,4.],[r['value'] for r in p['execution']['rows']])

    def test_missing_docs_incompatible_units_and_precomputed_means(self):
        p=self.execute(withhold_semantics=True)
        self.assertTrue(p['abstained']);self.assertEqual('unresolved',p['ranking'][0]['overall_state'])
        self.request['roles']['unit']='kilograms'
        self.assertEqual('violated',self.execute()['ranking'][0]['overall_state'])
        self.request['roles']['unit']='count'
        self.corpus['tables'][0]['semantics']['measure_kind']='precomputed_mean';self.write_corpus()
        p=self.execute()['ranking'][0]['procedures'][0]
        self.assertEqual('not_executed',p['execution']['status'])
        self.assertEqual('violated',p['outcome'])

    def test_ambiguous_predict_missing_group_and_sql_injection_value(self):
        self.request['roles']['statistic']='unspecified'
        self.assertEqual('ambiguous',ground_request(self.request)['status'])
        self.assertTrue(self.execute()['abstained'])
        self.request['intention_type']='predict'
        self.assertEqual('unsupported',ground_request(self.request)['status'])
        self.request['intention_type']='compare';self.request['roles']['statistic']='mean'
        self.request['roles']['groups']=['A',"B' OR 1=1 --"]
        p=self.execute()['ranking'][0]['procedures'][0]
        self.assertEqual('violated',p['outcome']);self.assertEqual('not_executed',p['execution']['status'])
        self.assertEqual('"x""; DROP TABLE t;--"',quote_identifier('x"; DROP TABLE t;--'))

    def test_hashes_gold_isolation_and_deterministic_ranking(self):
        first=self.execute();(self.root/'judgments.json').write_text('{"fixture":"useful"}')
        second=self.execute();(self.root/'judgments.json').unlink()
        third=self.execute()
        for result in [second,third]:
            self.assertEqual(first['candidates'],result['candidates'])
            self.assertEqual(first['ranking'][0]['overall_state'],result['ranking'][0]['overall_state'])
            self.assertEqual(first['ranking'][0]['procedures'],result['ranking'][0]['procedures'])
        (self.root/'observations.csv').write_text('changed')
        with self.assertRaisesRegex(ValueError,'HASH_MISMATCH'):self.execute()

    def test_split_family_and_topic_leakage(self):
        split={'schema_version':'1.0','designation':'development_only','partitions':{'development':{'table_ids':['fixture'],'request_ids':['test']}}}
        validate_splits(split,self.corpus,[self.request])
        split['designation']='topic_family_disjoint';split['partitions']['test']=copy.deepcopy(split['partitions']['development'])
        with self.assertRaisesRegex(ValueError,'SPLIT_LEAKAGE'):validate_splits(split,self.corpus,[self.request])

    def test_explicit_alternatives_keep_separate_verdicts(self):
        self.request['roles']['statistic']='documented_or_mean'
        result=self.execute()
        procedures=result['ranking'][0]['procedures']
        self.assertEqual(2,len(procedures))
        self.assertEqual(['violated','supported'],[p['outcome'] for p in procedures])
        self.assertEqual('supported',result['ranking'][0]['overall_state'])
        self.assertEqual('accepted_alternatives',result['grounded_intention']['procedure_relationship'])

    def test_bm25_and_ties_are_hand_checkable(self):
        import math
        tables=[{'table_id':'b','retrieval_text':'bike'},{'table_id':'a','retrieval_text':'bike'}]
        result=retrieve('bike',tables)
        self.assertEqual(['a','b'],[r['table_id'] for r in result])
        self.assertAlmostEqual(math.log(1+.5/2.5),result[0]['retrieval_score'])
        self.assertEqual(0,retrieve('absent',tables)[0]['retrieval_score'])


if __name__=='__main__':unittest.main()
