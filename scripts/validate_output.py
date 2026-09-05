#!/usr/bin/env python3
"""Validate a TRIZ result JSON against the output contract + semantic checks."""
from pathlib import Path
import json, sys

if len(sys.argv) != 2:
    print('usage: validate_output.py result.json'); raise SystemExit(2)

data = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
errors = []
warnings = []

REQUIRED = ['problem', 'assumptions', 'system_boundary', 'main_function', 'key_problem',
            'contradictions', 'ifr', 'resources', 'concepts', 'recommendation', 'metrics',
            'evidence', 'uncertainties']
for k in REQUIRED:
    if k not in data:
        errors.append(f'missing: {k}')

# contradictions: administrative required, at least one of technical/physical/dilemma
if 'contradictions' in data:
    c = data['contradictions']
    if not isinstance(c, dict):
        errors.append('contradictions must be an object')
    else:
        if not c.get('administrative'):
            errors.append('contradictions.administrative is required and non-empty')
        if not any(c.get(k) for k in ('technical', 'physical', 'dilemma')):
            errors.append('contradictions must contain at least one of technical/physical/dilemma')

# concepts
if 'concepts' in data:
    cs = data['concepts']
    if not isinstance(cs, list) or not cs:
        errors.append('concepts must be a non-empty list')
    else:
        for i, c in enumerate(cs, 1):
            for k in ['name', 'mechanism', 'assumptions', 'risks', 'test']:
                if k not in c:
                    errors.append(f'concept {i} missing: {k}')
            mech = c.get('mechanism')
            if isinstance(mech, str) and (len(mech.strip()) < 8 or mech.strip() == c.get('name', '')):
                errors.append(f'concept {i} mechanism too thin or equals name (no real mechanism)')
            tool = c.get('triz_tool')
            if isinstance(tool, str) and isinstance(mech, str) and tool == mech:
                errors.append(f'concept {i} mechanism repeats tool name — describe the mechanism, not the label')

# evidence status enum
for i, e in enumerate(data.get('evidence', []), 1):
    if not isinstance(e, dict):
        errors.append(f'evidence {i} must be an object'); continue
    for k in ['claim', 'status', 'source']:
        if k not in e:
            errors.append(f'evidence {i} missing: {k}')
    if e.get('status') not in ('verified', 'assumption', 'hypothesis', 'example'):
        errors.append(f'evidence {i} status must be verified/assumption/hypothesis/example')

# optional enums
for field, enum in [('domain', ('clear', 'complicated', 'complex', 'chaotic')),
                    ('problem_nature', ('technical_contradiction', 'physical_contradiction', 'dilemma', 'network_of_problems', 'uncertainty', 'infeasibility', 'multiobjective', 'none')),
                    ('exit', ('optimization', 'measure_first', 'insufficient_data', 'no_solution'))]:
    if field in data and data[field] not in enum:
        errors.append(f'{field} must be one of {enum}')

# semantic warning: technical contradiction should describe two opposing parameters
if isinstance(data.get('contradictions'), dict) and data['contradictions'].get('technical'):
    t = data['contradictions']['technical'].lower()
    if not any(marker in t for marker in ('если', 'if ', '→', 'worsens', 'degrade', 'ухудш', 'улучш', 'improves')):
        warnings.append('technical contradiction does not describe a parameter trade-off')

if errors:
    print('\n'.join(errors)); raise SystemExit(1)
if warnings:
    print('WARNINGS:\n' + '\n'.join(warnings))
print('OK: result satisfies TRIZ output contract (semantic checks passed)')
