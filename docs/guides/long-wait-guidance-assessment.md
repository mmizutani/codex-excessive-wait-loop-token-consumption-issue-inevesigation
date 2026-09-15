# Why we did not adopt blanket 10–25-minute waits

## TL;DR

We investigated the community advice because its core mechanism is credible: longer, interruptible subagent waits can avoid model calls caused solely by short timeouts. We held off on recommending it company-wide because:

- An interruptible wait can still prevent the parent from producing its required progress updates. Calling it “non-blocking” in AGENTS.md does not resolve that instruction conflict.
- A configured **10-minute minimum overrides shorter requests**, including the final patch's 45-second budget. The proposed **25-minute default** can postpone the parent's next check that long if no event arrives.
- Supported configuration keys and one user's reported quota saving do not establish suitable default durations, general savings, or acceptable recovery time. The advice also leaves command, Code Mode, CI, and goal-continuation issues to be addressed separately.

The [final patch](AGENTS.waiting-compatible.md) preserves the effective update requirements and has a direct comparison against no patch. **We have not compared it against either exact Reddit proposal.** Our decision reflects compatibility and evidence requirements; it does not establish that long waits are always worse.

## What we assessed

The [Reddit post and comment](https://www.reddit.com/r/codex/comments/1wenst7/comment/p9ih1ka/) propose two changes:

1. Add an AGENTS.md rule requiring every `wait_agent` call to use at least ten minutes, with five minutes offered as an alternative. The rule calls the wait non-blocking and therefore compatible with developer instructions. The author reports approximately 30% lower quota consumption.
2. Enable Multi-Agent V2 and its waiting tool, and configure a ten-minute minimum, 25-minute default, and one-hour maximum.

This assessment uses **Codex CLI 0.154.0**, its pinned `rust-v0.154.0` source, and the repository's captured runtime and model trials. The Reddit text was retrieved for this review. Source behavior and recorded measurements are distinguished below from expected consequences and untested claims.

## What the advice gets right

The examined V2 `wait_agent` suspends the parent's next model step until input-queue activity or a timeout. Mailbox updates and input **steered into the active turn** can end it early. Increasing its timeout does not require waiting the full duration after a delivered completion notification. It also does not extend or terminate the child job itself. See the [release handler](https://github.com/openai/codex/blob/rust-v0.154.0/codex-rs/core/src/tools/handlers/multi_agents_v2/wait.rs#L53-L63) and [tool description](https://github.com/openai/codex/blob/rust-v0.154.0/codex-rs/core/src/tools/handlers/multi_agents_spec.rs#L280-L287).

Longer timeouts can therefore reduce repeated parent inference during quiet periods. Time spent suspended inside the tool does not itself cause a model request each minute. Usage arises when control returns to the model and it produces another response. Necessary worker inference, messages, and verification still consume tokens.

Our [installed-runtime probes](../waiting-validation/runtime-results.json) support the mechanism: a five-minute wait returned about one second after starting when the driver delivered steering. Another probe showed that an explicit ten-second request still returned after about ten seconds even when the configured default was five minutes. Raising only the default cannot change explicitly requested short waits. These probes used scripted model replies; they establish runtime behavior, not token savings.

## Why “non-blocking” does not settle the prompt conflict

**The proposed AGENTS.md rule can conflict with Codex's built-in system-prompt instructions.** In the examined Codex CLI 0.154.0 environment, those built-in instructions require the agent to provide progress commentary at least every 60 seconds during ongoing work and to avoid blocking sleep or wait calls longer than 60 seconds. The commentary requirement explicitly says the user:

> should not be left without a commentary update for more than 60 seconds

These built-in instructions are stored in the [release model catalog](https://github.com/openai/codex/blob/rust-v0.154.0/codex-rs/models-manager/models.json). At the API message level, Codex supplies them with the [developer role](https://github.com/openai/codex/blob/rust-v0.154.0/codex-rs/core/src/context/base_instructions.rs#L12-L14), so they take priority over the user's AGENTS.md instructions.

The proposed AGENTS.md rule requires every `wait_agent` call to use a timeout of at least ten minutes. **If no event arrives within 60 seconds, that wait prevents the parent from producing the progress update required by Codex's built-in prompt.** Calling the wait “non-blocking” or declaring it compatible in AGENTS.md cannot override that higher-priority requirement. This conflict was one reason we did not adopt the rule as company-wide guidance.

Two different properties matter:

| Property | What an interruptible wait provides |
| --- | --- |
| Responding to delivered input | The runtime can return early when a mailbox update or steered input arrives. |
| Producing an update without incoming activity | The pending wait does not itself generate parent commentary. The parent needs control back to write it. |

For example, if the parent reports progress and starts a ten-minute wait, a message arriving after 20 seconds can wake it promptly. If nothing arrives for two minutes, the parent has already missed the 60-second commentary requirement. This is a consequence of the waiting mechanism, not a claim that every ten-minute wait will take ten minutes.

The tool description specifically refers to steered input. It does not establish that every frontend immediately delivers every submitted or queued user message that way. Likewise, a mailbox wakeup can be a progress message; it does not necessarily mean all children have finished.

The effective instructions may also prefer waits measured in minutes. The final patch treats waiting preferences as subject to required updates and actionable deadlines. The [Japanese explanation](AGENTS.waiting-explanation.ja.md#1-across-all-waitsすべての待機に共通する指示) explains why the patch leaves a 45-second waiting budget when a 60-second cadence applies.

## What the proposed configuration actually changes

The supplied configuration is reproduced here for assessment, **not as installation guidance**:

```toml
[features.multi_agent_v2]
enabled = true
wait_agent_enabled = true
min_wait_timeout_ms = 600000
default_wait_timeout_ms = 1500000
max_wait_timeout_ms = 3600000
```

All five keys exist in the [0.154.0 configuration schema](https://github.com/openai/codex/blob/rust-v0.154.0/codex-rs/core/config.schema.json) and [feature configuration type](https://github.com/openai/codex/blob/rust-v0.154.0/codex-rs/features/src/feature_configs.rs#L249-L290). The supplied durations fit their allowed range. Schema support establishes valid configuration, not the effectiveness of these chosen values.

`enabled` enables the V2 feature; `wait_agent_enabled` controls exposure of its waiting tool when V2 collaboration is available. The latter already defaults to true in the examined V2 configuration. Our measured environment exposed direct V2 waiting. Enabling a missing tool and choosing its timeouts are separate decisions. See [configuration defaults](https://github.com/openai/codex/blob/rust-v0.154.0/codex-rs/core/src/config/mod.rs#L1295-L1310) and [tool registration](https://github.com/openai/codex/blob/rust-v0.154.0/codex-rs/core/src/tools/spec_plan.rs#L1284-L1336).

| Setting | Runtime default in 0.154.0 | Proposed value | Effect |
| --- | ---: | ---: | --- |
| `min_wait_timeout_ms` | 10,000 ms / 10 s | 600,000 ms / 10 min | Raises an explicit shorter request to ten minutes. Early event delivery still returns sooner. |
| `default_wait_timeout_ms` | 30,000 ms / 30 s | 1,500,000 ms / 25 min | Used when `timeout_ms` is omitted. It does not replace an explicit value within the allowed range. |
| `max_wait_timeout_ms` | 3,600,000 ms / 60 min | 3,600,000 ms / 60 min | Unchanged maximum. Requests above it are rejected; it does not make every call wait an hour. |

The defaults come from the [release constants](https://github.com/openai/codex/blob/rust-v0.154.0/codex-rs/core/src/config/mod.rs#L235-L243). Applying the handler's rules to the proposed configuration gives these **source-derived examples**, not new runtime measurements:

| Model request | Effective observation timeout if no event arrives |
| --- | --- |
| `timeout_ms: 45000` | 600,000 ms: the minimum raises 45 seconds to ten minutes. |
| `timeout_ms: 300000` | 600,000 ms: a requested five minutes also becomes ten. |
| No `timeout_ms` argument | 1,500,000 ms: the default is 25 minutes. |

Consequently, **this ten-minute minimum cannot preserve the final patch's shorter wait budget**. A prompt cannot undo the runtime clamp. The minimum is also not a ten-minute recovery guarantee: an omitted timeout can leave a quiet, stuck worker unexamined by the parent for 25 minutes. Delivered failure notifications can wake the parent sooner; a silent hang with no delivered event is the concern. What counts as acceptable recovery time depends on the task and deadlines, and was not established by the comment.

## Why the available savings evidence was insufficient for blanket adoption

We did test a related five-minute instruction in the [initial live comparison](../waiting-validation/live-prompt-results.json). In its single Astra pair, responses fell from three to two. However, both Astra and Sol treatment runs waited through the 75-second observation without an intermediate update. Sol's response count did not improve. These tests used simulated pending-child state and a driver-delivered result, with no actual child agent; they were neither replicated nor a test of the exact ten-minute prompt or proposed configuration. The [independent validation report](../reports/CODEX_ASTRA_SOL_WAITING_INDEPENDENT_VALIDATION.md#measured-effect-of-the-earlier-instruction) records their scope.

The Reddit author's 30% quota reduction remains an individual report. It supplies a useful hypothesis but does not isolate runtime version, workload, instruction stack, cache state, or the account's quota calculation. Our API-price equivalents value recorded token categories; they cannot independently verify that subscription quota claim.

Subagent timeouts also address only one source of overhead. They do not adjust `exec_command` or `write_stdin`, coordinate outer `functions.exec` waits, consolidate CI queries into a watcher, or pause an active `/goal`. A blanket duration could reduce one set of calls while leaving the other mechanisms unchanged.

The thread also mentions choosing 25 minutes to stay within an assumed 30-minute prompt-cache lifetime. Even accepting that assumption does not prove a saving: a `wait_agent` return concerns the waiting parent, does not necessarily refresh a quiet child's context, and is not a guaranteed cache-refresh schedule for every relevant prefix. The repository has not independently established a fixed subscription cache TTL or measured these boundaries. Our patch therefore avoids cache-only keepalives without measured net savings. See the [cache discussion](AGENTS.waiting-explanation.ja.md#キャッシュ維持だけのアクセスは節約効果を測るまで追加しない).

## What we recommend, and what would justify reconsideration

Use the [verified patch](AGENTS.waiting-compatible.md) or [skill alternative](../../skills/codex-wait-efficiently/README.md): prefer suitable interruptible waits, keep useful independent work first, and choose durations within the effective update and deadline budget. Keep the runtime minimum low enough to permit those durations. The proposed ten-minute minimum should not be combined with this patch's 45-second budget.

The [direct final-patch comparison](../reports/CODEX_WAITING_LATEST_VS_NO_PATCH_BENCHMARK.md) measured 18 Astra trials, including real subagents: model responses fell 98→47, inclusive input fell 51.03%, and API valuation fell 42.31%. All nine patched parent sessions met the measured 60-second progress cadence. This establishes an observed benefit against no patch for those workloads; it does not rank the patch against the two community proposals.

Longer waits remain a reasonable candidate where the effective instructions allow a longer reporting interval and delivered events provide suitable responsiveness. Before recommending them company-wide, a representative comparison should check completed work, parent and child token categories, result delay, silent-worker recovery, actual input delivery, and cache behavior across long waits. The key unanswered question is the net benefit under that operating policy, including its responsiveness requirements.
