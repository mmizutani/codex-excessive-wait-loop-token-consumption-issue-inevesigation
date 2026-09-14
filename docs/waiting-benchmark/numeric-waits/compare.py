#!/usr/bin/env python3
"""Summarize numeric-wait trials without conflating cache shifts with responses."""
import argparse
from collections import defaultdict
import json
from pathlib import Path
import re
from statistics import mean
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
from analyze import analyze
from benchmark import RESULT


def returned_process_results(value):
    if isinstance(value,str):
        try:
            yield from returned_process_results(json.loads(value))
        except (ValueError,TypeError):
            return
    elif isinstance(value,list):
        for item in value:
            yield from returned_process_results(item)
    elif isinstance(value,dict):
        if 'exit_code' in value:
            yield value
        for item in value.values():
            if isinstance(item,(dict,list,str)):
                yield from returned_process_results(item)


def acceptance(record):
    usage_sessions={r['session_id'] for r in record['response_usage']}
    cumulative_sessions=set(record['cumulative_final_by_session'])
    finals=[m['text'].strip().strip('`').strip() for m in record['messages']
            if m['session_id']==record['thread_id'] and m['phase'] in ('final','final_answer')]
    processes=[p for o in record['tool_outputs'] for p in returned_process_results(o['output'])]
    checks={
        'reported_success':record['success'],
        'usage_sessions_have_cumulative':usage_sessions==cumulative_sessions,
        'all_contexts_low':bool(record['model_contexts']) and all(c['effort']=='low' for c in record['model_contexts']),
        'exact_final_result':bool(finals) and finals[-1]==RESULT,
        'exit_zero_with_result':any(p['exit_code']==0 and RESULT in str(p.get('output','')) for p in processes),
        'expected_child_count':record['child_session_count']==(1 if record['scenario']=='subagent' else 0),
        'one_job':record['job_launches']==(0 if record['scenario']=='ci' else 1),
    }
    if record.get('controlled_initial_cell_yield'):
        arguments=argument_snippets(record)
        outer=[a for a in arguments if a['tool']=='functions.exec']
        inner=[a for a in arguments if a['tool']=='exec_command']
        checks['forced_cell_path_observed']=bool(outer and inner and outer[0]['yield_time_ms']==1
            and inner[0]['yield_time_ms']==30000 and any(a['tool']=='functions.wait' for a in arguments))
    if record.get('phase') in ('outer-integration','outer-subagent','outer-subagent-unnamed') and record['scenario'] == 'subagent':
        spawns=[json.loads(c['arguments']) for c in record['calls'] if c.get('name') == 'spawn_agent']
        checks['requested_fork_all']=len(spawns)==1 and spawns[0].get('fork_turns')=='all'
        if record.get('phase') in ('outer-subagent','outer-subagent-unnamed'):
            checks['no_fork_overrides']=len(spawns)==1 and not any(k in spawns[0] for k in ['model','reasoning_effort'])
    return checks


