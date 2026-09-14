# Recorded waiting trials

API-price equivalents value the reported token categories at Standard rates. They are not subscription charges.
Input is the inclusive total. Ordinary input = input − cached reads − cache writes. Reasoning is included in output.

| Trial | Success | Parent responses | Input total | Ordinary input | Cached reads | Cache writes | Output | Included reasoning | Parent USD | Child USD | Combined USD |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gpt-6-astra-ci-old-r1 | True | 6 | 92,246 | 4,310 | 87,936 | 0 | 216 | 22 | $0.141836 | $0.000000 | $0.141836 |
| gpt-6-astra-subagent-old-r1 | True | 4 | 199,659 | 15,595 | 184,064 | 0 | 558 | 23 | $0.132740 | $0.235174 | $0.367914 |
| gpt-6-astra-terminal-old-r1 | True | 11 | 172,125 | 9,565 | 162,560 | 0 | 484 | 58 | $0.282410 | $0.000000 | $0.282410 |

## API-price breakdown

These disjoint dollar categories sum to Combined USD above; total input is not charged again.

| Trial | Ordinary input USD | Cached-read USD | Cache-write USD | Output USD |
|---|---:|---:|---:|---:|
| gpt-6-astra-ci-old-r1 | $0.043100 | $0.087936 | $0.000000 | $0.010800 |
| gpt-6-astra-subagent-old-r1 | $0.155950 | $0.184064 | $0.000000 | $0.027900 |
| gpt-6-astra-terminal-old-r1 | $0.095650 | $0.162560 | $0.000000 | $0.024200 |

## Parent and child token counts

| Trial | Scope | Responses | Input total | Ordinary input | Cached reads | Cache writes | Output |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| gpt-6-astra-ci-old-r1 | parent | 6 | 92,246 | 4,310 | 87,936 | 0 | 216 |
| gpt-6-astra-subagent-old-r1 | parent | 4 | 61,214 | 6,814 | 54,400 | 0 | 204 |
| gpt-6-astra-subagent-old-r1 | child | 9 | 138,445 | 8,781 | 129,664 | 0 | 354 |
| gpt-6-astra-terminal-old-r1 | parent | 11 | 172,125 | 9,565 | 162,560 | 0 | 484 |
