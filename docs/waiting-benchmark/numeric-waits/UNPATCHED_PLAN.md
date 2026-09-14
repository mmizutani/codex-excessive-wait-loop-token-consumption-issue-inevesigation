# Exact latest patch versus no patch: predeclared direct comparison

Date: 2026-09-15. The user requests a direct comparison after identifying that
the latest wording had only been compared with earlier patched versions.
No skills are used. Do not change the prompt or reuse previous trial results.

## Conditions

- `no-patch`: no AGENTS.md file installed in a fresh temporary CODEX_HOME.
- `wording-no-pragma`: the exact current distribution patch, frozen at SHA256
  `882067320df757cc72afaf1fa542e9c476d0c445d4f52a0ea683eb38e2daa411`.

Use the same official installed CLI 0.154.0, pinned model catalog, Astra/low,
live subscription authentication, fresh temporary homes and work directories,
disabled shared/bundled skill instructions, and 75-second workloads as before.
The only intentional difference is installing the waiting patch. Native sleep
exposure and all runtime configuration remain at the same settings in both arms.

Record whether AGENTS.md exists after setup and whether its waiting section occurs
in user-instruction messages in each captured session. No-patch controls must have
neither the file nor those instructions. Patched parent and child sessions must
contain the waiting section; verify the exact parent prompt and frozen hash too.
Temporary work directories are outside the investigation repository, so its global
waiting addition is not discovered through the working-directory ancestors.

## Workloads and ordering

Run terminal, CI and subagent workloads three times per condition: 18 fresh trials,
nine matched workload/repetition pairs. All three repetition blocks are declared
before live calls. Shuffle each block's six tasks with the recorded seed, run at
most two at once, and finish the block before the next. Both arms receive identical
task text. Subagent tasks explicitly require fork-all and inherited Astra/low,
without model or effort override arguments, as in the preceding wording study.

Commands and subagents are real. CI uses the same local state simulator, with no
built-in watch mode or completion notification. Do not prescribe wait values or
force running cells. Let each condition choose its actual waiting behavior.

## Measurement and interpretation

Reuse the audited usage collector and price accounting. New collector fields only
record instruction presence; they do not change tasks, tools or timing. Preserve
every trial, including failures and format deviations, and never count incomplete
work as savings. No silent retries or selection of favorable repetitions.

Reconcile unique response IDs with each session's cumulative counts. Separate
parent/child responses, inclusive input, ordinary input, cached reads, recorded
cache writes, output and included reasoning. Use the same dated September 14 API
rate card; these are subscription usage valuations, not subscription charges or
newly verified prices. Recorded write zeros may reflect missing upstream fields.

Report overall and workload-specific totals, matched-pair differences, completion,
exact final result, single job/child counts, actual model/effort, skill exclusion,
actual wait arguments, short preliminary polls, outer-cell returns and resumptions,
native sleeps/subagent waits, CI status-query counts, parent commentary gaps and
delivery delay. Inspect full calls where literal projections are insufficient.

Make the conclusion follow this direct comparison even if it contradicts the
earlier inferred benefit. Separate token/response effects from cache-dependent
dollar ranking and notification-delay tradeoffs. Three repetitions are still
small and do not establish universal savings, a statistical guarantee, behavior
on Sol or other runtime versions, or 30-minute cache/goal behavior.

Export a Markdown report with TL;DR and the disjoint token/dollar categories.
Update statements that the exact current prompt has no direct unpatched control,
while retaining all historical records and their original comparison scope.
