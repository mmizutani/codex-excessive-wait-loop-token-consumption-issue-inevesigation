# Codex waiting overhead: investigation and proposed mitigation

Codex can repeatedly return control to the model while waiting for subagents, terminal commands, or CI. Each model response consumes tokens, even when the underlying status has not changed. This repository investigates that overhead and measures a user-side AGENTS.md addition intended to reduce unnecessary model-driven checks while preserving completion handling and required progress reports.

## Latest and final proposed AGENTS.md patch

**Use [docs/waiting-validation/AGENTS.waiting-compatible.md](docs/waiting-validation/AGENTS.waiting-compatible.md). This is the latest and final proposed patch from this investigation, as of September 15, 2026.**

That exact wording was directly compared against no patch in the measurements below. It matches the frozen [AGENTS.wording-no-pragma.md](docs/waiting-benchmark/numeric-waits/prompts/AGENTS.wording-no-pragma.md). Earlier candidates, including files named `AGENTS.compact-final.md` and `AGENTS.waiting-recommended.md`, remain available as historical evidence.

The patch directs Codex to retain existing jobs and sessions, use suitable tool waits, coordinate outer and inner waits in Code Mode, and use bounded watchers for scriptable external status checks. It keeps required progress updates and verification, and avoids unmeasured cache-only keepalives. No skill is required.

### Apply it

1. Copy the complete contents of [AGENTS.waiting-compatible.md](docs/waiting-validation/AGENTS.waiting-compatible.md) into your global `${CODEX_HOME:-$HOME/.codex}/AGENTS.md`. With `CODEX_HOME` unset, this is normally `~/.codex/AGENTS.md`.
2. Replace an existing `## Waiting for work` section with this version, preserving your other instructions.
3. Start a new Codex session to load the addition.

See the [self-contained Japanese explanation](docs/waiting-validation/AGENTS.waiting-explanation.ja.md) for the purpose of each rule, its relationship to Codex's built-in instructions, and the measured tradeoffs.

### Skill alternative

For skill-based use, install **[codex-wait-efficiently](skills/codex-wait-efficiently/SKILL.md)**. The evaluated v4 skill follows the final patch, clarifies bounded CI watchers, and explicitly requests skill use in delegated work that includes waiting. The package is self-contained: `SKILL.md` holds all the rules, and `agents/openai.yaml` supplies the Codex UI name and description. Normal waiting requires no helper scripts, external references, or other skills. The bundled `evals/` directory contains optional evaluation tools and evidence.

1. Copy the entire `skills/codex-wait-efficiently/` directory into `${CODEX_HOME:-$HOME/.codex}/skills/codex-wait-efficiently/`.
2. Start a new Codex session. Automatic selection is allowed by default; to request it explicitly, include `Use $codex-wait-efficiently while waiting for this job.` in your prompt.
3. When switching from the AGENTS.md method, remove the corresponding `## Waiting for work` section from your global AGENTS.md to avoid loading duplicate instructions. Preserve your other global instructions.

The skill has a separate [runtime evaluation report](docs/CODEX_WAITING_SKILL_EVALUATION.md), covering activation, negative controls, command failure, bounded observations, child sessions, and measured usage. The [evaluation suite and evidence](skills/codex-wait-efficiently/evals/README.md) follow OpenAI's skill-evaluation workflow. Structural validation and a [CLI 0.154.0 discovery check](docs/waiting-validation/skill-package-validation.json) also passed.

Across 66 skill trials, all requested outcomes were correct. The final version passed 13/14 trials' deterministic checks, with one remaining short CI cell wait. Its three child trials read the skill and avoided short polls. **General skill-specific savings remain unproven:** the original and final 12-case suites used 57 and 58 responses respectively, with API equivalents of $1.856236 and $1.945212.

**The savings below belong to the AGENTS.md experiment.** The skill evaluation compares its original and revised versions; it does not establish the same savings against no skill or compare the two installation formats directly.

## Measured effects of the exact final patch

