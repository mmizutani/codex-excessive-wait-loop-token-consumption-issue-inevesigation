#!/usr/bin/env python3
"""Exercise installed Codex app-server with a local, scripted Responses server.

No OpenAI calls or credentials. A separate temporary CODEX_HOME is used.
Backend token counts are synthetic zeros: never use these tests for pricing.
Run: python3 docs/waiting-validation/runtime_probe.py --out tmp/wait-probes
"""
import argparse
import json
import os
from pathlib import Path
import queue
import subprocess
import tempfile
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


def function(namespace, name, arguments):
    return {"type": "function_call", "namespace": namespace, "name": name,
            "arguments": arguments, "call_id": "probe-call"}


def message(text="PROBE_DONE"):
    return {"type": "message", "role": "assistant", "id": "probe-message",
            "phase": "final_answer", "content": [{"type": "output_text", "text": text}]}


class Probe:
    def __init__(self, root, name, model, item, steer=False, extra=None):
        self.root, self.name, self.model = root, name, model
        self.item, self.steer, self.extra = item, steer, extra or {}
        self.requests, self.events = [], []
        self.queue = queue.Queue()
        self.responses = {}
        self.seq = 0
        self.start = time.monotonic()
        self.process = None
        self.server = None

    def now(self):
        return round(time.monotonic() - self.start, 4)

    def run(self):
        probe = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def do_POST(self):
                body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                if not probe.requests:
                    (probe.root / (probe.name + ".request.json")).write_text(json.dumps(body, indent=2))
                number = len(probe.requests) + 1
                if number > 12:
                    self.send_error(500, "probe request limit exceeded")
                    return
                probe.requests.append({"at": probe.now(), "number": number,
                    "model": body.get("model"), "path": self.path,
                    "tool_outputs": [i for i in body.get("input", [])
                                     if i.get("type") == "function_call_output"],
                    "tools": (body.get("tools", []) +
                              [i for i in body.get("input", []) if i.get("type") == "additional_tools"]) if number == 1 else [],
                    "input_items": len(body.get("input", []))})
                item = probe.item if number == 1 else message()
                if probe.name.startswith("goal-"):
                    item = message("" if probe.name == "goal-empty" else "Still waiting.")
                    time.sleep(0.3)
                rid = f"probe-response-{number}"
                events = [{"type": "response.created", "response": {"id": rid}},
                          {"type": "response.output_item.done", "item": item},
                          {"type": "response.completed", "response": {"id": rid,
                           "usage": {"input_tokens": 0, "output_tokens": 0,
                                     "total_tokens": 0}}}]
                payload = "".join("data: " + json.dumps(e) + "\n\n" for e in events).encode()
                self.send_response(200)
                self.send_header("Content-Type", "text/event-stream")
                self.send_header("Content-Length", str(len(payload)))
                self.end_headers()
                self.wfile.write(payload)

        try:
            self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
            threading.Thread(target=self.server.serve_forever, daemon=True).start()
            with tempfile.TemporaryDirectory(prefix="codex-wait-probe-") as tmp:
                home = Path(tmp)
                config = '\n'.join([
                    'model_provider = "audit"', f'model = "{self.model}"',
                    'approval_policy = "never"', 'sandbox_mode = "read-only"',
                    '[model_providers.audit]', 'name = "Local scripted test backend"',
                    f'base_url = "http://127.0.0.1:{self.server.server_port}/v1"',
                    'wire_api = "responses"', 'requires_openai_auth = false',
                    'supports_websockets = false', 'request_max_retries = 0',
                    '[features]', 'multi_agent = true',
                    'goals = true',
                    ('sleep_tool = { mode = "always_on" }' if self.name == "exposure-sol-always-on"
                     else 'sleep_tool = { enabled = true, mode = "always_on" }'),
                ])
                (home / "config.toml").write_text(config)
                env = os.environ.copy()
                env["CODEX_HOME"] = str(home)
                # No credentials are needed or forwarded to the local backend.
                for key in ["OPENAI_API_KEY", "CODEX_API_KEY"]:
                    env.pop(key, None)
                stderr = (self.root / (self.name + ".stderr.log")).open("w")
                self.process = subprocess.Popen(["codex", "app-server"],
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=stderr,
                    text=True, env=env, cwd=tmp)
                threading.Thread(target=self.read, daemon=True).start()
                self.rpc("initialize", {"clientInfo": {"name": "waiting_probe", "version": "1"},
                                       "capabilities": {"experimentalApi": True}})
                self.send({"method": "initialized", "params": {}})
                config_overrides = {"features.sleep_tool": {"enabled": True, "mode": "always_on"},
                                    **self.extra}
                result = self.rpc("thread/start", {"model": self.model, "modelProvider": "audit",
                    "cwd": tmp, "approvalPolicy": "never", "sandbox": "read-only",
                    "ephemeral": not self.name.startswith("goal-"), "config": config_overrides})
                self.thread_id = result["thread"]["id"]
                goal = self.name.startswith("goal-")
                if goal:
                    self.goal_created = self.rpc("thread/goal/set", {"threadId": self.thread_id,
                        "objective": "Synthetic runtime test: await an external signal.", "status": "active"})
                    turn_id = None
                else:
                    turn = self.rpc("turn/start", {"threadId": self.thread_id,
                        "input": [{"type": "text", "text": "Run the scripted runtime probe."}]})
                    turn_id = turn["turn"]["id"]
                deadline = time.monotonic() + 68
                steered = False
                while time.monotonic() < deadline:
                    self.pump(0.1)
                    if goal and len(self.requests) >= 4:
                        self.goal_before_pause = self.rpc("thread/goal/get", {"threadId": self.thread_id})
                        self.goal_paused = self.rpc("thread/goal/set", {"threadId": self.thread_id,
                            "status": "paused"})
                        quiet_deadline = time.monotonic() + 1.0
                        paused_count = len(self.requests)
                        while time.monotonic() < quiet_deadline:
                            self.pump(0.1)
                        self.requests_after_pause = len(self.requests) - paused_count
                        break
                    if self.steer and not steered and self.requests:
                        if self.now() - self.requests[0]["at"] >= 1.0:
                            self.steer_at = self.now()
                            self.rpc("turn/steer", {"threadId": self.thread_id,
                                "expectedTurnId": turn_id,
                                "input": [{"type": "text", "text": "PROBE_STEERING: return now."}]})
                            steered = True
                    if not goal and any(e.get("method") == "turn/completed" for e in self.events):
                        break
                else:
                    raise TimeoutError("probe exceeded 68-second deadline")
                result = {"name": self.name, "model_catalog_entry": self.model,
                          "backend": "scripted-local-no-model-inference", "status": "completed",
                          "elapsed_seconds": self.now(), "call": self.item,
                          "steer_at": getattr(self, "steer_at", None),
                          "requests": self.requests, "events": self.events}
                if goal:
                    result.update({"goal_before_pause": self.goal_before_pause,
                                   "goal_paused": self.goal_paused,
                                   "requests_after_pause_in_1s": self.requests_after_pause})
        except Exception as error:
            result = {"name": self.name, "status": "error", "error": repr(error),
                      "requests": self.requests, "events": self.events}
        finally:
            if self.process:
                self.process.terminate()
                try:
                    self.process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    self.process.kill()
                    self.process.wait()
            if self.server:
                self.server.shutdown()
                self.server.server_close()
        (self.root / (self.name + ".json")).write_text(json.dumps(result, indent=2) + "\n")
        concise = {k: v for k, v in result.items() if k not in ["requests", "events", "call"]}
        concise["request_times"] = [r["at"] for r in self.requests]
        concise["tool_outputs"] = [r["tool_outputs"] for r in self.requests if r["tool_outputs"]]
        print(json.dumps(concise), flush=True)
        return result

    def read(self):
        for line in self.process.stdout:
            try:
                self.queue.put(json.loads(line))
            except json.JSONDecodeError:
                pass

    def send(self, item):
        self.process.stdin.write(json.dumps(item) + "\n")
        self.process.stdin.flush()

    def pump(self, timeout):
        try:
            item = self.queue.get(timeout=timeout)
        except queue.Empty:
            return
        item["observed_at"] = self.now()
        if "id" in item and ("result" in item or "error" in item):
            self.responses[item["id"]] = item
        else:
            self.events.append(item)

    def rpc(self, method, params):
        self.seq += 1
        ident = self.seq
        self.send({"id": ident, "method": method, "params": params})
        deadline = time.monotonic() + 20
        while ident not in self.responses:
            if time.monotonic() > deadline:
                raise TimeoutError(f"RPC {method}")
            self.pump(0.1)
        response = self.responses.pop(ident)
        if "error" in response:
            raise RuntimeError(response["error"])
        return response["result"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--only")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    cases = [
        ("sleep-integer", "gpt-6-astra", function("clock", "sleep", '{"duration_ms":1000}'), False, {}),
        ("sleep-float-integral", "gpt-6-astra", function("clock", "sleep", '{"duration_ms":1.0}'), False, {}),
        ("sleep-float-fractional", "gpt-6-astra", function("clock", "sleep", '{"duration_ms":1.5}'), False, {}),
        ("wait-minimum", "gpt-6-astra", function("collaboration", "wait_agent", '{"timeout_ms":1}'), False, {}),
        ("wait-default", "gpt-6-astra", function("collaboration", "wait_agent", '{}'), False, {}),
        ("wait-long-steer-astra", "gpt-6-astra", function("collaboration", "wait_agent", '{"timeout_ms":300000}'), True, {}),
        ("wait-long-steer-sol", "gpt-5.6-sol", function("collaboration", "wait_agent", '{"timeout_ms":300000}'), True, {}),
        ("sleep-long-steer", "gpt-6-astra", function("clock", "sleep", '{"duration_ms":300000}'), True, {}),
        ("wait-float", "gpt-6-astra", function("collaboration", "wait_agent", '{"timeout_ms":10000.0}'), False, {}),
        ("wait-over-maximum", "gpt-6-astra", function("collaboration", "wait_agent", '{"timeout_ms":3600001}'), False, {}),
        ("wait-config-default", "gpt-6-astra", function("collaboration", "wait_agent", '{}'), False,
         {"features.multi_agent_v2": {"enabled": True, "min_wait_timeout_ms": 1, "default_wait_timeout_ms": 1000}}),
        ("wait-config-explicit-short", "gpt-6-astra", function("collaboration", "wait_agent", '{"timeout_ms":10000}'), False,
         {"features.multi_agent_v2": {"enabled": True, "default_wait_timeout_ms": 300000}}),
        ("goal-empty", "gpt-6-astra", message(""), False, {}),
        ("goal-status-text", "gpt-6-astra", message("Still waiting."), False, {}),
        ("exposure-astra-default", "gpt-6-astra", message(), False,
         {"features.sleep_tool": {"enabled": True, "mode": "model_driven"}}),
        ("exposure-sol-default", "gpt-5.6-sol", message(), False,
         {"features.sleep_tool": {"enabled": True, "mode": "model_driven"}}),
        ("exposure-sol-always-on", "gpt-5.6-sol", message(), False,
         {"features.sleep_tool": {"mode": "always_on"}}),
        ("exposure-sol-disabled", "gpt-5.6-sol", message(), False,
         {"features.sleep_tool": {"enabled": False, "mode": "always_on"}}),
    ]
    for name, model, item, steer, extra in cases:
        if not args.only or name in args.only.split(","):
            result = Probe(args.out, name, model, item, steer, extra).run()
            if result["status"] == "error":
                raise SystemExit(1)


if __name__ == "__main__":
    main()
