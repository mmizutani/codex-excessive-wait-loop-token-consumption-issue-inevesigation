# v4: rationale for the explicit subagent wait timeout

Checked: 2026-09-13. Audience: rollout maintainers, not the main Slack announcement.

## Decision

Adopt the useful part of the supplied Reddit advice: an explicit five-minute default for direct, interruptible subagent waiting, plus a short explanation that the timeout is an upper bound rather than a compulsory delay. Ten minutes remains an optional interval for explicitly requested longer observations. Neither value is empirically established as optimal in this rollout.

Do not adopt a mandatory ten-minute minimum for every waiting action, a claim that all user messages interrupt every wait, or a declaration that the local prompt cannot conflict with developer instructions.

## What the source establishes

The tagged `rust-v0.154.0` v2 wait handler accepts an optional integer `timeout_ms`. It validates against the configured maximum, applies the configured minimum, and uses the configured default when omitted. It awaits input-queue activity using an asynchronous timeout. Mailbox activity and user steering return early; existing pending activity can return immediately. A wakeup is therefore not proof of child completion, let alone completion of all children.

https://github.com/openai/codex/blob/rust-v0.154.0/codex-rs/core/src/tools/handlers/multi_agents_v2/wait.rs

The same handler was returned with the identical blob SHA `d2f92feb8d011bb468dcc1f81b0efc20e756179e` at the inspected default-branch snapshot:

https://github.com/openai/codex/blob/1715e55076737158ba61d43158ede504de6d4ce1/codex-rs/core/src/tools/handlers/multi_agents_v2/wait.rs

The tool description also explicitly refers to mailbox updates, final-status notifications, and user input steered into the active turn:

https://github.com/openai/codex/blob/1715e55076737158ba61d43158ede504de6d4ce1/codex-rs/core/src/tools/handlers/multi_agents_spec.rs

This supports calling it an **interruptible, event-driven runtime wait**. It suspends the parent's next model step; it need not freeze the application's input handling. An ordinary UI-queued message that has not been delivered as active-turn steering is not the same event. Runtime support is not a guarantee that every frontend routes input identically.

## Why the earlier guidance needed refinement

v3 said to choose useful intervals but removed numeric defaults. This left the model free to choose short waits for routine commentary even on a notification-aware path. v4 gives an explicit default scoped to subagent waiting and explains early return.

The tagged model instruction includes a warning against blocking waits longer than 60 seconds because of communication responsiveness. The runtime's early-return behavior makes a blanket assumption that a five-minute timeout necessarily prevents user interaction inaccurate. However, the source does not establish that a model will always interpret that warning narrowly. The prompt therefore states the behavior without asserting that it overrides higher-priority instructions. Persistent short waits or an instruction conflict are pilot failures to report, not something to hide through terminology.

https://github.com/openai/codex/blob/rust-v0.154.0/codex-rs/models-manager/models.json

## Relationship to other issues

Longer direct subagent waiting reduces timeout-only parent resumptions. It does not fix a generic code wrapper that yields early, add background-shell completion delivery, or create a durable goal scheduler. `clock.sleep` remains the fallback for other waits, not an extra sleep around `wait_agent`.

https://github.com/openai/codex/issues/35108
https://github.com/openai/codex/issues/28144
https://github.com/openai/codex/pull/34969
https://github.com/openai/codex/pull/41243

The proposed higher default in issue #36379 is corroborating discussion, not proof of a shipped default change. Its closed state was previously checked as a wrong-repository/downstream closure; this version does not claim that the default was changed upstream.

https://github.com/openai/codex/issues/36379

## Savings and evidence limits

The Reddit post could not be retrieved in this session; its text was supplied by the user. The reported 30% quota reduction is an anecdote, not a company forecast or a controlled benchmark.

https://www.reddit.com/r/codex/comments/1wenst7/i_figured_the_culprit_of_astra_token_burning_so/

For a hypothetical 20-minute interval with no delivered input, re-arming waits gives approximately 20 one-minute, 4 five-minute, or 2 ten-minute intervals. This is arithmetic about observation frequency, not a prediction of total tokens, credits, or bills. Real work, cached inputs, messages, and child-agent usage must be accounted for separately.

No model-behavior test or live token benchmark was run. The package is a source-informed pilot candidate, not a verified upstream fix. Validate early completion, delivered steering, actual timeout selection, and task quality before broad enforcement.
