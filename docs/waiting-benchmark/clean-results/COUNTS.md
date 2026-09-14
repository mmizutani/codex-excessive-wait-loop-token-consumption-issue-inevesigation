# Recorded waiting trials

API-price equivalents value the reported token categories at Standard rates. They are not subscription charges.
Input is the inclusive total. Ordinary input = input − cached reads − cache writes. Reasoning is included in output.

| Trial | Success | Parent responses | Input total | Ordinary input | Cached reads | Cache writes | Output | Included reasoning | Parent USD | Child USD | Combined USD |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gpt-5.6-sol-ci-new-r1 | True | 5 | 72,825 | 8,185 | 64,640 | 0 | 495 | 52 | $0.068496 | $0.000000 | $0.068496 |
| gpt-5.6-sol-ci-old-r1 | True | 6 | 89,002 | 31,274 | 57,728 | 0 | 523 | 109 | $0.158647 | $0.000000 | $0.158647 |
| gpt-5.6-sol-ci-patch-r1 | True | 6 | 90,338 | 9,314 | 81,024 | 0 | 652 | 93 | $0.082706 | $0.000000 | $0.082706 |
| gpt-5.6-sol-ci-tuned-r1 | True | 6 | 90,442 | 8,522 | 81,920 | 0 | 545 | 103 | $0.077756 | $0.000000 | $0.077756 |
| gpt-5.6-sol-subagent-new-r1 | True | 3 | 100,581 | 7,781 | 92,800 | 0 | 450 | 37 | $0.033644 | $0.043600 | $0.077244 |
| gpt-5.6-sol-subagent-old-r1 | True | 3 | 116,105 | 29,705 | 86,400 | 0 | 504 | 76 | $0.084706 | $0.078754 | $0.163460 |
| gpt-5.6-sol-subagent-patch-r1 | True | 3 | 103,452 | 15,644 | 87,808 | 0 | 461 | 64 | $0.035290 | $0.071629 | $0.106919 |
| gpt-5.6-sol-subagent-tuned-r1 | True | 4 | 118,817 | 19,617 | 99,200 | 0 | 576 | 69 | $0.070154 | $0.059514 | $0.129668 |
| gpt-5.6-sol-terminal-new-r1 | True | 4 | 57,679 | 7,247 | 50,432 | 0 | 278 | 19 | $0.054721 | $0.000000 | $0.054721 |
| gpt-5.6-sol-terminal-old-r1 | True | 4 | 58,044 | 23,100 | 34,944 | 0 | 226 | 8 | $0.110898 | $0.000000 | $0.110898 |
| gpt-5.6-sol-terminal-patch-r1 | True | 4 | 58,891 | 7,819 | 51,072 | 0 | 274 | 32 | $0.057185 | $0.000000 | $0.057185 |
| gpt-5.6-sol-terminal-tuned-r1 | True | 4 | 59,426 | 8,098 | 51,328 | 0 | 342 | 60 | $0.059763 | $0.000000 | $0.059763 |
| gpt-6-astra-ci-new-r1 | True | 8 | 123,659 | 14,603 | 109,056 | 0 | 259 | 16 | $0.268036 | $0.000000 | $0.268036 |
| gpt-6-astra-ci-patch-r1 | True | 8 | 126,165 | 12,245 | 113,920 | 0 | 246 | 0 | $0.248670 | $0.000000 | $0.248670 |
| gpt-6-astra-ci-tuned-r1 | True | 8 | 127,083 | 12,651 | 114,432 | 0 | 266 | 0 | $0.254242 | $0.000000 | $0.254242 |
| gpt-6-astra-subagent-new-r1 | True | 8 | 293,066 | 17,482 | 275,584 | 0 | 797 | 50 | $0.210168 | $0.280086 | $0.490254 |
| gpt-6-astra-subagent-patch-r1 | True | 5 | 171,732 | 12,756 | 158,976 | 0 | 435 | 0 | $0.129232 | $0.179054 | $0.308286 |
| gpt-6-astra-subagent-tuned-r1 | True | 5 | 156,869 | 9,029 | 147,840 | 0 | 415 | 13 | $0.130478 | $0.128402 | $0.258880 |
| gpt-6-astra-terminal-new-r1 | True | 9 | 139,249 | 8,177 | 131,072 | 0 | 357 | 24 | $0.230692 | $0.000000 | $0.230692 |
| gpt-6-astra-terminal-patch-r1 | True | 5 | 78,241 | 7,841 | 70,400 | 0 | 209 | 12 | $0.159260 | $0.000000 | $0.159260 |
| gpt-6-astra-terminal-tuned-r1 | True | 4 | 62,836 | 7,540 | 55,296 | 0 | 187 | 0 | $0.140046 | $0.000000 | $0.140046 |

