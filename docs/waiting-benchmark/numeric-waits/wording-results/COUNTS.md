# Recorded waiting trials

API-price equivalents value the reported token categories at Standard rates. They are not subscription charges.
Input is the inclusive total. Ordinary input = input − cached reads − cache writes. Reasoning is included in output.

| Trial | Success | Parent responses | Input total | Ordinary input | Cached reads | Cache writes | Output | Included reasoning | Parent USD | Child USD | Combined USD |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gpt-6-astra-ci-wording-measured-r1 | True | 5 | 80,049 | 5,041 | 75,008 | 0 | 595 | 42 | $0.155168 | $0.000000 | $0.155168 |
| gpt-6-astra-ci-wording-measured-r2 | True | 5 | 80,068 | 4,932 | 75,136 | 0 | 601 | 27 | $0.154506 | $0.000000 | $0.154506 |
| gpt-6-astra-ci-wording-no-pragma-r1 | True | 5 | 80,127 | 8,063 | 72,064 | 0 | 558 | 63 | $0.180594 | $0.000000 | $0.180594 |
| gpt-6-astra-ci-wording-no-pragma-r2 | True | 5 | 80,120 | 8,952 | 71,168 | 0 | 566 | 35 | $0.188988 | $0.000000 | $0.188988 |
| gpt-6-astra-ci-wording-with-pragma-r1 | True | 5 | 80,276 | 8,980 | 71,296 | 0 | 627 | 36 | $0.192446 | $0.000000 | $0.192446 |
| gpt-6-astra-ci-wording-with-pragma-r2 | True | 4 | 63,720 | 4,584 | 59,136 | 0 | 490 | 43 | $0.129476 | $0.000000 | $0.129476 |
| gpt-6-astra-subagent-wording-measured-r1 | True | 4 | 125,693 | 8,829 | 116,864 | 0 | 420 | 11 | $0.112212 | $0.113942 | $0.226154 |
| gpt-6-astra-subagent-wording-measured-r2 | True | 4 | 109,699 | 15,491 | 94,208 | 0 | 360 | 9 | $0.142988 | $0.124130 | $0.267118 |
| gpt-6-astra-subagent-wording-no-pragma-r1 | True | 4 | 125,834 | 8,586 | 117,248 | 0 | 404 | 0 | $0.111140 | $0.112168 | $0.223308 |
| gpt-6-astra-subagent-wording-no-pragma-r2 | True | 4 | 125,931 | 8,683 | 117,248 | 0 | 474 | 0 | $0.112170 | $0.115608 | $0.227778 |
| gpt-6-astra-subagent-wording-with-pragma-r1 | True | 4 | 110,039 | 11,735 | 98,304 | 0 | 362 | 12 | $0.141892 | $0.091862 | $0.233754 |
| gpt-6-astra-subagent-wording-with-pragma-r2 | True | 4 | 110,099 | 23,827 | 86,272 | 0 | 354 | 0 | $0.143904 | $0.198338 | $0.342242 |
| gpt-6-astra-terminal-wording-measured-r1 | True | 3 | 46,989 | 7,309 | 39,680 | 0 | 155 | 11 | $0.120520 | $0.000000 | $0.120520 |
| gpt-6-astra-terminal-wording-measured-r2 | True | 3 | 46,971 | 7,163 | 39,808 | 0 | 151 | 9 | $0.118988 | $0.000000 | $0.118988 |
| gpt-6-astra-terminal-wording-no-pragma-r1 | True | 4 | 63,027 | 7,731 | 55,296 | 0 | 216 | 8 | $0.143406 | $0.000000 | $0.143406 |
| gpt-6-astra-terminal-wording-no-pragma-r2 | True | 3 | 47,084 | 7,404 | 39,680 | 0 | 166 | 12 | $0.122020 | $0.000000 | $0.122020 |
| gpt-6-astra-terminal-wording-with-pragma-r1 | True | 3 | 47,063 | 4,055 | 43,008 | 0 | 149 | 9 | $0.091008 | $0.000000 | $0.091008 |
| gpt-6-astra-terminal-wording-with-pragma-r2 | True | 3 | 47,091 | 7,411 | 39,680 | 0 | 154 | 9 | $0.121490 | $0.000000 | $0.121490 |

## API-price breakdown

These disjoint dollar categories sum to Combined USD above; total input is not charged again.

