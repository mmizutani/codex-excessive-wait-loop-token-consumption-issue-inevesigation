# Codex Astra/Sol excessive usage during task waiting

## Investigation handoff: evidence, mechanisms, fix status, and verification plan

**Prepared:** September 14, 2026.  
**Audience:** An engineer or coding agent investigating this independently, without access to the preceding conversation.  
**Primary scope:** `gpt-6-astra` and `gpt-5.6-sol` in Codex, especially parent-agent supervision of subagents, background commands, and external jobs.  
**Release baseline:** Codex CLI `0.154.0`, tag `rust-v0.154.0`; selected later development snapshots are identified below. This is a historical, version-qualified baseline, **not a claim that 0.154.0 remains the latest release when this document is read**.  
**Evidence limits:** Source inspection and public reports; no controlled live-model experiment, company usage-log analysis, or billing-ledger audit has been completed for this investigation.

This document records the problem and how to verify it. It contains no proposed AGENTS.md instructions or Agent Skill prompts. Public prompt text is discussed only as evidence about the suspected mechanism. Operational settings and control commands appear only where needed to describe the environment or reproduce behavior.

---

## 1. Executive assessment

The central hypothesis is that **Codex sometimes repeatedly returns control to the parent model while the only useful next action is to wait**. The model then decides to check or wait again. Repeated inference requests can process nearly unchanged context and produce little more than status commentary or another waiting-tool call. This resembles busy waiting at the orchestration level; it is not necessarily a CPU spin loop or continuous token generation throughout a genuinely suspended tool call. A concrete public report documents multiple parent resumptions around one logical subagent wait. [S01]

There is no single established “Astra token-drain bug.” At least three mechanisms must be separated: short model-selected or default observation timeouts; outer tool wrappers that yield before an inner operation finishes; and active `/goal` continuation that can start another turn after the model ends its reply. Background-command notification delivery and contradictory waiting instructions are related but distinct concerns. [S01] [S02] [S03] [S04]

**Several relevant capabilities already existed in the inspected stable release.** Native sleep can be directly exposed outside code mode, v2 collaboration tools have a direct execution path, and genuine blocked/usage-limited goal states stop automatic continuation. Their presence does not prove that a model selects them appropriately, that every frontend delivers input identically, or that all external events wake an idle session. [S05] [S06] [S07] [S08]

The user's company reported an abrupt usage increase after adopting Astra in early September 2026. That is the incident motivating this investigation, **not an independently measured causal finding**. No raw company traces, precise rollout timestamp, denominator of completed work, billing mode, or quantified before/after series were supplied. The proportion attributable to wasteful watching remains unknown.

The investigation should determine **which paths are affected, on which builds and effective settings, and how much excess usage they actually explain**. Do not assume the model change, the 60-second instruction, a cached-token total, or a social-media improvement percentage establishes the entire cause.

## 2. Evidence status and scope

Use these distinctions when carrying findings forward:

| Label | Meaning |
|---|---|
| **Source-established** | A specific inspected source snapshot contains the stated code, setting, or instruction. This does not by itself establish live model behavior. |
| **Reported** | A user or issue author describes observed behavior. The report may be precise but was not independently reproduced here. |
| **Hypothesis** | A plausible causal explanation requiring an experiment or trace analysis. |
| **Not established** | Available evidence does not support a definite conclusion, particularly about rollout completeness, automatic wakeups, or financial impact. |

### Environment premise from the company rollout

The intended rollout assumes `features.sleep_tool.mode = "always_on"` has already been configured. Treat this as an investigator input, then inspect the **effective** feature state and exposed tools on the affected client. In the inspected tool-selection implementation, `always_on` removes the model-specific selection condition, while registration still depends on the sleep feature being enabled. It does not force a model to call sleep or choose a useful duration. [S09] [S10]

This investigation focuses on Astra and Sol. It does not prescribe different mitigation instructions for other models.

### Version and provenance anchors

The prior release audit recorded the following on September 13, 2026:

| Item | Recorded value |
|---|---|
| Stable CLI baseline | `0.154.0` |
| Release publication | September 9, 2026, 22:35:38 UTC / September 10, 07:35:38 JST |
| Annotated tag object | `36eab01061df3cde5f95ec20a526777b430091ba` |
| Release commit | `6b9826e3aa83b1a5947db50f4332cb9c65f1b340` |
| Earlier inspected development snapshot | `a592c38c16cdd7623dacc9168926ebccedfb67d3` |
| Later inspected development snapshot for v2 waiting | `1715e55076737158ba61d43158ede504de6d4ce1` |
| v2 wait-handler blob at release and latter snapshot | `d2f92feb8d011bb468dcc1f81b0efc20e756179e` |
| Native sleep-handler blob at release | `7defc8314bd2ddde3cf683601ec02a57588cb4f1` |

Release/tag metadata and pinned source links are provided in the source register. The two development hashes are separate snapshots; do not describe either as current `main`. A later release or cherry-pick must be checked independently. [S11] [S12] [S13] [S14]

