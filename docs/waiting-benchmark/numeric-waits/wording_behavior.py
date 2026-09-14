#!/usr/bin/env python3
"""Export command-wait and CI timing evidence from completed wording trials."""
from datetime import datetime
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
    target = Path(__file__).resolve().parent / 'wording-results'
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
        behaviors.append(row)
    (target / 'behavior.json').write_text(json.dumps(behaviors, indent=2) + '\n')
    print(f'Exported timing evidence for {len(behaviors)} trials.')


if __name__ == '__main__':
    main()