| Trial | Ordinary input USD | Cached-read USD | Cache-write USD | Output USD |
|---|---:|---:|---:|---:|
| gpt-6-astra-ci-wording-measured-r1 | $0.050410 | $0.075008 | $0.000000 | $0.029750 |
| gpt-6-astra-ci-wording-measured-r2 | $0.049320 | $0.075136 | $0.000000 | $0.030050 |
| gpt-6-astra-ci-wording-no-pragma-r1 | $0.080630 | $0.072064 | $0.000000 | $0.027900 |
| gpt-6-astra-ci-wording-no-pragma-r2 | $0.089520 | $0.071168 | $0.000000 | $0.028300 |
| gpt-6-astra-ci-wording-with-pragma-r1 | $0.089800 | $0.071296 | $0.000000 | $0.031350 |
| gpt-6-astra-ci-wording-with-pragma-r2 | $0.045840 | $0.059136 | $0.000000 | $0.024500 |
| gpt-6-astra-subagent-wording-measured-r1 | $0.088290 | $0.116864 | $0.000000 | $0.021000 |
| gpt-6-astra-subagent-wording-measured-r2 | $0.154910 | $0.094208 | $0.000000 | $0.018000 |
| gpt-6-astra-subagent-wording-no-pragma-r1 | $0.085860 | $0.117248 | $0.000000 | $0.020200 |
| gpt-6-astra-subagent-wording-no-pragma-r2 | $0.086830 | $0.117248 | $0.000000 | $0.023700 |
| gpt-6-astra-subagent-wording-with-pragma-r1 | $0.117350 | $0.098304 | $0.000000 | $0.018100 |
| gpt-6-astra-subagent-wording-with-pragma-r2 | $0.238270 | $0.086272 | $0.000000 | $0.017700 |
| gpt-6-astra-terminal-wording-measured-r1 | $0.073090 | $0.039680 | $0.000000 | $0.007750 |
| gpt-6-astra-terminal-wording-measured-r2 | $0.071630 | $0.039808 | $0.000000 | $0.007550 |
| gpt-6-astra-terminal-wording-no-pragma-r1 | $0.077310 | $0.055296 | $0.000000 | $0.010800 |
| gpt-6-astra-terminal-wording-no-pragma-r2 | $0.074040 | $0.039680 | $0.000000 | $0.008300 |
| gpt-6-astra-terminal-wording-with-pragma-r1 | $0.040550 | $0.043008 | $0.000000 | $0.007450 |
| gpt-6-astra-terminal-wording-with-pragma-r2 | $0.074110 | $0.039680 | $0.000000 | $0.007700 |

## Parent and child token counts

| Trial | Scope | Responses | Input total | Ordinary input | Cached reads | Cache writes | Output |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| gpt-6-astra-ci-wording-measured-r1 | parent | 5 | 80,049 | 5,041 | 75,008 | 0 | 595 |
| gpt-6-astra-ci-wording-measured-r2 | parent | 5 | 80,068 | 4,932 | 75,136 | 0 | 601 |
| gpt-6-astra-ci-wording-no-pragma-r1 | parent | 5 | 80,127 | 8,063 | 72,064 | 0 | 558 |
| gpt-6-astra-ci-wording-no-pragma-r2 | parent | 5 | 80,120 | 8,952 | 71,168 | 0 | 566 |
| gpt-6-astra-ci-wording-with-pragma-r1 | parent | 5 | 80,276 | 8,980 | 71,296 | 0 | 627 |
| gpt-6-astra-ci-wording-with-pragma-r2 | parent | 4 | 63,720 | 4,584 | 59,136 | 0 | 490 |
| gpt-6-astra-subagent-wording-measured-r1 | parent | 4 | 63,038 | 4,286 | 58,752 | 0 | 212 |
| gpt-6-astra-subagent-wording-measured-r1 | child | 4 | 62,655 | 4,543 | 58,112 | 0 | 208 |
| gpt-6-astra-subagent-wording-measured-r2 | parent | 4 | 62,960 | 7,792 | 55,168 | 0 | 198 |
| gpt-6-astra-subagent-wording-measured-r2 | child | 3 | 46,739 | 7,699 | 39,040 | 0 | 162 |
| gpt-6-astra-subagent-wording-no-pragma-r1 | parent | 4 | 63,131 | 4,251 | 58,880 | 0 | 195 |
| gpt-6-astra-subagent-wording-no-pragma-r1 | child | 4 | 62,703 | 4,335 | 58,368 | 0 | 209 |
| gpt-6-astra-subagent-wording-no-pragma-r2 | parent | 4 | 63,119 | 4,239 | 58,880 | 0 | 218 |
| gpt-6-astra-subagent-wording-no-pragma-r2 | child | 4 | 62,812 | 4,444 | 58,368 | 0 | 256 |
| gpt-6-astra-subagent-wording-with-pragma-r1 | parent | 4 | 63,161 | 7,609 | 55,552 | 0 | 205 |
| gpt-6-astra-subagent-wording-with-pragma-r1 | child | 3 | 46,878 | 4,126 | 42,752 | 0 | 157 |
| gpt-6-astra-subagent-wording-with-pragma-r2 | parent | 4 | 63,197 | 7,773 | 55,424 | 0 | 215 |
| gpt-6-astra-subagent-wording-with-pragma-r2 | child | 3 | 46,902 | 16,054 | 30,848 | 0 | 139 |
| gpt-6-astra-terminal-wording-measured-r1 | parent | 3 | 46,989 | 7,309 | 39,680 | 0 | 155 |
| gpt-6-astra-terminal-wording-measured-r2 | parent | 3 | 46,971 | 7,163 | 39,808 | 0 | 151 |
| gpt-6-astra-terminal-wording-no-pragma-r1 | parent | 4 | 63,027 | 7,731 | 55,296 | 0 | 216 |
| gpt-6-astra-terminal-wording-no-pragma-r2 | parent | 3 | 47,084 | 7,404 | 39,680 | 0 | 166 |
| gpt-6-astra-terminal-wording-with-pragma-r1 | parent | 3 | 47,063 | 4,055 | 43,008 | 0 | 149 |
| gpt-6-astra-terminal-wording-with-pragma-r2 | parent | 3 | 47,091 | 7,411 | 39,680 | 0 | 154 |
