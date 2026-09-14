#!/usr/bin/env python3
"""Bounded real-model prompt probes; consumes normal Codex account usage.

Uses a temporary CODEX_HOME with a private copy of existing authentication.
Never exports authentication or complete instruction/rollout content.
The synthetic worker result is delivered by turn/steer, not a real subagent.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import threading
import time
from runtime_probe import Probe


SCENARIO = """This is a controlled waiting test. A test driver will deliver a pending
worker's result into this active turn. No local work remains until that result
arrives, and its arrival time is unknown to you. Wait for the result, then report
its exact value. Do not create agents, run commands, access files, or query other
services: the driver owns the worker and will deliver its result. Use the available
waiting tools to keep this turn waiting for the result."""

CHILD_SCENARIO = """This is a controlled waiting test using simulated task state:
a V2 subagent is healthy and still working; only its result remains before you can
finish. No useful local work remains and its completion time is unknown. The test
driver owns this simulated worker and will deliver its result into this active
turn. Use the available waiting tools, then report the exact delivered value.
Do not create agents, inspect agent lists, run commands, access files, or query
services. Use the supplied task state and wait for the driver's result."""


class LiveProbe(Probe):
    def run_live(self, source_home, prompt_file, delay, effort, scenario):
        result = {"name": self.name, "model": self.model, "effort": effort,
                  "scenario": scenario, "event_delay_after_first_wait_seconds": delay,
                  "backend": "live-openai-via-codex", "prompt_file": str(prompt_file) if prompt_file else None}
        self.process = None
        home = None
        stderr = None
        first_wait = None
        delivered = False
        value = "WAIT_RESULT_7391"
        with tempfile.TemporaryDirectory(prefix="codex-live-wait-") as tmp:
            home = Path(tmp)
            try:
                auth = source_home / "auth.json"
                if not auth.exists():
                    raise RuntimeError("No existing Codex auth.json available")
                shutil.copyfile(auth, home / "auth.json")
                (home / "auth.json").chmod(0o600)
                if (source_home / "models_cache.json").exists():
                    shutil.copyfile(source_home / "models_cache.json", home / "models_cache.json")
                if prompt_file:
                    text = prompt_file.read_text()
                    (home / "AGENTS.md").write_text(text)
                    result["prompt_sha256"] = hashlib.sha256(text.encode()).hexdigest()
                (home / "config.toml").write_text('\n'.join([
                    f'model = "{self.model}"', f'model_reasoning_effort = "{effort}"',
                    'approval_policy = "never"', 'sandbox_mode = "read-only"',
                    '[features]', 'multi_agent = true',
                    'sleep_tool = { enabled = true, mode = "always_on" }',
                ]))
                work = home / "work"
                work.mkdir()
                env = os.environ.copy()
                env["CODEX_HOME"] = str(home)
                stderr = (self.root / (self.name + ".stderr.log")).open("w")
                self.process = subprocess.Popen(["codex", "app-server"], stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE, stderr=stderr, text=True, env=env, cwd=work)
                threading.Thread(target=self.read, daemon=True).start()
                self.rpc("initialize", {"clientInfo": {"name": "live_waiting_probe", "version": "1"},
                    "capabilities": {"experimentalApi": True}})
                self.send({"method": "initialized", "params": {}})
                started = self.rpc("thread/start", {"model": self.model,
                    "cwd": str(work), "approvalPolicy": "never", "sandbox": "read-only",
                    "ephemeral": False})
                thread_id = started["thread"]["id"]
                result["thread_id"] = thread_id
                turn = self.rpc("turn/start", {"threadId": thread_id,
                    "input": [{"type": "text", "text": scenario}], "effort": effort})
                turn_id = turn["turn"]["id"]
                deadline = time.monotonic() + delay + 90
                while time.monotonic() < deadline:
                    self.pump(0.1)
                    for event in self.events:
                        item = event.get("params", {}).get("item", {})
                        if event.get("method") == "item/started" and (
                            item.get("type") == "sleep" or
                            (item.get("type") == "collabAgentToolCall" and item.get("tool") == "wait")):
                            if first_wait is None:
                                first_wait = event["observed_at"]
                                print(json.dumps({"name": self.name, "first_wait_at": first_wait,
                                                  "wait_item": item}), flush=True)
                    if first_wait is not None and not delivered and self.now() >= first_wait + delay:
                        result["delivered_at"] = self.now()
                        self.rpc("turn/steer", {"threadId": thread_id, "expectedTurnId": turn_id,
                            "input": [{"type": "text", "text": f"The pending worker completed successfully. Its result is {value}. Report it now."}]})
                        delivered = True
                    terminal = [e for e in self.events if e.get("method") == "turn/completed"]
                    if terminal:
                        result["turn_status"] = terminal[-1]["params"]["turn"]["status"]
                        result["turn_error"] = terminal[-1]["params"]["turn"].get("error")
                        result["status"] = "completed_after_result" if delivered else "ended_before_result"
                        break
                else:
                    result["status"] = "deadline_exceeded"
                    self.rpc("turn/interrupt", {"threadId": thread_id, "turnId": turn_id})
                result["first_wait_at"] = first_wait
                result["elapsed_seconds"] = self.now()
            except Exception as error:
                result["status"] = "probe_error"
                result["error"] = repr(error)
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
                calls, usages, outputs, metadata = [], [], [], []
                loaded = False
                for rollout in (home / "sessions").rglob("*.jsonl"):
                    for line in rollout.open():
                        e = json.loads(line)
                        p = e.get("payload", {})
                        if e["type"] == "response_item":
                            if p.get("type") in ["function_call", "custom_tool_call"]:
                                calls.append({"at": e["timestamp"], **{k: p[k] for k in
                                    ["type", "name", "namespace", "call_id", "arguments", "input"] if k in p}})
                            elif p.get("type") in ["function_call_output", "custom_tool_call_output"]:
                                outputs.append({"at": e["timestamp"], "call_id": p.get("call_id"), "output": p.get("output")})
                            if prompt_file and "## Waiting for work" in json.dumps(p) and p.get("role") == "user":
                                loaded = True
                        elif e["type"] == "token_usage_record":
                            usages.append({"at": e["timestamp"], "response_id": p["response_id"], "usage": p["usage"]})
                        elif e["type"] == "turn_context":
                            metadata.append({k: p.get(k) for k in ["model", "effort", "turn_id"]})
                messages = [e["params"]["item"] for e in self.events if e.get("method") == "item/completed"
                            and e.get("params", {}).get("item", {}).get("type") == "agentMessage"]
                result.update({"calls": calls, "tool_outputs": outputs, "response_usage": usages,
                               "messages": messages, "model_metadata": metadata,
                               "candidate_found_in_user_instructions": loaded if prompt_file else None,
                               "result_reported": any(value in m.get("text", "") for m in messages)})
        (self.root / (self.name + ".json")).write_text(json.dumps(result, indent=2) + "\n")
        brief = {k: v for k, v in result.items() if k not in ["calls", "tool_outputs", "response_usage", "messages", "scenario"]}
        brief["calls"] = [{k: c[k] for k in ["name", "namespace", "arguments"] if k in c} for c in result["calls"]]
        brief["response_count"] = len(result["response_usage"])
        print(json.dumps(brief), flush=True)
        return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-home", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--model", choices=["gpt-6-astra", "gpt-5.6-sol"], required=True)
    parser.add_argument("--name", required=True)
    parser.add_argument("--prompt", type=Path)
    parser.add_argument("--delay", type=float, default=75)
    parser.add_argument("--effort", default="low")
    parser.add_argument("--scenario", choices=["external", "subagent"], default="external")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    probe = LiveProbe(args.out, args.name, args.model, None)
    result = probe.run_live(args.source_home.resolve(), args.prompt, args.delay, args.effort,
                            CHILD_SCENARIO if args.scenario == "subagent" else SCENARIO)
    if result["status"] in ["probe_error", "deadline_exceeded"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
