# Recorded waiting trials

API-price equivalents value the reported token categories at Standard rates. They are not subscription charges.
Input is the inclusive total. Ordinary input = input − cached reads − cache writes. Reasoning is included in output.

| Trial | Success | Parent responses | Input total | Ordinary input | Cached reads | Cache writes | Output | Included reasoning | Parent USD | Child USD | Combined USD |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gpt-6-astra-ci-e1s0w0-r1 | True | 4 | 63,603 | 8,435 | 55,168 | 0 | 479 | 35 | $0.163468 | $0.000000 | $0.163468 |
| gpt-6-astra-ci-e1s0w0-r2 | True | 4 | 63,651 | 8,227 | 55,424 | 0 | 437 | 14 | $0.159544 | $0.000000 | $0.159544 |
| gpt-6-astra-ci-outer-o0n1-r1 | True | 5 | 79,894 | 12,054 | 67,840 | 0 | 526 | 27 | $0.214680 | $0.000000 | $0.214680 |
| gpt-6-astra-ci-outer-o0n1-r2 | True | 5 | 80,018 | 15,890 | 64,128 | 0 | 578 | 38 | $0.251928 | $0.000000 | $0.251928 |
| gpt-6-astra-subagent-e1s0w0-r1 | True | 4 | 126,004 | 12,340 | 113,664 | 0 | 561 | 76 | $0.151706 | $0.113408 | $0.265114 |
| gpt-6-astra-subagent-e1s0w0-r2 | True | 4 | 125,819 | 8,955 | 116,864 | 0 | 561 | 117 | $0.120260 | $0.114204 | $0.234464 |
| gpt-6-astra-subagent-outer-o0n1-r1 | True | 4 | 109,871 | 12,079 | 97,792 | 0 | 406 | 46 | $0.116112 | $0.122770 | $0.238882 |
| gpt-6-astra-subagent-outer-o0n1-r2 | False | 1 | 15,574 | 3,414 | 12,160 | 0 | 236 | 180 | $0.058100 | $0.000000 | $0.058100 |
| gpt-6-astra-terminal-e1s0w0-r1 | True | 4 | 62,880 | 7,584 | 55,296 | 0 | 220 | 9 | $0.142136 | $0.000000 | $0.142136 |
| gpt-6-astra-terminal-e1s0w0-r2 | True | 3 | 46,993 | 7,313 | 39,680 | 0 | 157 | 14 | $0.120660 | $0.000000 | $0.120660 |
| gpt-6-astra-terminal-outer-o0n1-r1 | True | 3 | 46,982 | 7,302 | 39,680 | 0 | 150 | 9 | $0.120200 | $0.000000 | $0.120200 |
| gpt-6-astra-terminal-outer-o0n1-r2 | True | 3 | 46,994 | 7,314 | 39,680 | 0 | 156 | 9 | $0.120620 | $0.000000 | $0.120620 |

## API-price breakdown

These disjoint dollar categories sum to Combined USD above; total input is not charged again.

| Trial | Ordinary input USD | Cached-read USD | Cache-write USD | Output USD |
|---|---:|---:|---:|---:|
| gpt-6-astra-ci-e1s0w0-r1 | $0.084350 | $0.055168 | $0.000000 | $0.023950 |
| gpt-6-astra-ci-e1s0w0-r2 | $0.082270 | $0.055424 | $0.000000 | $0.021850 |
| gpt-6-astra-ci-outer-o0n1-r1 | $0.120540 | $0.067840 | $0.000000 | $0.026300 |
| gpt-6-astra-ci-outer-o0n1-r2 | $0.158900 | $0.064128 | $0.000000 | $0.028900 |
| gpt-6-astra-subagent-e1s0w0-r1 | $0.123400 | $0.113664 | $0.000000 | $0.028050 |
| gpt-6-astra-subagent-e1s0w0-r2 | $0.089550 | $0.116864 | $0.000000 | $0.028050 |
| gpt-6-astra-subagent-outer-o0n1-r1 | $0.120790 | $0.097792 | $0.000000 | $0.020300 |
| gpt-6-astra-subagent-outer-o0n1-r2 | $0.034140 | $0.012160 | $0.000000 | $0.011800 |
| gpt-6-astra-terminal-e1s0w0-r1 | $0.075840 | $0.055296 | $0.000000 | $0.011000 |
| gpt-6-astra-terminal-e1s0w0-r2 | $0.073130 | $0.039680 | $0.000000 | $0.007850 |
| gpt-6-astra-terminal-outer-o0n1-r1 | $0.073020 | $0.039680 | $0.000000 | $0.007500 |
| gpt-6-astra-terminal-outer-o0n1-r2 | $0.073140 | $0.039680 | $0.000000 | $0.007800 |

## Parent and child token counts

| Trial | Scope | Responses | Input total | Ordinary input | Cached reads | Cache writes | Output |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| gpt-6-astra-ci-e1s0w0-r1 | parent | 4 | 63,603 | 8,435 | 55,168 | 0 | 479 |
| gpt-6-astra-ci-e1s0w0-r2 | parent | 4 | 63,651 | 8,227 | 55,424 | 0 | 437 |
| gpt-6-astra-ci-outer-o0n1-r1 | parent | 5 | 79,894 | 12,054 | 67,840 | 0 | 526 |
| gpt-6-astra-ci-outer-o0n1-r2 | parent | 5 | 80,018 | 15,890 | 64,128 | 0 | 578 |
| gpt-6-astra-subagent-e1s0w0-r1 | parent | 4 | 63,287 | 7,991 | 55,296 | 0 | 330 |
| gpt-6-astra-subagent-e1s0w0-r1 | child | 4 | 62,717 | 4,349 | 58,368 | 0 | 231 |
| gpt-6-astra-subagent-e1s0w0-r2 | parent | 4 | 63,318 | 4,438 | 58,880 | 0 | 340 |
| gpt-6-astra-subagent-e1s0w0-r2 | child | 4 | 62,501 | 4,517 | 57,984 | 0 | 221 |
| gpt-6-astra-subagent-outer-o0n1-r1 | parent | 4 | 63,168 | 4,416 | 58,752 | 0 | 264 |
| gpt-6-astra-subagent-outer-o0n1-r1 | child | 3 | 46,703 | 7,663 | 39,040 | 0 | 142 |
| gpt-6-astra-subagent-outer-o0n1-r2 | parent | 1 | 15,574 | 3,414 | 12,160 | 0 | 236 |
| gpt-6-astra-terminal-e1s0w0-r1 | parent | 4 | 62,880 | 7,584 | 55,296 | 0 | 220 |
| gpt-6-astra-terminal-e1s0w0-r2 | parent | 3 | 46,993 | 7,313 | 39,680 | 0 | 157 |
| gpt-6-astra-terminal-outer-o0n1-r1 | parent | 3 | 46,982 | 7,302 | 39,680 | 0 | 150 |
| gpt-6-astra-terminal-outer-o0n1-r2 | parent | 3 | 46,994 | 7,314 | 39,680 | 0 | 156 |
