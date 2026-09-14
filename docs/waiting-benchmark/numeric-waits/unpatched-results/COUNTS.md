# Recorded waiting trials

API-price equivalents value the reported token categories at Standard rates. They are not subscription charges.
Input is the inclusive total. Ordinary input = input − cached reads − cache writes. Reasoning is included in output.

| Trial | Success | Parent responses | Input total | Ordinary input | Cached reads | Cache writes | Output | Included reasoning | Parent USD | Child USD | Combined USD |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gpt-6-astra-ci-no-patch-r1 | True | 10 | 155,357 | 12,125 | 143,232 | 0 | 308 | 14 | $0.279882 | $0.000000 | $0.279882 |
| gpt-6-astra-ci-no-patch-r2 | True | 8 | 123,624 | 8,296 | 115,328 | 0 | 276 | 31 | $0.212088 | $0.000000 | $0.212088 |
| gpt-6-astra-ci-no-patch-r3 | True | 10 | 155,149 | 8,589 | 146,560 | 0 | 312 | 18 | $0.248050 | $0.000000 | $0.248050 |
| gpt-6-astra-ci-wording-no-pragma-r1 | True | 5 | 80,135 | 4,871 | 75,264 | 0 | 550 | 37 | $0.151474 | $0.000000 | $0.151474 |
| gpt-6-astra-ci-wording-no-pragma-r2 | True | 5 | 79,815 | 8,775 | 71,040 | 0 | 492 | 29 | $0.183390 | $0.000000 | $0.183390 |
| gpt-6-astra-ci-wording-no-pragma-r3 | True | 4 | 63,722 | 8,426 | 55,296 | 0 | 496 | 41 | $0.164356 | $0.000000 | $0.164356 |
| gpt-6-astra-subagent-no-patch-r1 | True | 5 | 199,212 | 12,204 | 187,008 | 0 | 457 | 8 | $0.151154 | $0.180744 | $0.331898 |
| gpt-6-astra-subagent-no-patch-r2 | True | 4 | 199,561 | 12,297 | 187,264 | 0 | 485 | 17 | $0.105634 | $0.228850 | $0.334484 |
| gpt-6-astra-subagent-no-patch-r3 | True | 5 | 215,181 | 15,885 | 199,296 | 0 | 542 | 10 | $0.152952 | $0.232294 | $0.385246 |
| gpt-6-astra-subagent-wording-no-pragma-r1 | True | 4 | 125,799 | 12,007 | 113,792 | 0 | 405 | 6 | $0.142084 | $0.112028 | $0.254112 |
| gpt-6-astra-subagent-wording-no-pragma-r2 | True | 4 | 125,821 | 12,157 | 113,664 | 0 | 427 | 0 | $0.110950 | $0.145634 | $0.256584 |
| gpt-6-astra-subagent-wording-no-pragma-r3 | True | 4 | 110,020 | 11,716 | 98,304 | 0 | 372 | 18 | $0.142072 | $0.091992 | $0.234064 |
| gpt-6-astra-terminal-no-patch-r1 | True | 9 | 139,928 | 9,368 | 130,560 | 0 | 405 | 33 | $0.244490 | $0.000000 | $0.244490 |
| gpt-6-astra-terminal-no-patch-r2 | True | 11 | 172,017 | 5,745 | 166,272 | 0 | 486 | 39 | $0.248022 | $0.000000 | $0.248022 |
| gpt-6-astra-terminal-no-patch-r3 | True | 10 | 155,891 | 17,395 | 138,496 | 0 | 429 | 44 | $0.333896 | $0.000000 | $0.333896 |
| gpt-6-astra-terminal-wording-no-pragma-r1 | True | 3 | 47,060 | 852 | 46,208 | 0 | 150 | 10 | $0.062228 | $0.000000 | $0.062228 |
| gpt-6-astra-terminal-wording-no-pragma-r2 | True | 3 | 47,065 | 4,057 | 43,008 | 0 | 151 | 9 | $0.091128 | $0.000000 | $0.091128 |
| gpt-6-astra-terminal-wording-no-pragma-r3 | True | 4 | 62,980 | 4,356 | 58,624 | 0 | 217 | 7 | $0.113034 | $0.000000 | $0.113034 |

## API-price breakdown

These disjoint dollar categories sum to Combined USD above; total input is not charged again.