For this September 14 handoff, selected baseline files were re-read: the v2 wait handler, native sleep handler, v2 timeout constants, and Astra's instruction template. Issues #28144 and #35108 were also retrieved and remained open. Release membership, other PR metadata, and Sol's model definition are carried forward from the earlier source review, not presented as a new exhaustive release audit. [S01] [S02] [S03] [S04] [S05] [S15]

## 3. Mechanism overview

### 3.1 Model-driven observation loop

```text
Parent model           Waiting tool / runtime          Actual worker
     |                           |                          |
     +--- check or short wait -->|                          | working
     |<------ still running -----|                          |
     |                                                      |
     +--- another inference                                 |
     +--- check or short wait -->|                          | still working
     |<------ still running -----|                          |
     +--- another inference ...                             |
```

The expensive repetition is crossing back into model inference without useful new evidence. Timer checks implemented entirely inside ordinary runtime code are not equivalent to repeated model invocations.

### 3.2 Direct, interruptible runtime waiting

```text
Parent model            Runtime wait                   Worker / user
     |                        |                              |
     +--- wait -------------->|                              |
     |                   [suspended]                         |
     |              no repeated parent inference             |
     |                        |<--- delivered activity -------+
     |<------ wait returns ---|
     +--- process the new information
```

The inspected v2 handler waits on input-queue activity or a timeout. A configured maximum wait is not a compulsory delay: eligible activity can return control sooner. However, a new message is not necessarily proof of worker completion, and local support for steering does not prove end-to-end delivery from every frontend. [S03]

### 3.3 Separate goal-continuation loop

```text
Parent ends a reply while waiting
              |
              v
       Goal remains active
              |
              v
   Runtime starts another turn
              |
              v
   Parent checks the same state ...
```

A final assistant reply and a goal-state transition are different events. The active goal can outlive the reply. [S02] [S08]

## 4. Candidate causes and what the evidence supports

### A. Short default or explicitly selected subagent waits

**Source-established.** In the baseline v2 configuration, the minimum is `10000` ms, default is `30000` ms, and maximum is `3600000` ms. The handler uses the default when the argument is omitted, clamps a requested value below the minimum, and rejects a request above the configured maximum. These are configuration values in the inspected release, not a universal promise for every deployment. [S03] [S15]

**Hypothesis.** A model that repeatedly omits the timeout or selects a short timeout can cause unnecessary parent inference while a healthy child is still working. Raising a default alone will not change explicit short values emitted by the model.

**Critical distinction:** an observation timeout says that a wait returned without the expected activity. It does not establish a task execution timeout, worker failure, or a reason to restart the worker. The inspected wait handler does not terminate a worker merely because its own observation deadline expires. [S03]

**Verification target:** correlate the requested and effective timeout, actual wait duration, return reason, and subsequent model request. If the model requests a long wait but resumes early, determine whether a genuine message arrived, a wrapper yielded, or a separate timer or control path fired.

### B. The 60-second responsiveness instruction

**Source-established at the reviewed baseline.** The bundled Astra and Sol instruction templates contain guidance discouraging blocking sleep or wait calls above 60 seconds because they may prevent communication with the user. The key excerpt is:

> “Avoid performing blocking sleep or wait calls longer than 60 seconds”

This is evidence from the public model catalog, not a proposed instruction in this document. Earlier review found it in both models; the Astra template was re-read for this handoff. [S04]

**Hypothesis.** The model may apply that responsiveness rule to interruptible subagent waits, choosing frequent timeouts even though the runtime can return early on activity. The bundled v2 role guidance also recommends waits measured in minutes, so investigators must inspect how these potentially conflicting instructions are assembled and interpreted. [S07]

Do not describe this as a verified hard 60-second subagent lifetime. Do not assume every user's effective prompt exactly equals the bundled template. The role resolver can use model-catalog or configured text, so runtime configuration and remotely supplied metadata matter. [S07]

**Verification target:** identify which instructions actually reached the model in the affected session, and whether short timeouts reflect model choice or enforced runtime behavior. A public template establishes a candidate influence, not causality or universal deployment.

### C. Nested code-mode waits and outer-wrapper yields

**Reported with a concrete trace.** Issue #35108 describes a Windows Codex Desktop session, package `26.721.3404.0`, using a v1 subagent wait inside `functions.exec`. The requested inner wait was `60000` ms; the outer call yielded after roughly 11 seconds, the parent called a separate wrapper wait, and a subsequent timeout led to another parent continuation. The report records two successive inference usage events of approximately 164,000 input tokens each, mostly cached. These are reporter-provided measurements, not this investigation's benchmark. [S01]

```text
Inner subagent wait is still pending
           |
Outer execution wrapper yields a cell/session handle
           |
Parent model decides to wait for that wrapper
           |
Wrapper wait expires or yields
           |
Parent model runs again ...
```

**What is already different in the baseline:** v2 collaboration can be exposed directly outside code mode. Therefore, an old v1 nested-wrapper report must not be generalized to every Astra/Sol v2 session. At the same time, other long-running tools or wrappers may still create similar boundaries. [S06] [S09]

**Verification target:** record the actual outer and inner tool names, argument values, cell/session IDs, and model requests. Increasing only the inner timeout cannot prove that the outer polling boundary disappeared.

