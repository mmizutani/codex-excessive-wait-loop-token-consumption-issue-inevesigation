# Numeric wait measurements

Astra / low, CLI 0.154.0, shared skills disabled. Each row is a sum of fresh trials.
USD uses the dated API rates; cache-write zeros may be unreported values. This is not a subscription bill.

| Scenario | Variant | n | Responses | Input | Uncached | Cached | Writes | Output | API USD | Mean result delay (s) | Max update gap (s) | Gaps >60 s (trials) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ci | wording-measured | 2 | 10 | 160,117 | 9,973 | 150,144 | 0 | 1,196 | $0.309674 | 29.538 | 48.301 | 0 |
| ci | wording-no-pragma | 2 | 10 | 160,247 | 17,015 | 143,232 | 0 | 1,124 | $0.369582 | 22.631 | 44.278 | 0 |
| ci | wording-with-pragma | 2 | 9 | 143,996 | 13,564 | 130,432 | 0 | 1,117 | $0.321922 | 21.471 | 44.682 | 0 |
| subagent | wording-measured | 2 | 15 | 235,392 | 24,320 | 211,072 | 0 | 780 | $0.493272 | 7.184 | 53.847 | 0 |
| subagent | wording-no-pragma | 2 | 16 | 251,765 | 17,269 | 234,496 | 0 | 878 | $0.451086 | 7.617 | 49.012 | 0 |
| subagent | wording-with-pragma | 2 | 14 | 220,138 | 35,562 | 184,576 | 0 | 716 | $0.575996 | 4.288 | 48.916 | 0 |
| terminal | wording-measured | 2 | 6 | 93,960 | 14,472 | 79,488 | 0 | 306 | $0.239508 | 2.018 | 43.781 | 0 |
| terminal | wording-no-pragma | 2 | 7 | 110,111 | 15,135 | 94,976 | 0 | 382 | $0.265426 | 4.002 | 44.817 | 0 |
| terminal | wording-with-pragma | 2 | 6 | 94,154 | 11,466 | 82,688 | 0 | 303 | $0.212498 | 2.968 | 44.753 | 0 |

## Actual wait arguments

| Trial | exec_command ms | write_stdin ms | functions.exec ms | functions.wait ms | Running-cell returns |
|---|---|---|---|---|---:|
| gpt-6-astra-ci-wording-measured-r1 | 1000, 30000 | 44000, 44000 | 1000, 31000, 45000, 45000 | — | 0 |
| gpt-6-astra-ci-wording-measured-r2 | 30000, 30000 | 44000, 44000 | 31000, 31000, 45000, 45000 | — | 0 |
| gpt-6-astra-ci-wording-no-pragma-r1 | 1000, 30000 | 40000, 40000 | omitted, omitted, 45000, 45000 | — | 0 |
| gpt-6-astra-ci-wording-no-pragma-r2 | 30000, 30000 | 40000, 40000 | 35000, 35000, 45000, 45000 | — | 0 |
| gpt-6-astra-ci-wording-with-pragma-r1 | 30000, 30000 | 40000, 40000 | 35000, 35000, 45000, 45000 | — | 0 |
| gpt-6-astra-ci-wording-with-pragma-r2 | 1000, 30000 | 40000 | 45000, 35000, 45000 | — | 0 |
| gpt-6-astra-subagent-wording-measured-r1 | 30000 | 40000, 40000 | 35000, 45000, 45000 | — | 0 |
| gpt-6-astra-subagent-wording-measured-r2 | 30000 | 44000 | 31000, 45000 | — | 0 |
| gpt-6-astra-subagent-wording-no-pragma-r1 | 30000 | 40000, 40000 | 35000, 45000, 45000 | — | 0 |
| gpt-6-astra-subagent-wording-no-pragma-r2 | 30000 | 40000, 40000 | 35000, 45000, 45000 | — | 0 |
| gpt-6-astra-subagent-wording-with-pragma-r1 | 30000 | 44000 | 31000, 45000 | — | 0 |
| gpt-6-astra-subagent-wording-with-pragma-r2 | 30000 | 40000 | 35000, 45000 | — | 0 |
| gpt-6-astra-terminal-wording-measured-r1 | 30000 | 44000 | 31000, 45000 | — | 0 |
| gpt-6-astra-terminal-wording-measured-r2 | 30000 | 44000 | 31000, 45000 | — | 0 |
| gpt-6-astra-terminal-wording-no-pragma-r1 | 30000 | 40000, 40000 | 35000, 45000, 45000 | — | 0 |
| gpt-6-astra-terminal-wording-no-pragma-r2 | 30000 | 40000 | 35000, 45000 | — | 0 |
| gpt-6-astra-terminal-wording-with-pragma-r1 | 30000 | 44000 | 31000, 45000 | — | 0 |
| gpt-6-astra-terminal-wording-with-pragma-r2 | 30000 | 44000 | 31000, 45000 | — | 0 |
