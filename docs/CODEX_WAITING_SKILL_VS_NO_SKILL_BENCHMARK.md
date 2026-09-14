# Final Codex waiting skill versus no skill

September 15, 2026 (JST). Codex CLI 0.154.0, GPT-6 Astra, low reasoning effort.

## TL;DR

- **The final v4 skill reduced usage overall in this 18-trial comparison:** model responses **100 → 64 (−36.00%)**, input tokens **1,547,548 → 1,028,592 (−33.53%)**, and API-price equivalent **$2.705112 → $1.949598 (−27.93%)**.
- **The benefit came from terminal and subagent waiting.** Their API valuations fell 39.93% and 39.26%. CI used fewer responses but cost **12.87% more**; actual CI requests stayed at 12 per condition.
- **All 18 tasks returned correct results.** The skill loaded in all nine treatment parents and three treatment children. All nine treatment trials passed the deterministic checks. One-second `write_stdin` requests fell from 39 to zero.
- **Results arrived later in 8/9 pairs.** Mean extra delay was 0.25 seconds for terminal work, 7.82 seconds for subagents, and 25.27 seconds for CI. Short watcher startup waits and some outer/inner wait mismatches remained.
- This establishes an observed benefit for this mix of 75-second Astra workloads. It does not establish universal savings, subscription billing savings, or that the skill is cheaper than AGENTS.md.

## Why another comparison was needed

The [earlier 66-trial evaluation](CODEX_WAITING_SKILL_EVALUATION.md) tested the original skill and three revisions, activation, task correctness, and waiting behavior. Its original-versus-final 12-case suites used 57 versus 58 responses and $1.856236 versus $1.945212 API equivalent. That comparison could not answer whether installing the final skill saves usage compared with having no skill.

This new experiment compares **no skill** directly with the unchanged final **v4 skill**. The [plan](../skills/codex-wait-efficiently/evals/comparisons/skill-vs-none/PLAN.md) and [18-trial manifest](../skills/codex-wait-efficiently/evals/comparisons/skill-vs-none/skill-vs-none.json) were frozen before inference. The prior evidence, skill body, and AGENTS.md patch remain unchanged.

## Conditions and method

| Setting | No skill | Final v4 skill |
| --- | --- | --- |
| Model and effort | GPT-6 Astra / low | GPT-6 Astra / low |
| Runtime | Codex CLI 0.154.0 | Codex CLI 0.154.0 |
| AGENTS.md patch | Absent | Absent |
| Enabled skills | None | Only `codex-wait-efficiently` |
| Invocation | Identical task prompt, no skill mention or attachment | Same task prompt, normal automatic selection |
| Bundled and unrelated shared skills | Disabled | Disabled |
| `sleep_tool` | Runtime default | Runtime default |
| Workloads | Terminal, real subagent, local CI simulator | Same three workloads |
| Repetitions | Three per workload; nine trials | Three per workload; nine trials |

Each workload lasts 75 seconds. The terminal case starts one command and awaits its result. The subagent case delegates that command once to one child using `fork_turns: all`, inheriting Astra/low without model or effort overrides. The CI case monitors an existing simulated run via its authoritative status command, with no built-in watcher or completion notifications. No independent work remains in these tasks.

Every trial uses a fresh temporary Codex home and workspace. The actual enabled skill catalog is checked before the turn. The control disables any shared copy of the target skill as well as unrelated skills. Captured control sessions show neither the target skill in a catalog nor skill-body loading. All treatment parents and children loaded the skill body through observed reads. Skill loading and child inference are included in treatment usage.

The task prompts and fixtures are identical across matched workload/repetition pairs. The model catalog is pinned to the previous study's hash, `e17cbd5fba8d477929a6a57f3d522325c488acb5e2f488e267aa59f3f239ba40`. Every recorded parent/child model context was Astra/low; all base instruction hashes matched. Both conditions use the same runtime options except the target skill installation and its enabled/disabled setting.

The complete schedule was shuffled with seed 20260915 and run with at most two concurrent trials. Pairs identify the same task and repetition; paired runs were not necessarily adjacent. Cache state and backend scheduling were uncontrolled. The existing deadline and item limit bound each run. No trial was discarded or repeated because of unfavorable results.

## Recorded tokens and API-price equivalents

