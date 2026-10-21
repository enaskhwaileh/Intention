"""Parsing, closed schema validation, and deterministic provenance checks."""
import json
from importlib.resources import files

from jsonschema import Draft202012Validator

from ..provider_errors import provider_diagnostic

SCHEMA_VERSION = '2.0'
NORMALIZATION_VERSION = '1.0'
SCHEMA = json.loads(files(__package__).joinpath('schema.json').read_text())
VALIDATOR = Draft202012Validator(SCHEMA)


class ContractError(ValueError):
    """Deliberately contains only a safe diagnostic code."""


def require(condition, code):
    if not condition:
        raise ContractError(code)


def parse_response(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError('duplicate key')
            result[key] = value
        return result

    def constant(_):
        raise ValueError('non-JSON constant')

    try:
        return json.loads(raw, object_pairs_hook=pairs, parse_constant=constant)
    except (ValueError, TypeError, RecursionError):
        raise ContractError('MALFORMED_JSON') from None


def validate(document, input_id, original_input):
    require(not list(VALIDATOR.iter_errors(document)), 'SCHEMA_VALIDATION')
    require(document['input_id'] == input_id and document['original_input'] == original_input,
            'INPUT_MISMATCH')
    evidence = {}
    for item in document['evidence']:
        start, end = item['start'], item['end']
        require(type(start) is int and type(end) is int and
                0 <= start < end <= len(original_input), 'INVALID_SPAN')
        require(original_input[start:end] == item['text'], 'SPAN_TEXT_MISMATCH')
        require(item['id'] not in evidence, 'DUPLICATE_ID')
        evidence[item['id']] = item['text']

    def check_refs(refs):
        require(all(r in evidence for r in refs), 'UNRESOLVED_EVIDENCE')

    def walk(node):
        if isinstance(node, list):
            for child in node:
                walk(child)
        elif isinstance(node, dict):
            if isinstance(node.get('evidence'), list) and all(isinstance(r, str) for r in node['evidence']):
                check_refs(node['evidence'])
            if 'literal' in node:
                require(all(evidence[r] == node['literal'] for r in node['evidence']), 'LITERAL_MISMATCH')
                normalized = node['normalized']
                if normalized:
                    check_refs(normalized['evidence'])
                    require(normalized['evidence'] == node['evidence'], 'NORMALIZATION_SOURCE')
                    literal = node['literal']
                    if normalized['rule_id'] == 'casefold-v1':
                        expected = literal.casefold()
                    else:
                        expected = {'annual':'year', 'annually':'year', 'yearly':'year'}.get(literal.casefold())
                    require(expected is not None and normalized['value'] == expected, 'INVALID_NORMALIZATION')
            for child in node.values():
                walk(child)
    walk(document)
    intentions = {a['id']: a for a in document['intentions']}
    require(len(intentions) == len(document['intentions']), 'DUPLICATE_ID')
    candidates = {}
    for intention in intentions.values():
        for candidate in intention['candidates']:
            require(candidate['id'] not in candidates and candidate['id'] not in intentions, 'DUPLICATE_ID')
            candidates[candidate['id']] = intention['id']
    covered_intentions, covered_candidates = set(), set()
    competing = False
    for rel in document['relationships']:
        members = rel['members']
        require(len(set(members)) == len(members), 'RELATIONSHIP_MEMBERS')
        if rel['kind'] == 'competing_interpretations':
            require(len(members) >= 2 and all(m in candidates for m in members), 'RELATIONSHIP_MEMBERS')
            require(len({candidates[m] for m in members}) == 1, 'RELATIONSHIP_MEMBERS')
            covered_candidates.update(members)
            competing = True
        else:
            require(all(m in intentions for m in members), 'RELATIONSHIP_MEMBERS')
            require(len(members) == 1 if rel['kind'] == 'single' else len(members) >= 2,
                    'RELATIONSHIP_MEMBERS')
            require(not covered_intentions.intersection(members), 'RELATIONSHIP_CONFLICT')
            covered_intentions.update(members)
    require(covered_intentions == set(intentions), 'RELATIONSHIP_COVERAGE')
    for intention in intentions.values():
        if len(intention['candidates']) > 1:
            require(all(c['id'] in covered_candidates for c in intention['candidates']), 'AMBIGUITY_REQUIRED')
    status, codes = document['status'], set(document['diagnostics'])
    missing = [m for a in intentions.values() for m in a['missing']]
    require(status != 'unambiguous' or (bool(intentions) and not missing and not codes and not competing), 'STATUS_CONFLICT')
    require(status != 'ambiguous' or (competing and 'COMPETING_INTERPRETATIONS' in codes), 'STATUS_CONFLICT')
    require(not competing or status == 'ambiguous', 'STATUS_CONFLICT')
    require(status != 'insufficient' or (bool(missing) and bool(codes & {'MISSING_ARGUMENT','UNRESOLVED_REFERENCE'})), 'STATUS_CONFLICT')
    require(status != 'unsupported' or (not intentions and codes == {'OUT_OF_SCOPE'}), 'STATUS_CONFLICT')
    return document


def interpret(input_id, original_input, provider):
    """Return an execution envelope; interpretation status exists only on success."""
    result = {'metadata': {'schema_version': SCHEMA_VERSION,
                           'normalization_version': NORMALIZATION_VERSION},
              'raw_response': None, 'interpretation': None, 'failure': None,
              'provider_error': None}
    if not isinstance(input_id, str) or not input_id.strip() or not isinstance(original_input, str) or not original_input.strip():
        result['failure'] = 'INVALID_INPUT'
        return result
    try:
        result['metadata'].update(provider.metadata)
        raw = provider.invoke(input_id, original_input)
        result["metadata"].update(provider.metadata)
        if hasattr(provider,"actual_model"): result["metadata"]["actual_model"] = provider.actual_model
    except Exception as exc:
        result['failure'] = 'PROVIDER_FAILURE'
        result['provider_error'] = provider_diagnostic(exc)
        return result
    result['raw_response'] = raw if isinstance(raw, str) else None
    try:
        result['interpretation'] = validate(parse_response(raw), input_id, original_input)
    except ContractError as exc:
        result['failure'] = str(exc)
    return result


def interpret_structured(record):
    """Explicit author-supplied semantic representation; no natural-language inference."""
    from ..contracts import validate_request
    import copy
    validated = validate_request(copy.deepcopy(record))
    return {'schema_version':'1.0','input_mode':'authored_structured_request',
            'status':'validated','structured_intention_record':validated,
            'notice':'Semantic roles supplied by the author, not extracted by a live LLM; wording-to-role correctness requires review.'}
