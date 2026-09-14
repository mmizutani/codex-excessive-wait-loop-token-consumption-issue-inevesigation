# Numeric wait measurements

Astra / low, CLI 0.154.0, shared skills disabled. Each row is a sum of fresh trials.
USD uses the dated API rates; cache-write zeros may be unreported values. This is not a subscription bill.

| Scenario | Variant | n | Responses | Input | Uncached | Cached | Writes | Output | API USD | Mean result delay (s) | Max update gap (s) | Gaps >60 s (trials) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| terminal | outer-o0n0 | 3 | 9 | 140,822 | 15,126 | 125,696 | 0 | 438 | $0.298856 | 2.872 | 45.205 | 0 |
| terminal | outer-o0n1 | 3 | 10 | 156,875 | 25,419 | 131,456 | 0 | 537 | $0.412496 | 4.075 | 45.273 | 0 |
| terminal | outer-o1n0 | 3 | 9 | 140,930 | 11,906 | 129,024 | 0 | 462 | $0.271184 | 2.637 | 45.284 | 0 |
| terminal | outer-o1n1 | 3 | 9 | 141,034 | 18,538 | 122,496 | 0 | 456 | $0.330676 | 2.505 | 44.102 | 0 |

## Actual wait arguments

| Trial | exec_command ms | write_stdin ms | functions.exec ms | functions.wait ms | Running-cell returns |
|---|---|---|---|---|---:|
| gpt-6-astra-terminal-outer-o0n0-r1 | 30000 | 44000 | 31000, 45000 | — | 0 |
| gpt-6-astra-terminal-outer-o0n0-r2 | 30000 | 44000 | 31000, 45000 | — | 0 |
| gpt-6-astra-terminal-outer-o0n0-r3 | 30000 | 44000 | 31000, 45000 | — | 0 |
| gpt-6-astra-terminal-outer-o0n1-r1 | 30000 | 44000 | 31000, 45000 | — | 0 |
| gpt-6-astra-terminal-outer-o0n1-r2 | 30000 | 40000, 40000 | 35000, 45000, 45000 | — | 0 |
| gpt-6-astra-terminal-outer-o0n1-r3 | 30000 | 44000 | 31000, 45000 | — | 0 |
| gpt-6-astra-terminal-outer-o1n0-r1 | 30000 | 44000 | 45000, 45000 | — | 0 |
| gpt-6-astra-terminal-outer-o1n0-r2 | 30000 | 44000 | 45000, 45000 | — | 0 |
| gpt-6-astra-terminal-outer-o1n0-r3 | 30000 | 44000 | 45000, 45000 | — | 0 |
| gpt-6-astra-terminal-outer-o1n1-r1 | 30000 | 40000 | 45000, 45000 | — | 0 |
| gpt-6-astra-terminal-outer-o1n1-r2 | 30000 | 40000 | 45000, 45000 | — | 0 |
| gpt-6-astra-terminal-outer-o1n1-r3 | 30000 | 44000 | 45000, 45000 | — | 0 |
