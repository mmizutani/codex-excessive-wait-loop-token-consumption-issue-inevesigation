#!/usr/bin/env python3
"""Export command-wait and CI timing evidence from completed wording trials."""
from datetime import datetime
import argparse
import json
from pathlib import Path

from compare import argument_snippets


def process_outputs(value):
    if isinstance(value, str):
        try:
            yield from process_outputs(json.loads(value))
        except (ValueError, TypeError):
            return
    elif isinstance(value, list):
        for item in value:
            yield from process_outputs(item)
    elif isinstance(value, dict):
        if 'chunk_id' in value and 'wall_time_seconds' in value:
            yield value
        for item in value.values():
            if isinstance(item, (dict, list, str)):
                yield from process_outputs(item)


def timestamp(value):
    return datetime.fromisoformat(value.replace('Z', '+00:00')).timestamp()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--phase', choices=['wording', 'unpatched'], default='wording')
    args = parser.parse_args()
    target = Path(__file__).resolve().parent / f'{args.phase}-results'
    records = json.loads((target / 'trial-evidence.json').read_text())
    behaviors = []
    for record in records:
        arguments = argument_snippets(record)
        calls = {c['call_id']: c for c in record['calls']}
        completed_at = next((e['at'] for e in record['job_events'] if e['event'] == 'complete'), None)
        waits = []
        for output in record['tool_outputs']:
            call = calls.get(output['call_id'], {})
            if 'tools.write_stdin' not in call.get('input', ''):
                continue
            for process in process_outputs(output['output']):
                waits.append({
                    'at': output['at'],
                    'wait_ms': [a['yield_time_ms'] for a in arguments
                                if a['tool'] == 'write_stdin' and a['at'] == call.get('at')],
                    'exit_code': process.get('exit_code'),
                    'actual_wall_seconds': process['wall_time_seconds'],
                    'seconds_before_job_completion': round(completed_at - timestamp(output['at']), 6)
                        if completed_at is not None else None,
                })
        row = {
            **{k: record[k] for k in ['name', 'condition', 'scenario', 'repetition']},
            'arguments': [{k: a[k] for k in ['tool', 'yield_time_ms']} for a in arguments],
            'running_cell_returns': sum('Script running with cell ID' in str(o['output'])
                                        for o in record['tool_outputs']),
            'stdin_results': waits,
            'ci_check_count': len(record['ci_checks']),
        }
        if record['ci_checks']:
            start = record['ci_checks'][0]['at']
            row['ci_checks_elapsed_seconds'] = [round(c['at'] - start, 3) for c in record['ci_checks']]
            row['ci_status_at_checks'] = [c['done'] for c in record['ci_checks']]
        if args.phase == 'unpatched':
            row['initial_cell_returns'] = sum(
                calls.get(o['call_id'], {}).get('name') in ('exec', 'functions.exec')
                and 'Script running with cell ID' in str(o['output'])
                for o in record['tool_outputs'])
            row['cell_resumption_calls'] = sum(a['tool'] == 'functions.wait' for a in arguments)
            row['short_stdin_requests'] = sum(
                a['tool'] == 'write_stdin' and isinstance(a['yield_time_ms'], int)
                and a['yield_time_ms'] <= 1000 for a in arguments)
            native_waits = []
            for call in record['calls']:
                name = call.get('name', '')
                if name not in ('wait_agent', 'sleep', 'clock.sleep'):
                    continue
                source = call.get('arguments', call.get('input', '{}'))
                try:
                    parameters = json.loads(source) if isinstance(source, str) else source
                except json.JSONDecodeError:
                    parameters = {'unparsed': source}
                native_waits.append({'at': call['at'], 'tool': name, 'arguments': parameters})
            row['native_waits'] = native_waits
            row['parent_update_cadence_met'] = record['max_parent_message_gap_seconds'] <= 60
            row['waiting_patch_file_present'] = record['waiting_patch_file_present']
            row['waiting_instruction_sessions'] = record['waiting_instruction_sessions']
        behaviors.append(row)
    (target / 'behavior.json').write_text(json.dumps(behaviors, indent=2) + '\n')
    print(f'Exported timing evidence for {len(behaviors)} trials.')


if __name__ == '__main__':
    main()