def argument_snippets(record):
    """Retain exact call text for review; numbers are literal-only diagnostics."""
    rows=[]
    for call in record['calls']:
        source=call.get('input',call.get('arguments',''))
        if not isinstance(source,str):
            source=json.dumps(source)
        name=call.get('name','')
        if name in ('wait','functions.wait'):
            try:
                args=json.loads(source)
            except json.JSONDecodeError:
                args={}
            rows.append({'at':call['at'],'session_id':call['session_id'],'tool':'functions.wait',
                         'yield_time_ms':args.get('yield_time_ms','omitted'),'source':source})
        elif name in ('exec','functions.exec'):
            pragma=re.search(r'^\s*//\s*@exec:\s*(\{[^\n]*\})',source)
            try:
                outer=json.loads(pragma.group(1)).get('yield_time_ms','omitted') if pragma else 'omitted'
            except json.JSONDecodeError:
                outer='unparsed'
            rows.append({'at':call['at'],'session_id':call['session_id'],'tool':'functions.exec',
                         'yield_time_ms':outer,'source':source})
            for match in re.finditer(r'tools\.(exec_command|write_stdin)\s*\(',source):
                # Literal projection only. Exact source remains the authority.
                tail=source[match.end():]
                next_call=re.search(r'tools\.\w+\s*\(',tail)
                if next_call:
                    tail=tail[:next_call.start()]
                duration=re.search(r'[\"\']?yield_time_ms[\"\']?\s*:\s*([\d_]+)',tail)
                value=int(duration.group(1).replace('_','')) if duration else 'omitted-or-expression'
                rows.append({'at':call['at'],'session_id':call['session_id'],'tool':match.group(1),
                             'yield_time_ms':value,'source':tail})
        elif name in ('exec_command','write_stdin'):
            args=json.loads(source)
            rows.append({'at':call['at'],'session_id':call['session_id'],'tool':name,
                         'yield_time_ms':args.get('yield_time_ms','omitted'),'source':source})
    return rows


def aggregate(rows):
    tokens=defaultdict(int)
    usd=defaultdict(float)
    for row in rows:
        for k,v in row['scopes']['combined']['tokens'].items(): tokens[k]+=v
        for k,v in row['scopes']['combined']['usd'].items(): usd[k]+=v
    delays=[r['result_delay_seconds'] for r in rows if r['result_delay_seconds'] is not None]
    return {'n':len(rows),'responses':sum(r['scopes']['combined']['responses'] for r in rows),
            'successes':sum(r['success'] for r in rows),'tokens':dict(tokens),'usd':dict(usd),
            'delay_mean':mean(delays) if delays else None,
            'max_update_gap':max((r['max_parent_message_gap_seconds'] for r in rows),default=0),
            'over_60':sum(r['max_parent_message_gap_seconds']>60 for r in rows)}


