# Runtime remeasurement of the September 15 wording

Date: 2026-09-15. The user requests live remeasurement after removing the
first-line `@exec` syntax from the clarified outer/inner wait instruction.
No skills are used. Historical prompts, manifests and measurements stay frozen.

## Conditions and scope

Run three complete prompts, frozen before live execution:

- `wording-measured`: exact previously selected `outer-o0n0` wording, with implicit
  tool ownership and explicit first-line pragma guidance.
- `wording-with-pragma`: the September 15 clarification naming the outer and inner
  tools and explaining cell resumption, still with first-line pragma guidance.
- `wording-no-pragma`: exact current distribution prompt; retains named roles and
  timing requirements, but delegates outer-setting syntax to the runtime schema.

The latter pair changes only the first sentence of the Code Mode paragraph.
It measures the practical rewrite, including its phrasing, rather than an isolated
effect of the literal `@exec` token. The first versus third compares the complete
revision to the previously measured recommendation using fresh controls.

Use official installed CLI 0.154.0, the same pinned catalog as prior experiments,
Astra/low, live subscription authentication, fresh private CODEX_HOME/work directories,
disabled shared/bundled skill instructions, and 75-second jobs. Terminal processes
and subagents are real; CI status comes from the same local simulator. No API model
responses are mocked. At most two trials run concurrently.

Run all three conditions on terminal, CI and subagent scenarios twice: 18 trials.
Shuffle each repetition with the recorded seed and complete its nine trials before
starting the next repetition. Subagent tasks explicitly request fork-all, inherited
parent Astra/low settings and omission of model/effort overrides, avoiding the earlier
task ambiguity. All other scenario instructions remain unchanged.

Do not prescribe tool arguments or force an outer-cell return in these natural
workloads. If no running cell occurs, report that the fallback was not exercised
in these new trials; do not claim its behavior was newly established.

## Evidence and decision

Reuse the audited collector and accounting. Count unique model responses; inclusive
input, ordinary input, cached reads, recorded writes, output and included reasoning;
and parent/child usage separately. Reconcile every session to cumulative counters.
Value at the same dated September 14 API rates for comparability, not as subscription
charges or a newly verified price quote. A recorded write count of zero can mean
the upstream field was absent.

Check exact result, successful exit, one original job, required child count,
actual model/effort/fork settings, loaded prompt, disabled skills, actual wait
arguments, outer running-cell returns, cell-resumption calls, meaningful CI checks,
parent update gaps and result-delivery delay. Inspect full call text where projected
literal arguments are insufficient. Preserve all failures, format violations and
usage; do not silently retry or select favorable samples.

Compare paired response counts and behavior first, and report token categories and
API valuation even when cache variation reverses their ranking. Two repetitions do
not establish statistical equivalence or universal portability. In particular,
identify any return-to-model caused by an outer default shorter than its inner wait.
An extra inner wait just before job completion is a different mechanism.

Keep the user's revised wording if the trials do not reveal a material defect.
If a repeatable outer-wait regression appears, inspect its mechanism before proposing
a minimal correction; do not silently restore syntax the user asked to remove.
No extra tuning trials are preauthorized by this plan merely to find cheaper values.
Report the completed comparison in Markdown and synchronize the guidance's evidence
references to the exact version actually measured.