### D. Background-command completion does not necessarily wake the model

**Source-established difference, bounded conclusion.** The supplied fork commit `tekacs/codex@9ffcf8d` explicitly adds model-visible completion input for unified-exec processes that yielded as background work. It routes that input through `inject_or_start`, handles active and idle sessions, and attempts to suppress duplicate delivery when the original command returned its terminal result inline. [S16]

The previously inspected upstream exit watcher emitted completion events and metrics without that same explicit model-input injection. Equivalent end-to-end behavior through another path was **not established**. The fork is evidence of a proposed implementation, not proof that upstream lacks every possible wake route or that the fork is production-correct. [S17]

```text
Process exits
    |
    +--> UI / analytics completion event
    |
    +--> Model-visible input + active/idle delivery + resumption
         This second path must be verified separately.
```

This explains why a shell `sleep`, or an external watcher script, does not automatically eliminate model-driven checking: the model can still supervise that process repeatedly. It also explains why simply ending the parent turn may strand the workflow when no verified wake route exists.

**Verification target:** test completion during an active parent turn and while the parent is idle, including races around the initial tool return, duplicate suppression, cancellation, and resumed sessions.

### E. `/goal` auto-continuation without durable event waiting

**Source-established plus open feature request.** Active goals can continue when a thread becomes idle. The inspected runtime also recognizes paused, blocked, usage-limited, budget-limited, and complete states. A healthy external job that has not finished is not automatically equivalent to a genuine blocker. [S08]

Issue #28144 asks for a persisted waiting state with wake metadata and event/time-driven resumption. It remained open when rechecked. The prior audit did not establish that its requested durable scheduling semantics had shipped. Issue state alone is not sufficient proof of absence; source and release checks are still required. [S02]

A native sleep suspends an in-flight operation. It is not, by itself, a persisted goal scheduler that survives restart and wakes on the correct external dependency. Similarly, a reply announcing that the agent is waiting is not a state transition to paused. [S02] [S05] [S08]

**Verification target:** distinguish a tool continuation inside one turn from a new goal-generated turn. Observe actual goal-state transitions; separately inspect whether outstanding workers or commands remain alive after the goal stops continuing.

### F. Native sleep exposure and numeric argument mismatch

**Source-established.** Native `clock.sleep` is registered as `DirectModelOnly` in the baseline. It waits inside the runtime and can return early on input activity. The `always_on` feature mode makes its selection independent of the model's advertised clock capability, provided the feature is enabled. [S05] [S09] [S10]

The sleep argument is advertised using `JsonSchema::number`, but `SleepArgs.duration_ms` is parsed as `u64`. This is a schema/parser mismatch worth testing with integer, integer-valued floating-point, and fractional JSON representations. The source difference is established; the exact acceptance/rejection behavior and prevalence in real model calls need a focused test. [S05]

**Hypothesis.** Repeated invalid arguments could create additional model/tool-error turns or encourage substitution of an inferior waiting mechanism. Do not confuse this with the short-wait loop or claim it explains the whole usage spike.

The existing `always_on` setting does not repair numeric parsing, select the duration, guarantee actual tool use, or add durable goal wakeup.

### G. Intermediate notifications, duplicated work, and inherited instructions

**Source-established foundation; amplification is a hypothesis.** The v2 wait can return on any eligible mailbox activity and on already-pending activity, not only final completion. Therefore, a long timeout does not prevent frequent wakeups when workers send frequent progress messages. Whether any such wakeup is unnecessary depends on its content and the work it enables. [S03]

Potential secondary amplifiers include repeated status narration, re-fetching unchanged logs, redundant parent investigation, watcher-only subagents, and restarting healthy tasks after observation timeouts. These were concerns raised during the discussion, not separately reproduced defects.

A supplied public update also reported that some older skills were over-triggering or discouraging verification. The full thread could not be retrieved, and that announcement could not be mapped to a particular CLI release or to the waiting fixes. Preserve this as a lead, not proof of universal resolution. [S23]

**Verification target:** determine whether a parent resume was caused by a timeout, useful message, redundant notification, or explicit custom instruction. Never count all delegation or all notifications as waste.

## 5. Astra and Sol: shared mechanisms, different effective environments

The reviewed bundled definitions select v2 collaboration and code-mode-only general tool exposure for both Astra and Sol. Astra advertises `clock` among its experimental tools; Sol's reviewed entry does not. Native v2 collaboration and native sleep can nevertheless remain direct exceptions to general code-mode exposure. [S04] [S09]

With the assumed `always_on` setting, model-specific clock advertising should not be the default explanation for a missing sleep tool. Inspect resolved feature policy and registration first. Do not infer identical observed behavior simply because both models use the same handler: tool selection, effective instructions, reasoning settings, model changes, and frontend delivery remain separate variables. [S09] [S10]

The analysis must distinguish:

```text
model behavior        chooses how to supervise work
model instructions    influence duration, delegation, and commentary
runtime implementation implements waiting, wakeup, and continuation
client/frontend       routes input and may bundle a different runtime
accounting            measures tokens, allowances, credits, and money
```

