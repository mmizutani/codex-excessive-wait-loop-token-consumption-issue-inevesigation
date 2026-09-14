# Three-condition waiting benchmark

Run actual Astra and Sol inference through isolated Codex app-server instances.

- (1) Official CLI 0.151.0, the latest stable tag excluding PR #41243.
- (2) Official CLI 0.154.0.
- (3) CLI 0.154.0 plus a frozen copy of the current global waiting addition.
- All cases use today's backend and the same pinned current model catalog, low reasoning, normal speed, and explicit multi-agent availability. Sleep gating remains at each runtime's default in the primary comparison.
- Three workloads: one real 75-second terminal process, one real subagent running that process, and a local CI-status simulator with a 75-second pending stage. The CI simulator has no completion callback or watch command.
- Two repetitions per cell where feasible; at most two trials concurrently. Counterbalance condition order across repetitions. Never overwrite a recorded trial.
- Record per-response input, cached input, cache-write input, output, included reasoning, total tokens, response count, tool calls, successful completion, detection delay, and commentary gaps. Separate parent and child usage. Zero/defaulted cache-write fields do not prove free cache writes.
- Compare runtime conditions (1)/(2) separately from prompt conditions (2)/(3). Differences reflect the full client release delta, not a causal estimate for a single PR. Today's old-client runs cannot restore the backend conditions described in the September 12 announcement.
- A useful prompt improvement targets at least 20% fewer parent model responses without premature completion, duplicate jobs, or substantial detection-delay regression. Report raw tokens even when this criterion fails. Small samples and cache variation prohibit a company-savings claim.
- If the prompt is weak or inconsistent, consult an agent on concrete traces, make a bounded revision, and run fresh matched trials. Preserve the original prompt and results.
- This short benchmark does not measure the 30-minute cache TTL or historical backend fixes.

## Follow-up phase: isolate skills and validate a revision

The primary homes still discover shared `~/.agents/skills`. This common environment is retained and labeled, rather than silently reclassifying it as a bare runtime comparison. In particular, both models loaded the monitoring skill for CI.

A second phase disables the skills instruction block and bundled skills through supported configuration on both versions. Two 2-second smoke runs confirmed successful execution without a skills instruction block. The analyzer also rejects skill-reading tool calls in the clean phase.

Run one fresh 75-second trial for every supported model/scenario/condition across old, new, original patch, and tuned-v2 (21 trials). Keep at most two trials concurrently. This exploratory phase separates ambient skill effects and tests a concrete revision; it is not a statistically powered study. Preserve all original results, and repeat a targeted matched pair if the candidate needs a stability check.

The v2 candidate makes wrapper controls explicit, removes preliminary short command polls, and budgets waits from the last commentary update. It replaces the untested 25-minute cache checkpoint with the user's current preference against cache-only keepalives without measured savings. The 75-second runs cannot validate cache TTL.

Two additional clean Sol CI trials (new-on and tuned-on) enable `sleep_tool` in `always_on` mode. These run after the clean phase and isolate the optional feature setting from the primary runtime/prompt conditions. They are exploratory single repetitions, not pooled into default-gating results.

The first clean v2 Astra terminal trace reduced responses to 4, but missed the update interval (65.371s): after a 30s tool return, model turnaround consumed another 11s before a 19s wait. V3 replaces elapsed-budget arithmetic with a brief update in the same response before each blocking wait while only waiting remains. Before v3 trials start, set its cap to 45s to leave 15s for turnaround, informed by the observed 11.336s delay. This is a margin heuristic, not a hard latency guarantee. Run six fresh v3 trials, one per model/workload, after the other phases; compare transparently against the earlier clean controls. This is another exploratory phase, not a new randomized control study. Preserve the failed cadence result for v2.

Before v3 begins, clean Astra CI traces show 8 responses for both baseline and v2: each status cycle is a separate model-issued sleep and command, and backoff raises detection delay from 11.002s to 43.882s. V3 clarifies the existing watcher preference: when checks can be scripted, run one bounded shell watcher emitting meaningful changes and retain its session; native sleep is the fallback. This is tested across both CI cases in the six-trial v3 phase.

V3 completed all six workloads with parent message gaps below 60s, but trace review found neither CI watcher had an explicit termination bound. Sol increased status checks from 4 to 15. V4 changes only the CI clause to require an explicit time/check-count limit and apply interval selection/backoff to watchers as well. Run two additional 75-second CI trials, one per model, with no skill instructions and default sleep gating. V4 terminal/subagent behavior is not separately rerun; the unchanged rules were exercised under v3. Preserve both versions' traces and mark this validation boundary.

## Astra baseline follow-up: CLI 0.153.1

The user identified PR #42605, which backports the Astra catalog to 0.153.1. Download the official CLI and matching code-mode host, verify release-asset SHA256 digests, and run a 2-second compatibility probe. The live backend accepted Astra; this removes the previous inability to test an earlier Astra client.

Run six 75-second Astra trials with 0.153.1 and no waiting patch (2 repetitions × 3 workloads) in the original ambient-skill environment. Then run three equivalent clean trials (1 per workload). Preserve the existing 0.154.0 controls and initial-patch records; comparisons are supplemental sequential observations, not newly randomized contemporaneous pairs. Keep at most two workload trials concurrently, the same pinned current catalog and low effort, and default sleep gating.

This baseline already contains PR #41243. Its V2 wait handler, sleep handler, and multi-agent session file match 0.154.0 byte-for-byte, while other execution code differs. It is an earlier compatible client, not a pre-#41243 baseline or a reconstruction of historical server behavior. Export all token categories, parent/child counts, API-rate valuations, completion results, and delays separately, and update the report's Astra-unavailable wording without erasing the actual 0.151.0 rejection.

## Final compact patch: Astra-only clean tables

Freeze the current export as `AGENTS.compact-final.md`. Run three new 75-second Astra trials on official CLI 0.154.0, one per terminal/subagent/CI workload, with shared skill instructions and bundled skills disabled, low effort, the same pinned catalog, and default sleep gating. Keep at most two trials concurrent. Use a fresh output directory and preserve every prior result.

The requested final-patch tables compare these three new trials with the existing three clean Astra 0.153.1 trials and three clean unpatched 0.154.0 trials. These are sequential exploratory comparisons, not new randomized pairs. Do not substitute the earlier v3 or v4 measurements for the compact patch. Verify actual prompt loading/hash, parent and child accounting, model identity, skill isolation, successful completion, watcher behavior, and update gaps. Export all input/cache/output categories and API-rate dollar equivalents; retain their cache-write observability limitation.
