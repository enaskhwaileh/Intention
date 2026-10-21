"""Integration and local-interface boundaries; no provider calls or model downloads."""
import http.client
import json
from pathlib import Path
import subprocess
import threading
import unittest
from unittest.mock import patch
from http.server import ThreadingHTTPServer

from intention_grounding import dashboard


class DashboardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), dashboard.Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def request(self, method, path, body=None, headers=None):
        connection = http.client.HTTPConnection('127.0.0.1', self.server.server_port, timeout=10)
        connection.request(method, path, body=body, headers=headers or {})
        response = connection.getresponse()
        data = response.read()
        result = response.status, dict(response.getheaders()), data
        connection.close()
        return result

    def test_demo_executes_existing_components_with_explicit_provenance(self):
        with patch('intention_grounding.groq_config.groq_api_key', side_effect=AssertionError('No credentials')):
            status, _, raw = self.request('POST', '/api/demo', '{}', {'Content-Type': 'application/json'})
        self.assertEqual(200, status)
        result = json.loads(raw)
        self.assertEqual('offline_manual_replay', result['mode'])
        self.assertEqual('compare.time', result['grounding']['grounded_intention']['intention_id'])
        self.assertEqual(4, len(result['rows']))
        self.assertEqual(4, result['profile']['row_count'])
        self.assertEqual('unresolved', result['comparison']['tables'][0]['overall_state'])
        self.assertTrue(result['provenance']['implementation_sha256'])
        self.assertIn('Synthetic', result['notice'])

    def test_all_replay_outcomes_and_unknown_case(self):
        for case in dashboard.cases():
            with self.subTest(case=case['input_id']):
                self.assertTrue(dashboard.run_case(case['input_id'])['passed'])
        status, _, _ = self.request('POST', '/api/case', '{"id":"invented"}', {'Content-Type':'application/json'})
        self.assertEqual(400, status)

    def test_catalog_and_assets_loaded_without_directory_exposure(self):
        status, _, body = self.request('GET', '/api/overview')
        self.assertEqual(200,status)
        overview = json.loads(body)
        self.assertEqual(13,len(overview['cases']))
        status, _, body = self.request('GET', '/api/intention?id=predict.forecasting')
        self.assertEqual(200,status)
        self.assertFalse(json.loads(body)['groundable'])
        self.assertEqual(404,self.request('GET','/api/intention?id=missing')[0])
        for asset in ('/', '/app.js', '/style.css'):
            status, headers, body = self.request('GET',asset)
            self.assertEqual(200,status)
            self.assertTrue(body)
            self.assertIn('Content-Security-Policy',headers)
        for path in ('/.env','/../pyproject.toml','/intention_grounding/.env'):
            self.assertEqual(404,self.request('GET',path)[0])

    def test_cross_origin_invalid_json_and_oversized_requests_rejected(self):
        for headers in ({'Host':'evil.example'}, {'Origin':'https://evil.example'}, {'Content-Type':'text/plain'}):
            self.assertEqual(403,self.request('POST','/api/demo','{}',headers)[0])
        self.assertEqual(400,self.request('POST','/api/demo','[]',{'Content-Type':'application/json'})[0])
        self.assertEqual(413,self.request('POST','/api/demo','x'*4097,{'Content-Type':'application/json'})[0])
        self.assertEqual(403,self.request('GET','/api/overview',headers={'Host':'evil.example'})[0])

    def test_test_endpoint_returns_runner_results_and_never_selects_commands(self):
        report={'status':'passed','tests_run':7,'tests':[]}
        with patch.object(dashboard,'run_checks',return_value=report) as runner:
            status, _, raw=self.request('POST','/api/tests','{"command":"ignored"}',{'Content-Type':'application/json'})
        runner.assert_called_once_with()
        self.assertEqual(200,status)
        self.assertEqual(report,json.loads(raw))

    def test_runner_failure_timeout_and_credentials_boundary(self):
        identity={'implementation_sha256':'stable'}
        report={'status':'failed','tests_run':1,'failures':1,'tests':[]}
        with patch.object(dashboard,'identity',return_value=identity), patch.object(dashboard.subprocess,'run') as run:
            def complete(command, **kwargs):
                Path(command[-1]).write_text(json.dumps(report))
                return subprocess.CompletedProcess(command,1,'child test output','')
            run.side_effect=complete
            self.assertEqual('failed',dashboard.run_checks()['status'])
            kwargs=run.call_args.kwargs
            self.assertNotIn('GROQ_API_KEY',kwargs['env'])
            self.assertEqual(60,kwargs['timeout'])
            run.side_effect=subprocess.TimeoutExpired('fixed command',60)
            self.assertEqual('timeout',dashboard.run_checks()['status'])
            run.side_effect=None
            run.return_value=subprocess.CompletedProcess([],0,'not json','')
            self.assertEqual('error',dashboard.run_checks()['status'])
        dashboard.TEST_LOCK.acquire()
        try:
            self.assertEqual('busy',dashboard.run_checks()['status'])
        finally:
            dashboard.TEST_LOCK.release()


if __name__ == '__main__':
    unittest.main()