Switching models changes one or more of these variables but does not itself establish that a runtime defect was fixed. Likewise, the same named reasoning level should be treated as an experimental setting, not an assumption of identical compute or cost across models. Consult current official usage guidance and the actual account agreement rather than importing a fixed quota conversion. [S24]

## 6. Release-qualified fix status

**“Present by 0.154.0” means verified in the recorded stable baseline. It does not identify the first containing stable release or confirm all desktop/server deployments.** The next investigator must refresh this matrix.

| Change or gap | Recorded status | Scope and remaining question |
|---|---|---|
| PR #34969: keep sleep outside code mode; merged July 23, 2026 | Present by 0.154.0 | Direct native sleep avoids that wrapper path. It does not fix arbitrary nested tools or shell sleeps. [S05] [S18] |
| PR #41243: configurable sleep gating; merged August 28, 2026 | Present by 0.154.0 | Adds `model_driven` / `always_on` selection. Availability is not correct invocation. [S10] |
| PR #25266: v2 direct-tool defaults; merged June 1, 2026 | Present by 0.154.0 | Separates v2 collaboration from nested code-mode exposure. Does not establish that every session uses that effective configuration. [S06] [S09] |
| PR #35594: longer-wait guidance; PR #37189: usage-hint tracking | Related changes found in earlier review | Guidance was present in baseline role text; do not equate a guidance change with a changed numeric default. Exact first-release attribution remains to verify. [S07] [S19] |
| PR #23094: goal blocked/usage-limit stopping; merged May 18, 2026 | Present by 0.154.0 | Stops continuation for the relevant states. It is not general event-driven waiting. [S08] [S20] |
| v2 default observation wait | Still 30 seconds in baseline | Long maximum support does not change omitted arguments or explicit 60-second choices. [S15] |
| 60-second blocking-wait instruction | Present in reviewed Astra and Sol templates | Effective delivery, interpretation, and any later prompt rollout need verification. [S04] |
| Legacy/nested wait problem, #35108 | Open on September 14 recheck | Report concerns a specific v1/wrapper environment; actual current path must be reproduced. [S01] |
| Durable goal waiting, #28144 | Open on September 14 recheck; implementation not established by prior audit | Inspect newer state, persistence, and wake code rather than relying only on issue status. [S02] |
| Generic background-exec model wakeup equivalent to fork `9ffcf8d` | Not established upstream by prior audit | Verify semantic equivalence, not just commit title or presence of an exit event. [S16] [S17] |
| Sleep numeric schema/parser mismatch | Present in re-read baseline source | Test serialization/error behavior and trace frequency separately. [S05] |
| Server-side efficiency or older-skill updates | Not release-mapped in this investigation | Public announcements may describe narrower or backend-only changes. [S23] |

Issue #36379 must not be counted as a shipped default-timeout fix merely because it is closed. The previously retrieved author comment says it was filed against the wrong repository and belonged downstream. [S21]

The earlier audit did not establish an additional main-only fix resolving the durable-goal or generic background-exec-wakeup gaps. That is a bounded historical conclusion, not a claim to have audited every later commit, prerelease, or equivalent implementation.

## 7. Public reports and their evidentiary weight

### Original discovery and usage-drain discussion

The first Reddit thread, the Relux article, and Ivan Oparin's X thread were supplied as starting points. The supplied Ivan excerpt described encountering a float-to-integer tool-call problem while using an alternative model with Codex. This is relevant to investigating argument parsing, but the full diagnostic chain was not independently reconstructed. Direct retrieval of these pages failed during preparation; preserve the URLs and retrieve them independently. [S25] [S26] [S27]

### Claimed improvement from longer subagent waits

The user supplied the text of a later Reddit post. Its author attributed short waits to the 60-second instruction, reported using longer subagent-wait timeouts, and claimed approximately **30% lower quota consumption** with more waits returning on messages instead of timeout. The full post could not be fetched here. [S28]

The mechanism is compatible with the source-established early-return behavior. The percentage remains an uncontrolled individual report: no matched task sample, complete traces, rate-card attribution, or account-state controls were supplied. This document intentionally does not reproduce the author's workaround prompt.

### “60-second subagent limit” claim

The supplied Japanese X excerpt described a 60-second subagent-related instruction and reduced usage after disabling it. The exact customization, effective prompt, client version, and controlled measurements were not supplied. Subsequent source review identified a blocking-wait recommendation, not a universal worker execution lifetime. That distinction must survive any retelling. [S29] [S04]

### Technical issue report versus accounting proof

Issue #35108 offers useful tool-boundary and input-token evidence. It does not prove a proportional increase in a bill or subscription allowance. The author explicitly distinguishes raw totals dominated by cached input from billing interpretation. Its linked adjacent issues are useful leads, but their statuses and fixes were not separately audited here. [S01]

## 8. Independent investigation procedure

### 8.1 Identify the actual environment before attributing symptoms

Record the client surface and build, actual executing runtime path/version, OS, repository/workload revision, authentication/billing mode, model identifier, reasoning and speed settings, parent/child model choices, and goal state. Record whether the session was new, resumed, or compacted.

