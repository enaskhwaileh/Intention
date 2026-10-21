"""Explicit v1/v0.2 import adapters. New runtime never emits the old field names."""
import copy
import json
from pathlib import Path

FIELD_MAP = {'actions': 'intentions', 'action': 'intention', 'action_id': 'intention_id',
             'ab_version': 'il_version', 'ab_path': 'il_path', 'grounded_card': 'grounded_intention',
             'selected_parent_action_id': 'parent_intention_id', 'selected_child_action_id': 'intention_id',
             'groundable_action_ids': 'groundable_intention_ids'}


def migrate(value):
    if isinstance(value, list):
        return [migrate(v) for v in value]
    if isinstance(value, dict):
        return {('intention_instance_id' if k == 'action_id' and 'argument_index' in value else FIELD_MAP.get(k, k)): migrate(v)
                for k, v in value.items()}
    return value


def read_interpretation_v1(document):
    if document.get('schema_version') != '1.0':
        raise ValueError('LEGACY_VERSION_MISMATCH')
    result = migrate(copy.deepcopy(document))
    result['schema_version'] = '2.0'
    return result


def read_library(path):
    document = json.loads(Path(path).read_text())
    if document.get('ab_version') not in ('0.1.0-draft', '0.2.0-draft'):
        raise ValueError('LEGACY_VERSION_MISMATCH')
    return migrate(document)
