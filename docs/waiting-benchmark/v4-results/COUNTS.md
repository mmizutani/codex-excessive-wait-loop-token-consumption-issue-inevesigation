# Recorded waiting trials

API-price equivalents value the reported token categories at Standard rates. They are not subscription charges.
Input is the inclusive total. Ordinary input = input − cached reads − cache writes. Reasoning is included in output.

| Trial | Success | Parent responses | Input total | Ordinary input | Cached reads | Cache writes | Output | Included reasoning | Parent USD | Child USD | Combined USD |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gpt-5.6-sol-ci-tuned-r1 | True | 6 | 91,080 | 13,128 | 77,952 | 0 | 586 | 32 | $0.095413 | $0.000000 | $0.095413 |
| gpt-6-astra-ci-tuned-r1 | True | 4 | 63,863 | 11,767 | 52,096 | 0 | 525 | 25 | $0.196016 | $0.000000 | $0.196016 |

## API-price breakdown

These disjoint dollar categories sum to Combined USD above; total input is not charged again.

| Trial | Ordinary input USD | Cached-read USD | Cache-write USD | Output USD |
|---|---:|---:|---:|---:|
| gpt-5.6-sol-ci-tuned-r1 | $0.052512 | $0.031181 | $0.000000 | $0.011720 |
| gpt-6-astra-ci-tuned-r1 | $0.117670 | $0.052096 | $0.000000 | $0.026250 |

## Parent and child token counts

| Trial | Scope | Responses | Input total | Ordinary input | Cached reads | Cache writes | Output |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| gpt-5.6-sol-ci-tuned-r1 | parent | 6 | 91,080 | 13,128 | 77,952 | 0 | 586 |
| gpt-6-astra-ci-tuned-r1 | parent | 4 | 63,863 | 11,767 | 52,096 | 0 | 525 |
