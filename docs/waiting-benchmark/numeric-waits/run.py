#!/usr/bin/env python3
"""Live Astra numeric-wait comparison; reuses the audited benchmark collector."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import random
import subprocess
import sys
from types import SimpleNamespace

HERE = Path(__file__).resolve().parent
BENCH = HERE.parent
ROOT = BENCH.parents[1]
sys.path.insert(0, str(BENCH))
from benchmark import Trial, prompt_for

MODEL = 'gpt-6-astra'
SEED = 20260914
CELL_PROMPT = '''This is a controlled test of resuming a running Code Mode cell.
Run the following JavaScript through functions.exec exactly as written, including
the first-line 1 ms yield. This initial yield deliberately exposes a running cell;
it overrides the global outer-yield preference for this initial call only.

// @exec: {"yield_time_ms": 1}
text(await tools.exec_command({cmd:"python3 bench_job.py",yield_time_ms:30000,max_output_tokens:1000}));

If a running cell is returned, resume that cell with functions.wait until its
result is received. After that, follow the global waiting instructions to wait
for the same command to finish. No other work is needed. Do not delegate. Run the
command exactly once, do not inspect or modify the supplied benchmark scripts,
and report its exact result only after successful completion.
'''


def write_once(path, text):
    if path.exists():
        assert path.read_text() == text, f'Refusing to change frozen file: {path}'
    else:
        path.write_text(text)


def make_prompts():
    base = (BENCH / 'AGENTS.compact-final.md').read_text()
    phrases = {
        'exec': ('with `yield_time_ms: 30000`, shortened to the budget',
                 'with a long `yield_time_ms` within tool limits and the budget'),
        'stdin': ('use empty `write_stdin` waits within budget',
                  'use empty `write_stdin` waits with `yield_time_ms: 40000`, shortened to the budget'),
        'wait': ('use functions.wait', 'unused'),
    }
    for old, new in list(phrases.values())[:2]:
        assert base.count(old) == 1, old
    result = {}
    for explicit_exec in [False, True]:
        for explicit_stdin in [False, True]:
            name = f'e{int(explicit_exec)}s{int(explicit_stdin)}w0'
            text = base
            if not explicit_exec:
                text = text.replace(*phrases['exec'])
            if explicit_stdin:
                text = text.replace(*phrases['stdin'])
            result[name] = text
    wait_old = 'with `functions.wait` within budget instead of 1-second/default checks'
    wait_new = ('with `functions.wait` using `yield_time_ms: 45000`, shortened to the budget, '
                'instead of 1-second/default checks')
    assert base.count(wait_old) == 1
    result['e1s0w1'] = base.replace(wait_old, wait_new)
    result['e1s1w1'] = result['e1s1w0'].replace(wait_old, wait_new)
    paths = {}
    for name, text in result.items():
        path = HERE / 'prompts' / f'AGENTS.{name}.md'
        write_once(path, text)
        paths[name] = path
    return paths


def make_outer_prompts(paths):
    base = paths['e0s0w0'].read_text()
    original = ('In code mode, set first-line `// @exec: {"yield_time_ms": 45000}`, '
                'adjusted to budget, covering the inner wait plus a small margin.')
    qualitative = ('In code mode, set first-line `@exec` `yield_time_ms` within budget, '
                   'covering the inner wait plus a small margin.')
    assert base.count(original) == 1
    for numeric in [False, True]:
        for named in [False, True]:
            clause = original if numeric else qualitative
            if named:
                clause = clause.replace('set first-line', 'set `functions.exec`\'s first-line', 1)
            name = f'outer-o{int(numeric)}n{int(named)}'
            path = HERE / 'prompts' / f'AGENTS.{name}.md'
            write_once(path, base.replace(original, clause))
            paths[name] = path
    return paths


def make_wording_prompts(paths):
    current = (ROOT / 'docs/waiting-validation/AGENTS.waiting-compatible.md').read_text()
    no_pragma = ('In Code Mode, set the outer `functions.exec` wait long enough to cover '
                 'the inner `exec_command` or `write_stdin` wait plus a small margin, '
                 'while staying within budget.')
    with_pragma = ('In Code Mode, set the outer `functions.exec` wait via first-line '
                   '`@exec` `yield_time_ms` within budget, covering the inner '
                   '`exec_command` or `write_stdin` wait plus a small margin.')
    assert current.count(no_pragma) == 1
    variants = {
        'wording-measured': paths['outer-o0n0'].read_text(),
        'wording-with-pragma': current.replace(no_pragma, with_pragma),
        'wording-no-pragma': current,
    }
    for name, text in variants.items():
        path = HERE / 'prompts' / f'AGENTS.{name}.md'
        write_once(path, text)
        paths[name] = path
    return paths


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--phase', choices=['isolated', 'integration', 'section', 'outer', 'outer-integration', 'outer-subagent', 'outer-ci-name', 'outer-subagent-unnamed', 'wording', 'unpatched'], default='isolated')
    p.add_argument('--selected', default='e1s1w1')
    p.add_argument('--out', type=Path, default=ROOT / 'tmp/wait-benchmark-numeric-waits')
    p.add_argument('--source-home', type=Path, default=ROOT / '.codex_home')
    p.add_argument('--binary', type=Path, default=Path('/opt/homebrew/bin/codex'))
    p.add_argument('--catalog', type=Path, default=ROOT / 'tmp/wait-benchmark-catalog.json')
    p.add_argument('--workers', type=int, default=2)
    p.add_argument('--prepare-only', action='store_true')
    args = p.parse_args()
    args.out = args.out.resolve() / args.phase
    args.out.mkdir(parents=True, exist_ok=True)
    paths = make_prompts()
    if args.phase in ('outer', 'outer-integration', 'outer-subagent', 'outer-ci-name', 'outer-subagent-unnamed', 'wording', 'unpatched'):
        paths = make_outer_prompts(paths)
    if args.phase in ('wording', 'unpatched'):
        paths = make_wording_prompts(paths)
    if args.phase == 'unpatched':
        paths['no-patch'] = None
    if args.phase == 'section':
        base = paths['e1s0w0'].read_text()
        start = base.index('### Terminal commands\n')
        end = base.index('### CI and external work\n', start)
        path = HERE / 'prompts' / 'AGENTS.no-terminal.md'
        write_once(path, base[:start] + base[end:])
        paths['no-terminal'] = path
    version = subprocess.check_output([str(args.binary), '--version'], text=True).strip()
    assert version == 'codex-cli 0.154.0', version
    assert hashlib.sha256(args.catalog.read_bytes()).hexdigest() == 'e17cbd5fba8d477929a6a57f3d522325c488acb5e2f488e267aa59f3f239ba40'
    reps = 3 if args.phase in ('isolated', 'outer', 'unpatched') else 2
    blocks = []
    phase_seed = SEED + {'isolated':0, 'integration':1, 'section':2, 'outer':3, 'outer-integration':4, 'outer-subagent':5, 'outer-ci-name':6, 'outer-subagent-unnamed':7, 'wording':8, 'unpatched':9}[args.phase]
    rng = random.Random(phase_seed)
    for rep in range(1, reps + 1):
        if args.phase == 'isolated':
            pairs = [('terminal', v) for v in ['e0s0w0','e1s0w0','e0s1w0','e1s1w0']]
            pairs += [('cell', v) for v in ['e1s0w0','e1s0w1']]
        elif args.phase == 'section':
            pairs = [(s,v) for s in ['terminal','ci','subagent'] for v in ['e1s0w0','no-terminal']]
        elif args.phase == 'outer':
            pairs = [('terminal',f'outer-o{o}n{n}') for o in [0,1] for n in [0,1]]
        elif args.phase in ('outer-subagent','outer-subagent-unnamed'):
            pairs = [('subagent',v) for v in ['e1s0w0',args.selected]]
        elif args.phase == 'outer-ci-name':
            pairs = [('ci',v) for v in ['outer-o0n0','outer-o0n1']]
        elif args.phase == 'wording':
            pairs = [(s,v) for s in ['terminal','ci','subagent']
                     for v in ['wording-measured','wording-with-pragma','wording-no-pragma']]
        elif args.phase == 'unpatched':
            pairs = [(s,v) for s in ['terminal','ci','subagent']
                     for v in ['no-patch','wording-no-pragma']]
        else:
            assert args.selected != 'e1s0w0', 'Unchanged control needs no integration rerun'
            pairs = [(s,v) for s in ['terminal','ci','subagent'] for v in ['e1s0w0',args.selected]]
        rng.shuffle(pairs)
        blocks.append([{'scenario':s, 'variant':v, 'repetition':rep,
                        'name':f'{MODEL}-{s}-{v}-r{rep}'} for s,v in pairs])
    manifest = {'phase':args.phase, 'cli_version':version,
                'binary':str(args.binary.resolve()), 'catalog_sha256':hashlib.sha256(args.catalog.read_bytes()).hexdigest(),
                'model':MODEL, 'effort':'low', 'delay_seconds':75, 'workers':args.workers,
                'seed':phase_seed, 'blocks':blocks,
                'prompts':{v:({'path':str(path.relative_to(ROOT)), 'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
                              if path is not None else {'path':None,'sha256':None,'installation':'AGENTS.md absent'})
                           for v,path in paths.items()},
                'cell_prompt':CELL_PROMPT}
    if args.phase == 'outer-integration':
        manifest['subagent_fork_policy'] = 'all (explicit task instruction in both conditions)'
    if args.phase in ('outer-subagent','outer-subagent-unnamed','wording','unpatched'):
        manifest['subagent_fork_policy'] = 'all; inherit parent settings; omit model/effort override arguments'
    write_once(HERE / f'{args.phase}-manifest.json', json.dumps(manifest, indent=2) + '\n')
    if args.prepare_only:
        print(json.dumps({'phase':args.phase,'trials':sum(map(len,blocks)),'prepared':True}),flush=True)
        return

    def run(task):
        target = args.out / (task['name'] + '.json')
        if target.exists():
            record = json.loads(target.read_text())
            print(json.dumps({'event':'retained-existing','trial':task['name']}),flush=True)
            return record
        opts = SimpleNamespace(old_binary=args.binary.resolve(), new_binary=args.binary.resolve(),
            patch=paths[task['variant']], tuned_patch=None, effort='low', delay=75,
            catalog=args.catalog.resolve(), source_home=args.source_home.resolve(), no_skill_instructions=True)
        scenario_prompt = CELL_PROMPT if task['scenario']=='cell' else prompt_for(task['scenario'],MODEL)
        if args.phase == 'outer-integration' and task['scenario'] == 'subagent':
            scenario_prompt += '\nFor this controlled comparison, set fork_turns to "all" when spawning the child.\n'
        if args.phase in ('outer-subagent','outer-subagent-unnamed','wording','unpatched') and task['scenario'] == 'subagent':
            original = f'using model `{MODEL}` at low reasoning effort.'
            replacement = ('with `fork_turns: "all"`, inheriting the parent model and reasoning settings. '
                'The parent is already configured as GPT-6 Astra at low reasoning effort. '
                'Omit the model and reasoning_effort override arguments from the spawn call.')
            assert scenario_prompt.count(original) == 1
            scenario_prompt = scenario_prompt.replace(original,replacement)
        condition = 'new' if task['variant'] == 'no-patch' else 'patch'
        record = Trial(args.out,task['name'],MODEL,None).execute(opts,condition,task['scenario'],task['repetition'],
                                                               scenario_prompt=scenario_prompt)
        record['condition'] = task['variant']
        record['phase'] = args.phase
        record['controlled_initial_cell_yield'] = task['scenario']=='cell'
        target.write_text(json.dumps(record,indent=2)+'\n')
        return record

    failed = 0
    for number, block in enumerate(blocks,1):
        print(json.dumps({'event':'block-start','phase':args.phase,'block':number}),flush=True)
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            records = list(pool.map(run,block))
        failed += sum(not r['success'] for r in records)
        print(json.dumps({'event':'block-complete','phase':args.phase,'block':number,'unsuccessful':failed}),flush=True)
    print(json.dumps({'event':'phase-complete','phase':args.phase,'trials':sum(map(len,blocks)),'unsuccessful':failed}),flush=True)


if __name__ == '__main__':
    main()
