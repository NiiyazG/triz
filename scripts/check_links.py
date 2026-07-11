#!/usr/bin/env python3
"""Check local Markdown links without external dependencies."""
from pathlib import Path
import re, sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
pattern = re.compile(r'\[[^\]]*\]\(([^)]+)\)')
errors = []
for md in root.rglob('*.md'):
    text = md.read_text(encoding='utf-8')
    for raw in pattern.findall(text):
        target = raw.strip().split('#',1)[0]
        if not target or '://' in target or target.startswith('mailto:'):
            continue
        p = (md.parent / target).resolve()
        try:
            p.relative_to(root)
        except ValueError:
            errors.append(f'{md.relative_to(root)}: link escapes package: {raw}')
            continue
        if not p.exists():
            errors.append(f'{md.relative_to(root)}: missing: {raw}')
if errors:
    print('\n'.join(errors))
    raise SystemExit(1)
print(f'OK: local Markdown links valid in {root}')
