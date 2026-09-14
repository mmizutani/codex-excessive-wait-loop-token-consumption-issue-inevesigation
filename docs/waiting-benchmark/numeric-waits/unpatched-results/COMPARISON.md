# Numeric wait measurements

Astra / low, CLI 0.154.0, shared skills disabled. Each row is a sum of fresh trials.
USD uses the dated API rates; cache-write zeros may be unreported values. This is not a subscription bill.

| Scenario | Variant | n | Responses | Input | Uncached | Cached | Writes | Output | API USD | Mean result delay (s) | Max update gap (s) | Gaps >60 s (trials) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ci | no-patch | 3 | 28 | 434,130 | 29,010 | 405,120 | 0 | 896 | $0.740020 | 20.405 | 78.565 | 2 |
| ci | wording-no-pragma | 3 | 14 | 223,672 | 22,072 | 201,600 | 0 | 1,538 | $0.499220 | 18.746 | 47.853 | 0 |
| subagent | no-patch | 3 | 40 | 613,954 | 40,386 | 573,568 | 0 | 1,484 | $1.051628 | 8.278 | 69.424 | 3 |
| subagent | wording-no-pragma | 3 | 23 | 361,640 | 35,880 | 325,760 | 0 | 1,204 | $0.744760 | 7.227 | 49.647 | 0 |
| terminal | no-patch | 3 | 30 | 467,836 | 32,508 | 435,328 | 0 | 1,320 | $0.826408 | 2.259 | 78.128 | 3 |
| terminal | wording-no-pragma | 3 | 10 | 157,105 | 9,265 | 147,840 | 0 | 518 | $0.266390 | 3.353 | 43.786 | 0 |

## Actual wait arguments

| Trial | exec_command ms | write_stdin ms | functions.exec ms | functions.wait ms | Running-cell returns |
|---|---|---|---|---|---:|
| gpt-6-astra-ci-no-patch-r1 | omitted-or-expression, omitted-or-expression, omitted-or-expression, omitted-or-expression, omitted-or-expression | — | omitted, omitted, omitted, omitted, omitted | — | 0 |
| gpt-6-astra-ci-no-patch-r2 | omitted-or-expression, omitted-or-expression, omitted-or-expression, omitted-or-expression | — | omitted, omitted, omitted, omitted | — | 0 |
| gpt-6-astra-ci-no-patch-r3 | omitted-or-expression, omitted-or-expression, omitted-or-expression, omitted-or-expression, omitted-or-expression | — | omitted, omitted, omitted, omitted, omitted | — | 0 |
| gpt-6-astra-ci-wording-no-pragma-r1 | 30000, 30000 | 40000, 40000 | 35000, 35000, 45000, 45000 | — | 0 |
| gpt-6-astra-ci-wording-no-pragma-r2 | 1000, 30000 | 40000, 40000 | omitted, 35000, 45000, 45000 | — | 0 |
| gpt-6-astra-ci-wording-no-pragma-r3 | 30000, 30000 | 40000 | 35000, 35000, 45000 | — | 0 |
| gpt-6-astra-subagent-no-patch-r1 | 1000 | 1000, 60000, 60000 | omitted, omitted, omitted, omitted | 1000, 30000 | 2 |
| gpt-6-astra-subagent-no-patch-r2 | 1000 | 1000, 1000, 60000 | omitted, omitted, omitted, omitted | 1000, 1000, 10000, 10000 | 4 |
| gpt-6-astra-subagent-no-patch-r3 | 1000 | 1000, 60000, 60000 | omitted, omitted, omitted, omitted | 1000, 1000, 30000 | 3 |
| gpt-6-astra-subagent-wording-no-pragma-r1 | 30000 | 40000, 40000 | 35000, 45000, 45000 | — | 0 |
| gpt-6-astra-subagent-wording-no-pragma-r2 | 30000 | 40000, 40000 | 35000, 45000, 45000 | — | 0 |
| gpt-6-astra-subagent-wording-no-pragma-r3 | 30000 | 40000 | 35000, 45000 | — | 0 |
| gpt-6-astra-terminal-no-patch-r1 | 1000 | 1000, 1000, 1000, 10000, 10000, 10000, 10000 | omitted, omitted, omitted, omitted, omitted, omitted, omitted, omitted | — | 0 |
| gpt-6-astra-terminal-no-patch-r2 | 1000 | 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000 | omitted, omitted, omitted, omitted, omitted, omitted, omitted, omitted, omitted, omitted | — | 0 |
| gpt-6-astra-terminal-no-patch-r3 | 1000 | 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000 | omitted, omitted, omitted, omitted, omitted, omitted, omitted, omitted, omitted | — | 0 |
| gpt-6-astra-terminal-wording-no-pragma-r1 | 30000 | 40000 | 35000, 45000 | — | 0 |
| gpt-6-astra-terminal-wording-no-pragma-r2 | 30000 | 40000 | 35000, 45000 | — | 0 |
| gpt-6-astra-terminal-wording-no-pragma-r3 | 30000 | 40000, 40000 | 35000, 45000, 45000 | — | 0 |
