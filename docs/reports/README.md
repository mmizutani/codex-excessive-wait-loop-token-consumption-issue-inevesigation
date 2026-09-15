# Investigation and benchmark reports

The current recommendation is [AGENTS.waiting-compatible.md](../guides/AGENTS.waiting-compatible.md). Read its [Japanese explanation](../guides/AGENTS.waiting-explanation.ja.md) for the purpose of each instruction, or the [documentation index](../README.md) for installation and evidence links.

## Current recommendation and direct measurements

| Report | What it establishes |
| --- | --- |
| [Final patch versus no patch](CODEX_WAITING_LATEST_VS_NO_PATCH_BENCHMARK.md) | Direct 18-trial Astra comparison of the exact current AGENTS.md wording, including tokens, API valuation, and result delays. |
| [Final skill versus no skill](CODEX_WAITING_SKILL_VS_NO_SKILL_BENCHMARK.md) | Direct 18-trial Astra comparison of final-skill installation, including CI regressions and the separate AGENTS.md study's results. |
| [Skill evaluation](CODEX_WAITING_SKILL_EVALUATION.md) | Activation, outcomes, waiting behavior, child sessions, and usage across skill revisions. |
| [Independent runtime validation](CODEX_ASTRA_SOL_WAITING_INDEPENDENT_VALIDATION.md) | Source and runtime evidence for waiting mechanisms, relevant fixes, configuration, and remaining limitations. |

## Earlier comparisons and prompt decisions

These reports explain how the final wording was selected. Their historical candidates are retained in the [patch archive](../archive/agents-patches/README.md).

| Report | Scope |
| --- | --- |
| [Runtime and prompt benchmark](CODEX_WAITING_RUNTIME_PROMPT_BENCHMARK.md) | Older/current CLI comparisons, Astra/Sol differences, prompt tuning, and later result summaries. |
| [Numeric wait overrides](CODEX_WAITING_NUMERIC_OVERRIDES_BENCHMARK.md) | Explicit tool timeout values and removal of the Terminal commands section. |
| [Outer Code Mode wait](CODEX_WAITING_OUTER_EXEC_BENCHMARK.md) | Outer wait duration, explicit tool naming, and integration checks. |
| [Pragma removal](CODEX_WAITING_PRAGMA_REMOVAL_BENCHMARK.md) | Remeasurement after clarifying outer/inner waits and omitting configuration syntax. |

Reports moved here from the `docs/` root. Their measurements and conclusions are preserved; local links follow the current layout.
