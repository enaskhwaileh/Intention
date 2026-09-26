"""Offline fixtures only. Each execution creates an isolated directory."""
import argparse
import json
from importlib.resources import files
from pathlib import Path
import tempfile

from .core import interpret
from .providers import ReplayProvider


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-root', type=Path, default=Path('outputs/ab-m1'))
    args = parser.parse_args()
    args.output_root.mkdir(parents=True, exist_ok=True)
    output = Path(tempfile.mkdtemp(prefix='manual-replay-', dir=args.output_root))
    fixtures = json.loads(files(__package__).joinpath('fixtures/replay.json').read_text())
    failures = 0
    for case in fixtures:
        result = interpret(case['input_id'], case['input'], ReplayProvider(case['raw_response']))
        prefix = output / case['input_id']
        prefix.with_suffix('.raw.txt').write_text(case['raw_response'], encoding='utf-8')
        validated = {k:v for k,v in result.items() if k != 'raw_response'}
        prefix.with_suffix('.result.json').write_text(json.dumps(validated, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
        observed = result['failure'] or result['interpretation']['status']
        failures += observed != case['expected']
        print(f"{case['input_id']}: {observed} (expected {case['expected']})")
    print(f'Manually authored fixtures; not model evaluation. Outputs: {output}')
    return int(bool(failures))


if __name__ == '__main__':
    raise SystemExit(main())
