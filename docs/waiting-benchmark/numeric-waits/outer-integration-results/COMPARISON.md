# Numeric wait measurements

Astra / low, CLI 0.154.0, shared skills disabled. Each row is a sum of fresh trials.
USD uses the dated API rates; cache-write zeros may be unreported values. This is not a subscription bill.

| Scenario | Variant | n | Responses | Input | Uncached | Cached | Writes | Output | API USD | Mean result delay (s) | Max update gap (s) | Gaps >60 s (trials) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ci | e1s0w0 | 2 | 8 | 127,254 | 16,662 | 110,592 | 0 | 916 | $0.323012 | 11.633 | 45.648 | 0 |
| ci | outer-o0n1 | 2 | 10 | 159,912 | 27,944 | 131,968 | 0 | 1,104 | $0.466608 | 32.494 | 49.837 | 0 |
| subagent | e1s0w0 | 2 | 16 | 251,823 | 21,295 | 230,528 | 0 | 1,122 | $0.499578 | 9.099 | 48.134 | 0 |
| subagent | outer-o0n1 | 2 | 8 | 125,445 | 15,493 | 109,952 | 0 | 642 | $0.296982 | 8.265 | 48.175 | 0 |
| terminal | e1s0w0 | 2 | 7 | 109,873 | 14,897 | 94,976 | 0 | 377 | $0.262796 | 4.958 | 45.133 | 0 |
| terminal | outer-o0n1 | 2 | 6 | 93,976 | 14,616 | 79,360 | 0 | 306 | $0.240820 | 2.084 | 43.852 | 0 |

## Actual wait arguments

| Trial | exec_command ms | write_stdin ms | functions.exec ms | functions.wait ms | Running-cell returns |
|---|---|---|---|---|---:|
| gpt-6-astra-ci-e1s0w0-r1 | 30000, 30000 | 40000 | 45000, 45000, 45000 | — | 0 |
| gpt-6-astra-ci-e1s0w0-r2 | 30000 | 40000, 40000 | 45000, 45000, 45000 | — | 0 |
| gpt-6-astra-ci-outer-o0n1-r1 | 1000, 30000 | 43000, 43000 | 1000, 32000, 45000, 45000 | — | 0 |
| gpt-6-astra-ci-outer-o0n1-r2 | 30000, 30000 | 44000, 44000 | 35000, 35000, 45000, 45000 | — | 0 |
| gpt-6-astra-subagent-e1s0w0-r1 | 30000 | 40000, 40000 | 45000, 45000, 45000 | — | 0 |
| gpt-6-astra-subagent-e1s0w0-r2 | 30000 | 40000, 40000 | 45000, 45000, 45000 | — | 0 |
| gpt-6-astra-subagent-outer-o0n1-r1 | 30000 | 44000 | 31000, 45000 | — | 0 |
| gpt-6-astra-subagent-outer-o0n1-r2 | — | — | — | — | 0 |
| gpt-6-astra-terminal-e1s0w0-r1 | 30000 | 40000, 40000 | 45000, 45000, 45000 | — | 0 |
| gpt-6-astra-terminal-e1s0w0-r2 | 30000 | 44000 | 45000, 45000 | — | 0 |
| gpt-6-astra-terminal-outer-o0n1-r1 | 30000 | 43000 | 35000, 45000 | — | 0 |
| gpt-6-astra-terminal-outer-o0n1-r2 | 30000 | 44000 | 31000, 45000 | — | 0 |
