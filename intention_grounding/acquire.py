"""Reproduce the bounded official UCI bike corpus; originals are never overwritten."""
import argparse
import csv
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import urllib.request
import zipfile

from .profiler import sha256

ROOT = Path(__file__).resolve().parent.parent
SOURCES = {
    '275': {'slug': 'bike+sharing+dataset', 'sha256': 'b70182d0d0508e9abbb79306ce5c0cec34869000f8220175ac83d11dbe845401'},
    '560': {'slug': 'seoul+bike+sharing+demand', 'sha256': '139e9908f0a3544bb222386855c9ce107e96467306bb8e4ce936aab59e7baac4'},
}


def immutable(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_bytes() != data:
            raise ValueError('IMMUTABLE_FILE_CONFLICT:' + str(path))
    else:
        with path.open('xb') as handle:
            handle.write(data)


def fetch(url, path, *, offline=False, expected=None):
    if not path.exists():
        if offline:
            raise ValueError('NOT_ACQUIRED:' + str(path))
        try:
            with urllib.request.urlopen(url, timeout=45) as response:
                data = response.read(10_000_001)
        except Exception as exc:
            raise RuntimeError(f'SOURCE_ACCESS_FAILED:{url}:{type(exc).__name__}') from exc
        if len(data) > 10_000_000:
            raise ValueError('SOURCE_SIZE_LIMIT')
        if expected and hashlib.sha256(data).hexdigest() != expected:
            raise ValueError('SOURCE_HASH_MISMATCH:' + url)
        immutable(path, data)
    if expected and sha256(path) != expected:
        raise ValueError('SOURCE_HASH_MISMATCH:' + str(path))
    return path.read_bytes()


def acquire(root=ROOT, *, offline=False):
    root = Path(root)
    manifest_path = root / 'data/manifests/uci-bikes-v1.json'
    old = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    cached = all((root/f'data/raw/uci-{ident}.zip').exists() and (root/f'data/raw/uci-{ident}-source.html').exists() for ident in SOURCES)
    acquired = old.get('acquisition_date') if cached and old.get('acquisition_date') else datetime.now(timezone.utc).isoformat()
    tables, sources = [], []
    for ident, source in SOURCES.items():
        url = f'https://archive.ics.uci.edu/static/public/{ident}/{source["slug"]}.zip'
        page_url = f'https://archive.ics.uci.edu/dataset/{ident}/{source["slug"]}'
        archive_path = root / f'data/raw/uci-{ident}.zip'
        archive = fetch(url, archive_path, offline=offline, expected=source['sha256'])
        page = root / f'data/raw/uci-{ident}-source.html'
        fetch(page_url, page, offline=offline)
        # Licensing evidence is retained as the actual retrieved source page, not an invented license.
        html = page.read_text(errors='replace')
        if 'creativecommons.org/licenses/by/4.0' not in html:
            raise ValueError('LICENSE_NOT_VERIFIED:' + page_url)
        sources.append({'official_id': 'uci:' + ident, 'source_url': page_url, 'download_url': url,
                        'archive_path': str(archive_path.relative_to(root)), 'archive_sha256': sha256(archive_path),
                        'source_document_path': str(page.relative_to(root)), 'source_document_sha256': sha256(page),
                        'acquisition_date': acquired, 'license': 'CC BY 4.0',
                        'redistribution': 'Attribution required; retain source citation and indicate transformations.'})
        with zipfile.ZipFile(io.BytesIO(archive)) as z:
            members = ['day.csv','hour.csv'] if ident == '275' else ['SeoulBikeData.csv']
            if ident == '275':
                immutable(root/'data/raw/uci-275-Readme.txt', z.read('Readme.txt'))
            for member in members:
                raw = z.read(member)
                rows = list(csv.DictReader(io.StringIO(raw.decode('utf-8' if ident=='275' else 'latin-1'))))
                names = list(rows[0])
                if ident == '560':
                    for row in rows:
                        row['Date'] = datetime.strptime(row['Date'], '%d/%m/%Y').date().isoformat()
                buf = io.StringIO(newline='')
                writer = csv.DictWriter(buf, names, lineterminator='\n');writer.writeheader();writer.writerows(rows)
                tid = 'uci-275-' + member[:-4] if ident=='275' else 'uci-560-hour'
                normalized = root / f'data/normalized/{tid}.csv'
                immutable(normalized, buf.getvalue().encode('utf-8'))
                date = 'dteday' if ident=='275' else 'Date'
                grain = 'day' if member=='day.csv' else 'hour'
                doc = root/'data/raw/uci-275-Readme.txt' if ident=='275' else page
                locator = 'Dataset characteristics: cnt, dteday, workingday, yr; Files: day.csv/hour.csv; Data Set: Washington D.C.' if ident=='275' else 'Additional Variable Information; dataset description: Seoul, count per hour'
                measure = 'cnt' if ident=='275' else 'Rented Bike Count'
                bindings = {'measure': measure, 'date': date}
                if grain == 'hour':bindings['hour'] = 'hr' if ident=='275' else 'Hour'
                if ident=='275':bindings['workingday']='workingday'
                semantics = {'measure_concept': 'bike_rental_count', 'unit': 'rentals',
                             'population': 'capital_bikeshare_dc' if ident=='275' else 'seoul_bike_system',
                             'grain': grain, 'measure_kind': 'interval_count', 'columns': bindings,
                             'group_domains': {'workingday': {'0':'weekend_or_holiday','1':'neither_weekend_nor_holiday'}} if ident=='275' else {},
                             'source_document': {'path': str(doc.relative_to(root)), 'sha256': sha256(doc),
                                                 'url': page_url, 'locator': locator},
                             'mapping_origin': 'project-authored mapping of inspected source documentation, not usefulness gold'}
                tables.append({'table_id': tid, 'source_family': 'uci:' + ident, 'topic': 'urban_bicycle_rentals',
                               'source_url': page_url, 'official_id': 'uci:' + ident, 'acquisition_date': acquired,
                               'license': 'CC BY 4.0', 'path': str(normalized.relative_to(root)),
                               'normalized_sha256': sha256(normalized), 'original_member': member,
                               'original_member_sha256': hashlib.sha256(raw).hexdigest(),
                               'archive_sha256': sha256(archive_path), 'row_count': len(rows), 'columns': names,
                               'period': [min(r[date] for r in rows), max(r[date] for r in rows)],
                               'attribute_documentation': semantics['source_document'], 'semantics': semantics,
                               'normalization': ['Decode '+('UTF-8' if ident=='275' else 'Latin-1')+' and write UTF-8 CSV with LF newlines',
                                                 'Normalize Date from DD/MM/YYYY to ISO date' if ident=='560' else 'Preserve values, columns and all observations'],
                               'related_tables': ['uci-275-hour' if grain=='day' else 'uci-275-day'] if ident=='275' else [],
                               'relationship': 'shared underlying rental logs at different grains' if ident=='275' else 'distinct system and period; no mirror relationship asserted',
                               'why_selected': 'Documented counts at '+grain+' grain; same-topic candidates allow grain and population compatibility to be tested.',
                               'limitations': ['Descriptive observed intervals only; no causal interpretation or complete-grid claim.',
                                               'Temperature/season metadata conflict between UCI page and Readme; excluded from binding.' if ident=='275' else 'Non-functioning hours retained; no extrapolation to operating-hour demand.',
                                               'Mean of interval counts is not a mean of trip-level records. Missing intervals are not imputed.'],
                               'retrieval_text': f"Bike bicycle rental count {grain} {'daily' if grain=='day' else 'hourly'} date {'Washington DC Capital Bikeshare workingday weekend holiday 2011 2012' if ident=='275' else 'Seoul 2017 2018 hourly weather'}"})
    manifest = {'schema_version': '1.0', 'corpus_id': 'uci-bikes-v1', 'partition': 'development_only',
                'acquisition_date': acquired, 'sources': sources, 'tables': tables,
                'independent_usefulness_judgments': False, 'notes': 'Two source families in one topic; no held-out effectiveness claim.'}
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest,indent=2)+'\n')
    return manifest


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--offline', action='store_true', help='Verify/reconstruct from cached original files without network')
    args=parser.parse_args()
    try:
        result=acquire(offline=args.offline)
    except (ValueError,RuntimeError) as exc:
        parser.exit(2,str(exc)+'\n')
    for table in result['tables']:
        print(table['table_id'],table['row_count'],table['normalized_sha256'])


if __name__=='__main__':main()
