#!/usr/bin/env python3
"""Validate TRIZ skill package structure and core invariants."""
from pathlib import Path
import re, sys, json

root = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
required = [
    'SKILL.md', 'README.md', 'CHANGELOG.md', 'LICENSE',
    'references/methodology-map.md', 'references/problem-identification.md',
    'references/physical-contradictions.md', 'references/sufield-and-76-sis.md',
    'references/ariz-85c.md', 'references/ariz-85c-routing.md', 'references/sources.md',
    'references/toc-evaporating-cloud.md', 'references/otsm-network.md',
    'references/ck-theory.md', 'references/morphological-analysis.md',
    'references/axiomatic-design.md', 'references/decision-analysis.md',
    'references/cynefin-routing.md', 'references/ssm-catwoe.md',
    'references/kepner-tregoe.md', 'references/sit.md',
    'references/biomimicry-fos.md', 'references/synectics.md',
    'references/lateral-thinking-six-hats.md', 'references/double-diamond.md',
    'references/doe.md', 'references/stpa.md',
    'schemas/triz-result.schema.json', 'evals/trigger-cases.csv',
    'evals/behavior-cases.jsonl', 'evals/adversarial-cases.jsonl', 'evals/rubric.yaml'
]
errors = []
for rel in required:
    if not (root/rel).is_file():
        errors.append(f'missing required file: {rel}')

skill = (root/'SKILL.md').read_text(encoding='utf-8') if (root/'SKILL.md').exists() else ''
for field in ['name: triz', 'version: 3.0.0', 'author: Niyaz Garipov', 'license: MIT', '## When to Use', '## Procedure', '## Pitfalls', '## Verification']:
    if field not in skill:
        errors.append(f'SKILL.md missing invariant: {field}')
if len(skill.splitlines()) > 320:
    errors.append('SKILL.md exceeds 320 lines; progressive disclosure degraded')
for bad in ['В1 + В2 -> П', 'сокращённый АРИЗ', 'таблица Альтшуллера ниже']:
    if bad in skill:
        errors.append(f'forbidden legacy phrase in SKILL.md: {bad}')

try:
    schema = json.loads((root/'schemas/triz-result.schema.json').read_text(encoding='utf-8'))
    cprops = schema.get('properties', {}).get('contradictions', {})
    if 'anyOf' not in cprops:
        errors.append('schema must allow optional contradiction kinds (anyOf)')
except Exception as e:
    errors.append(f'invalid JSON schema: {e}')

for rel in ['evals/behavior-cases.jsonl', 'evals/adversarial-cases.jsonl']:
    p = root/rel
    if p.exists():
        for i, line in enumerate(p.read_text(encoding='utf-8').splitlines(), 1):
            try:
                json.loads(line)
            except Exception as e:
                errors.append(f'{rel}:{i}: invalid JSON: {e}')

if errors:
    print('\n'.join(errors)); raise SystemExit(1)
print(f'OK: TRIZ skill package valid ({len(skill.splitlines())} lines in SKILL.md)')
