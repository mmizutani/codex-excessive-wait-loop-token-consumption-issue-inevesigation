# Waiting comparison tables

## Totals across all three workloads

Counts and dollars in this table are sums, including children. Compare conditions with the same number of trials.

| Model | Condition | Trials | Responses | Input total | Ordinary input | Cached reads | Writes reported | Output | API-rate USD |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| gpt-5.6-sol | old | 3 | 18 | 263,151 | 84,079 | 179,072 | 0 | 1,253 | $0.433005 |
| gpt-5.6-sol | new | 3 | 16 | 231,085 | 23,213 | 207,872 | 0 | 1,223 | $0.200461 |
| gpt-5.6-sol | patch | 3 | 17 | 252,681 | 32,777 | 219,904 | 0 | 1,387 | $0.246810 |
| gpt-5.6-sol | tuned | 3 | 18 | 268,685 | 36,237 | 232,448 | 0 | 1,463 | $0.267187 |
| gpt-6-astra | new | 3 | 36 | 555,974 | 40,262 | 515,712 | 0 | 1,413 | $0.988982 |
| gpt-6-astra | patch | 3 | 24 | 376,138 | 32,842 | 343,296 | 0 | 890 | $0.716216 |
| gpt-6-astra | tuned | 3 | 22 | 346,788 | 29,220 | 317,568 | 0 | 868 | $0.653168 |

## Workload outcomes

Each row is the mean of its repetitions except maximum update gap. P+C means parent plus child responses. Costs include both.

| Model | Workload | Condition | n | Successes | P+C responses | API-rate USD | Result delay (s) | Maximum parent update gap (s) |
|---|---|---|---:|---:|---:|---:|---:|---:|
| gpt-5.6-sol | ci | old | 1 | 1 | 6+0 | $0.158647 | 36.31 | 106.32 |
| gpt-5.6-sol | ci | new | 1 | 1 | 5+0 | $0.068496 | 32.53 | 72.47 |
| gpt-5.6-sol | ci | patch | 1 | 1 | 6+0 | $0.082706 | 14.81 | 47.87 |
| gpt-5.6-sol | ci | tuned | 1 | 1 | 6+0 | $0.077756 | 19.63 | 51.51 |
| gpt-5.6-sol | subagent | old | 1 | 1 | 3+5 | $0.163460 | 7.55 | 91.53 |
| gpt-5.6-sol | subagent | new | 1 | 1 | 3+4 | $0.077244 | 5.14 | 88.16 |
| gpt-5.6-sol | subagent | patch | 1 | 1 | 3+4 | $0.106919 | 4.74 | 89.59 |
| gpt-5.6-sol | subagent | tuned | 1 | 1 | 4+4 | $0.129668 | 7.59 | 57.75 |
| gpt-5.6-sol | terminal | old | 1 | 1 | 4+0 | $0.110898 | 2.43 | 79.70 |
| gpt-5.6-sol | terminal | new | 1 | 1 | 4+0 | $0.054721 | 2.01 | 35.29 |
| gpt-5.6-sol | terminal | patch | 1 | 1 | 4+0 | $0.057185 | 2.44 | 67.47 |
| gpt-5.6-sol | terminal | tuned | 1 | 1 | 4+0 | $0.059763 | 2.86 | 60.38 |
| gpt-6-astra | ci | new | 1 | 1 | 8+0 | $0.268036 | 11.00 | 58.15 |
| gpt-6-astra | ci | patch | 1 | 1 | 8+0 | $0.248670 | 58.11 | 72.78 |
| gpt-6-astra | ci | tuned | 1 | 1 | 8+0 | $0.254242 | 43.88 | 61.05 |
| gpt-6-astra | subagent | new | 1 | 1 | 8+11 | $0.490254 | 7.01 | 82.37 |
| gpt-6-astra | subagent | patch | 1 | 1 | 5+6 | $0.308286 | 7.90 | 69.04 |
| gpt-6-astra | subagent | tuned | 1 | 1 | 5+5 | $0.258880 | 5.74 | 57.28 |
| gpt-6-astra | terminal | new | 1 | 1 | 9+0 | $0.230692 | 4.79 | 77.56 |
| gpt-6-astra | terminal | patch | 1 | 1 | 5+0 | $0.159260 | 4.30 | 63.83 |
| gpt-6-astra | terminal | tuned | 1 | 1 | 4+0 | $0.140046 | 2.46 | 65.37 |

## Aggregate contrasts

Percent changes compare per-trial means; negative values are decreases. Small, non-randomized samples do not establish causal or population savings.

| Model | Comparison | Combined responses change | Inclusive input change | API-rate USD change |
|---|---|---:|---:|---:|
| gpt-5.6-sol | old → new | -11.11% | -12.19% | -53.70% |
| gpt-5.6-sol | new → patch | +6.25% | +9.35% | +23.12% |
| gpt-5.6-sol | new → tuned | +12.50% | +16.27% | +33.29% |
| gpt-5.6-sol | patch → tuned | +5.88% | +6.33% | +8.26% |
| gpt-6-astra | new → patch | -33.33% | -32.35% | -27.58% |
| gpt-6-astra | new → tuned | -38.89% | -37.63% | -33.96% |
| gpt-6-astra | patch → tuned | -8.33% | -7.80% | -8.80% |