**18 fresh trials:** GPT-6 Astra at low reasoning effort, Codex CLI 0.154.0, with shared and bundled skill instructions disabled. Each condition contains three repetitions each of a 75-second terminal command, a real subagent running that command, and a local CI status simulator. Both conditions use the same runtime configuration; only the waiting patch is added. Totals include parent and child inference.

| Metric | No patch | Exact final patch | Reduction |
| --- | ---: | ---: | ---: |
| Model responses | 98 | 47 | 52.04% |
| Input tokens, including cached input | 1,515,920 | 742,417 | 51.03% |
| API-price equivalent | $2.618056 | $1.510370 | 42.31% |

All nine matched workload/repetition pairs improved on these three measures. One-second `write_stdin` requests fell from 24 to zero, and extra Code Mode cell-resumption calls fell from nine to zero. All 18 jobs completed and their usage counters reconciled. Parent progress gaps stayed within 60 seconds in 1/9 unpatched trials and 9/9 patched trials. One unpatched trial returned the correct result with extra formatting and failed the strict answer-format check; it remains in the totals.

These are **observed savings for these Astra workloads**. The latest wording has not been measured on Sol; earlier Sol comparisons did not establish consistent overall savings. The measurements do not establish universal savings or the cheapest possible wording.

Result delivery became slower in five of nine matched pairs. Terminal delivery was about 1.1 seconds slower on average; one CI pair was about 11.4 seconds slower. Actual CI status requests fell only 14→13, while model responses fell 28→14. Reducing model calls, reducing service requests, and delivering results promptly are separate outcomes.

Dollar amounts apply the study's September 14, 2026 Standard API rates to subscription-reported counters; they are **not subscription charges**. Input includes cached reads. Recorded cache writes were zero, but missing upstream fields may have been normalized to zero. The [full counts](docs/waiting-benchmark/numeric-waits/unpatched-results/COUNTS.md) separate ordinary input, cached reads, recorded writes, output, and dollar components. These 75-second trials do not measure 30-minute cache expiration, prolonged `/goal` waits, or production CI failure handling.

## Reports and evidence

| File | Purpose |
| --- | --- |
| [Final patch](docs/waiting-validation/AGENTS.waiting-compatible.md) | The proposed addition to install in global AGENTS.md. |
| [Skill alternative](skills/codex-wait-efficiently/SKILL.md) | Evaluated v4 skill, with bounded-watcher clarification and explicit skill invocation in delegated waiting work. |
| [Skill evaluation](docs/CODEX_WAITING_SKILL_EVALUATION.md) | Activation, process review, failure handling, token/cost measurements, and reproducible fixtures for the original and revised skills. |
| [Japanese explanation](docs/waiting-validation/AGENTS.waiting-explanation.ja.md) | Why each instruction is needed and how to apply it. |
| [Latest direct-comparison report](docs/CODEX_WAITING_LATEST_VS_NO_PATCH_BENCHMARK.md) | TL;DR, methods, token and dollar breakdowns, paired results, wait behavior, and limitations. |
| [Runtime and prompt benchmark](docs/CODEX_WAITING_RUNTIME_PROMPT_BENCHMARK.md) | Current results plus historical CLI, Astra/Sol, and prompt-version comparisons. |
| [Independent runtime validation](docs/CODEX_ASTRA_SOL_WAITING_INDEPENDENT_VALIDATION.md) | Runtime mechanisms, source evidence, and remaining issues. |
| [Reproduction instructions](docs/waiting-benchmark/numeric-waits/README.md#exact-current-wording-versus-no-patch) | How to reproduce and analyze the exact final-patch comparison. Live runs consume normal account usage. |
| [Captured calls and usage](docs/waiting-benchmark/numeric-waits/unpatched-results/trial-evidence.json) | Selected per-trial execution and accounting evidence. |
| [Integrity checks](docs/waiting-benchmark/numeric-waits/unpatched-results/validation.json) | Prompt identity, counter reconciliation, retained exceptions, and comparison totals. |

Earlier frozen prompts and reports preserve the history of this independent investigation. Their filenames and earlier conclusions should be read in the context of the version each experiment measured.