## API-price breakdown

These disjoint dollar categories sum to Combined USD above; total input is not charged again.

| Trial | Ordinary input USD | Cached-read USD | Cache-write USD | Output USD |
|---|---:|---:|---:|---:|
| gpt-5.6-sol-ci-new-r1 | $0.032740 | $0.025856 | $0.000000 | $0.009900 |
| gpt-5.6-sol-ci-old-r1 | $0.125096 | $0.023091 | $0.000000 | $0.010460 |
| gpt-5.6-sol-ci-patch-r1 | $0.037256 | $0.032410 | $0.000000 | $0.013040 |
| gpt-5.6-sol-ci-tuned-r1 | $0.034088 | $0.032768 | $0.000000 | $0.010900 |
| gpt-5.6-sol-subagent-new-r1 | $0.031124 | $0.037120 | $0.000000 | $0.009000 |
| gpt-5.6-sol-subagent-old-r1 | $0.118820 | $0.034560 | $0.000000 | $0.010080 |
| gpt-5.6-sol-subagent-patch-r1 | $0.062576 | $0.035123 | $0.000000 | $0.009220 |
| gpt-5.6-sol-subagent-tuned-r1 | $0.078468 | $0.039680 | $0.000000 | $0.011520 |
| gpt-5.6-sol-terminal-new-r1 | $0.028988 | $0.020173 | $0.000000 | $0.005560 |
| gpt-5.6-sol-terminal-old-r1 | $0.092400 | $0.013978 | $0.000000 | $0.004520 |
| gpt-5.6-sol-terminal-patch-r1 | $0.031276 | $0.020429 | $0.000000 | $0.005480 |
| gpt-5.6-sol-terminal-tuned-r1 | $0.032392 | $0.020531 | $0.000000 | $0.006840 |
| gpt-6-astra-ci-new-r1 | $0.146030 | $0.109056 | $0.000000 | $0.012950 |
| gpt-6-astra-ci-patch-r1 | $0.122450 | $0.113920 | $0.000000 | $0.012300 |
| gpt-6-astra-ci-tuned-r1 | $0.126510 | $0.114432 | $0.000000 | $0.013300 |
| gpt-6-astra-subagent-new-r1 | $0.174820 | $0.275584 | $0.000000 | $0.039850 |
| gpt-6-astra-subagent-patch-r1 | $0.127560 | $0.158976 | $0.000000 | $0.021750 |
| gpt-6-astra-subagent-tuned-r1 | $0.090290 | $0.147840 | $0.000000 | $0.020750 |
| gpt-6-astra-terminal-new-r1 | $0.081770 | $0.131072 | $0.000000 | $0.017850 |
| gpt-6-astra-terminal-patch-r1 | $0.078410 | $0.070400 | $0.000000 | $0.010450 |
| gpt-6-astra-terminal-tuned-r1 | $0.075400 | $0.055296 | $0.000000 | $0.009350 |

## Parent and child token counts

