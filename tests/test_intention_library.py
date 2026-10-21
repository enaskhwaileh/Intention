"""Library integrity and semantic boundaries; no model calls or usefulness claims."""
import contextlib
import copy
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from intention_grounding.intention_library import (
    IntentionLibraryError, CANONICAL_IL_PATH, LEGACY_IL_PATH, describe_intention,
    is_groundable, list_intentions, load_intention_library, validate_intention_library,
)
from intention_grounding.cli import _offline_inputs, main
from intention_grounding.grounder import ReplayGrounderProvider, ground
from intention_grounding.interpreter.core import interpret


class IntentionLibraryTests(unittest.TestCase):
    def setUp(self):
        self.il = load_intention_library()

    def requirements(self, intention_id):
        return set().union(*(set(p['requirement_logic']['all_of'])
                             for p in describe_intention(intention_id, self.il)['procedures']))

    def test_named_families_and_prediction_tasks_are_present(self):
        for family in ('compare', 'retrieve', 'summarize', 'aggregate', 'associate',
                       'predict', 'cluster', 'detect', 'explain', 'test', 'estimate',
                       'monitor', 'integrate', 'prepare', 'validate', 'visualize',
                       'recommend', 'optimize', 'simulate', 'spatial', 'network',
                       'text', 'discover'):
            with self.subTest(family=family):
                self.assertTrue(self.il['intentions'][family]['abstract'])
                self.assertTrue(describe_intention(family, self.il)['children'])
        for task in ('classification', 'regression', 'forecasting', 'survival'):
            self.assertFalse(self.il['intentions']['predict.' + task]['abstract'])
        self.assertFalse(self.il['exhaustive'])

    def test_supervised_prediction_does_not_require_time_series(self):
        for intention in ('predict.classification', 'predict.regression'):
            for procedure in describe_intention(intention, self.il)['procedures']:
                self.assertNotIn('time_axis', procedure['required_roles'])
                self.assertNotIn('time_grain', procedure['required_roles'])
                self.assertIn('prediction_time', procedure['required_roles'])
                self.assertIn('feature_availability', procedure['requirement_logic']['all_of'])
                self.assertIn('leakage_control', procedure['requirement_logic']['all_of'])
        self.assertIn('categorical_target', self.requirements('predict.classification'))
        self.assertIn('numeric_target', self.requirements('predict.regression'))

    def test_forecast_alternatives_keep_distinct_requirements(self):
        procedures = {p['procedure_id']: p for p in describe_intention('predict.forecasting', self.il)['procedures']}
        history = procedures['predict.forecasting.univariate']
        covariates = procedures['predict.forecasting.with_covariates']
        for proc in (history, covariates):
            self.assertTrue({'time_axis','time_grain','horizon','prediction_time'} <= set(proc['required_roles']))
            self.assertIn('temporal_observations', proc['requirement_logic']['all_of'])
        self.assertNotIn('features', history['required_roles'])
        self.assertNotIn('feature_availability', history['requirement_logic']['all_of'])
        self.assertIn('features', covariates['required_roles'])
        self.assertIn('feature_availability', covariates['requirement_logic']['all_of'])
        self.assertIn('event_followup', self.requirements('predict.survival'))

    def test_causal_model_and_association_explanations_are_distinct(self):
        self.assertNotIn('causal_identification', self.requirements('explain.association'))
        self.assertNotIn('causal_identification', self.requirements('explain.model'))
        self.assertIn('model_available', self.requirements('explain.model'))
        self.assertIn('causal_identification', self.requirements('explain.causal'))
        self.assertNotIn('target_observed', self.requirements('associate.correlation'))
        self.assertIn('numeric_variables', self.requirements('associate.correlation'))

    def test_compare_contract_and_legacy_loading_preserved(self):
        from intention_grounding.legacy.reader import read_library
        legacy = read_library(LEGACY_IL_PATH)
        for aid, old in legacy['intentions'].items():
            for key, value in old.items():
                self.assertEqual(value, self.il['intentions'][aid][key], (aid, key))
        for key in ('grounding_rules', 'system_policies'):
            self.assertEqual(legacy[key], self.il[key])
        for rid, template in legacy['requirement_templates'].items():
            self.assertEqual(template, self.il['requirement_templates'][rid])
        self.assertNotIn('aggregation_valid', self.requirements('compare.time'))
        self.assertNotIn('procedure_assumptions', self.requirements('compare.time'))
        self.assertNotEqual(CANONICAL_IL_PATH, LEGACY_IL_PATH)

    def test_multi_table_and_model_evidence_not_single_table_claims(self):
        for intention in ('integrate.join','integrate.union','integrate.entity_resolution','discover.compatible'):
            for proc in describe_intention(intention, self.il)['procedures']:
                self.assertEqual('table_set', proc['input_scope'])
        for intention in ('explain.model','simulate.scenario'):
            for proc in describe_intention(intention, self.il)['procedures']:
                self.assertEqual('model_and_table', proc['input_scope'])

    def test_inspection_resolves_evidence_contracts_without_mutation(self):
        before = copy.deepcopy(self.il)
        for aid, intention in self.il['intentions'].items():
            for procedure in describe_intention(aid, self.il)['procedures']:
                reqs = procedure['requirement_templates']
                self.assertEqual(set(reqs), set(procedure['requirement_logic']['all_of']))
                for template in reqs.values():
                    self.assertIn('evidence_contract', procedure['predicate_definitions'][template['predicate']])
        result = describe_intention('predict.classification', self.il)
        result['procedures'][0]['requirement_templates'].clear()
        self.assertEqual(before, self.il)

    def test_bad_references_and_capability_escalation_are_rejected(self):
        mutations = [
            lambda il: il['intentions']['predict'].update(parent='predict.classification'),
            lambda il: il['intentions']['predict.classification']['required_roles'].append('invented'),
            lambda il: il['intentions']['predict.classification']['procedure_ids'].append('invented'),
            lambda il: il['procedures']['predict.classification.linear_classifier'].update(intention_id='predict.regression'),
            lambda il: il['procedures']['predict.classification.linear_classifier']['additional_requirements'].append('invented'),
            lambda il: il['procedures']['predict.classification.linear_classifier'].update(runtime_support='grounding_only'),
            lambda il: il['runtime_policy']['groundable_intention_ids'].append('predict.classification'),
            lambda il: il['verdict_contract'].update(missing_evidence='supported'),
            lambda il: il['verdict_contract'].update(gold_access='allowed'),
            lambda il: il['composition_policy'].update(competing_interpretations='any_of'),
            lambda il: il.update(exhaustive=True),
            lambda il: il['predicates']['causal_identification']['evidence_contract'].pop('unresolved'),
        ]
        for index, mutate in enumerate(mutations):
            with self.subTest(index=index):
                il=copy.deepcopy(self.il); mutate(il)
                with self.assertRaises(IntentionLibraryError): validate_intention_library(il)

    def test_malformed_catalog_types_have_controlled_errors(self):
        for mutate in (lambda il: il.update(intentions=[]),
                       lambda il: il['intentions']['predict'].update(parent=[]),
                       lambda il: il['intentions']['predict'].update(required_roles=[{}]),
                       lambda il: il.update(procedures=[])):
            il=copy.deepcopy(self.il); mutate(il)
            with self.assertRaises(IntentionLibraryError): validate_intention_library(il)

    def test_runtime_boundary_for_every_concrete_catalog_action(self):
        input_id, text, ip, gp = _offline_inputs()
        interpreted = interpret(input_id, text, ip)
        proposal=json.loads(gp.raw_response)
        for aid, intention in self.il['intentions'].items():
            if intention['abstract'] or is_groundable(aid, self.il): continue
            with self.subTest(intention=aid):
                candidate={**proposal,'intention_id':aid}
                result=ground(interpreted,self.il,ReplayGrounderProvider(json.dumps(candidate)),run_id='boundary')
                self.assertEqual('unsupported',result['status'])
                self.assertEqual(['INTENTION_CATALOG_ONLY'],result['reasons'])
                self.assertIsNone(result['grounded_intention'])

    def test_abstract_and_malformed_model_ids_fail_safely(self):
        input_id,text,ip,gp=_offline_inputs()
        interpreted=interpret(input_id,text,ip); proposal=json.loads(gp.raw_response)
        for aid in ('compare', [], {}):
            result=ground(interpreted,self.il,ReplayGrounderProvider(json.dumps({**proposal,'intention_id':aid})),run_id='bad-id')
            self.assertEqual('invalid_model_response',result['status'])
            self.assertIsNone(result['grounded_intention'])

    def test_cli_inspection_is_offline_and_writes_no_run(self):
        with tempfile.TemporaryDirectory() as temp:
            output=Path(temp)/'unused'
            with patch('intention_grounding.cli.GroqProvider', side_effect=AssertionError('No provider allowed')):
                for args in (['--list-intentions'], ['--intention','predict.forecasting']):
                    stream=io.StringIO()
                    with contextlib.redirect_stdout(stream):
                        self.assertEqual(0,main(args+['--output',str(output)]))
                    self.assertEqual(self.il['il_version'],json.loads(stream.getvalue())['il_version'])
            self.assertFalse(output.exists())
        stream=io.StringIO()
        with contextlib.redirect_stdout(stream):
            self.assertEqual(2,main(['--intention','invented']))
        self.assertEqual('library_error=UNKNOWN_INTENTION_ID',stream.getvalue().strip())

    def test_frozen_library_requires_explicit_legacy_reader(self):
        from intention_grounding.legacy.reader import read_library
        self.assertEqual('0.1.0-draft', read_library(LEGACY_IL_PATH)['il_version'])
        with self.assertRaises(IntentionLibraryError):
            load_intention_library(LEGACY_IL_PATH)

    def test_no_legacy_statistical_minima_or_scoring_weights_imported(self):
        def walk(value):
            if isinstance(value,dict):
                for key,item in value.items():
                    self.assertNotIn(key,('min_rows','weights','confidence_threshold'))
                    walk(item)
            elif isinstance(value,list):
                for item in value: walk(item)
        walk(self.il)
        self.assertIsNone(self.il['scoring_policy'])
        self.assertFalse(self.il['provenance']['empirically_validated'])


if __name__=='__main__':
    unittest.main()
