# Astra: 0.153.1 follow-up versus existing 0.154.0 controls

`old` = CLI 0.153.1 without the patch; `new` = CLI 0.154.0 without the patch; `patch` = CLI 0.154.0 with the frozen initial addition. Six new `old` trials are compared with twelve existing control trials. These were measured sequentially, not as new interleaved pairs.

Dollars are Standard API-rate equivalents of reported subscription counters, not charges. Cache writes are reported/defaulted zeros; actual writes are not separately recoverable. CLI 0.153.1 already includes PR #41243.

## Totals across all three workloads

Counts and dollars in this table are sums, including children. Compare conditions with the same number of trials.

| Model | Condition | Trials | Responses | Input total | Ordinary input | Cached reads | Writes reported | Output | API-rate USD |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| gpt-6-astra | old | 6 | 48 | 891,728 | 117,584 | 774,144 | 0 | 2,115 | $2.055734 |
| gpt-6-astra | new | 6 | 48 | 896,684 | 103,084 | 793,600 | 0 | 2,196 | $1.934240 |
| gpt-6-astra | patch | 6 | 41 | 781,473 | 84,257 | 697,216 | 0 | 2,098 | $1.644686 |

## Workload outcomes

Each row is the mean of its repetitions except maximum update gap. P+C means parent plus child responses. Costs include both.

| Model | Workload | Condition | n | Successes | P+C responses | API-rate USD | Result delay (s) | Maximum parent update gap (s) |
|---|---|---|---:|---:|---:|---:|---:|---:|
| gpt-6-astra | ci | old | 2 | 2 | 5+0 | $0.237727 | 58.85 | 69.16 |
| gpt-6-astra | ci | new | 2 | 2 | 5+0 | $0.243398 | 59.40 | 69.06 |
| gpt-6-astra | ci | patch | 2 | 2 | 5+0 | $0.185962 | 53.89 | 70.09 |
| gpt-6-astra | subagent | old | 2 | 2 | 4+7.5 | $0.510471 | 7.00 | 72.10 |
| gpt-6-astra | subagent | new | 2 | 2 | 4+7.5 | $0.441636 | 6.10 | 69.28 |
| gpt-6-astra | subagent | patch | 2 | 2 | 4+5.5 | $0.408623 | 5.19 | 71.01 |
| gpt-6-astra | terminal | old | 2 | 2 | 7.5+0 | $0.279669 | 8.00 | 77.62 |
| gpt-6-astra | terminal | new | 2 | 2 | 7.5+0 | $0.282086 | 3.27 | 79.92 |
| gpt-6-astra | terminal | patch | 2 | 2 | 6+0 | $0.227758 | 2.54 | 73.50 |

## Aggregate contrasts

Percent changes compare per-trial means; negative values are decreases. Small, non-randomized samples do not establish causal or population savings.

| Model | Comparison | Combined responses change | Inclusive input change | API-rate USD change |
|---|---|---:|---:|---:|
| gpt-6-astra | old → new | +0.00% | +0.56% | -5.91% |
| gpt-6-astra | new → patch | -14.58% | -12.85% | -14.97% |
