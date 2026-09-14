# Recorded waiting trials

API-price equivalents value the reported token categories at Standard rates. They are not subscription charges.
Input is the inclusive total. Ordinary input = input − cached reads − cache writes. Reasoning is included in output.

| Trial | Success | Parent responses | Input total | Ordinary input | Cached reads | Cache writes | Output | Included reasoning | Parent USD | Child USD | Combined USD |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gpt-6-astra-ci-patch-r1 | True | 4 | 63,656 | 4,520 | 59,136 | 0 | 420 | 15 | $0.125336 | $0.000000 | $0.125336 |
| gpt-6-astra-subagent-patch-r1 | True | 4 | 125,649 | 12,241 | 113,408 | 0 | 483 | 22 | $0.115612 | $0.144356 | $0.259968 |
| gpt-6-astra-terminal-patch-r1 | True | 4 | 62,895 | 7,727 | 55,168 | 0 | 217 | 9 | $0.143288 | $0.000000 | $0.143288 |

## API-price breakdown

These disjoint dollar categories sum to Combined USD above; total input is not charged again.

| Trial | Ordinary input USD | Cached-read USD | Cache-write USD | Output USD |
|---|---:|---:|---:|---:|
| gpt-6-astra-ci-patch-r1 | $0.045200 | $0.059136 | $0.000000 | $0.021000 |
| gpt-6-astra-subagent-patch-r1 | $0.122410 | $0.113408 | $0.000000 | $0.024150 |
| gpt-6-astra-terminal-patch-r1 | $0.077270 | $0.055168 | $0.000000 | $0.010850 |

## Parent and child token counts

| Trial | Scope | Responses | Input total | Ordinary input | Cached reads | Cache writes | Output |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| gpt-6-astra-ci-patch-r1 | parent | 4 | 63,656 | 4,520 | 59,136 | 0 | 420 |
| gpt-6-astra-subagent-patch-r1 | parent | 4 | 63,073 | 4,321 | 58,752 | 0 | 273 |
| gpt-6-astra-subagent-patch-r1 | child | 4 | 62,576 | 7,920 | 54,656 | 0 | 210 |
| gpt-6-astra-terminal-patch-r1 | parent | 4 | 62,895 | 7,727 | 55,168 | 0 | 217 |
