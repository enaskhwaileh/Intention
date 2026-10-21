"""Check maintained runtime names. Frozen history and explicit readers are excluded.

Exceptions: argparse's third-party action= keyword; legacy/ and docs/ab_proposal/
are frozen inputs/readers; scripts/, kb/, data/, results/ are historical provenance.
tests/test_ab_proposal.py verifies frozen historical contracts.
Generic unknown data-source values are allowed; requirement verdicts use unresolved.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
FORBIDDEN = re.compile(r'\b(?:actions|action_id|ab_version|ab_path|grounded_card|selected_child_action_id|selected_parent_action_id|load_action_base|validate_action_base|ActionBaseError)\b')


def check():
    paths = [*ROOT.glob('*.py'), *ROOT.glob('interpreter/*.py'), *ROOT.glob('interpreter/*.json'),
             *ROOT.glob('interpreter/fixtures/*.json'), *ROOT.glob('library/*.json'), *ROOT.glob('ui/*'), *ROOT.glob('schemas/*.json'),
             *ROOT.parent.glob('configs/*.json'),
             *(p for p in (ROOT.parent/'tests').glob('*.py') if p.name != 'test_ab_proposal.py')]
    violations = []
    for p in paths:
        if p.name == 'terminology.py':
            continue  # the checker must name the rejected vocabulary
        for number, line in enumerate(p.read_text().splitlines(), 1):
            if FORBIDDEN.search(line):
                violations.append(f'{p.relative_to(ROOT.parent)}:{number}')
    return violations


if __name__ == '__main__':
    violations = check()
    print('\n'.join(violations) if violations else 'Canonical runtime terminology verified.')
    raise SystemExit(bool(violations))