Capture the resolved sleep feature, actual wait-tool schemas, default/minimum/maximum timeouts, effective collaboration path, and relevant instruction provenance. Hash local instruction/config files where useful; do not publish secrets or private content. A shell's `codex --version` alone is not evidence of a desktop app's embedded runtime version.

Keep the company rollout premise separate from observation: configured `always_on` is not sufficient evidence that a particular session exposed native sleep.

### 8.2 Refresh release evidence, not just search results

Retrieve the latest stable and relevant prerelease metadata, resolve the release tag to its commit, and inspect the relevant files at immutable commits. For each candidate fix, check merge state, merge commit, release inclusion, effective enablement, and a behavior-level regression test. A closed issue, merged PR, or new prerelease is insufficient on its own.

The following are optional read-only source-inspection commands for a separate local clone. They require Git, GitHub CLI authentication for `gh api`, and `jq`. They do not execute models, modify the upstream repository, or change a user's Codex settings.

```sh
# Work in a new directory rather than an existing development checkout.
audit_dir="$(mktemp -d -t codex-wait-audit.XXXXXX)"
git clone --filter=blob:none --no-checkout \
  https://github.com/openai/codex.git "$audit_dir/codex"
cd "$audit_dir/codex"

gh api repos/openai/codex/releases/latest \
  --jq '{tag_name, published_at, prerelease, html_url}'

baseline="$(git rev-parse 'rust-v0.154.0^{commit}')"
printf 'Baseline commit: %s\n' "$baseline"

git show "$baseline:codex-rs/core/src/tools/handlers/multi_agents_v2/wait.rs"
git show "$baseline:codex-rs/core/src/tools/handlers/sleep.rs"
git show "$baseline:codex-rs/core/src/config/mod.rs" |
  grep 'DEFAULT_MULTI_AGENT_V2_.*WAIT_TIMEOUT_MS'

# Inspect the model metadata and only the relevant public instruction lines.
git show "$baseline:codex-rs/models-manager/models.json" |
  jq '.models[] | select(.slug == "gpt-6-astra" or .slug == "gpt-5.6-sol") |
      {slug, tool_mode, multi_agent_version, experimental_supported_tools}'

git show "$baseline:codex-rs/models-manager/models.json" |
  jq -r '.models[] | select(.slug == "gpt-6-astra" or .slug == "gpt-5.6-sol") |
      .slug as $model | (.model_messages.instructions_template // "") |
      split("\n")[] | select(test("60 seconds|blocking sleep")) |
      "\($model): \(.)"'

for pr in 34969 41243 25266 23094; do
  gh api "repos/openai/codex/pulls/$pr" \
    --jq '{number, title, merged, merged_at, merge_commit_sha, html_url}'
done
```

For each verified merge SHA, test ancestry against the release commit. If ancestry fails, investigate backports or equivalent cherry-picks before declaring the behavior absent. If it succeeds, still check configuration gates and subsequent reverts. Code movement or renamed symbols requires tracing behavior, not treating a missing filename as proof of removal.

### 8.3 Separate runtime tests from model-behavior tests

**Runtime tests:** Use the repository's existing mocked-response test infrastructure or an equivalent instrumented harness that exercises the actual handler. Supply deterministic wait calls and deliver controlled mailbox/steering events. Measure actual parent inference requests. A mock whose own implementation defines efficient waiting cannot validate Codex.

**Model-behavior tests:** Let Astra and Sol select their actions on matched, bounded tasks. Observe requested timeouts, routing, commentary, and completion handling. Passing a handler test does not show that a model will select that handler or comply with its intended usage.

Start with synthetic, disposable workloads. Set external run limits before testing active goals or long waits so reproducing the incident does not itself cause unbounded usage.

### 8.4 Minimal experiment matrix

The durations below are test variables, not recommended user prompts or optimal production defaults.

| Test | Controlled setup | Observation that matters |
|---|---|---|
| T1: timeout selection | Identical subagent workload under Astra and Sol; goal disabled | Omitted versus explicit timeout values; direct versus nested calls; no-progress parent resumptions |
| T2: timeout-only waiting | Actual v2 handler, no delivered events; compare omitted, 60-second, 300-second, and 600-second requests within allowed limits | Effective duration and number of inference resumptions; distinguish default selection from runtime capping |
| T3: early child event | Longer requested timeout; deliver a child message or final-status notification at a known earlier time | Return occurs after delivery rather than at the timeout; correctly distinguish message from completion |
| T4: user input delivery | During a wait, separately send active-turn steering, next-turn queued input, and cancellation | End-to-end delivery/resume latency for each supported frontend path; do not assume identical semantics |
| T5: wrapper boundary | Same controlled long-running operation through direct and relevant nested paths | Outer versus inner yield times and actual model request count |
| T6: shell completion | Command outlives its initial tool call; test active and idle parent sessions | Exactly what event is emitted, whether model input is delivered, whether idle inference resumes, and whether delivery duplicates |
| T7: goal lifecycle | Finite objective waiting on a controlled external event; compare active, paused, and resumed state | New goal-generated turns versus tool continuations; real state and worker/process state after pausing |
| T8: schema mismatch | Exercise actual sleep argument parsing with integer, integer-valued floating-point, and fractional JSON values | Acceptance/rejection, error type, repeated invalid arguments, and any model fallback behavior |
| T9: notification churn | Hold useful work fixed; vary intermediate worker messages and already-pending input | Useful versus redundant wakeups; processing of delivered input before another wait |
| T10: completion correctness | Several children, staggered completion, one observation timeout, one genuine failure | No premature global completion, duplicate restart, ignored error, or skipped required verification |

