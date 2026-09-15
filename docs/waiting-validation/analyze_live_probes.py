#!/usr/bin/env python3
"""Validate and summarize the bounded live prompt comparison."""
import hashlib
import json
from pathlib import Path
import sys

source = Path(sys.argv[1] if len(sys.argv) > 1 else "tmp/live-wait-probes")
target = Path(__file__).parent
prompt_hash = hashlib.sha256((target.parent / "archive/agents-patches/waiting-validation/AGENTS.waiting-recommended.md").read_bytes()).hexdigest()
names = ["astra-subagent-baseline-75", "astra-subagent-recommended-75",
         "sol-subagent-baseline-75", "sol-subagent-recommended-75"]
rows, evidence = [], []
for name in names:
    data = json.loads((source / (name + ".json")).read_text())
    assert data["status"] == "completed_after_result" and data["result_reported"], name
    assert data["event_delay_after_first_wait_seconds"] == 75
    assert data["model_metadata"][0]["model"] == data["model"]
    assert data["model_metadata"][0]["effort"] == "low"
    if "recommended" in name:
        assert data["candidate_found_in_user_instructions"]
        assert data["prompt_sha256"] == prompt_hash
    ids = [r["response_id"] for r in data["response_usage"]]
    assert len(ids) == len(set(ids)), "Do not double-count a response"
    totals = {k: sum(r["usage"][k] for r in data["response_usage"])
              for k in ["input_tokens", "cached_input_tokens", "output_tokens", "reasoning_output_tokens"]}
    waiting = [{"tool": c.get("namespace", "") + "." + c["name"],
                "arguments": json.loads(c["arguments"])} for c in data["calls"]
               if c["name"] in ["sleep", "wait_agent"]]
    assert len(waiting) == len(data["calls"]), "Unexpected extra tools must be investigated"
    rows.append({"name": name, "model": data["model"], "condition": "recommended" if "recommended" in name else "baseline",
                 "waiting_calls": waiting, "response_count": len(ids), "usage_totals": totals,
                 "result_latency_seconds": round(data["elapsed_seconds"] - data["delivered_at"], 4),
                 "result_correct": True, "prompt_loaded": data["candidate_found_in_user_instructions"],
                 "prompt_sha256": data.get("prompt_sha256")})
    evidence.append(data)
for offset in [0, 2]:
    assert evidence[offset]["scenario"] == evidence[offset + 1]["scenario"]
for name in ["astra-candidate-smoke", "astra-subagent-candidate-smoke"]:
    evidence.append(json.loads((source / (name + ".json")).read_text()))
output = {"scope": "One paired 75-second simulated-subagent scenario per model at low effort; actual OpenAI model inference through Codex 0.154.0. A driver delivered results via active-turn steering; no real subagents were created.",
          "limitations": "Not randomized or repeated; cache warmness differs. Counts measure this scenario, not company costs or general prompt reliability. Initial smoke tests used the earlier candidate, not the recommended file.",
          "comparisons": rows, "selected_trial_records": evidence}
(target / "live-prompt-results.json").write_text(json.dumps(output, indent=2) + "\n")
for row in rows:
    print(json.dumps(row))
print("PASS: completed results, model/effort, prompt provenance, and distinct response accounting verified")
