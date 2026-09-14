# Agent consultation after weak initial prompt results

The user authorized agent consultation and prompt tuning if the additional prompt had weak effects. After the first Astra terminal pair showed 8 versus 7 parent responses, two bounded read-only reviews were performed while the primary trials continued.

- Astra at low effort reviewed the exact tool traces. It identified an unnecessary initial short process poll, a long inner wait with the outer code-mode yield left at its default, repeated one-second wrapper waits, and a wait duration that ignored time already elapsed since commentary. The parent independently checked those calls and timestamps.
- Sol at low effort reviewed attribution, pricing, and experimental design. It confirmed disjoint input/read/write/output pricing and the per-request long-context rule. It recommended checking every session against final cumulative counters, checking input plus output against total, and retaining the old-client Astra limitation and cache/concurrency caveats. Those counter checks were added to the analyzer.

The first Astra pair was 8→7 responses (12.5%) and $0.291390→$0.280352 at Standard API rates applied to the reported counts (3.79%). The patch increased ordinary input and output slightly despite reducing cached reads. These observations did not meet the predeclared 20% response-count target. Both runs missed the nominal 60-second commentary cadence.

[AGENTS.tuned-v1.md](AGENTS.tuned-v1.md) makes the wrapper-yield syntax explicit, avoids a preliminary short process poll, and budgets waits against the time since the last update. The supplied cache-TTL paragraph remains unchanged. The candidate must be evaluated in fresh trials; the original metrics do not validate it.

The methodological reviewer also suggested changing global response-ID deduplication to a composite key. The parent retained globally unique upstream response IDs to avoid counting replayed parent history as child inference; cross-source duplicate counts are checked for equality, and per-session totals are reconciled. No response-ID collision between independent completions has been observed.

Review-agent usage is separate from the controlled trial measurements. These reviews are advice supported by trace inspection, not additional benchmark samples.

## Follow-up reviews

The trace reviewer confirmed that parent subagent silence came from waits that did not budget time since commentary: Astra used 60-second waits after roughly 6 seconds of other work; Sol selected 25-minute or 60-minute timeouts that returned only when the child finished. Completion awareness does not itself schedule parent commentary.

The shared monitoring skill was discovered in primary CI traces. Its interval guidance is a plausible contributor to long detection delays, but these trials do not isolate that cause. The clean phase removes its instruction catalog.

The [v2 candidate](AGENTS.tuned-v2.md) adds an explicit 30,000ms initial terminal wait when waiting is the only task and explicitly bounds native agent waits by the remaining update budget. It removes the untested 25-minute checkpoint. The reviewer found the four rules coherent, with remaining risks in model compliance and CI backoff choices. V1 remains an untested intermediate draft.

The accounting follow-up confirmed that a missing cache-write field makes API-dollar totals conditional valuations. If some input classified as ordinary is actually written to cache under API semantics, its listed price would be 25% higher. API cache-retention documentation does not establish the same behavior for Codex subscriptions. Neither a 25-minute checkpoint nor any cache-only wake-up savings was measured.

## Final primary accounting audit and v3 review

The independent accounting review reconciled all 30 primary trials and confirmed the exact total $6.0173308. It emphasized that the predeclared target concerns parent responses, while headline cost/count totals include children. Only Astra terminal and Sol subagent met that parent-response threshold. The initial patch exceeded the 60-second parent cadence in five of six workload cells; baselines also frequently exceeded it.

The v3 review agreed that placing an update before an already-needed wait adds message tokens without inherently adding a new model response. It identified 50s as insufficient margin for the observed 11.336s turnaround and noted ambiguous inherited elapsed-budget wording. Before v3 live execution, the parent selected 45s (15s margin) and removed that wrapper-budget ambiguity. This remains a heuristic, not a guaranteed latency bound.

## Final candidate trace review

The final prompt reviewer found no material conflict with native wait semantics or higher-priority cadence rules. V3 terminal traces had three commentary/wait-call pairs and four total responses, demonstrating that updates shared existing responses. Sol did not consistently include the explicit wrapper pragma, so observed success is not proof of literal compliance.

V3 CI scripts exposed a further issue: both lacked an explicit time/check-count bound, and Sol made 15 service checks. V4 changed only that clause. The two fresh v4 CI scripts had an 1800-second observation deadline (Astra) or 12-check limit (Sol), backed off unchanged status, and completed correctly with parent message gaps below 60 seconds. Actual service checks were five and six. These traces validate the successful-completion path, not all possible CI failure states.

The final independent audit recomputed all 61 workload totals and confirmed the v3/v4 comparison scope, watcher limits, update gaps, and synchronized export hashes. It found no material inconsistency in the report's token accounting, API-rate valuations, or recommendation.