Repeat matched trials and report dispersion, not a single favorable run. Define actionable progress and classification rules before comparing results. Hold instruction/config changes, workload state, context size, cache warmness, client build, and concurrent account activity constant where feasible.

## 9. Measuring excess usage without confusing accounting layers

### 9.1 Reconstruct a timeline

For each parent and child, correlate model request/response IDs, root/parent/child thread IDs, turn IDs, tool-call IDs, process handles, and timestamps. Record requested/effective timeout, actual duration, return reason, goal transitions, and delivered input. Preserve the distinction between a wrapper yielding, a tool reporting an observation timeout, and the worker itself exiting.

A tool event is not necessarily one inference request. Conversely, a single user-visible turn can contain multiple model responses. Count actual requests/resumptions where instrumentation permits; do not estimate model calls from a status animation.

A suggested analysis record is:

```text
trial_id, client_build, runtime_commit, model, reasoning_setting,
root_thread_id, thread_id, parent_thread_id, turn_id, response_id,
tool_call_id, tool_name, outer_wrapper_id, process_or_agent_handle,
requested_timeout_ms, effective_timeout_ms, wait_elapsed_ms,
return_reason, delivered_event_id, goal_status_before, goal_status_after,
input_tokens, cached_input_tokens, output_tokens, reasoning_tokens,
usage_counter_semantics, progress_classification, verification_outcome
```

Unavailable fields should remain unknown, not be invented. Redact content while retaining enough correlation data to reconstruct causality.

### 9.2 Keep five measurements separate

| Measurement | Purpose | Common mistake |
|---|---|---|
| No-progress parent resumptions per minute of waiting | Direct evidence of busy observation | Counting useful child messages as waste |
| Parent and child token usage, separately and combined | Attribute supervisor overhead versus actual work | Calling a parent-only saving a whole-workflow saving |
| Cached versus uncached input and output | Understand repeated context processing | Adding cached tokens twice when they are already included in total input |
| Subscription allowance / credit changes | Measure the account's actual depletion | Assuming a raw token count maps directly to a quota percentage |
| Billed amount under the applicable contract | Quantify financial impact | Applying API prices to a different subscription or enterprise meter |

Verify each telemetry schema's counter semantics. Do not sum cumulative snapshots as though they were incremental usage. Reasoning tokens may be included within another output field; check before adding them. Account for resumes, compaction, retries, duplicated events, late child activity, and threads created before the observation window but still active during it.

An illustrative cost equation, **only when the applicable meter uses these categories**, is:

```text
U = total_input - cached_input        # only if total_input includes cached_input
C = cached_input
O = output                           # avoid double-counting included reasoning
metered_cost = (U * price_U + C * price_C + O * price_O) / 1_000_000
```

This is not a formula for subscription allowance. Use current official pricing/account guidance and the applicable agreement; this handoff intentionally carries no fixed price or quota multiplier. [S24]

### 9.3 Causal tests and disconfirming results

A strong result would show matched trials where suppressing timeout-only parent resumptions reduces attributed observation usage while preserving child work, event responsiveness, and verification quality.

Results that would weaken the main hypothesis include: few or no parent requests during the supposedly wasteful interval; most usage occurring in productive child work; unchanged wait behavior but different account depletion; or repeated wakeups explained by useful messages. A larger context, changed reasoning/speed setting, different workload mix, retries, compaction, or concurrent sessions may explain part of the incident without a waiting regression.

For a hypothetical 20-minute interval with no delivered activity, one-minute, five-minute, and ten-minute waiting intervals produce roughly 20, 4, and 2 timer intervals, ignoring model overhead. This arithmetic is about observation frequency, **not total-token savings or the Reddit author's reported 30%**.

## 10. Questions the next investigator should answer

1. Which exact affected builds and effective model instructions produce repeated short waits? Does the live model choose 60 seconds, omit the argument, or request a long interval that the runtime cuts short?
2. How often do the observed waits return for genuine input, timeout, wrapper yield, or another reason? Is the parent processing delivered input correctly?
3. Which fixes are in the installed stable/runtime build, which exist only on development branches, and which are backend or prompt rollouts that cannot be inferred from a CLI tag?
4. Does background-command completion reach the model during active and idle states, exactly once, under races and cancellation? Does a frontend queue input differently from active-turn steering?
5. How much does `/goal` contribute beyond within-turn tool continuation? What state persists across restart, and what actually happens to child work after a pause?
6. Are numeric argument errors or stale/custom instructions material contributors, or only occasional adjacent issues?
7. After separating workload, parent/child activity, cache effects, settings, and accounting rules, how much of the company's usage increase is attributable to unnecessary watching?

A useful follow-up deliverable is a version-pinned evidence table with reproducible traces, pass/fail results for the relevant tests, a current shipped/unreleased/unresolved matrix, and an explicit list of disproved hypotheses. Identify the first containing release only when ancestry or equivalent patch evidence supports it.