Each column totals nine trials, including parent and child inference. Ordinary input, cached reads, and recorded writes are disjoint parts of total input. Total input is not charged again on top of those categories. Reasoning is already included in output.

| Metric | No skill | Final v4 skill |
| --- | ---: | ---: |
| Model responses | 100 | 64 |
| Input total | 1,547,548 | 1,028,592 |
| Ordinary input | 106,396 | 76,784 |
| Cached reads | 1,441,152 | 951,808 |
| Recorded cache writes | 0 | 0 |
| Output | 4,000 | 4,599 |
| Reasoning included in output | 300 | 122 |
| Ordinary-input USD | $1.063960 | $0.767840 |
| Cached-read USD | $1.441152 | $0.951808 |
| Recorded-write USD | $0.000000 | $0.000000 |
| Output USD | $0.200000 | $0.229950 |
| Total API equivalent | $2.705112 | $1.949598 |

Input fell by 518,956 tokens, while output increased by 599 tokens. The net API valuation fell by $0.755514. The complete comparison consumed **164 unique responses**, **2,576,140 input tokens**, **8,599 output tokens**, and **$4.654710 API equivalent**. These workload totals exclude the surrounding authoring conversation and documentation work. This additional comparison did not run a separate model-based trace judge.

Prices use the original study's September 14, 2026 Standard API rate card: per million tokens, ordinary input $10, cached reads $1, recorded writes $12.50, and output $50. [The accounting implementation](waiting-benchmark/accounting.py) applies the same rates to every response. No request crossed the 272,000-input-token pricing threshold; the largest had 16,961 input tokens.

These values price subscription-reported counters at API rates. **Actual subscription charges and quota changes are unmeasured.** The runtime can normalize an absent upstream cache-write field to zero; zero recorded writes do not prove the service performed no cache writes.

## Results by workload

Each row contains three trials per condition. Delivery delay is measured from the underlying job's completion to the parent's final answer. For the CI simulator, completion time is its first status check plus the fixed 75-second duration; the model may discover it later. These delay figures exclude time before job startup, including initial skill loading; token and cost totals include that work.

| Workload | Responses: no skill → v4 | Input: no skill → v4 | API USD: no skill → v4 | Mean delivery delay: no skill → v4 |
| --- | ---: | ---: | ---: | ---: |
| terminal | 27 → 13 | 419,569 → 207,391 | $0.680330 → $0.408696 | 3.589 s → 3.839 s |
| subagent | 49 → 30 | 757,371 → 478,523 | $1.428170 → $0.867522 | 4.420 s → 12.239 s |
| ci | 24 → 21 | 370,608 → 342,678 | $0.596612 → $0.673380 | 5.805 s → 31.073 s |

Terminal and subagent work had lower responses, input, and API valuation in every matched pair. Across all nine pairs, eight used fewer responses and input tokens, and seven had a lower API valuation. The third CI pair used the same number of responses and more input; the second and third CI pairs cost more. All pairs, including unfavorable ones, appear in [COUNTS.md](../skills/codex-wait-efficiently/evals/comparisons/skill-vs-none/COUNTS.md).

### Why CI cost more despite fewer responses

All three controls made four separate status checks, with direct 20-second sleeps between them. Each used eight model responses. All three treatment runs used a bounded shell watcher after an initial status check, reducing model responses to six, seven, and eight. Both conditions still made four actual status requests per trial.

The treatment's CI ordinary-input valuation increased by $0.052220 and output valuation by $0.057700. Cached-read valuation decreased by $0.033152. The resulting net increase was $0.076768, or **12.87%**. Skill reads and generated watcher code add work; uncontrolled cache behavior also affects the ordinary/cached split. These records do not isolate the dollar effect of each source of overhead.

The watcher in the first treatment trial used 10/20/40-second backoff; the other two used 15/30/60 seconds. The latter pair delivered results 36.658 and 39.010 seconds later than their controls. Across all three CI trials, mean delivery delay increased from 5.805 to 31.073 seconds. This backoff tradeoff must be considered alongside the small CI response reduction.

### Remaining waiting behavior

| Diagnostic | No skill | Final v4 skill |
| --- | ---: | ---: |
| One-second `write_stdin` requests | 39 | 0 |
| Code Mode cell-resumption calls | 3 | 2 |
| One-second cell-resumption requests | 2 | 0 |
| Actual CI status requests | 12 | 12 |
| Trials with parent progress gaps over 60 seconds | 6/9 | 0/9 |
| Maximum parent progress gap | 75.948 s | 58.063 s |

