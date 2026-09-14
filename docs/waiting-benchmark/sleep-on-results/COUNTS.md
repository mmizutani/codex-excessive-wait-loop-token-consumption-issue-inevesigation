# Recorded waiting trials

API-price equivalents value the reported token categories at Standard rates. They are not subscription charges.
Input is the inclusive total. Ordinary input = input − cached reads − cache writes. Reasoning is included in output.

| Trial | Success | Parent responses | Input total | Ordinary input | Cached reads | Cache writes | Output | Included reasoning | Parent USD | Child USD | Combined USD |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gpt-5.6-sol-ci-new-on-r1 | True | 8 | 117,686 | 18,230 | 99,456 | 0 | 487 | 25 | $0.122442 | $0.000000 | $0.122442 |
| gpt-5.6-sol-ci-tuned-on-r1 | True | 8 | 121,342 | 19,070 | 102,272 | 0 | 515 | 13 | $0.127489 | $0.000000 | $0.127489 |

## API-price breakdown

These disjoint dollar categories sum to Combined USD above; total input is not charged again.

| Trial | Ordinary input USD | Cached-read USD | Cache-write USD | Output USD |
|---|---:|---:|---:|---:|
| gpt-5.6-sol-ci-new-on-r1 | $0.072920 | $0.039782 | $0.000000 | $0.009740 |
| gpt-5.6-sol-ci-tuned-on-r1 | $0.076280 | $0.040909 | $0.000000 | $0.010300 |

## Parent and child token counts

| Trial | Scope | Responses | Input total | Ordinary input | Cached reads | Cache writes | Output |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| gpt-5.6-sol-ci-new-on-r1 | parent | 8 | 117,686 | 18,230 | 99,456 | 0 | 487 |
| gpt-5.6-sol-ci-tuned-on-r1 | parent | 8 | 121,342 | 19,070 | 102,272 | 0 | 515 |