## 11. Boundaries of the present conclusion

This record supports investigating a family of **model-driven waiting and orchestration inefficiencies**. It does not establish that Astra alone introduced them, that every subagent has a 60-second execution limit, that waiting always costs tokens continuously, that all native waits are broken, or that one community intervention will produce a particular company saving.

The durable-goal request predates the reported company Astra rollout. Efficient direct-wait mechanisms coexist with remaining selection, routing, and scheduling concerns. Source support for early interruption must be distinguished from frontend delivery guarantees, and telemetry totals must be distinguished from charges. [S02] [S03] [S05] [S01]

No live Codex reproduction or company-level attribution has been completed for this handoff. The independent investigation should verify or reject the mechanisms above rather than treating them as a completed root-cause analysis.

---

## Source register

All technical baseline source links use an immutable commit where available. Public issue and announcement pages are mutable; record retrieval dates and relevant comments when rechecking them. The older source-review findings summarized here were obtained from the original repository during the preceding investigation, not solely inferred from public commentary.

### Primary code, release, and issue sources

| ID | Source and use |
|---|---|
| [S01] | Issue #35108: nested v1 wait/wrapper report, environment, parent-resumption evidence, and adjacent issue links. Rechecked September 14; open. |
| [S02] | Issue #28144: durable goal wait/wake request; opened June 14, 2026. Rechecked September 14; open. |
| [S03] | Baseline v2 `wait.rs`: timeout handling, mailbox/steering subscription, pending-input early return, and returned status. Re-read for this handoff. |
| [S04] | Baseline `models.json`: Astra/Sol model metadata and bundled instruction templates. Astra's relevant template was re-read; Sol findings are from the preceding review. |
| [S05] | Baseline `sleep.rs`: direct exposure, interruption behavior, and number-schema/u64-parser mismatch. Re-read for this handoff. |
| [S06] | PR #25266: v2 direct-model-only defaults; merge metadata reviewed previously. |
| [S07] | Baseline `session/multi_agents.rs`: minute-scale waiting guidance and configured/catalog/bundled role resolution. |
| [S08] | Baseline goal runtime: active continuation and stopped-state handling. |
| [S09] | Baseline `tools/spec_plan.rs`: model/feature sleep selection and direct v2 collaboration registration. |
| [S10] | PR #41243: sleep feature gating and `always_on`; reviewed previously as merged and represented in the baseline. |
| [S11] | Stable release page for 0.154.0; release publication recorded in the prior audit. |
| [S12] | Annotated tag object resolving `rust-v0.154.0` to its release commit. |
| [S13] | Previously inspected development tree `a592c38c...`; historical snapshot, not current main. |
| [S14] | v2 wait handler at development commit `1715e550...`; previously returned the same blob as the baseline. |
| [S15] | Baseline core configuration: v2 minimum, default, and maximum wait constants. Re-read for this handoff. |
| [S16] | `tekacs/codex` fork commit `9ffcf8d`: proposed background-exec completion input and active/idle wake path. Not established as upstream-equivalent or production-validated. |
| [S17] | Baseline upstream unified-exec exit watcher: terminal-event path examined in the prior audit. |
| [S18] | PR #34969: keep sleep outside code mode; reviewed previously as merged and represented in the baseline. |
| [S19] | PR #35594, with related PR #37189 linked below: waiting guidance and usage-hint tracking leads. |
| [S20] | PR #23094: goal stopping on genuine blockers and usage limits; reviewed previously as merged and represented in the baseline. |
| [S21] | Issue #36379 author comment: closure because the proposed work belonged downstream, not evidence of a shipped default-timeout fix. |
| [S22] | Baseline `pending_input.rs` test suite: starting point for checking steering/mailbox delivery tests; test presence is not proof tests were executed here. |
| [S24] | Official OpenAI Work/Codex usage context and links to current usage/pricing documentation. Accounting must be verified against the actual account. |

