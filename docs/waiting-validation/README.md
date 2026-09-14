# Waiting-validation evidence

Companion to [the independent validation report](../CODEX_ASTRA_SOL_WAITING_INDEPENDENT_VALIDATION.md), September 14, 2026.

| File | Contents |
|---|---|
| `runtime_probe.py` | Bounded installed-binary app-server probes with scripted local Responses replies. No live model inference. |
| `verify_results.py` | Assertions over the captured probe results; exports the compact JSON below. |
| `runtime-results.json` | Verified outcomes for the original 14 scenarios plus four sleep-exposure cases, request timestamps, tool outputs, and narrow goal-pause observations. |
| `live-probes.json` | Selected actual Astra tool calls, outputs, per-response usage, and shell completion timestamps from this investigation. |
| `source-provenance.json` | Installed CLI version, pinned release/check-out commits, and relevant Git blob comparisons. |
| `release-audit.json` | Retrieved public PR/release/issue metadata and merge-ancestry results. |
| `sleep-exposure-results.json` | Four installed-binary configuration cases: Astra/Sol defaults, always-on sleep, and explicitly disabled sleep. |
| `live_prompt_probe.py` | Bounded real Astra/Sol inference through Codex with temporary global AGENTS.md instructions. Uses normal account usage. |
| `analyze_live_probes.py` | Checks live trial completion, instruction loading, model identity, and distinct response accounting. |
| `live-prompt-results.json` | Four matched-scenario live runs and two initial smoke tests, with selected tool calls and actual usage. |
| `AGENTS.waiting-compatible.md` | Final compact waiting patch, matching `../waiting-benchmark/AGENTS.compact-final.md`. Tested in three clean Astra workloads; no cache-only checkpoint is prescribed. Also exported to the active workspace-specific `$CODEX_HOME/AGENTS.md`. |
| [AGENTS.waiting-explanation.ja.md](AGENTS.waiting-explanation.ja.md) | Self-contained Japanese explanation of every final-patch instruction, its intended effect, measured tradeoffs, and application steps; includes the exact English patch. |
| `AGENTS.waiting-recommended.md` | Earlier tested prompt, retained unchanged for provenance despite its filename. Superseded as distribution guidance because the five-minute rule conflicts with required commentary. |
| `AGENTS.waiting-candidate.md` | Earlier candidate retained for provenance of the smoke tests. Its external sleep interval was not reliably followed. |

Run from the repository root:

```sh
python3 docs/waiting-validation/runtime_probe.py --out tmp/wait-probes
python3 docs/waiting-validation/verify_results.py tmp/wait-probes
```

Python 3 and `codex` on `PATH` are required. Tests need permission to create a loopback listener and launch `codex app-server`. Each scenario uses a fresh temporary Codex home and a local provider that returns predetermined responses. The fake provider reports zero token usage; this is not a token-efficiency measurement. The current user's auth is not copied into the temporary home.

Each ordinary wait/parser scenario expects two backend requests. Goal scenarios allow four requests before a real `thread/goal/set` pause, then observe for one second. Per-case turn waiting is capped at 68 seconds, RPC waits at 20 seconds, and the fake backend refuses requests beyond 12. These are synthetic test goals, not objectives for this investigation or production jobs.

Select cases with `--only case-name` or comma-separated names. The complete run takes about one minute plus runtime startup and machine overhead. Raw generated requests, notifications, and stderr remain under `tmp/wait-probes`; review those before sharing. The compact exported JSON contains only selected diagnostic evidence.

The recorded `wait-config-default` case uses a one-second default and a one-millisecond minimum solely to measure that configuration is applied. These are not recommended settings. The separate explicit-short case configures a five-minute default but requests ten seconds, demonstrating that the explicit value wins.

The verifier checks recorded observations, not another runtime execution. Re-running only the verifier does not constitute a new runtime trial. Latency tolerances target local tests; a heavily loaded host can fail timing bounds without establishing a semantic regression.

The initial `live-probes.json` traces came from an intentionally instructed Astra session at `xhigh`. The later `live-prompt-results.json` contains actual Astra and Sol inference at `low`. Neither is a natural failure-rate sample. Retained response usage belongs to model responses, not to time spent inside a waiting tool. The private source conversation was not copied into this evidence package.

## Live prompt comparison

The live script consumes normal Codex account usage. It uses a private temporary copy of the existing login, removes that temporary home after the run, and exports selected diagnostics rather than authentication or complete instruction/rollout content. No real subagent is created: the prompt explicitly supplies simulated pending-subagent state, and the driver delivers the result using active-turn steering 75 seconds after the first wait begins.

Example reproducing the earlier treatment (use `AGENTS.waiting-compatible.md` and a distinct run name to investigate the revision):

```sh
python3 docs/waiting-validation/live_prompt_probe.py \
  --source-home "${CODEX_HOME:-$HOME/.codex}" --out tmp/live-wait-probes \
  --model gpt-6-astra --name astra-subagent-recommended-75 \
  --prompt docs/waiting-validation/AGENTS.waiting-recommended.md \
  --scenario subagent --delay 75
```

Omit `--prompt` for the baseline and use a distinct `--name`. The recorded comparison used one baseline and one treatment per model, all at `low`, with `sleep_tool` explicitly enabled in `always_on` mode. Astra baseline and Sol treatment ran concurrently, followed by Sol baseline and Astra treatment. This was not randomized or replicated, and cache warmness varied. The result demonstrates selection of the requested tool and a possible reduction in redundant model responses, not company savings or general reliability. Both treatment runs omitted intermediate commentary during the 75-second wait, so these results do not establish compatibility with the built-in one-minute update requirement. They do not measure the subsequent compatibility revision.

`analyze_live_probes.py` expects the four named comparison files and the two original smoke-test files. The checked-in compact JSON preserves their selected records for inspection without rerunning model calls.
