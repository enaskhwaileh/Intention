import copy
import importlib.resources
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, patch

from intention_grounding.interpreter.core import SCHEMA, VALIDATOR, interpret
from intention_grounding.interpreter.providers import GroqProvider, ReplayProvider, SYSTEM_PROMPT, list_available_models
from intention_grounding.provider_errors import provider_diagnostic

FIXTURES = json.loads(importlib.resources.files('intention_grounding.interpreter').joinpath('fixtures/replay.json').read_text())


class ContractTests(unittest.TestCase):
    def setUp(self):
        env_dir = tempfile.TemporaryDirectory()
        self.addCleanup(env_dir.cleanup)
        env_patch = patch('intention_grounding.groq_config.ENV_PATH', Path(env_dir.name) / '.env')
        env_patch.start()
        self.addCleanup(env_patch.stop)
        self.doc = json.loads(FIXTURES[0]['raw_response'])

    def run_doc(self, d):
        return interpret(d['input_id'], d['original_input'], ReplayProvider(json.dumps(d)))

    def reject(self, mutate, expected=None, doc=None):
        d = copy.deepcopy(doc or self.doc)
        mutate(d)
        result = self.run_doc(d)
        self.assertIsNone(result['interpretation'])
        self.assertTrue(result['failure'])
        if expected:
            self.assertEqual(expected, result['failure'])

    def test_schema_and_fixtures(self):
        VALIDATOR.check_schema(SCHEMA)
        for case in FIXTURES:
            with self.subTest(case=case['input_id']):
                result = interpret(case['input_id'], case['input'], ReplayProvider(case['raw_response']))
                self.assertEqual(case['expected'], result['failure'] or result['interpretation']['status'])
                self.assertEqual(case['raw_response'], result['raw_response'])
                self.assertNotIn('model', result['metadata'])

    def test_independent_semantic_expectations(self):
        docs = {c['input_id']:self.run_doc(json.loads(c['raw_response']))['interpretation'] for c in FIXTURES[:10]}
        def roles(name):
            return [(a['role'], a['value']['literal']) for a in docs[name]['intentions'][0]['arguments']]
        self.assertIn(('time_points','2021'), roles('groups_year'))
        self.assertNotIn('time_grain', [r for r,v in roles('groups_year')])
        self.assertEqual('  Compare income in France and Germany in 2021.  ', docs['groups_year']['original_input'])
        self.assertIn(('time_range','between 2019 and 2021'), roles('trajectories'))
        self.assertNotIn('time_points', [r for r,v in roles('trajectories')])
        self.assertEqual(['2019','2021'], [v for r,v in roles('observations') if r=='time_points'])
        self.assertEqual('unresolved_reference',docs['insufficient']['intentions'][0]['missing'][0]['reason'])
        self.assertEqual('joint', docs['joint']['relationships'][0]['kind'])
        self.assertEqual('accepted_alternatives', docs['alternatives']['relationships'][0]['kind'])
        self.assertEqual(2,len(docs['ambiguous']['intentions'][0]['candidates']))
        self.assertEqual([],docs['unsupported']['intentions'])
        goals=self.run_doc(json.loads(FIXTURES[-1]['raw_response']))['interpretation']
        self.assertEqual('ambiguous',goals['status'])
        self.assertEqual(1,len(goals['intentions']))
        self.assertEqual(['Contrast income across countries.','Summarize income separately for each country.'],[c['reading']['description'] for c in goals['intentions'][0]['candidates']])
        self.assertEqual('Forecast',docs['non_compare']['intentions'][0]['expression']['literal'])

    def test_unknown_fields_at_every_object_level(self):
        def paths(node, path=()):
            if isinstance(node,dict):
                yield path
                for k,v in node.items(): yield from paths(v,path+(k,))
            elif isinstance(node,list):
                for k,v in enumerate(node): yield from paths(v,path+(k,))
        doc=json.loads(FIXTURES[1]['raw_response'])
        for path in paths(doc):
            def mutate(d):
                for key in path: d=d[key]
                d['extra']=True
            with self.subTest(path=path): self.reject(mutate,'SCHEMA_VALIDATION',doc)
        self.reject(lambda d:d.update(schema_version='999'),'SCHEMA_VALIDATION')

    def test_prohibited_claim_fields(self):
        for key in ['confidence','table_requirements','suitability','ab_action_id','system_defaults']:
            self.reject(lambda d:d['intentions'][0].update({key:0.9}),'SCHEMA_VALIDATION')

    def test_spans_and_references(self):
        for start in [True, 0.0, -1, 10000, '2']:
            self.reject(lambda d:d['evidence'][0].update(start=start))
        self.reject(lambda d:d['evidence'][0].update(end=d['evidence'][0]['start']))
        self.reject(lambda d:d['evidence'][0].update(text='Germany'),'SPAN_TEXT_MISMATCH')
        self.reject(lambda d:d['intentions'][0]['expression'].update(evidence=['missing']),'UNRESOLVED_EVIDENCE')
        self.reject(lambda d:d['relationships'][0].update(evidence=['missing']),'UNRESOLVED_EVIDENCE')
        self.reject(lambda d:d['evidence'].append(d['evidence'][0]),'DUPLICATE_ID')
        self.reject(lambda d:d['intentions'][0]['expression'].update(literal='invented'),'LITERAL_MISMATCH')
        doc=json.loads(FIXTURES[9]['raw_response'])
        spans=[e for e in doc['evidence'] if e['text']=='café']
        self.assertEqual([10,20], [e['start'] for e in spans])
        self.reject(lambda d:d['evidence'][0].update(start=11),'SPAN_TEXT_MISMATCH',doc)
        self.reject(lambda d:d['evidence'][1].update(end=23),'SPAN_TEXT_MISMATCH',doc)

    def test_normalization(self):
        def normalize(d,rule,value):
            v=d['intentions'][0]['expression']
            v['normalized']={'rule_id':rule,'value':value,'evidence':v['evidence']}
        d=copy.deepcopy(self.doc);normalize(d,'casefold-v1','compare')
        self.assertIsNone(self.run_doc(d)['failure'])
        self.reject(lambda d:normalize(d,'unknown','compare'),'SCHEMA_VALIDATION')
        self.reject(lambda d:normalize(d,'casefold-v1','forecast'),'INVALID_NORMALIZATION')
        self.reject(lambda d:normalize(d,'annual-v1','year'),'INVALID_NORMALIZATION')
        self.reject(lambda d:d['intentions'][0]['expression'].update(normalized={'value':'compare'}),'SCHEMA_VALIDATION')
        self.reject(lambda d:d['intentions'][0]['expression']['normalized'].update(evidence=['missing']), 'UNRESOLVED_EVIDENCE',d)

    def test_status_relationship_consistency(self):
        self.reject(lambda d:d.update(status='ambiguous'),'STATUS_CONFLICT')
        self.reject(lambda d:d.update(status='unsupported'),'STATUS_CONFLICT')
        self.reject(lambda d:d.update(status='insufficient'),'STATUS_CONFLICT')
        self.reject(lambda d:d['relationships'].append(d['relationships'][0]),'RELATIONSHIP_CONFLICT')
        self.reject(lambda d:d.update(relationships=[]),'RELATIONSHIP_COVERAGE')
        self.reject(lambda d:d['relationships'][0].update(members=['absent']),'RELATIONSHIP_MEMBERS')
        self.reject(lambda d:d['relationships'][0].update(kind='joint'),'RELATIONSHIP_MEMBERS')
        ambiguous=json.loads(FIXTURES[6]['raw_response'])
        self.reject(lambda d:d.update(status='unambiguous'),'STATUS_CONFLICT',ambiguous)
        self.reject(lambda d:d['relationships'].pop(),'AMBIGUITY_REQUIRED',ambiguous)

    def test_execution_failures(self):
        for raw in ['{','{"x":1,"x":2}','NaN','```json\n{}\n```']:
            self.assertEqual('MALFORMED_JSON',interpret('x','text',ReplayProvider(raw))['failure'])
        for value in [None,'','  ',[],17]:
            self.assertEqual('INVALID_INPUT',interpret('x',value,ReplayProvider('{}'))['failure'])
        provider=MagicMock();provider.metadata={};provider.invoke.side_effect=RuntimeError('SECRET')
        result=interpret('x','text',provider)
        self.assertEqual('PROVIDER_FAILURE',result['failure'])
        self.assertNotIn('SECRET',json.dumps(result))
        self.assertIsNone(result['raw_response'])
        self.assertEqual('INPUT_MISMATCH',interpret('wrong',self.doc['original_input'],ReplayProvider(json.dumps(self.doc)))['failure'])

    def test_legacy_boundary(self):
        from intention_grounding.legacy.reader import read_interpretation_v1
        old = json.loads((Path(__file__).resolve().parents[1] / 'intention_grounding/legacy/interpreter-v1.json').read_text())[0]
        migrated = read_interpretation_v1(json.loads(old['raw_response']))
        self.assertIsNone(self.run_doc(migrated)['failure'])

    def test_mocked_groq(self):
        factory=MagicMock()
        client=factory.return_value.__enter__.return_value
        client.chat.completions.create.return_value.choices[0].message.content=json.dumps(self.doc)
        provider=GroqProvider(model='explicit-test-model',client_factory=factory)
        with patch.dict(os.environ,{'GROQ_API_KEY':'fake-key'}):
            result=interpret(self.doc['input_id'],self.doc['original_input'],provider)
        self.assertIsNone(result['failure'])
        factory.assert_called_once_with(api_key='fake-key',timeout=30.0,max_retries=0)
        kwargs=client.chat.completions.create.call_args.kwargs
        self.assertEqual('explicit-test-model',kwargs['model'])
        self.assertEqual(0.0,kwargs['temperature'])
        self.assertEqual(SYSTEM_PROMPT,kwargs['messages'][0]['content'])
        self.assertEqual(self.doc['original_input'],json.loads(kwargs['messages'][1]['content'])['original_input'])
        self.assertNotIn('fake-key',json.dumps(result))
        client.chat.completions.create.side_effect=RuntimeError('secret-provider-details')
        with patch.dict(os.environ,{'GROQ_API_KEY':'fake-key'}):
            self.assertEqual('PROVIDER_FAILURE',interpret('x','text',provider)['failure'])
        with patch.dict(os.environ,{},clear=True):
            self.assertEqual('PROVIDER_FAILURE',interpret('x','text',provider)['failure'])
        for kwargs in [{'model':''},{'model':'x','timeout':float('nan')},{'model':'x','max_retries':3}]:
            with self.assertRaises((ValueError, RuntimeError)):GroqProvider(**kwargs)

    def test_safe_provider_diagnostics_and_missing_configuration(self):
        class FakeStatusError(Exception):
            status_code = 401
            code = 'invalid_api_key'
            def __str__(self):
                return 'secret-value Authorization: Bearer secret-value'
        FakeStatusError.__module__ = 'groq._exceptions'
        factory = MagicMock()
        factory.return_value.__enter__.return_value.chat.completions.create.side_effect = FakeStatusError()
        provider = GroqProvider(model='explicit-test-model', client_factory=factory)
        with patch.dict(os.environ, {'GROQ_API_KEY': 'secret-value'}):
            result = interpret(self.doc['input_id'], self.doc['original_input'], provider)
        self.assertEqual('PROVIDER_FAILURE', result['failure'])
        self.assertEqual({'exception_type': 'ProviderError', 'http_status': 401,
                          'error_code': 'invalid_api_key'}, result['provider_error'])
        self.assertNotIn('secret-value', json.dumps(result))
        with patch.dict(os.environ, {}, clear=True):
            missing = interpret(self.doc['input_id'], self.doc['original_input'], provider)
        self.assertEqual({'exception_type': 'MissingGroqCredentialError',
                          'error_code': 'MISSING_GROQ_API_KEY'}, missing['provider_error'])
        self.assertEqual({'exception_type': 'ProviderError'},
                         provider_diagnostic(type('SecretKey', (Exception,), {})('secret-value')))

    def test_model_listing_is_ids_only_and_requires_key(self):
        from types import SimpleNamespace
        factory = MagicMock()
        factory.return_value.__enter__.return_value.models.list.return_value = SimpleNamespace(
            data=[SimpleNamespace(id='z-model'), SimpleNamespace(id='a/model')])
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(Exception):
                list_available_models(client_factory=factory)
        factory.assert_not_called()
        with patch.dict(os.environ, {'GROQ_API_KEY': 'secret-value'}):
            self.assertEqual(['a/model', 'z-model'], list_available_models(client_factory=factory))
        factory.assert_called_once_with(api_key='secret-value', timeout=30.0, max_retries=0)

    def test_no_optional_sdks_credentials_or_network(self):
        code='''
import sys, os, socket
class Block:
 def find_spec(self, fullname, *args):
  if fullname.split('.')[0] == 'groq': raise ImportError('blocked optional SDK')
sys.meta_path.insert(0,Block())
def audit(event,args):
 if event in {'socket.connect','socket.getaddrinfo'}: raise AssertionError('network forbidden')
sys.addaudithook(audit)
os.environ.pop('GROQ_API_KEY',None)
from intention_grounding.scripts.interpreter_production import interpret_query
from intention_grounding.interpreter.providers import ReplayProvider
assert interpret_query('text',input_id='x',provider=ReplayProvider('{'))['failure']=='MALFORMED_JSON'
import tempfile
from intention_grounding.interpreter.demo import main
with tempfile.TemporaryDirectory() as output:
 sys.argv=['demo','--output-root',output]
 assert main()==0
'''
        subprocess.run([sys.executable,'-c',code],check=True)


if __name__ == '__main__':
    unittest.main()
