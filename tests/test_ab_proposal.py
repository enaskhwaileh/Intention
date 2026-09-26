"""Offline checks of declarative research fixtures, not executable grounding.

Run: python -m unittest discover -s tests -p test_ab_proposal.py -v
Manual condition annotations are inspected, never inferred from natural language.
"""
import copy
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1] / 'intention_grounding/docs/ab_proposal'
GRID_RULE = 'derive_explicit_group_time_grid_v1'
CONDITIONS = {'groups', 'time_domain', 'time_grain', 'exhaustive_coverage', 'all_groups_scope'}


def require(value, message):
    if not value:
        raise ValueError(message)


def walk(node):
    if isinstance(node, dict):
        yield node
        for value in node.values():
            yield from walk(value)
    elif isinstance(node, list):
        for value in node:
            yield from walk(value)


def check_grid_certificate(certificate, action, evidence):
    """Validate a manually supplied certificate; never derive a coverage policy."""
    require(certificate.get('source') == 'grounding_derivation', 'coverage is a derivation')
    require(certificate.get('rule_id') == GRID_RULE, 'coverage rule')
    require('normalization_rule' not in certificate, 'coverage is not normalization')
    require(certificate.get('binding_refs') == {
        'groups': 'groups', 'time_domain': 'time_points', 'time_grain': 'time_grain'}, 'binding refs')
    reviewed = certificate.get('reviewed_conditions', {})
    require(set(reviewed) == CONDITIONS and all(v is True for v in reviewed.values()), 'unresolved activation')
    refs = certificate.get('evidence_refs', {})
    require(set(refs) == CONDITIONS, 'required evidence categories')
    for values in refs.values():
        require(isinstance(values, list) and values and all(v in evidence for v in values), 'required evidence refs')
    bindings = action['bindings']
    require(len(set(bindings.get('groups', []))) >= 2, 'resolved groups')
    require(bool(bindings.get('time_points')) and bool(bindings.get('time_grain')), 'resolved temporal domain')


def check_proposal(ab, examples):
    actions, predicates, templates = ab['actions'], ab['predicates'], ab['requirement_templates']
    roles = ab['roles']
    for name, action in actions.items():
        seen = {name}
        parent = action['parent']
        while parent is not None:
            require(parent in actions and parent not in seen, 'invalid/cyclic parent')
            seen.add(parent)
            parent = actions[parent]['parent']
        require(set(action['required_roles']) <= roles.keys(), 'action roles')
        require(set(action['requirements']) <= templates.keys(), 'template refs')
    for predicate in predicates.values():
        require(predicate['axis'] in ab['axes'], 'predicate axis')
        require(set(predicate['argument_roles']) <= roles.keys(), 'predicate roles')
    for template in templates.values():
        require(template['predicate'] in predicates, 'predicate ref')
        require(template['axis'] == predicates[template['predicate']]['axis'], 'template axis')
        require(set(template['bind_present_roles']) <= roles.keys(), 'template roles')

    rule = ab['grounding_rules'][GRID_RULE]
    require(rule['stage'] == 'grounding' and rule['version'] == 1, 'rule stage/version')
    require(rule['kind'] == 'request_specific_coverage_derivation', 'rule kind')
    require(set(rule['inputs']) == {'groups', 'time_domain', 'time_grain', 'coverage_expression', 'coverage_scope'}, 'rule inputs')
    require(rule['activation']['operator'] == 'all_of', 'all conditions required')
    require(set(rule['activation']['conditions']) == CONDITIONS, 'activation conditions')
    require(all(isinstance(v, str) and v for v in rule['activation']['conditions'].values()), 'condition semantics')
    require(set(rule['required_evidence']) == CONDITIONS, 'rule evidence contract')
    require(rule['output'] == {'role': 'coverage_policy', 'value': 'complete_grid'}, 'rule output')
    require(rule['provenance']['source'] == 'grounding_derivation', 'rule provenance')
    require(set(rule['provenance']['required']) == {'rule_id', 'binding_refs', 'evidence_refs', 'reviewed_conditions'}, 'provenance fields')
    require(bool(rule['on_unresolved']) and bool(rule['limitations']), 'rule limitations')
    require(templates['complete_requested_grid']['activation'] == {
        'coverage_policy': 'complete_grid', 'derivation_rule_id': GRID_RULE}, 'template activation')
    require(ab['system_policies']['default_available_observations_v1']['source'] == 'system_policy', 'default origin')
    require(ab['system_policies']['default_available_observations_v1']['output'] == {
        'role': 'coverage_policy', 'value': 'available_observations'}, 'default output')
    normalization = examples['normalization_rules']
    require(GRID_RULE not in normalization and 'default_available_observations_v1' not in normalization, 'rule separation')
    registry = set(ab['grounding_rules']) | set(ab['system_policies'])
    for node in walk([ab, examples]):
        for field in ('rule_id', 'default_rule_id', 'derivation_rule_id'):
            if field in node:
                require(node[field] in registry, 'rule reference')
        if 'normalization_rule' in node:
            require(node['normalization_rule'] in normalization, 'normalization reference')
    for example in examples['examples']:
        evidence = example.get('evidence', {})
        for node in walk(example):
            if 'span' in node:
                start, end = node['span']
                require(type(start) is int and type(end) is int and 0 <= start < end <= len(example['input']), 'span bounds')
                require(example['input'][start:end] == node['text'], 'span text')
            if 'evidence_refs' in node:
                refs = node['evidence_refs']
                groups = refs.values() if isinstance(refs, dict) else [refs]
                for group in groups:
                    require(isinstance(group, list) and group and all(r in evidence for r in group), 'evidence reference')
        card = example['card']
        instances = {a['instance_id']: a for a in card['actions']}
        for action in instances.values():
            require(action['action_id'] in actions, 'action ref')
            policy = action['bindings']['coverage_policy']
            certificate = action['binding_evidence']['coverage_policy']
            if policy == 'complete_grid':
                check_grid_certificate(certificate, action, evidence)
                literal = action['extracted_coverage_expression']
                require(literal['normalization_rule'] == 'fixture_literal_v1', 'literal extraction rule')
                require(all(evidence[r]['text'] == literal['literal'] for r in literal['evidence_refs']), 'literal coverage')
                require(literal['evidence_refs'] == certificate['evidence_refs']['exhaustive_coverage'], 'coverage source link')
            else:
                require(policy == 'available_observations' and certificate == {
                    'source': 'system_policy', 'rule_id': 'default_available_observations_v1'}, 'system default provenance')
        ids = {r['id'] for r in card['requirements']}
        require(len(ids) == len(card['requirements']), 'duplicate requirement')
        require(set(card['requirement_logic']['all_of']) == ids, 'logic refs')
        for requirement in card['requirements']:
            origin = requirement['origin']
            require(requirement['predicate'] in predicates, 'card predicate')
            require(origin['template_id'] in templates and origin['action_id'] in actions, 'origin refs')
            require(requirement['predicate'] == templates[origin['template_id']]['predicate'], 'origin predicate')
            require(requirement['action_instance'] in instances, 'instance ref')
            action = instances[requirement['action_instance']]
            for role, provenance in origin['binding_evidence'].items():
                require(provenance == action['binding_evidence'][role], 'propagated binding evidence')
            if requirement['id'] == 'complete_requested_grid':
                require(action['bindings']['coverage_policy'] == 'complete_grid', 'grid policy')
                require(origin['coverage_derivation'] == action['binding_evidence']['coverage_policy'], 'propagated derivation')
        require(('complete_requested_grid' in ids) == any(a['bindings']['coverage_policy'] == 'complete_grid' for a in instances.values()), 'grid activation')
    for case in examples['non_grounded_cases']:
        if 'candidate_action' in case:
            require(case['candidate_action'] in actions, 'candidate ref')
    for case in examples['coverage_review_cases']:
        reviewed = case['reviewed_conditions']
        require(set(reviewed) == CONDITIONS and all(type(v) is bool for v in reviewed.values()), 'negative condition structure')
        require(not all(reviewed.values()) and case['expected_derivation'] is None, 'underspecified coverage must not activate')


