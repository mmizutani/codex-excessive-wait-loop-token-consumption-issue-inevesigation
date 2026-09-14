# Waiting skill evaluation plan

This suite follows [OpenAI's skill evaluation workflow](https://developers.openai.com/blog/eval-skills): define observable success, test explicit and implicit use plus negative controls, retain execution evidence, and revise only in response to failures. The existing app-server collector supplies structured events and per-response accounting instead of starting a separate `codex exec --json` collector.

## Scope and controls

- Freeze the existing skill as `versions/v1` before running it. Keep the final AGENTS.md patch unchanged.
- Use real CLI 0.154.0, Astra/low, the existing pinned catalog and subscription authentication. Fresh temporary homes/workspaces contain no AGENTS.md. Disable bundled and unrelated shared skills by name; verify only the target skill is enabled. Never copy credentials into exported artifacts.
- Explicit cases use a normal skill input attachment plus a named user prompt. Implicit and negative cases receive only their task text and the skill catalog, with no injected skill body.
- Run the 12 cases in `cases.json` once as a discovery pass. Review failures and complete traces before choosing a candidate. Preserve all trials, including failures.
- If a revision is justified, freeze it separately and rerun the complete suite. Then repeat the affected cases and the three core implicit workloads against both frozen versions in interleaved order. Do not infer savings from discarded failures or silently rerun until passing.
- Long core jobs last 75 seconds. Failure, observation-limit, and negative cases are shorter. Each trial has a finite wall-clock and event-count limit. At most two model workloads run concurrently. A driver timeout is reported as incomplete, never as a successful cheap run.

## Scores, defined before running

Report dimensions separately rather than hiding failures inside one aggregate score:

1. **Activation:** the body actually reaches a session, through explicit skill injection or a successful file read. A catalog entry or a claim to use the skill alone is insufficient. Expected positives must load it; negative controls must not.
2. **Outcome and scope:** correct result after actual completion, one job/child as requested, no fixture changes; a failed command is reported as failed, and an observation limit preserves pending status. Independent work must produce the correct artifact before the command completes.
3. **Process:** retain process/cell identity; avoid short preliminary polls; respect the requested observation count; measure parent progress gaps against 60 seconds. Inspect full call text for wrapper/inner relations and generated watcher limits. Do not require exact wait numbers or count setup reads as process polls.
4. **Efficiency:** unique parent/child model responses, ordinary input, cached reads, recorded cache writes, output and API-price equivalent using the existing dated rate card; report delivery delay separately. Skill loading overhead counts.

Use deterministic checks for execution facts and retain human-readable reasons for manual trace judgments. Add a structured model-assisted review only where qualitative interpretation cannot be reliably decided from those facts. Test the graders with deliberately bad records so failed or unstarted work cannot appear as success.

## Limits and completion

This is a small skill evaluation, not a replay of the earlier no-patch comparison. Automatic discovery, explicit invocation, and child loading are separate observations. It does not establish Sol effects, long-term cache retention, production CI integration, or every `/goal` state transition.

Export results and a Markdown report with TL;DR, initial misses, exact changes, final outcomes, accounting, remaining limitations, and reproduction commands. Update installation documentation to distinguish the evaluated skill from the unchanged AGENTS.md patch. Keep runtime artifacts and graders outside the installable skill so they do not enter routine model context.

## Post-evaluation packaging update

After the evaluation, the user requested moving this suite into `skills/codex-wait-efficiently/evals/`. This supersedes the original packaging choice above. The evaluated skill instructions, frozen inputs, and captured results are unchanged; the skill instructions do not load the evaluation suite.

A discovery-only check after the move found that the archived `SKILL.md` files were also listed as skills. Their filenames now end in `.fixture`; the evaluator restores `SKILL.md` when installing a selected snapshot into a temporary home. File contents and recorded hashes are preserved.
