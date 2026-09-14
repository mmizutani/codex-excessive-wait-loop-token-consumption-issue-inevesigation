---
name: codex-wait-efficiently
description: Reduce unnecessary model calls in Codex when awaiting subagent results, starting long terminal commands, or monitoring CI and external jobs that remain in progress.
---

# Efficient waiting in Codex

## Across all waits

Follow higher-priority instructions; do useful independent work first. When only waiting remains, put any required brief progress update in the same response before each blocking wait. For a 60-second update cadence, cap waits and wrapper yields at 45 seconds; shorten for tool limits or actionable deadlines. Use integer milliseconds. Updates alone do not justify status queries.

Longer waits may not reduce usage; add no cache-only keepalives without measured savings.

## Subagent results

When delegating work that includes waiting, include `Use $codex-wait-efficiently` in the child's task.

When only subagent results remain, prefer direct `wait_agent` with `timeout_ms` within that budget.

## Terminal commands

When only command completion remains, start `exec_command` with a long `yield_time_ms` within tool limits and the budget. Retain its session; use empty `write_stdin` waits within budget, without preliminary short polls.

In Code Mode, set the outer `functions.exec` wait long enough to cover the inner `exec_command` or `write_stdin` wait plus a small margin, while staying within budget. If `functions.exec` returns a running cell, wait for that same cell with `functions.wait` using `yield_time_ms` within budget instead of 1-second/default checks; finish the cell before calling `write_stdin` again.

## CI and external work

Retain job identity; prefer completion notifications. Otherwise, keep repeated scriptable checks inside one shell watcher, bounded by time or total check count, including any initial query in the user's limit. Apply the Terminal commands rules to that watcher and retain its session; emit only meaningful changes. Choose intervals for acceptable result delay; back off unchanged status.

If a watcher is impractical, use direct `clock.sleep` when available between useful checks. Do not add sleep around event-aware waits or assume it wakes on shell or CI completion.

## Results and goal state

Process results promptly; preserve required verification. Observation timeouts are not task failures.

If an active `/goal` would only wait on a prolonged external dependency, ask once about pausing; verify its state before treating it as paused. A final reply does not pause it. Never mark unfinished work complete or invent blockers to stop usage.
