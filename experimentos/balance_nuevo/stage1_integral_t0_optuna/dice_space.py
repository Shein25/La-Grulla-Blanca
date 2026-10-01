"""Biblioteca LAB de dados generada por banda de media.

No importa distribuciones de monstruos anteriores. Las opciones se generan
mecánicamente y luego Optuna elige una notación explícita con
suggest_categorical().
"""
from __future__ import annotations

import re


def dice_mean(notation: str) -> float:
    m=re.fullmatch(r"(\d+)d(\d+)(?:\+(\d+))?",notation)
    if not m:
        raise ValueError(f"unsupported Stage1 dice notation: {notation}")
    n=int(m.group(1));sides=int(m.group(2));mod=int(m.group(3) or 0)
    return n*(sides+1)/2+mod


def dice_candidates(low_mean: float,high_mean: float) -> tuple[str,...]:
    if low_mean>high_mean:
        raise ValueError("low_mean > high_mean")
    out=[]
    for n in (1,2):
        for sides in (2,3,4,6):
            for mod in range(0,11):
                notation=f"{n}d{sides}" + (f"+{mod}" if mod else "")
                mean=dice_mean(notation)
                if low_mean<=mean<=high_mean:
                    out.append((mean,n,sides,mod,notation))
    out.sort()
    unique=[]
    seen=set()
    for *_,notation in out:
        if notation not in seen:
            seen.add(notation);unique.append(notation)
    if not unique:
        raise ValueError(f"no dice candidates for mean band {low_mean}..{high_mean}")
    return tuple(unique)
