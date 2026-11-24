#!/usr/bin/env python3
"""Descriptive retention analysis. Explicit axes; no causal or predictive verdict."""
import argparse
import csv
import json
import math
from pathlib import Path
import sys


def load_csv(path):
    text = Path(path).read_text(encoding='utf-8-sig')
    try:
        dialect = csv.Sniffer().sniff(text[:8192], delimiters=',;\t')
    except csv.Error:
        dialect = csv.excel
    rows = []
    for line, r in enumerate(csv.reader(text.splitlines(), dialect), 1):
        if not r or all(not x.strip() for x in r):
            continue
        if len(r) < 2:
            raise ValueError(f'Row {line}: expected two columns')
        try:
            vals = []
            for cell in r[:2]:
                cell = cell.strip().removesuffix('%').strip()
                if dialect.delimiter != ',':
                    cell = cell.replace(',', '.')
                vals.append(float(cell))
            x,y = vals
        except ValueError:
            if not rows:
                continue
            raise ValueError(f'Row {line}: invalid number') from None
        if not all(math.isfinite(v) and v >= 0 for v in (x,y)):
            raise ValueError(f'Row {line}: values must be finite and nonnegative')
        if rows and x <= rows[-1][0]:
            raise ValueError(f'Row {line}: positions must be strictly increasing')
        rows.append((x,y))
    if len(rows) < 2:
        raise ValueError('At least two numeric observations are needed')
    return rows


def value_at(rows, t):
    if t < rows[0][0] or t > rows[-1][0]:
        return None
    for (a, ya), (b, yb) in zip(rows, rows[1:]):
        if a <= t <= b:
            return ya + (yb-ya)*(t-a)/(b-a)
    return rows[-1][1]


def analyze(rows, axis, duration=None, values='percent'):
    if axis != 'seconds' and (duration is None or not math.isfinite(duration) or duration <= 0):
        raise ValueError('--duration is required and positive for percent/fraction positions')
    if duration is not None and (not math.isfinite(duration) or duration <= 0):
        raise ValueError('--duration must be finite and positive')
    divisor = {'seconds':1, 'percent':100, 'fraction':1}[axis]
    limit = {'percent':100, 'fraction':1}.get(axis)
    if limit is not None and any(x > limit for x,_ in rows):
        raise ValueError('Position exceeds the selected axis range')
    points = [(x if axis == 'seconds' else x/divisor*duration, y*(100 if values == 'fraction' else 1)) for x,y in rows]
    if duration is not None and points[-1][0] > duration+1e-6:
        raise ValueError('Position exceeds video duration')
    end = min(30, points[-1][0])
    hook_y = value_at(points, end)
    hook_loss = points[0][1]-hook_y if points[0][0] == 0 and hook_y is not None else None
    cliffs = []
    for (a,ya),(b,yb) in zip(points,points[1:]):
        if ya-yb > 0.8:
            cliffs.append({'from_seconds':a,'to_seconds':b,'lost_pp':round(ya-yb,4),'rate_pp_per_second':round((ya-yb)/(b-a),6)})
    cliffs.sort(key=lambda c: -c['rate_pp_per_second'])
    y30 = value_at(points,30)
    slide = (y30-points[-1][1])/(points[-1][0]-30) if y30 is not None and points[-1][0] > 30 else None
    return {'points':len(points),'axis':axis,'values':values,'observation_start_seconds':points[0][0],
            'observation_end_seconds':points[-1][0],'start':points[0][1],'end':points[-1][1],
            'hook_interval_end_seconds':end,'hook_loss_pp':round(hook_loss,4) if hook_loss is not None else None,
            'cliffs':cliffs[:5],'middle_net_loss_pp_per_second':round(slide,6) if slide is not None else None,
            'interpretation':'Descriptive sampled changes, not evidence of a cause or a universal quality threshold.'}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('csv')
    ap.add_argument('--axis',choices=['seconds','percent','fraction'],required=True)
    ap.add_argument('--values',choices=['percent','fraction'],default='percent')
    ap.add_argument('--duration',type=float)
    ap.add_argument('--transcript')
    ap.add_argument('--json',action='store_true')
    args=ap.parse_args()
    try:
        out=analyze(load_csv(args.csv),args.axis,args.duration,args.values)
        if args.transcript:
            sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'yt-edit'))
            from deadair import load
            cues=load(args.transcript)
            for c in out['cliffs']:
                c['transcript_near_drop']=' '.join(t for a,b,t in cues if a <= c['to_seconds']+4 and b >= c['from_seconds']-4)[:240]
    except (ValueError,OSError) as exc:
        ap.error(str(exc))
    print(json.dumps(out,ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
