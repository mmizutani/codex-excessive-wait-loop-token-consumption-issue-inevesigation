# Evaluate the waiting skill

This directory contains the fixtures, frozen skill versions, graders, and selected execution evidence for [the skill evaluation report](../../../docs/reports/CODEX_WAITING_SKILL_EVALUATION.md). The suite is bundled in the skill’s `evals/` directory. Normal use follows the parent `SKILL.md`, which does not load these evaluation files. Run the evaluation tools from this repository: they also use its benchmark collector and historical fixtures.

Frozen versions use `versions/v*/SKILL.md.fixture`: Codex CLI 0.154.0 recursively discovers files named `SKILL.md`, so keeping that name for archived versions would expose duplicate skills when this package is installed. `run.py` restores the filename to `SKILL.md` in each isolated test home. Snapshot contents and recorded hashes are unchanged. The older package-validation records retain their original paths as historical evidence.

## What is measured

The [predeclared plan](PLAN.md) separates activation, outcomes, process, and efficiency. The [12 cases](cases.json) include explicit invocation, automatic discovery, CI, a real child agent, forced Code Mode cell resumption, command failure, independent work, a limited observation, and four negative controls.

`run.py` runs actual Codex app-server turns in isolated temporary homes. It verifies that only this skill is enabled, or that no skills are enabled for a `none` control, and that no AGENTS.md is installed. It includes skill reads and child responses in accounting. `grade.py` checks captured facts; `judge.py` provides an independent, read-only review of selected traces using the [structured rubric](rubric.schema.json). Its usage is separate from the workload measurements. Qualitative review requires checking its conclusions against the complete evidence.

## Run from the repository root

Regrade the checked-in evidence without model calls or authentication:

```sh
python3 skills/codex-wait-efficiently/evals/summarize.py \
  --evidence skills/codex-wait-efficiently/evals/results/final/trial-evidence.json \
  --out tmp/wait-skill-rechecked
python3 skills/codex-wait-efficiently/evals/verify.py
```

For live runs, prerequisites are Python 3, Codex CLI 0.154.0, the study's pinned catalog at `tmp/wait-benchmark-catalog.json`, and existing subscription login in `.codex_home/auth.json`. The catalog hash is pinned in `run.py`; recover the matching model catalog from the original study environment before attempting a strict reproduction. A current catalog or newer runtime requires a separately identified evaluation.

Live runs consume normal account usage. Each run uses a temporary private copy of the login, removes it afterward, and exports selected calls, outputs, and counters. Do not distribute authentication files or complete private session logs.

```sh
python3 -m unittest discover -s skills/codex-wait-efficiently/evals -p 'test_*.py'
python3 skills/codex-wait-efficiently/evals/run.py --phase discovery --prepare-only
python3 skills/codex-wait-efficiently/evals/run.py --phase discovery
python3 skills/codex-wait-efficiently/evals/run.py --phase revised --versions v2
python3 skills/codex-wait-efficiently/evals/run.py --phase sharpened --versions v3
python3 skills/codex-wait-efficiently/evals/run.py --phase confirmation --versions v1,v2 \
  --cases implicit-terminal,contextual-ci,implicit-subagent,explicit-observation-limit \
  --repetitions 2
python3 skills/codex-wait-efficiently/evals/run.py --phase handoff --versions v4 \
  --cases implicit-subagent --repetitions 2
python3 skills/codex-wait-efficiently/evals/run.py --phase final-suite --versions v4
python3 skills/codex-wait-efficiently/evals/summarize.py discovery revised sharpened confirmation handoff final-suite \
  --out tmp/wait-skill-eval-scores
python3 skills/codex-wait-efficiently/evals/judge.py discovery \
  --out tmp/wait-skill-discovery-judgment.json
```

Use a new `--phase` for a fresh repetition; completed trial files are reused, never silently rerun. Frozen manifests reject changes to the case set, seed, or skill hash. `--prepare-only` writes a manifest without inference. Live runs use at most two workers. Raw files go to the ignored `tmp/wait-skill-evals/<phase>/`; exported records retain every trial, including failed checks.

The `confirmation-final` manifest for v1/v3 was prepared but never executed. The longer v3 candidate did not demonstrate added value, so the [revision log](REVISIONS.md) records its rejection and the return to v2 for the original `confirmation` block. That block exposed a child handoff failure, motivating v4 and two dedicated child tests followed by its complete suite. All intermediate results remain part of the evidence.

The inherited collector's `success` field means that it saw the original benchmark completion marker. Expected command failure, pending observations, and negative controls can therefore have `success: false`. Use the new `evaluation.checks.outcome` and individual checks to assess these cases. `overall_pass` covers the deterministic checks only; watcher choice and other qualitative process rules are reviewed separately.

The dollar figures apply the original study's dated API rate card to reported subscription tokens. They are not subscription charges or a measurement of quota percentages. Recorded cache-write zeros may represent missing upstream fields. Repeating with a different account, cache state, model catalog, or runtime can change both behavior and usage.

## Final skill versus no skill

The separate [comparison plan](comparisons/skill-vs-none/PLAN.md) freezes 18 fresh trials: three repetitions each of implicit terminal, subagent, and CI tasks under `none` and `v4`. The same unnamed task prompts are used in both conditions. The `none` control also disables any shared copy of the target skill. Explicit skill-mention cases are rejected for this control. A final-skill activation miss remains part of the comparison.

Reproduce the scheduled comparison with the live prerequisites above. `--prepare-only` checks or writes the manifest without inference; remove it to execute the trials. The checked-in phase name reuses any completed local trial files. For an independent repetition, choose a new phase name and a separate manifest directory.

```sh
python3 skills/codex-wait-efficiently/evals/run.py \
  --phase skill-vs-none --versions none,v4 \
  --cases implicit-terminal,implicit-subagent,contextual-ci --repetitions 3 \
  --manifest-dir skills/codex-wait-efficiently/evals/comparisons/skill-vs-none \
  --prepare-only
```

Execute the live trials, then export and verify their results:

```sh
python3 skills/codex-wait-efficiently/evals/run.py \
  --phase skill-vs-none --versions none,v4 \
  --cases implicit-terminal,implicit-subagent,contextual-ci --repetitions 3 \
  --manifest-dir skills/codex-wait-efficiently/evals/comparisons/skill-vs-none
python3 skills/codex-wait-efficiently/evals/summarize.py skill-vs-none \
  --out skills/codex-wait-efficiently/evals/comparisons/skill-vs-none
python3 skills/codex-wait-efficiently/evals/compare_controls.py
```

To regrade the published comparison without model calls or credentials:

```sh
python3 skills/codex-wait-efficiently/evals/summarize.py \
  --evidence skills/codex-wait-efficiently/evals/comparisons/skill-vs-none/trial-evidence.json \
  --out tmp/wait-skill-control-rechecked
python3 skills/codex-wait-efficiently/evals/compare_controls.py
```

`compare_controls.py` verifies the complete 18-trial manifest, frozen skill and case hashes, unchanged AGENTS.md patch, identical paired task prompts, common base instructions, actual condition isolation, unique responses, and reconciled parent/child accounting. It writes aggregate and paired token/cost/latency results to `comparison.json` and `COUNTS.md`. The earlier 66-trial evidence remains under `results/final/`.
