# Final skill versus no skill: recorded counts

September 14, 2026 Standard API valuation of subscription counters; not subscription charges. Recorded write zeros can represent unreported fields.

Each condition contains nine trials. Counts include parent and child inference and skill loading. Input includes cached reads and recorded writes; reasoning is already included in output.

| Metric | No skill | Final v4 skill |
| --- | ---: | ---: |
| Model responses | 100 | 64 |
| Input total | 1,547,548 | 1,028,592 |
| Ordinary input | 106,396 | 76,784 |
| Cached reads | 1,441,152 | 951,808 |
| Recorded cache writes | 0 | 0 |
| Output | 4,000 | 4,599 |
| Reasoning included in output | 300 | 122 |
| API USD: uncached | $1.063960 | $0.767840 |
| API USD: cached | $1.441152 | $0.951808 |
| API USD: write | $0.000000 | $0.000000 |
| API USD: output | $0.200000 | $0.229950 |
| API USD: total | $2.705112 | $1.949598 |

## Workloads

| Workload | Responses: no skill → v4 | Input: no skill → v4 | API USD: no skill → v4 | Mean delivery delay: no skill → v4 |
| --- | ---: | ---: | ---: | ---: |
| terminal | 27 → 13 | 419,569 → 207,391 | $0.680330 → $0.408696 | 3.589 s → 3.839 s |
| subagent | 49 → 30 | 757,371 → 478,523 | $1.428170 → $0.867522 | 4.420 s → 12.239 s |
| ci | 24 → 21 | 370,608 → 342,678 | $0.596612 → $0.673380 | 5.805 s → 31.073 s |

## Parent and child accounting

