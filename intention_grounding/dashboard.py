"""Local, offline research demonstrator using the existing framework components."""
import argparse
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import time
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit, parse_qs

from .intention_library import load_intention_library, list_intentions, describe_intention, IntentionLibraryError
from .cli import _offline_inputs
from .interpreter.core import interpret
from .interpreter.providers import ReplayProvider
from .grounder import ground
from .profiler import profile_table
from .aligner import compare_card

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
UI = PACKAGE / 'ui'
TEST_LOCK = threading.Lock()


def identity():
    digest = hashlib.sha256()
    paths = sorted([*PACKAGE.rglob('*.py'), *PACKAGE.rglob('*.json'), *UI.glob('*'),
                    *(ROOT / 'tests').glob('*.py'), ROOT / 'pyproject.toml'])
    for path in paths:
        if path.is_file():
            digest.update(str(path.relative_to(ROOT)).encode())
            digest.update(path.read_bytes())
    try:
        sha = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, stderr=subprocess.DEVNULL, timeout=3).decode().strip()
        dirty = bool(subprocess.check_output(['git', 'status', '--porcelain'], cwd=ROOT, stderr=subprocess.DEVNULL, timeout=3))
    except (OSError, subprocess.SubprocessError):
        sha, dirty = 'unavailable', None
    return {'commit': sha, 'working_tree_dirty': dirty, 'implementation_sha256': digest.hexdigest(),
            'python': sys.version.split()[0], 'timestamp': datetime.now(timezone.utc).isoformat()}


def cases():
    return json.loads((PACKAGE / 'interpreter/fixtures/replay.json').read_text())


def run_case(case_id):
    case = next((c for c in cases() if c['input_id'] == case_id), None)
    if case is None:
        raise ValueError('Unknown replay case')
    start = time.perf_counter()
    result = interpret(case['input_id'], case['input'], ReplayProvider(case['raw_response']))
    observed = result['failure'] or result['interpretation']['status']
    return {'case_id': case_id, 'request': case['input'], 'expected': case['expected'],
            'observed': observed, 'passed': observed == case['expected'], 'result': result,
            'elapsed_ms': round((time.perf_counter() - start) * 1000, 2),
            'origin': 'manual replay; expected rejection can be a passing contract check'}


def replay_demo():
    start = time.perf_counter()
    il = load_intention_library()
    input_id, request, interpreter_provider, grounder_provider = _offline_inputs(il['il_version'])
    interpreted = interpret(input_id, request, interpreter_provider)
    grounded = ground(interpreted, il, grounder_provider, run_id='dashboard-offline')
    metadata = json.loads((PACKAGE / 'fixtures/offline-source-metadata.json').read_text())
    path = PACKAGE / 'fixtures/offline_table.csv'
    profile = profile_table(path, dataset_id=metadata['dataset_id'], source_metadata=metadata)
    comparison = compare_card(grounded['grounded_intention'], [profile])
    return {'request': request, 'mode': 'offline_manual_replay', 'il_version': il['il_version'],
            'interpretation': interpreted, 'grounding': grounded, 'profile': profile,
            'comparison': comparison, 'rows': list(csv.DictReader(io.StringIO(path.read_text()))),
            'elapsed_ms': round((time.perf_counter() - start) * 1000, 2), 'provenance': identity(),
            'notice': 'Synthetic fixture. No LLM inference, retrieval, ranking or usefulness measurement was performed.'}


def corpus_overview():
    path = ROOT/'data/manifests/uci-bikes-v1.json'
    if not path.exists():
        return {'ready':False,'tables':[], 'message':'Run python -m intention_grounding.acquire first.'}
    corpus=json.loads(path.read_text())
    missing=[t['path'] for t in corpus['tables'] if not (ROOT/t['path']).exists()]
    return {'ready':not missing,'tables':corpus['tables'],'sources':corpus['sources'],
            'partition':corpus['partition'],'message':'Cached real data ready.' if not missing else 'Data not acquired. Run python -m intention_grounding.acquire.'}


def real_cases():
    return json.loads((ROOT/'data/requests/demo-v1.json').read_text())['cases']


