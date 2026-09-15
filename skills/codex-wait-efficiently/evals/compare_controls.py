#!/usr/bin/env python3
"""Verify and summarize final-skill/no-skill evidence without model calls."""
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
from statistics import mean

from grade import grade
from compare import argument_snippets

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
TOKEN_KEYS = ['input', 'uncached', 'cached', 'write', 'output', 'reasoning_in_output']
USD_KEYS = ['uncached', 'cached', 'write', 'output', 'total']


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def aggregate(rows):
    scopes = {}
    for scope in ['parent', 'child', 'combined']:
        usage = [r['evaluation']['usage'][scope] for r in rows]
        scopes[scope] = {
            'responses': sum(u['responses'] for u in usage),
            'tokens': {k: sum(u['tokens'].get(k, 0) for u in usage) for k in TOKEN_KEYS},
            'usd': {k: sum(u['usd'].get(k, 0) for u in usage) for k in USD_KEYS},
        }
    delays = [r['result_delay_seconds'] for r in rows if r['result_delay_seconds'] is not None]
    return {
        'trials': len(rows), 'scopes': scopes,
        'correct_outcomes': sum(r['evaluation']['checks']['outcome'] for r in rows),
        'deterministic_passes': sum(r['evaluation']['overall_pass'] for r in rows),
        'parent_skill_loaded': sum(r['thread_id'] in r['skill_loaded_sessions'] for r in rows),
        'children_skill_loaded': sum(r['evaluation']['loaded_child_sessions'] for r in rows),
        'short_stdin_requests': sum(r['evaluation']['short_stdin_requests'] for r in rows),
        'cell_resumptions': sum(r['evaluation']['cell_resumptions'] for r in rows),
        'short_cell_requests': sum(
            a['tool'] == 'functions.wait' and isinstance(a['yield_time_ms'], int) and a['yield_time_ms'] <= 1000
            for r in rows for a in argument_snippets(r)),
        'running_cell_returns': sum('Script running with cell ID' in str(o['output'])
                                    for r in rows for o in r['tool_outputs']),
        'ci_status_requests': sum(len(r['ci_checks']) for r in rows),
        'mean_result_delay_seconds': mean(delays) if delays else None,
        'delay_observations': len(delays),
        'parent_gaps_over_60_seconds': sum(r['max_parent_message_gap_seconds'] > 60 for r in rows),
        'max_parent_gap_seconds': max(r['max_parent_message_gap_seconds'] for r in rows),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--results', type=Path, default=HERE/'comparisons/skill-vs-none')
    args = parser.parse_args()
    manifest = json.loads((args.results/'skill-vs-none.json').read_text())
    records = json.loads((args.results/'trial-evidence.json').read_text())
    expected = {f"{t['version']}-{t['case']['id']}-r{t['repetition']}": t for t in manifest['tasks']}
    assert len(records) == len(expected) == 18
    assert len({r['name'] for r in records}) == len(records)
    assert {r['name'] for r in records} == set(expected)
    assert digest(HERE/'cases.json') == manifest['cases_sha256']
    final_hash = digest(ROOT/'skills/codex-wait-efficiently/SKILL.md')
    assert final_hash == manifest['versions']['v4'] == digest(HERE/'versions/v4/SKILL.md.fixture')
    assert digest(ROOT/'docs/guides/AGENTS.waiting-compatible.md') == '882067320df757cc72afaf1fa542e9c476d0c445d4f52a0ea683eb38e2daa411'
    ids = [u['response_id'] for r in records for u in r['response_usage']]
    assert len(ids) == len(set(ids))
    instruction_hashes = {entry['sha256'] for r in records for entry in r['base_instruction_hashes']}
    assert len(instruction_hashes) == 1, 'Different base instructions across conditions'
    for r in records:
        task = expected[r['name']]
        assert r['eval_case'] == task['case']
        assert r['scenario_prompt'] == task['case']['prompt']
        assert r['skill_version'] == task['version']
        assert r['skill_sha256'] == manifest['versions'][task['version']]
        assert r['catalog_sha256'] == manifest['catalog_sha256']
        assert r['cli_version'] == 'codex-cli 0.154.0'
        assert r['sleep_mode'] == 'default' and not r['patch_sha256']
        assert not r['waiting_patch_file_present'] and not r['global_agents_present']
        assert r['skill_installed'] == (task['version'] == 'v4')
        assert r['evaluation'] == grade(r)
        assert r['evaluation']['checks']['accounting']
        assert r['evaluation']['checks']['isolated_skill']
        assert r['evaluation']['checks']['model_and_effort']
        if task['version'] == 'none':
            assert not r['skill_loaded_sessions']
            assert not any(r['skill_catalog_sessions'].values())
    totals = {v: aggregate([r for r in records if r['skill_version'] == v]) for v in ['none', 'v4']}
    groups = {s: {v: aggregate([r for r in records if r['scenario'] == s and r['skill_version'] == v])
                  for v in ['none', 'v4']} for s in ['terminal', 'subagent', 'ci']}
    by_pair = defaultdict(dict)
    for r in records:
        by_pair[(r['eval_case']['id'], r['repetition'])][r['skill_version']] = r
    pairs = []
    for (case, repetition), pair in sorted(by_pair.items()):
        assert set(pair) == {'none', 'v4'}
        a, b = pair['none'], pair['v4']
        assert a['scenario_prompt'] == b['scenario_prompt']
        ua, ub = [r['evaluation']['usage']['combined'] for r in [a, b]]
        pairs.append({'case': case, 'repetition': repetition,
            'none': a['name'], 'v4': b['name'],
            'response_delta': ub['responses'] - ua['responses'],
            'token_deltas': {k: ub['tokens'].get(k, 0) - ua['tokens'].get(k, 0) for k in TOKEN_KEYS},
            'usd_delta': ub['usd']['total'] - ua['usd']['total'],
            'result_delay_delta_seconds': b['result_delay_seconds'] - a['result_delay_seconds']
                if a['result_delay_seconds'] is not None and b['result_delay_seconds'] is not None else None})
    a, b = [totals[v]['scopes']['combined'] for v in ['none', 'v4']]
    reductions = {
        'responses_percent': 100 * (1 - b['responses']/a['responses']),
        'input_percent': 100 * (1 - b['tokens']['input']/a['tokens']['input']),
        'usd_percent': 100 * (1 - b['usd']['total']/a['usd']['total']),
    }
    result = {'trials': len(records), 'pairs': len(pairs), 'unique_responses': len(ids),
        'final_skill_sha256': final_hash, 'totals': totals, 'by_scenario': groups,
        'reductions': reductions, 'paired_deltas': pairs,
        'fewer_responses_pairs': sum(p['response_delta'] < 0 for p in pairs),
        'lower_input_pairs': sum(p['token_deltas']['input'] < 0 for p in pairs),
        'lower_usd_pairs': sum(p['usd_delta'] < 0 for p in pairs),
        'slower_delivery_pairs': sum(p['result_delay_delta_seconds'] is not None
                                     and p['result_delay_delta_seconds'] > 0 for p in pairs),
        'retained_failures': [{'name': r['name'], 'checks': r['evaluation']['failed_checks']}
                              for r in records if not r['evaluation']['overall_pass']],
        'all_accounting_reconciled': True, 'condition_isolation_verified': True,
        'base_instruction_sha256': next(iter(instruction_hashes)),
        'frozen_inputs_match': True, 'agents_patch_unchanged': True,
        'pricing': 'September 14, 2026 Standard API valuation of subscription counters; not subscription charges. Recorded write zeros can represent unreported fields.'}
    (args.results/'comparison.json').write_text(json.dumps(result, indent=2)+'\n')
    lines = ['# Final skill versus no skill: recorded counts', '', result['pricing'], '',
        'Each condition contains nine trials. Counts include parent and child inference and skill loading. Input includes cached reads and recorded writes; reasoning is already included in output.', '',
        '| Metric | No skill | Final v4 skill |', '| --- | ---: | ---: |',
        f"| Model responses | {a['responses']:,} | {b['responses']:,} |"]
    for key, label in [('input', 'Input total'), ('uncached', 'Ordinary input'), ('cached', 'Cached reads'),
                       ('write', 'Recorded cache writes'), ('output', 'Output'), ('reasoning_in_output', 'Reasoning included in output')]:
        lines.append(f"| {label} | {a['tokens'][key]:,} | {b['tokens'][key]:,} |")
    for key in USD_KEYS:
        lines.append(f"| API USD: {key} | ${a['usd'][key]:.6f} | ${b['usd'][key]:.6f} |")
    lines += ['', '## Workloads', '',
        '| Workload | Responses: no skill → v4 | Input: no skill → v4 | API USD: no skill → v4 | Mean delivery delay: no skill → v4 |',
        '| --- | ---: | ---: | ---: | ---: |']
    for scenario, group in groups.items():
        a, b = [group[v]['scopes']['combined'] for v in ['none', 'v4']]
        da, db = [group[v]['mean_result_delay_seconds'] for v in ['none', 'v4']]
        delay = f'{da:.3f} s → {db:.3f} s' if da is not None and db is not None else 'unavailable'
        lines.append(f"| {scenario} | {a['responses']} → {b['responses']} | {a['tokens']['input']:,} → {b['tokens']['input']:,} | ${a['usd']['total']:.6f} → ${b['usd']['total']:.6f} | {delay} |")
    lines += ['', '## Parent and child accounting', '',
        '| Trial | Scope | Responses | Input | Ordinary | Cached reads | Recorded writes | Output | Ordinary USD | Cached USD | Write USD | Output USD | Total USD |',
        '| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |']
    for r in records:
        for scope in ['parent', 'child', 'combined']:
            u = r['evaluation']['usage'][scope]
            if not u['responses']:
                continue
            values = [r['name'], scope, str(u['responses'])]
            values += [f"{u['tokens'].get(k, 0):,}" for k in TOKEN_KEYS[:-1]]
            values += [f"${u['usd'].get(k, 0):.6f}" for k in USD_KEYS]
            lines.append('| '+' | '.join(values)+' |')
    lines += ['', '## Matched changes', '', 'Deltas are v4 minus no skill. Negative usage deltas mean lower usage; positive delay deltas mean slower result delivery.', '',
        '| Case / repetition | Responses delta | Input delta | API USD delta | Delivery delay delta (s) |',
        '| --- | ---: | ---: | ---: | ---: |']
    for p in pairs:
        delay = p['result_delay_delta_seconds']
        delay_text = f'{delay:+.3f}' if delay is not None else 'unavailable'
        lines.append(f"| {p['case']} / {p['repetition']} | {p['response_delta']:+d} | {p['token_deltas']['input']:+,} | ${p['usd_delta']:+.6f} | {delay_text} |")
    (args.results/'COUNTS.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps({k: result[k] for k in ['trials', 'unique_responses', 'reductions', 'fewer_responses_pairs', 'lower_input_pairs', 'lower_usd_pairs', 'slower_delivery_pairs', 'retained_failures']}, indent=2))


if __name__ == '__main__':
    main()
