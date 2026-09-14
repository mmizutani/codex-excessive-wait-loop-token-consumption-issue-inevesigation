# Final skill versus no skill: measurement plan

Declared before running this comparison on September 15, 2026.

Measure whether installing the unchanged final v4 skill reduces model responses, token usage, and API-price equivalent for sustained waiting. Preserve the requested outcomes and report latency separately. The audience is Codex users deciding whether to install this skill; these measurements cannot establish universal savings.

## Conditions and sample

- Codex CLI 0.154.0, GPT-6 Astra at low reasoning effort, the same pinned catalog and dated rate card as the prior evaluations.
- `none`: no target skill installed or enabled. `v4`: only the frozen final skill enabled, with normal automatic selection. Both receive identical task prompts without a skill mention or attachment.
- No AGENTS.md in either condition. Bundled and unrelated shared skills disabled. Verify the actual enabled catalog before each turn; check captured parent and child sessions for unexpected skill loading in the control.
- Reuse the frozen `implicit-terminal`, `implicit-subagent`, and `contextual-ci` cases. Each job takes 75 seconds. The CI status service is simulated locally; terminal commands and children are real.
- Three fresh repetitions per case and condition: **18 trials, nine matched pairs**. Shuffle the full schedule with seed 20260915; run at most two trials concurrently. Each trial gets a fresh temporary home and workspace. Skill loading and any child handoff are part of treatment usage.
- Keep all runs, including missed activation, short polling, result-format failures, and deadline failures. Do not silently rerun unfavorable observations. The existing per-trial deadline and item limit bound runtime usage.

## Measurements and interpretation

Report aggregate and per-workload parent-plus-child response counts; total input, ordinary input, cached reads, recorded writes, output tokens; disjoint API dollar components; matched changes; and result-delivery delay. Inspect short process waits, Code Mode resumptions, actual CI request counts, activation, job identity, completion, and progress gaps.

Primary comparison: all nine workload runs per condition, plus all nine paired changes. Correctness and accounting must be assessed before describing a decrease as efficiency. A deterministic process failure remains visible even when the task outcome is correct. Include activation overhead and failures in the totals.

Use the study's September 14 Standard API rate card as a consistent valuation of subscription counters. Recorded write zeros can represent absent upstream fields; actual subscription billing and quota savings are unmeasured. Cache state and service scheduling are uncontrolled. This is an interleaved small-sample comparison, not a guarantee for other jobs, models, durations, or configurations.

## Artifacts

Freeze the manifest here before inference. Export selected evidence and a reproducible comparison summary into this directory. Keep the prior 66-trial evidence separate and unchanged. Update the evaluation report and the new English/Japanese skill READMEs with the measured scope, results, and limitations. Do not change the evaluated SKILL.md as part of this comparison.