def real_demo(case_id):
    from .discovery import run, save_report
    case=next((c for c in real_cases() if c['request']['request_id']==case_id),None)
    if case is None:raise ValueError('Unknown demonstration case')
    if not corpus_overview()['ready']:
        raise ValueError('DATA_NOT_ACQUIRED: run python -m intention_grounding.acquire')
    report=run(case['request'],**case['run_options'])
    path=save_report(report,ROOT/'outputs/dashboard')
    report['saved_prediction_path']=str(path.relative_to(ROOT))
    report['saved_prediction_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
    return report


def run_checks():
    """Fixed offline command, isolated from web requests and provider credentials."""
    if not (ROOT / 'tests/test_pipeline.py').exists():
        return {'status': 'unavailable', 'message': 'Run this interface from a source checkout with tests.'}
    if not TEST_LOCK.acquire(blocking=False):
        return {'status': 'busy', 'message': 'A test run is already in progress.'}
    try:
        before = identity()
        env = {key: os.environ[key] for key in ('PATH', 'SYSTEMROOT', 'TMPDIR', 'LANG') if key in os.environ}
        env['PYTHONPATH'] = str(ROOT)
        with tempfile.TemporaryDirectory(prefix='intention-test-report-') as temp:
            path = Path(temp) / 'report.json'
            result = subprocess.run([sys.executable, '-m', 'intention_grounding.dashboard_checks',
                                     '--report', str(path)], cwd=ROOT, env=env,
                                    capture_output=True, text=True, timeout=60)
            if result.returncode not in (0, 1):
                return {'status': 'error', 'message': 'Test process did not complete normally.'}
            report = json.loads(path.read_text(encoding='utf-8'))
        report['provenance'] = before
        report['source_changed_during_run'] = before['implementation_sha256'] != identity()['implementation_sha256']
        return report
    except subprocess.TimeoutExpired:
        return {'status': 'timeout', 'message': 'Offline checks exceeded 60 seconds; no pass result recorded.'}
    except (OSError, ValueError):
        return {'status': 'error', 'message': 'Could not start or read the offline checks.'}
    finally:
        TEST_LOCK.release()


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def send(self, value, status=200, content_type='application/json; charset=utf-8'):
        body = value if isinstance(value, bytes) else json.dumps(value, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Content-Security-Policy', "default-src 'self'; style-src 'self'; script-src 'self'; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'")
        self.end_headers()
        self.wfile.write(body)

    def local_request(self):
        hosts = {f'127.0.0.1:{self.server.server_port}', f'localhost:{self.server.server_port}'}
        host = self.headers.get('Host', '')
        origin = self.headers.get('Origin')
        return host in hosts and (not origin or origin == 'http://' + host)

    def do_GET(self):
        if not self.local_request():
            return self.send({'error': 'Local origin required'}, 403)
        url = urlsplit(self.path)
        assets = {'/': ('index.html', 'text/html'), '/app.js': ('app.js', 'text/javascript'), '/style.css': ('style.css', 'text/css')}
        if url.path in assets:
            name, mime = assets[url.path]
            return self.send((UI / name).read_bytes(), content_type=mime+'; charset=utf-8')
        if url.path == '/api/overview':
            il = load_intention_library()
            return self.send({'library': list_intentions(il), 'procedures': len(il.get('procedures', {})),
                              'cases': [{k: c[k] for k in ('input_id', 'input', 'expected')} for c in cases()],
                              'provenance': identity(), 'corpus':corpus_overview(), 'real_cases':real_cases()})
        if url.path == '/api/intention':
            try:
                aid = parse_qs(url.query).get('id', [''])[0]
                return self.send(describe_intention(aid, load_intention_library()))
            except IntentionLibraryError:
                return self.send({'error': 'Unknown intention'}, 404)
        return self.send({'error': 'Not found'}, 404)

    def do_POST(self):
        if not self.local_request() or self.headers.get('Content-Type') != 'application/json':
            return self.send({'error': 'Same-origin JSON required'}, 403)
        try:
            length = int(self.headers.get('Content-Length', '0'))
            if not 0 < length <= 4096:
                return self.send({'error': 'Invalid request size'}, 413)
            payload = json.loads(self.rfile.read(length))
            if not isinstance(payload, dict):
                raise ValueError()
            if self.path == '/api/demo':
                return self.send(real_demo(payload.get('case_id','dc_daily')))
            if self.path == '/api/replay-pipeline':
                return self.send(replay_demo())
            if self.path == '/api/case':
                return self.send(run_case(payload.get('id')))
            if self.path == '/api/tests':
                return self.send(run_checks())
        except (ValueError, TypeError) as exc:
            message='Invalid request or unknown case'
            if str(exc).startswith('DATA_NOT_ACQUIRED'): message=str(exc)
            return self.send({'error': message}, 400)
        except Exception:
            return self.send({'error': 'Operation failed; no result claimed'}, 500)
        return self.send({'error': 'Not found'}, 404)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8765)
    args = parser.parse_args()
    try:
        server = ThreadingHTTPServer(('127.0.0.1', args.port), Handler)
    except OSError as exc:
        parser.exit(2, f'Cannot start local interface ({type(exc).__name__}); try another --port.\n')
    print(f'Intention research demo: http://127.0.0.1:{server.server_port}', flush=True)
    print('Offline only. Press Ctrl+C to stop.', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
