#!/usr/bin/env python3
"""Check captured runtime observations and export compact, shareable evidence."""
import json
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "tmp/wait-probes")
destination = Path(__file__).parent / "runtime-results.json"
names = ["sleep-integer", "sleep-float-integral", "sleep-float-fractional",
         "wait-minimum", "wait-default", "wait-long-steer-astra", "wait-long-steer-sol",
         "sleep-long-steer", "wait-float", "wait-over-maximum", "wait-config-default",
         "wait-config-explicit-short", "goal-empty", "goal-status-text",
         "exposure-astra-default", "exposure-sol-default", "exposure-sol-always-on", "exposure-sol-disabled"]
results = []
for name in names:
    data = json.loads((root / (name + ".json")).read_text())
    assert data["status"] == "completed", (name, data.get("error"))
    requests = data["requests"]
    times = [r["at"] for r in requests]
    outputs = [item["output"] for r in requests for item in r["tool_outputs"]]
    row = {"name": name, "model_catalog_entry": data["model_catalog_entry"],
           "backend": data["backend"], "call": data["call"],
           "request_times_seconds": times, "request_count": len(times), "tool_outputs": outputs}
    if name.startswith("exposure-"):
        def sleep_tools(value):
            if isinstance(value, dict):
                if value.get("name") == "sleep":
                    return [value]
                return [item for child in value.values() for item in sleep_tools(child)]
            if isinstance(value, list):
                return [item for child in value for item in sleep_tools(child)]
            return []
        exposed = bool(sleep_tools(requests[0]["tools"]))
        assert len(times) == 1 and not outputs
        assert exposed == (name in ["exposure-astra-default", "exposure-sol-always-on"])
        row["sleep_exposed"] = exposed
    elif name.startswith("goal-"):
        assert len(times) == 4, (name, times)
        assert data["goal_before_pause"]["goal"]["status"] == "active"
        assert data["goal_paused"]["goal"]["status"] == "paused"
        assert data["requests_after_pause_in_1s"] == 0
        row.update({"before_pause": "active", "after_pause": "paused",
                    "new_requests_in_1s_after_pause": 0,
                    "completed_turns": sum(e.get("method") == "turn/completed" for e in data["events"])})
    else:
        assert len(times) == 2, (name, times)
        assert len(outputs) == 1, (name, outputs)
        gap = times[1] - times[0]
        row["request_gap_seconds"] = round(gap, 4)
        if name in ["sleep-float-integral", "sleep-float-fractional", "wait-float"]:
            assert "failed to parse function arguments: invalid type: floating point" in outputs[0]
            assert gap < 2
        elif name == "wait-over-maximum":
            assert "timeout_ms must be at most 3600000" in outputs[0]
        elif data["steer_at"] is not None:
            assert "interrupted by new input" in outputs[0]
            latency = times[1] - data["steer_at"]
            assert 0 <= latency < 1, (name, latency)
            row["steer_to_next_request_seconds"] = round(latency, 4)
        elif name == "sleep-integer":
            assert 1 <= gap < 3 and "Sleep completed." in outputs[0]
        elif name in ["wait-minimum", "wait-config-explicit-short"]:
            assert 10 <= gap < 13 and json.loads(outputs[0])["timed_out"]
        elif name == "wait-default":
            assert 30 <= gap < 33 and json.loads(outputs[0])["timed_out"]
        elif name == "wait-config-default":
            assert 1 <= gap < 3 and json.loads(outputs[0])["timed_out"]
        if name == "wait-minimum":
            assert "clamped to the minimum of 10000ms" in outputs[0]
    row["assertions"] = "passed"
    results.append(row)
destination.write_text(json.dumps({"measurement_note": "Scripted backend: request counts and runtime behavior are real; model inference and all token usage are simulated.",
                                  "cases": results}, indent=2) + "\n")
print(f"PASS: {len(results)} cases; evidence written to {destination}")
