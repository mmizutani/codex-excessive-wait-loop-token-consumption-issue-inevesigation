# Outer functions.exec guidance: predeclared follow-up

Date: 2026-09-14. The user requests testing the outer `functions.exec` 45-second
recommendation and an explicit mention of the tool itself. Remove per-tool numeric
recommendations that have no demonstrated benefit. No skills are used.

The previous 18 numeric trials kept this outer number in every condition. They
cannot establish its necessity. The previous 12 section-deletion trials changed
many instructions together and do not isolate it either.

## Controls and candidates

Use the same official CLI 0.154.0, pinned catalog, Astra/low, live subscription
inference, fresh private Codex homes, disabled shared/bundled skills, 75-second job,
and audited usage collector. At most two trials run concurrently. Complete each
repetition block before the next, with a separately seeded randomized order.

All four candidates replace initial `exec_command: 30000` with the previously
tested instruction to use a long yield within tool limits and the reporting budget.
Empty `write_stdin` and `functions.wait` remain qualitative. The common 45-second
ceiling for a 60-second update cadence remains in every condition: removing a
per-tool number does not remove the reporting budget or ask for runtime defaults.

Vary two factors independently:

- Outer number: the existing literal 45,000-ms first-line pragma example versus
  qualitative first-line `@exec` / `yield_time_ms` guidance. Both require the outer
  yield to cover the inner wait plus a margin and fit the reporting budget.
- Tool name: insert `functions.exec` as the owner of that first-line setting,
  or retain the original implicit reference.

The qualitative example retains the pragma name and argument name without an
invalid placeholder JSON value. Consequently it tests practical prompt wording,
not an isolated token-level causal intervention on the digits alone. All frozen
wording and hashes are recorded in the outer manifest before live calls.

## Stage 1: factorial comparison

Run all four candidates on the natural terminal scenario, three fresh repetitions
each (12 trials). Do not force a running cell or prescribe concrete call arguments
in the task prompt: outer-default mistakes and cell resumptions must occur naturally.
The `outer-o1n0` candidate equals the previously tested `e0s0w0` prompt, but receives
fresh measurements here. Do not substitute old controls.

Count unique model responses, inclusive/uncached/cached/write/output tokens,
API-rate dollars by category, actual inner and outer arguments, running-cell returns,
functions.wait calls, completion correctness, parent commentary gaps, and result
delivery delay. Inspect exact calls where literal argument extraction is insufficient.

## Selection and confirmation

Treat a repeated return-to-model or wrapper-resumption regression as evidence for
retaining the relevant guidance. Do not attribute cache-hit shifts alone to prompt
quality. If the numeric recommendation shows no repeatable behavioral benefit,
remove it as requested, even if the qualitative wording is a few characters longer.
The previous exec30 comparison remains relevant; do not retain that number merely
because its wording is shorter.

If explicit naming has equal behavior, prefer it for clarity about which tool owns
the setting; do not claim token savings from clarity alone. If there is a material
regression, inspect its mechanism and narrowly confirm it before selecting.

Compare the selected exact candidate against the frozen original compact prompt
`e1s0w0` on terminal, CI and subagent workloads, two fresh repetitions per condition
(12 trials). This tests the combined selected wording across all relevant waits.
For this confirmation, both subagent conditions explicitly request `fork_turns:
"all"` so different history selection does not add the previously observed confound.
Record the actual call and audit compliance; parent and child usage remain separate.
Keep failures and noncompliance visible. Do not silently retry or omit them.

Update the current exported/global patch and Japanese explanation to the selected
wording, while preserving frozen historical prompts, their hashes and their results.
Distinguish the final recommendation's measurements from the original 30 follow-ups
and the older 73 trials. Subscription cache-write zero can mean unreported data;
API-rate dollars are not subscription billing. No TTL boundary is tested.

## Interrupted earlier attempt

The earlier `integration --selected e0s0w0` command was interrupted by the user.
It left a manifest and two stderr logs, without completed trial JSON records.
Process inspection after interruption found no remaining benchmark runner/app-server.
Retain those artifacts; do not count that attempt as a successful or zero-token trial.
Its unrecorded usage, if any, cannot be recovered from those files. The new stages use
separate manifests and output directories and do not resume or overwrite it.

## Scoped amendment after confirmation failure

The candidate's second subagent confirmation stopped before spawning, asking whether
to keep fork-all and inherit settings or use no history with model/effort overrides.
The added fork-all directive and the inherited task's model/effort wording admitted
this interpretation. Preserve that failed trial and its usage. Another original
subagent trial returned the correct marker plus an unrequested exit-status line;
keep its strict-format failure visible as well.

Run four fresh subagent-only trials (original and candidate, two repetitions each)
with an unambiguous common task: fork all, inherit the already configured parent
Astra/low settings, and omit model/reasoning override arguments. Use a new phase,
seed and directory (`outer-subagent`). Verify actual inheritance and omitted fields.
Do not replace the earlier records or combine their anomalously low failed counts
with successful savings comparisons. Terminal and CI work is not rerun by this fix.

## Bounded CI naming follow-up

The original confirmation's CI regression repeated: original4+4 responses versus
candidate5+5, and mean result delay11.633 versus32.494 seconds. There were no wrapper
resumptions; watcher schedules and command grouping differed. Before final selection,
run only four fresh CI trials, two each of named and unnamed qualitative wording,
under a separate seed/phase `outer-ci-name`. This assesses practical naming policy,
not pure wait-duration causality. Do not continue searching through wording until
a cheap sample appears. If outcomes are mixed, report the uncertainty and distinguish
the clarity preference from efficiency claims.

The subagent-only phase prepared for the named candidate has not yet executed at
this point. Choose its final scope after the bounded CI comparison; preserve its
prepared manifest if a different candidate needs a separately named confirmation.

## Final candidate after the bounded naming comparison

CI naming trials produced unnamed4+5 responses and named5+5, with no named advantage
in response count. Naming also had no response-count benefit in the natural terminal
factorial (unnamed9 versus named10 with no outer number). Select `outer-o0n0` for
the final subagent confirmation: omit per-tool numbers and omit the tested name
insertion. This follows minimality and observed outcomes; it does not establish that
tool naming generally increases costs or that the variants are statistically unequal.

Run the corrected four subagent trials in `outer-subagent-unnamed`, preserving the
unexecuted named-candidate `outer-subagent` manifest. The selected exact wording has
three terminal and two CI measurements in the prior separate phases. Report those
with their actual controls and sample sizes; do not present them together as one
fresh full-suite comparison against the original. No further CI search is planned.
