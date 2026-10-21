"""Authored mock outputs test contracts and integration, NOT measured LLM accuracy."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from intention_grounding.discovery import run_text
from intention_grounding.language import adapt, interpret_input
from intention_grounding.interpreter.core import interpret
from intention_grounding.interpreter.providers import ReplayProvider
from intention_grounding.semantic_retrieval import retrieve, serialize
from intention_grounding.profiler import sha256

DIRECT='Contrast recorded values of daily bike rental counts in rentals for Capital Bikeshare Washington DC on 2011-01-01 versus 2011-01-02.'
MEAN='For Capital Bikeshare Washington DC compare the arithmetic mean of hourly bike rental counts in rentals by working-day status for working days and weekends and holidays during 2011.'


def mock_document(text=DIRECT, mean=False, statistic_present=True):
    evidence=[]
    def value(literal):
        start=text.index(literal);ident='e'+str(len(evidence)+1)
        evidence.append({'id':ident,'start':start,'end':start+len(literal),'text':literal})
        return {'literal':literal,'normalized':None,'evidence':[ident]}
    expression=value('compare' if mean else 'Contrast')
    pairs=[('population','Capital Bikeshare Washington DC'),('measure','bike rental counts'),('unit','rentals'),
           ('time_grain','hourly' if mean else 'daily'),('method','arithmetic mean' if mean else 'recorded values')]
    pairs+=([('group_dimension','working-day status'),('groups','working days'),('groups','weekends and holidays'),('time_range','2011')] if mean else [('time_points','2011-01-01'),('time_points','2011-01-02')])
    if not statistic_present:pairs=[p for p in pairs if p[0]!='method']
    args=[{'role':role,'value':value(literal)} for role,literal in pairs]
    return {'schema_version':'2.0','input_id':'test','original_input':text,'evidence':evidence,
            'query_profile':{'topics':[],'entities':[args[0]['value']],'measures':[args[1]['value']],
                             'constraints':[a['value'] for a in args if a['role'].startswith('time_')]},
            'intentions':[{'id':'i1','expression':expression,'arguments':args,'missing':[],
                           'candidates':[{'id':'c1','label':expression,'arguments':copy.deepcopy(args),
                                          'reading':{'description':'Authored contract fixture','evidence':expression['evidence']}}]}],
            'relationships':[{'kind':'single','members':['i1'],'evidence':expression['evidence']}],
            'status':'unambiguous','diagnostics':[]}


class FakeEncoder:
    model_id='explicit-test-encoder'
    revision='test-revision'
    def __init__(self):self.calls=[]
    def encode(self,texts):
        self.calls.extend(texts)
        return [[1.,float(len(t)%7+1),2.] for t in texts]
    def prepare(self,serialization):return serialization['text'],{}
    def truncation(self,text):return {'tokens_before_limit':len(text.split()),'model_max_tokens':256,'tokens_truncated':0}


class LanguageDiscoveryTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
        (self.root/'table.csv').write_text('date,workingday,cnt\n2011-01-01,0,2\n2011-01-02,1,4\n2011-12-31,0,6\n')
        (self.root/'source.txt').write_text('Synthetic contract fixture only; no real source claim.')
        self.table={'table_id':'fixture','source_family':'fixture','topic':'fixture','path':'table.csv',
                    'normalized_sha256':sha256(self.root/'table.csv'),'retrieval_text':'bike rental counts daily hourly',
                    'title':'Synthetic counts','description':'Authored fixture, not UCI data',
                    'semantics':{'population':'capital_bikeshare_dc','measure_concept':'bike_rental_count','unit':'rentals','grain':'day',
                                 'measure_kind':'interval_count','columns':{'measure':'cnt','date':'date','workingday':'workingday'},
                                 'source_document':{'path':'source.txt','sha256':sha256(self.root/'source.txt')}}}
        self.manifest=self.root/'manifest.json';self.write_manifest()

    def write_manifest(self):
        self.manifest.write_text(json.dumps({'schema_version':'1.0','corpus_id':'fixture','partition':'development_only',
            'sources':[],'tables':[self.table],'independent_usefulness_judgments':False}))

    def execute(self,doc=None,**kwargs):
        doc=doc or mock_document()
        return run_text(doc['original_input'],input_id='test',provider=ReplayProvider(json.dumps(doc)),
                        root=self.root,manifest_path=self.manifest,**kwargs)

    def test_direct_compatibility_and_evidence_separation(self):
        report=self.execute(retrieval_method='bm25',execute=True)
        self.assertFalse(report['abstained'],report)
        self.assertEqual('Capital Bikeshare Washington DC',report['grounded_intention']['procedures'][0]['bindings']['population'])
        p=report['ranking'][0]['procedures'][0]
        self.assertEqual([2.,4.],[r['value'] for r in p['execution']['rows']])
        self.assertIn('request-vocabulary',{e['id'] for e in p['evidence']})
        self.assertIn('Authored mock',report['request']['purpose'])
        self.assertEqual(0,report['diagnostics']['live_model_calls'])

    def test_explicit_mean_and_sbert_ranking_share_assessment(self):
        self.table['semantics']['grain']='hour';self.write_manifest()
        report=self.execute(mock_document(MEAN,True),encoder=FakeEncoder(),execute=True)
        self.assertFalse(report['abstained'],report)
        self.assertEqual([4.,4.],[r['value'] for r in report['ranking'][0]['procedures'][0]['execution']['rows']])
        self.assertEqual('SBERT cosine similarity',report['ranking_policy']['within_state_score'])
        self.assertIn('Capital Bikeshare Washington DC',report['retrieval_query'])
        self.assertIn('2011',report['retrieval_query'])
        self.assertNotIn('arithmetic mean',report['retrieval_query'])

    def test_missing_statistic_and_unit_never_default(self):
        for missing in ('method','unit'):
            doc=mock_document();intention=doc['intentions'][0]
            intention['arguments']=[a for a in intention['arguments'] if a['role']!=missing]
            intention['candidates'][0]['arguments']=copy.deepcopy(intention['arguments'])
            result=self.execute(doc,retrieval_method='bm25')
            self.assertTrue(result['abstained'])
            self.assertEqual([],result['grounded_intention']['procedures'])
            self.assertNotIn('statistic' if missing=='method' else 'unit',result['request']['roles'])

    def test_actually_unspecified_statistic_and_predict_abstain(self):
        text=DIRECT.replace('recorded values of ','')
        doc=mock_document(text,statistic_present=False)
        result=self.execute(doc,retrieval_method='bm25')
        self.assertTrue(result['abstained']);self.assertNotIn('statistic',result['request']['roles'])
        doc=mock_document()
        # Predict is unsupported even if all Compare-shaped arguments are present.
        doc['original_input']=doc['original_input'].replace('Contrast','Forecast')
        doc['evidence'][0]['text']='Forecast'
        doc['intentions'][0]['expression']['literal']='Forecast'
        result=self.execute(doc,retrieval_method='bm25')
        self.assertTrue(result['abstained']);self.assertEqual('unsupported',result['grounded_intention']['status'])

    def test_cli_input_routes_to_discovery_without_diagnostic_fallback(self):
        from intention_grounding.cli import main
        import contextlib,io
        path=self.root/'mock.json';path.write_text(json.dumps(mock_document()))
        with patch('intention_grounding.discovery.run_text',return_value={'run_id':'test','abstained':True}) as run, patch('intention_grounding.discovery.save_report',return_value=Path('predictions.json')),contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(0,main(['--input',DIRECT,'--input-id','test','--mock-response',str(path),'--no-execute']))
        self.assertEqual(DIRECT,run.call_args.args[0]);self.assertEqual('sbert',run.call_args.kwargs['retrieval_method'])
        self.assertFalse(run.call_args.kwargs['allow_live']);self.assertFalse(run.call_args.kwargs['execute'])
        with contextlib.redirect_stderr(io.StringIO()),self.assertRaises(SystemExit):
            main(['--mode','discovery','--input',DIRECT,'--case','dc_daily'])

    def test_invented_literals_and_unsupported_scope_are_rejected(self):
        doc=mock_document();doc['intentions'][0]['arguments'][0]['value']['literal']='invented_population_code'
        result=self.execute(doc,retrieval_method='bm25')
        self.assertEqual('INTERPRETER_LITERAL_MISMATCH',result['failure'])
        doc=mock_document();doc['query_profile']['constraints'].append(doc['intentions'][0]['expression'])
        result=self.execute(doc,retrieval_method='bm25')
        self.assertTrue(result['abstained']);self.assertIn('UNSUPPORTED_SCOPE_RESTRICTION',result['interpreter']['adapter']['unresolved'])

    def test_uncurated_semantics_stay_unresolved(self):
        doc=mock_document();old='Capital Bikeshare Washington DC';new='Unmapped rental population'
        text=DIRECT.replace(old,new)
        # Move exact evidence offsets after the replacement; never assert invented literals.
        for e in doc['evidence']:
            e['text']=e['text'].replace(old,new);e['start']=text.index(e['text']);e['end']=e['start']+len(e['text'])
        for arg in doc['intentions'][0]['arguments']:
            arg['value']['literal']=arg['value']['literal'].replace(old,new)
        doc['intentions'][0]['candidates'][0]['arguments']=copy.deepcopy(doc['intentions'][0]['arguments'])
        doc['original_input']=text
        result=self.execute(doc,retrieval_method='bm25',execute=True)
        self.assertTrue(result['abstained'],result)
        self.assertEqual('unresolved',result['ranking'][0]['overall_state'])

    def test_serialization_cache_invalidation_ties_and_baseline(self):
        encoder=FakeEncoder();tables=[dict(self.table,table_id='b'),dict(self.table,table_id='a')]
        first=retrieve('bike',tables,self.root,encoder=encoder)
        self.assertEqual(['a','b'],[r['table_id'] for r in first])
        self.assertIn('Columns:',first[0]['serialization']['text']);self.assertIn('First observed rows:',first[0]['serialization']['text'])
        again=retrieve('bike',tables,self.root,encoder=encoder,query_mode='full_request')
        self.assertTrue(all(r['cache_hit'] for r in again));self.assertEqual(first[0]['embedding_cache_key'],again[0]['embedding_cache_key'])
        tables[0]['description']='changed metadata'
        changed=retrieve('bike',tables,self.root,encoder=encoder)
        self.assertFalse(next(r for r in changed if r['table_id']=='b')['cache_hit'])
        (self.root/'table.csv').write_text((self.root/'table.csv').read_text()+'2011-12-30,1,3\n')
        self.assertFalse(retrieve('bike',tables,self.root,encoder=encoder)[0]['cache_hit'])
        with patch('intention_grounding.semantic_retrieval.SERIALIZATION','different-version'):
            self.assertFalse(retrieve('bike',tables,self.root,encoder=encoder)[0]['cache_hit'])
        encoder.revision='new-revision'
        self.assertFalse(retrieve('bike',tables,self.root,encoder=encoder)[0]['cache_hit'])

    def test_gold_isolation_and_explicit_model_failure(self):
        a=self.execute(encoder=FakeEncoder())
        (self.root/'judgments.json').write_text('{"fixture":"not useful"}')
        b=self.execute(encoder=FakeEncoder())
        self.assertEqual(a['ranking'][0]['overall_state'],b['ranking'][0]['overall_state'])
        self.assertEqual(a['ranking'][0]['retrieval_score'],b['ranking'][0]['retrieval_score'])
        with patch('intention_grounding.semantic_retrieval.SBERT',side_effect=RuntimeError('SBERT_UNAVAILABLE: test')):
            failure=self.execute()
        self.assertEqual('failed',failure['status']);self.assertEqual([],failure['ranking'])

    def test_provider_failure_cache_and_no_live_without_budget(self):
        class Failing:
            metadata={'provider':'mock'}
            def invoke(self,*args):raise RuntimeError('secret must never leak')
        failure=run_text(DIRECT,input_id='test',provider=Failing(),root=self.root)
        self.assertEqual('INTERPRETER_PROVIDER_FAILURE',failure['failure']);self.assertNotIn('secret',json.dumps(failure))
        class Live:
            metadata={'provider':'groq','model':'test-model'}
            def invoke(self,*args):raise AssertionError('No live calls allowed')
        with self.assertRaisesRegex(ValueError,'NO_APPROVED_SPENDING_BUDGET'):
            interpret_input(DIRECT,'test',provider=Live(),cache_dir=self.root/'responses')
        provider=ReplayProvider(json.dumps(mock_document()))
        first=interpret_input(DIRECT,'test',provider=provider,cache_dir=self.root/'responses')
        with patch.object(provider,'invoke',side_effect=AssertionError('cache must be reused')):
            second=interpret_input(DIRECT,'test',provider=provider,cache_dir=self.root/'responses')
        self.assertFalse(first['execution']['response_cache_hit']);self.assertTrue(second['execution']['response_cache_hit'])


if __name__=='__main__':unittest.main()
