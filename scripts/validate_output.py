#!/usr/bin/env python3
"""Minimal stdlib validator for the required TRIZ output contract."""
from pathlib import Path
import json, sys

if len(sys.argv) != 2:
    print('usage: validate_output.py result.json'); raise SystemExit(2)
data=json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
required=['problem','assumptions','system_boundary','main_function','key_problem','contradictions','ifr','resources','concepts','recommendation','metrics','evidence','uncertainties']
errors=[f'missing: {k}' for k in required if k not in data]
if 'contradictions' in data:
    for k in ['administrative','technical','physical']:
        if k not in data['contradictions']: errors.append(f'missing contradiction: {k}')
if not isinstance(data.get('concepts'),list) or not data.get('concepts'):
    errors.append('concepts must be a non-empty list')
for i,c in enumerate(data.get('concepts',[]),1):
    for k in ['name','triz_tool','mechanism','assumptions','risks','test']:
        if k not in c: errors.append(f'concept {i} missing: {k}')
if errors:
    print('\n'.join(errors)); raise SystemExit(1)
print('OK: result satisfies minimal TRIZ output contract')
