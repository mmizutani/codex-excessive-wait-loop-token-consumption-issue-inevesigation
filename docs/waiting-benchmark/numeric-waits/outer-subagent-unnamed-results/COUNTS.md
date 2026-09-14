# Recorded waiting trials

API-price equivalents value the reported token categories at Standard rates. They are not subscription charges.
Input is the inclusive total. Ordinary input = input − cached reads − cache writes. Reasoning is included in output.

| Trial | Success | Parent responses | Input total | Ordinary input | Cached reads | Cache writes | Output | Included reasoning | Parent USD | Child USD | Combined USD |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gpt-6-astra-subagent-e1s0w0-r1 | True | 4 | 125,609 | 15,657 | 109,952 | 0 | 410 | 0 | $0.140844 | $0.146178 | $0.287022 |
| gpt-6-astra-subagent-e1s0w0-r2 | True | 4 | 109,739 | 8,619 | 101,120 | 0 | 345 | 9 | $0.112104 | $0.092456 | $0.204560 |
| gpt-6-astra-subagent-outer-o0n0-r1 | True | 4 | 109,608 | 11,944 | 97,664 | 0 | 342 | 0 | $0.142778 | $0.091426 | $0.234204 |
| gpt-6-astra-subagent-outer-o0n0-r2 | True | 4 | 109,750 | 17,206 | 92,544 | 0 | 365 | 12 | $0.112924 | $0.169930 | $0.282854 |

## API-price breakdown

These disjoint dollar categories sum to Combined USD above; total input is not charged again.

| Trial | Ordinary input USD | Cached-read USD | Cache-write USD | Output USD |
|---|---:|---:|---:|---:|
| gpt-6-astra-subagent-e1s0w0-r1 | $0.156570 | $0.109952 | $0.000000 | $0.020500 |
| gpt-6-astra-subagent-e1s0w0-r2 | $0.086190 | $0.101120 | $0.000000 | $0.017250 |
| gpt-6-astra-subagent-outer-o0n0-r1 | $0.119440 | $0.097664 | $0.000000 | $0.017100 |
| gpt-6-astra-subagent-outer-o0n0-r2 | $0.172060 | $0.092544 | $0.000000 | $0.018250 |

## Parent and child token counts

| Trial | Scope | Responses | Input total | Ordinary input | Cached reads | Cache writes | Output |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| gpt-6-astra-subagent-e1s0w0-r1 | parent | 4 | 63,011 | 7,587 | 55,424 | 0 | 191 |
| gpt-6-astra-subagent-e1s0w0-r1 | child | 4 | 62,598 | 8,070 | 54,528 | 0 | 219 |
| gpt-6-astra-subagent-e1s0w0-r2 | parent | 4 | 62,997 | 4,373 | 58,624 | 0 | 195 |
| gpt-6-astra-subagent-e1s0w0-r2 | child | 3 | 46,742 | 4,246 | 42,496 | 0 | 150 |
| gpt-6-astra-subagent-outer-o0n0-r1 | parent | 4 | 62,929 | 7,761 | 55,168 | 0 | 200 |
| gpt-6-astra-subagent-outer-o0n0-r1 | child | 3 | 46,679 | 4,183 | 42,496 | 0 | 142 |
| gpt-6-astra-subagent-outer-o0n0-r2 | parent | 4 | 62,994 | 4,370 | 58,624 | 0 | 212 |
| gpt-6-astra-subagent-outer-o0n0-r2 | child | 3 | 46,756 | 12,836 | 33,920 | 0 | 153 |
