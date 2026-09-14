# Numeric wait measurements

Astra / low, CLI 0.154.0, shared skills disabled. Each row is a sum of fresh trials.
USD uses the dated API rates; cache-write zeros may be unreported values. This is not a subscription bill.

| Scenario | Variant | n | Responses | Input | Uncached | Cached | Writes | Output | API USD | Mean result delay (s) | Max update gap (s) | Gaps >60 s (trials) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| subagent | e1s0w0 | 2 | 15 | 235,348 | 24,276 | 211,072 | 0 | 755 | $0.491582 | 8.318 | 49.898 | 0 |
| subagent | outer-o0n0 | 2 | 14 | 219,358 | 29,150 | 190,208 | 0 | 707 | $0.517058 | 5.663 | 48.771 | 0 |

## Actual wait arguments

| Trial | exec_command ms | write_stdin ms | functions.exec ms | functions.wait ms | Running-cell returns |
|---|---|---|---|---|---:|
| gpt-6-astra-subagent-e1s0w0-r1 | 30000 | 40000, 40000 | 45000, 45000, 45000 | — | 0 |
| gpt-6-astra-subagent-e1s0w0-r2 | 30000 | 40000 | 45000, 45000 | — | 0 |
| gpt-6-astra-subagent-outer-o0n0-r1 | 30000 | 44000 | 31000, 45000 | — | 0 |
| gpt-6-astra-subagent-outer-o0n0-r2 | 30000 | 44000 | 31000, 45000 | — | 0 |
