"""Versioned, closed public request contracts and corpus integrity checks."""
from datetime import date
import json
from pathlib import Path
from jsonschema import Draft202012Validator
from .profiler import sha256

SCHEMAS = Path(__file__).parent / 'schemas'


def validate(kind, value):
    schema = json.loads((SCHEMAS / (kind + '.json')).read_text())
    errors = list(Draft202012Validator(schema).iter_errors(value))
    if errors:
        raise ValueError('INVALID_' + kind.upper() + '_CONTRACT')
    return value


def validate_request(value):
    validate('request', value)
    if value['status'] == 'ready' and value['intention_type'] == 'compare':
        roles = value['roles']
        required = {'population','measure_concept','unit','grain','group_role','groups','period','statistic'}
        if not required <= roles.keys() or len(set(roles['groups'])) < 2:
            raise ValueError('MISSING_COMPARE_ROLES')
        start,end=map(date.fromisoformat,roles['period'])
        if start>end: raise ValueError('INVALID_PERIOD')
    return value


def load_corpus(path, root):
    corpus = validate('corpus', json.loads(Path(path).read_text()))
    ids = [t['table_id'] for t in corpus['tables']]
    if len(ids) != len(set(ids)):
        raise ValueError('DUPLICATE_TABLE_ID')
    for table in corpus['tables']:
        data = (Path(root) / table['path']).resolve()
        if not data.is_relative_to(Path(root).resolve()) or not data.is_file():
            raise ValueError('CORPUS_FILE_MISSING_OR_OUTSIDE_ROOT')
        if sha256(data) != table['normalized_sha256']:
            raise ValueError('CORPUS_HASH_MISMATCH')
        # Semantic facts require their retained source document to match its recorded bytes.
        doc = table.get('semantics',{}).get('source_document')
        if doc:
            source=(Path(root)/doc['path']).resolve()
            if not source.is_relative_to(Path(root).resolve()) or not source.is_file() or sha256(source)!=doc['sha256']:
                raise ValueError('DOCUMENTATION_HASH_MISMATCH')
    return corpus


def validate_splits(split, corpus, requests):
    validate('splits', split)
    table_map={t['table_id']:t for t in corpus['tables']}
    request_map={r['request_id']:r for r in requests}
    seen_tables,seen_requests,seen_topics,seen_families=set(),set(),set(),set()
    for name,part in split['partitions'].items():
        tids,rids=part['table_ids'],part['request_ids']
        if len(tids)!=len(set(tids)) or len(rids)!=len(set(rids)):
            raise ValueError('DUPLICATE_SPLIT_ID')
        if not set(tids)<=table_map.keys() or not set(rids)<=request_map.keys():
            raise ValueError('UNKNOWN_SPLIT_ID')
        topics={table_map[t]['topic'] for t in tids}|{request_map[r]['topic'] for r in rids}
        families={table_map[t]['source_family'] for t in tids}
        if seen_tables.intersection(tids) or seen_requests.intersection(rids) or seen_topics & topics or seen_families & families:
            raise ValueError('SPLIT_LEAKAGE')
        seen_tables.update(tids);seen_requests.update(rids);seen_topics.update(topics);seen_families.update(families)
    if split['designation']=='development_only' and set(split['partitions'])!={'development'}:
        raise ValueError('DEVELOPMENT_ONLY_HAS_HOLDOUT')
    return split