All three treatment CI watchers still started with a one-second terminal yield. Two initially left the outer Code Mode wait too short for their 40- or 45-second inner wait, requiring an extra cell resumption. The resumes themselves used 10 or 15 seconds, so they passed the short-cell-poll check. The complete deterministic pass flag therefore does not imply every waiting instruction was followed.

The three treatment children each read the skill, avoided short polls, and finished their tasks; every subagent trial used exactly one child with the requested inherited model/effort and fork setting. Combined parent/child responses fell from 15/17/17 to 10/10/10. Result delivery in the subagent workload was about 7.82 seconds slower on average. Terminal mean delay changed by only about 0.25 seconds, with one pair faster and two slower. Overall, eight of nine pairs delivered later.

## Correctness and verification

All 18 turns completed with the actual successful benchmark result and the expected job/child counts. None changed the protected fixtures. The terminal and subagent final answers were exactly `BENCH_RESULT_7391`; CI answers reported the same result and run identity. All response IDs were unique, and response-level input, cached-input, recorded-write, and output totals reconciled with cumulative counters for every parent and child session.

The nine treatment trials passed every deterministic check. Six control trials failed short-poll or progress-cadence diagnostics while still completing their tasks correctly. These control process failures are retained in all totals. They measure the waiting behavior under comparison and are distinct from task-outcome failure. The [machine-readable comparison](../skills/codex-wait-efficiently/evals/comparisons/skill-vs-none/comparison.json) lists every retained failure.

The analysis also checks complete manifest coverage, identical paired task prompts, frozen case and skill hashes, common base instructions, model/effort identity, absence of AGENTS.md in both conditions, and actual skill isolation. The original 66-trial export still regrades identically. The final skill SHA-256 remains `14bc9f85b382ba1bc313246b23dff2b6e205cc75d880ab8a9160e5fc8514f173`.

## What users can conclude

For these Astra waiting workloads, installing the final skill with automatic selection reduced overall response counts, input tokens, and API-price equivalent. The strongest evidence is in terminal and subagent waiting. CI shows that reducing model involvement can still raise cost and delay completion reporting; neither a bounded watcher nor a longer wait guarantees a saving.

This is a small sample of idle waits lasting 75 seconds, with the target skill isolated from competing skills and no global AGENTS.md patch. It does not measure Sol, mixed active work, production CI behavior, long cache-retention intervals, `/goal` pause transitions, or reliable activation among many competing skills. A fresh repetition or a different runtime, account, catalog, or task can change the result.

The [AGENTS.md experiment](CODEX_WAITING_LATEST_VS_NO_PATCH_BENCHMARK.md) remains separate. The current comparison does not test the skill against AGENTS.md and cannot establish which format is cheaper. It also leaves the earlier conclusion intact that the v1-to-v4 revisions themselves did not demonstrate general savings. The new result answers the different question of final-skill installation versus no skill.

## Files and reproduction

- [English skill README](../skills/codex-wait-efficiently/README.md) and [Japanese skill README](../skills/codex-wait-efficiently/README.ja.md): purpose, installation, benefits, and measured limitations.
- [Plan](../skills/codex-wait-efficiently/evals/comparisons/skill-vs-none/PLAN.md) and [manifest](../skills/codex-wait-efficiently/evals/comparisons/skill-vs-none/skill-vs-none.json): inputs frozen before inference.
- [Captured evidence](../skills/codex-wait-efficiently/evals/comparisons/skill-vs-none/trial-evidence.json), [per-trial scores](../skills/codex-wait-efficiently/evals/comparisons/skill-vs-none/SCORES.md), and [counts](../skills/codex-wait-efficiently/evals/comparisons/skill-vs-none/COUNTS.md): all 18 trials and parent/child accounting.
- [Comparison verifier](../skills/codex-wait-efficiently/evals/compare_controls.py) and [reproduction instructions](../skills/codex-wait-efficiently/evals/README.md#final-skill-versus-no-skill): live execution and offline regrading.

Run `python3 skills/codex-wait-efficiently/evals/compare_controls.py` from the repository root to verify and regenerate the comparison without model calls or authentication. Live repetitions consume normal account usage. Published evidence contains selected synthetic workload records; authentication and full private session instructions are excluded.
