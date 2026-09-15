# Runtime evaluation of the Codex waiting skill

September 15, 2026. Codex CLI 0.154.0, GPT-6 Astra, low reasoning effort.

## TL;DR

- **Evaluated 66 real Astra/low trials** following OpenAI's skill-evaluation workflow. All requested outcomes were correct; all response counters reconciled. Failures and rejected candidates are retained.
- **Use [the final v4 skill](../../skills/codex-wait-efficiently/SKILL.md)** for the skill alternative. It adds 31 words to the original: clearer bounded CI watchers and explicit skill invocation in delegated waiting work. All three final child trials read the skill and avoided short polls.
- **Waiting inefficiency remains.** Across its 12-case suite and two handoff trials, the final skill passed 13/14 trials' deterministic checks; one CI run still used a one-second cell wait. Watcher startup and outer waits were not consistently followed.
- **Revising the skill did not demonstrate general savings.** Across the same 12-case suite, the original used **57 responses / $1.856236**, and the final skill used **58 / $1.945212**. These are API-price equivalents of subscription counters. A subsequent [18-trial comparison against no skill](CODEX_WAITING_SKILL_VS_NO_SKILL_BENCHMARK.md) measured 36.00% fewer responses and 27.93% lower API valuation overall, with higher CI cost and latency. There is still no direct skill-versus-AGENTS comparison.

## What was evaluated

