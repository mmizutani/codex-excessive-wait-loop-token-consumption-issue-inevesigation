# Codex waiting: measured runtime and AGENTS.md comparison

## TL;DR

**73 actual 75-second workloads completed successfully, including nine Astra trials on CLI 0.153.1 and three tests of the final compact patch. Waiting overhead is still reproducible on 0.154.0, and neither upgrading nor enabling sleep universally eliminates it.**

- **Historical comparison is limited:** Sol's 0.151.0 baseline excludes PR #41243. Astra works on the subsequently tested 0.153.1, but that release already includes #41243. Today's backend rejects Astra on 0.151.0. Neither older client reproduces the server changes described in the linked announcement.
- **Astra now has an earlier-client comparison:** configured-environment responses were 48→48→41 for 0.153.1→0.154.0→initial patch; API-rate equivalents were $2.055734→$1.934240→$1.644686. Clean responses were 30→36→24, with dollars $0.792160→$0.988982→$0.716216. The later 0.153.1 trials reuse the original 0.154.0 controls, so these are exploratory sequential comparisons.
- **The original patch is not a reliable general cost fix.** In the configured environment, its API-rate equivalents fell 15.0% for Astra and 20.9% for Sol. In clean controls, the Sol result reversed to a 23.1% increase.
- **Tuning helped Astra:** v3 reduced combined responses 52.8% and API-rate equivalents 40.1% across its three clean workloads; Sol responses were unchanged and its dollar equivalent rose 16.8%. All six v3 trials met the measured update cadence.
- **The original compact patch has three clean Astra measurements:** responses fell 36→16, input fell 54.64%, and API-rate equivalents fell $0.988982→$0.528592 (46.55%). All parent update gaps stayed below 60 seconds, but CI result delivery was 16.34 seconds later. The [Astra-only final-patch tables](#final-compact-patch-astra-only-shared-skills-disabled) use the frozen original compact wording and retain the limits of this small sequential comparison. Sol has not been tested with the compact wording. [Exported addition](waiting-validation/AGENTS.waiting-compatible.md)
- **Do not require `always_on` solely as a cost fix.** It exposes native sleep; the separate Sol test used more model responses after enabling it. No cache-only keepalive or 25-minute wake-up rule has demonstrated savings.
- **Token categories and dollar components are separated below.** Dollars are Standard API-rate equivalents of subscription-reported counters, not account charges. Cache-write fields were normalized zero; actual writes cannot be recovered separately and may have been omitted upstream.
- **Further measurements updated the current export.** The first [30 follow-up trials](CODEX_WAITING_NUMERIC_OVERRIDES_BENCHMARK.md) examined numeric overrides and whole-section deletion. The subsequent [32-trial outer-yield study](CODEX_WAITING_OUTER_EXEC_BENCHMARK.md) selected qualitative initial and outer waits, removing `30000` and `45000` from the Terminal commands section. Explicit `functions.exec` naming was tested and omitted. The selected wording passed seven trials across three phases; it is distinct from the frozen compact version measured below.

## What the three conditions mean

| Condition | Runtime | Waiting addition | Scope |
| --- | --- | --- | --- |
| (1) Earlier, Sol | Official CLI 0.151.0 | None | Latest stable tag excluding #41243; supported for Sol, rejected for Astra by today's backend. |
| (1) Earlier, Astra | Official CLI 0.153.1 | None | User-requested follow-up after the Astra catalog backport; already includes #41243. |
| (2) New | Official CLI 0.154.0 | None | User-specified stable release, also verified as the latest stable when testing began. |
| (3) New + initial patch | Official CLI 0.154.0 | Frozen [initial addition](waiting-benchmark/AGENTS.initial.md) | Same runtime and configuration as (2); only the global waiting addition changes. |
| (3), final compact comparison | Official CLI 0.154.0 | Frozen [final compact addition](waiting-benchmark/AGENTS.compact-final.md) | Three clean Astra workloads, reported separately from the historical initial-patch condition. |

The [linked September 12 announcement](https://x.com/thsottiaux/status/2098612714704891959), retrieved through a public mirror after X returned 403, discusses skill behavior, a disabled context-management experiment, and backend engine routing. It does not identify PR #41243 or promise a waiting-specific CLI fix. An old CLI still uses today's backend: this experiment cannot reproduce the old server-side experiment or routing configuration.

[PR #41243](https://github.com/openai/codex/pull/41243) adds configurable sleep-tool gating. Its default preserves previous model-dependent behavior. Git ancestry shows that CLI 0.151.0 excludes this PR and 0.154.0 includes it. Several earlier wait improvements are already present in both versions, and the V2 wait handler has the same Git blob in both. Thus (1) is a defined client-release baseline, not “before every waiting fix.” [Pinned provenance](waiting-benchmark/provenance.json)

The backend rejects Astra on 0.151.0 with an explicit upgrade-required error. That cell remains **unavailable**, not a successful run with zero tokens. The requested follow-up confirmed that the official 0.153.1 client successfully runs Astra against today's subscription backend. No version header was spoofed. Astra's three-way comparison therefore uses a different earlier release from Sol's.

[PR #42605](https://github.com/openai/codex/pull/42605) backported the Astra catalog entry to the 0.153 release branch, and [0.153.1](https://github.com/openai/codex/releases/tag/rust-v0.153.1) contains it. The bundled 0.153.0 catalog lacks this entry; 0.153.1 includes it as hidden and API-supported. This verifies the catalog backport, not the absolute minimum client version accepted by today's backend. In particular, 0.153.0 was not tested live. CLI 0.153.1 already includes #41243, and its sleep handler, V2 agent-wait handler, and multi-agent session implementation are byte-identical to 0.154.0. Other execution code differs. Consequently, a 0.153.1→0.154.0 difference cannot be attributed to introducing those waiting fixes. [Follow-up provenance, source hashes, and successful compatibility probe](waiting-benchmark/astra-1531-provenance.json)

## Experimental controls and limits

- Actual model inference through Codex app-server, authenticated using the existing subscription. No scripted model responses are used in these measurements.
- Astra and Sol at `low` reasoning effort. Child agents are explicitly instructed to use the same model and effort. This controls reasoning within the comparison; it does not establish behavior at `xhigh` or on substantial coding tasks.
- The same pinned current model catalog is supplied to both clients. It fixes the catalog input but does not freeze backend model weights, runtime-injected instructions, routing, or cache state.
- Fresh private Codex homes and work directories, containing the same test scripts and only the applicable AGENTS.md addition. **These homes still discover shared `~/.agents/skills`.** Primary trials therefore measure the configured environment; CI trials loaded the existing monitoring skill. A separate clean phase disables the skills instruction block and bundled skills through supported configuration on both versions. Authentication is copied privately and removed with each temporary home.
- Primary conditions retain default sleep gating and enable the same multi-agent capability. (3) does not silently add `always_on` configuration to (2).
- Two repetitions per supported original primary cell, with reversed condition ordering on repetition two and at most two primary trials concurrently. The later Astra 0.153.1 follow-up adds two repetitions per configured workload and one per clean workload, compared with the existing 0.154.0 controls; these are sequential comparisons, not fresh interleaved pairs. This small, non-randomized sample describes observed executions; it does not estimate population-level savings or isolate every release change causally.
- Warmness, cache routing, fresh working-directory prefixes, startup latency, and concurrent activity can affect counts and prices. Token categories are retained so a lower cache-hit rate is not mistaken for more waiting responses.
- No trial waits 30 minutes. The 25-minute paragraph is included in the initial-patch trials, but cache expiration and the proposed 25-minute precaution are not tested by these short workloads.

| Workload | Actual pending work | Completion evidence |
| --- | --- | --- |
| Terminal | A real process sleeps for 75 seconds and emits a fixed result. | Exactly one start, terminal marker, exit, and correct final result. |
| Subagent | One real model-driven child runs that terminal process. | Parent receives the correct result; command launches once; parent and child usage counted separately. |
| CI status | Local CI simulator remains pending for 75 seconds after the first status request. It has no push notification or watch subcommand. | Authoritative status reports completion and the parent returns the correct result. This is not an actual GitHub Actions run. |

The predeclared response-count target was at least 20% fewer parent model responses, while preserving completion and avoiding a substantial result-delivery delay regression. Required commentary cadence is assessed separately. Result-delivery delay is the final answer's recorded completion time minus the job's completion time; it includes detection and model response latency. Update gaps use completed parent messages, including the final answer and the delay before the first update. Small overages near 60 seconds can include streaming/timestamp effects; the large observed gaps are unambiguous. A cheaper run that stops early or ignores update requirements is not an accepted efficiency fix. [Plan](waiting-benchmark/PLAN.md)

## Token categories and API-price dollars

A response here is one upstream completion with a unique response ID; one user turn can contain many such responses. For each response, let `I` be total input, `R` cache-read input, `W` cache-write input, and `O` output. Ordinary uncached input is `U = I − R − W`. These input categories are disjoint; `I` already includes `R` and `W`. Reasoning output is included in `O` and is not charged a second time.

Standard API USD per million tokens, checked September 14, 2026:

| Model | Ordinary input U | Cached reads R | Cache writes W | Output O |
| --- | ---: | ---: | ---: | ---: |
| GPT-6 Astra | $10.00 | $1.00 | $12.50 | $50.00 |
| GPT-5.6 Sol | $4.00 | $0.40 | $5.00 | $20.00 |

`API-price equivalent = (U × input rate + R × cached rate + W × write rate + O × output rate) / 1,000,000`.

Requests exceeding 272,000 input tokens use twice the input-category rates and 1.5 times the output rate for the whole request. This threshold is applied **per response**, not to a trial's accumulated input. These calculations assume Standard service without regional uplift or other paid tools. [Official API pricing](https://developers.openai.com/api/docs/pricing), [Astra pricing details](https://developers.openai.com/api/docs/models/gpt-6-astra), [Sol pricing details](https://developers.openai.com/api/docs/models/gpt-5.6-sol)

These dollar amounts value the **subscription-reported counters at API rates, treating unreported cache writes as zero**. They are not an actual subscription bill or proof of what an otherwise identical API session would report. In particular, Codex can default a missing upstream cache-write field to zero. All measured write values are normalized zeros; the actual write count is not separately recoverable from these records. A reported zero is retained as zero in the arithmetic and is explicitly not evidence that API cache writes would be free or absent. If some ordinary-classified input was actually a cache write, its API valuation would be 25% higher for those tokens. The tables therefore do not reconstruct an actual API bill.

Upstream response IDs are deduplicated. Raw completion notifications and rollout usage are reconciled with final session counters. Parent and child responses are separated by session identity. Cumulative snapshots are not summed as individual requests. Category separation and per-request pricing have executable checks. [Accounting implementation](waiting-benchmark/accounting.py), [analyzer](waiting-benchmark/analyze.py)

## Measured results

All 30 original primary trials and the six later configured-environment Astra 0.153.1 trials completed successfully, with one command launch per terminal or subagent trial. Each model-condition row contains six trials: two repetitions of each workload. The Astra (1) row was measured later; the other rows retain their original measurements. Counts include parent and child inference. Writes are reported zeros with the observability limitation explained above.

| Model | Condition | Responses | Total input | Ordinary input | Cached reads | Writes reported | Output | API-rate USD |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Sol | (1) 0.151.0 | 38 | 719,953 | 181,201 | 538,752 | 0 | 3,450 | $1.009305 |
| Sol | (2) 0.154.0 | 42 | 784,936 | 111,656 | 673,280 | 0 | 4,099 | $0.797916 |
| Sol | (3) initial patch | 39 | 713,699 | 78,179 | 635,520 | 0 | 3,213 | $0.631184 |
| Astra | (1) 0.153.1, follow-up | 48 | 891,728 | 117,584 | 774,144 | 0 | 2,115 | $2.055734 |
| Astra | (2) 0.154.0 | 48 | 896,684 | 103,084 | 793,600 | 0 | 2,196 | $1.934240 |
| Astra | (3) initial patch | 41 | 781,473 | 84,257 | 697,216 | 0 | 2,098 | $1.644686 |

For Sol, (1)→(2) increased combined responses 10.53% and inclusive input 9.03%, while its dollar equivalent fell 20.94%. Ordinary input fell substantially and cached reads increased. This is not evidence that the runtime upgrade eliminated model-driven polling.

For Astra, 0.153.1→0.154.0 left combined responses unchanged at 48 (33 parent + 15 child). Inclusive input rose 0.56%; its dollar equivalent fell 5.91%, with ordinary input decreasing and cached reads increasing. Mean response counts were identical for every workload: terminal 7.5, subagent 4 parent + 7.5 child, CI 5. Thus this configured-environment comparison shows no reduction in model response boundaries from that upgrade. The 0.153.1 terminal trace still includes an initial one-second poll and short outer wrapper waits; CI reads the shared monitoring skill and makes two 60-second sleep calls. All six earlier-client trials exceeded the nominal 60-second parent update interval. [Astra three-way workload comparison](waiting-benchmark/astra-1531-results/COMPARISON.md), [new trial counts and category-specific dollars](waiting-benchmark/astra-1531-results/COUNTS.md)

For (2)→(3), combined responses fell 14.58% for Astra and 7.14% for Sol; dollar equivalents fell 14.97% and 20.90%. These are observed aggregates in the configured skill environment. Parent-only totals fell 9.09% for Astra and 14.71% for Sol. Only Astra terminal (20%) and Sol subagent (33.3%) met the predeclared parent-response target; the latter also increased child responses from a mean of 4 to 5. The patch exceeded the 60-second update interval in five of six workload cells, as did many baselines. Sol CI mean result-delivery delay worsened from 93.18 to 108.77 seconds after completion.

The dollar totals for the original 30 primary workloads sum to $6.017331 at the chosen API rates. Adding the six Astra 0.153.1 workloads brings this configured-environment total to $8.073065. Both exclude setup probes, the investigation session, and reviewer agents. Neither is a subscription charge.

[Every trial's counts, separate parent/child counts, and category-specific dollars](waiting-benchmark/results/COUNTS.md); [workload means, delays, and contrasts](waiting-benchmark/results/COMPARISON.md); [selected response/tool evidence](waiting-benchmark/results/trial-evidence.json).

## Clean comparison: shared skill instructions disabled

All 21 original clean trials and the three later Astra 0.153.1 clean trials completed successfully. There is one trial per model/workload/condition. The table uses three workloads per row and includes children. “V2” is the first executed tuned candidate. These controls remove the shared skill catalog, not all backend/cache variation.

| Model | Condition | Trials | Responses | Input total | Ordinary input | Cached reads | Writes reported | Output | API-rate USD |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Sol | (1) old | 3 | 18 | 263,151 | 84,079 | 179,072 | 0 | 1,253 | $0.433005 |
| Sol | (2) new | 3 | 16 | 231,085 | 23,213 | 207,872 | 0 | 1,223 | $0.200461 |
| Sol | (3) initial | 3 | 17 | 252,681 | 32,777 | 219,904 | 0 | 1,387 | $0.246810 |
| Sol | v2 | 3 | 18 | 268,685 | 36,237 | 232,448 | 0 | 1,463 | $0.267187 |
| Astra | (1) 0.153.1, follow-up | 3 | 30 | 464,030 | 29,470 | 434,560 | 0 | 1,258 | $0.792160 |
| Astra | (2) new | 3 | 36 | 555,974 | 40,262 | 515,712 | 0 | 1,413 | $0.988982 |
| Astra | (3) initial | 3 | 24 | 376,138 | 32,842 | 343,296 | 0 | 890 | $0.716216 |
| Astra | v2 | 3 | 22 | 346,788 | 29,220 | 317,568 | 0 | 868 | $0.653168 |

The clean sample reverses the initial Sol patch's dollar result: compared with new, it uses 6.25% more responses and has a 23.12% higher dollar equivalent. V2 uses 12.5% more responses and costs 33.29% more. Some additional parent work delivers the required updates, but these observations do not establish Sol savings. Astra's initial patch reduces combined responses 33.33%; v2 reduces them 38.89%, with dollar equivalents down 27.58% and 33.96%.

The added clean Astra baseline also gives mixed runtime results. From 0.153.1 to 0.154.0, terminal responses fell 11→9, subagent responses rose 13→19 (parent 4→8; child 9→11), and CI responses rose 6→8. Across the three workloads, responses increased 20%, input 19.81%, and API-rate dollars 24.85%. The 0.153.1 terminal made nine one-second `write_stdin` polls; its subagent child made six before switching to a longer wait. The parent used two 60-second `wait_agent` calls. Only CI met the measured 60-second update cadence. These single trials confirm that inefficient wait choices are possible without shared skill instructions, but do not establish a causal regression or improvement between releases. [Clean Astra three-way comparison](waiting-benchmark/astra-1531-clean-results/COMPARISON.md), [token categories and dollar components](waiting-benchmark/astra-1531-clean-results/COUNTS.md)

Astra CI remains a weak case for both prompts: all three 0.154.0 variants use eight responses, and result-delivery delay rises from 11.00 seconds without the patch to 58.11 with the initial patch or 43.88 with v2. This is why the final candidate clarifies the shell-watcher behavior. Neither environment supports presenting the initial patch as a universal cost reduction.

[All clean token categories and dollar components](waiting-benchmark/clean-results/COUNTS.md); [workload counts, delays, and contrasts](waiting-benchmark/clean-results/COMPARISON.md); [selected evidence](waiting-benchmark/clean-results/trial-evidence.json).

## Investigation and prompt tuning

The first Astra terminal pair was weak: (2) used eight parent responses and (3) used seven. Its API-price equivalents were $0.291390 and $0.280352 respectively, only a 3.79% difference. Both exceeded the nominal 60-second commentary interval. Two independent agents reviewed the concrete traces and accounting. [Consultation record](waiting-benchmark/AGENT_REVIEW.md)

The observed extra boundaries were an unnecessary initial short process poll, a long inner wait whose outer code-mode yield remained at its default, and repeated short wrapper checks. The existing instruction to “coordinate” those durations did not reliably cause the model to set the actual first-line `@exec` control. Its wait budgeting also ignored time already elapsed since the last update.

The frozen [tuned candidate](waiting-benchmark/AGENTS.tuned-v2.md) supplies the executable wrapper-yield syntax, avoids preliminary short polls, and budgets waits against an elapsed update deadline. It also removes the untested 25-minute cache checkpoint, matching the current user preference against cache-only keepalives without measured savings. The earlier v1 draft was not tested. V2 reduced clean Astra terminal responses from 9 to 4, but still had a 65.371-second update gap. Its trace shows 11.336 seconds of model turnaround between a 30-second wait and a 19-second wait; the agent budgeted tool durations rather than actual elapsed time.

The [v3 candidate](waiting-benchmark/AGENTS.tuned-v3.md) simplifies that instruction: when only waiting remains and updates are required, include the update in the same response before the next waiting tool call. This adds message tokens without inherently adding another response boundary. Its 45-second wait limit leaves 15 seconds for turnaround under the 60-second cadence. The margin is informed by observed latency, not a hard guarantee. V3 was evaluated in six further clean trials after the other phases; those results are separate from the original comparison.

## V3: six fresh validation trials

All six v3 trials completed successfully. Every recorded parent update gap was below 60 seconds (maximum 48.36s). The controls are the earlier clean 0.154.0 runs: these are exploratory sequential comparisons, not simultaneous randomized pairs.

| Model | Condition | Trials | Responses | Input total | Ordinary input | Cached reads | Writes reported | Output | API-rate USD |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Sol | v3 | 3 | 16 | 238,430 | 29,662 | 208,768 | 0 | 1,596 | $0.234075 |
| Astra | v3 | 3 | 17 | 269,108 | 28,852 | 240,256 | 0 | 1,279 | $0.592726 |

| Model / workload | Combined responses, new→v3 | API-rate USD, new→v3 | Result delay seconds, new→v3 | V3 maximum update gap (s) |
| --- | ---: | ---: | ---: | ---: |
| Sol / ci | 5→4 | $0.068496→$0.057574 | 32.53→7.01 | 38.11 |
| Sol / subagent | 7→8 | $0.077244→$0.117384 | 5.14→6.55 | 47.93 |
| Sol / terminal | 4→4 | $0.054721→$0.059117 | 2.01→2.42 | 34.81 |
| Astra / ci | 8→5 | $0.268036→$0.187448 | 11.00→26.00 | 44.18 |
| Astra / subagent | 19→8 | $0.490254→$0.263254 | 7.01→9.56 | 48.36 |
| Astra / terminal | 9→4 | $0.230692→$0.142024 | 4.79→5.62 | 43.68 |

Astra's combined responses fell 52.78%, input 51.60%, and API-rate dollars 40.07%. Sol's combined response count was unchanged, input rose 3.18%, and dollar equivalent rose 16.77%. Sol's extra subagent parent response supplied an update omitted by the cheaper baseline. Its CI case improved, but these results do not establish overall Sol savings. Astra CI returned the result 15.00 seconds later, so the Astra count reduction is not an unqualified latency-neutral success.

The terminal review confirmed commentary shared the existing responses with wait calls; it did not create separate update-only requests. Sol did not consistently follow the wrapper-pragma instruction, so passing outcomes do not prove literal compliance with every clause.

Both CI models created shell watchers and reduced model responses. However, neither script had an explicit time/check-count bound. Astra made four service-status checks (same as baseline), while Sol made 15 (baseline four). The benchmark harness bounded execution, but that does not validate the prompt's watcher-bound wording for production. This prompted a narrow v4 correction before exporting the recommendation.

[All v3 token categories, parent/child counts, and category-specific dollars](waiting-benchmark/v3-results/COUNTS.md); [selected traces](waiting-benchmark/v3-results/trial-evidence.json).

## Final v4 correction: explicit watcher limit and backoff

V4 changes only the CI clause to require a time or check-count limit and apply backoff to the watcher itself. Both fresh CI trials completed correctly and kept update gaps below 60 seconds. Astra generated a 30-minute observation deadline; Sol generated a 12-check limit. Both backed off unchanged status and retained their process session. These are observation limits, not declarations of CI failure.

| Model | Input | Ordinary input | Cached reads | Writes reported | Output | Responses | API-rate USD | Status checks | Result delay (s) | Maximum update gap (s) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Astra | 63,863 | 11,767 | 52,096 | 0 | 525 | 4 | $0.196016 | 5 | 10.67 | 43.11 |
| Sol | 91,080 | 13,128 | 77,952 | 0 | 586 | 6 | $0.095413 | 6 | 29.32 | 37.35 |

Compared with the clean new baseline, Astra CI responses fell 8→4 and its dollar equivalent fell $0.268036→$0.196016 (26.87%), with result delay 11.00→10.67 seconds. Sol rose 5→6 responses and $0.068496→$0.095413 (39.30% higher), while result delay fell 32.53→29.32 seconds. Sol again omitted the explicit outer pragma on its initial call and incurred an additional wrapper wait.

V4 reduced Sol's status checks from the 15 seen in v3 to six, but the baseline used four. Fewer model responses and fewer service requests are different measures. Generated watchers were tested on successful completion only; their failure-state behavior and production CI integration were not validated.

[All v4 token/dollar categories and selected traces](waiting-benchmark/v4-results/COUNTS.md), [v4 evidence](waiting-benchmark/v4-results/trial-evidence.json). Do not combine v4 CI rows with v3 terminal/subagent rows and label the sum an actually executed v4 suite.

## Final compact patch: Astra only, shared skills disabled

The final-compact label here identifies the historical version used for these tables. The current export subsequently removed individual wait numbers; its separate measurements and limitations are in the [outer-yield follow-up](CODEX_WAITING_OUTER_EXEC_BENCHMARK.md).

These tables use the original compact wording, frozen as [AGENTS.compact-final.md](waiting-benchmark/AGENTS.compact-final.md), with SHA256 `a60d7f36e699d61a17abf4fafc46c9dcfe3195826d6e59e6546e39737b9ff2cf`. All three new workloads completed successfully on CLI 0.154.0. Shared skill instructions and bundled skills were disabled for every row; no skill catalog or skill-reading call appeared in the new parent/child traces. Each condition contains one 75-second trial per workload, at low reasoning effort, with default sleep gating and the same pinned model catalog.

Here **(3) means the final compact patch**; the earlier tables retain their explicitly labeled historical prompt versions. Conditions (1) and (2) reuse the existing clean Astra controls, so these are small, sequential comparisons rather than fresh interleaved pairs. CLI 0.153.1 already contains #41243 and is not a pre-fix baseline. Token counts and dollars include parent and child inference. Writes are reported/defaulted zeros, not separately recovered actual cache writes; dollars are API-rate equivalents of subscription counters, not account charges.

| Model | Condition | Trials | Responses | Input total | Ordinary input | Cached reads | Writes reported | Output | API-rate USD |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Astra | (1) 0.153.1, no patch | 3 | 30 | 464,030 | 29,470 | 434,560 | 0 | 1,258 | $0.792160 |
| Astra | (2) 0.154.0, no patch | 3 | 36 | 555,974 | 40,262 | 515,712 | 0 | 1,413 | $0.988982 |
| Astra | (3) 0.154.0 + final compact patch | 3 | 16 | 252,200 | 24,488 | 227,712 | 0 | 1,120 | $0.528592 |

The workload table compares **pre = (2), unpatched 0.154.0**, with **post = (3), final compact patch on 0.154.0**. Each cell reports the actual single-trial result, not an average across different prompt versions.

| Model / workload | Combined responses, pre→post | Input total, pre→post | API-rate USD, pre→post | Result delay (s), pre→post | Maximum parent update gap (s), pre→post |
| --- | ---: | ---: | ---: | ---: | ---: |
| Astra / ci | 8→4 | 123,659→63,656 | $0.268036→$0.125336 | 11.00→27.34 | 58.15→45.33 |
| Astra / subagent | 19→8 | 293,066→125,649 | $0.490254→$0.259968 | 7.01→6.99 | 82.37→48.17 |
| Astra / terminal | 9→4 | 139,249→62,895 | $0.230692→$0.143288 | 4.79→8.22 | 77.56→45.84 |

Across these workloads, the compact patch reduced combined responses **55.56%**, inclusive input **54.64%**, and API-rate dollars **46.55%** versus (2). The subagent row changed from 8 parent + 11 child responses to 4 + 4. Every new parent update gap was below 60 seconds. Terminal and child traces used the explicit wrapper pragma, a 30-second initial command wait, and subsequent 40-second process waits; the parent used direct 45-second agent waits.

The savings have a latency tradeoff: CI result delay increased 11.002→27.343 seconds (+16.341 seconds), and terminal delay increased 4.795→8.224 seconds. CI used one watcher bounded to 120 checks, backed off its intervals, and emitted only changed status, but made six service checks versus four in the baseline. Its completion path passed; failure-state handling and production CI integration remain untested. These observations support measured savings on these workloads, not a latency-neutral or production-wide guarantee. Sol was not tested with this compact version.

[New trial counts, parent/child accounting, and dollar components](waiting-benchmark/compact-final-astra-results/COUNTS.md); [selected traces](waiting-benchmark/compact-final-astra-results/trial-evidence.json); [comparison data](waiting-benchmark/compact-final-astra-results/comparison-metrics.json); [prompt and control provenance](waiting-benchmark/compact-final-astra-provenance.json).

## Separate `always_on` configuration check

Two further clean Sol CI trials enabled native sleep on 0.154.0. The default-gating rows below are the earlier clean controls, not simultaneous or randomized replicas. “V2” refers to that candidate, not the later final prompt.

| Prompt | Sleep gating | Responses | Input | Cached reads | Writes reported | Output | API-rate USD | Result delay (s) |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| None | Default | 5 | 72,825 | 64,640 | 0 | 495 | $0.068496 | 32.53 |
| None | Always on | 8 | 117,686 | 99,456 | 0 | 487 | $0.122442 | 7.91 |
| V2 | Default | 6 | 90,442 | 81,920 | 0 | 545 | $0.077756 | 19.63 |
| V2 | Always on | 8 | 121,342 | 102,272 | 0 | 515 | $0.127489 | 35.70 |

Both always-on trials completed and used native `clock.sleep`. Without the setting, the unpatched model combined shell sleep and a status command in one call. With the setting, it issued native sleep and a separate status command, creating more response boundaries. The unpatched always-on run delivered the result sooner; its higher response count is not evidence that exposing the tool failed. It is evidence that exposing it does not ensure cheaper behavior.

This small diagnostic does not establish expected configuration savings or validate v3 with always-on. It does refute an unconditional inference from “sleep is available” to “model-driven waiting overhead is solved.” [Counts and category-specific dollars](waiting-benchmark/sleep-on-results/COUNTS.md), [selected traces](waiting-benchmark/sleep-on-results/trial-evidence.json).

## What the runtime fixes resolve, and what remains

The runtime provides working mechanisms for waiting without repeatedly invoking the model: direct native sleep, completion-aware terminal waits, and event-aware subagent waits. Earlier fixes moved sleep outside code mode and encouraged longer native agent waits. These capabilities already exist in the older release used here. The newer configurable gating feature can expose sleep consistently across models; its default does not force all models to receive it. [Release/PR ancestry](waiting-benchmark/provenance.json), [earlier runtime validation](CODEX_ASTRA_SOL_WAITING_INDEPENDENT_VALIDATION.md)

The remaining problem is choosing and combining those mechanisms correctly. In the clean 0.154.0 Astra subagent baseline, the parent spontaneously issued five 10-second `wait_agent` calls followed by a 60-second wait. The parent and child together made 19 responses for one 75-second command. This is a concrete current-runtime reproduction, with the shared skill catalog absent. A short process poll, an outer code-mode yield that expires before the inner wait, or an overlong parent wait can still cause extra inference or missed updates. CI sleep does not wake automatically on CI completion. Pausing `/goal` is a different operation from ending a turn. None of these behaviors is universally corrected by an AGENTS.md preference. A global user instruction also cannot override higher-priority minute-by-minute commentary requirements: those updates themselves require inference even when no external status query is useful.

`always_on` is useful when the desired model otherwise lacks `clock.sleep`; it is not evidence that every user must change configuration to eliminate waiting overhead. Astra already receives native sleep under the pinned default catalog. The separate Sol CI configuration comparison avoids attributing a tool-availability change to the prompt. Where desired, the explicit setting is:

```toml
[features]
sleep_tool = { enabled = true, mode = "always_on" }
```

Merge it into an existing `[features]` table rather than creating a duplicate table. The configuration path is `${CODEX_HOME:-$HOME/.codex}/config.toml`; a custom `CODEX_HOME` changes that location.

## Cache TTL and the prompt recommendation

The API documentation describes a renewable minimum cache lifetime of 30 minutes for these model generations, measured from the most recent write or reuse. That is not independent verification of a Codex subscription guarantee or a hard expiry exactly 30 minutes later. [Official prompt-caching documentation](https://developers.openai.com/api/docs/guides/prompt-caching)

The initial patch's 25-minute checkpoint is an untested margin heuristic. Even if the user's 30-minute subscription premise holds, a cache-only wake-up creates a request with its own read, new-input, and output costs. It can help in some cost scenarios and hurt in others. The current 60-second commentary requirement already causes normal model resumptions well inside that interval. These 75-second trials do not measure cache expiration or justify a universal 25-minute cap.

The compact export therefore retains only: “Longer waits may not reduce usage; add no cache-only keepalives without measured savings.” This preserves cache awareness without claiming an optimum.

## Recommended user-side addition and rollout scope

The current four-rule addition is a compact rewrite of v4, exported as [AGENTS.waiting-compatible.md](waiting-validation/AGENTS.waiting-compatible.md) and synchronized with this workspace's active [global AGENTS.md](../.codex_home/AGENTS.md). The exact wording tested in the three new Astra workloads is frozen at [AGENTS.compact-final.md](waiting-benchmark/AGENTS.compact-final.md); the earlier [v4 wording](waiting-benchmark/AGENTS.tuned-v4.md) is also preserved. The compact version has now demonstrated savings in these short Astra workloads, with the CI latency tradeoff reported above. It has not been tested on Sol or directly established as behaviorally equivalent to v4. The original prompt and every tested candidate remain available for audit.

The useful additions are concrete: retain native wait/session handles, avoid preliminary short polls, coordinate wrapper and inner durations, put required updates in existing wait responses, and turn scriptable CI polling into a bounded command. The four rules preserve verification and the distinction between an observation timeout, a failed task, and an actually paused goal. They can coexist with the built-in instructions because they explicitly defer to higher-priority limits. They cannot guarantee obedience or a response-latency bound.

**Recommend a targeted pilot for observed waiting loops, especially Astra; do not mandate this prompt or `always_on` as a universal Sol/company cost reduction.** The evidence does not justify enlarging the global prompt further to force a savings percentage. Retain existing skills for useful work; disabling their catalog here was an experimental control, not a company recommendation.

Before distributing a savings claim, evaluate representative company tasks with the actual model effort, instruction/skill stack, CI service, and acceptable result delay. Record combined parent/child usage, cache categories, service checks, completion correctness, and update gaps. The 73 runs here establish concrete mechanisms and tradeoffs, not production-wide savings, a subscription billing conversion, a 30-minute TTL, or historical backend behavior. `/goal` cost comparisons were not part of this workload matrix; its pause/continuation behavior is covered by the earlier runtime investigation.

## Verification and reproduction

All 73 workloads completed successfully. The original 61-trial audit is preserved: 418 responses and $10.891320 in Standard API-rate equivalents. The nine Astra 0.153.1 follow-up workloads add 78 responses, 1,355,758 inclusive input tokens (147,054 ordinary-classified input; 1,208,704 cached reads; zero reported/defaulted writes), and 3,373 output tokens, for $2.847894. The final three compact-patch workloads add 16 responses, 252,200 inclusive input tokens (24,488 ordinary-classified input; 227,712 cached reads; zero reported/defaulted writes), and 1,120 output tokens, for $0.528592. [Original audit](waiting-benchmark/audit-summary.json), [73-workload combined audit](waiting-benchmark/compact-final-astra-audit-summary.json)

Across all 73 workloads, 512 unique upstream responses reconcile with session counters: 8,700,714 inclusive input tokens, 1,129,258 ordinary-classified input, 7,571,456 cached reads, zero reported/defaulted writes, and 33,034 output tokens (including 4,342 reasoning tokens). Their total Standard API-rate equivalent is $14.267806. No request exceeded 23,197 input tokens, so the long-context multiplier was not applied. Reused control rows in follow-up comparison tables are counted once. Setup probes and investigator/reviewer usage are excluded.

The three accounting tests passed, covering disjoint input categories, included reasoning, and the per-request long-context boundary. All per-session cumulative counters reconcile to deduplicated responses; prompt hashes, parent prompt loading, single job launch, clean skill isolation, and model identities were checked. At the original benchmark completion, export/global files matched the frozen v4 prompt. Subsequent edits first organized the sections, then shortened the wording and consolidated shared constraints. Review of the compact wording checked preservation of instruction priority, progress-update timing, wait arguments and wrapper coordination, session/job identity, bounded watchers and backoff, cache guidance, verification, and accurate goal state. The compact version then received the three separate Astra workload tests reported above. Its frozen copy, export, and active global copy match; historical prompt files and hashes remain unchanged. Historical v3/v4 savings remain attributed to those versions, separately from the compact version's own results.


The [benchmark README](waiting-benchmark/README.md) contains the commands and evidence layout. Official old-release assets and their hashes are recorded in [provenance](waiting-benchmark/provenance.json). Setup smoke tests, including the rejected Astra request and the initial missing old code-mode host, are separate from primary results. The investigation's own model usage and reviewer-agent usage are excluded from the controlled workload tables.
