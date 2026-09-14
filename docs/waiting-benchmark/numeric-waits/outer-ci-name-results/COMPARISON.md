# Numeric wait measurements

Astra / low, CLI 0.154.0, shared skills disabled. Each row is a sum of fresh trials.
USD uses the dated API rates; cache-write zeros may be unreported values. This is not a subscription bill.

| Scenario | Variant | n | Responses | Input | Uncached | Cached | Writes | Output | API USD | Mean result delay (s) | Max update gap (s) | Gaps >60 s (trials) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ci | outer-o0n0 | 2 | 9 | 143,625 | 16,265 | 127,360 | 0 | 1,112 | $0.345610 | 20.017 | 44.110 | 0 |
| ci | outer-o0n1 | 2 | 10 | 159,834 | 10,074 | 149,760 | 0 | 1,123 | $0.306650 | 30.334 | 50.776 | 0 |

## Actual wait arguments

| Trial | exec_command ms | write_stdin ms | functions.exec ms | functions.wait ms | Running-cell returns |
|---|---|---|---|---|---:|
| gpt-6-astra-ci-outer-o0n0-r1 | 1000, 30000 | 44000 | 1000, 31000, 45000 | — | 0 |
| gpt-6-astra-ci-outer-o0n0-r2 | 30000, 30000 | 40000, 40000 | 35000, 35000, 45000, 45000 | — | 0 |
| gpt-6-astra-ci-outer-o0n1-r1 | 30000, 30000 | 44000, 44000 | 31000, 31000, 45000, 45000 | — | 0 |
| gpt-6-astra-ci-outer-o0n1-r2 | 30000, 30000 | 44000, 44000 | 31000, 31000, 45000, 45000 | — | 0 |