| Trial | Scope | Responses | Input | Ordinary | Cached reads | Recorded writes | Output | Ordinary USD | Cached USD | Write USD | Output USD | Total USD |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| none-contextual-ci-r1 | parent | 8 | 123,471 | 4,815 | 118,656 | 0 | 262 | $0.048150 | $0.118656 | $0.000000 | $0.013100 | $0.179906 |
| none-contextual-ci-r1 | combined | 8 | 123,471 | 4,815 | 118,656 | 0 | 262 | $0.048150 | $0.118656 | $0.000000 | $0.013100 | $0.179906 |
| none-contextual-ci-r2 | parent | 8 | 123,616 | 8,032 | 115,584 | 0 | 269 | $0.080320 | $0.115584 | $0.000000 | $0.013450 | $0.209354 |
| none-contextual-ci-r2 | combined | 8 | 123,616 | 8,032 | 115,584 | 0 | 269 | $0.080320 | $0.115584 | $0.000000 | $0.013450 | $0.209354 |
| none-contextual-ci-r3 | parent | 8 | 123,521 | 7,809 | 115,712 | 0 | 271 | $0.078090 | $0.115712 | $0.000000 | $0.013550 | $0.207352 |
| none-contextual-ci-r3 | combined | 8 | 123,521 | 7,809 | 115,712 | 0 | 271 | $0.078090 | $0.115712 | $0.000000 | $0.013550 | $0.207352 |
| none-implicit-subagent-r1 | parent | 4 | 61,127 | 3,783 | 57,344 | 0 | 178 | $0.037830 | $0.057344 | $0.000000 | $0.008900 | $0.104074 |
| none-implicit-subagent-r1 | child | 11 | 170,420 | 21,684 | 148,736 | 0 | 450 | $0.216840 | $0.148736 | $0.000000 | $0.022500 | $0.388076 |
| none-implicit-subagent-r1 | combined | 15 | 231,547 | 25,467 | 206,080 | 0 | 628 | $0.254670 | $0.206080 | $0.000000 | $0.031400 | $0.492150 |
| none-implicit-subagent-r2 | parent | 5 | 76,563 | 6,931 | 69,632 | 0 | 186 | $0.069310 | $0.069632 | $0.000000 | $0.009300 | $0.148242 |
| none-implicit-subagent-r2 | child | 12 | 186,169 | 6,073 | 180,096 | 0 | 475 | $0.060730 | $0.180096 | $0.000000 | $0.023750 | $0.264576 |
| none-implicit-subagent-r2 | combined | 17 | 262,732 | 13,004 | 249,728 | 0 | 661 | $0.130040 | $0.249728 | $0.000000 | $0.033050 | $0.412818 |
| none-implicit-subagent-r3 | parent | 5 | 76,660 | 4,084 | 72,576 | 0 | 199 | $0.040840 | $0.072576 | $0.000000 | $0.009950 | $0.123366 |
| none-implicit-subagent-r3 | child | 12 | 186,432 | 21,056 | 165,376 | 0 | 478 | $0.210560 | $0.165376 | $0.000000 | $0.023900 | $0.399836 |
| none-implicit-subagent-r3 | combined | 17 | 263,092 | 25,140 | 237,952 | 0 | 677 | $0.251400 | $0.237952 | $0.000000 | $0.033850 | $0.523202 |
| none-implicit-terminal-r1 | parent | 8 | 123,392 | 7,808 | 115,584 | 0 | 331 | $0.078080 | $0.115584 | $0.000000 | $0.016550 | $0.210214 |
| none-implicit-terminal-r1 | combined | 8 | 123,392 | 7,808 | 115,584 | 0 | 331 | $0.078080 | $0.115584 | $0.000000 | $0.016550 | $0.210214 |
| none-implicit-terminal-r2 | parent | 11 | 172,205 | 9,389 | 162,816 | 0 | 517 | $0.093890 | $0.162816 | $0.000000 | $0.025850 | $0.282556 |
| none-implicit-terminal-r2 | combined | 11 | 172,205 | 9,389 | 162,816 | 0 | 517 | $0.093890 | $0.162816 | $0.000000 | $0.025850 | $0.282556 |
| none-implicit-terminal-r3 | parent | 8 | 123,972 | 4,932 | 119,040 | 0 | 384 | $0.049320 | $0.119040 | $0.000000 | $0.019200 | $0.187560 |
| none-implicit-terminal-r3 | combined | 8 | 123,972 | 4,932 | 119,040 | 0 | 384 | $0.049320 | $0.119040 | $0.000000 | $0.019200 | $0.187560 |
| v4-contextual-ci-r1 | parent | 6 | 97,614 | 5,582 | 92,032 | 0 | 578 | $0.055820 | $0.092032 | $0.000000 | $0.028900 | $0.176752 |
| v4-contextual-ci-r1 | combined | 6 | 97,614 | 5,582 | 92,032 | 0 | 578 | $0.055820 | $0.092032 | $0.000000 | $0.028900 | $0.176752 |
| v4-contextual-ci-r2 | parent | 7 | 114,093 | 10,029 | 104,064 | 0 | 670 | $0.100290 | $0.104064 | $0.000000 | $0.033500 | $0.237854 |
| v4-contextual-ci-r2 | combined | 7 | 114,093 | 10,029 | 104,064 | 0 | 670 | $0.100290 | $0.104064 | $0.000000 | $0.033500 | $0.237854 |
| v4-contextual-ci-r3 | parent | 8 | 130,971 | 10,267 | 120,704 | 0 | 708 | $0.102670 | $0.120704 | $0.000000 | $0.035400 | $0.258774 |
| v4-contextual-ci-r3 | combined | 8 | 130,971 | 10,267 | 120,704 | 0 | 708 | $0.102670 | $0.120704 | $0.000000 | $0.035400 | $0.258774 |
| v4-implicit-subagent-r1 | parent | 5 | 80,016 | 4,880 | 75,136 | 0 | 268 | $0.048800 | $0.075136 | $0.000000 | $0.013400 | $0.137336 |
| v4-implicit-subagent-r1 | child | 5 | 79,478 | 4,982 | 74,496 | 0 | 324 | $0.049820 | $0.074496 | $0.000000 | $0.016200 | $0.140516 |
| v4-implicit-subagent-r1 | combined | 10 | 159,494 | 9,862 | 149,632 | 0 | 592 | $0.098620 | $0.149632 | $0.000000 | $0.029600 | $0.277852 |
| v4-implicit-subagent-r2 | parent | 5 | 79,988 | 8,564 | 71,424 | 0 | 267 | $0.085640 | $0.071424 | $0.000000 | $0.013350 | $0.170414 |
| v4-implicit-subagent-r2 | child | 5 | 79,445 | 4,949 | 74,496 | 0 | 325 | $0.049490 | $0.074496 | $0.000000 | $0.016250 | $0.140236 |
| v4-implicit-subagent-r2 | combined | 10 | 159,433 | 13,513 | 145,920 | 0 | 592 | $0.135130 | $0.145920 | $0.000000 | $0.029600 | $0.310650 |
| v4-implicit-subagent-r3 | parent | 5 | 80,027 | 4,763 | 75,264 | 0 | 267 | $0.047630 | $0.075264 | $0.000000 | $0.013350 | $0.136244 |
| v4-implicit-subagent-r3 | child | 5 | 79,569 | 5,073 | 74,496 | 0 | 351 | $0.050730 | $0.074496 | $0.000000 | $0.017550 | $0.142776 |
| v4-implicit-subagent-r3 | combined | 10 | 159,596 | 9,836 | 149,760 | 0 | 618 | $0.098360 | $0.149760 | $0.000000 | $0.030900 | $0.279020 |
| v4-implicit-terminal-r1 | parent | 4 | 63,672 | 8,248 | 55,424 | 0 | 259 | $0.082480 | $0.055424 | $0.000000 | $0.012950 | $0.150854 |
| v4-implicit-terminal-r1 | combined | 4 | 63,672 | 8,248 | 55,424 | 0 | 259 | $0.082480 | $0.055424 | $0.000000 | $0.012950 | $0.150854 |
| v4-implicit-terminal-r2 | parent | 5 | 80,010 | 4,874 | 75,136 | 0 | 331 | $0.048740 | $0.075136 | $0.000000 | $0.016550 | $0.140426 |
| v4-implicit-terminal-r2 | combined | 5 | 80,010 | 4,874 | 75,136 | 0 | 331 | $0.048740 | $0.075136 | $0.000000 | $0.016550 | $0.140426 |
| v4-implicit-terminal-r3 | parent | 4 | 63,709 | 4,573 | 59,136 | 0 | 251 | $0.045730 | $0.059136 | $0.000000 | $0.012550 | $0.117416 |
| v4-implicit-terminal-r3 | combined | 4 | 63,709 | 4,573 | 59,136 | 0 | 251 | $0.045730 | $0.059136 | $0.000000 | $0.012550 | $0.117416 |

## Matched changes

Deltas are v4 minus no skill. Negative usage deltas mean lower usage; positive delay deltas mean slower result delivery.

| Case / repetition | Responses delta | Input delta | API USD delta | Delivery delay delta (s) |
| --- | ---: | ---: | ---: | ---: |
| contextual-ci / 1 | -2 | -25,857 | $-0.003154 | +0.137 |
| contextual-ci / 2 | -1 | -9,523 | $+0.028500 | +36.658 |
| contextual-ci / 3 | +0 | +7,450 | $+0.051422 | +39.010 |
| implicit-subagent / 1 | -5 | -72,053 | $-0.214298 | +7.571 |
| implicit-subagent / 2 | -7 | -103,299 | $-0.102168 | +7.977 |
| implicit-subagent / 3 | -7 | -103,496 | $-0.244182 | +7.909 |
| implicit-terminal / 1 | -4 | -59,720 | $-0.059360 | -4.299 |
| implicit-terminal / 2 | -6 | -92,195 | $-0.142130 | +5.010 |
| implicit-terminal / 3 | -4 | -60,263 | $-0.070144 | +0.040 |
