# Recorded waiting trials

API-price equivalents value the reported token categories at Standard rates. They are not subscription charges.
Input is the inclusive total. Ordinary input = input − cached reads − cache writes. Reasoning is included in output.

| Trial | Success | Parent responses | Input total | Ordinary input | Cached reads | Cache writes | Output | Included reasoning | Parent USD | Child USD | Combined USD |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gpt-5.6-sol-ci-tuned-r1 | True | 4 | 60,375 | 5,079 | 55,296 | 0 | 757 | 273 | $0.057574 | $0.000000 | $0.057574 |
| gpt-5.6-sol-subagent-tuned-r1 | True | 4 | 118,691 | 16,291 | 102,400 | 0 | 563 | 0 | $0.057725 | $0.059659 | $0.117384 |
| gpt-5.6-sol-terminal-tuned-r1 | True | 4 | 59,364 | 8,292 | 51,072 | 0 | 276 | 16 | $0.059117 | $0.000000 | $0.059117 |
| gpt-6-astra-ci-tuned-r1 | True | 5 | 80,036 | 8,868 | 71,168 | 0 | 552 | 59 | $0.187448 | $0.000000 | $0.187448 |
| gpt-6-astra-subagent-tuned-r1 | True | 4 | 126,098 | 12,434 | 113,664 | 0 | 505 | 20 | $0.150156 | $0.113098 | $0.263254 |
| gpt-6-astra-terminal-tuned-r1 | True | 4 | 62,974 | 7,550 | 55,424 | 0 | 222 | 9 | $0.142024 | $0.000000 | $0.142024 |

## API-price breakdown

These disjoint dollar categories sum to Combined USD above; total input is not charged again.

| Trial | Ordinary input USD | Cached-read USD | Cache-write USD | Output USD |
|---|---:|---:|---:|---:|
| gpt-5.6-sol-ci-tuned-r1 | $0.020316 | $0.022118 | $0.000000 | $0.015140 |
| gpt-5.6-sol-subagent-tuned-r1 | $0.065164 | $0.040960 | $0.000000 | $0.011260 |
| gpt-5.6-sol-terminal-tuned-r1 | $0.033168 | $0.020429 | $0.000000 | $0.005520 |
| gpt-6-astra-ci-tuned-r1 | $0.088680 | $0.071168 | $0.000000 | $0.027600 |
| gpt-6-astra-subagent-tuned-r1 | $0.124340 | $0.113664 | $0.000000 | $0.025250 |
| gpt-6-astra-terminal-tuned-r1 | $0.075500 | $0.055424 | $0.000000 | $0.011100 |

## Parent and child token counts

| Trial | Scope | Responses | Input total | Ordinary input | Cached reads | Cache writes | Output |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| gpt-5.6-sol-ci-tuned-r1 | parent | 4 | 60,375 | 5,079 | 55,296 | 0 | 757 |
| gpt-5.6-sol-subagent-tuned-r1 | parent | 4 | 59,171 | 8,099 | 51,072 | 0 | 245 |
| gpt-5.6-sol-subagent-tuned-r1 | child | 4 | 59,520 | 8,192 | 51,328 | 0 | 318 |
| gpt-5.6-sol-terminal-tuned-r1 | parent | 4 | 59,364 | 8,292 | 51,072 | 0 | 276 |
| gpt-6-astra-ci-tuned-r1 | parent | 5 | 80,036 | 8,868 | 71,168 | 0 | 552 |
| gpt-6-astra-subagent-tuned-r1 | parent | 4 | 63,282 | 7,986 | 55,296 | 0 | 300 |
| gpt-6-astra-subagent-tuned-r1 | child | 4 | 62,816 | 4,448 | 58,368 | 0 | 205 |
| gpt-6-astra-terminal-tuned-r1 | parent | 4 | 62,974 | 7,550 | 55,424 | 0 | 222 |
