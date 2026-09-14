# Recorded waiting trials

API-price equivalents value the reported token categories at Standard rates. They are not subscription charges.
Input is the inclusive total. Ordinary input = input − cached reads − cache writes. Reasoning is included in output.

| Trial | Success | Parent responses | Input total | Ordinary input | Cached reads | Cache writes | Output | Included reasoning | Parent USD | Child USD | Combined USD |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gpt-6-astra-ci-old-r1 | True | 5 | 96,037 | 15,141 | 80,896 | 0 | 222 | 11 | $0.243406 | $0.000000 | $0.243406 |
| gpt-6-astra-ci-old-r2 | True | 5 | 95,983 | 13,935 | 82,048 | 0 | 213 | 0 | $0.232048 | $0.000000 | $0.232048 |
| gpt-6-astra-subagent-old-r1 | True | 4 | 201,603 | 33,027 | 168,576 | 0 | 510 | 42 | $0.146998 | $0.377348 | $0.524346 |
| gpt-6-astra-subagent-old-r2 | True | 4 | 220,496 | 27,600 | 192,896 | 0 | 554 | 23 | $0.201254 | $0.295342 | $0.496596 |
| gpt-6-astra-terminal-old-r1 | True | 7 | 129,418 | 13,962 | 115,456 | 0 | 287 | 16 | $0.269426 | $0.000000 | $0.269426 |
| gpt-6-astra-terminal-old-r2 | True | 8 | 148,191 | 13,919 | 134,272 | 0 | 329 | 25 | $0.289912 | $0.000000 | $0.289912 |

## API-price breakdown

These disjoint dollar categories sum to Combined USD above; total input is not charged again.

| Trial | Ordinary input USD | Cached-read USD | Cache-write USD | Output USD |
|---|---:|---:|---:|---:|
| gpt-6-astra-ci-old-r1 | $0.151410 | $0.080896 | $0.000000 | $0.011100 |
| gpt-6-astra-ci-old-r2 | $0.139350 | $0.082048 | $0.000000 | $0.010650 |
| gpt-6-astra-subagent-old-r1 | $0.330270 | $0.168576 | $0.000000 | $0.025500 |
| gpt-6-astra-subagent-old-r2 | $0.276000 | $0.192896 | $0.000000 | $0.027700 |
| gpt-6-astra-terminal-old-r1 | $0.139620 | $0.115456 | $0.000000 | $0.014350 |
| gpt-6-astra-terminal-old-r2 | $0.139190 | $0.134272 | $0.000000 | $0.016450 |

## Parent and child token counts

| Trial | Scope | Responses | Input total | Ordinary input | Cached reads | Cache writes | Output |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| gpt-6-astra-ci-old-r1 | parent | 5 | 96,037 | 15,141 | 80,896 | 0 | 222 |
| gpt-6-astra-ci-old-r2 | parent | 5 | 95,983 | 13,935 | 82,048 | 0 | 213 |
| gpt-6-astra-subagent-old-r1 | parent | 4 | 73,634 | 6,946 | 66,688 | 0 | 217 |
| gpt-6-astra-subagent-old-r1 | child | 7 | 127,969 | 26,081 | 101,888 | 0 | 293 |
| gpt-6-astra-subagent-old-r2 | parent | 4 | 73,570 | 13,026 | 60,544 | 0 | 209 |
| gpt-6-astra-subagent-old-r2 | child | 8 | 146,926 | 14,574 | 132,352 | 0 | 345 |
| gpt-6-astra-terminal-old-r1 | parent | 7 | 129,418 | 13,962 | 115,456 | 0 | 287 |
| gpt-6-astra-terminal-old-r2 | parent | 8 | 148,191 | 13,919 | 134,272 | 0 | 329 |
