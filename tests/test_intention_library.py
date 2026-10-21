"""Library integrity and semantic boundaries; no model calls or usefulness claims."""
import contextlib
import copy
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from intention_grounding.action_base import (
    ActionBaseError, CANONICAL_AB_PATH, LEGACY_AB_PATH, describe_intention,
    is_groundable, list_intentions, load_action_base, validate_action_base,
)
from intention_grounding.cli import _offline_inputs, main
from intention_grounding.grounder import ReplayGrounderProvider, ground
from intention_grounding.interpreter.core import interpret


class IntentionLibraryTests(unittest.TestCase):
    def setUp(self):
        self.ab = load_action_base()

    def requirements(self, action_id):
        return set().union(*(set(p['requirement_logic']['all_of'])
                             for p in describe_intention(action_id, self.ab)['procedures']))

    def test_named_families_and_prediction_tasks_are_present(self):
        for family in ('compare', 'retrieve', 'summarize', 'aggregate', 'associate',
                       'predict', 'cluster', 'detect', 'explain', 'test', 'estimate',
                       'monitor', 'integrate', 'prepare', 'validate', 'visualize',
                       'recommend', 'optimize', 'simulate', 'spatial', 'network',
                       'text', 'discover'):
            with self.subTest(family=family):
                self.assertTrue(self.ab['actions'][family]['abstract'])
                self.assertTrue(describe_intention(family, self.ab)['children'])
        for task in ('classification', 'regression', 'forecasting', 'survival'):
            self.assertFalse(self.ab['actions']['predict.' + task]['abstract'])
        self.assertFalse(self.ab['exhaustive'])

    def test_supervised_prediction_does_not_require_time_series(self):
        for action in ('predict.classification', 'predict.regression'):
            for procedure in describe_intention(action, self.ab)['procedures']:
                self.assertNotIn('time_axis', procedure['required_roles'])
                self.assertNotIn('time_grain', procedure['required_roles'])
                self.assertIn('prediction_time', procedure['required_roles'])
                self.assertIn('feature_availability', procedure['requirement_logic']['all_of'])
                self.assertIn('leakage_control', procedure['requirement_logic']['all_of'])
        self.assertIn('categorical_target', self.requirements('predict.classification'))
        self.assertIn('numeric_target', self.requirements('predict.regression'))

    def test_forecast_alternatives_keep_distinct_requirements(self):
        procedures = {p['procedure_id']: p for p in describe_intention('predict.forecasting', self.ab)['procedures']}
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
        legacy = load_action_base(LEGACY_AB_PATH, expected_version='0.1.0-draft')
        for aid, old in legacy['actions'].items():
            for key, value in old.items():
                self.assertEqual(value, self.ab['actions'][aid][key], (aid, key))
        for key in ('grounding_rules', 'system_policies'):
            self.assertEqual(legacy[key], self.ab[key])
        for rid, template in legacy['requirement_templates'].items():
            self.assertEqual(template, self.ab['requirement_templates'][rid])
        self.assertNotIn('aggregation_valid', self.requirements('compare.time'))
        self.assertNotIn('procedure_assumptions', self.requirements('compare.time'))
        self.assertNotEqual(CANONICAL_AB_PATH, LEGACY_AB_PATH)

    def test_multi_table_and_model_evidence_not_single_table_claims(self):
        for action in ('integrate.join','integrate.union','integrate.entity_resolution','discover.compatible'):
            for proc in describe_intention(action, self.ab)['procedures']:
                self.assertEqual('table_set', proc['input_scope'])
        for action in ('explain.model','simulate.scenario'):
            for proc in describe_intention(action, self.ab)['procedures']:
                self.assertEqual('model_and_table', proc['input_scope'])

    def test_inspection_resolves_evidence_contracts_without_mutation(self):
        before = copy.deepcopy(self.ab)
        for aid, action in self.ab['actions'].items():
            for procedure in describe_intention(aid, self.ab)['procedures']:
                reqs = procedure['requirement_templates']
                self.assertEqual(set(reqs), set(procedure['requirement_logic']['all_of']))
                for template in reqs.values():
                    self.assertIn('evidence_contract', procedure['predicate_definitions'][template['predicate']])
        result = describe_intention('predict.classification', self.ab)
        result['procedures'][0]['requirement_templates'].clear()
        self.assertEqual(before, self.ab)

    def test_bad_references_and_capability_escalation_are_rejected(self):
        mutations = [
            lambda ab: ab['actions']['predict'].update(parent='predict.classification'),
            lambda ab: ab['actions']['predict.classification']['required_roles'].append('invented'),
            lambda ab: ab['actions']['predict.classification']['procedure_ids'].append('invented'),
            lambda ab: ab['procedures']['predict.classification.linear_classifier'].update(action_id='predict.regression'),
            lambda ab: ab['procedures']['predict.classification.linear_classifier']['additional_requirements'].append('invented'),
            lambda ab: ab['procedures']['predict.classification.linear_classifier'].update(runtime_support='grounding_only'),
            lambda ab: ab['runtime_policy']['groundable_action_ids'].append('predict.classification'),
            lambda ab: ab['verdict_contract'].update(missing_evidence='supported'),
            lambda ab: ab['verdict_contract'].update(gold_access='allowed'),
            lambda ab: ab['composition_policy'].update(competing_interpretations='any_of'),
            lambda ab: ab.update(exhaustive=True),
            lambda ab: ab['predicates']['causal_identification']['evidence_contract'].pop('unresolved'),
        ]
        for index, mutate in enumerate(mutations):
            with self.subTest(index=index):
                ab=copy.deepcopy(self.ab); mutate(ab)
                with self.assertRaises(ActionBaseError): validate_action_base(ab)

    def test_malformed_catalog_types_have_controlled_errors(self):
        for mutate in (lambda ab: ab.update(actions=[]),
                       lambda ab: ab['actions']['predict'].update(parent=[]),
                       lambda ab: ab['actions']['predict'].update(required_roles=[{}]),
                       lambda ab: ab.update(procedures=[])):
            ab=copy.deepcopy(self.ab); mutate(ab)
            with self.assertRaises(ActionBaseError): validate_action_base(ab)

    def test_runtime_boundary_for_every_concrete_catalog_action(self):
        input_id, text, ip, gp = _offline_inputs()
        interpreted = interpret(input_id, text, ip)
        proposal=json.loads(gp.raw_response)
        for aid, action in self.ab['actions'].items():
            if action['abstract'] or is_groundable(aid, self.ab): continue
            with self.subTest(action=aid):
                candidate={**proposal,'action_id':aid}
                result=ground(interpreted,self.ab,ReplayGrounderProvider(json.dumps(candidate)),run_id='boundary')
                self.assertEqual('unsupported',result['status'])
                self.assertEqual(['ACTION_CATALOG_ONLY'],result['reasons'])
                self.assertIsNone(result['grounded_card'])

    def test_abstract_and_malformed_model_ids_fail_safely(self):
        input_id,text,ip,gp=_offline_inputs()
        interpreted=interpret(input_id,text,ip); proposal=json.loads(gp.raw_response)
        for aid in ('compare', [], {}):
            result=ground(interpreted,self.ab,ReplayGrounderProvider(json.dumps({**proposal,'action_id':aid})),run_id='bad-id')
            self.assertEqual('invalid_model_response',result['status'])
            self.assertIsNone(result['grounded_card'])

    def test_cli_inspection_is_offline_and_writes_no_run(self):
        with tempfile.TemporaryDirectory() as temp:
            output=Path(temp)/'unused'
            with patch('intention_grounding.cli.GroqProvider', side_effect=AssertionError('No provider allowed')):
                for args in (['--list-intentions'], ['--intention','predict.forecasting']):
                    stream=io.StringIO()
                    with contextlib.redirect_stdout(stream):
                        self.assertEqual(0,main(args+['--output',str(output)]))
                    self.assertEqual(self.ab['ab_version'],json.loads(stream.getvalue())['ab_version'])
            self.assertFalse(output.exists())
        stream=io.StringIO()
        with contextlib.redirect_stdout(stream):
            self.assertEqual(2,main(['--intention','invented']))
        self.assertEqual('library_error=UNKNOWN_ACTION_ID',stream.getvalue().strip())

    def test_offline_cli_can_still_use_frozen_legacy_catalog(self):
        for flag in ('--il', '--ab'):
            with self.subTest(flag=flag), tempfile.TemporaryDirectory() as temp, contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(0,main([flag,str(LEGACY_AB_PATH),'--output',temp]))
                run=next(Path(temp).iterdir())
                self.assertEqual('0.1.0-draft',json.loads((run/'run.json').read_text())['ab_version'])

    def test_no_legacy_statistical_minima_or_scoring_weights_imported(self):
        def walk(value):
            if isinstance(value,dict):
                for key,item in value.items():
                    self.assertNotIn(key,('min_rows','weights','confidence_threshold'))
                    walk(item)
            elif isinstance(value,list):
                for item in value: walk(item)
        walk(self.ab)
        self.assertIsNone(self.ab['scoring_policy'])
        self.assertFalse(self.ab['provenance']['empirically_validated'])


if __name__=='__main__':
    unittest.main()
