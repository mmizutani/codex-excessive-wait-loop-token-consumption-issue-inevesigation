# Recorded waiting trials

API-price equivalents value the reported token categories at Standard rates. They are not subscription charges.
Input is the inclusive total. Ordinary input = input − cached reads − cache writes. Reasoning is included in output.

| Trial | Success | Parent responses | Input total | Ordinary input | Cached reads | Cache writes | Output | Included reasoning | Parent USD | Child USD | Combined USD |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gpt-6-astra-ci-outer-o0n0-r1 | True | 4 | 63,673 | 7,993 | 55,680 | 0 | 538 | 47 | $0.162510 | $0.000000 | $0.162510 |
| gpt-6-astra-ci-outer-o0n0-r2 | True | 5 | 79,952 | 8,272 | 71,680 | 0 | 574 | 41 | $0.183100 | $0.000000 | $0.183100 |
| gpt-6-astra-ci-outer-o0n1-r1 | True | 5 | 79,943 | 5,063 | 74,880 | 0 | 595 | 45 | $0.155260 | $0.000000 | $0.155260 |
| gpt-6-astra-ci-outer-o0n1-r2 | True | 5 | 79,891 | 5,011 | 74,880 | 0 | 528 | 46 | $0.151390 | $0.000000 | $0.151390 |

## API-price breakdown

These disjoint dollar categories sum to Combined USD above; total input is not charged again.

| Trial | Ordinary input USD | Cached-read USD | Cache-write USD | Output USD |
|---|---:|---:|---:|---:|
| gpt-6-astra-ci-outer-o0n0-r1 | $0.079930 | $0.055680 | $0.000000 | $0.026900 |
| gpt-6-astra-ci-outer-o0n0-r2 | $0.082720 | $0.071680 | $0.000000 | $0.028700 |
| gpt-6-astra-ci-outer-o0n1-r1 | $0.050630 | $0.074880 | $0.000000 | $0.029750 |
| gpt-6-astra-ci-outer-o0n1-r2 | $0.050110 | $0.074880 | $0.000000 | $0.026400 |

## Parent and child token counts

| Trial | Scope | Responses | Input total | Ordinary input | Cached reads | Cache writes | Output |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| gpt-6-astra-ci-outer-o0n0-r1 | parent | 4 | 63,673 | 7,993 | 55,680 | 0 | 538 |
| gpt-6-astra-ci-outer-o0n0-r2 | parent | 5 | 79,952 | 8,272 | 71,680 | 0 | 574 |
| gpt-6-astra-ci-outer-o0n1-r1 | parent | 5 | 79,943 | 5,063 | 74,880 | 0 | 595 |
| gpt-6-astra-ci-outer-o0n1-r2 | parent | 5 | 79,891 | 5,011 | 74,880 | 0 | 528 |
