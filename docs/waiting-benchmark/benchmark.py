#!/usr/bin/env python3
"""Bounded, live subscription-backed Codex waiting benchmark. Consumes usage.

Credentials stay in private temporary homes. Export selected diagnostic records,
never credentials or full system/developer instructions. CI is a local simulator;
terminal processes and subagents are real. No historical backend is recreated.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import threading
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'waiting-validation'))
from runtime_probe import Probe

TOKENS = ['input_tokens', 'cached_input_tokens', 'cache_write_input_tokens',
          'output_tokens', 'reasoning_output_tokens', 'total_tokens']
RESULT = 'BENCH_RESULT_7391'

JOB = '''import json,time
from pathlib import Path
p=Path("job-events.jsonl")
with p.open("a") as f: f.write(json.dumps({"event":"start","at":time.time()})+"\\n")
time.sleep({delay})
with p.open("a") as f: f.write(json.dumps({"event":"complete","at":time.time()})+"\\n")
print("BENCH_RESULT_7391",flush=True)
'''

CI = '''import json,time,sys
from pathlib import Path
assert sys.argv[1:]==["status"]
p=Path("ci-start.json")
now=time.time()
if not p.exists(): p.write_text(json.dumps({{"started":now}}))
started=json.loads(p.read_text())["started"]
done=now-started>={delay}
with Path("ci-checks.jsonl").open("a") as f:
 f.write(json.dumps({{"at":now,"done":done}})+"\\n")
print(json.dumps({{"run_id":"job-7391","status":"completed" if done else "running",
 "result":"BENCH_RESULT_7391" if done else None}}))
'''

def timestamp(value):
    return datetime.fromisoformat(value.replace('Z', '+00:00')).timestamp()

def total(records):
    result = {k: sum(r['usage'].get(k, 0) or 0 for r in records) for k in TOKENS}
    result['responses'] = len(records)
    result['input_minus_cached'] = result['input_tokens'] - result['cached_input_tokens']
    return result

def prompt_for(scenario, model):
    common = ('No other work is needed. Preserve the existing job; report its exact '
              'result only after successful completion. Do not inspect or modify '
              'the implementation of the supplied benchmark scripts.\n')
    if scenario == 'terminal':
        return ('Run `python3 bench_job.py` exactly once and wait for it to finish. '
                'Run it yourself; do not delegate. ' + common)
    if scenario == 'subagent':
        return (f'Delegate running `python3 bench_job.py` exactly once to exactly one '
                f'subagent, using model `{model}` at low reasoning effort. '
                'The child should wait for command completion and return its result. '
                'You have no independent work while that child runs. ' + common)
    return ('The CI run `job-7391` is pending. Its authoritative status command is '
            '`python3 bench_ci.py status`. It provides no completion notifications '
            'or watch mode. Monitor it until it completes; do not delegate. ' + common)

class Trial(Probe):
    def execute(self, options, condition, scenario, repetition):
        self.start = time.monotonic()
        wall_start = time.time()
        name = self.name
        record_path = self.root / (name + '.json')
        if record_path.exists():
            raise RuntimeError(f'Refusing to overwrite {record_path}')
        binary = options.old_binary if condition == 'old' else options.new_binary
        patch = options.patch if condition in ('patch', 'tuned', 'patch-on', 'tuned-on') else None
        if condition in ('tuned', 'tuned-on') and options.tuned_patch:
            patch = options.tuned_patch
        always_on = condition.endswith('-on')
        record = {'name': name, 'condition': condition, 'scenario': scenario,
                  'model': self.model, 'effort': options.effort, 'repetition': repetition,
                  'delay_seconds': options.delay, 'backend': 'live-current-subscription',
                  'binary': str(binary), 'sleep_mode': 'always_on' if always_on else 'default',
                  'catalog_sha256': hashlib.sha256(options.catalog.read_bytes()).hexdigest(),
                  'scenario_prompt': prompt_for(scenario, self.model),
                  'patch_sha256': hashlib.sha256(patch.read_bytes()).hexdigest() if patch else None,
                  'patch_file': str(patch) if patch else None}
        record['skills_mode'] = 'instructions_disabled' if options.no_skill_instructions else 'ambient'
        private_home = tempfile.TemporaryDirectory(prefix='codex-wait-benchmark-')
        home = Path(private_home.name)
        work = home / 'work'
        work.mkdir()
        self.process = None
        stderr = None
        self.thread_id = None
        turn_id = None
        try:
            shutil.copyfile(options.source_home / 'auth.json', home / 'auth.json')
            (home / 'auth.json').chmod(0o600)
            shutil.copyfile(options.catalog, home / 'models.json')
            if patch:
                shutil.copyfile(patch, home / 'AGENTS.md')
            config = [f'model = "{self.model}"', f'model_reasoning_effort = "{options.effort}"',
                      'approval_policy = "never"', 'sandbox_mode = "workspace-write"',
                      'model_catalog_json = "models.json"', '[features]', 'multi_agent = true']
            if always_on:
                config.append('sleep_tool = { enabled = true, mode = "always_on" }')
            if options.no_skill_instructions:
                config.extend(['[skills]', 'include_instructions = false',
                               '[skills.bundled]', 'enabled = false'])
            (home / 'config.toml').write_text('\n'.join(config) + '\n')
            (work / 'bench_job.py').write_text(JOB.replace('{delay}', str(options.delay)))
            (work / 'bench_ci.py').write_text(CI.format(delay=options.delay))
            env = os.environ.copy()
            env['CODEX_HOME'] = str(home)
            for key in ['OPENAI_API_KEY', 'CODEX_API_KEY']:
                env.pop(key, None)
            record['cli_version'] = subprocess.check_output([str(binary), '--version'], text=True).strip()
            stderr = (self.root / (name + '.stderr.log')).open('w')
            self.process = subprocess.Popen([str(binary), 'app-server'], stdin=subprocess.PIPE,
                stdout=subprocess.PIPE, stderr=stderr, text=True, env=env, cwd=work)
            threading.Thread(target=self.read, daemon=True).start()
            self.rpc('initialize', {'clientInfo': {'name': 'waiting_benchmark', 'version': '1'},
                                  'capabilities': {'experimentalApi': True}})
            self.send({'method': 'initialized', 'params': {}})
            thread = self.rpc('thread/start', {'model': self.model, 'cwd': str(work),
                'approvalPolicy': 'never', 'sandbox': 'workspace-write', 'ephemeral': False,
                'experimentalRawEvents': True})
            self.thread_id = thread['thread']['id']
            record['thread_id'] = self.thread_id
            record['turn_start_epoch'] = time.time()
            turn = self.rpc('turn/start', {'threadId': self.thread_id,
                'input': [{'type': 'text', 'text': record['scenario_prompt']}], 'effort': options.effort})
            turn_id = turn['turn']['id']
            deadline = time.monotonic() + options.delay + 150
            announced = False
            while time.monotonic() < deadline:
                self.pump(0.2)
                if not announced and ((work / 'job-events.jsonl').exists() or (work / 'ci-start.json').exists()):
                    print(json.dumps({'trial': name, 'event': 'job-started'}), flush=True)
                    announced = True
                finished = [e for e in self.events if e.get('method') == 'turn/completed'
                            and e.get('params', {}).get('threadId') == self.thread_id]
                if finished:
                    record['turn_status'] = finished[-1]['params']['turn']['status']
                    record['turn_error'] = finished[-1]['params']['turn'].get('error')
                    record['turn_end_epoch'] = time.time()
                    record['status'] = 'completed' if record['turn_status'] == 'completed' else 'turn_failed'
                    break
                # A hard limit bounds pathological inference loops. Events are not inference counts.
                if sum(e.get('method') == 'item/started' for e in self.events) > 120:
                    record['status'] = 'item_limit'
                    break
                if self.process.poll() is not None:
                    raise RuntimeError('app-server exited before turn completion')
            else:
                record['status'] = 'deadline_exceeded'
            if record['status'] in ('deadline_exceeded', 'item_limit'):
                self.rpc('turn/interrupt', {'threadId': self.thread_id, 'turnId': turn_id})
            # Drain already-delivered events without adding model work.
            while not self.queue.empty():
                self.pump(0)
        except Exception as error:
            record['status'] = 'probe_error'
            record['error'] = repr(error)
        finally:
            if self.process:
                self.process.terminate()
                try:
                    self.process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    self.process.kill()
                    self.process.wait()
            if stderr:
                stderr.close()
            record['elapsed_seconds'] = self.now()
            calls, outputs, usages, messages, contexts, instruction_hashes = [], [], [], [], [], []
            legacy_usages = []
            cumulative_final = {}
            prompt_loaded = False
            skills_instruction_sessions = set()
            for rollout in sorted((home / 'sessions').rglob('*.jsonl')):
                rows = [json.loads(line) for line in rollout.open() if line.strip()]
                metas = [e['payload'] for e in rows if e.get('type') == 'session_meta']
                sid = metas[0].get('id') if metas else str(rollout.name)
                previous_total = None
                for e in rows:
                    p = e.get('payload', {})
                    base = {'at': e.get('timestamp'), 'session_id': sid}
                    if e.get('type') == 'session_meta':
                        instructions = p.get('base_instructions')
                        if instructions:
                            instruction_hashes.append({'session_id': sid,
                                'sha256': hashlib.sha256(json.dumps(instructions, sort_keys=True).encode()).hexdigest()})
                    elif e.get('type') == 'token_usage_record':
                        usages.append({**base, 'response_id': p['response_id'], 'usage': p['usage'],
                                       'source': 'per_response_rollout'})
                    elif e.get('type') == 'event_msg' and p.get('type') == 'token_count' and p.get('info'):
                        info = p['info']
                        current = info.get('total_token_usage')
                        if current and current != previous_total:
                            usage = info.get('last_token_usage')
                            if usage and usage.get('total_tokens',0)>0:
                                legacy_usages.append({**base,
                                    'response_id': f"legacy:{sid}:{len(legacy_usages)}",
                                    'usage':usage,'source':'last_usage_on_distinct_cumulative_snapshot',
                                    'cumulative_snapshot':current})
                            previous_total = current
                            cumulative_final[sid] = current
                    elif e.get('type') == 'turn_context':
                        contexts.append({**base, **{k: p.get(k) for k in ['model', 'effort', 'turn_id']}})
                    elif e.get('type') == 'response_item':
                        if p.get('type') == 'message':
                            message_text = '\n'.join(c.get('text', '') for c in p.get('content', []))
                            if '<skills_instructions>' in message_text or '### Available skills' in message_text:
                                skills_instruction_sessions.add(sid)
                        if p.get('type') in ('function_call', 'custom_tool_call'):
                            calls.append({**base, **{k: p[k] for k in
                                ['type', 'name', 'namespace', 'call_id', 'arguments', 'input'] if k in p}})
                        elif p.get('type') in ('function_call_output', 'custom_tool_call_output'):
                            outputs.append({**base, 'call_id': p.get('call_id'), 'output': p.get('output')})
                        elif p.get('type') == 'message' and p.get('role') == 'assistant':
                            messages.append({**base, 'phase': p.get('phase'),
                                'text': '\n'.join(c.get('text', '') for c in p.get('content', []))})
                        elif p.get('role') == 'user' and patch and sid == self.thread_id:
                            if patch.read_text().strip() in '\n'.join(c.get('text', '') for c in p.get('content', [])):
                                prompt_loaded = True
            field_map={'totalTokens':'total_tokens','inputTokens':'input_tokens',
                'cachedInputTokens':'cached_input_tokens','cacheWriteInputTokens':'cache_write_input_tokens',
                'outputTokens':'output_tokens','reasoningOutputTokens':'reasoning_output_tokens'}
            for event in self.events:
                if event.get('method') == 'rawResponse/completed' and event['params'].get('usage'):
                    p=event['params']
                    usages.append({'at':datetime.fromtimestamp(wall_start+event['observed_at'],timezone.utc).isoformat(),
                        'session_id':p['threadId'],'response_id':p['responseId'],
                        'usage':{field_map[k]:v for k,v in p['usage'].items() if k in field_map},
                        'source':'raw_response_notification'})
            raw_sessions={u['session_id'] for u in usages}
            usages.extend(u for u in legacy_usages if u['session_id'] not in raw_sessions)
            unique = {}
            for usage in usages:
                key = usage['response_id']
                if key in unique:
                    assert all(unique[key]['usage'].get(k,0)==usage['usage'].get(k,0) for k in TOKENS), 'conflicting duplicated usage'
                    if usage['session_id'] == self.thread_id:
                        unique[key] = usage
                else:
                    unique[key] = usage
            usages = sorted(unique.values(), key=lambda x: x['at'])
            parent = [u for u in usages if u['session_id'] == self.thread_id]
            children = [u for u in usages if u['session_id'] != self.thread_id]
            parent_messages = [m for m in messages if m['session_id'] == self.thread_id]
            events_path = work / 'job-events.jsonl'
            job_events = [json.loads(l) for l in events_path.read_text().splitlines()] if events_path.exists() else []
            ci_path = work / 'ci-checks.jsonl'
            checks = [json.loads(l) for l in ci_path.read_text().splitlines()] if ci_path.exists() else []
            completed_at = next((e['at'] for e in job_events if e['event'] == 'complete'), None)
            if (work / 'ci-start.json').exists():
                completed_at = json.loads((work / 'ci-start.json').read_text())['started'] + options.delay
            result_messages = [m for m in parent_messages if RESULT in m['text'] and m['phase'] in ('final_answer', 'final')]
            observed_complete = any(c['done'] for c in checks) if scenario == 'ci' else completed_at is not None
            success = bool(record.get('status') == 'completed' and result_messages and observed_complete)
            if completed_at and result_messages:
                success = success and timestamp(result_messages[-1]['at']) >= completed_at
            points = [record.get('turn_start_epoch', time.time())] + [timestamp(m['at']) for m in parent_messages]
            gaps = [round(b-a, 3) for a,b in zip(points, points[1:])]
            record.update({'success': success, 'prompt_loaded': prompt_loaded if patch else None,
                'skills_instruction_sessions': sorted(skills_instruction_sessions),
                'calls': calls, 'tool_outputs': outputs, 'response_usage': usages, 'messages': messages,
                'model_contexts': contexts, 'base_instruction_hashes': instruction_hashes,
                'cumulative_final_by_session': cumulative_final,
                'parent_usage': total(parent), 'child_usage': total(children), 'combined_usage': total(usages),
                'child_session_count': len({u['session_id'] for u in children}), 'job_events': job_events,
                'job_launches': sum(e['event'] == 'start' for e in job_events), 'ci_checks': checks,
                'result_delay_seconds': round(timestamp(result_messages[-1]['at'])-completed_at,3)
                    if result_messages and completed_at else None,
                'parent_message_gaps_seconds': gaps, 'max_parent_message_gap_seconds': max(gaps, default=0)})
            record_path.write_text(json.dumps(record, indent=2) + '\n')
            private_home.cleanup()
        print(json.dumps({k: record[k] for k in ['name', 'status', 'success', 'parent_usage',
            'child_usage', 'job_launches', 'result_delay_seconds', 'max_parent_message_gap_seconds']}), flush=True)
        return record

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-home', type=Path, required=True)
    parser.add_argument('--old-binary', type=Path, required=True)
    parser.add_argument('--new-binary', type=Path, required=True)
    parser.add_argument('--catalog', type=Path, required=True)
    parser.add_argument('--patch', type=Path, required=True)
    parser.add_argument('--tuned-patch', type=Path)
    parser.add_argument('--no-skill-instructions', action='store_true')
    parser.add_argument('--after-dir', type=Path)
    parser.add_argument('--after-count', type=int, default=30)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--models', default='gpt-6-astra,gpt-5.6-sol')
    parser.add_argument('--conditions', default='old,new,patch')
    parser.add_argument('--scenarios', default='terminal,subagent,ci')
    parser.add_argument('--repetitions', type=int, default=2)
    parser.add_argument('--start-repetition', type=int, default=1)
    parser.add_argument('--workers', type=int, default=2)
    parser.add_argument('--delay', type=int, default=75)
    parser.add_argument('--effort', default='low')
    args = parser.parse_args()
    for key in ['source_home', 'old_binary', 'new_binary', 'catalog', 'patch', 'out']:
        setattr(args, key, getattr(args, key).resolve())
    if args.tuned_patch:
        args.tuned_patch = args.tuned_patch.resolve()
    old_cli_version = subprocess.check_output([str(args.old_binary), '--version'], text=True).strip()
    args.out.mkdir(parents=True, exist_ok=True)
    if args.after_dir:
        print(json.dumps({'event':'queued-after-existing-phase','directory':str(args.after_dir),
                          'expected_records':args.after_count}), flush=True)
        queue_deadline = time.monotonic()+1800
        while len(list(args.after_dir.glob('gpt-*.json'))) < args.after_count:
            if time.monotonic() > queue_deadline:
                raise TimeoutError('Previous benchmark phase did not produce expected records')
            time.sleep(2)
    tasks=[]
    for rep in range(args.start_repetition, args.start_repetition+args.repetitions):
        conditions=args.conditions.split(',')
        if rep%2==0:
            conditions.reverse()
        for scenario in args.scenarios.split(','):
            for model in args.models.split(','):
                for condition in conditions:
                    if model == 'gpt-6-astra' and condition == 'old' and old_cli_version == 'codex-cli 0.151.0':
                        print(json.dumps({'model':model,'condition':condition,'status':'unavailable',
                            'reason':'Backend rejects Astra on CLI 0.151.0; see smoke evidence.'}),flush=True)
                        continue
                    name=f'{model}-{scenario}-{condition}-r{rep}'
                    if not (args.out/(name+'.json')).exists():
                        tasks.append((name,model,condition,scenario,rep))
    failed=0
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        pending={pool.submit(Trial(args.out,name,model,None).execute,args,cond,scen,rep):name
                 for name,model,cond,scen,rep in tasks}
        for future in as_completed(pending):
            result=future.result()
            failed += not result['success']
    print(json.dumps({'trials_run':len(tasks),'unsuccessful':failed}),flush=True)

if __name__=='__main__':
    main()
