# Codex waiting overhead: investigation and proposed mitigation

Codex can repeatedly call the model while waiting for subagents, terminal commands, or CI, consuming tokens even when nothing has changed. This repository provides a measured AGENTS.md patch and a skill alternative to reduce that overhead while preserving required progress reports and completion checks.

## Latest and final proposed AGENTS.md patch

**Use [AGENTS.waiting-compatible.md](docs/guides/AGENTS.waiting-compatible.md), the final verified patch as of September 15, 2026.**

It directs Codex to wait through existing tools and sessions, coordinate outer and inner waits in Code Mode, and use bounded watchers for external jobs. The exact wording was directly compared against no patch in the measurements below.

### Apply it

1. Copy the patch into your global `${CODEX_HOME:-$HOME/.codex}/AGENTS.md` (normally `~/.codex/AGENTS.md`).
2. Replace any existing `## Waiting for work` section, preserving your other instructions.
3. Start a new Codex session.

The [Japanese explanation](docs/guides/AGENTS.waiting-explanation.ja.md) covers each rule, its relationship to Codex's built-in instructions, and the measured tradeoffs.

### Skill alternative

Install **[codex-wait-efficiently](skills/codex-wait-efficiently/SKILL.md)** if you prefer automatic skill selection to global AGENTS.md instructions.

1. Copy the entire `skills/codex-wait-efficiently/` directory into `${CODEX_HOME:-$HOME/.codex}/skills/codex-wait-efficiently/`.
2. Start a new Codex session. To request the skill explicitly, include `Use $codex-wait-efficiently while waiting for this job.` in your prompt.
3. If switching from the patch, remove its `## Waiting for work` section from global AGENTS.md to avoid duplicate instructions. Preserve your other instructions.

See the [English skill README](skills/codex-wait-efficiently/README.md) or [日本語 README](skills/codex-wait-efficiently/README.ja.md) for usage and evaluation details. Its measured effects are compared below.

## Measured effects of the exact final patch

**18 trials on GPT-6 Astra / low, Codex CLI 0.154.0:** three repetitions per condition of a 75-second terminal command, a real subagent, and a local CI simulator. Shared and bundled skill instructions were disabled; only the patch differed between conditions. Totals include parent and child inference.

| Metric | No patch | Exact final patch | Reduction |
| --- | ---: | ---: | ---: |
| Model responses | 98 | 47 | 52.04% |
| Input tokens, including cached input | 1,515,920 | 742,417 | 51.03% |
| API-price equivalent | $2.618056 | $1.510370 | 42.31% |

All 18 jobs completed, and all nine matched pairs improved on these three measures. One-second `write_stdin` requests fell **24→0**, and extra Code Mode cell-resumption calls **9→0**. Parent progress gaps stayed within 60 seconds in **1/9** unpatched trials and **9/9** patched trials. Result delivery was slower in five of nine pairs. See the [full report](docs/reports/CODEX_WAITING_LATEST_VS_NO_PATCH_BENCHMARK.md) for methods, timing, and retained check failures.

These savings apply to the tested Astra workloads. The final patch has not been measured on Sol, and these short trials do not establish effects for 30-minute cache expiration, prolonged `/goal` waits, or production CI.

## AGENTS.md patch and skill: observed reductions

Two separate 18-trial Astra/low experiments on CLI 0.154.0 measured each option against its own untreated control:

| Metric reduced | AGENTS.md patch | Final skill |
| --- | ---: | ---: |
| Model responses | 52.04% | 36.00% |
| Input tokens, including cached input | 51.03% | 33.53% |
| API-price equivalent | 42.31% | 27.93% |

All 18 skill-study tasks completed correctly. Terminal and subagent API valuations fell about 40%; CI's rose **12.87%**, with results delivered **25.27 seconds later** on average. This reduced the skill's overall saving.

The skill showed smaller reductions, but the studies used different task prompts and instruction-loading conditions, with uncontrolled cache state and scheduling. They do **not establish which installation format is cheaper**. See the [skill comparison and its limits](docs/reports/CODEX_WAITING_SKILL_VS_NO_SKILL_BENCHMARK.md#comparison-with-agentsmd-measurements).

Dollar figures in both studies apply September 14, 2026 Standard API rates to subscription-reported tokens; they are **not subscription charges**. Recorded cache writes were zero, which may reflect missing upstream fields. The reports link complete input, cached-read, cache-write, and output counts.

## Reports and evidence

The [documentation index](docs/README.md) links the guides, reports, captured results, and reproduction instructions.
