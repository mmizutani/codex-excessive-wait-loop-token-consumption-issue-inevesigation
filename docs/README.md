# Documentation

**Start with the [latest verified AGENTS.md patch](guides/AGENTS.waiting-compatible.md) and its [Japanese explanation](guides/AGENTS.waiting-explanation.ja.md).** The patch's contents are unchanged; its distribution path is now `docs/guides/AGENTS.waiting-compatible.md`. Installation instructions and the measured-effects summary are in the [repository README](../README.md).

For skill-based installation, see the [English skill README](../skills/codex-wait-efficiently/README.md) or [日本語 README](../skills/codex-wait-efficiently/README.ja.md).

## Find what you need

| Location | Contents |
| --- | --- |
| [guides/](guides/) | The current verified patch and its explanation. |
| [reports/](reports/README.md) | Conclusions, measured effects, and limitations, with a reading order. |
| [waiting-benchmark/](waiting-benchmark/README.md) | Runtime and prompt benchmark scripts, study plans, token accounting, and captured results. |
| [waiting-validation/](waiting-validation/README.md) | Runtime probes, source and release provenance, and initial validation evidence. |
| [archive/](archive/README.md) | Superseded patches, the original investigation handoff and chat, and early distribution drafts. |

The skill's evaluation scripts and evidence remain inside its package at [skills/codex-wait-efficiently/evals/](../skills/codex-wait-efficiently/evals/README.md).

## Read the results

1. [Final AGENTS.md patch versus no patch](reports/CODEX_WAITING_LATEST_VS_NO_PATCH_BENCHMARK.md): the direct comparison of the current wording.
2. [Final skill versus no skill](reports/CODEX_WAITING_SKILL_VS_NO_SKILL_BENCHMARK.md): installation effects and the limits of comparing the two separate studies.
3. [Independent runtime validation](reports/CODEX_ASTRA_SOL_WAITING_INDEPENDENT_VALIDATION.md): waiting mechanisms, shipped fixes, and unresolved behavior.

For earlier prompt experiments and skill revisions, use the [report index](reports/README.md). Each report identifies the version it measured. Archived filenames containing `recommended` or `final` are historical labels.

## Evidence and reproduction

Captured JSON records, frozen manifests, raw logs, and patch contents retain their original data. Paths recorded in that evidence describe the layout at the time of the experiment. Maintained documentation and reproduction commands use the current layout; the [patch path index](archive/agents-patches/paths.json) and [resolver](waiting-benchmark/patch_paths.py) let benchmark tools read relocated patch files.

Reorganization does not constitute a new runtime measurement. Offline verification rechecks saved evidence; live benchmark commands consume account usage, as documented in their READMEs.
