# Numeric wait overrides

This follow-up isolates numeric recommendations for `exec_command`, `write_stdin`,
and `functions.wait`. See [the predeclared plan](PLAN.md). The original
`functions.exec` 45-second pragma is common to every numeric-comparison condition.
The separate whole-section experiment removes all Terminal commands guidance,
including that pragma recommendation, while retaining the common 45-second ceiling.

The subsequent [outer-yield follow-up](OUTER_PLAN.md) tests the outer number and
explicit `functions.exec` naming independently. Its scope differs from the original
numeric tests; use the phase-specific frozen prompts and results.

Variant names encode explicit numbers: `e` = exec 30 seconds, `s` = empty stdin
40 seconds, `w` = functions.wait 45 seconds. `1` supplies the number; `0` retains
qualitative tool/budget guidance. `e1s0w0` is byte-identical to the previously
measured compact prompt. A zero is **not** an instruction to use the runtime
default, and it does not remove the other waiting rules.

| Variant | exec_command | write_stdin | functions.wait |
|---|---|---|---|
| e0s0w0 | Qualitative long wait | Qualitative | Qualitative |
| e1s0w0 (original control) | 30,000 ms | Qualitative | Qualitative |
| e0s1w0 | Qualitative long wait | 40,000 ms | Qualitative |
| e1s1w0 | 30,000 ms | 40,000 ms | Qualitative |
| e1s0w1 | 30,000 ms | Qualitative | 45,000 ms |
| e1s1w1 (combined candidate, if selected) | 30,000 ms | 40,000 ms | 45,000 ms |

Each numeric recommendation still permits shortening for the reporting budget.
All frozen variants are in [prompts](prompts/). The cell workload deliberately
uses a 1 ms initial outer yield to exercise a real running cell. Its initial code
is identical across both wait variants. Normal terminal runs exercise naturally
chosen calls. The command itself runs for 75 seconds in both workloads.

Run from the repository root; consumes live subscription usage:

```sh
python3 docs/waiting-benchmark/numeric-waits/run.py --prepare-only
python3 docs/waiting-benchmark/numeric-waits/run.py
python3 docs/waiting-benchmark/analyze.py \
  tmp/wait-benchmark-numeric-waits/isolated \
  --out docs/waiting-benchmark/numeric-waits/isolated-results
python3 docs/waiting-benchmark/numeric-waits/compare.py \
  tmp/wait-benchmark-numeric-waits/isolated \
  --out docs/waiting-benchmark/numeric-waits/isolated-results
```

`run.py` refuses to alter frozen prompts/manifests and skips existing trials.
Its optional `--phase integration --selected <variant>` compares a changed
candidate against the original control on fresh terminal/CI/subagent workloads.
The reused collector gains only an optional scenario-prompt argument; existing
historical benchmark behavior is preserved.

The user-requested `--phase section` compares the control against
[no-terminal](prompts/AGENTS.no-terminal.md), which deletes the entire Terminal
commands section. It uses two fresh repetitions per terminal/CI/subagent condition
(12 trials) and a separate shuffled [manifest](section-manifest.json). Run and export:

```sh
python3 docs/waiting-benchmark/numeric-waits/run.py --phase section
python3 docs/waiting-benchmark/analyze.py \
  tmp/wait-benchmark-numeric-waits/section \
  --out docs/waiting-benchmark/numeric-waits/section-results
python3 docs/waiting-benchmark/numeric-waits/compare.py \
  tmp/wait-benchmark-numeric-waits/section \
  --out docs/waiting-benchmark/numeric-waits/section-results
```

`analyze.py` performs the historical token and cumulative-counter reconciliation.
`compare.py` additionally checks cumulative coverage for every usage session,
low-effort contexts, exact final results, exit-zero output, expected child count,
and the forced cell path. Its argument projections are literal diagnostics;
the complete tool-call text is retained as the authority.

For cell trials, inspect the `functions.wait` calls separately from later stdin
calls. Two trials can use the identical cell-resumption call but differ in total
responses when a later wait ends just before command completion. Report the whole
trial's tokens and costs without attributing that difference to the wait clause.

Costs use the same September 14 Standard API rate card as the historical report.
Cache-write zeros may represent absent upstream fields. Cache-hit variation can
change dollar equivalents even when response counts and inclusive input are equal.
These amounts are not subscription charges. Investigation/reviewer usage is outside
the controlled trial totals.

