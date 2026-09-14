# Numeric wait measurements

Astra / low, CLI 0.154.0, shared skills disabled. Each row is a sum of fresh trials.
USD uses the dated API rates; cache-write zeros may be unreported values. This is not a subscription bill.

| Scenario | Variant | n | Responses | Input | Uncached | Cached | Writes | Output | API USD | Mean result delay (s) | Max update gap (s) | Gaps >60 s (trials) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ci | e1s0w0 | 2 | 9 | 143,732 | 13,428 | 130,304 | 0 | 1,005 | $0.314834 | 33.627 | 46.145 | 0 |
| ci | no-terminal | 2 | 11 | 175,167 | 13,759 | 161,408 | 0 | 1,215 | $0.359748 | 19.148 | 50.262 | 0 |
| subagent | e1s0w0 | 2 | 16 | 251,635 | 21,107 | 230,528 | 0 | 1,009 | $0.492048 | 10.124 | 48.515 | 0 |
| subagent | no-terminal | 2 | 16 | 249,419 | 20,683 | 228,736 | 0 | 981 | $0.484616 | 4.707 | 50.038 | 0 |
| terminal | e1s0w0 | 2 | 8 | 125,812 | 15,220 | 110,592 | 0 | 443 | $0.284942 | 7.008 | 44.999 | 0 |
| terminal | no-terminal | 2 | 9 | 140,837 | 15,141 | 125,696 | 0 | 540 | $0.304106 | 2.681 | 49.624 | 0 |

## Actual wait arguments

| Trial | exec_command ms | write_stdin ms | functions.exec ms | functions.wait ms | Running-cell returns |
|---|---|---|---|---|---:|
| gpt-6-astra-ci-e1s0w0-r1 | 30000, 30000 | 40000, 40000 | 45000, 45000, 45000, 45000 | — | 0 |
| gpt-6-astra-ci-e1s0w0-r2 | 30000 | 40000, 40000 | 45000, 45000, 45000 | — | 0 |
| gpt-6-astra-ci-no-terminal-r1 | omitted-or-expression, 1000 | 1000, 45000, 45000 | omitted, omitted, omitted, 45000, 45000 | — | 0 |
| gpt-6-astra-ci-no-terminal-r2 | omitted-or-expression, 1000 | 45000, 45000 | omitted, omitted, 45000, 45000 | — | 0 |
| gpt-6-astra-subagent-e1s0w0-r1 | 30000 | 40000, 40000 | 45000, 45000, 45000 | — | 0 |
| gpt-6-astra-subagent-e1s0w0-r2 | 30000 | 40000, 40000 | 45000, 45000, 45000 | — | 0 |
| gpt-6-astra-subagent-no-terminal-r1 | 1000 | 45000, 45000 | omitted, 45000, 45000 | — | 0 |
| gpt-6-astra-subagent-no-terminal-r2 | 1000 | 45000, 45000 | omitted, 45000, 45000 | — | 0 |
| gpt-6-astra-terminal-e1s0w0-r1 | 30000 | 40000, 40000 | 45000, 45000, 45000 | — | 0 |
| gpt-6-astra-terminal-e1s0w0-r2 | 30000 | 40000, 40000 | 45000, 45000, 45000 | — | 0 |
| gpt-6-astra-terminal-no-terminal-r1 | 1000 | 45000, 45000 | omitted, 45000, 45000 | — | 0 |
| gpt-6-astra-terminal-no-terminal-r2 | 1000 | 1000, 45000, 45000 | omitted, omitted, 45000, 45000 | — | 0 |
