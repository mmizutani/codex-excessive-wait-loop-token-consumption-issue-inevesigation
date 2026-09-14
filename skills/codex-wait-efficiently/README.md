# Codex Efficient Waiting

[日本語](README.ja.md)

`codex-wait-efficiently` is a Codex skill for reducing unnecessary model calls while awaiting subagents, long terminal commands, and CI or other external jobs. It provides the waiting guidance from this repository as an automatically selectable skill, with clarifications based on runtime evaluations. The current version is **v4**, in [SKILL.md](SKILL.md).

## TL;DR

- The skill aims to keep waiting inside suitable tools and bounded watchers, reducing repeated model responses when there is no new information.
- In the new 18-trial Astra comparison, installing the final skill reduced model responses by **36.00%**, input tokens by **33.53%**, and API-price equivalent by **27.93%** overall. CI alone cost **12.87% more** and delivered results later.

## Why this skill exists

Codex can repeatedly return control to the model to check whether a command, child agent, or CI job has finished. A new model response processes input context and produces output even when the job's state is unchanged. Cached input can lower the valuation of that context, but repeated responses still consume tokens. Fixes in the examined Codex CLI 0.154.0 runtime did not eliminate every inefficient waiting pattern.

The skill guides tool selection and monitoring structure. A shell watcher can make repeated status checks without involving the model each time, while an existing terminal session can wait for output or completion. The table below describes the intended changes.

Use this format if you prefer task-based skill selection to global AGENTS.md rules. Codex discovers the skill from its name and description, then loads its instructions when selected. The measurements include that loading cost.

## Intended benefits and behavior

| Situation | Guidance | Intended effect |
| --- | --- | --- |
| Subagent work | Await the existing child with `wait_agent`; request skill use in a child task that includes waiting. | Reduce repeated status checks and help children follow the same waiting rules. |
| Long terminal commands | Retain the process session and use appropriate `exec_command` / `write_stdin` waits. | Avoid short polls that repeatedly return control to the model. |
| Code Mode | Make the outer `functions.exec` wait cover the inner command wait; resume the same running cell with `functions.wait`. | Avoid extra model responses caused by the wrapper returning too early. |
| CI and external jobs | Prefer completion notifications; otherwise use one watcher bounded by time or total check count. | Keep repeated scriptable checks in the shell, preserve job identity, and respect the user's observation limit. |
| Completion and responsiveness | Do useful independent work first, preserve required updates and verification, and report actual results. | Reduce waiting overhead while still completing the requested work. |

The rules preserve higher-priority instructions, required updates, and verification. For a 60-second progress cadence, individual waits are capped at 45 seconds to leave reporting time. They avoid unmeasured cache-only keepalives, distinguish observation timeouts from job failure, and require confirming the actual pause state for prolonged `/goal` waits.

Longer check intervals can delay detecting completion. Benefits depend on activation and instruction following; fewer model calls do not automatically mean fewer service requests or faster results.

## Install and use

1. Copy this entire directory to `${CODEX_HOME:-$HOME/.codex}/skills/codex-wait-efficiently/`. With `CODEX_HOME` unset, the destination is `~/.codex/skills/codex-wait-efficiently/`. Replace a previous copy of this skill when updating.
2. Start a new Codex session. Automatic selection is enabled by default. To request the skill explicitly, include:

   ```text
   Use $codex-wait-efficiently while waiting for this job.
   ```

3. If switching from this repository's AGENTS.md patch, remove its `## Waiting for work` section from your global AGENTS.md to avoid loading duplicate rules. Preserve your other instructions.

Normal use needs no helper scripts or other skills. The runtime evaluations used the default `sleep_tool` setting. The skill uses `clock.sleep` only when available and appropriate. The READMEs and `evals/` are supporting documentation; `SKILL.md` does not require Codex to read them during ordinary waiting.

## Direct measurement against no skill

September 15, 2026: **18 fresh trials**, Codex CLI 0.154.0, GPT-6 Astra at low reasoning effort. Each condition contains three repetitions each of a 75-second terminal command, a real subagent, and a local CI simulator. The task prompts are identical between conditions. The treatment enables only the final v4 skill with automatic selection; the control has no enabled skills. Neither condition has an AGENTS.md patch. Bundled and unrelated shared skills are disabled.

| Metric | No skill | Final v4 skill |
| --- | ---: | ---: |
| Model responses | 100 | 64 |
| Input total | 1,547,548 | 1,028,592 |
| Ordinary input | 106,396 | 76,784 |
| Cached reads | 1,441,152 | 951,808 |
| Recorded cache writes | 0 | 0 |
| Output | 4,000 | 4,599 |
| API-price equivalent | $2.705112 | $1.949598 |

Each workload row totals three trials per condition. Delay is the mean time from job completion to the final answer.

