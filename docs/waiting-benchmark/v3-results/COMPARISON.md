# Waiting comparison tables

## Totals across all three workloads

Counts and dollars in this table are sums, including children. Compare conditions with the same number of trials.

| Model | Condition | Trials | Responses | Input total | Ordinary input | Cached reads | Writes reported | Output | API-rate USD |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| gpt-5.6-sol | tuned | 3 | 16 | 238,430 | 29,662 | 208,768 | 0 | 1,596 | $0.234075 |
| gpt-6-astra | tuned | 3 | 17 | 269,108 | 28,852 | 240,256 | 0 | 1,279 | $0.592726 |

## Workload outcomes

Each row is the mean of its repetitions except maximum update gap. P+C means parent plus child responses. Costs include both.

| Model | Workload | Condition | n | Successes | P+C responses | API-rate USD | Result delay (s) | Maximum parent update gap (s) |
|---|---|---|---:|---:|---:|---:|---:|---:|
| gpt-5.6-sol | ci | tuned | 1 | 1 | 4+0 | $0.057574 | 7.01 | 38.11 |
| gpt-5.6-sol | subagent | tuned | 1 | 1 | 4+4 | $0.117384 | 6.55 | 47.93 |
| gpt-5.6-sol | terminal | tuned | 1 | 1 | 4+0 | $0.059117 | 2.42 | 34.81 |
| gpt-6-astra | ci | tuned | 1 | 1 | 5+0 | $0.187448 | 26.00 | 44.18 |
| gpt-6-astra | subagent | tuned | 1 | 1 | 4+4 | $0.263254 | 9.56 | 48.36 |
| gpt-6-astra | terminal | tuned | 1 | 1 | 4+0 | $0.142024 | 5.62 | 43.68 |

## Aggregate contrasts

Percent changes compare per-trial means; negative values are decreases. Small, non-randomized samples do not establish causal or population savings.

| Model | Comparison | Combined responses change | Inclusive input change | API-rate USD change |
|---|---|---:|---:|---:|
