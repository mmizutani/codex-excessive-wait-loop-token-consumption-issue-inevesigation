# Explicit numeric waits: predeclared comparison

Date: 2026-09-14. The user requests live measurements to choose whether to state
numeric overrides for `exec_command`, `write_stdin`, and `functions.wait`.
`functions.exec` retains its explicit 45,000 ms outer yield in every variant.

## Controls

- Official installed Codex CLI 0.154.0; GPT-6 Astra, low reasoning; live subscription
  inference, same pinned catalog as the earlier benchmark.
- Shared skill instructions and bundled skills disabled, fresh private Codex homes,
  existing authentication copied privately and removed after each trial.
- Same 75-second job and completion verification as the earlier benchmark.
- No changes to frozen historical prompts. The existing compact prompt is the
  control: explicit initial exec 30 seconds, qualitative stdin/wrapper continuation.
- Three repetition blocks; deterministic shuffled condition order, at most two
  trials concurrently, complete one block before the next. No old controls are
  substituted for fresh runs. Cache and backend variation remain uncontrolled.

## Comparisons

1. Terminal: 2×2 factorial (12 trials). Explicit initial exec 30,000 ms versus a
   long wait within tool/reporting limits; explicit empty stdin 40,000 ms versus
   the existing qualitative budget instruction. All retain the qualitative
   `functions.wait` clause. This distinguishes initial and subsequent command waits.
2. Running Code Mode cell: qualitative versus explicit `functions.wait` 45,000 ms
   (6 trials), other clauses equal to the existing compact control. The scenario
   requires the same initial JavaScript with a 1 ms outer yield and 30-second inner
   exec wait, ensuring a real running cell needs resumption. After that, normal
   patch guidance applies. This is a deliberately forced diagnostic, not evidence
   of the frequency of this situation in ordinary workloads. Model inference and
   the 75-second command remain real.

## Outcomes and decision

Retain every attempted trial, including failures and noncompliance. Require exactly
one command launch, completion evidence, correct final result, no shared skills,
and reconciled per-response/cumulative counters. Inspect actual numeric arguments,
early wrapper returns, parent commentary gaps, and result delay.

Report inclusive input, uncached input, cached reads, normalized cache writes,
output (reasoning included), response count, and category-specific API-price USD
using the same dated Standard rate card as the historical comparison. A normalized
zero cache-write count may mean an absent upstream field; this is not a bill.

Prefer a candidate when repeated runs show fewer responses and lower aggregate
token/cost usage without a completion failure or a systematic reporting/delivery
regression. A single cheap run or cache-hit shift is insufficient. If equal or
mixed, avoid claiming demonstrated savings; retain the established wording unless
a simpler equivalent is consistently observed. This small sample does not prove
global optimality. Do not attribute effects to a clause the model never used.

After examining the isolated results, test the chosen combined wording against
the current control on terminal, CI, and subagent workloads with two fresh runs per
condition if the chosen wording changes. Preserve historical results and identify
the newly recommended version separately in the report and Japanese explanation.

## User-requested extension: remove the entire terminal section

Added while the last two isolated trials were running, before any whole-section
trial: the user asks whether `### Terminal commands` is itself unnecessary.

Run two fresh blocks of terminal, CI, and subagent workloads, comparing the exact
current compact control with a variant deleting only the entire Terminal commands
section (12 trials). Other sections, including the common 45-second wait ceiling,
are unchanged. This tests all the section's guidance together; it does not attribute
an effect to any one sentence. Use a separate deterministic shuffle seed and the
same runtime, model, effort, catalog, skill isolation, delay, and acceptance checks.

Do not use the earlier numeric trials as these controls. If deletion has consistent
cost/response savings with no meaningful regression across workloads, prefer the
shorter patch. If deletion produces extra polling, weaker execution or reporting,
or mixed evidence, retain the section and explain the observed scope. If the chosen
change is exactly this deletion, this phase supplies the cross-workload validation;
do not repeat the same integration experiment under another name.