def main():
    p=argparse.ArgumentParser()
    p.add_argument('directory',type=Path)
    p.add_argument('--out',type=Path,required=True)
    args=p.parse_args()
    records=[json.loads(path.read_text()) for path in sorted(args.directory.glob('gpt-*.json'))]
    rows=[analyze(r) for r in records]
    by_key={(r['scenario'],r['condition'],r['repetition']):r for r in rows}
    grouped=defaultdict(list)
    for row in rows: grouped[(row['scenario'],row['condition'])].append(row)
    groups=[{'scenario':s,'condition':v,**aggregate(rs)} for (s,v),rs in sorted(grouped.items())]
    effects=[]
    definitions=[('exec_command','terminal',[('e0s0w0','e1s0w0'),('e0s1w0','e1s1w0')]),
                 ('write_stdin','terminal',[('e0s0w0','e0s1w0'),('e1s0w0','e1s1w0')]),
                 ('functions.wait','cell',[('e1s0w0','e1s0w1')])]
    for tool,scenario,variants in definitions:
        pairs=[]
        for before,after in variants:
            for rep in sorted({r['repetition'] for r in rows}):
                a,b=by_key.get((scenario,before,rep)),by_key.get((scenario,after,rep))
                if a and b: pairs.append((a,b))
        if not pairs: continue
        effects.append({'tool':tool,'pairs':len(pairs),'qualitative':aggregate([a for a,b in pairs]),
                        'numeric':aggregate([b for a,b in pairs]),
                        'pair_details':[{'qualitative':a['name'],'numeric':b['name'],
                          'response_delta':b['scopes']['combined']['responses']-a['scopes']['combined']['responses'],
                          'usd_delta':b['scopes']['combined']['usd']['total']-a['scopes']['combined']['usd']['total'],
                          'input_delta':b['scopes']['combined']['tokens']['input']-a['scopes']['combined']['tokens']['input'],
                          'delay_delta':b['result_delay_seconds']-a['result_delay_seconds']
                             if b['result_delay_seconds'] is not None and a['result_delay_seconds'] is not None else None}
                         for a,b in pairs]})
    outer_effects=[]
    outer_definitions=[
        ('outer_number',[('outer-o0n0','outer-o1n0'),('outer-o0n1','outer-o1n1')]),
        ('explicit_tool_name',[('outer-o0n0','outer-o0n1'),('outer-o1n0','outer-o1n1')]),
    ]
    for factor,variants in outer_definitions:
        pairs=[]
        for before,after in variants:
            for rep in sorted({r['repetition'] for r in rows}):
                a,b=by_key.get(('terminal',before,rep)),by_key.get(('terminal',after,rep))
                if a and b: pairs.append((a,b))
        if pairs:
            outer_effects.append({'factor':factor,'pairs':len(pairs),
                'without':aggregate([a for a,b in pairs]),'with':aggregate([b for a,b in pairs]),
                'pair_details':[{'without':a['name'],'with':b['name'],
                    'response_delta':b['scopes']['combined']['responses']-a['scopes']['combined']['responses'],
                    'input_delta':b['scopes']['combined']['tokens']['input']-a['scopes']['combined']['tokens']['input'],
                    'usd_delta':b['scopes']['combined']['usd']['total']-a['scopes']['combined']['usd']['total'],
                    'delay_delta':b['result_delay_seconds']-a['result_delay_seconds']}
                    for a,b in pairs]})
    evidence=[{'name':r['name'],'arguments':argument_snippets(r),'acceptance':acceptance(r),
               'running_cell_returns':sum('Script running with cell ID' in str(o['output']) for o in r['tool_outputs']),
               'model_contexts':r['model_contexts'],'messages':r['messages']} for r in records]
    response_ids=[u['response_id'] for r in records for u in r['response_usage']]
    assert len(response_ids)==len(set(response_ids)), 'Cross-trial response duplication'
    result={'groups':groups,'effects':effects,'outer_effects':outer_effects,'all_trials':aggregate(rows),
            'acceptance':{r['name']:r['acceptance'] for r in evidence},
            'unique_response_ids':len(response_ids),'trials':rows}
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/'comparison.json').write_text(json.dumps(result,indent=2)+'\n')
    (args.out/'argument-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n')
    lines=['# Numeric wait measurements','',
        'Astra / low, CLI 0.154.0, shared skills disabled. Each row is a sum of fresh trials.',
        'USD uses the dated API rates; cache-write zeros may be unreported values. This is not a subscription bill.','',
        '| Scenario | Variant | n | Responses | Input | Uncached | Cached | Writes | Output | API USD | Mean result delay (s) | Max update gap (s) | Gaps >60 s (trials) |',
        '|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
    for g in groups:
        lines.append('| '+' | '.join([g['scenario'],g['condition'],str(g['n']),str(g['responses'])]+[
            f"{g['tokens'].get(k,0):,}" for k in ['input','uncached','cached','write','output']]+[
            f"${g['usd']['total']:.6f}",f"{g['delay_mean']:.3f}" if g['delay_mean'] is not None else 'N/A',
            f"{g['max_update_gap']:.3f}",str(g['over_60'])])+' |')
    lines+=['','## Actual wait arguments','',
            '| Trial | exec_command ms | write_stdin ms | functions.exec ms | functions.wait ms | Running-cell returns |',
            '|---|---|---|---|---|---:|']
    for row in evidence:
        cells=[]
        for tool in ['exec_command','write_stdin','functions.exec','functions.wait']:
            cells.append(', '.join(str(c['yield_time_ms']) for c in row['arguments'] if c['tool']==tool) or '—')
        lines.append('| '+row['name']+' | '+' | '.join(cells)+' | '+str(row['running_cell_returns'])+' |')
    (args.out/'COMPARISON.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps({'groups':groups,'effects':effects,'total':result['all_trials']},indent=2))


if __name__=='__main__': main()
