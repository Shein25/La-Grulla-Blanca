"""Conversión de métricas agregadas a objetivos Optuna.

Rata es la primera especie ejecutable. Las otras permanecen bloqueadas hasta
que su métrica identitaria específica esté instrumentada y validada.
"""
from __future__ import annotations


class ObjectiveNotReady(RuntimeError):
    pass


def objective_values(species_id: str,candidate,aggregate: dict) -> tuple[float,...]:
    if species_id=="rata_qi":
        return (
            1.0-float(aggregate["hp_final_pct_mean"]),
            float(candidate.stats["hp"]),
            float(candidate.stats["defense"]),
            float(aggregate["rounds_mean"]),
        )
    raise ObjectiveNotReady(
        f"{species_id}: identity-specific objective metrics are not executable yet"
    )
