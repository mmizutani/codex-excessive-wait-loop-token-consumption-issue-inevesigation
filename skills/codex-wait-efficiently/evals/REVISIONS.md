# Evidence-driven revision

## Original v1

`versions/v1` preserves the first skill package, whose operational paragraphs matched the final AGENTS.md patch. Its 12 discovery trials passed the deterministic activation and outcome checks. Qualitative trace review found a narrower process failure:

- `v1-explicit-observation-limit-r1` made three separate model-driven CI status calls, with two direct timers between them, although a bounded shell watcher was practical. The independent structured reviewer also classified this as a watcher-choice failure.
- `v1-contextual-ci-r1` did create a bounded watcher, but launched it with `exec_command` yielding after 1,000 ms and initially used the default outer Code Mode wait around a 45,000-ms `write_stdin`. The outer cell needed another model-driven resumption. The terminal rules were not consistently applied to a CI watcher.

The first issue distinguishes a successful outcome from following the intended waiting process. The second is visible in the full calls but is not covered by the short-`write_stdin` deterministic check. The complete traces remain authoritative.

## Candidate v2

Only the first paragraph under **CI and external work** changes. It explicitly keeps repeated scriptable checks inside one watcher, applies the Terminal commands rules to the watcher, and counts an initial query within a user-supplied observation limit. The other operational instructions, trigger description, and UI metadata stay unchanged. No fixed wait durations or installation resources are added.

The check-count clarification preserves the original user-limit requirement; no original trial exceeded that limit. It avoids ambiguity when moving formerly separate checks into one process.

Freeze v2 before its full-suite run. Evaluate the same 12 cases, then run two fresh repetitions of both versions for the affected observation-limit case and the three core implicit workloads. The confirmation manifest contains 16 shuffled, interleaved trials and is frozen before those trials start. Preserve every result; assess watcher choice, outcomes, latency, and usage separately. A lower response count in one discovery run is insufficient evidence of a general saving.

## Candidate v3 after the v2 suite

V2 passed all 12 deterministic checks. The observation-limit case used a watcher and fell from seven responses to four. However, its contextual-CI trial repeated the short watcher startup and mismatched outer wait, using eight responses versus the original trial's seven. The reference to another section did not reliably convey how to await the watcher.

V3 replaces that cross-reference with direct instructions for a long watcher-startup `exec_command` yield and an outer `functions.exec` wait covering each inner wait. It adds no fixed durations. All other paragraphs and metadata still match v1.

The prepared `confirmation` manifest for v1/v2 was deferred while v3 was tested. A separate `confirmation-final` manifest for v1/v3 was prepared before that comparison would begin. This was a plan adjustment, not a discarded run.

## Selection after v3

V3 repeated the short watcher startup in both CI cases and the default outer wait in contextual CI. Its contextual-CI run also missed the 60-second parent update cadence (68.464 seconds). The extra wording did not demonstrate the targeted process improvement. This small sample does not prove that the extra words caused the cadence miss.

Restore the more compact v2 package and execute the original frozen `confirmation` block, v1 versus v2, with two repetitions of each of four cases. The `confirmation-final` manifest remains **prepared but unexecuted**. All v3 workload trials remain exported, including the cadence failure. Make no claim that the selected skill enforces long watcher waits; evaluate its watcher-choice change and remaining limitations separately.

## V4: explicit delegation handoff after confirmation

`confirmation/v2-implicit-subagent-r1` completed correctly but used 14 model responses. Its parent read the skill and used direct `wait_agent`; its child made no fresh skill read/injection visible to the collector, used a 1,000-ms `write_stdin`, and briefly resumed a running cell with 1,000 ms. The child may have inherited earlier context through `fork_turns: all`; a parent read alone did not establish that the child applied the skill.

V4 retains v2's compact CI paragraph and adds one sentence under Subagent results: when delegating work that includes waiting, include an explicit `Use $codex-wait-efficiently` request in the child's task. This targets an observed handoff assumption instead of adding more terminal timing detail.

Freeze v4, run two fresh actual-child trials (`handoff`), and then the complete 12-case suite (`final-suite`). Preserve the v2 confirmation failure and all its usage. Do not claim universal child activation or general cost reduction from a small number of successful handoffs.

## Review-evidence correction

The original qualitative grader input omitted complete tool outputs for calls that read `SKILL.md`. One CI call also returned the initial status, so this caused the reviewer to mark that initial report uncertain. The complete workload evidence contains the status and supports the report. The later grader input omits only the skill-body block and retains sibling command outputs. This changes review-context completeness, not trial behavior, workload usage, or deterministic scores. The original judgment remains preserved.
