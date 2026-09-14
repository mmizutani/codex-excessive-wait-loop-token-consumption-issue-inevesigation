#!/usr/bin/env python3
"""Run bounded real Codex skill evals; consumes normal subscription usage."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import random
import shutil
import subprocess
import sys
import tempfile
import threading
from types import SimpleNamespace

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path[:0] = [str(ROOT/'docs/waiting-benchmark/numeric-waits'),
               str(ROOT/'docs/waiting-benchmark'), str(ROOT/'docs/waiting-validation')]
from benchmark import Trial
from runtime_probe import Probe
from grade import grade

NAME = 'codex-wait-efficiently'
MARKER = 'Longer waits may not reduce usage; add no cache-only keepalives without measured savings.'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_once(path, value):
    text = json.dumps(value, indent=2) + '\n'
    if path.exists():
        assert path.read_text() == text, f'Refusing to change frozen file: {path}'
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)


def other_skill_names(binary):
    """Discover names to disable using only skills/list, with no model turn."""
    with tempfile.TemporaryDirectory(prefix='codex-eval-catalog-') as tmp:
        home = Path(tmp)
        (home/'config.toml').write_text('[skills.bundled]\nenabled = false\n')
        env = os.environ.copy()
        env['CODEX_HOME'] = tmp
        for key in ['OPENAI_API_KEY', 'CODEX_API_KEY']:
            env.pop(key, None)
        probe = Probe(home, 'catalog', None, None)
        probe.process = subprocess.Popen([str(binary), 'app-server'], stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, env=env, cwd=tmp)
        try:
            threading.Thread(target=probe.read, daemon=True).start()
            probe.rpc('initialize', {'clientInfo': {'name':'skill_eval_catalog','version':'1'},
                                    'capabilities': {'experimentalApi':True}})
            probe.send({'method':'initialized','params':{}})
            reply = probe.rpc('skills/list', {'cwds':[tmp], 'forceReload':True})
            return sorted({s['name'] for d in reply['data'] for s in d['skills'] if s['name'] != NAME})
        finally:
            probe.process.terminate()
            try:
                probe.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                probe.process.kill()
                probe.process.wait()


def run_case(args, task, disabled):
    case = task['case']
    installed = task['version'] != 'none'
    version = HERE/'versions'/task['version'] if installed else None
    assert installed or not case['explicit'], 'No-skill controls must use unnamed task prompts'
    name = f"{task['version']}-{case['id']}-r{task['repetition']}"
    target = args.out/(name+'.json')
    if target.exists():
        return json.loads(target.read_text())
    evidence = {}
    options = SimpleNamespace(old_binary=args.binary, new_binary=args.binary,
        patch=None, tuned_patch=None, source_home=args.source_home, catalog=args.catalog,
        effort='low', delay=case['delay'], no_skill_instructions=False,
        timeout_seconds=case.get('deadline_seconds', max(90, case['delay']+100)))
    trial = Trial(args.out, name, 'gpt-6-astra', None)

    def prepare(home, work, config, record):
        if installed:
            shutil.copytree(version, home/'skills'/NAME)
            (home/'skills'/NAME/'SKILL.md.fixture').rename(home/'skills'/NAME/'SKILL.md')
        config.extend(['[skills.bundled]', 'enabled = false'])
        for skill_name in disabled + ([] if installed else [NAME]):
            config.extend(['[[skills.config]]', f'name = {json.dumps(skill_name)}', 'enabled = false'])
        fixture = case.get('fixture')
        if fixture == 'failure':
            path = work/'bench_job.py'
            path.write_text(path.read_text().replace('BENCH_RESULT_7391', 'BENCH_FAILURE_7391')+'\nraise SystemExit(7)\n')
        if fixture == 'independent':
            (work/'numbers.json').write_text('[17, 23, 41]\n')
        if fixture == 'edit':
            (work/'README.md').write_text('Polling CI sttaus is optional.\n')
        record['fixture_hashes_before'] = {p.name:digest(p) for p in work.iterdir() if p.is_file()}
        evidence['home'] = home
        evidence['work'] = work

    def inputs(home, work):
        reply = trial.rpc('skills/list', {'cwds':[str(work)], 'forceReload':True})
        enabled = [s for d in reply['data'] for s in d['skills'] if s.get('enabled')]
        expected = [NAME] if installed else []
        assert [s['name'] for s in enabled] == expected, f'Unexpected enabled skills: {[s["name"] for s in enabled]}'
        evidence['enabled_skills'] = [s['name'] for s in enabled]
        if case['explicit']:
            return [{'type':'skill', 'name':NAME, 'path':str(home/'skills'/NAME/'SKILL.md')}]
        return []

    def inspect(home, work, record):
        injected = set()
        catalogs = {}
        for path in (home/'sessions').rglob('*.jsonl'):
            rows = [json.loads(line) for line in path.read_text().splitlines() if line]
            sid = next(r['payload']['id'] for r in rows if r.get('type') == 'session_meta')
            for row in rows:
                p = row.get('payload', {})
                if row.get('type') != 'response_item' or p.get('type') != 'message' or p.get('role') == 'assistant':
                    continue
                text = '\n'.join(c.get('text','') for c in p.get('content',[]))
                if MARKER in text:
                    injected.add(sid)
                if '<skills_instructions>' in text or '### Available skills' in text:
                    catalogs[sid] = NAME in text
        calls = {c['call_id']:c for c in record['calls']}
        read_sessions = {calls[o['call_id']]['session_id'] for o in record['tool_outputs']
                         if o['call_id'] in calls and MARKER in str(o['output'])}
        artifacts = {str(p.relative_to(work)):{'sha256':digest(p), 'size':p.stat().st_size,
                    'modified_at':p.stat().st_mtime, 'text':p.read_text(errors='replace')[:20000]}
                    for p in work.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
        immutable = set(record['fixture_hashes_before']) - ({'README.md'} if case.get('fixture') == 'edit' else set())
        changed = [p for p in immutable if p not in artifacts or artifacts[p]['sha256'] != record['fixture_hashes_before'][p]]
        record.update({'eval_case':case, 'skill_version':task['version'],
            'skill_sha256':digest(version/'SKILL.md.fixture') if installed else None,
            'skill_installed':installed, 'enabled_skills':evidence.get('enabled_skills',[]),
            'skill_injected_sessions':sorted(injected), 'skill_read_sessions':sorted(read_sessions),
            'skill_loaded_sessions':sorted(injected | read_sessions), 'skill_catalog_sessions':catalogs,
            'fixture_changes':changed, 'artifacts':artifacts,
            'global_agents_present':(home/'AGENTS.md').exists()})
        record['evaluation'] = grade(record)
        trace = []
        for kind, key in [('call','calls'),('tool_output','tool_outputs'),('message','messages'),('usage','response_usage')]:
            trace.extend({'kind':kind,**item} for item in record[key])
        trace.sort(key=lambda row:row.get('at',''))
        (args.out/(name+'.trace.jsonl')).write_text(''.join(json.dumps(r)+'\n' for r in trace))

    record = trial.execute(options, 'new', case['scenario'], task['repetition'],
        scenario_prompt=case['prompt'], prepare=prepare, extra_input=inputs, inspect=inspect)
    print(json.dumps({'event':'evaluated', 'name':name, **record['evaluation']}), flush=True)
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--versions',default='v1')
    parser.add_argument('--cases',default='all')
    parser.add_argument('--repetitions',type=int,default=1)
    parser.add_argument('--phase',required=True)
    parser.add_argument('--manifest-dir',type=Path,default=HERE/'manifests')
    parser.add_argument('--workers',type=int,default=2)
    parser.add_argument('--prepare-only',action='store_true')
    parser.add_argument('--binary',type=Path,default=Path('/opt/homebrew/bin/codex'))
    parser.add_argument('--source-home',type=Path,default=ROOT/'.codex_home')
    parser.add_argument('--catalog',type=Path,default=ROOT/'tmp/wait-benchmark-catalog.json')
    args = parser.parse_args()
    assert 1 <= args.workers <= 2
    assert subprocess.check_output([str(args.binary),'--version'],text=True).strip() == 'codex-cli 0.154.0'
    assert digest(args.catalog) == 'e17cbd5fba8d477929a6a57f3d522325c488acb5e2f488e267aa59f3f239ba40'
    versions = args.versions.split(',')
    cases = json.loads((HERE/'cases.json').read_text())
    if args.cases != 'all':
        selected = args.cases.split(',')
        cases = [c for c in cases if c['id'] in selected]
        assert len(cases) == len(selected)
    assert 'none' not in versions or not any(c['explicit'] for c in cases)
    args.out = ROOT/'tmp/wait-skill-evals'/args.phase
    args.out.mkdir(parents=True,exist_ok=True)
    tasks = [{'version':v,'case':c,'repetition':r} for r in range(1,args.repetitions+1) for c in cases for v in versions]
    random.Random(20260915).shuffle(tasks)
    manifest = {'phase':args.phase,'model':'gpt-6-astra','effort':'low','workers':args.workers,
        'versions':{v:digest(HERE/'versions'/v/'SKILL.md.fixture') if v != 'none' else None for v in versions},
        'cases_sha256':digest(HERE/'cases.json'),'catalog_sha256':digest(args.catalog),
        'tasks':tasks, 'seed':20260915}
    write_once(args.manifest_dir/(args.phase+'.json'),manifest)
    if args.prepare_only:
        print(json.dumps({'prepared':args.phase,'trials':len(tasks)}))
        return
    disabled = other_skill_names(args.binary)
    print(json.dumps({'phase':args.phase,'trials':len(tasks),'unrelated_skills_disabled':len(disabled)}),flush=True)
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        records = list(pool.map(lambda task:run_case(args,task,disabled),tasks))
    print(json.dumps({'finished':args.phase,'trials':len(records),
        'full_passes':sum(r.get('evaluation',{}).get('overall_pass',False) for r in records)}),flush=True)


if __name__ == '__main__':
    main()