| Trial | Ordinary input USD | Cached-read USD | Cache-write USD | Output USD |
|---|---:|---:|---:|---:|
| gpt-6-astra-ci-no-patch-r1 | $0.121250 | $0.143232 | $0.000000 | $0.015400 |
| gpt-6-astra-ci-no-patch-r2 | $0.082960 | $0.115328 | $0.000000 | $0.013800 |
| gpt-6-astra-ci-no-patch-r3 | $0.085890 | $0.146560 | $0.000000 | $0.015600 |
| gpt-6-astra-ci-wording-no-pragma-r1 | $0.048710 | $0.075264 | $0.000000 | $0.027500 |
| gpt-6-astra-ci-wording-no-pragma-r2 | $0.087750 | $0.071040 | $0.000000 | $0.024600 |
| gpt-6-astra-ci-wording-no-pragma-r3 | $0.084260 | $0.055296 | $0.000000 | $0.024800 |
| gpt-6-astra-subagent-no-patch-r1 | $0.122040 | $0.187008 | $0.000000 | $0.022850 |
| gpt-6-astra-subagent-no-patch-r2 | $0.122970 | $0.187264 | $0.000000 | $0.024250 |
| gpt-6-astra-subagent-no-patch-r3 | $0.158850 | $0.199296 | $0.000000 | $0.027100 |
| gpt-6-astra-subagent-wording-no-pragma-r1 | $0.120070 | $0.113792 | $0.000000 | $0.020250 |
| gpt-6-astra-subagent-wording-no-pragma-r2 | $0.121570 | $0.113664 | $0.000000 | $0.021350 |
| gpt-6-astra-subagent-wording-no-pragma-r3 | $0.117160 | $0.098304 | $0.000000 | $0.018600 |
| gpt-6-astra-terminal-no-patch-r1 | $0.093680 | $0.130560 | $0.000000 | $0.020250 |
| gpt-6-astra-terminal-no-patch-r2 | $0.057450 | $0.166272 | $0.000000 | $0.024300 |
| gpt-6-astra-terminal-no-patch-r3 | $0.173950 | $0.138496 | $0.000000 | $0.021450 |
| gpt-6-astra-terminal-wording-no-pragma-r1 | $0.008520 | $0.046208 | $0.000000 | $0.007500 |
| gpt-6-astra-terminal-wording-no-pragma-r2 | $0.040570 | $0.043008 | $0.000000 | $0.007550 |
| gpt-6-astra-terminal-wording-no-pragma-r3 | $0.043560 | $0.058624 | $0.000000 | $0.010850 |

## Parent and child token counts

| Trial | Scope | Responses | Input total | Ordinary input | Cached reads | Cache writes | Output |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| gpt-6-astra-ci-no-patch-r1 | parent | 10 | 155,357 | 12,125 | 143,232 | 0 | 308 |
| gpt-6-astra-ci-no-patch-r2 | parent | 8 | 123,624 | 8,296 | 115,328 | 0 | 276 |
| gpt-6-astra-ci-no-patch-r3 | parent | 10 | 155,149 | 8,589 | 146,560 | 0 | 312 |
| gpt-6-astra-ci-wording-no-pragma-r1 | parent | 5 | 80,135 | 4,871 | 75,264 | 0 | 550 |
| gpt-6-astra-ci-wording-no-pragma-r2 | parent | 5 | 79,815 | 8,775 | 71,040 | 0 | 492 |
| gpt-6-astra-ci-wording-no-pragma-r3 | parent | 4 | 63,722 | 8,426 | 55,296 | 0 | 496 |
| gpt-6-astra-subagent-no-patch-r1 | parent | 5 | 76,764 | 7,260 | 69,504 | 0 | 181 |
| gpt-6-astra-subagent-no-patch-r1 | child | 8 | 122,448 | 4,944 | 117,504 | 0 | 276 |
| gpt-6-astra-subagent-no-patch-r2 | parent | 4 | 61,253 | 3,909 | 57,344 | 0 | 184 |
| gpt-6-astra-subagent-no-patch-r2 | child | 9 | 138,308 | 8,388 | 129,920 | 0 | 301 |
| gpt-6-astra-subagent-no-patch-r3 | parent | 5 | 76,894 | 7,262 | 69,632 | 0 | 214 |
| gpt-6-astra-subagent-no-patch-r3 | child | 9 | 138,287 | 8,623 | 129,664 | 0 | 328 |
| gpt-6-astra-subagent-wording-no-pragma-r1 | parent | 4 | 63,115 | 7,691 | 55,424 | 0 | 195 |
| gpt-6-astra-subagent-wording-no-pragma-r1 | child | 4 | 62,684 | 4,316 | 58,368 | 0 | 210 |
| gpt-6-astra-subagent-wording-no-pragma-r2 | parent | 4 | 63,097 | 4,217 | 58,880 | 0 | 198 |
| gpt-6-astra-subagent-wording-no-pragma-r2 | child | 4 | 62,724 | 7,940 | 54,784 | 0 | 229 |
| gpt-6-astra-subagent-wording-no-pragma-r3 | parent | 4 | 63,154 | 7,602 | 55,552 | 0 | 210 |
| gpt-6-astra-subagent-wording-no-pragma-r3 | child | 3 | 46,866 | 4,114 | 42,752 | 0 | 162 |
| gpt-6-astra-terminal-no-patch-r1 | parent | 9 | 139,928 | 9,368 | 130,560 | 0 | 405 |
| gpt-6-astra-terminal-no-patch-r2 | parent | 11 | 172,017 | 5,745 | 166,272 | 0 | 486 |
| gpt-6-astra-terminal-no-patch-r3 | parent | 10 | 155,891 | 17,395 | 138,496 | 0 | 429 |
| gpt-6-astra-terminal-wording-no-pragma-r1 | parent | 3 | 47,060 | 852 | 46,208 | 0 | 150 |
| gpt-6-astra-terminal-wording-no-pragma-r2 | parent | 3 | 47,065 | 4,057 | 43,008 | 0 | 151 |
| gpt-6-astra-terminal-wording-no-pragma-r3 | parent | 4 | 62,980 | 4,356 | 58,624 | 0 | 217 |
