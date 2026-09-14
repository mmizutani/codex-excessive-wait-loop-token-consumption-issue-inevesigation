# Recorded waiting trials

API-price equivalents value the reported token categories at Standard rates. They are not subscription charges.
Input is the inclusive total. Ordinary input = input − cached reads − cache writes. Reasoning is included in output.

| Trial | Success | Parent responses | Input total | Ordinary input | Cached reads | Cache writes | Output | Included reasoning | Parent USD | Child USD | Combined USD |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gpt-6-astra-ci-e1s0w0-r1 | True | 5 | 80,076 | 8,908 | 71,168 | 0 | 578 | 41 | $0.189148 | $0.000000 | $0.189148 |
| gpt-6-astra-ci-e1s0w0-r2 | True | 4 | 63,656 | 4,520 | 59,136 | 0 | 427 | 14 | $0.125686 | $0.000000 | $0.125686 |
| gpt-6-astra-ci-no-terminal-r1 | True | 6 | 95,859 | 5,107 | 90,752 | 0 | 671 | 48 | $0.175372 | $0.000000 | $0.175372 |
| gpt-6-astra-ci-no-terminal-r2 | True | 5 | 79,308 | 8,652 | 70,656 | 0 | 544 | 60 | $0.184376 | $0.000000 | $0.184376 |
| gpt-6-astra-subagent-e1s0w0-r1 | True | 4 | 125,764 | 12,484 | 113,280 | 0 | 509 | 36 | $0.148026 | $0.115544 | $0.263570 |
| gpt-6-astra-subagent-e1s0w0-r2 | True | 4 | 125,871 | 8,623 | 117,248 | 0 | 500 | 16 | $0.116420 | $0.112058 | $0.228478 |
| gpt-6-astra-subagent-no-terminal-r1 | True | 4 | 124,756 | 8,660 | 116,096 | 0 | 507 | 35 | $0.113698 | $0.114348 | $0.228046 |
| gpt-6-astra-subagent-no-terminal-r2 | True | 4 | 124,663 | 12,023 | 112,640 | 0 | 474 | 31 | $0.143290 | $0.113280 | $0.256570 |
| gpt-6-astra-terminal-e1s0w0-r1 | True | 4 | 62,909 | 7,485 | 55,424 | 0 | 221 | 15 | $0.141324 | $0.000000 | $0.141324 |
| gpt-6-astra-terminal-e1s0w0-r2 | True | 4 | 62,903 | 7,735 | 55,168 | 0 | 222 | 9 | $0.143618 | $0.000000 | $0.143618 |
| gpt-6-astra-terminal-no-terminal-r1 | True | 4 | 62,473 | 7,305 | 55,168 | 0 | 233 | 13 | $0.139868 | $0.000000 | $0.139868 |
| gpt-6-astra-terminal-no-terminal-r2 | True | 5 | 78,364 | 7,836 | 70,528 | 0 | 307 | 21 | $0.164238 | $0.000000 | $0.164238 |

## API-price breakdown

These disjoint dollar categories sum to Combined USD above; total input is not charged again.

| Trial | Ordinary input USD | Cached-read USD | Cache-write USD | Output USD |
|---|---:|---:|---:|---:|
| gpt-6-astra-ci-e1s0w0-r1 | $0.089080 | $0.071168 | $0.000000 | $0.028900 |
| gpt-6-astra-ci-e1s0w0-r2 | $0.045200 | $0.059136 | $0.000000 | $0.021350 |
| gpt-6-astra-ci-no-terminal-r1 | $0.051070 | $0.090752 | $0.000000 | $0.033550 |
| gpt-6-astra-ci-no-terminal-r2 | $0.086520 | $0.070656 | $0.000000 | $0.027200 |
| gpt-6-astra-subagent-e1s0w0-r1 | $0.124840 | $0.113280 | $0.000000 | $0.025450 |
| gpt-6-astra-subagent-e1s0w0-r2 | $0.086230 | $0.117248 | $0.000000 | $0.025000 |
| gpt-6-astra-subagent-no-terminal-r1 | $0.086600 | $0.116096 | $0.000000 | $0.025350 |
| gpt-6-astra-subagent-no-terminal-r2 | $0.120230 | $0.112640 | $0.000000 | $0.023700 |
| gpt-6-astra-terminal-e1s0w0-r1 | $0.074850 | $0.055424 | $0.000000 | $0.011050 |
| gpt-6-astra-terminal-e1s0w0-r2 | $0.077350 | $0.055168 | $0.000000 | $0.011100 |
| gpt-6-astra-terminal-no-terminal-r1 | $0.073050 | $0.055168 | $0.000000 | $0.011650 |
| gpt-6-astra-terminal-no-terminal-r2 | $0.078360 | $0.070528 | $0.000000 | $0.015350 |

## Parent and child token counts

| Trial | Scope | Responses | Input total | Ordinary input | Cached reads | Cache writes | Output |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| gpt-6-astra-ci-e1s0w0-r1 | parent | 5 | 80,076 | 8,908 | 71,168 | 0 | 578 |
| gpt-6-astra-ci-e1s0w0-r2 | parent | 4 | 63,656 | 4,520 | 59,136 | 0 | 427 |
| gpt-6-astra-ci-no-terminal-r1 | parent | 6 | 95,859 | 5,107 | 90,752 | 0 | 671 |
| gpt-6-astra-ci-no-terminal-r2 | parent | 5 | 79,308 | 8,652 | 70,656 | 0 | 544 |
| gpt-6-astra-subagent-e1s0w0-r1 | parent | 4 | 63,119 | 7,823 | 55,296 | 0 | 290 |
| gpt-6-astra-subagent-e1s0w0-r1 | child | 4 | 62,645 | 4,661 | 57,984 | 0 | 219 |
| gpt-6-astra-subagent-e1s0w0-r2 | parent | 4 | 63,169 | 4,289 | 58,880 | 0 | 293 |
| gpt-6-astra-subagent-e1s0w0-r2 | child | 4 | 62,702 | 4,334 | 58,368 | 0 | 207 |
| gpt-6-astra-subagent-no-terminal-r1 | parent | 4 | 62,601 | 4,233 | 58,368 | 0 | 260 |
| gpt-6-astra-subagent-no-terminal-r1 | child | 4 | 62,155 | 4,427 | 57,728 | 0 | 247 |
| gpt-6-astra-subagent-no-terminal-r2 | parent | 4 | 62,580 | 7,540 | 55,040 | 0 | 257 |
| gpt-6-astra-subagent-no-terminal-r2 | child | 4 | 62,083 | 4,483 | 57,600 | 0 | 217 |
| gpt-6-astra-terminal-e1s0w0-r1 | parent | 4 | 62,909 | 7,485 | 55,424 | 0 | 221 |
| gpt-6-astra-terminal-e1s0w0-r2 | parent | 4 | 62,903 | 7,735 | 55,168 | 0 | 222 |
| gpt-6-astra-terminal-no-terminal-r1 | parent | 4 | 62,473 | 7,305 | 55,168 | 0 | 233 |
| gpt-6-astra-terminal-no-terminal-r2 | parent | 5 | 78,364 | 7,836 | 70,528 | 0 | 307 |
