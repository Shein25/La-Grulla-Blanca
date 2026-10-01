"""Selección geométrica de representantes del frente Pareto.

No rankea ni elige un ganador. Sólo toma puntos distribuidos a lo largo de la
curva para pruebas de robustez posteriores.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _norm(v,lo,hi):
    return 0.0 if hi<=lo else (float(v)-float(lo))/(float(hi)-float(lo))


def select_coverage(front: list[dict],count: int) -> list[dict]:
    if count<2:
        raise ValueError("coverage count must be >= 2")
    if len(front)<count:
        raise ValueError("front smaller than requested coverage count")

    ordered=sorted(front,key=lambda x:(float(x["values"][1]),-float(x["values"][0])))
    pressures=[float(x["values"][0]) for x in ordered]
    budgets=[float(x["values"][1]) for x in ordered]
    pmin,pmax=min(pressures),max(pressures)
    bmin,bmax=min(budgets),max(budgets)

    coords=[
        (_norm(float(x["values"][1]),bmin,bmax),_norm(float(x["values"][0]),pmin,pmax))
        for x in ordered
    ]
    cumulative=[0.0]
    for (x0,y0),(x1,y1) in zip(coords,coords[1:]):
        cumulative.append(cumulative[-1]+math.hypot(x1-x0,y1-y0))
    total=cumulative[-1]
    if total<=0:
        raise ValueError("degenerate Pareto geometry")

    fractions=[i/(count-1) for i in range(count)]
    chosen=[]
    used=set()
    for frac in fractions:
        target=frac*total
        candidates=sorted(
            range(len(ordered)),
            key=lambda i:(abs(cumulative[i]-target),i),
        )
        idx=next(i for i in candidates if i not in used)
        used.add(idx)
        row=dict(ordered[idx])
        row["coverage_fraction"]=frac
        row["coverage_arc_position"]=cumulative[idx]/total
        chosen.append(row)
    return chosen


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--source",required=True)
    ap.add_argument("--out",required=True)
    ap.add_argument("--count",type=int,default=5)
    args=ap.parse_args()

    front=load_json(args.source)
    selected=select_coverage(front,args.count)
    Path(args.out).write_text(
        json.dumps(selected,ensure_ascii=False,indent=2,sort_keys=True)+"\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "status":"COVERAGE_REPRESENTATIVES_NOT_RANKED",
        "source_candidates":len(front),
        "selected_representatives":len(selected),
        "numbers":[x["number"] for x in selected],
        "coverage_fractions":[x["coverage_fraction"] for x in selected],
        "selection_is_canonical":False,
    },ensure_ascii=False,indent=2))


if __name__=="__main__":
    main()
