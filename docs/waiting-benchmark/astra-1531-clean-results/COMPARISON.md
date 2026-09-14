# Astra: clean 0.153.1 follow-up versus existing 0.154.0 controls

`old` = CLI 0.153.1 without the patch; `new` = CLI 0.154.0 without the patch; `patch` = CLI 0.154.0 with the frozen initial addition. Three new `old` trials are compared with six existing control trials, with shared skill instructions disabled. These were measured sequentially, not as new interleaved pairs.

Dollars are Standard API-rate equivalents of reported subscription counters, not charges. Cache writes are reported/defaulted zeros; actual writes are not separately recoverable. CLI 0.153.1 already includes PR #41243.

## Totals across all three workloads

Counts and dollars in this table are sums, including children. Compare conditions with the same number of trials.

| Model | Condition | Trials | Responses | Input total | Ordinary input | Cached reads | Writes reported | Output | API-rate USD |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| gpt-6-astra | old | 3 | 30 | 464,030 | 29,470 | 434,560 | 0 | 1,258 | $0.792160 |
| gpt-6-astra | new | 3 | 36 | 555,974 | 40,262 | 515,712 | 0 | 1,413 | $0.988982 |
| gpt-6-astra | patch | 3 | 24 | 376,138 | 32,842 | 343,296 | 0 | 890 | $0.716216 |

## Workload outcomes

Each row is the mean of its repetitions except maximum update gap. P+C means parent plus child responses. Costs include both.

| Model | Workload | Condition | n | Successes | P+C responses | API-rate USD | Result delay (s) | Maximum parent update gap (s) |
|---|---|---|---:|---:|---:|---:|---:|---:|
| gpt-6-astra | ci | old | 1 | 1 | 6+0 | $0.141836 | 32.56 | 56.74 |
| gpt-6-astra | ci | new | 1 | 1 | 8+0 | $0.268036 | 11.00 | 58.15 |
| gpt-6-astra | ci | patch | 1 | 1 | 8+0 | $0.248670 | 58.11 | 72.78 |
| gpt-6-astra | subagent | old | 1 | 1 | 4+9 | $0.367914 | 6.18 | 68.94 |
| gpt-6-astra | subagent | new | 1 | 1 | 8+11 | $0.490254 | 7.01 | 82.37 |
| gpt-6-astra | subagent | patch | 1 | 1 | 5+6 | $0.308286 | 7.90 | 69.04 |
| gpt-6-astra | terminal | old | 1 | 1 | 11+0 | $0.282410 | 2.74 | 78.75 |
| gpt-6-astra | terminal | new | 1 | 1 | 9+0 | $0.230692 | 4.79 | 77.56 |
| gpt-6-astra | terminal | patch | 1 | 1 | 5+0 | $0.159260 | 4.30 | 63.83 |

## Aggregate contrasts

Percent changes compare per-trial means; negative values are decreases. Small, non-randomized samples do not establish causal or population savings.

| Model | Comparison | Combined responses change | Inclusive input change | API-rate USD change |
|---|---|---:|---:|---:|
| gpt-6-astra | old → new | +20.00% | +19.81% | +24.85% |
| gpt-6-astra | new → patch | -33.33% | -32.35% | -27.58% |
