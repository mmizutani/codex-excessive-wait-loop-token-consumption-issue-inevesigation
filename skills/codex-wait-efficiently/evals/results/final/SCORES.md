# Skill evaluation scores

September 14, 2026 Standard API valuation of subscription counters; not subscription charges. Recorded write zeros may be unreported.

| Phase | Version / case | Activated | Pass | Failed checks | Responses | Input | Ordinary | Cached reads | Writes | Output | API USD | Delay (s) | Max parent gap (s) |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| discovery | v1 / contextual-ci | True | True | — | 7 | 114,449 | 5,905 | 108,544 | 0 | 679 | $0.201544 | 42.449 | 48.595 |
| discovery | v1 / explicit-cell | True | True | — | 5 | 79,938 | 8,642 | 71,296 | 0 | 307 | $0.173066 | 1.979 | 42.334 |
| discovery | v1 / explicit-failure | True | True | — | 3 | 47,423 | 4,287 | 43,136 | 0 | 213 | $0.096656 | None | 16.454 |
| discovery | v1 / explicit-independent-work | True | True | — | 6 | 96,603 | 9,179 | 87,424 | 0 | 422 | $0.200314 | 2.067 | 44.531 |
| discovery | v1 / explicit-observation-limit | True | True | — | 7 | 112,850 | 5,330 | 107,520 | 0 | 382 | $0.179920 | None | 45.904 |
| discovery | v1 / explicit-terminal | True | True | — | 5 | 79,753 | 7,817 | 71,936 | 0 | 328 | $0.166506 | 5.009 | 43.953 |
| discovery | v1 / implicit-subagent | True | True | — | 9 | 155,150 | 20,110 | 135,040 | 0 | 533 | $0.362790 | 5.608 | 57.929 |
| discovery | v1 / implicit-terminal | True | True | — | 5 | 79,877 | 4,997 | 74,880 | 0 | 330 | $0.141350 | 5.156 | 44.552 |
| discovery | v1 / negative-doc-edit | False | True | — | 5 | 77,692 | 7,420 | 70,272 | 0 | 291 | $0.159022 | None | 14.304 |
| discovery | v1 / negative-explanation | False | True | — | 1 | 15,266 | 3,106 | 12,160 | 0 | 57 | $0.046070 | None | 12.756 |
| discovery | v1 / negative-one-status | False | True | — | 2 | 30,701 | 3,437 | 27,264 | 0 | 73 | $0.065284 | None | 7.794 |
| discovery | v1 / negative-quick-command | False | True | — | 2 | 30,634 | 3,370 | 27,264 | 0 | 55 | $0.063714 | None | 6.519 |
| revised | v2 / contextual-ci | True | True | — | 8 | 130,766 | 5,838 | 124,928 | 0 | 713 | $0.218958 | 41.986 | 48.53 |
| revised | v2 / explicit-cell | True | True | — | 6 | 96,459 | 9,163 | 87,296 | 0 | 356 | $0.196726 | 6.422 | 45.082 |
| revised | v2 / explicit-failure | True | True | — | 3 | 47,394 | 7,202 | 40,192 | 0 | 196 | $0.122012 | None | 16.155 |
| revised | v2 / explicit-independent-work | True | True | — | 6 | 96,615 | 5,223 | 91,392 | 0 | 408 | $0.164022 | 2.125 | 43.451 |
| revised | v2 / explicit-observation-limit | True | True | — | 4 | 63,910 | 4,774 | 59,136 | 0 | 494 | $0.131576 | None | 39.558 |
| revised | v2 / explicit-terminal | True | True | — | 5 | 79,961 | 5,081 | 74,880 | 0 | 344 | $0.142890 | 5.765 | 44.077 |
| revised | v2 / implicit-subagent | True | True | — | 9 | 153,513 | 12,073 | 141,440 | 0 | 417 | $0.283020 | 5.599 | 58.16 |
| revised | v2 / implicit-terminal | True | True | — | 5 | 79,942 | 8,774 | 71,168 | 0 | 340 | $0.175908 | 5.617 | 43.946 |
| revised | v2 / negative-doc-edit | False | True | — | 5 | 77,710 | 4,366 | 73,344 | 0 | 272 | $0.130604 | None | 13.181 |
| revised | v2 / negative-explanation | False | True | — | 1 | 15,274 | 3,114 | 12,160 | 0 | 57 | $0.046150 | None | 7.322 |
| revised | v2 / negative-one-status | False | True | — | 2 | 30,686 | 3,422 | 27,264 | 0 | 77 | $0.065334 | None | 7.796 |
| revised | v2 / negative-quick-command | False | True | — | 2 | 30,665 | 3,401 | 27,264 | 0 | 55 | $0.064024 | None | 6.41 |
| sharpened | v3 / contextual-ci | True | False | parent_update_cadence | 7 | 114,006 | 9,942 | 104,064 | 0 | 617 | $0.234334 | 28.274 | 68.464 |
| sharpened | v3 / explicit-cell | True | True | — | 6 | 96,568 | 5,432 | 91,136 | 0 | 377 | $0.164306 | 5.915 | 45.022 |
| sharpened | v3 / explicit-failure | True | True | — | 3 | 47,423 | 4,287 | 43,136 | 0 | 207 | $0.096356 | None | 15.676 |
| sharpened | v3 / explicit-independent-work | True | True | — | 6 | 96,785 | 9,233 | 87,552 | 0 | 417 | $0.200732 | 2.044 | 44.055 |
| sharpened | v3 / explicit-observation-limit | True | True | — | 5 | 80,551 | 8,103 | 72,448 | 0 | 482 | $0.177578 | None | 38.955 |
| sharpened | v3 / explicit-terminal | True | True | — | 4 | 63,639 | 4,631 | 59,008 | 0 | 251 | $0.117868 | 1.757 | 42.539 |
| sharpened | v3 / implicit-subagent | True | True | — | 10 | 173,900 | 27,724 | 146,176 | 0 | 542 | $0.450516 | 3.605 | 56.634 |
| sharpened | v3 / implicit-terminal | True | True | — | 5 | 80,076 | 4,812 | 75,264 | 0 | 332 | $0.139984 | 4.966 | 43.774 |
| sharpened | v3 / negative-doc-edit | False | True | — | 5 | 77,658 | 4,314 | 73,344 | 0 | 282 | $0.130584 | None | 13.691 |
| sharpened | v3 / negative-explanation | False | True | — | 1 | 15,266 | 3,106 | 12,160 | 0 | 54 | $0.045920 | None | 7.847 |
| sharpened | v3 / negative-one-status | False | True | — | 2 | 30,702 | 3,438 | 27,264 | 0 | 73 | $0.065294 | None | 7.806 |
| sharpened | v3 / negative-quick-command | False | True | — | 2 | 30,607 | 3,343 | 27,264 | 0 | 61 | $0.063744 | None | 6.729 |
| confirmation | v1 / contextual-ci | True | True | — | 7 | 114,368 | 10,304 | 104,064 | 0 | 674 | $0.240804 | 40.653 | 43.975 |
| confirmation | v1 / contextual-ci | True | True | — | 7 | 114,409 | 10,089 | 104,320 | 0 | 703 | $0.240360 | 31.498 | 54.222 |
| confirmation | v1 / explicit-observation-limit | True | True | — | 7 | 112,798 | 5,406 | 107,392 | 0 | 389 | $0.180902 | None | 45.543 |
| confirmation | v1 / explicit-observation-limit | True | True | — | 7 | 112,717 | 5,581 | 107,136 | 0 | 381 | $0.181996 | None | 46.027 |
| confirmation | v1 / implicit-subagent | True | True | — | 10 | 173,736 | 16,680 | 157,056 | 0 | 568 | $0.352256 | 5.377 | 56.425 |
| confirmation | v1 / implicit-subagent | True | True | — | 10 | 173,462 | 22,550 | 150,912 | 0 | 559 | $0.404362 | 4.112 | 55.949 |
| confirmation | v1 / implicit-terminal | True | True | — | 5 | 79,758 | 4,878 | 74,880 | 0 | 313 | $0.139310 | 4.364 | 43.606 |
| confirmation | v1 / implicit-terminal | True | True | — | 4 | 63,530 | 4,650 | 58,880 | 0 | 247 | $0.117730 | 1.95 | 43.091 |
| confirmation | v2 / contextual-ci | True | True | — | 6 | 97,771 | 5,611 | 92,160 | 0 | 646 | $0.180570 | 31.336 | 58.195 |
| confirmation | v2 / contextual-ci | True | True | — | 8 | 130,803 | 5,875 | 124,928 | 0 | 699 | $0.218628 | 30.429 | 44.254 |
| confirmation | v2 / explicit-observation-limit | True | True | — | 4 | 63,947 | 4,811 | 59,136 | 0 | 458 | $0.130146 | None | 38.594 |
| confirmation | v2 / explicit-observation-limit | True | True | — | 4 | 63,928 | 4,792 | 59,136 | 0 | 355 | $0.124806 | None | 35.489 |
| confirmation | v2 / implicit-subagent | True | False | no_short_stdin_polls, no_short_cell_polls | 14 | 244,327 | 16,999 | 227,328 | 0 | 585 | $0.426568 | 7.667 | 58.684 |
| confirmation | v2 / implicit-subagent | True | True | — | 10 | 173,865 | 12,841 | 161,024 | 0 | 595 | $0.319184 | 3.602 | 56.022 |
| confirmation | v2 / implicit-terminal | True | True | — | 5 | 79,938 | 8,898 | 71,040 | 0 | 320 | $0.176020 | 6.535 | 44.813 |
| confirmation | v2 / implicit-terminal | True | True | — | 5 | 79,931 | 5,051 | 74,880 | 0 | 318 | $0.141290 | 5.661 | 43.64 |
| handoff | v4 / implicit-subagent | True | True | — | 10 | 159,489 | 9,857 | 149,632 | 0 | 612 | $0.278802 | 7.319 | 56.523 |
| handoff | v4 / implicit-subagent | True | True | — | 10 | 159,347 | 9,843 | 149,504 | 0 | 580 | $0.276934 | 5.907 | 57.859 |
| final-suite | v4 / contextual-ci | True | False | no_short_cell_polls | 7 | 114,492 | 5,820 | 108,672 | 0 | 639 | $0.198822 | 27.97 | 58.489 |
| final-suite | v4 / explicit-cell | True | True | — | 6 | 96,603 | 5,339 | 91,264 | 0 | 382 | $0.163754 | 4.623 | 43.594 |
| final-suite | v4 / explicit-failure | True | True | — | 3 | 47,434 | 4,298 | 43,136 | 0 | 207 | $0.096466 | None | 15.882 |
| final-suite | v4 / explicit-independent-work | True | True | — | 6 | 96,812 | 5,292 | 91,520 | 0 | 418 | $0.165340 | 2.908 | 44.043 |
| final-suite | v4 / explicit-observation-limit | True | True | — | 6 | 96,949 | 5,301 | 91,648 | 0 | 437 | $0.166508 | None | 51.789 |
| final-suite | v4 / explicit-terminal | True | True | — | 5 | 80,022 | 4,886 | 75,136 | 0 | 329 | $0.140446 | 3.984 | 43.441 |
| final-suite | v4 / implicit-subagent | True | True | — | 10 | 174,791 | 24,903 | 149,888 | 0 | 608 | $0.429318 | 5.287 | 56.037 |
| final-suite | v4 / implicit-terminal | True | True | — | 5 | 80,019 | 4,883 | 75,136 | 0 | 332 | $0.140566 | 4.368 | 43.596 |
| final-suite | v4 / negative-doc-edit | False | True | — | 5 | 77,620 | 19,636 | 57,984 | 0 | 290 | $0.268844 | None | 16.592 |
| final-suite | v4 / negative-explanation | False | True | — | 1 | 15,274 | 3,114 | 12,160 | 0 | 54 | $0.046000 | None | 7.164 |
| final-suite | v4 / negative-one-status | False | True | — | 2 | 30,701 | 3,437 | 27,264 | 0 | 73 | $0.065284 | None | 6.907 |
| final-suite | v4 / negative-quick-command | False | True | — | 2 | 30,649 | 3,385 | 27,264 | 0 | 55 | $0.063864 | None | 7.926 |
