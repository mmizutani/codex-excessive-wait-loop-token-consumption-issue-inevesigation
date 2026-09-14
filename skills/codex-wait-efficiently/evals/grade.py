"""Deterministic outcome, activation, process, and accounting checks."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT/'docs/waiting-benchmark/numeric-waits'), str(ROOT/'docs/waiting-benchmark')]
from analyze import analyze
from compare import argument_snippets, returned_process_results


def grade(record):
    case = record['eval_case']
    finals = [m['text'] for m in record['messages'] if m['session_id']==record.get('thread_id')
              and m['phase'] in ('final','final_answer')]
    final = finals[-1] if finals else ''
    processes = [p for o in record['tool_outputs'] for p in returned_process_results(o['output'])]
    fixture = case.get('fixture')
    completed_turn = record.get('status') == 'completed' and bool(finals)
    checks = {'turn_completed':completed_turn,
        'activation':(record.get('thread_id') in record['skill_loaded_sessions']) == case['should_trigger'],
        'isolated_skill':record['enabled_skills']==['codex-wait-efficiently'] and not record['global_agents_present'],
        'fixtures_preserved':not record['fixture_changes'],
        'child_count':record['child_session_count']==(1 if case['scenario']=='subagent' else 0),
        'model_and_effort':bool(record['model_contexts']) and all(c['model']=='gpt-6-astra' and c['effort']=='low' for c in record['model_contexts'])}
    checks['no_extra_job'] = record['job_launches'] == (1 if case['scenario'] in ('terminal','subagent')
        and fixture not in ('quick','explanation','edit') else 0)
    if fixture == 'failure':
        checks['outcome'] = (completed_turn and any(p['exit_code']==7 for p in processes)
            and 'BENCH_FAILURE_7391' in final and '7' in final and 'BENCH_RESULT_7391' not in final)
    elif fixture == 'pending':
        count = len(record['ci_checks'])
        bound = 1 if case['id']=='negative-one-status' else 3
        checks['status_query_bound'] = 1 <= count <= bound
        checks['outcome'] = (completed_turn and checks['status_query_bound']
            and not any(c['done'] for c in record['ci_checks'])
            and any(word in final.lower() for word in ['running','pending','in progress'])
            and 'BENCH_RESULT_7391' not in final)
    elif fixture == 'quick':
        checks['outcome'] = completed_turn and final.strip().strip('`').strip() == '42'
    elif fixture == 'explanation':
        checks['outcome'] = completed_turn and all(w in final.lower() for w in ['wait','sleep']) and not record['calls']
    elif fixture == 'edit':
        checks['outcome'] = completed_turn and record['artifacts'].get('README.md',{}).get('text')=='Polling CI status is optional.\n'
    else:
        checks['outcome'] = record['success'] and any(p['exit_code']==0 and 'BENCH_RESULT_7391' in str(p.get('output','')) for p in processes)
    if fixture == 'independent':
        artifact = record['artifacts'].get('summary.json',{})
        try:
            correct_sum = json.loads(artifact.get('text','')) == {'sum':81}
        except (ValueError,TypeError):
            correct_sum = False
        times = {e['event']:e['at'] for e in record['job_events']}
        checks['independent_work'] = (correct_sum and times.get('start',float('inf'))
            < artifact.get('modified_at',0) < times.get('complete',0))
    args = argument_snippets(record)
    short_polls = sum(a['tool']=='write_stdin' and isinstance(a['yield_time_ms'],int)
                      and a['yield_time_ms']<=1000 for a in args)
    cell_waits = [a for a in args if a['tool']=='functions.wait']
    if case['should_trigger']:
        checks['no_short_stdin_polls'] = short_polls == 0
        checks['no_short_cell_polls'] = all(isinstance(a['yield_time_ms'],int)
            and a['yield_time_ms']>1000 for a in cell_waits)
        checks['parent_update_cadence'] = record['max_parent_message_gap_seconds'] <= 60
    if case['id']=='explicit-cell':
        checks['forced_cell_exercised'] = bool(cell_waits) and any(
            'Script running with cell ID' in str(o['output']) for o in record['tool_outputs'])
    try:
        usage = analyze(record)['scopes']
        sessions = {r['session_id'] for r in record['response_usage']}
        checks['accounting'] = sessions == set(record['cumulative_final_by_session'])
    except (AssertionError,KeyError,ValueError) as error:
        usage = {'error':str(error)}
        checks['accounting'] = False
    return {'overall_pass':all(checks.values()), 'checks':checks,
        'failed_checks':[k for k,v in checks.items() if not v],
        'short_stdin_requests':short_polls, 'cell_resumptions':len(cell_waits),
        'loaded_child_sessions':len(set(record['skill_loaded_sessions'])-{record.get('thread_id')}),
        'usage':usage, 'parent_max_gap_seconds':record['max_parent_message_gap_seconds'],
        'result_delay_seconds':record['result_delay_seconds']}
