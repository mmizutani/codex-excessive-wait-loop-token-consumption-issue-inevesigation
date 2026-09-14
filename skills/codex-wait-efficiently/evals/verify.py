#!/usr/bin/env python3
"""Verify exported evidence and frozen inputs without model calls or login."""
from collections import Counter
import hashlib
import json
from pathlib import Path

from grade import grade

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    target = HERE/'results/final'
    records = json.loads((target/'trial-evidence.json').read_text())
    scores = json.loads((target/'scores.json').read_text())
    rows = {(r['phase'],r['name']):r for r in records}
    assert len(rows) == len(records)
    response_ids = [u['response_id'] for r in records for u in r['response_usage']]
    assert len(response_ids) == len(set(response_ids)) == scores['unique_response_ids']
    for row in scores['trials']:
        record = rows[row['phase'],row['name']]
        evaluated = grade(record)
        assert evaluated == record['evaluation']
        assert all(row[k] == v for k,v in evaluated.items())
        assert evaluated['checks']['accounting']
        assert record['skill_sha256'] == digest(HERE/'versions'/record['skill_version']/'SKILL.md.fixture')
    phases = set(r['phase'] for r in records)
    for phase in phases:
        manifest = json.loads((HERE/'manifests'/(phase+'.json')).read_text())
        actual = {r['name']:r for r in records if r['phase']==phase}
        expected = {f"{t['version']}-{t['case']['id']}-r{t['repetition']}":t for t in manifest['tasks']}
        assert set(actual) == set(expected)
        assert manifest['cases_sha256'] == digest(HERE/'cases.json')
        for name,task in expected.items():
            record = actual[name]
            assert record['eval_case'] == task['case']
            assert record['skill_sha256'] == manifest['versions'][task['version']]
            assert record['catalog_sha256'] == manifest['catalog_sha256']
    assert digest(ROOT/'skills/codex-wait-efficiently/SKILL.md') == digest(HERE/'versions/v4/SKILL.md.fixture')
    assert digest(ROOT/'docs/waiting-validation/AGENTS.waiting-compatible.md') == '882067320df757cc72afaf1fa542e9c476d0c445d4f52a0ea683eb38e2daa411'
    failures = [{'phase':r['phase'],'name':r['name'],'checks':r['evaluation']['failed_checks']}
                for r in records if not r['evaluation']['overall_pass']]
    result = {'trials':len(records),'unique_responses':len(response_ids),
        'phases':dict(Counter(r['phase'] for r in records)),
        'all_outcomes_correct':all(r['evaluation']['checks']['outcome'] for r in records),
        'all_accounting_reconciled':True,'frozen_inputs_match':True,
        'agents_patch_unchanged':True,'final_skill_version':'v4',
        'final_skill_sha256':digest(ROOT/'skills/codex-wait-efficiently/SKILL.md'),
        'retained_deterministic_failures':failures,
        'unused_manifests':sorted(p.stem for p in (HERE/'manifests').glob('*.json') if p.stem not in phases)}
    (target/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
