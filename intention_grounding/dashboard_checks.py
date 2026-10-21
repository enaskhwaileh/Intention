"""Machine-readable report of the real unittest suite for the local interface."""
import argparse
import contextlib
import io
import json
from pathlib import Path
import time
import unittest


class Results(unittest.TextTestResult):
    def __init__(self, *args):
        super().__init__(*args)
        self.records = []

    def addSuccess(self, test):
        super().addSuccess(test)
        self.records.append({'test': test.id(), 'status': 'passed'})

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.records.append({'test': test.id(), 'status': 'failed', 'error_type': err[0].__name__})

    def addError(self, test, err):
        super().addError(test, err)
        self.records.append({'test': test.id(), 'status': 'error', 'error_type': err[0].__name__})

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self.records.append({'test': test.id(), 'status': 'skipped'})

    def addSubTest(self, test, subtest, err):
        super().addSubTest(test, subtest, err)
        if err:
            self.records.append({'test': subtest.id(), 'status': 'failed', 'error_type': err[0].__name__})

    def addExpectedFailure(self, test, err):
        super().addExpectedFailure(test, err)
        self.records.append({'test': test.id(), 'status': 'expected_failure'})

    def addUnexpectedSuccess(self, test):
        super().addUnexpectedSuccess(test)
        self.records.append({'test': test.id(), 'status': 'unexpected_success'})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    start = time.perf_counter()
    root = Path(__file__).resolve().parent.parent
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        suite = unittest.defaultTestLoader.discover(str(root / 'tests'))
        result = unittest.TextTestRunner(stream=io.StringIO(), resultclass=Results).run(suite)
    report = {'status': 'passed' if result.wasSuccessful() else 'failed', 'tests_run': result.testsRun,
              'failures': len(result.failures), 'errors': len(result.errors), 'skipped': len(result.skipped),
              'unexpected_successes': len(result.unexpectedSuccesses),
              'elapsed_seconds': round(time.perf_counter()-start, 3), 'tests': result.records,
              'notice': 'Software contract verification, not model accuracy or retrieval effectiveness.'}
    if args.report:
        args.report.write_text(json.dumps(report), encoding='utf-8')
    else:
        print(json.dumps(report))
    return int(not result.wasSuccessful())


if __name__ == '__main__':
    raise SystemExit(main())
