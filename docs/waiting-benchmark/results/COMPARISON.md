# Waiting comparison tables

## Totals across all three workloads

Counts and dollars in this table are sums, including children. Compare conditions with the same number of trials.

| Model | Condition | Trials | Responses | Input total | Ordinary input | Cached reads | Writes reported | Output | API-rate USD |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| gpt-5.6-sol | old | 6 | 38 | 719,953 | 181,201 | 538,752 | 0 | 3,450 | $1.009305 |
| gpt-5.6-sol | new | 6 | 42 | 784,936 | 111,656 | 673,280 | 0 | 4,099 | $0.797916 |
| gpt-5.6-sol | patch | 6 | 39 | 713,699 | 78,179 | 635,520 | 0 | 3,213 | $0.631184 |
| gpt-6-astra | new | 6 | 48 | 896,684 | 103,084 | 793,600 | 0 | 2,196 | $1.934240 |
| gpt-6-astra | patch | 6 | 41 | 781,473 | 84,257 | 697,216 | 0 | 2,098 | $1.644686 |

## Workload outcomes

Each row is the mean of its repetitions except maximum update gap. P+C means parent plus child responses. Costs include both.

| Model | Workload | Condition | n | Successes | P+C responses | API-rate USD | Result delay (s) | Maximum parent update gap (s) |
|---|---|---|---:|---:|---:|---:|---:|---:|
| gpt-5.6-sol | ci | old | 2 | 2 | 7.5+0 | $0.149250 | 63.42 | 145.24 |
| gpt-5.6-sol | ci | new | 2 | 2 | 8+0 | $0.152052 | 93.18 | 133.63 |
| gpt-5.6-sol | ci | patch | 2 | 2 | 7.5+0 | $0.123029 | 108.77 | 167.85 |
| gpt-5.6-sol | subagent | old | 2 | 2 | 3+4 | $0.213811 | 6.45 | 92.36 |
| gpt-5.6-sol | subagent | new | 2 | 2 | 4.5+4 | $0.171187 | 6.54 | 106.20 |
| gpt-5.6-sol | subagent | patch | 2 | 2 | 3+5 | $0.132460 | 6.43 | 92.85 |
| gpt-5.6-sol | terminal | old | 2 | 2 | 4.5+0 | $0.141592 | 12.09 | 58.16 |
| gpt-5.6-sol | terminal | new | 2 | 2 | 4.5+0 | $0.075719 | 2.69 | 67.23 |
| gpt-5.6-sol | terminal | patch | 2 | 2 | 4+0 | $0.060103 | 1.87 | 44.04 |
| gpt-6-astra | ci | new | 2 | 2 | 5+0 | $0.243398 | 59.40 | 69.06 |
| gpt-6-astra | ci | patch | 2 | 2 | 5+0 | $0.185962 | 53.89 | 70.09 |
| gpt-6-astra | subagent | new | 2 | 2 | 4+7.5 | $0.441636 | 6.10 | 69.28 |
| gpt-6-astra | subagent | patch | 2 | 2 | 4+5.5 | $0.408623 | 5.19 | 71.01 |
| gpt-6-astra | terminal | new | 2 | 2 | 7.5+0 | $0.282086 | 3.27 | 79.92 |
| gpt-6-astra | terminal | patch | 2 | 2 | 6+0 | $0.227758 | 2.54 | 73.50 |

## Aggregate contrasts

Percent changes compare per-trial means; negative values are decreases. Small, non-randomized samples do not establish causal or population savings.

| Model | Comparison | Combined responses change | Inclusive input change | API-rate USD change |
|---|---|---:|---:|---:|
| gpt-5.6-sol | old → new | +10.53% | +9.03% | -20.94% |
| gpt-5.6-sol | new → patch | -7.14% | -9.08% | -20.90% |
| gpt-6-astra | new → patch | -14.58% | -12.85% | -14.97% |