| Trial | Scope | Responses | Input total | Ordinary input | Cached reads | Cache writes | Output |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| gpt-5.6-sol-ci-new-r1 | parent | 5 | 72,825 | 8,185 | 64,640 | 0 | 495 |
| gpt-5.6-sol-ci-old-r1 | parent | 6 | 89,002 | 31,274 | 57,728 | 0 | 523 |
| gpt-5.6-sol-ci-patch-r1 | parent | 6 | 90,338 | 9,314 | 81,024 | 0 | 652 |
| gpt-5.6-sol-ci-tuned-r1 | parent | 6 | 90,442 | 8,522 | 81,920 | 0 | 545 |
| gpt-5.6-sol-subagent-new-r1 | parent | 3 | 42,767 | 3,727 | 39,040 | 0 | 156 |
| gpt-5.6-sol-subagent-new-r1 | child | 4 | 57,814 | 4,054 | 53,760 | 0 | 294 |
| gpt-5.6-sol-subagent-old-r1 | parent | 3 | 43,091 | 17,875 | 25,216 | 0 | 156 |
| gpt-5.6-sol-subagent-old-r1 | child | 5 | 73,014 | 11,830 | 61,184 | 0 | 348 |
| gpt-5.6-sol-subagent-patch-r1 | parent | 3 | 43,930 | 3,994 | 39,936 | 0 | 167 |
| gpt-5.6-sol-subagent-patch-r1 | child | 4 | 59,522 | 11,650 | 47,872 | 0 | 294 |
| gpt-5.6-sol-subagent-tuned-r1 | parent | 4 | 59,268 | 11,524 | 47,744 | 0 | 248 |
| gpt-5.6-sol-subagent-tuned-r1 | child | 4 | 59,549 | 8,093 | 51,456 | 0 | 328 |
| gpt-5.6-sol-terminal-new-r1 | parent | 4 | 57,679 | 7,247 | 50,432 | 0 | 278 |
| gpt-5.6-sol-terminal-old-r1 | parent | 4 | 58,044 | 23,100 | 34,944 | 0 | 226 |
| gpt-5.6-sol-terminal-patch-r1 | parent | 4 | 58,891 | 7,819 | 51,072 | 0 | 274 |
| gpt-5.6-sol-terminal-tuned-r1 | parent | 4 | 59,426 | 8,098 | 51,328 | 0 | 342 |
| gpt-6-astra-ci-new-r1 | parent | 8 | 123,659 | 14,603 | 109,056 | 0 | 259 |
| gpt-6-astra-ci-patch-r1 | parent | 8 | 126,165 | 12,245 | 113,920 | 0 | 246 |
| gpt-6-astra-ci-tuned-r1 | parent | 8 | 127,083 | 12,651 | 114,432 | 0 | 266 |
| gpt-6-astra-subagent-new-r1 | parent | 8 | 123,302 | 7,974 | 115,328 | 0 | 302 |
| gpt-6-astra-subagent-new-r1 | child | 11 | 169,764 | 9,508 | 160,256 | 0 | 495 |
| gpt-6-astra-subagent-patch-r1 | parent | 5 | 78,474 | 4,362 | 74,112 | 0 | 230 |
| gpt-6-astra-subagent-patch-r1 | child | 6 | 93,258 | 8,394 | 84,864 | 0 | 205 |
| gpt-6-astra-subagent-tuned-r1 | parent | 5 | 78,844 | 4,476 | 74,368 | 0 | 227 |
| gpt-6-astra-subagent-tuned-r1 | child | 5 | 78,025 | 4,553 | 73,472 | 0 | 188 |
| gpt-6-astra-terminal-new-r1 | parent | 9 | 139,249 | 8,177 | 131,072 | 0 | 357 |
| gpt-6-astra-terminal-patch-r1 | parent | 5 | 78,241 | 7,841 | 70,400 | 0 | 209 |
| gpt-6-astra-terminal-tuned-r1 | parent | 4 | 62,836 | 7,540 | 55,296 | 0 | 187 |
