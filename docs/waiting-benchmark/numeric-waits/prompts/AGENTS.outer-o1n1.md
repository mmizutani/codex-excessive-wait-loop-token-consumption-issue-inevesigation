## Waiting for work

### Across all waits

Follow higher-priority instructions; do useful independent work first. When only waiting remains, put any required brief progress update in the same response before each blocking wait. For a 60-second update cadence, cap waits and wrapper yields at 45 seconds; shorten for tool limits or actionable deadlines. Use integer milliseconds. Updates alone do not justify status queries.

Longer waits may not reduce usage; add no cache-only keepalives without measured savings.

### Subagent results

When only subagent results remain, prefer direct `wait_agent` with `timeout_ms` within that budget.

### Terminal commands

When only command completion remains, start `exec_command` with a long `yield_time_ms` within tool limits and the budget. Retain its session; use empty `write_stdin` waits within budget, without preliminary short polls.

In code mode, set `functions.exec`'s first-line `// @exec: {"yield_time_ms": 45000}`, adjusted to budget, covering the inner wait plus a small margin. Resume running cells with `functions.wait` within budget instead of 1-second/default checks; finish the cell before polling the process again.

### CI and external work

Retain job identity; prefer completion notifications. Otherwise, if scriptable, use one shell watcher with an explicit time or check-count limit, retain its session, and emit only meaningful changes. Choose intervals for acceptable result delay; back off unchanged status.

If a watcher is impractical, use direct `clock.sleep` when available between useful checks. Do not add sleep around event-aware waits or assume it wakes on shell or CI completion.

### Results and goal state

Process results promptly; preserve required verification. Observation timeouts are not task failures.

If an active `/goal` would only wait on a prolonged external dependency, ask once about pausing; verify its state before treating it as paused. A final reply does not pause it. Never mark unfinished work complete or invent blockers to stop usage.