| Workload | Responses: none → v4 | API equivalent: none → v4 | Mean delay: none → v4 |
| --- | ---: | ---: | ---: |
| Terminal | 27 → 13 | $0.680330 → $0.408696 | 3.589 s → 3.839 s |
| Subagent | 49 → 30 | $1.428170 → $0.867522 | 4.420 s → 12.239 s |
| CI | 24 → 21 | $0.596612 → $0.673380 | 5.805 s → 31.073 s |

All 18 tasks returned correct results. The skill loaded in all nine treatment parents and three treatment children. All nine treatment trials passed the deterministic checks; one-second `write_stdin` requests fell from 39 to zero. Eight of nine pairs used fewer responses and input tokens, and seven cost less.

**CI cost increased despite fewer model responses.** It made 12 actual status requests per condition. Higher recorded ordinary input and output outweighed cached-read savings, increasing its API valuation by 12.87%. Two watchers used 15/30/60-second backoff and delivered results roughly 37–39 seconds later than their controls. All three watchers still started with a one-second yield, and two needed an extra Code Mode cell resumption. The deterministic pass flag does not cover every instruction.

Result delivery was slower in eight of nine pairs. The workload table shows the mean delay after job completion; it excludes time spent before the job starts, such as initial skill loading. The strongest measured savings came from terminal and subagent waiting.

Counts include parent and child inference, skill loading, and retained failed checks. Input includes cached reads and recorded writes. Dollars use the study's September 14, 2026 Standard API rate card; actual subscription charges and quota savings are unmeasured. Zero recorded writes can reflect missing upstream fields.

This is a small, interleaved Astra sample with simulated CI and uncontrolled cache state. It does not cover Sol, production CI, long-term cache retention, `/goal` pause transitions, or activation among many competing skills. The [comparison report](../../docs/CODEX_WAITING_SKILL_VS_NO_SKILL_BENCHMARK.md) provides the complete method and accounting.

## Earlier evaluation and improvements

The earlier evaluation ran **66 real Astra/low trials** across four skill versions and follow-up repetitions. It tested explicit and automatic activation, negative controls, actual children, command failure, bounded observations, independent work, and Code Mode cell resumption. All requested outcomes were correct.

V4 adds 31 words to the original: clearer bounded CI watchers and explicit skill invocation in delegated waiting work. All three final child trials loaded the skill and avoided short polls. Across its complete suite and two child follow-ups, v4 had **14/14 correct outcomes and 13/14 complete deterministic passes**; one CI run still used a one-second cell wait.

The original and final 12-case suites used **57 versus 58 responses**, with API equivalents of **$1.856236 versus $1.945212**. Those results did not establish savings from revising the skill. The new comparison above answers the separate question of installing the final skill versus no skill. See the [earlier report](../../docs/CODEX_WAITING_SKILL_EVALUATION.md) for all candidates and retained failures.

## Relationship to the AGENTS.md patch

The skill started from the [final AGENTS.md patch](../../docs/waiting-validation/AGENTS.waiting-compatible.md). The observed reductions were smaller for the skill. Each column below shows the reduction against that experiment's own untreated control; both studies used 18 Astra/low trials on CLI 0.154.0.

| Metric reduced | AGENTS.md patch | Final v4 skill |
| --- | ---: | ---: |
| Model responses | 52.04% | 36.00% |
| Input tokens, including cached input | 51.03% | 33.53% |
| API-price equivalent | 42.31% | 27.93% |

Within the skill experiment, terminal and subagent API valuations fell 39.93% and 39.26%, while CI's increased 12.87%, reducing the overall saving. These workload effects do not isolate the reason for the difference between the two studies.

The [AGENTS.md experiment](../../docs/CODEX_WAITING_LATEST_VS_NO_PATCH_BENCHMARK.md) and [skill experiment](../../docs/CODEX_WAITING_SKILL_VS_NO_SKILL_BENCHMARK.md) used different task prompts and instruction-loading conditions, with uncontrolled cache state and backend scheduling. This supports smaller observed savings in the skill study. A direct controlled comparison is still needed to establish whether the installation format itself changes efficiency.

## Package and evidence

| File | Purpose |
| --- | --- |
| [SKILL.md](SKILL.md) | Current v4 instructions used by Codex. |
| [agents/openai.yaml](agents/openai.yaml) | Codex display name and description. |
| [evals/README.md](evals/README.md) | Evaluation procedures, prerequisites, and offline regrading. |
| [Direct comparison plan](evals/comparisons/skill-vs-none/PLAN.md) | Conditions and measurements declared before inference. |
| [Direct comparison counts](evals/comparisons/skill-vs-none/COUNTS.md) | Per-trial parent/child tokens, costs, and matched changes. |
| [Revision history](evals/REVISIONS.md) | Why candidates were changed or rejected. |

The evaluation tools also depend on collectors and fixtures elsewhere in this repository. Run them from a repository checkout. Live evaluations consume account usage; regrading the exported evidence needs no model calls. Archived versions use `SKILL.md.fixture` so Codex does not discover them as duplicate installed skills.
