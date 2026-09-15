#!/usr/bin/env python3
"""Verify trials and export raw counts plus API-price equivalents."""
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
from statistics import mean
from accounting import price_response, RATES
from patch_paths import resolve_patch_path

def analyze(record):
    assert record['response_usage'], f"No model usage: {record['name']}"
    assert len({r['response_id'] for r in record['response_usage']}) == len(record['response_usage'])
    for row in record['response_usage']:
        u=row['usage']
        assert u['input_tokens']+u['output_tokens']==u['total_tokens'],record['name']
    for session in record.get('cumulative_final_by_session',{}):
        entries=[r['usage'] for r in record['response_usage'] if r['session_id']==session]
        final=record['cumulative_final_by_session'][session]
        for key in ['input_tokens','cached_input_tokens','cache_write_input_tokens','output_tokens','total_tokens']:
            assert sum(u.get(key,0) for u in entries)==final.get(key,0), (record['name'],session,key)
    if record['patch_sha256']:
        assert record['prompt_loaded'], f"Patch was not loaded: {record['name']}"
        assert hashlib.sha256(resolve_patch_path(record['patch_file']).read_bytes()).hexdigest() == record['patch_sha256']
    if record['success'] and record['scenario'] != 'ci':
        assert record['job_launches'] == 1, f"Duplicate job: {record['name']}"
    if record.get('skills_mode') == 'instructions_disabled':
        assert not record['skills_instruction_sessions'], record['name']
        assert not any('SKILL.md' in str(c) for c in record['calls']), record['name']
    for context in record['model_contexts']:
        assert context['model'] == record['model'], (record['name'], context)
    scopes = {}
    for scope in ['parent', 'child', 'combined']:
        rows = [r for r in record['response_usage'] if scope == 'combined' or
                (r['session_id'] == record['thread_id']) == (scope == 'parent')]
        usd = defaultdict(float)
        counters = defaultdict(int)
        for row in rows:
            priced = price_response(record['model'], row['usage'])
            for key, val in priced['counts'].items():
                counters[key] += val
            for key, val in priced['usd'].items():
                usd[key] += val
            usd['total'] += priced['total_usd']
            counters['reasoning_in_output'] += row['usage'].get('reasoning_output_tokens', 0)
        scopes[scope] = {'responses': len(rows), 'tokens': dict(counters), 'usd': dict(usd)}
    return {**{k:record[k] for k in ['name','model','scenario','condition','repetition','status',
        'success','delay_seconds','effort','cli_version','sleep_mode','patch_sha256','catalog_sha256',
        'job_launches','child_session_count','result_delay_seconds','max_parent_message_gap_seconds']},
        'ci_check_count':len(record['ci_checks']),
        'skills_mode':record.get('skills_mode', 'ambient'), 'scopes':scopes}

def main():
    p=argparse.ArgumentParser()
    p.add_argument('trials',type=Path)
    p.add_argument('--out',type=Path,required=True)
    args=p.parse_args()
    args.out.mkdir(parents=True,exist_ok=True)
    records=[json.loads(f.read_text()) for f in sorted(args.trials.glob('gpt-*.json'))]
    rows=[analyze(r) for r in records]
    groups=defaultdict(list)
    for row in rows:
        groups[(row['model'],row['scenario'],row['condition'])].append(row)
    summaries=[]
    for (model,scenario,condition),items in groups.items():
        summaries.append({'model':model,'scenario':scenario,'condition':condition,'n':len(items),
            'successes':sum(r['success'] for r in items),
            'parent_responses_mean':mean(r['scopes']['parent']['responses'] for r in items),
            'combined_usd_mean':mean(r['scopes']['combined']['usd']['total'] for r in items),
            'parent_usd_mean':mean(r['scopes']['parent']['usd']['total'] for r in items),
            'combined_usd_categories_mean':{k:mean(r['scopes']['combined']['usd'].get(k,0) for r in items)
                for k in ['uncached','cached','write','output']},
            'result_delay_mean':mean(r['result_delay_seconds'] for r in items if r['result_delay_seconds'] is not None),
            'max_message_gap':max(r['max_parent_message_gap_seconds'] for r in items),
            'combined_tokens_mean':{k:mean(r['scopes']['combined']['tokens'].get(k,0) for r in items)
                for k in ['input','uncached','cached','write','output','reasoning_in_output']}})
    result={'pricing':{'date':'2026-09-14','unit':'USD per 1M tokens','rates':RATES,
        'source':'https://developers.openai.com/api/docs/pricing',
        'scope':'Standard API valuation of reported subscription token categories; not an account bill.',
        'long_context':'Above 272000 input tokens per request: 2x all input categories, 1.5x output.',
        'cache_write_caveat':'Codex can default an absent upstream cache-write field to zero.'},
        'trials':rows,'groups':summaries}
    (args.out/'metrics.json').write_text(json.dumps(result,indent=2)+'\n')
    (args.out/'trial-evidence.json').write_text(json.dumps(records,indent=2)+'\n')
    lines=['# Recorded waiting trials','',
        'API-price equivalents value the reported token categories at Standard rates. They are not subscription charges.',
        'Input is the inclusive total. Ordinary input = input − cached reads − cache writes. Reasoning is included in output.',
        '','| Trial | Success | Parent responses | Input total | Ordinary input | Cached reads | Cache writes | Output | Included reasoning | Parent USD | Child USD | Combined USD |',
        '|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
    for row in rows:
        c=row['scopes']['combined']['tokens']
        scopes=row['scopes']
        lines.append('| '+ ' | '.join([row['name'],str(row['success']),str(scopes['parent']['responses'])]+
            [f"{c.get(k,0):,}" for k in ['input','uncached','cached','write','output','reasoning_in_output']]+
            [f"${scopes[s]['usd'].get('total',0):.6f}" for s in ['parent','child','combined']])+' |')
    lines.extend(['', '## API-price breakdown', '',
        'These disjoint dollar categories sum to Combined USD above; total input is not charged again.', '',
        '| Trial | Ordinary input USD | Cached-read USD | Cache-write USD | Output USD |',
        '|---|---:|---:|---:|---:|'])
    for row in rows:
        usd=row['scopes']['combined']['usd']
        lines.append('| '+row['name']+' | '+' | '.join(f"${usd.get(k,0):.6f}" for k in
            ['uncached','cached','write','output'])+' |')
    lines.extend(['', '## Parent and child token counts', '',
        '| Trial | Scope | Responses | Input total | Ordinary input | Cached reads | Cache writes | Output |',
        '|---|---|---:|---:|---:|---:|---:|---:|---:|'])
    for row in rows:
        for scope in ['parent','child']:
            s=row['scopes'][scope]
            if not s['responses']:continue
            lines.append('| '+row['name']+' | '+scope+' | '+str(s['responses'])+' | '+
                ' | '.join(f"{s['tokens'].get(k,0):,}" for k in ['input','uncached','cached','write','output'])+' |')
    (args.out/'COUNTS.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps(summaries,indent=2))

if __name__=='__main__':
    main()
