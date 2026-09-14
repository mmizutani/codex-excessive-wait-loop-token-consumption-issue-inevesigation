#!/usr/bin/env python3
"""Export scored traces and comparable totals from completed skill evals."""
import argparse
from collections import defaultdict
import json
from pathlib import Path
from grade import grade

ROOT = Path(__file__).resolve().parents[3]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('phases',nargs='*')
    parser.add_argument('--evidence',type=Path,help='Regrade exported trial-evidence.json without live inference')
    parser.add_argument('--out',type=Path,required=True)
    args = parser.parse_args()
    assert bool(args.phases) != bool(args.evidence), 'Supply phases or --evidence, but not both'
    rows = []
    records = []
    if args.evidence:
        source = json.loads(args.evidence.read_text())
    else:
        source = [{'phase':phase,**json.loads(path.read_text())} for phase in args.phases
            for path in sorted((ROOT/'tmp/wait-skill-evals'/phase).glob('*.json'))]
    for r in source:
        e = grade(r)
        rows.append({'phase':r['phase'],'name':r['name'],'version':r['skill_version'],
            'case':r['eval_case']['id'],'should_trigger':r['eval_case']['should_trigger'],
            'explicit':r['eval_case']['explicit'],'parent_loaded':r['thread_id'] in r['skill_loaded_sessions'],
            'skill_sha256':r['skill_sha256'],**e})
        records.append(r)
    ids = [u['response_id'] for r in records for u in r['response_usage']]
    assert len(ids)==len(set(ids)), 'Repeated response IDs across exported trials'
    groups = defaultdict(list)
    for row in rows:
        groups[(row['phase'],row['version'])].append(row)
    summaries = []
    for (phase,version),items in groups.items():
        good_usage = [r['usage']['combined'] for r in items if 'combined' in r['usage']]
        summaries.append({'phase':phase,'version':version,'trials':len(items),
            'overall_passes':sum(r['overall_pass'] for r in items),
            'check_passes':{k:sum(r['checks'].get(k,False) for r in items) for k in sorted({k for r in items for k in r['checks']})},
            'check_totals':{k:sum(k in r['checks'] for r in items) for k in sorted({k for r in items for k in r['checks']})},
            'responses':sum(r['responses'] for r in good_usage),
            'tokens':{k:sum(r['tokens'].get(k,0) for r in good_usage) for k in ['input','uncached','cached','write','output','reasoning_in_output']},
            'usd':{k:sum(r['usd'].get(k,0) for r in good_usage) for k in ['uncached','cached','write','output','total']}})
    args.out.mkdir(parents=True,exist_ok=True)
    result={'source_phases':list(dict.fromkeys(r['phase'] for r in rows)),
        'unique_response_ids':len(ids),'groups':summaries,'trials':rows,
        'pricing':'September 14, 2026 Standard API valuation of subscription counters; not subscription charges. Recorded write zeros may be unreported.'}
    (args.out/'scores.json').write_text(json.dumps(result,indent=2)+'\n')
    (args.out/'trial-evidence.json').write_text(json.dumps(records,indent=2)+'\n')
    lines=['# Skill evaluation scores','',result['pricing'],'',
        '| Phase | Version / case | Activated | Pass | Failed checks | Responses | Input | Ordinary | Cached reads | Writes | Output | API USD | Delay (s) | Max parent gap (s) |',
        '| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |']
    for row in rows:
        u=row['usage'].get('combined',{}); t=u.get('tokens',{}); usd=u.get('usd',{})
        lines.append(f"| {row['phase']} | {row['version']} / {row['case']} | {row['parent_loaded']} | {row['overall_pass']} | {', '.join(row['failed_checks']) or '—'} | {u.get('responses','?')} | {t.get('input',0):,} | {t.get('uncached',0):,} | {t.get('cached',0):,} | {t.get('write',0):,} | {t.get('output',0):,} | ${usd.get('total',0):.6f} | {row['result_delay_seconds']} | {row['parent_max_gap_seconds']} |")
    (args.out/'SCORES.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps({'trials':len(rows),'groups':summaries},indent=2))


if __name__=='__main__':
    main()
