# Numeric wait measurements

Astra / low, CLI 0.154.0, shared skills disabled. Each row is a sum of fresh trials.
USD uses the dated API rates; cache-write zeros may be unreported values. This is not a subscription bill.

| Scenario | Variant | n | Responses | Input | Uncached | Cached | Writes | Output | API USD | Mean result delay (s) | Max update gap (s) | Gaps >60 s (trials) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| cell | e1s0w0 | 3 | 13 | 205,854 | 20,254 | 185,600 | 0 | 739 | $0.425090 | 4.390 | 45.776 | 0 |
| cell | e1s0w1 | 3 | 13 | 205,623 | 40,631 | 164,992 | 0 | 729 | $0.607752 | 4.623 | 44.389 | 0 |
| terminal | e0s0w0 | 3 | 9 | 140,993 | 21,953 | 119,040 | 0 | 453 | $0.361220 | 3.343 | 44.960 | 0 |
| terminal | e0s1w0 | 3 | 11 | 172,833 | 27,809 | 145,024 | 0 | 575 | $0.451864 | 5.275 | 43.841 | 0 |
| terminal | e1s0w0 | 3 | 9 | 140,957 | 21,661 | 119,296 | 0 | 452 | $0.358506 | 3.002 | 44.799 | 0 |
| terminal | e1s1w0 | 3 | 11 | 172,935 | 16,007 | 156,928 | 0 | 575 | $0.345748 | 5.250 | 46.163 | 0 |

## Actual wait arguments

| Trial | exec_command ms | write_stdin ms | functions.exec ms | functions.wait ms | Running-cell returns |
|---|---|---|---|---|---:|
| gpt-6-astra-cell-e1s0w0-r1 | 30000 | 40000 | 1, 45000 | 45000 | 1 |
| gpt-6-astra-cell-e1s0w0-r2 | 30000 | 40000, 40000 | 1, 45000, 45000 | 45000 | 1 |
| gpt-6-astra-cell-e1s0w0-r3 | 30000 | 40000 | 1, 45000 | 45000 | 1 |
| gpt-6-astra-cell-e1s0w1-r1 | 30000 | 40000, 40000 | 1, 45000, 45000 | 45000 | 1 |
| gpt-6-astra-cell-e1s0w1-r2 | 30000 | 40000 | 1, 45000 | 45000 | 1 |
| gpt-6-astra-cell-e1s0w1-r3 | 30000 | 40000 | 1, 45000 | 45000 | 1 |
| gpt-6-astra-terminal-e0s0w0-r1 | 30000 | 44000 | 45000, 45000 | — | 0 |
| gpt-6-astra-terminal-e0s0w0-r2 | 30000 | 44000 | 45000, 45000 | — | 0 |
| gpt-6-astra-terminal-e0s0w0-r3 | 30000 | 44000 | 45000, 45000 | — | 0 |
| gpt-6-astra-terminal-e0s1w0-r1 | 30000 | 40000 | 45000, 45000 | — | 0 |
| gpt-6-astra-terminal-e0s1w0-r2 | 30000 | 40000, 40000 | 45000, 45000, 45000 | — | 0 |
| gpt-6-astra-terminal-e0s1w0-r3 | 30000 | 40000, 40000 | 45000, 45000, 45000 | — | 0 |
| gpt-6-astra-terminal-e1s0w0-r1 | 30000 | 40000 | 45000, 45000 | — | 0 |
| gpt-6-astra-terminal-e1s0w0-r2 | 30000 | 40000 | 45000, 45000 | — | 0 |
| gpt-6-astra-terminal-e1s0w0-r3 | 30000 | 40000 | 45000, 45000 | — | 0 |
| gpt-6-astra-terminal-e1s1w0-r1 | 30000 | 40000, 40000 | 45000, 45000, 45000 | — | 0 |
| gpt-6-astra-terminal-e1s1w0-r2 | 30000 | 40000 | 45000, 45000 | — | 0 |
| gpt-6-astra-terminal-e1s1w0-r3 | 30000 | 40000, 40000 | 45000, 45000, 45000 | — | 0 |
