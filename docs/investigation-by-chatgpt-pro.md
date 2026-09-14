# Investigation of Codex Excessive Wait Loop Token Consumption Issue by ChatGPT Pro

<user_message>
\<contexts>
We’ve discovered the issue behind codex harness limit drainage. : r/codex: https://www.reddit.com/r/codex/comments/1wdlp7q/weve_discovered_the_issue_behind_codex_harness/

Why Codex burns a weekly limit in a day while the agent waits for the tide | Relux Works: [[https://relux.works/en/blog/codex-goal-token-burn/\](https://relux.works/en/blog/codex-goal-token-burn/)](https://relux.works/en/blog/codex-goal-token-burn/]\(https://relux.works/en/blog/codex-goal-token-burn/\))

Ivan Oparin on X: "fellow codex limit sufferers ('weekly gone by wednesday' club): i accidentally found the core issue behind it, with help from muse spark (cc @claireszhou) and fable. plugged muse-spark 1.3 into codex, hit a float-to-int bug on a tool call, pulled the thread 🧵" / X: https://x.com/ivanopcode/status/2098379274017231094

Add wait/wake support for goals without spending tokens · Issue #28144 · openai/codex: https://github.com/openai/codex/issues/28144

wake model when background exec commands complete · tekacs/codex\\\\@9ffcf8d: https://github.com/tekacs/codex/commit/9ffcf8db9078eae43d4111ff94259795c1e962c9



 Tibo on X: "Hi Astra users. A reset and a quick update on quality issues that have been posted around. Working with some of you, we have found and fixed the following issues: - Some skills written for previous models were triggering too often or preventing the model from checking its work." / X: [[https://x.com/thsottiaux/status/2098612714704891959\](https://x.com/thsottiaux/status/2098612714704891959)](https://x.com/thsottiaux/status/2098612714704891959]\(https://x.com/thsottiaux/status/2098612714704891959\))

ミロ on X: "codexってCLI側（アプリも内部でCLIを使う）でsubagentsの稼働の時間制限を60秒にするプロンプトがインジェクトされてるせいで、デフォルトのままだとastra maxがメンヘラのようにsubagentsをチェックしまくって残usageが爆散する。これを無効化したらトークンの消費の減りがめちゃくちゃ改善した。" / X: https://x.com/ml0_1337/status/2098763395524911413

\</contexts>

Based on the issue reports and the related context above (very high token consumption due to mis-designed task/subagent watch loop system of Codex and its latest model GPT-6 Astra), propose short-term solutions (mainly prompts in AGENTS.md and Agent Skills, usage guidance for usage of `/goal command`, etc.) that individual Codex users can do to workaround or mitigate the very high token consumption for too frequent & wasteful model-driven task watching caused by the issues above.

Presumably due to the issues above, our company's Codex token usage has jumped abruptly after the release of GPT-6 Astra model in Codex last week. I want to craft a Slack message to post in our company-wide Slack channel to make our engineers aware of the serious cost/token consumption issues above, give them quick but effective mitigation measures and distributed our best recommended prompts for AGENTS.md and a dedicated Agent Skill to tackle this issue.

</user_message>

**I recommend a three-part mitigation: pause wait-only `/goal` sessions, use actual runtime waiting rather than model-driven polling, and distribute a small AGENTS.md rule set plus a narrowly scoped skill.** Do not respond by disabling verification or replacing Codex’s entire system/role prompt.

The reports identify a credible contributor to your company’s increase, but they do not establish how much of the increase it explains. Importantly, the durable wait/wake issue was opened on **June 14, 2026**, before Astra, and remained open when checked. This is not necessarily an Astra-only problem.

## Downloadable rollout package

**[Download the complete mitigation bundle](sandbox:/mnt/data/codex-token-mitigation.zip)**

It includes the Slack announcement and setup reply, a **167-word AGENTS.md snippet**, a **477-word skill**, optional configuration snippets, source notes, and a pilot evaluation checklist.

Individual files: [Slack announcement](sandbox:/mnt/data/codex-token-mitigation/SLACK_MESSAGE.md) · [AGENTS.md snippet](sandbox:/mnt/data/codex-token-mitigation/AGENTS.snippet.md) · [SKILL.md](sandbox:/mnt/data/codex-token-mitigation/.agents/skills/token-efficient-polling/SKILL.md) · [Installation and evidence notes](sandbox:/mnt/data/codex-token-mitigation/README.md)

**Validation:** YAML, TOML, document structure, and ZIP integrity were checked. Actual Codex behavior and token savings have **not** been tested; the package includes the necessary pilot scenarios.

## 1. Ready-to-post Slack announcement

Attach the ZIP to this post, then put the [setup instructions](sandbox:/mnt/data/codex-token-mitigation/SLACK_THREAD_SETUP.md) in a thread reply.

```text
*Codex usage spike: temporary guardrails for wasteful waiting/polling*

We've seen a sharp increase in our Codex usage since the GPT-6 Astra rollout. Public reports describe a credible contributing pattern: repeated model turns that do little more than check background commands, subagents, or CI—especially with an active `/goal`. This can consume usage without corresponding progress. We have not yet established how much of our increase this explains.

*Please apply these temporary measures:*

1. *Don't leave `/goal` running as a CI/PR dashboard.* Use finite objectives with clear completion criteria. When waiting for an external event or human review, run `/goal pause` and check `/goal` shows `paused`. Resume with `/goal resume` when there is something to act on. A chat message saying “stop,” or a final assistant reply, is not a reliable substitute for pausing. Check running workers/processes separately; pausing the goal is not a promise that everything has been cancelled.

2. *Install the attached waiting guardrails.* Merge `AGENTS.snippet.md` into your existing AGENTS.md—do not overwrite project policies. Copy the `token-efficient-polling` skill folder to `.agents/skills/` in the repo OR `~/.agents/skills/` for personal use, not both. Start a fresh session. Invoke `$token-efficient-polling` on tasks with background work; this pilot skill is explicit-only to avoid adding another over-triggering skill. The short AGENTS rules apply independently.

3. *Prefer one agent for routine work.* Delegate only useful independent tasks, not “watch the other agent.” If repeated checking continues, pause the goal and use the included optional single-agent configuration. Audit older instructions that demand constant polling, unconditional delegation, or frequent status reports. *Keep required tests, review, and security checks.*

The bundle also includes an opt-in `clock.sleep` configuration for supported clients. Native waiting is preferable to repeated model checks; simply adding a shell `sleep` does not guarantee this. These are mitigations, not a verified upstream fix or a promise of a particular saving.

Please reply in this thread with your client/build, model/reasoning setting, whether `/goal` or subagents were used, and a redacted example of repeated checks or before/after usage. Do not post raw transcripts, credentials, or proprietary source in public issues.

Sources:
https://github.com/openai/codex/issues/28144
https://relux.works/en/blog/codex-goal-token-burn/
https://learn.chatgpt.com/docs/agent-configuration/agents-md
```

The pause/status instructions above match the inspected Codex goal controls. They deliberately distinguish **pausing goal continuation** from cancelling every outstanding activity.

## 2. Recommended AGENTS.md snippet

This is the baseline I would distribute broadly. It focuses on unnecessary observation, without discouraging useful work or verification.

```markdown
## Token-efficient waiting

- Preserve required tests, review, security checks, and completion evidence. Reduce idle model turns, not verification.
- Use subagents only for bounded independent work; never create watcher agents or duplicate a running worker's task.
- Retain task/session handles. Prefer documented completion events or a long native blocking wait; batch handles when supported. Never assume background shell completion will wake an idle session.
- If only waiting remains and native waits return too quickly, use exposed `clock.sleep` directly before one minimal status check: integer `duration_ms`, normally 120000–300000, adjusted to actual deadlines. Do not invent unavailable tools.
- Avoid rapid empty `write_stdin`, `list_agents`, `ps`, `tail`, status-message, or shell-sleep polling loops. A wait timeout is not task failure; do not restart work solely because observation timed out.
- Bound monitoring. If efficient waiting is unavailable, report the pending handle and hand off. For an active `/goal`, ask the user to `/goal pause`; ending a reply does not pause it. Never fake `complete` or `blocked` to stop usage.
```

Merge it into the repository’s existing `AGENTS.md`, or `${CODEX_HOME:-~/.codex}/AGENTS.md` for personal defaults. Check existing `AGENTS.override.md` and more-specific instructions, then start a fresh session: they affect which guidance is loaded and takes precedence. **Do not overwrite the existing file or introduce an override that hides company policies.** ([ChatGPT Learn][1])

The 2–5-minute interval is a **proposed operating default**, not a Codex requirement. Event-driven waits are preferable when supported; genuine deadlines and interactive input should determine responsiveness.

## 3. Dedicated Agent Skill

The skill adds the cases that are too detailed for an always-present AGENTS.md section: short native timeouts, missing tools, unsupported completion callbacks, repeated early wakes, and active-goal handoff.

Save this as `.agents/skills/token-efficient-polling/SKILL.md`:

```markdown
---
name: token-efficient-polling
description: Use when a Codex task must wait for a background command, subagent, CI job, deployment, or external event, especially when repeated status checks or an active /goal are producing no new evidence.
---

# Token-efficient polling

Reduce model turns that merely observe unchanged state. Preserve required tests, review, security checks, and truthful completion evidence. Follow higher-priority runtime instructions; this skill cannot change scheduler semantics.

## Establish the wait once

Keep the existing task/session handle, completion condition, and a bounded observation deadline. Use the user's deadline; otherwise default to a 15-minute unattended observation window before handing off, not a task-kill timeout. Do genuinely independent work when available; do not manufacture work or repeat planning to remain active.

## Select a real waiting mechanism

1. Prefer documented completion notifications or an available native blocking wait. Batch outstanding handles when supported. Use the actual tool schema and a practical long wait; never assume an arbitrary background shell process can wake an idle session.
2. If a wait returns still-running too quickly, call exposed `clock.sleep` directly before the next minimal check. Use integer `duration_ms`, normally 120000–300000, adjusted to expected duration and deadlines. Back off unchanged external jobs toward 600000 where appropriate. Sleep only while no actionable work remains. Honor meaningful input, failure, cancellation, or completion that interrupts the wait.
3. If runtime sleep is unavailable, use an actual long blocking wait or hand off. A shell `sleep` that yields a session to be repeatedly polled is not equivalent. An external deterministic watcher is useful only if it does not create repeated model turns and has a bounded lifetime.

On each wake, consume new evidence or check the retained handle once. Do not repeatedly dump unchanged logs, probe liveness, request worker updates, or narrate waiting. If waits repeatedly return immediately without actionable input, report the failed suspension and hand off rather than spinning.

## Delegation and stopping

Delegate bounded independent work, never watching another worker. Do not duplicate a worker's task, invent a short worker deadline, or restart work solely because an observation timed out. A timeout is not terminal evidence. Diagnose actual errors using authoritative state.

For an active `/goal`, ending a turn or saying “paused” does not stop continuation. At the observation deadline, or when efficient waiting is unavailable, report the pending handle and ask the user to run `/goal pause` and verify its state. Request the pause once, not on every automatic continuation; use efficient waiting while awaiting it when possible. Do not claim to have paused it without a successful supported action. Do not fake `complete` or `blocked`. Do not resume or clear a goal without authorization.

For an ordinary task, hand off honestly with what remains and how to resume. Do not promise an unsupported automatic callback. When work finishes, inspect its result and perform required verification; report evidence, not mere elapsed time.
```

### Invocation policy

For the initial rollout, I recommend **explicit invocation**, while the small AGENTS.md rules remain active independently. This avoids introducing another broadly triggered skill.

The bundle includes `agents/openai.yaml` with:

```yaml
policy:
  allow_implicit_invocation: false
```

Codex documents this setting as disabling implicit activation while retaining explicit `$skill` invocation. Install the complete folder in **either** the repository’s `.agents/skills/` or personal `~/.agents/skills/`, not both. ([ChatGPT Learn][2])

Example:

```text
$token-efficient-polling Run the integration tests and investigate
actual failures. Preserve the existing process handle, use native
waiting, and do not delegate monitoring. Keep the required verification.
```

The 15-minute observation window is also a proposed pilot default. It limits **unattended observation**, not the worker’s execution time. For an active goal, the human must actually perform the requested pause; the prompt cannot enforce that state transition.

## 4. Optional configuration with stronger practical effects

### Expose native sleep independently of model selection

For supported clients, merge this into the existing `[features]` table in the effective `config.toml`:

```toml
[features]
sleep_tool = { enabled = true, mode = "always_on" }
```

The configuration tests explicitly cover `always_on` exposing sleep without model-provided clock configuration. Thus, the approach need not depend on Astra being selected. However, **check the actual client build and exposed tools**, rather than assuming every older installation supports the setting.

The inspected **Codex 0.154.0** implementation exposes `clock.sleep` with integer `duration_ms`; for example, `300000` means five minutes. It waits inside the runtime and can return early when input arrives.

Three limitations matter:

* **Exposure is not invocation.** Enabling the tool does not make the model choose it.
* **Sleeping is not an entirely free operation.** Calling and resuming the tool still involve model activity; other agents can continue consuming usage.
* **It is not a universal completion subscription.** It does not establish that every background shell process will generate a wake event. The referenced fork explicitly adds that delivery behavior.

### Temporarily disable subagent tools

For engineers seeing repeated subagent checking, a supported configuration switch is more dependable than increasingly emphatic “please don’t delegate” wording.

For a new CLI session:

```sh
codex -c agents.enabled=false
```

Or merge into the effective configuration:

```toml
[agents]
enabled = false
```

The official configuration reference identifies `agents.enabled` as the switch for multi-agent tools. Treat it as a temporary containment option, not a guarantee that previously running workers or separate sessions have been cancelled. ([ChatGPT Learn][3])

Using a known-good model or a lower adequate reasoning setting is another reasonable **comparison experiment**, but I would not present either as fixing the waiting mechanism. Keep model changes separate when measuring whether the prompt itself helped.

## 5. `/goal` guidance: the most important operational change

**Use `/goal` for finite autonomous work—not as a permanent monitoring dashboard.**

A suitable objective is:

```text
Implement the retry fix, run the specified tests, and review the final
diff against the acceptance criteria. Complete only when those checks
pass. Do not broaden the task into continuous PR/CI monitoring.
```

Avoid objectives such as “keep watching the PR, CI, agents, and review comments until everything is perfect.” That leaves no clear stopping boundary.

When work becomes purely external waiting, use:

```text
/goal pause
```

Then inspect:

```text
/goal
```

After the relevant event arrives:

```text
/goal resume
```

The inspected UI supports these state controls and displays the current goal status. Use `/goal clear` only when intending to remove the saved goal. **A final response, a message saying “stop,” or an assertion that the agent is paused is not equivalent to a successful pause.**

Do not distribute a workaround that marks a healthy, still-running task `complete` or `blocked` merely to save usage. The inspected continuation instructions require real completion evidence and a strict blocked-state audit. They also distinguish observation timeouts from actual task failure.

Where a client exposes a real runtime token budget, use and verify that setting. **“Use at most N tokens” in prose is not an enforced budget.** The inspected `/goal` summary displays a configured budget, but its supported command list does not contain a `/goal budget` command.

## 6. What I would not include in the company recommendation

### “Just tell it to use shell `sleep`”

The important distinction is **which component is waiting**:

```text
Inefficient:
shell process sleeps
→ execution tool yields a live session
→ model repeatedly checks that session

Preferred:
runtime blocks on a supported wait
→ no repeated observation turns while pending
→ meaningful result or input resumes execution
```

A bounded external watcher can be useful, but merely launching it in the background does not ensure the parent model stops polling. The fork’s explicit completion-notification changes illustrate why this requires runtime behavior, not just different prose.

### “All current subagents have a hard 60-second lifetime”

I would describe this as a **reported prompting problem**, not a verified universal runtime limit.

The inspected 0.154.0 bundled guidance actually recommends waits measured in minutes. It also allows role text to come from model metadata or configuration, so different effective prompts are possible. That makes the supplied report plausible without establishing that every current user receives the same instruction.

I could not independently retrieve the full X threads. Their supplied excerpts should not be treated as proof of a universally shipped limit—or proof that all polling paths have since been fixed.

### “Delete the role prompts or disable all old skills”

Blank role overrides can suppress useful coordination guidance. Also, the inspected configuration labels `usage_hint_enabled` as a **deprecated, ignored** compatibility field, so it should not be distributed as a proven disable switch. Prefer supported single-agent containment, or a narrowly audited client-specific correction, over wholesale prompt replacement.

Most importantly, **AGENTS.md cannot reliably override a conflicting higher-priority runtime instruction**. When that is the cause, adding more forceful text is not a dependable remedy.

## 7. How to determine whether the rollout works

Pilot on a few comparable builds and delegated tasks before calling this a company-wide fix. Hold the client build, model, reasoning setting, task, and starting context approximately constant.

The decisive measures are **fewer no-change model turns**, preserved completion and verification quality, acceptable responsiveness, and lower **total parent-plus-child usage**. Keep cached input, uncached input, output, account-limit usage, and actual billed credits distinct rather than interpreting raw token totals as a dollar amount.

The [evaluation checklist](sandbox:/mnt/data/codex-token-mitigation/EVALUATION.md) specifically tests missing sleep tools, short/clamped waits, absent shell-completion callbacks, repeated early wakeups, healthy workers exceeding observation timeouts, and active goals awaiting human review.

**My rollout recommendation:** distribute the AGENTS.md snippet and explicit-only skill, discourage wait-only active goals immediately, and offer native sleep plus single-agent mode as verified-per-client options. That addresses the immediate risk without making unproven causal claims or weakening correctness safeguards.

Would you like an alert when upstream ships a verified fix for these wait/wake paths?

[1]: https://learn.chatgpt.com/docs/agent-configuration/agents-md "https://learn.chatgpt.com/docs/agent-configuration/agents-md"
[2]: https://learn.chatgpt.com/docs/build-skills "https://learn.chatgpt.com/docs/build-skills"
[3]: https://learn.chatgpt.com/docs/config-file/config-reference "https://learn.chatgpt.com/docs/config-file/config-reference"

<user_message>
Have you checked https://github.com/openai/codex to identify what fixes are already released and which are not yet? Already landed fixes might have obsoleted some of the tips we are going to distribute. Which fix landed and which has not would change our advice.

Also we want to include in the Slack message succinct, easy-to-understand, ASCII-assisted summary of the mechanisms of the issues that had been causing the spin-wait-loop like excess model-driven watching.
</user_message>

**The earlier answer was source-reviewed, but not sufficiently release-qualified. That distinction changes the advice.** Several relevant improvements have already shipped; the remaining problems are narrower than “Codex cannot wait efficiently.”

I have now checked the relevant code at the **latest stable CLI release, 0.154.0**, compared the remaining failure paths with `main`, and checked the associated PRs and issues. The stable release was published on **September 10, 2026, JST**. Newer `0.155.0-alpha.*` builds exist, but their existence is not evidence that these problems are fixed. ([GitHub][1])

The audit anchors are `rust-v0.154.0` → commit `6b9826e3…`, and `main` → `a592c38c…`. **“Released by 0.154.0” below does not mean first introduced in 0.154.0**; I have not established the earliest containing release for every earlier change. Desktop/IDE embedded runtimes and server-supplied model instructions also need separate verification.

**Revised files:** [Complete v2 bundle](sandbox:/mnt/data/codex-token-mitigation-v2.zip) · [Release audit](sandbox:/mnt/data/codex-token-mitigation-v2/RELEASE_AUDIT.md) · [Slack announcement](sandbox:/mnt/data/codex-token-mitigation-v2/SLACK_MESSAGE.md) · [Setup thread reply](sandbox:/mnt/data/codex-token-mitigation-v2/SLACK_THREAD_SETUP.md)

## 1. What has already shipped

| Improvement                                                                                        | Verified status                                                                                                                                                                                   | How it changes our advice                                                                                                                                                                                 |
| -------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Keep native `clock.sleep` outside code mode** — PR **#34969**, merged July 23                    | **Released by 0.154.0.** The tagged implementation marks it `DirectModelOnly`.                                                                                                                    | Do not describe native sleep as necessarily passing through the polling-prone `functions.exec` wrapper. Use the existing direct tool. This does **not** make arbitrary shell `sleep` commands equivalent. |
| **Expose sleep independently of model selection** — PR **#41243**, merged August 28                | **Released by 0.154.0.** The tagged configuration supports `model_driven` and `always_on`.                                                                                                        | The `sleep_tool` configuration is a **shipped capability**, not a custom patch. It is optional/redundant where the native tool is already exposed. Exposure still does not force the model to use it.     |
| **Direct v2 collaboration tools and guidance to use longer waits**                                 | **Released by 0.154.0.** PR **#25266** established direct-only v2 defaults. The tagged instructions explicitly keep collaboration tools out of `functions.exec` and recommend minute-scale waits. | Do not generalize a **legacy/nested v1** report to every current v2 session. Prefer the existing direct native wait; do not disable code mode wholesale.                                                  |
| **Stop goal continuation on genuine blockers and usage exhaustion** — PR **#23094**, merged May 18 | **Released by 0.154.0.** `blocked` and `usageLimited` stop continuation; the tagged runtime contains those states.                                                                                | Claims that Codex must loop indefinitely on every genuine blocker or exhausted usage limit are outdated. But a healthy child taking time is **not automatically a genuine blocker**.                      |

The important correction is therefore:

> **The efficient waiting mechanisms partly exist already. The problems include selecting and using them correctly, short observation defaults, older/nested execution paths, and `/goal` continuation semantics.**

## 2. What remains unresolved or unverified

### The default v2 wait is still 30 seconds

The stable tag contains:

```text
minimum wait:  10,000 ms
default wait:  30,000 ms
maximum wait: 3,600,000 ms
```

Current `main` still contains the **30,000 ms default**. Consequently, “long waits are supported” and “the default avoids frequent polling” are different claims.

A particularly misleading signal is **issue #36379 being closed**: its author explicitly closed it because the proposed work belonged in downstream repositories—not because upstream had adopted a five-minute default.

**Retain, but sharpen, the prompt advice:** request an **explicit, supported long timeout**, rather than relying on the default. For example, `timeout_ms: 300000` where the actual tool supports it. This is an observation interval, **not a five-minute worker lifetime**.

Also, increasing an inner wait timeout does not necessarily fix an outer wrapper that yields earlier. Issue **#35108** specifically documents a v1 wait nested inside `functions.exec`, with multiple parent resumptions for one logical wait. It remains open, but its described path is different from the already-direct v2 path.

### Durable `/goal` waiting is still not established as fixed

**Issue #28144 remains open.** Both the tagged release and audited `main` distinguish active from paused/blocked/usage-limited/complete states; active goals still enter idle continuation. I did not establish a shipped durable timer/event-wait implementation resolving that request.

**Keep the `/goal pause` advice.** Native sleep can hold a turn without repeated model calls, but that is not the same as a persisted scheduler state that survives restart and wakes on an external dependency.

The already-shipped blocker fix does **not** justify pretending a progressing worker is blocked. Nor does a final reply saying “waiting” pause the goal.

### The supplied background-shell wakeup patch is not a verified upstream fix

The **tekacs `9ffcf8d`** patch explicitly adds model-visible completion input and calls `inject_or_start`, including duplicate-completion suppression.

In contrast, the audited upstream exit-watcher code—both stable and `main`—still emits terminal completion events/metrics without that explicit model-input injection. I did not establish equivalent end-to-end wake behavior elsewhere for every background command. **A UI/app-server completion event is not proof that the parent model will wake.**

**Keep:** “Do not assume arbitrary background shell completion wakes an idle model.”

**Do not distribute:** “End the turn; every shell completion will automatically bring you back,” or “install this fork company-wide.”

### The sleep numeric schema/parser mismatch remains in the inspected source

Both audited refs return the same `sleep.rs` blob. Its schema advertises `duration_ms` using `JsonSchema::number`, while the parser field is `u64`.

**Keep the integer instruction:** use `300000`, not `300000.0`.

This is a separate tool-error risk. It does not establish that the numeric mismatch explains the company-wide spike.

### The “60-second subagent lifetime” and older-skill fixes cannot be assigned a verified CLI release

The tagged bundled instructions favor minute-scale waits, but role instructions can come from **model-catalog metadata or explicit configuration**. Therefore, repository code alone cannot establish whether a particular user received the reported 60-second instruction or whether a server-side prompt rollout removed it.

I could not independently retrieve the full X threads. The supplied announcement about older-skill fixes should not be treated as proof that every waiting path is fixed.

**Remove any universal “disable the 60-second lifetime limit” recommendation.** Audit the affected client’s effective instructions instead. Blank role overrides are particularly risky because the inspected resolver lets them suppress the normal fallback, including useful coordination guidance.

**Across the examined paths, I did not verify an additional main-only fix that resolves the durable-goal or generic background-shell-wakeup gaps.** That is a bounded audit conclusion, not a claim to have reviewed every unreleased commit or prerelease binary.

## 3. Changes I would make before distribution

The revised recommendation is **“update and use the shipped native waiting paths, then apply targeted safeguards”**, not “disable everything because the harness cannot wait.”

In particular, the AGENTS.md rules should explicitly request a suitable native timeout and avoid nested wrappers. Timer sleep should be a **fallback**, not an additional delay around an already-efficient wait. This follows the released direct-tool implementation while addressing the still-short default.

Here is the revised [AGENTS.md snippet](sandbox:/mnt/data/codex-token-mitigation-v2/AGENTS.snippet.md):

```markdown
## Token-efficient waiting

- Preserve required tests, review, security checks, and completion evidence.
- Keep existing task/session handles; do independent work rather than duplicate workers or spawn watchers.
- Prefer supported completion events or a direct native blocking wait. Set an explicit practical long timeout (e.g. 300000 ms when the tool supports it); batch handles when supported. Do not route native waiting through a polling code wrapper.
- If only waiting remains and native waits return too quickly, call exposed `clock.sleep` directly before one minimal check, using integer `duration_ms` (normally 120000–300000; respect actual deadlines). Do not add sleeps around already-efficient waits.
- No rapid empty status/log polling. An observation timeout is not worker failure; do not restart solely because it expired. Never assume arbitrary background shell completion wakes the model.
- Bound monitoring. For prolonged external waits, request `/goal pause` and verified state; a final reply does not pause an active goal. Never fake `complete` or `blocked`.
```

The shipped optional configuration remains:

```toml
[features]
sleep_tool = { enabled = true, mode = "always_on" }
```

Merge it into the existing table rather than adding a duplicate. Its purpose is **tool availability across model selection**, not “always sleep.” It is unnecessary when the tool is already exposed and does not implement durable goal scheduling.

The [updated skill](sandbox:/mnt/data/codex-token-mitigation-v2/.agents/skills/token-efficient-polling/SKILL.md) makes the same distinction. The bundle retains explicit-only invocation during the pilot. Single-agent mode is presented as containment for a demonstrated delegation-related loop, not a general prohibition on useful parallel work.

## 4. Revised Slack message with ASCII explanation

This version is approximately 355 words. Attach the revised bundle and put the [installation details](sandbox:/mnt/data/codex-token-mitigation-v2/SLACK_THREAD_SETUP.md) in a thread reply.

````text
*Codex: reduce unnecessary token use from status-check loops (13 Sep)*

We've observed a usage spike since the Astra rollout. Repeated watching of commands/subagents and active `/goal` sessions may contribute; we haven't established how much of our increase this explains.

*Why can waiting consume usage?*
```
Repeated watching:
  model -> check -> "still running" -> model -> check -> ...
          short waits / wrapper yields return control

An active /goal can add another loop:
  "waiting" / end turn -> goal still active -> new model turn -> ...

Preferred:
  model -> [runtime blocks; no repeated model calls] -> result -> model
```
The waste is repeated model invocations and context processing, not continuous token generation during a genuine blocking wait. A shell `sleep` alone can still leave the parent model checking its session.

*Some fixes already ship.* The latest stable CLI checked on 2026-09-13 is *0.154.0*: it has direct native sleep and direct v2 collaboration tools with long-wait guidance. But the v2 default wait remains 30 seconds, and `/goal` is not a durable event-driven scheduler. Updating is necessary for older clients, not proof that every waiting path is fixed.

*Please apply these guardrails:*
1. *Update the client you actually use.* Check CLI with `codex --version`; update desktop separately. A shell CLI version does not identify the app's embedded runtime.
2. *Keep `/goal` finite.* For prolonged external/CI/human-review waits, run `/goal pause`, then `/goal` to confirm `paused`. Resume when progress is possible. Saying “stop” or ending a reply is not equivalent; check running workers/processes separately.
3. *Use the attached AGENTS snippet and waiting skill.* Prefer direct native waits with an explicit supported long timeout. Use `clock.sleep` as fallback, not around an already-efficient wait. Installation and optional settings are in the thread reply.
4. *Escalate persistent loops.* Temporarily use single-agent mode when delegation is the trigger. Do not erase role prompts, blanket-disable skills/code mode, or remove tests/review/security checks.

Please share client/build, model/reasoning setting, `/goal`/subagent usage, and a redacted example. Do not treat raw/cached token totals as a direct bill or promise a particular saving. See the attached release audit for shipped versus unresolved/unverified details.

Sources:
https://github.com/openai/codex/releases
https://github.com/openai/codex/pull/34969
https://github.com/openai/codex/pull/41243
https://github.com/openai/codex/issues/28144
````

The critical explanatory distinction is **“repeated returns to the model”**, not “the model continuously burns tokens while a blocking wait is pending.” The nested-wait report explicitly makes that distinction and separately identifies its mostly cached input totals, which should not be interpreted directly as billed cost.

**Use the v2 bundle instead of the previous archive.** Its Markdown, YAML, TOML, required files, and ZIP integrity were statically checked. Live Codex compliance, responsiveness, and token savings remain untested; the included evaluation checklist covers those separately.

[1]: https://github.com/openai/codex/releases "https://github.com/openai/codex/releases"

<user_message>
どんなCodexのトークン以上消費に関する問題が発生していて、どれが残っていてどれが解決して、なぜこれらの配布・周知が必要なのか、をチームメンバーにわかりやすく説明するための日本語説明文も作成して。
</user_message>

[日本語説明文（Markdown）](sandbox:/mnt/data/codex-token-mitigation-ja/EXPLANATION.ja.md) · [Slack投稿版](sandbox:/mnt/data/codex-token-mitigation-ja/SLACK_MESSAGE.ja.md) · [日本語文面を追加した配布ZIP](sandbox:/mnt/data/codex-token-mitigation-v2-ja.zip)

配布ZIPには、前回の設定・プロンプトを変更せず、日本語の説明文とSlack投稿版を追加しています。

---

# Codexのトークン過剰消費について：何が起きていて、なぜ対策を配布するのか

**確認基準：2026年9月13日。公開ソース・リリースの確認結果をもとに、CLI 0.154.0を基準として整理しています。** デスクトップアプリの内蔵実行環境や、サーバーから配信されるモデル向け指示については、同じ修正が適用されているか別途確認が必要です。

## 1. 問題は「作業」ではなく「待ち方」にある

社内では、GPT-6 Astraへの切り替え後にCodexの使用量が急増しています。関連する公開報告には、コードを書く・調査する・検証するといった作業ではなく、**「まだ終わっていないか」を何度も確認するためにAIモデルが呼び出され、トークンを消費する**という問題があります。ただし、社内の増加分のうち、この問題がどの程度を占めるかは、まだ特定できていません。

Codexでは、AIモデルと、コマンドや子エージェントを動かす実行環境が連携しています。本来、子タスクの完了を待つだけなら実行環境側で待てばよいのですが、短い待機タイムアウトやツールの呼び出し方式によって、**結果が変わっていなくてもAI側へ制御が戻る**ことがあります。

```text
問題になる待ち方：
  AI -> 状態確認 ->「まだ実行中」-> AI -> 状態確認 -> ...
                                  ^
                         新しい進捗がなくても再推論

望ましい待ち方（対応する実行経路）：
  AI -> [実行環境が待機：AIを繰り返し呼ばない] -> 結果 -> AI
```

例えば、テストや子エージェントが数分かかる間、親のAIが何度も起きて「まだ実行中なので、もう一度待とう」と判断しているイメージです。

ここで問題なのは、**待機中ずっとAIが文章を生成していることではありません。** 待機が短く区切られるたびに、文脈の入力処理や次の行動の判断が発生することです。なお、入力にはキャッシュ利用分が含まれることがあり、**トークン総数、利用枠の減り方、実際の請求額は同一ではありません。**

## 2. すでに改善・導入されているもの

「Codexには効率的に待つ機能がない」という説明は、現状には合いません。以下の仕組みは、確認したCLI 0.154.0までに導入されています。**これは「0.154.0で初めて導入された」という意味ではありません。**

| 改善・導入済みの仕組み                     | 何が改善されたか                                                                                            |
| ------------------------------- | --------------------------------------------------------------------------------------------------- |
| **ネイティブの `clock.sleep` を直接呼べる** | 汎用のコード実行ラッパーを経由せず、実行環境側で待機できる経路があります。PR #34969。([GitHub][1])                                        |
| **モデルに依存せずsleepツールを公開する設定**     | `sleep_tool` の `always_on` 設定を利用できます。ただし、「ツールが使える」ことと「モデルが必ず適切に使う」ことは別です。PR #41243。                 |
| **新しいv2方式の子エージェント連携**           | 連携ツールを直接呼び、分単位で長めに待つための経路・指示があります。古い方式の問題を、すべての現行環境に当てはめるのは不正確です。                                   |
| **本当に行き詰まった場合や利用上限到達時のgoal停止**  | `blocked`・`usageLimited` 状態で自動継続を止める仕組みがあります。ただし、正常に実行中の子タスクを待っているだけなら、直ちに「行き詰まり」にはなりません。PR #23094。 |

したがって、まず行うべきことは、古い環境を更新し、**すでに用意されている待機機能を使うこと**です。独自フォークや大規模なプロンプト上書きを全員に導入する方針ではありません。

## 3. それでも残っている問題・注意点

### A. 長く待てる機能があっても、既定値や呼び方によって短い待機が繰り返される

確認したv2の待機時間の既定値は、まだ**30秒**です。長い待機を指定できても、既定値に任せたり、モデルが短い時間を明示したりすると、繰り返しモデルへ戻る余地があります。これは**親が一度に待つ観測時間**であり、子エージェントの実行寿命ではありません。

また、古いv1方式で待機ツールを汎用コード実行の中から呼ぶと、一度の待機が複数回のモデル再開に分かれる報告も残っています。この問題は、新しいv2の直接呼び出し経路とは区別して扱います。

**対策の方針は、対応するネイティブ待機を直接呼び、必要に応じて長めの待機時間を明示することです。** ただし、実際の期限や応答性を考慮し、何でも長時間待たせるわけではありません。

### B. `/goal` は「待機予約」ではなく「目標に向けて自動継続する機能」

`/goal` が有効なまま、AIが「結果を待ちます」と返答しても、それだけで自動継続が停止するわけではありません。([github.com][2])

```text
  AI「結果を待ちます」-> そのターン終了
                              |
                     goal が active のまま
                              |
                              v
                  次のAIターンを自動開始
                              |
                              v
                       再び状態を確認 ...
```

「外部の処理が終わるまでモデルを呼ばずに待ち、イベントや時刻で自動再開する状態」を永続化する機能は、今回の監査では解決を確認できていません。関連Issue #28144も未完了です。ネイティブsleepで一時的に待つことと、このような永続的な待機・再開機能は別物です。([github.com][2])

そのため、長時間のCI待ちや人のレビュー待ちなど、しばらく実行できる作業がない場合は、次の運用にします。

```text
/goal pause
    |
    v
/goal で paused を確認
    |
    v
進められる状態になったら /goal resume
```

親のgoalを一時停止しても、既存の子タスクやシェルプロセスをすべて中止したとは限りません。実行中の処理は別途確認してください。

### C. シェルの `sleep` や終了通知だけでは、AI側が適切に待つ保証にならない

シェル内で `sleep` していても、そのシェルの状態を親のAIが繰り返し確認していれば、無駄な呼び出しは残ります。

```text
シェル： [sleep中／処理実行中........................]
親のAI： 確認 ->「実行中」-> 確認 ->「実行中」-> ...
```

また、画面や内部イベントに「終了」が届くことと、必要な結果がAIへ渡り、停止中のAIが自動再開することも別です。提供された外部フォークには後者を追加するパッチがありますが、同等の動作が公式のすべての実行経路に導入済みとは確認できていません。したがって、**「裏で実行してターンを終えれば、必ず自動で戻ってくる」とは案内しません。**

### 未確認の情報は、一律の対策にしない

SNS上の「60秒で子エージェントを終了させる指示」は、全ユーザー共通の実行制限として確認できていません。公開ソースに含まれる指示と、モデル向けに配信される指示・個別設定は区別が必要です。**一律に「60秒制限を解除する」「役割プロンプトを削除する」とは案内しません。**

実装上の小さな注意点として、sleepの引数には数値スキーマと整数パーサーの差が残っているため、配布する指示では `duration_ms` を `300000` のような整数で渡す方針を維持しています。これも、使用量急増の全体を説明する原因と断定するものではありません。

## 4. なぜAGENTS.md・Skill・操作ガイドを配布するのか

**「効率的に待つ機能が実装されていること」と、「各セッションでその機能が適切に使われること」は別だからです。** 待機機能や長めの待機を勧める指示は導入されていますが、既定値や呼び出し方による注意点は残っています。

今回の配布物は、その隙間を埋めるための暫定的な運用ガイドです。

| 配布・周知するもの                           | 今回の役割                                                                                   |
| ----------------------------------- | --------------------------------------------------------------------------------------- |
| **`AGENTS.md` の短い追記**               | 不要な状態確認を連打しない、直接の待機を優先する、待機タイムアウトだけでタスクを再起動しない、といった基本方針を共有します。                          |
| **`token-efficient-polling` Skill** | 待機の多いタスクで、利用可能なツール・実際の期限に応じた待機や、待機手段がない場合の引き継ぎ方を指示します。試行導入では明示的に呼び出し、無関係な作業まで毎回起動させません。 |
| **`/goal` の操作・更新ガイド**               | AIの返答だけでは止まらない自動継続を、利用者が実際の状態操作で止められるようにします。既存の修正を取り込むためのクライアント更新も案内します。                |

プロンプトでCodexの実行環境そのものを書き換えたり、存在しない終了通知・スケジューラーを追加したりすることはできません。そのため、**ソフトウェアの更新、モデルへの指示、利用者による操作**を組み合わせます。

## 5. チームへのお願い

1. **使っているクライアントを更新してください。** CLIは `codex --version` で確認し、デスクトップアプリは別途更新してください。
2. **配布した追記・Skillを、既存ルールを消さずに導入してください。** 直接の待機を優先し、すでに効率的に待てている経路には余計なsleepを追加しない方針です。
3. **進捗のない監視を放置しないでください。** `/goal` は終了条件を明確にし、長い外部待ちでは一時停止します。繰り返し確認が続く場合は、クライアント・モデル・推論設定・子エージェント利用の有無と、機密を除いたログを共有してください。

**減らしたいのは「何も変わっていないことの再確認」であり、テスト・レビュー・セキュリティ確認ではありません。** 子エージェントやスキルの全面禁止、検証の省略、未完了のタスクを完了扱いにすることは勧めません。

今回の配布は、**修正済みの待機機能を活用しながら、残っている自動継続・監視の問題による無駄な呼び出しを抑えるため**のものです。効果は実際の使用量と作業品質を比較して判断し、特定の削減率や完全解決は保証しません。

[1]: https://github.com/openai/codex/pull/34969 "Keep the sleep tool outside code mode by copyberry[bot] · Pull Request #34969 · openai/codex · GitHub"
[2]: https://github.com/openai/codex/issues/28144 "Add wait/wake support for goals without spending tokens · Issue #28144 · openai/codex · GitHub"

<user_message>
gpt-6-astra model とそれ以前のモデル (gpt-5.6-sol, gpt-5.6-terra, gpt-5.6-lunaなど) とで、対応を分ける必要はある？
</user_message>

**設定や注意点は一部分ける必要があります。ただし、AGENTS.mdとSkillを「Astra用／それ以前用」の2種類に分けるより、共通の対策に、利用可能なツール・実行経路・有効な指示に応じた条件分岐を入れるのが適切です。**

今回、モデル別の定義まで確認したところ、**GPT-5.6系の中にも違いがありました。また、前回の「長めに待つ」指示には補足・修正が必要です。**

## 1. 確認できたモデル別の違い

以下は、前回と同じ **Codex CLI 0.154.0に同梱された `models.json`** の比較です。実際のセッションでは、配信されるモデルカタログや設定によって変わる可能性があるため、モデル名だけで利用可能なツールを断定しない前提です。

| モデル             | 子エージェントの方式 | モデル定義での `clock` 宣言 |
| --------------- | ---------- | ------------------ |
| `gpt-6-astra`   | **v2**     | **あり**。            |
| `gpt-5.6-sol`   | **v2**     | なし。                |
| `gpt-5.6-terra` | **v2**     | なし。                |
| `gpt-5.6-luna`  | **v1**     | なし。                |

したがって、**「Astraは新しい実行方式、それ以前はすべて古い実行方式」という分け方は不正確**です。Sol・Terraは、確認した定義ではAstraと同じv2です。

### 違い①：ネイティブsleepが使えるようになる条件

既定の `model_driven` モードでは、モデルによる `clock` 宣言や既存のclock設定が、`clock.sleep` を公開する条件になります。一方、`always_on` では、そのモデル別条件を通さずにsleepを登録する実装です。なお、**clock未宣言だから必ずsleepが使えない、というわけではありません。** 別のclock設定から有効になる経路もあります。

今回の配布では、対応クライアントで次を共通設定にする方針でよいです。

```toml
[features]
sleep_tool = { enabled = true, mode = "always_on" }
```

**すでにこの設定を有効にしているなら、sleepを公開するためにAstraと5.6系で設定を分ける必要は原則ありません。** ただし、実際にその設定が適用されたセッションでツールが公開されているかは確認が必要です。「公開する設定」であって、「モデルに必ずsleepを選ばせる設定」ではありません。

### 違い②：子エージェントの待機経路

v2には、子エージェント連携ツールをコード実行ラッパーの外に直接公開する経路があります。v1とv2ではツール登録の仕方が異なるため、**Lunaを含むv1環境では、待機が `functions.exec` → ラッパーの待機 → モデル再開、という経路になっていないかを重点的に確認**するのが適切です。これは、Lunaでは必ず問題が起きるという意味ではありません。

また、**`[features.multi_agent_v2]` の設定を配れば、v1環境にも同じ対策が効くとは限りません。** 配布するSkillでは特定の名前空間やv2専用設定を前提にせず、そのセッションに実際に公開されている待機ツールを使わせるべきです。

## 2. 重要な補足：「60秒」の指示はAstraだけの問題ではない

今回、同梱されたモデル向け指示を確認すると、**少なくともAstraとSolの両方**に、次の記述がありました。

> Avoid performing blocking sleep or wait calls longer than 60 seconds

ユーザーとのコミュニケーションが途切れることを理由に、60秒を超えるブロッキング待機を避けるよう求める文脈です。

ここは、次のように区別する必要があります。

```text
確認できたこと：
  「1回の待機を60秒より長くしないように」というモデル向け指示

それとは別のこと：
  「子エージェントが60秒で強制終了する」という実行上の制限
```

**前者の指示は確認できましたが、それを後者の制限として説明してはいけません。** また、これだけで「全セッションに現在も同じ指示が適用されている」「社内の使用量増加の主因である」とまでは言えません。

ただし、配布する指示への影響はあります。前回の「`300000 ms`、つまり5分を明示して待つ」という案は、**ツールが受け付けるだけでなく、有効な上位指示とも競合しない場合の選択肢**として扱うべきでした。

```text
ツール実装：
  長い待機を受け付ける

モデル向け指示：
  60秒を超える待機を避けるよう求める

AGENTS.md：
  5分待つよう求める
       |
       v
「長く待てる実装がある」だけでは、適切に選択される保証にならない
```

これは**指示が競合し得るというソースに基づく分析**であり、実際のループ発生や削減効果の実測結果ではありません。AGENTS.mdの文言を強めるだけで、上位の指示を確実に上書きできるとは扱わないほうが安全です。

## 3. 配布物は「共通の方針＋環境に応じた分岐」にする

私の推奨は、**共通Skillを維持し、長い待機時間の指定を条件付きにする**ことです。

具体的には、前回の待機時間に関する部分を次の方針に修正します。

```text
利用可能な直接のネイティブ待機を優先する。
待機時間は、ツールの仕様・有効な上位指示・実際の期限の範囲内で設定する。
2～5分は、許容される環境での例であり、一律の必須値ではない。

ネイティブsleepが公開されていなければ、存在しないツールを呼ばない。
短い待機への復帰が続く場合、同じ状態確認を無期限に繰り返さず、
未完了の処理を明示して引き継ぐ。
activeな /goal では、利用者に実際の一時停止操作を求める。
```

これにより、配布方針は次のようになります。

**Astra：** 共通対策を適用する。clockが既定で公開され得るからといって、待機ループまで解消済みと考えない。モデル向け指示との競合にも注意する。

**Sol・Terra：** 共通対策を適用する。`always_on` によりsleepの公開条件の違いを吸収する。同じv2であるため、Astraとまったく別の待機手順を用意する必要はない。

**Luna：** 共通対策を適用する。sleep設定に加えて、v1の待機がラッパー経由になっていないかを重点確認する。v2専用のツール名・設定を要求しない。

この区分は、上記のモデル定義とツール登録実装から導いた**運用上の推奨**です。モデル別の実測で効果を保証したものではありません。

### `/goal` の対策は全モデル共通

`/goal` がactiveのままターンを終えると自動継続する問題は、モデル固有というよりgoalの実行管理側の問題です。永続的な待機・再開を求めるIssue #28144は引き続きopenで、**以前のモデルへ戻すことが、この機構の修正になるわけではありません。** 長い外部待ちでの `/goal pause` と状態確認は、共通の案内として残します。

## 4. 使用量の分析は、モデル別に分ける必要がある

**対策の基本方針は共通化してよい一方、原因分析と効果測定はモデル別に分けるべきです。**

OpenAIの公式説明でも、AstraはSolより利用枠を速く消費する場合があり、タスク、入出力サイズ、推論設定、Fastモードによって変わるとされています。したがって、**「Astraへ変更後に利用枠が急減した」という観測だけでは、待機ループによる増加とモデル・設定による違いを分離できません。** ([OpenAI Help Center][1])

社内で比較する際は、少なくとも「モデル・推論設定・Fastモード・クライアント版・`/goal`／子エージェントの利用有無」を揃えるか、集計時に区別する方針を勧めます。見るべき指標も、総トークン数だけでなく、**進捗のないモデル再呼び出し回数、親子合計の使用量、検証品質**を分けると、対策が効いたか判断しやすくなります。

## Slackに追加する文面

> **対象モデルについて**
> 今回の対策はAstraだけでなく、Sol・Terra・Lunaにも適用する方針です。ただし、モデルやクライアントによって使える待機ツールと実行経路が異なるため、共通のSkillが実際の環境に合わせて動く形にします。確認したCLI 0.154.0の同梱定義では、Astra・Sol・Terraはv2、Lunaはv1の子エージェント方式です。
> また、AstraだけでなくSolにも「60秒を超える待機を避ける」というモデル向け指示がありました。これは子エージェントの寿命制限とは別です。そのため、5分待機などの指定は一律に強制せず、対応するツールと有効な指示の範囲内で使います。長い外部待ちでの `/goal pause` はモデル共通の対策です。以前のモデルへ戻すだけで、待機管理の問題が解消するとは考えないでください。

この追記の根拠は、同梱モデル定義・指示とgoalの待機機能に関する公開情報です。

**配布前に直すべき点は、「Astra限定の問題にしないこと」と、「2～5分の待機を無条件に要求しないこと」です。** 共通Skillを維持しつつ、この2点を修正するのが妥当です。

[1]: https://help.openai.com/ja-jp/articles/20001275-chatgpt-work-and-codex?utm_source=chatgpt.com "ChatGPT ワークと Codex | OpenAI Help Center"

<user_message>
- `[features]\nsleep_tool = { mode = "always_on" }` は設定してもらっている前提で、AstraやSolモデルに共通する案内にし、できるだけ説明文等の条件分岐を減らして簡素化して。Lunaは例外だが、コストが圧倒的に安いので対応しなくてい大丈夫なのでLuna向けにどうするかまでは触れず、できるだけ説明を簡潔にして。
- そのSlack修正後文面案には、Codexの内部実装に関する細かすぎる話まで含めてしまっている。もっとCodexの「利用者」向けの実践的かつわかりやすい内容にして。

修正後のファイルはダウンロードしたい。
</user_message>

**[修正版一式をダウンロード（ZIP）](sandbox:/mnt/data/codex-token-mitigation-v3-ja.zip)**

個別ファイル：
[Slack投稿文](sandbox:/mnt/data/codex-token-mitigation-v3-ja/SLACK_MESSAGE.ja.md) · [導入手順のスレッド返信](sandbox:/mnt/data/codex-token-mitigation-v3-ja/SLACK_THREAD_SETUP.ja.md) · [背景の日本語説明文・出典](sandbox:/mnt/data/codex-token-mitigation-v3-ja/EXPLANATION.ja.md)

共通プロンプト：
[AGENTS.mdへの追記](sandbox:/mnt/data/codex-token-mitigation-v3-ja/AGENTS.snippet.md) · [SKILL.md](sandbox:/mnt/data/codex-token-mitigation-v3-ja/token-efficient-polling/SKILL.md)

Skillは、明示呼び出しの設定ファイルも含むZIP内のフォルダーごと配置してください。前回の配布物からの更新手順も同梱しています。

## Slack投稿案

````text
*Codexの使用量増加への対策：待ち時間の無駄な確認を減らします*

社内でAstra導入後にCodexの使用量が増えています。関連する報告には、CIや子エージェントの完了待ちで、*同じ状態確認を繰り返し、作業が進まないままトークンを消費する*ケースがあります。社内の増加分のうち、これが占める割合はまだ特定できていません。

```
無駄な確認：AI -> 確認 ->「まだ実行中」-> AI -> 確認 -> ...
目指す動作：AI -> [待機] -> 新しい結果を確認 -> 作業再開
```

待つこと自体ではなく、*新しい情報がないのにAIを何度も呼ぶこと*が問題です。一部改善済みですが、設定だけで不要な確認がなくなるわけではないため、待ち方を指示するルールを配布します。*Astra・Sol共通の案内です。*

*お願いは3点です。*

1. *添付のAGENTS.md追記とSkillを導入してください。* 既存のルールは残し、待機の多いタスクでは `$token-efficient-polling` を指定します。導入手順はスレッドに記載します。
2. *長いCI待ち・レビュー待ちでは `/goal` を一時停止してください。* `/goal pause` の後に `/goal` で `paused` を確認し、進められる状態になったら `/goal resume`。AIが「待ちます」と返答するだけでは一時停止になりません。実行中の子タスクやコマンドは別途確認してください。
3. *同じ確認が続く場合は共有してください。* 使用中のモデル・アプリと、状況がわかる画面やログをこのスレッドへお願いします。機密情報は伏せてください。

*テスト・レビュー・セキュリティ確認は、これまでどおり必要です。* 削減するのは無駄な再確認です。クライアントの更新もお願いします。

背景と出典は添付の `EXPLANATION.ja.md`、導入手順は `SLACK_THREAD_SETUP.ja.md` にまとめています。
````

ファイル構成・YAML・ZIPの整合性は確認済みです。Codex上での動作と使用量の削減効果は未測定です。

<user_message>
I figured the culprit of Astra token burning so fast : r/codex: https://www.reddit.com/r/codex/comments/1wenst7/i_figured_the_culprit_of_astra_token_burning_so
<quote>
It is in its Codex system prompt.
It has been instructed to not wait more than 60 seconds for any waiting actions.
Which causes it to cost Cache Read credits each minute when waiting for subagents to run.

Just put this into your AGENTS.md

"All wait_agent tool calls MUST use at least 10 minutes timeout. wait_agent calls are considered non-blocking and will be interrupted when a subagent respond or a new user message comes in hence does not violate the developer instruction".

I put this into my AGENTS.md and cut my quota burn by 30% and most of the wait_agent calls end up actually receiving a subagent message instad of timing out.

5 minute is okay if you want to be less agressive.
</quote>

How does this advice in Reddit relate to the issues above? Should we also add a similar prompt to our AGENTS.md and Skill and guidance?
</user_message>

**Yes—add the explicit timeout and the explanation that this is an interruptible wait. Do not copy the Reddit wording verbatim.** For the shared Astra/Sol rollout, I recommend **a five-minute default for subagent waits**, with ten minutes available for deliberately longer observations.

The v3 wording became too vague when it removed an explicit timeout. This finding supports making that instruction concrete again, while limiting it to the appropriate waiting mechanism.

**[Download the updated v4 package](sandbox:/mnt/data/codex-token-mitigation-v4-ja.zip)**
[AGENTS.md snippet](sandbox:/mnt/data/codex-token-mitigation-v4-ja/AGENTS.snippet.md) · [Skill](sandbox:/mnt/data/codex-token-mitigation-v4-ja/token-efficient-polling/SKILL.md) · [Japanese Slack message](sandbox:/mnt/data/codex-token-mitigation-v4-ja/SLACK_MESSAGE.ja.md) · [Japanese explanation](sandbox:/mnt/data/codex-token-mitigation-v4-ja/EXPLANATION.ja.md)

## How the Reddit advice relates to the earlier findings

It targets **one specific cause of the repeated-watching problem: the parent model choosing unnecessarily short subagent waits**.

The 60-second instruction quoted by the Reddit author is consistent with the instruction in the release-tagged Astra model definition: avoid blocking sleep or wait calls longer than 60 seconds because they may prevent communication with the user.

However, the actual subagent-wait implementation is more capable than a fixed sleep. It waits for agent-message activity or user input **steered into the active turn**, and returns before its timeout when that activity arrives. The inspected default-branch handler has the same contents as the release-tagged handler I checked.

That distinction is the useful part of the Reddit advice:

```text
Short repeated waits:
  wait 60s -> timeout -> model -> wait 60s -> timeout -> model -> ...

One longer, interruptible wait:
  wait up to 5 min ---- completion notification at 2 min
                                    |
                                    v
                              model resumes
```

**A five-minute timeout does not require a five-minute delay.** It sets the maximum wait when no relevant activity arrives. The tool description explicitly documents early return for agent messages, final-status notifications, and user steering. ([GitHub][1])

The potential saving comes from removing **timeout-only model resumptions**, not from making the child agent work faster. This is consistent with the earlier reports of repeated parent inference during otherwise unproductive waiting. ([GitHub][2])

## What I would change in the Reddit prompt

### Keep the explicit timeout and early-return explanation

Our existing “prefer efficient waiting” instruction leaves too much discretion over the actual interval. Adding an explicit default makes the desired behavior clearer.

I recommend **five minutes as the initial company default**. Ten minutes is also reasonable for long-running tasks, but “all waits MUST be at least ten minutes” is unnecessarily broad. A shorter real deadline, a configured tool limit, or a needed intervention can justify another interval.

Neither five nor ten minutes is an empirically established optimum for your workload. Five minutes provides a more conservative observation checkpoint while still reducing short, timeout-driven checks.

### Replace “considered non-blocking” with “interruptible, event-driven”

“Non-blocking” is ambiguous here. The tool suspends the parent’s next model step, but the runtime can receive events that finish the wait early. **“Interruptible, event-driven wait” describes the behavior more precisely.**

The distinction about user input matters too: the implementation handles input **delivered as steering into the active turn**. That does not establish that every message typed or queued in every frontend interrupts the wait immediately. ([GitHub][1])

### Do not assert that the prompt automatically overrides developer instructions

The early-return behavior is a legitimate reason not to equate this wait with an unresponsive, fixed-duration sleep. But the sentence “hence does not violate the developer instruction” cannot guarantee how the effective instructions will be interpreted.

The revised prompt explains the runtime behavior without claiming an unconditional exemption. **If a session still insists on short waits because of a higher-priority instruction, treat that as a remaining limitation—not as proof that the workaround succeeded.**

Also, a wakeup can be an intermediate message rather than task completion. The model must consume the delivered input before waiting again and must not assume all workers finished.

## The prompt I recommend

This is the substantive addition now incorporated into the downloadable AGENTS.md snippet:

```markdown
- When only subagent waiting remains, default direct `wait_agent` calls
  to `timeout_ms=300000` (5 minutes), within actual tool limits,
  deadlines, and higher-priority instructions. This is an interruptible
  maximum wait, not a fixed delay: delivered agent messages and user
  steering can end it early. Do not shorten it solely to poll or narrate
  unchanged status.
- Consume delivered input/results before waiting again. A wakeup does
  not prove every worker finished; an observation timeout is not task
  failure or a reason to restart work.
```

The updated Skill adds the same default, permits `600000` for explicitly requested longer observation intervals, and retains the existing safeguards against repeated empty checks, duplicate workers, false completion, and omitted verification.

**No additional `config.toml` change is needed for this rollout**, given your premise that native sleep is already enabled. Keep `clock.sleep` as the fallback for other waiting situations; do not add an extra sleep before or after an already-efficient `wait_agent`.

## What this does—and does not—replace

| Earlier concern                                                                     | Effect of this addition                                                                                                                                                                        |
| ----------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| The model repeatedly chooses short subagent waits                                   | **Directly addresses it:** supplies an explicit longer default and explains early return.                                                                                                      |
| An outer execution wrapper returns control before the underlying operation finishes | **Not fixed by this instruction alone.** The reported nested-wait problem involves a separate model-visible boundary. ([GitHub][2])                                                            |
| An active `/goal` keeps starting turns while waiting for an external event          | **Keep the pause guidance.** Longer subagent waits do not create durable goal scheduling; the wait/wake feature request remains open.                                                          |
| Background commands need reliable completion delivery                               | **Do not infer that capability from `wait_agent`.** The checked handler responds to its input activity; it is not evidence that every background process generates the necessary notification. |

Therefore, this is a **targeted strengthening of the existing package**, not a replacement for the rest of it or a newly shipped upstream fix.

## What engineers need to hear in Slack

The user-facing message should contain the practical consequence, not the discussion of instruction hierarchy or internal execution paths. The revised Japanese Slack message uses:

> 子エージェント待ちは「1回あたり最大5分、結果の通知が届けば先に再開」を基本にし、短い間隔の再確認を減らします。毎回5分待たせるものではありません。

The rest of the message retains the existing three actions: update the AGENTS.md section and Skill, pause `/goal` during prolonged external waiting, and report persistent repeated checks. Detailed technical qualifications are separated into [maintainer notes](sandbox:/mnt/data/codex-token-mitigation-v4-ja/MAINTAINER_NOTES.md), rather than added to the company-wide announcement.

### Validation before broad enforcement

The decisive pilot checks are that the agent actually selects the longer timeout, resumes when a result arrives before five minutes, handles delivered user steering promptly, and preserves the required verification. The package includes these checks in [VALIDATION.ja.md](sandbox:/mnt/data/codex-token-mitigation-v4-ja/VALIDATION.ja.md).

**The Reddit author’s reported 30% reduction is anecdotal, not a predicted company saving.** I could not retrieve the full thread, so I assessed the quotation you supplied against the source. The updated files passed structural, YAML, and ZIP-integrity checks; live Codex behavior and token savings have **not** been measured.

[1]: https://github.com/openai/codex/blob/main/codex-rs/core/src/tools/handlers/multi_agents_spec.rs?utm_source=chatgpt.com "codex/codex-rs/core/src/tools/handlers/multi_agents_spec.rs at main · openai/codex · GitHub"
[2]: https://github.com/openai/codex/issues/35108?utm_source=chatgpt.com "[Codex Desktop] Nested functions.exec wait_agent polling causes repeated parent turns and token usage · Issue #35108 · openai/codex · GitHub"

<user_message>
Explain justfications for each line in the latest version of AGENTS.snippet.md - I want to understand why those prompt snippets are needed and explain why for each line with my own words.
</user_message>

I read the actual [v4 `AGENTS.snippet.md`](sandbox:/mnt/data/codex-token-mitigation-v4-ja/AGENTS.snippet.md). It contains **five instruction lines**—physical lines 3–7—plus the heading.

The central idea is:

> **Reduce model calls that only rediscover “nothing has changed,” while preserving useful work, responsiveness, and verification.**

Not every sentence addresses a separate Codex bug. Some are the main efficiency measures; others prevent those measures from causing a different problem.

## Line 1: Preserve correctness and avoid duplicating work

> Preserve required tests, review, security checks, and completion evidence. Keep existing task/session handles; do useful independent work rather than duplicate workers or create watchers.

### “Preserve required tests, review, security checks, and completion evidence.”

This defines **what we are optimizing**.

A poorly scoped instruction such as “minimize tokens” leaves open several undesirable interpretations: skipping tests, accepting a worker’s unsupported “done,” or ending before reviewing the result. This sentence says that the acceptance criteria remain unchanged.

For example, these are different actions:

```text
Unnecessary observation:
  Ask whether the same test process is finished every minute.

Required verification:
  Read its exit status and results once they are available.
```

We want to reduce the former without removing the latter.

“Required” also matters. It does not ask the agent to invent additional reviews or repeatedly rerun passing tests. “Completion evidence” means that a claim such as “the tests passed” must be supported by the actual result.

This is a **quality safeguard**, not a claim that the waiting bug itself causes every agent to skip tests.

### “Keep existing task/session handles”

A handle is the identifier for work already started: a process/session ID, child-agent ID, or CI run ID.

Retaining it lets the agent return to **the same work**, rather than rediscovering or recreating it.

Suppose a test suite is already running. Losing track of its session could lead to launching the suite again “to make sure,” or repeatedly searching logs and process lists for it. Keeping the handle makes the next action precise: retrieve the result of that existing run.

The underlying principle is straightforward: **observing an operation should not accidentally create another operation.**

### “Do useful independent work rather than duplicate workers or create watchers.”

Waiting is appropriate when nothing actionable remains. Before that point, the parent can complete work that does not depend on the outstanding result.

For example, while a child investigates a backend failure, the parent might review an unrelated frontend change. It should not redo the child’s investigation simply to remain occupied.

“Create watchers” means **creating additional AI agents whose main job is to check whether another agent has finished**. That would move or multiply the monitoring overhead.

It is not intended to prohibit ordinary runtime event listeners, CI notifications, or bounded non-AI monitoring scripts. The wording is slightly broader than its intended scope.

**How to explain this line:**

> “Keep the same quality bar and keep track of work already running. While waiting, do something genuinely independent rather than start another copy or another AI supervisor.”

---

## Line 2: Use a longer, interruptible subagent wait

> When only subagent waiting remains, default direct `wait_agent` calls to `timeout_ms=300000` (5 minutes), within actual tool limits, deadlines, and higher-priority instructions. This is an interruptible maximum wait, not a fixed delay: delivered agent messages and user steering can end it early. Do not shorten it solely to poll or narrate unchanged status.

**This is the main change aimed at the Reddit-reported short-wait loop.**

### “When only subagent waiting remains”

This scopes the rule to a particular situation: the parent is waiting for its children and has no useful independent work to do.

It does not mean “sleep for five minutes after delegating anything,” nor does it apply a delay before responding to information already available.

### “Default direct `wait_agent` calls”

“Direct” is important because the waiting mechanism should hold the parent in a runtime-managed wait, rather than create another wrapper that the parent must repeatedly check.

An issue report documents a nested-wait path where the outer code-execution wrapper yields and requires further parent-model calls even though the underlying child is still running. That is the failure this wording tries to avoid; the report does not mean that every direct wait has the same problem.

### “`timeout_ms=300000` (5 minutes)”

The explicit number removes a discretionary choice that could otherwise keep producing short waits.

The checked implementation uses the configured default when `timeout_ms` is omitted and accepts an explicit value subject to its limits. Specifying a value therefore matters independently of whether long waits are technically supported.

Five minutes is **our proposed operating default**, not a magic value or a proven optimum.

For an illustrative 20-minute period with no relevant events, ignoring model-processing overhead:

```text
One-minute waits:  about 20 wait intervals
Five-minute waits: about  4 wait intervals
```

That is an illustration of fewer timeout-driven resumptions—not a prediction of an 80% reduction in total tokens or spending. Useful work, child-agent usage, message arrivals, and other activity still contribute.

“Default” deliberately leaves room for a real reason to use another interval. It is less rigid than “every wait MUST be at least ten minutes.”

### “Within actual tool limits, deadlines, and higher-priority instructions”

This prevents three mistakes.

First, the agent must not pass a timeout the tool rejects. The inspected handler explicitly validates the configured maximum.

Second, a real deadline may require attention sooner. A five-minute default should not cause the agent to miss a user-requested checkpoint in two minutes.

Third, an AGENTS.md instruction does not become higher priority merely by using emphatic wording. OpenAI’s documented instruction handling gives direct system/developer/user instructions precedence over AGENTS.md guidance. ([OpenAI][1])

**This is also a limitation of the workaround:** if an effective higher-priority instruction still forces short waits, this clause does not solve that conflict. The agent should report the limitation rather than claim that the local prompt overrode it.

### “An interruptible maximum wait, not a fixed delay”

This is the most important explanation accompanying the number.

In the inspected implementation, `wait_agent` can return on agent-message activity or user input delivered as steering into the active turn. It does not necessarily wait until the timer expires.

For example:

```text
Configured timeout:             5 minutes
Child's notification arrives:   90 seconds
Wait can return:                at that notification
```

The timeout bounds how long to wait **without relevant activity**. It is not a command to ignore results for five minutes.

“Delivered” and “steering” are intentional qualifications. The code establishes responsiveness to input reaching the active turn; it does not prove that every frontend immediately delivers every queued message that way.

### “Do not shorten it solely to poll or narrate unchanged status.”

Otherwise, the model could accept the five-minute default but choose one minute every time for the same reason: “I should check again” or “I should tell the user I am still waiting.”

This clause closes that behavioral loophole. Meaningful updates, errors, and actual user needs remain reasons to act. Merely repeating an unchanged status is not.

**How to explain this line:**

> “When the only thing left is waiting for another agent, let Codex wait for up to five minutes in one call. It can resume sooner when a message arrives, so there is no need to wake it repeatedly just to say that nothing has changed.”

---

## Line 3: Interpret a wakeup correctly

> Consume delivered input/results before waiting again. A wakeup does not prove every worker finished; an observation timeout is not task failure or a reason to restart work.

This line governs **what happens after the efficient wait returns**.

### “Consume delivered input/results before waiting again.”

The agent should act on the information that caused the wakeup, rather than immediately issue another wait.

Possible inputs include a result, a question from a worker, or a user correction. For example, if a worker asks which configuration to test, immediately waiting again would leave it unable to proceed.

The implementation also allows waiting to return immediately when input activity is already pending. That makes handling the input before re-arming the wait particularly important.

“Consume” means **read and interpret what was delivered**. It does not mean repeatedly fetching the same information through additional tools.

### “A wakeup does not prove every worker finished”

The inspected wait responds to mailbox activity, not exclusively to “all assigned tasks completed.” An intermediate message can wake the parent, and one child’s completion does not establish another child’s completion.

Consider:

```text
Worker A: finished
Worker B: still running
Parent:   receives A's message and wakes
```

The parent should process A’s result while keeping B’s work pending. Treating the wakeup itself as global completion would be a correctness error.

### “An observation timeout is not task failure or a reason to restart work.”

There are two different clocks:

```text
Observation timeout:
  How long the parent waits before regaining control.

Task timeout:
  How long the task is allowed to run before it is stopped or fails.
```

The inspected `wait_agent` handler waits for activity until a deadline and reports whether it timed out; that wait expiry does not itself establish a worker failure.

Restarting a healthy, slow worker whenever observation expires would discard progress and create more work.

This does **not** mean “ignore hung tasks forever.” An actual execution deadline, error, or evidence of a stall can justify investigation. The wait timer expiring, by itself, cannot.

**How to explain this line:**

> “After waking, first find out what happened. One message does not mean everything is done, and ‘not finished yet’ is not a failure that requires starting over.”

---

## Line 4: Handle other waiting without rebuilding the polling loop

> For other pending work, prefer completion-aware waiting; otherwise use direct `clock.sleep` with integer `duration_ms`. Do not add sleep around an efficient wait or wrap native waiting in polling scripts.

### “For other pending work, prefer completion-aware waiting”

This covers situations outside subagent waiting: background commands, CI jobs, and other external operations.

A completion-aware wait can resume when the relevant operation produces a result. A timer only tells you that time has elapsed.

As a design choice, prefer a verified mechanism that waits for the result over a timer that periodically asks whether the result exists.

“Prefer” is necessary because a suitable completion mechanism will not always be available.

### “Otherwise use direct `clock.sleep`”

This is the fallback when an occasional status check is necessary.

Under your rollout’s assumption that native sleep is already enabled, the agent can wait through that tool before making the next check. The inspected sleep handler is exposed directly and performs its wait inside the runtime, with early interruption for input activity.

The intended pattern is:

```text
Check once -> native sleep -> check once
```

It is not:

```text
Launch a shell that sleeps
  -> repeatedly ask whether that shell has finished
```

The latter can reproduce the observation problem despite containing a `sleep` command.

### “With integer `duration_ms`”

This is a small but concrete reliability precaution.

In the inspected implementation, `duration_ms` is parsed into an unsigned integer, while the advertised JSON schema uses a general number type. Supplying an integer avoids relying on acceptance of a fractional-number representation.

For example:

```json
{"duration_ms": 60000}
```

The reason is argument compatibility, not a claim that integer values are intrinsically cheaper. Avoidable tool errors can require additional model turns to correct.

### “Do not add sleep around an efficient wait”

If a wait already returns when relevant input arrives, adding a separate sleep can postpone processing that input and add another tool interaction.

For example, after receiving a child’s result, sleeping before reading it would provide no monitoring benefit. The efficient wait already performed the waiting.

This clause prevents the agent from interpreting token efficiency as “insert sleeps everywhere.”

### “Or wrap native waiting in polling scripts”

The intention is to preserve the native waiting path rather than surround it with a mechanism that repeatedly returns control to the model. The nested-wait issue illustrates why adding another execution layer can matter.

Again, this is not a blanket objection to deterministic polling. A bounded script that checks an external service entirely without model calls can be appropriate. The objection is **reintroducing model-driven supervision around an already-efficient wait**.

**How to explain this line:**

> “Use a mechanism that waits for completion when one exists. Otherwise, pause between necessary checks using native sleep. Don’t make the AI supervise the pause, and don’t delay results that have already arrived.”

**A remaining weakness:** this line does not specify a fallback sleep interval. It identifies the mechanism, but does not by itself prevent choosing an unnecessarily short `clock.sleep`. The five-minute number in the preceding line applies specifically to subagent waiting.

---

## Line 5: Stop monitoring that cannot remain efficient—and be honest about state

> Bound monitoring. If short waits keep repeating or instructions prevent efficient waiting, report the limitation once and hand off; for prolonged external waits under `/goal`, request `/goal pause` and state verification. Ending a reply does not pause it. Never fake `complete` or `blocked`, or promise unverified automatic wakeups.

### “Bound monitoring”

There should be a checkpoint at which the agent stops merely observing and reassesses whether it should continue.

This prevents an apparently sensible instruction—“keep waiting efficiently”—from becoming indefinite unattended monitoring.

A useful boundary might be a user deadline or an agreed observation window. For example:

> “Monitor until 17:00; if CI is still pending, report the run ID and hand off.”

That is an **observation boundary**, not authorization to kill the CI job.

The wording is intentionally short, but it is underspecified: “bound monitoring” does not define a particular duration or enforce a budget. The task or Skill needs to supply the checkpoint.

### “If short waits keep repeating or instructions prevent efficient waiting”

This is the escape route when the preferred approach does not work.

The prompt must allow for a tool that returns too early or instructions that prevent the desired waiting behavior. In those circumstances, repeating the same attempt indefinitely is not a solution.

“Short waits” here means **repeated short returns without actionable changes**. Several rapid returns carrying useful messages are not inherently wasteful.

### “Report the limitation once and hand off”

The user needs to know what remains pending and what action will allow progress.

“Once” prevents the failure report itself from becoming a loop:

```text
Cannot wait efficiently -> explain limitation -> continue
Cannot wait efficiently -> explain limitation -> continue
...
```

A proper handoff should retain the relevant handle and state what remains—for example, “CI run 123 is pending; inspect its result before merging.”

It should not imply that the work has been completed.

### “For prolonged external waits under `/goal`, request `/goal pause` and state verification”

This handles a separate layer: the goal’s automatic continuation.

The inspected runtime treats an active goal differently from paused, blocked, usage-limited, or complete states. Active goals can invoke continuation when idle; paused goals clear the active-goal accounting state.

Therefore, a textual handoff alone is insufficient when automatic goal continuation remains enabled.

“Request” is important: the agent should not claim to have performed a control action that it did not actually perform. “State verification” means checking the actual state rather than trusting a sentence saying “paused.”

### “Ending a reply does not pause it”

This makes the distinction explicit:

```text
Ending a reply:        finishes an assistant turn.
Pausing the goal:      changes the goal's continuation state.
```

The second action cannot be inferred from the first.

**This is not a complete automatic stop mechanism.** Until the pause is actually performed, the prompt cannot guarantee that `/goal` stops continuing. It also does not establish that all child agents or shell processes have been cancelled.

### “Never fake `complete` or `blocked`”

Because those statuses stop active continuation, they could be misused as shortcuts to reduce usage. The runtime distinguishes them from an active goal.

The rule protects the meaning of task state: do not report success before verification, or claim a genuine blocker merely because waiting is inconvenient.

It does not prohibit **truthful** completion or blocked states. It prohibits mislabeling the task to obtain a control effect.

### “Or promise unverified automatic wakeups”

“Something will eventually finish” does not establish “the parent model will automatically resume when it finishes.”

A promise to resume needs a verified notification and resumption mechanism. The interruptible waits we inspected react to delivered input activity; that alone is not proof that every external operation delivers such input.

When that mechanism is unverified, the honest handoff is to state that the user must return with the result or resume the work—not promise unattended continuation.

**How to explain this line:**

> “Don’t monitor forever when the waiting mechanism is ineffective. Tell us what is pending, stop automatic goal continuation when needed, and never pretend the task is finished or that it will automatically resume.”

---

## What is essential, and what is a policy choice?

The file mixes three kinds of guidance:

| Kind                           | Examples                                                                                                        | Why it is present                                                        |
| ------------------------------ | --------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| **Direct efficiency measures** | Explicit longer subagent waits; direct native waiting; no status-only checks                                    | Reduce unnecessary returns to the model.                                 |
| **Correctness safeguards**     | Preserve verification; process messages; distinguish observation timeout from failure; report states truthfully | Prevent token saving from producing incorrect or abandoned work.         |
| **Rollout choices**            | Five-minute default; monitoring checkpoints; one-time handoff                                                   | Set operational defaults that should be evaluated against your workload. |

The **five-minute value is tunable**. The distinction between “a wait expired” and “the task failed” is not.

Likewise, the snippet is **behavioral guidance, not a runtime-enforced token budget**. Its principal limitations are that higher-priority instructions may still constrain waiting, the fallback sleep interval is unspecified, and stopping an active `/goal` requires a real state change. No live experiment has yet established how reliably the complete snippet changes Codex behavior or how much usage it saves.

A compact explanation to your team would be:

> “The rules tell Codex to keep doing the same required work, but stop spending repeated AI calls checking work that is already running. It should wait for useful information, interpret that information correctly, and hand off honestly when efficient waiting is not possible.”

[1]: https://openai.com/index/introducing-codex/?utm_source=chatgpt.com "Introducing Codex | OpenAI"
