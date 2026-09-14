#!/usr/bin/env python3
"""Render phase totals and workload comparisons from validated metrics."""
import argparse
from collections import defaultdict
import json
from pathlib import Path
from statistics import mean

def render(path):
    data=json.loads(path.read_text())
    rows=data['trials']
    grouped=defaultdict(list)
    for r in rows:
        grouped[(r['model'],r['condition'])].append(r)
    lines=['## Totals across all three workloads', '',
        'Counts and dollars in this table are sums, including children. Compare conditions with the same number of trials.', '',
        '| Model | Condition | Trials | Responses | Input total | Ordinary input | Cached reads | Writes reported | Output | API-rate USD |',
        '|---|---|---:|---:|---:|---:|---:|---:|---:|---:|']
    order={'old':0,'new':1,'patch':2,'tuned':3,'new-on':4,'tuned-on':5}
    for (model,condition),items in sorted(grouped.items(),key=lambda kv:(kv[0][0],order.get(kv[0][1],9))):
        counts={k:sum(r['scopes']['combined']['tokens'].get(k,0) for r in items)
                for k in ['input','uncached','cached','write','output']}
        responses=sum(r['scopes']['combined']['responses'] for r in items)
        usd=sum(r['scopes']['combined']['usd']['total'] for r in items)
        lines.append('| '+' | '.join([model,condition,str(len(items)),str(responses)]+
            [f'{counts[k]:,}' for k in counts]+[f'${usd:.6f}'])+' |')
    lines.extend(['', '## Workload outcomes', '',
        'Each row is the mean of its repetitions except maximum update gap. P+C means parent plus child responses. Costs include both.', '',
        '| Model | Workload | Condition | n | Successes | P+C responses | API-rate USD | Result delay (s) | Maximum parent update gap (s) |',
        '|---|---|---|---:|---:|---:|---:|---:|---:|'])
    for g in sorted(data['groups'],key=lambda g:(g['model'],g['scenario'],order.get(g['condition'],9))):
        items=[r for r in rows if all(r[k]==g[k] for k in ['model','scenario','condition'])]
        child=mean(r['scopes']['child']['responses'] for r in items)
        lines.append('| '+' | '.join([g['model'],g['scenario'],g['condition'],str(g['n']),str(g['successes']),
            f"{g['parent_responses_mean']:g}+{child:g}",f"${g['combined_usd_mean']:.6f}",
            f"{g['result_delay_mean']:.2f}",f"{g['max_message_gap']:.2f}"])+' |')
    lines.extend(['', '## Aggregate contrasts', '',
        'Percent changes compare per-trial means; negative values are decreases. Small, non-randomized samples do not establish causal or population savings.', '',
        '| Model | Comparison | Combined responses change | Inclusive input change | API-rate USD change |',
        '|---|---|---:|---:|---:|'])
    for model in sorted({r['model'] for r in rows}):
        for before,after in [('old','new'),('new','patch'),('new','tuned'),('patch','tuned')]:
            a=grouped.get((model,before)); b=grouped.get((model,after))
            if not a or not b:continue
            values=[]
            for f in [lambda r:r['scopes']['combined']['responses'],
                      lambda r:r['scopes']['combined']['tokens']['input'],
                      lambda r:r['scopes']['combined']['usd']['total']]:
                values.append(100*(mean(map(f,b))/mean(map(f,a))-1))
            lines.append('| '+' | '.join([model,f'{before} → {after}']+[f'{v:+.2f}%' for v in values])+' |')
    return '\n'.join(lines)+'\n'

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('metrics',type=Path)
    p.add_argument('--out',type=Path,required=True)
    a=p.parse_args()
    a.out.write_text('# Waiting comparison tables\n\n'+render(a.metrics))
