# Final compact patch: clean Astra comparison

Conditions reuse the existing earlier-client and unpatched controls. Each condition has three workloads; all token counts include children. Dollars are API-rate equivalents, and reported zero writes are not proof of absent actual writes.

| Model | Condition | Trials | Responses | Input total | Ordinary input | Cached reads | Writes reported | Output | API-rate USD |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Astra | (1) 0.153.1, no patch | 3 | 30 | 464,030 | 29,470 | 434,560 | 0 | 1,258 | $0.792160 |
| Astra | (2) 0.154.0, no patch | 3 | 36 | 555,974 | 40,262 | 515,712 | 0 | 1,413 | $0.988982 |
| Astra | (3) 0.154.0 + final compact patch | 3 | 16 | 252,200 | 24,488 | 227,712 | 0 | 1,120 | $0.528592 |

Pre = unpatched 0.154.0; post = final compact patch on 0.154.0.

| Model / workload | Combined responses, pre→post | Input total, pre→post | API-rate USD, pre→post | Result delay (s), pre→post | Maximum parent update gap (s), pre→post |
| --- | ---: | ---: | ---: | ---: | ---: |
| Astra / ci | 8→4 | 123,659→63,656 | $0.268036→$0.125336 | 11.00→27.34 | 58.15→45.33 |
| Astra / subagent | 19→8 | 293,066→125,649 | $0.490254→$0.259968 | 7.01→6.99 | 82.37→48.17 |
| Astra / terminal | 9→4 | 139,249→62,895 | $0.230692→$0.143288 | 4.79→8.22 | 77.56→45.84 |
