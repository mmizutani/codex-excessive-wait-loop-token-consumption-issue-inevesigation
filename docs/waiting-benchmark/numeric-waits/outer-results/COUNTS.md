# Recorded waiting trials

API-price equivalents value the reported token categories at Standard rates. They are not subscription charges.
Input is the inclusive total. Ordinary input = input − cached reads − cache writes. Reasoning is included in output.

| Trial | Success | Parent responses | Input total | Ordinary input | Cached reads | Cache writes | Output | Included reasoning | Parent USD | Child USD | Combined USD |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gpt-6-astra-terminal-outer-o0n0-r1 | True | 3 | 46,914 | 7,234 | 39,680 | 0 | 138 | 0 | $0.118920 | $0.000000 | $0.118920 |
| gpt-6-astra-terminal-outer-o0n0-r2 | True | 3 | 46,964 | 756 | 46,208 | 0 | 150 | 10 | $0.061268 | $0.000000 | $0.061268 |
| gpt-6-astra-terminal-outer-o0n0-r3 | True | 3 | 46,944 | 7,136 | 39,808 | 0 | 150 | 10 | $0.118668 | $0.000000 | $0.118668 |
| gpt-6-astra-terminal-outer-o0n1-r1 | True | 3 | 47,007 | 7,327 | 39,680 | 0 | 151 | 11 | $0.120500 | $0.000000 | $0.120500 |
| gpt-6-astra-terminal-outer-o0n1-r2 | True | 4 | 62,885 | 10,917 | 51,968 | 0 | 237 | 9 | $0.172988 | $0.000000 | $0.172988 |
| gpt-6-astra-terminal-outer-o0n1-r3 | True | 3 | 46,983 | 7,175 | 39,808 | 0 | 149 | 9 | $0.119008 | $0.000000 | $0.119008 |
| gpt-6-astra-terminal-outer-o1n0-r1 | True | 3 | 46,964 | 3,956 | 43,008 | 0 | 149 | 9 | $0.090018 | $0.000000 | $0.090018 |
| gpt-6-astra-terminal-outer-o1n0-r2 | True | 3 | 46,999 | 3,991 | 43,008 | 0 | 161 | 9 | $0.090968 | $0.000000 | $0.090968 |
| gpt-6-astra-terminal-outer-o1n0-r3 | True | 3 | 46,967 | 3,959 | 43,008 | 0 | 152 | 12 | $0.090198 | $0.000000 | $0.090198 |
| gpt-6-astra-terminal-outer-o1n1-r1 | True | 3 | 47,018 | 7,210 | 39,808 | 0 | 149 | 9 | $0.119358 | $0.000000 | $0.119358 |
| gpt-6-astra-terminal-outer-o1n1-r2 | True | 3 | 47,011 | 7,331 | 39,680 | 0 | 156 | 14 | $0.120790 | $0.000000 | $0.120790 |
| gpt-6-astra-terminal-outer-o1n1-r3 | True | 3 | 47,005 | 3,997 | 43,008 | 0 | 151 | 11 | $0.090528 | $0.000000 | $0.090528 |

## API-price breakdown

These disjoint dollar categories sum to Combined USD above; total input is not charged again.

| Trial | Ordinary input USD | Cached-read USD | Cache-write USD | Output USD |
|---|---:|---:|---:|---:|
| gpt-6-astra-terminal-outer-o0n0-r1 | $0.072340 | $0.039680 | $0.000000 | $0.006900 |
| gpt-6-astra-terminal-outer-o0n0-r2 | $0.007560 | $0.046208 | $0.000000 | $0.007500 |
| gpt-6-astra-terminal-outer-o0n0-r3 | $0.071360 | $0.039808 | $0.000000 | $0.007500 |
| gpt-6-astra-terminal-outer-o0n1-r1 | $0.073270 | $0.039680 | $0.000000 | $0.007550 |
| gpt-6-astra-terminal-outer-o0n1-r2 | $0.109170 | $0.051968 | $0.000000 | $0.011850 |
| gpt-6-astra-terminal-outer-o0n1-r3 | $0.071750 | $0.039808 | $0.000000 | $0.007450 |
| gpt-6-astra-terminal-outer-o1n0-r1 | $0.039560 | $0.043008 | $0.000000 | $0.007450 |
| gpt-6-astra-terminal-outer-o1n0-r2 | $0.039910 | $0.043008 | $0.000000 | $0.008050 |
| gpt-6-astra-terminal-outer-o1n0-r3 | $0.039590 | $0.043008 | $0.000000 | $0.007600 |
| gpt-6-astra-terminal-outer-o1n1-r1 | $0.072100 | $0.039808 | $0.000000 | $0.007450 |
| gpt-6-astra-terminal-outer-o1n1-r2 | $0.073310 | $0.039680 | $0.000000 | $0.007800 |
| gpt-6-astra-terminal-outer-o1n1-r3 | $0.039970 | $0.043008 | $0.000000 | $0.007550 |

## Parent and child token counts

| Trial | Scope | Responses | Input total | Ordinary input | Cached reads | Cache writes | Output |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| gpt-6-astra-terminal-outer-o0n0-r1 | parent | 3 | 46,914 | 7,234 | 39,680 | 0 | 138 |
| gpt-6-astra-terminal-outer-o0n0-r2 | parent | 3 | 46,964 | 756 | 46,208 | 0 | 150 |
| gpt-6-astra-terminal-outer-o0n0-r3 | parent | 3 | 46,944 | 7,136 | 39,808 | 0 | 150 |
| gpt-6-astra-terminal-outer-o0n1-r1 | parent | 3 | 47,007 | 7,327 | 39,680 | 0 | 151 |
| gpt-6-astra-terminal-outer-o0n1-r2 | parent | 4 | 62,885 | 10,917 | 51,968 | 0 | 237 |
| gpt-6-astra-terminal-outer-o0n1-r3 | parent | 3 | 46,983 | 7,175 | 39,808 | 0 | 149 |
| gpt-6-astra-terminal-outer-o1n0-r1 | parent | 3 | 46,964 | 3,956 | 43,008 | 0 | 149 |
| gpt-6-astra-terminal-outer-o1n0-r2 | parent | 3 | 46,999 | 3,991 | 43,008 | 0 | 161 |
| gpt-6-astra-terminal-outer-o1n0-r3 | parent | 3 | 46,967 | 3,959 | 43,008 | 0 | 152 |
| gpt-6-astra-terminal-outer-o1n1-r1 | parent | 3 | 47,018 | 7,210 | 39,808 | 0 | 149 |
| gpt-6-astra-terminal-outer-o1n1-r2 | parent | 3 | 47,011 | 7,331 | 39,680 | 0 | 156 |
| gpt-6-astra-terminal-outer-o1n1-r3 | parent | 3 | 47,005 | 3,997 | 43,008 | 0 | 151 |
