"""Full local scans with truthful provenance, explicit parsing and content-addressed caches."""
import csv
import hashlib
import json
import math
from pathlib import Path

PROFILE_SCHEMA_VERSION = '2.0'
PROFILER_VERSION = '2.0.0'


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _type(values):
    if not values:
        return 'unresolved'
    if all(isinstance(v, bool) or isinstance(v, str) and v.casefold() in ('true', 'false') for v in values):
        return 'boolean'
    if any(isinstance(v, bool) for v in values):
        return 'mixed'
    try:
        for value in values:
            if not math.isfinite(float(value)):
                return 'nonfinite_or_mixed'
        return 'number'
    except (ValueError, TypeError, OverflowError):
        pass
    try:
        from datetime import datetime
        for value in values:
            datetime.fromisoformat(str(value).replace('Z', '+00:00'))
        return 'datetime'
    except ValueError:
        return 'string'


def read_table(path):
    path = Path(path)
    if path.suffix.lower() == '.csv':
        with path.open(encoding='utf-8-sig', newline='') as handle:
            reader = csv.DictReader(handle, strict=True)
            names = reader.fieldnames or []
            if len(names) != len(set(names)) or any(not name for name in names):
                raise ValueError('INVALID_CSV_HEADERS')
            rows = list(reader)
            if any(None in row or any(v is None for v in row.values()) for row in rows):
                raise ValueError('CSV_ROW_WIDTH_MISMATCH')
        return rows, names, 'csv'
    if path.suffix.lower() == '.json':
        value = json.loads(path.read_text(encoding='utf-8'))
        if isinstance(value, dict) and isinstance(value.get('rows'), list):
            value = value['rows']
        if not isinstance(value, list) or not all(isinstance(row, dict) for row in value):
            raise ValueError('JSON_TABLE_MUST_BE_ARRAY_OF_OBJECTS_OR_ROWS_OBJECT')
        if any(isinstance(v, (dict, list)) for row in value for v in row.values()):
            raise ValueError('NESTED_TABLE_CELLS_UNSUPPORTED')
        return value, list(dict.fromkeys(k for row in value for k in row)), 'json'
    raise ValueError('UNSUPPORTED_TABLE_FORMAT')


def profile_table(path, *, dataset_id='local', source_metadata=None, cache_dir=None, missing_tokens=('',)):
    path = Path(path).resolve()
    digest = sha256(path)
    metadata = dict(source_metadata or {})
    metadata.setdefault('source_kind', 'local_unknown')
    for field in ('source_url', 'license', 'acquisition_date', 'source_family'):
        metadata.setdefault(field, None)
    required = ('source_url', 'license', 'acquisition_date', 'source_family', 'attribute_documentation')
    missing_provenance = [field for field in required if not metadata.get(field) or metadata[field] == 'unknown']
    metadata['benchmark_eligible'] = not missing_provenance
    metadata['missing_provenance'] = missing_provenance
    config = {'missing_tokens': list(missing_tokens), 'scan': 'full', 'encoding': 'utf-8-sig'}
    identity = {'sha256': digest, 'profiler_version': PROFILER_VERSION, 'config': config,
                'path': str(path), 'dataset_id': dataset_id, 'metadata': metadata}
    key = hashlib.sha256(json.dumps(identity, sort_keys=True).encode()).hexdigest()
    cache = Path(cache_dir) / (key + '.json') if cache_dir else None
    if cache and cache.exists():
        result = json.loads(cache.read_text())
        if result.get('cache_key') == key:
            result['cache_hit'] = True
            return result
    try:
        rows, names, table_format = read_table(path)
    except (ValueError, UnicodeError, csv.Error) as exc:
        raise ValueError('TABLE_PARSE_FAILURE:' + type(exc).__name__) from exc
    columns, evidence = [], []
    source = {'path': str(path), 'sha256': digest}
    def missing(v):
        return v is None or isinstance(v, str) and v in missing_tokens
    for index, name in enumerate(names):
        values = [row.get(name) for row in rows]
        present = [v for v in values if not missing(v)]
        inferred = _type(present)
        eid = f'column-{index}'
        evidence.append({'id': eid, 'fact': 'observed_column_profile', 'column': name,
                         'method': 'full_local_scan_v2', 'scope': 'entire_local_file',
                         'complete': True, 'source': source})
        item = {'name': name, 'observed_type': inferred, 'null_count': len(values)-len(present),
                'missing_fraction': (len(values)-len(present))/len(rows) if rows else None,
                'evidence_ref': eid, 'distinct_count': len({str(v) for v in present})}
        if inferred == 'number':
            nums = [float(v) for v in present]
            item['numeric_statistics'] = {'finite_count': len(nums), 'minimum': min(nums), 'maximum': max(nums)}
        columns.append(item)
    evidence.append({'id': 'table-scan', 'fact': 'observed_table_identity_and_row_count',
                     'method': 'full_local_scan_v2', 'scope': 'entire_local_file', 'complete': True, 'source': source})
    result = {'schema_version': PROFILE_SCHEMA_VERSION, 'profiler_version': PROFILER_VERSION,
              'dataset_id': dataset_id, 'table_id': f'{dataset_id}:{digest[:16]}', 'source_file': str(path),
              'format': table_format, 'row_count': len(rows), 'column_names': names, 'columns': columns,
              'file_sha256': digest, 'source_metadata': metadata, 'evidence': evidence,
              'scan': {'scope': 'full_table', 'complete': True, 'sampled': False}, 'parsing': config,
              'semantic_annotations': {'status': 'unresolved', 'reason': 'not inferred by primitive profiler'},
              'cache_key': key, 'cache_hit': False}
    if cache:
        cache.parent.mkdir(parents=True, exist_ok=True)
        import os, tempfile
        with tempfile.NamedTemporaryFile(mode='w', dir=cache.parent, delete=False, encoding='utf-8') as handle:
            json.dump(result, handle)
            temp = handle.name
        os.replace(temp, cache)
    return result


def profile_paths(paths, **kwargs):
    return [profile_table(path, **kwargs) for path in sorted(map(Path, paths), key=str)]