class ProposalTests(unittest.TestCase):
    def setUp(self):
        self.ab = json.loads((ROOT / 'action-base-v0.1.json').read_text())
        self.examples = json.loads((ROOT / 'grounded-card-examples-v0.1.json').read_text())

    def test_proposal_consistency(self):
        check_proposal(self.ab, self.examples)

    def test_reject_missing_evidence_and_unresolved_conditions(self):
        for condition in CONDITIONS:
            for field in ('evidence_refs', 'reviewed_conditions'):
                with self.subTest(condition=condition, field=field):
                    examples = copy.deepcopy(self.examples)
                    certificate = examples['examples'][1]['card']['actions'][0]['binding_evidence']['coverage_policy']
                    if field == 'evidence_refs':
                        certificate[field].pop(condition)
                    else:
                        certificate[field][condition] = False
                    with self.assertRaises(ValueError):
                        check_proposal(self.ab, examples)

    def test_negative_cases_and_explicit_positive_evidence(self):
        cases = {c['id']: c for c in self.examples['coverage_review_cases']}
        self.assertEqual({'every_year_alone', 'annual_only', 'range_only', 'missing_group_scope', 'unresolved_between'}, set(cases))
        self.assertFalse(cases['every_year_alone']['reviewed_conditions']['time_domain'])
        self.assertFalse(cases['annual_only']['reviewed_conditions']['exhaustive_coverage'])
        self.assertFalse(cases['range_only']['reviewed_conditions']['time_grain'])
        self.assertFalse(cases['missing_group_scope']['reviewed_conditions']['all_groups_scope'])
        positive = self.examples['examples'][1]
        self.assertEqual('each of France and Spain in every year', positive['evidence']['all_groups_scope']['text'])
        self.assertEqual('from 2019 to 2021 inclusive', positive['evidence']['time_domain']['text'])
        for case in self.examples['non_grounded_cases']:
            if 'between 2019 and 2021' in case['input']:
                self.assertEqual('ambiguous', case['status'])
                self.assertIn('time_grain', case['missing_roles'])

    def test_reject_bad_references_spans_and_legacy_coverage_rule(self):
        mutations = [
            lambda a, e: a['actions']['compare'].update(parent='missing'),
            lambda a, e: a['actions']['compare'].update(parent='compare.groups'),
            lambda a, e: a['actions']['compare']['requirements'].append('missing'),
            lambda a, e: a['requirement_templates']['time_coverage'].update(predicate='missing'),
            lambda a, e: e['examples'][1]['evidence']['groups'].update(span=[0, 2]),
            lambda a, e: e['examples'][1]['card']['actions'][0]['binding_evidence']['coverage_policy'].update(rule_id='fixture_literal_v1'),
        ]
        for mutate in mutations:
            ab, examples = copy.deepcopy(self.ab), copy.deepcopy(self.examples)
            mutate(ab, examples)
            with self.assertRaises(ValueError):
                check_proposal(ab, examples)


if __name__ == '__main__':
    unittest.main()
