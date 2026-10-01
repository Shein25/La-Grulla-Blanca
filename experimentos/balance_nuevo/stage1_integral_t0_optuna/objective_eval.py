"""Conversión de métricas agregadas a objetivos Optuna.

Rata es la primera especie ejecutable. Las otras permanecen bloqueadas hasta
que su métrica identitaria específica esté instrumentada y validada.
"""
from __future__ import annotations

from dice_space import dice_mean
from search_space import LIANQI_I_T0_SEARCH_SPACES


class ObjectiveNotReady(RuntimeError):
    pass


def _normalized(value: float,low: float,high: float) -> float:
    if high<=low:
        return 0.0
    return max(0.0,min(1.0,(float(value)-float(low))/(float(high)-float(low))))


def normalized_candidate_budget(candidate) -> float:
    space=LIANQI_I_T0_SEARCH_SPACES[candidate.species_id]
    vals={
        "hp":float(candidate.stats["hp"]),
        "defense":float(candidate.stats["defense"]),
        "evasion":float(candidate.stats["evasion"]),
        "tenacity":float(candidate.stats["tenacity"]),
        "precision":float(candidate.stats["precision"]),
        "basic_damage_mean":dice_mean(candidate.stats["basic_damage"]),
    }
    parts=[]
    for key,value in vals.items():
        spec=space.free[key]
        parts.append(_normalized(value,spec.low,spec.high))
    return sum(parts)/len(parts)


def objective_values(species_id: str,candidate,aggregate: dict) -> tuple[float,...]:
    if species_id=="rata_qi":
        return (
            1.0-float(aggregate["hp_final_pct_mean"]),
            normalized_candidate_budget(candidate),
        )
    raise ObjectiveNotReady(
        f"{species_id}: identity-specific objective metrics are not executable yet"
    )