Related primary sources to follow during verification: [PR #37189](https://github.com/openai/codex/pull/37189), [PR #41331](https://github.com/openai/codex/pull/41331), and [baseline subagent notification tests](https://github.com/openai/codex/blob/6b9826e3aa83b1a5947db50f4332cb9c65f1b340/codex-rs/core/tests/suite/subagent_notifications.rs). Control-tool analytics classification alone is not evidence of a billing change. The adjacent issues linked from #35108 include [#18394](https://github.com/openai/codex/issues/18394), [#32640](https://github.com/openai/codex/issues/32640), [#29122](https://github.com/openai/codex/issues/29122), [#13733](https://github.com/openai/codex/issues/13733), and [#24951](https://github.com/openai/codex/issues/24951); their individual status and release resolution are not asserted here.

### Supplied public reports: retrieve independently

| ID | Source and limitations |
|---|---|
| [S23] | Tibo/Thibault Sottiaux X update about Astra quality and older skills. Only the user-supplied excerpt was available; full retrieval failed. No CLI release mapping established. |
| [S25] | First Reddit discovery thread. Supplied as context; full retrieval failed. |
| [S26] | Relux Works article about goal-related token burn. Supplied as context; full retrieval failed during handoff preparation. |
| [S27] | Ivan Oparin X discovery thread. User supplied an excerpt mentioning a float-to-integer tool-call problem; full retrieval failed. |
| [S28] | Later Reddit post about short waits and a claimed 30% quota improvement. Text supplied by the user; full retrieval failed. Anecdotal outcome only. |
| [S29] | Japanese X report about a 60-second subagent-related instruction and usage improvement. User-supplied excerpt only; exact change and live environment unverified. |

A fetch failure is an access limitation, not evidence that a page or reported problem does not exist. No figures from inaccessible posts should be upgraded into verified measurements.

[S01]: https://github.com/openai/codex/issues/35108 "Nested wait polling and parent inference report"
[S02]: https://github.com/openai/codex/issues/28144 "Durable goal wait/wake request"
[S03]: https://github.com/openai/codex/blob/6b9826e3aa83b1a5947db50f4332cb9c65f1b340/codex-rs/core/src/tools/handlers/multi_agents_v2/wait.rs "Release-pinned v2 wait handler"
[S04]: https://github.com/openai/codex/blob/6b9826e3aa83b1a5947db50f4332cb9c65f1b340/codex-rs/models-manager/models.json "Release-pinned model catalog and public instructions"
[S05]: https://github.com/openai/codex/blob/6b9826e3aa83b1a5947db50f4332cb9c65f1b340/codex-rs/core/src/tools/handlers/sleep.rs "Release-pinned native sleep handler"
[S06]: https://github.com/openai/codex/pull/25266 "Set multi-agent v2 defaults"
[S07]: https://github.com/openai/codex/blob/6b9826e3aa83b1a5947db50f4332cb9c65f1b340/codex-rs/core/src/session/multi_agents.rs "Release-pinned multi-agent role guidance"
[S08]: https://github.com/openai/codex/blob/6b9826e3aa83b1a5947db50f4332cb9c65f1b340/codex-rs/ext/goal/src/runtime.rs "Release-pinned goal runtime"
[S09]: https://github.com/openai/codex/blob/6b9826e3aa83b1a5947db50f4332cb9c65f1b340/codex-rs/core/src/tools/spec_plan.rs "Release-pinned tool registration and exposure"
[S10]: https://github.com/openai/codex/pull/41243 "Configurable sleep gating"
[S11]: https://github.com/openai/codex/releases/tag/rust-v0.154.0 "Codex 0.154.0 release"
[S12]: https://api.github.com/repos/openai/codex/git/tags/36eab01061df3cde5f95ec20a526777b430091ba "Annotated release tag object"
[S13]: https://github.com/openai/codex/tree/a592c38c16cdd7623dacc9168926ebccedfb67d3 "Earlier audited development snapshot"
[S14]: https://github.com/openai/codex/blob/1715e55076737158ba61d43158ede504de6d4ce1/codex-rs/core/src/tools/handlers/multi_agents_v2/wait.rs "Later audited v2 wait snapshot"
[S15]: https://github.com/openai/codex/blob/6b9826e3aa83b1a5947db50f4332cb9c65f1b340/codex-rs/core/src/config/mod.rs "Release-pinned timeout constants"
[S16]: https://github.com/tekacs/codex/commit/9ffcf8db9078eae43d4111ff94259795c1e962c9 "Fork background-exec wakeup patch"
[S17]: https://github.com/openai/codex/blob/6b9826e3aa83b1a5947db50f4332cb9c65f1b340/codex-rs/core/src/unified_exec/async_watcher.rs "Release-pinned upstream exec watcher"
[S18]: https://github.com/openai/codex/pull/34969 "Keep sleep outside code mode"
[S19]: https://github.com/openai/codex/pull/35594 "Recommend longer v2 waits"
[S20]: https://github.com/openai/codex/pull/23094 "Stop goal continuation on blockers and usage limits"
[S21]: https://github.com/openai/codex/issues/36379#issuecomment-5146516255 "Wrong-repository closure explanation"
[S22]: https://github.com/openai/codex/blob/6b9826e3aa83b1a5947db50f4332cb9c65f1b340/codex-rs/core/tests/suite/pending_input.rs "Release-pinned pending-input tests"
[S23]: https://x.com/thsottiaux/status/2098612714704891959 "Supplied Astra quality and skill update"
[S24]: https://help.openai.com/en/articles/20001275/ "Official Work and Codex account/usage context"
[S25]: https://www.reddit.com/r/codex/comments/1wdlp7q/weve_discovered_the_issue_behind_codex_harness/ "Supplied Reddit harness-limit discovery report"
[S26]: https://relux.works/en/blog/codex-goal-token-burn/ "Supplied Relux goal token-burn article"
[S27]: https://x.com/ivanopcode/status/2098379274017231094 "Supplied Ivan Oparin discovery thread"
[S28]: https://www.reddit.com/r/codex/comments/1wenst7/i_figured_the_culprit_of_astra_token_burning_so/ "Supplied Reddit longer-wait observation"
[S29]: https://x.com/ml0_1337/status/2098763395524911413 "Supplied Japanese subagent-wait report"
