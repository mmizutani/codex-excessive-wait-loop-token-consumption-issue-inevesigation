## Token-efficient waiting

- Preserve required tests, review, security checks, and completion evidence. Keep existing task/session handles; do useful independent work rather than duplicate workers or create watchers.
- When only subagent waiting remains, default direct `wait_agent` calls to `timeout_ms=300000` (5 minutes), within actual tool limits, deadlines, and higher-priority instructions. This is an interruptible maximum wait, not a fixed delay: delivered agent messages and user steering can end it early. Do not shorten it solely to poll or narrate unchanged status.
- Consume delivered input/results before waiting again. A wakeup does not prove every worker finished; an observation timeout is not task failure or a reason to restart work.
- For other pending work, prefer completion-aware waiting; otherwise use direct `clock.sleep` with integer `duration_ms`. Do not add sleep around an efficient wait or wrap native waiting in polling scripts.
- Bound monitoring. If short waits keep repeating or instructions prevent efficient waiting, report the limitation once and hand off; for prolonged external waits under `/goal`, request `/goal pause` and state verification. Ending a reply does not pause it. Never fake `complete` or `blocked`, or promise unverified automatic wakeups.
