# Runtime and prompt waiting benchmark

The **latest and final proposed patch** is [AGENTS.waiting-compatible.md](../waiting-validation/AGENTS.waiting-compatible.md). Its exact current wording was directly compared with no patch in [18 fresh Astra trials](../CODEX_WAITING_LATEST_VS_NO_PATCH_BENCHMARK.md): model responses fell 98→47, input 51.03%, and API-price equivalents 42.31%. All nine matched pairs improved on those measures; completion delays varied. See [the latest phase's reproduction instructions and evidence](numeric-waits/README.md#exact-current-wording-versus-no-patch). The sections below preserve the original study and its earlier prompt versions.

This experiment uses actual Codex subscription inference and consumes normal account usage. Read [PLAN.md](PLAN.md) for the comparison design. The final report distinguishes client release changes, prompt changes, and historical server-side changes that cannot be recreated.

The original three primary conditions are official CLI 0.151.0, official CLI 0.154.0, and CLI 0.154.0 with [the frozen original addition](AGENTS.initial.md). The current backend rejects Astra on 0.151.0, so that cell is unavailable, not zero-cost. A later user-requested follow-up successfully uses official 0.153.1 as Astra's earlier-client baseline. Unlike Sol's 0.151.0 baseline, it already includes PR #41243. All clients receive the same pinned current model catalog; this permits a controlled current-model comparison, not a replay of historical model behavior or bundled catalog differences.

`benchmark.py` creates private temporary Codex homes, copies existing authentication privately, runs bounded jobs, exports selected diagnostic data, and removes the temporary homes. It does not change the normal installation. The parent and child models use low reasoning. CLI and tool versions, prompt and catalog hashes, returned counters, completion signals, and messages are recorded.

The terminal workload is a real sleeping process that emits a fixed result after 75 seconds. The subagent workload delegates that command to one real model-driven child. CI is a local status simulator with no push notification or watcher; it is not an actual GitHub Actions run. Repetitions use reversed condition order, with at most two trials running concurrently. Timing, changing prefixes, and cache routing remain sources of variation.

Example from the repository root, after placing the verified old release and matching code-mode host under `tmp/codex-versions/0.151.0/` and saving the model catalog:

```sh
python3 docs/waiting-benchmark/benchmark.py \
  --source-home .codex_home \
  --old-binary tmp/codex-versions/0.151.0/codex-aarch64-apple-darwin \
  --new-binary /opt/homebrew/bin/codex \
  --catalog tmp/wait-benchmark-catalog.json \
  --patch docs/waiting-benchmark/AGENTS.initial.md \
  --out tmp/wait-benchmark-main --repetitions 2 --workers 2 --delay 75
```

Existing trial files are skipped, never overwritten. A non-successful trial is retained and must be investigated before inclusion as a successful comparison. The per-trial deadline is workload delay plus 150 seconds; an item-count limit bounds pathological loops.

`accounting.py` calculates Standard API-price equivalents from the subscription-reported categories, using per-request long-context rates when required. These are not actual subscription dollar charges. Ordinary input equals total input minus cache reads minus cache writes. Reasoning is included in output. The runtime can map absent cache-write fields to zero, so a zero reported write count does not prove that a corresponding API request would have no cache writes.

`analyze.py` deduplicates response identities, validates prompt loading and single job execution, and exports counts, costs, and selected traces. Old-client raw response notifications supply both parent and child usage; any legacy fallback uses the last-usage records from distinct cumulative snapshots and checks their sum against the final cumulative counters. Cumulative snapshots are never summed as if they were per-response usage.

```sh
python3 -m unittest discover -s docs/waiting-benchmark -p test_accounting.py
python3 docs/waiting-benchmark/analyze.py tmp/wait-benchmark-main --out docs/waiting-benchmark/results
```

The accounting tests verify category separation, included reasoning, and per-request long-context pricing. They are not new live trials. Smoke/setup failures are separate from measured workloads, including the rejected old-client Astra attempt and the initially missing old code-mode host.

No short trial measures a 30-minute cache TTL, subscription allowance conversion, or the backend conditions before the September 12 announcement. [provenance.json](provenance.json) records release identities and download hashes.

## Astra 0.153.1 follow-up

PR #42605 backported the Astra catalog to the 0.153 release branch. The official 0.153.1 binary and matching code-mode host passed a two-second compatibility probe with today's subscription backend. Download digests, release identity, catalog checks, and source ancestry are recorded in [astra-1531-provenance.json](astra-1531-provenance.json). This release already includes #41243; it is not a pre-fix substitute for the rejected 0.151.0 Astra cell. The pinned current catalog also means this experiment does not measure differences between the bundled catalogs.

After placing the verified assets under `tmp/codex-versions/0.153.1/`, run the six configured-environment trials:

```sh
python3 docs/waiting-benchmark/benchmark.py \
  --source-home .codex_home \
  --old-binary tmp/codex-versions/0.153.1/codex-aarch64-apple-darwin \
  --new-binary /opt/homebrew/bin/codex \
  --catalog tmp/wait-benchmark-catalog.json \
  --patch docs/waiting-benchmark/AGENTS.initial.md \
  --out tmp/wait-benchmark-astra-1531 \
  --models gpt-6-astra --conditions old \
  --repetitions 2 --workers 2 --delay 75
```

For the three clean trials, change the output to `tmp/wait-benchmark-astra-1531-clean`, set `--repetitions 1`, and add `--no-skill-instructions`. They were queued with `--after-dir tmp/wait-benchmark-astra-1531 --after-count 6`. The `old` condition installs no waiting patch; passing the frozen patch path does not activate it. The runner skips the known rejected Astra/0.151.0 pair specifically, while allowing other older binaries to be tested.

The [configured counts](astra-1531-results/COUNTS.md) and [clean counts](astra-1531-clean-results/COUNTS.md) contain only the nine new 75-second workloads. Their `COMPARISON.md` and `comparison-metrics.json` files reuse the corresponding earlier Astra 0.154.0 `new` and `patch` controls; they are convenience views, not additional executions or fresh interleaved comparisons. Setup smoke usage is excluded from these workload totals. Historical result directories and frozen prompts are preserved.

## Clean comparison and tuning

Temporary `CODEX_HOME` alone does not isolate shared `~/.agents/skills`. Primary results retain that configured environment. To remove the automatic skill catalog, add `--no-skill-instructions`; this sets `[skills] include_instructions=false` and `[skills.bundled] enabled=false`. The analyzer verifies no catalog block or skill-reading tool call was recorded, including child sessions. The actual shared files are unchanged.

The clean phase uses the same command with these argument changes:

```sh
--out tmp/wait-benchmark-clean --conditions old,new,patch,tuned \
--tuned-patch docs/waiting-benchmark/AGENTS.tuned-v2.md \
--repetitions 1 --no-skill-instructions
```

`--after-dir tmp/wait-benchmark-main --after-count 30` can queue this phase until all 30 primary records exist. The queue is handled locally without model status polling. Its 30-minute watchdog fails explicitly if the preceding phase does not produce the expected records.

The frozen initial and tuned prompts are kept separately. V1 is an untested intermediate; v2 is the clean-phase candidate. Setup smoke evidence is exported separately and does not enter primary 75-second aggregates.

V3 is a second, separate candidate: `AGENTS.tuned-v3.md`. It uses a brief update before a model-issued wait call and a 45-second limit when a 60-second update cadence applies. The fresh v3 output directory is `tmp/wait-benchmark-v3`; compare its `tuned` rows with the earlier clean controls, not with the identically named v2 `tuned` rows as though they were repetitions of one prompt. Prompt hashes distinguish them.

The sleep-tool diagnostic uses `--conditions new-on,tuned-on --models gpt-5.6-sol --scenarios ci`, with v2 as its tuned prompt. It is a separate two-trial configuration comparison. All phases retain their own output directories and counter tables.

Timing definition: `result_delay_seconds` measures the final answer's recorded completion timestamp minus the authoritative job completion time. It includes status-detection and final model-response latency. `max_parent_message_gap_seconds` uses completed parent messages (including final), plus the initial turn-to-first-message gap. These are not first-streamed-token timestamps; interpret tiny cadence overages cautiously.

## Historical compact export and completed original phases

The final compact Astra phase freezes the exported wording in [AGENTS.compact-final.md](AGENTS.compact-final.md). Its reproduction command is:

```sh
python3 docs/waiting-benchmark/benchmark.py \
  --source-home .codex_home \
  --old-binary tmp/codex-versions/0.153.1/codex-aarch64-apple-darwin \
  --new-binary /opt/homebrew/bin/codex \
  --catalog tmp/wait-benchmark-catalog.json \
  --patch docs/waiting-benchmark/AGENTS.compact-final.md \
  --out tmp/wait-benchmark-compact-final-astra \
  --models gpt-6-astra --conditions patch \
  --repetitions 1 --workers 2 --delay 75 --no-skill-instructions
```

The three final-patch workloads reuse the existing clean Astra controls from `astra-1531-clean-results` (condition 1) and `clean-results` (condition 2). The requested tables compare sequential observations, not fresh interleaved pairs. Earlier initial/v3/v4 patch rows are not substituted for this compact version.

The tested v4 wording is frozen in [AGENTS.tuned-v4.md](AGENTS.tuned-v4.md). The historical [AGENTS.compact-final.md](AGENTS.compact-final.md) completed the three clean Astra workloads above. Their [counts](compact-final-astra-results/COUNTS.md), [two comparison tables](compact-final-astra-results/COMPARISON.md), and [provenance](compact-final-astra-provenance.json) are separate from earlier v3/v4 measurements. Sol has not been tested with that compact rewrite. V4 changes only the CI watcher clause from v3; its two CI trials are in `tmp/wait-benchmark-v4`, while its unchanged terminal/subagent clauses were exercised under v3 and were not rerun as a whole v4 suite.

Subsequent measurements revised the export. The current distribution file and this workspace's `.codex_home/AGENTS.md` now match [AGENTS.wording-no-pragma.md](numeric-waits/prompts/AGENTS.wording-no-pragma.md). The [numeric-waits follow-up documentation](numeric-waits/README.md) records those revisions and the final direct no-patch comparison. Historical frozen prompts and result directories remain unchanged.

Completed original phases: 30 configured-environment trials, 21 clean comparison trials, 2 always-on diagnostics, 6 v3 validation trials, 2 v4 CI trials (61 total). The Astra 0.153.1 follow-up adds six configured and three clean trials; the compact-final phase adds three clean Astra trials, bringing the total to 73. Every workload completed correctly. See [the final report](../CODEX_WAITING_RUNTIME_PROMPT_BENCHMARK.md) for limits and model-specific conclusions.

Reanalyze any completed phase by passing its raw directory to `analyze.py --out <phase-results-directory>`. Each result directory contains `metrics.json`, `trial-evidence.json`, and `COUNTS.md` (including category-specific dollars and separate parent/child counts). `report_tables.py` renders aggregate tables from a metrics file. [audit-summary.json](audit-summary.json) preserves the original 61-trial totals, exclusions, and frozen final prompt hash. [astra-1531-audit-summary.json](astra-1531-audit-summary.json) preserves the subsequent 70-trial audit. [compact-final-astra-audit-summary.json](compact-final-astra-audit-summary.json) records the three compact-patch workloads and combined 73-trial totals without double-counting reused controls.