The original skill packaged the final AGENTS.md patch as a discoverable skill. This evaluation follows [OpenAI's “Testing Agent Skills Systematically with Evals” workflow](https://developers.openai.com/blog/eval-skills): define observable success before editing, test explicit and implicit activation plus negative controls, inspect execution evidence, and revise against observed failures. A structured, independent model review supplements deterministic checks.

The installable package is [skills/codex-wait-efficiently](../../skills/codex-wait-efficiently/SKILL.md). The [fixtures, frozen versions, graders, and results](../../skills/codex-wait-efficiently/evals/README.md) are bundled in its `evals/` directory. Normal use loads the self-contained `SKILL.md`; it does not instruct Codex to read the evaluation suite. Optional Codex UI metadata lives in `agents/openai.yaml`. Waiting requires no helper scripts or external instruction dependencies. The evaluation tools use collectors and fixtures elsewhere in this repository. Implicit invocation remains enabled by default.

This 66-trial evaluation compares the original and revised skill. It is separate from the earlier [AGENTS.md versus no-patch experiment](CODEX_WAITING_LATEST_VS_NO_PATCH_BENCHMARK.md) and the subsequent [final-skill versus no-skill experiment](CODEX_WAITING_SKILL_VS_NO_SKILL_BENCHMARK.md). The latter adds a no-skill control without changing the evidence below. No skill-versus-AGENTS comparison has been run.

## Cases and controls

The [plan](../../skills/codex-wait-efficiently/evals/PLAN.md) and [12 prompts](../../skills/codex-wait-efficiently/evals/cases.json) were frozen before discovery. The suite contains:

| Case | Invocation | Observable requirement |
| --- | --- | --- |
| Long terminal command | Explicit | Start once, wait for completion, report its actual result. |
| Long terminal command | Implicit | Discover the skill from the task and complete the command. |
| CI without notifications or watch mode | Implicit/contextual | Monitor the existing run through a bounded scriptable watcher. |
| Real subagent | Implicit | Create exactly one child with the same model/effort, await its actual result. |
| Forced early Code Mode yield | Explicit | Resume the same running cell before polling its inner process again. |
| Command exits with status 7 | Explicit | Report the observed failure and exit code without retrying. |
| At most three CI checks | Explicit | Respect the total check limit and report pending state without altering the job. |
| Independent calculation while a command runs | Explicit | Write the correct sum before command completion. |
| Quick command | Negative | Return 42 without loading the waiting skill. |
| Single CI snapshot | Negative | Check once; do not wait or start a watcher. |
| Conceptual `wait`/`sleep` explanation | Negative | Explain without tools or skill loading. |
| Small documentation edit | Negative | Make the requested edit without monitoring work or loading the skill. |

Each trial used a fresh temporary Codex home and workspace, existing subscription authentication, and the same pinned model catalog as the preceding investigation. There was **no AGENTS.md**. Bundled skills were disabled, unrelated shared skills were disabled by name, and a real `skills/list` call verified that only the target skill was enabled before each turn. The observed name list contained 49 unrelated skills; the isolation assertion checks the actual resulting catalog rather than trusting that count.

The runtime configuration enabled multi-agent support and left `sleep_tool` at its default. It did not install the global waiting patch or require `always_on` sleep exposure.

Explicit cases supplied the normal skill attachment and a named prompt. Implicit cases and negative controls received the task and discovery metadata. Activation required evidence that the skill body had been loaded, not merely listed in the catalog or mentioned in an assistant update. The captured runs loaded the body through file reads; an explicit attachment alone was not treated as proof of body injection.

Long core jobs lasted 75 seconds. The failure case lasted eight seconds. The pending CI fixture remained unfinished throughout its observation. CI was a local status-command simulator, and the subagent was a real Codex child session. Each trial had a finite driver deadline and event limit, with at most two workload trials running concurrently. Completion, artifact timing, actual CI query counts, process outputs, parent/child inference, and progress-message timestamps were recorded.

The existing app-server collector provided structured execution and response accounting. The qualitative reviewer used a separate, read-only `codex exec --json --output-schema` invocation with the captured evidence and a fixed rubric. It received no prior conversation or proposed fix. Its usage is reported separately from workload totals.

## What the original skill missed and what changed

All 12 original discovery trials passed the deterministic activation and outcome checks. Full traces revealed two CI process issues:

1. **Separate model calls between scriptable checks.** In `v1-explicit-observation-limit-r1`, Codex made three status-command calls separated by two direct timers. It returned the correct pending result within the requested count, but did not use the available bounded-watcher approach. The independent reviewer also marked watcher choice as a failure.
2. **CI watcher waits did not consistently inherit the terminal rules.** In `v1-contextual-ci-r1`, Codex launched a long watcher with a 1,000-ms initial yield, then initially left the outer Code Mode wait at its default around a 45,000-ms inner `write_stdin`. An additional model response was needed to resume the outer cell. The watcher itself was bounded and ultimately completed correctly.

The first candidate, v2, changed only the first CI paragraph to keep repeated checks inside one watcher and explicitly refer to the Terminal commands rules. It improved the limited-observation discovery case, but its contextual-CI run repeated both the short startup yield and the mismatched outer wait. That result prompted one further revision, rather than treating the deterministic pass count as sufficient.

The longer candidate, v3, stated watcher-startup and outer waits directly. It still used a short startup yield in both CI cases, repeated the mismatched outer wait in contextual CI, and missed the parent update cadence once (68.464 seconds). This small sample does not establish that its extra wording caused the missed update. It did not demonstrate added value, so v2 was selected for the interleaved comparison.

The v2 CI paragraph, retained in the final v4 skill, is:

> Retain job identity; prefer completion notifications. Otherwise, keep repeated scriptable checks inside one shell watcher, bounded by time or total check count, including any initial query in the user's limit. Apply the Terminal commands rules to that watcher and retain its session; emit only meaningful changes. Choose intervals for acceptable result delay; back off unchanged status.

This adds 18 whitespace-delimited words. It makes the connection between a shell watcher and terminal waits explicit, and retains the user's total observation budget when checks move into a watcher. No fixed wait duration is added. No original trial exceeded its check limit; that clarification preserves a requirement rather than fixing an observed overrun. The trigger description, UI metadata, and all other operational paragraphs are unchanged. The AGENTS.md patch itself remains unchanged.

The interleaved comparison then exposed a different assumption. In `confirmation/v2-implicit-subagent-r1`, the parent read the skill and used direct agent waits, but its child showed no fresh skill read/injection, made a one-second `write_stdin` request, and briefly resumed a running cell with one second. The job completed correctly, using 14 combined responses. `fork_turns: all` may have made earlier context available; the evidence does not prove the child lacked that context. It does show that the parent's skill read did not establish child compliance.

**The final v4 skill adds an explicit handoff instruction:**

> When delegating work that includes waiting, include `Use $codex-wait-efficiently` in the child's task.

This adds 13 words to v2. The final package adds 31 words to v1 in total and retains the original trigger metadata. It does not add repeated reminders to already running children. Two dedicated actual-child trials test the handoff before the final complete suite.

The [revision log](../../skills/codex-wait-efficiently/evals/REVISIONS.md) preserves the reasoning. All four versions were frozen and tested against the same 12 cases. The separate confirmation block compares v1 and v2 in shuffled, interleaved order: two fresh repetitions each of the affected observation case, implicit terminal work, contextual CI, and a real subagent. The two v4 handoff trials bring the total to 66. Every trial is retained. The prepared v1/v3 confirmation manifest was never executed after v3 was rejected; its unused manifest is retained.

## Results

### Complete 12-case suites

| Version | Expected activation/non-activation | Correct outcomes | All deterministic checks | Responses | Input total | Ordinary input | Cached reads | Recorded writes | Output | API equivalent |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| v1, original | 12/12 | 12/12 | 12/12 | 57 | 920,336 | 83,600 | 836,736 | 0 | 3,670 | $1.856236 |
| v2, compact CI revision | 12/12 | 12/12 | 12/12 | 56 | 902,895 | 72,431 | 830,464 | 0 | 3,729 | $1.741224 |
| v3, rejected longer candidate | 12/12 | 12/12 | 11/12 | 56 | 907,181 | 88,365 | 818,816 | 0 | 3,695 | $1.887216 |
| v4, final skill | 12/12 | 12/12 | 11/12 | 58 | 941,366 | 90,294 | 851,072 | 0 | 3,824 | $1.945212 |

Each suite loaded the skill in all eight intended cases and left it unloaded in all four negative controls. The v3 failure was its 68.464-second parent progress gap; the CI job completed correctly and remains in all totals. V2's one-response aggregate reduction and 6.20% lower API valuation in these separate suite blocks are modest observations, not sufficient evidence of a general saving.

### Fresh interleaved confirmation

Both versions have two fresh trials per row. Counts and costs include parent and child inference.

| Workload | Responses v1 → v2 | API equivalent v1 → v2 | Mean delivery delay v1 → v2 |
| --- | ---: | ---: | ---: |
| Three-check observation | 14 → 8 | $0.362898 → $0.254952 | — → — |
| CI completion | 14 → 14 | $0.481164 → $0.399198 | 36.075 s → 30.883 s |
| Terminal | 9 → 10 | $0.257040 → $0.317310 | 3.157 s → 6.098 s |
| Subagent | 20 → 24 | $0.756618 → $0.745752 | 4.745 s → 5.635 s |

The observation case used a watcher in all three v2 runs across its suite and confirmation, versus separate status/timer model calls in all three v1 runs. However, the mean first-to-last query window in confirmation also shortened from **72.575 to 38.529 seconds**. Each run made three actual status requests. The response reduction combines batching with a shorter observation window; it does not isolate batching at fixed intervals.

The confirmation totals were **57 → 56 responses**, **944,778 → 934,510 input tokens**, and **$1.857720 → $1.717212 API equivalent**. All 16 outcomes were correct. V1 passed all deterministic checks in 8/8 trials; v2 passed 7/8 because of the retained child polling failure. This does not establish a meaningful general efficiency improvement.

### Final v4 suite and handoff checks

The final complete suite had correct activation/non-activation and outcomes in **12/12 cases**, with **11/12 passing all deterministic checks**. Its CI completion case still launched the watcher with a one-second yield, initially omitted an outer wait covering the 45-second inner wait, and resumed the resulting cell once with one second. It then resumed the same cell properly and delivered the correct result. Parent progress gaps stayed within 60 seconds in all eight positive cases.

Together with the two dedicated handoff trials, v4 had **14/14 correct outcomes and 13/14 complete deterministic passes**. In all three actual-child cases, the child read the skill and avoided the short-poll failure seen once in v2. Each used ten combined responses. The two dedicated runs consumed 20 responses, 318,836 input tokens (19,700 ordinary; 299,136 cached; zero recorded writes), 1,192 output tokens, and $0.555736 API equivalent. These few successful handoffs do not establish a population failure rate or universal propagation.

The final full-suite total is one response higher and 4.79% more expensive than the original suite. This is not a randomized final-versus-original comparison. Cache variation matters: the final negative documentation-edit case never loaded the skill, yet its API valuation was higher than the original's. The final limited-observation case used a watcher and six responses, versus the original discovery run's seven; its first-to-last query window was also shorter. The evidence supports a narrower behavioral clarification, not a demonstrated general efficiency gain.

Across **all eight contextual-CI trials**, every version requested a one-second watcher-startup yield. V3's additional direct wording did not change that pattern. In the final limited-observation case, the watcher also printed unchanged states. These are observed limits of instruction following; outcome and accounting checks alone do not establish full compliance with every skill rule.

The independent final reviewer examined nine traces and marked all applicable identity, watcher-choice, watcher-bound, state-reporting, and scope criteria as passing. It made no tool calls, and all cited call IDs were valid. This rubric does not grade wait-duration efficiency or every output-style requirement; it therefore does not override the recorded one-second cell-wait failure or the manual findings above.

### Dollar components by evaluation block

| Block | Trials | Ordinary input USD | Cached-read USD | Recorded-write USD | Output USD | Total API equivalent |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| discovery / v1 | 12 | $0.836000 | $0.836736 | $0.000000 | $0.183500 | $1.856236 |
| revised / v2 | 12 | $0.724310 | $0.830464 | $0.000000 | $0.186450 | $1.741224 |
| sharpened / v3 | 12 | $0.883650 | $0.818816 | $0.000000 | $0.184750 | $1.887216 |
| confirmation / v1 | 8 | $0.801380 | $0.864640 | $0.000000 | $0.191700 | $1.857720 |
| confirmation / v2 | 8 | $0.648780 | $0.869632 | $0.000000 | $0.198800 | $1.717212 |
| handoff / v4 | 2 | $0.197000 | $0.299136 | $0.000000 | $0.059600 | $0.555736 |
| final-suite / v4 | 12 | $0.902940 | $0.851072 | $0.000000 | $0.191200 | $1.945212 |
| All workload trials | 66 | $4.994060 | $5.370496 | $0.000000 | $1.196000 | $11.560556 |

All workload trials total **360 unique responses, 5,869,902 input tokens** (499,406 ordinary; 5,370,496 cached reads; zero recorded writes), **23,920 output tokens**, and **$11.560556 API equivalent**. The [per-trial score table](../../skills/codex-wait-efficiently/evals/results/final/SCORES.md) summarizes each run. The [machine-readable scores](../../skills/codex-wait-efficiently/evals/results/final/scores.json) additionally separate parent and child accounting.

### Separate reviewer usage

| Review | Input / ordinary input | Cached reads | Recorded writes | Output | API equivalent |
| --- | ---: | ---: | ---: | ---: | ---: |
| Original review | 29,285 | 0 | 0 | 3,399 | $0.462800 |
| Final review | 30,960 | 0 | 0 | 3,639 | $0.491550 |

These two review runs consumed 60,245 input tokens and 7,038 output tokens, valued at **$0.954350** separately from the workloads. Their [reported counters and valuation](../../skills/codex-wait-efficiently/evals/results/reviewer-usage.json) are retained.

## Interpreting the accounting

Input is the inclusive total. The disjoint charged input categories are ordinary input, cached reads, and recorded cache writes:

`ordinary input = total input − cached reads − recorded cache writes`

The tables include parent and child responses, skill discovery/read overhead, and failed checks. Reasoning tokens are included in output, not added again. Per-response counts are deduplicated by response ID and reconciled to each session's cumulative counters.

Workload totals exclude this authoring conversation. The separate trace-reviewer's usage is listed separately; the report does not measure the total account usage of conducting the investigation.

Dollar figures use the study's **September 14, 2026 Standard API rate card**, in USD per million tokens: ordinary input $10, cached reads $1, cache writes $12.50, output $50. These are valuations of reported subscription tokens, **not subscription charges or measured quota percentages**. They are not a fresh claim about today's pricing. The existing [accounting implementation](../waiting-benchmark/accounting.py) applies the dated rate card consistently to both versions. No request here crossed its long-context pricing threshold.

Recorded cache-write counts are zero. The collector/runtime may normalize an absent upstream write field to zero, so these records do not establish that the service performed no cache writes. Cache warmness and scheduling were not controlled; a small dollar difference with unchanged response counts can reflect cache variation.

## Review quality and limitations

The deterministic checks are tested against deliberately bad records, including an early stop, catalog-only activation, an extra status request, and incorrect failure handling. Their aggregate pass flag does **not** cover every qualitative instruction. Watcher choice, bounds, session identity, and state reporting are also reviewed against complete calls and outputs.

The original independent review marked the initial CI report uncertain because its reduced input accidentally omitted a status output bundled with a skill read. The complete evidence contains that status and supports the report. The review-input filter was corrected to retain sibling command outputs while omitting only the skill body. The original judgment remains available; the correction changes no workload or usage record. Model judgments are supporting evidence, not an automatic correctness oracle.

These are small, targeted Astra samples. They do not measure Sol, production CI integrations, every notification path, long-term cache retention, or `/goal` pause transitions. Those skill rules remain unchanged, but were not behaviorally validated by this suite. The forced early-yield case tests actual cell resumption; it is deliberately artificial and should not be read as a normal-use failure rate.

Successful automatic activation in these prompts does not guarantee selection in every future session. Loading a skill also has overhead; these results do not establish that installing this skill costs less than the AGENTS.md method. Latency and external service request counts must be assessed separately from model-response reductions.

## Files and reproduction

Install the complete [current skill directory](../../skills/codex-wait-efficiently/SKILL.md), following the [root README](../../README.md#skill-alternative). Replace a prior copy of this skill; avoid loading duplicate waiting rules through both installation methods.

See [evaluation commands and prerequisites](../../skills/codex-wait-efficiently/evals/README.md) for replay. Fresh live runs consume normal account usage. Exported evidence contains selected calls, outputs, fixtures, and counters; authentication and complete private instruction/session logs are excluded.

| Evidence | Purpose |
| --- | --- |
| [Final skill package validation](../waiting-validation/skill-package-validation.json) | Exact v4 hash, structural validity, and actual CLI discovery. |
| [Frozen versions and revision log](../../skills/codex-wait-efficiently/evals/REVISIONS.md) | Every candidate and the evidence behind the changes. |
| [Per-trial scores](../../skills/codex-wait-efficiently/evals/results/final/SCORES.md) | Activation, failed checks, counts, API valuation, and latency. |
| [Captured trial evidence](../../skills/codex-wait-efficiently/evals/results/final/trial-evidence.json) | All 66 workloads, including rejected candidates and retained failures. |
| [Integrity verification](../../skills/codex-wait-efficiently/evals/results/final/validation.json) | Unique response IDs, reconciled counters, complete manifests, and unchanged AGENTS.md patch. |
| [CI trace summary](../../skills/codex-wait-efficiently/evals/results/final/ci-trace-summary.json) | Watcher call IDs, startup yields, actual query counts, and observation windows. |
| [Original trace review](../../skills/codex-wait-efficiently/evals/results/discovery-judge.json) | Independent rubric review with the original uncertainty preserved. |
| [Final trace review](../../skills/codex-wait-efficiently/evals/results/final-judge.json) | Independent review of the final complete suite. |

The final skill SHA-256 is `14bc9f85b382ba1bc313246b23dff2b6e205cc75d880ab8a9160e5fc8514f173`. Run `python3 skills/codex-wait-efficiently/evals/verify.py` to recheck the exported evidence without inference.