## First 30 trials

All 30 initial trials completed successfully: 18 numeric comparisons and 12
whole-section comparisons, 135 unique responses, $4.790474 at the dated API rates.
This phase kept the outer 45-second pragma in numeric conditions and therefore could not
establish its necessity. Explicit stdin 40-second and functions.wait 45-second values showed no benefit;
exec 30-second guidance tied qualitative wording. Whole-section deletion increased responses from 33 to 36
and API valuation by 5.19%, with faster delivery. The later outer-yield study supersedes
the original decision to retain individual numbers merely for brevity.

- [Japanese report and decision](../../CODEX_WAITING_NUMERIC_OVERRIDES_BENCHMARK.md)
- [Numeric results](isolated-results/COMPARISON.md), [token/USD categories](isolated-results/COUNTS.md)
- [Section results](section-results/COMPARISON.md), [token/USD categories](section-results/COUNTS.md)

`e1s1w1` is a frozen candidate only; it was not selected or executed. The later
interrupted `integration --selected e0s0w0` attempt has no completed records; see its
ledger below. Do not infer zero consumption from the missing trial results.

## Outer yield and explicit tool name

`outer-o{0,1}n{0,1}` encodes outer numeric guidance and explicit naming respectively.
All four variants remove the initial exec 30-second number using the previously tested
qualitative text, retain the common 45-second waiting ceiling, and leave stdin and
functions.wait qualitative. The natural terminal comparison has three repetitions
per condition; its task does not force a short outer yield.

```sh
python3 docs/waiting-benchmark/numeric-waits/run.py --phase outer
python3 docs/waiting-benchmark/analyze.py \
  tmp/wait-benchmark-numeric-waits/outer \
  --out docs/waiting-benchmark/numeric-waits/outer-results
python3 docs/waiting-benchmark/numeric-waits/compare.py \
  tmp/wait-benchmark-numeric-waits/outer \
  --out docs/waiting-benchmark/numeric-waits/outer-results
```

After selecting the exact frozen variant, use `--phase outer-integration --selected
<variant>` for the two-repetition comparison against the original compact control
on terminal/CI/subagent. The subagent scenario explicitly requests `fork_turns:
"all"` in both conditions, and the exported acceptance checks verify it. Use the
matching `outer-integration` input/output paths when running the two analyzers.

The earlier interrupted `integration --selected e0s0w0` attempt has no completed
trial records. Its potentially consumed usage is unknown, not zero; it is recorded
in [the interruption ledger](interrupted-attempt.json) and is not reused.

## Final selection after outer-yield measurements

The selected current export is [outer-o0n0](prompts/AGENTS.outer-o0n0.md): qualitative
initial and outer waits, no added explicit functions.exec name, common 45-second cap
retained. [Final selection and hash](final-selection.json), [Japanese report](../../CODEX_WAITING_OUTER_EXEC_BENCHMARK.md).

The outer study executed 32 trials (12 factorial + 12 first confirmation + 4 CI naming
checks + 4 corrected subagent checks), with 140 unique responses and $5.063908 API valuation.
31 workloads completed; 29 passed every strict check. One candidate asked a question
before spawning, and two trials returned extra text/JSON instead of the exact marker.
All usage is retained. The selected wording passed all seven of its exposures across
three phases; these are not one fresh matched suite against the original.

- [Outer factorial](outer-results/COMPARISON.md)
- [First confirmation, including failure](outer-integration-results/COUNTS.md)
- [Bounded CI naming comparison](outer-ci-name-results/COMPARISON.md)
- [Corrected final subagent comparison](outer-subagent-unnamed-results/COMPARISON.md)

Additional phase commands used:

```sh
python3 docs/waiting-benchmark/numeric-waits/run.py --phase outer-ci-name
python3 docs/waiting-benchmark/numeric-waits/run.py \
  --phase outer-subagent-unnamed --selected outer-o0n0
```

Use each phase name in the input/output paths for analyze.py and compare.py, as in
the examples above. The named-candidate `outer-subagent` manifest was prepared but
not executed; final subagent confirmation used its separately named unnamed phase.
Historical prompts/manifests and measurements remain unchanged.
