# Skill evaluation scores

September 14, 2026 Standard API valuation of subscription counters; not subscription charges. Recorded write zeros may be unreported.

| Phase | Version / case | Activated | Pass | Failed checks | Responses | Input | Ordinary | Cached reads | Writes | Output | API USD | Delay (s) | Max parent gap (s) |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| skill-vs-none | none / contextual-ci | False | True | — | 8 | 123,471 | 4,815 | 118,656 | 0 | 262 | $0.179906 | 7.582 | 56.685 |
| skill-vs-none | none / contextual-ci | False | True | — | 8 | 123,616 | 8,032 | 115,584 | 0 | 269 | $0.209354 | 5.027 | 55.48 |
| skill-vs-none | none / contextual-ci | False | True | — | 8 | 123,521 | 7,809 | 115,712 | 0 | 271 | $0.207352 | 4.805 | 54.851 |
| skill-vs-none | none / implicit-subagent | False | False | no_short_stdin_polls, parent_update_cadence | 15 | 231,547 | 25,467 | 206,080 | 0 | 628 | $0.492150 | 3.802 | 67.218 |
| skill-vs-none | none / implicit-subagent | False | False | no_short_stdin_polls, parent_update_cadence | 17 | 262,732 | 13,004 | 249,728 | 0 | 661 | $0.412818 | 5.749 | 67.061 |
| skill-vs-none | none / implicit-subagent | False | False | no_short_stdin_polls, parent_update_cadence | 17 | 263,092 | 25,140 | 237,952 | 0 | 677 | $0.523202 | 3.708 | 67.301 |
| skill-vs-none | none / implicit-terminal | False | False | no_short_stdin_polls, no_short_cell_polls, parent_update_cadence | 8 | 123,392 | 7,808 | 115,584 | 0 | 331 | $0.210214 | 6.326 | 75.948 |
| skill-vs-none | none / implicit-terminal | False | False | no_short_stdin_polls, parent_update_cadence | 11 | 172,205 | 9,389 | 162,816 | 0 | 517 | $0.282556 | 2.58 | 71.748 |
| skill-vs-none | none / implicit-terminal | False | False | no_short_stdin_polls, parent_update_cadence | 8 | 123,972 | 4,932 | 119,040 | 0 | 384 | $0.187560 | 1.861 | 65.853 |
| skill-vs-none | v4 / contextual-ci | True | True | — | 6 | 97,614 | 5,582 | 92,032 | 0 | 578 | $0.176752 | 7.719 | 43.671 |
| skill-vs-none | v4 / contextual-ci | True | True | — | 7 | 114,093 | 10,029 | 104,064 | 0 | 670 | $0.237854 | 41.685 | 45.846 |
| skill-vs-none | v4 / contextual-ci | True | True | — | 8 | 130,971 | 10,267 | 120,704 | 0 | 708 | $0.258774 | 43.815 | 49.023 |
| skill-vs-none | v4 / implicit-subagent | True | True | — | 10 | 159,494 | 9,862 | 149,632 | 0 | 592 | $0.277852 | 11.373 | 57.892 |
| skill-vs-none | v4 / implicit-subagent | True | True | — | 10 | 159,433 | 13,513 | 145,920 | 0 | 592 | $0.310650 | 13.726 | 57.74 |
| skill-vs-none | v4 / implicit-subagent | True | True | — | 10 | 159,596 | 9,836 | 149,760 | 0 | 618 | $0.279020 | 11.617 | 58.063 |
| skill-vs-none | v4 / implicit-terminal | True | True | — | 4 | 63,672 | 8,248 | 55,424 | 0 | 259 | $0.150854 | 2.027 | 41.958 |
| skill-vs-none | v4 / implicit-terminal | True | True | — | 5 | 80,010 | 4,874 | 75,136 | 0 | 331 | $0.140426 | 7.59 | 43.746 |
| skill-vs-none | v4 / implicit-terminal | True | True | — | 4 | 63,709 | 4,573 | 59,136 | 0 | 251 | $0.117416 | 1.901 | 42.395 |
