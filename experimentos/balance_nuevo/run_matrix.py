"""Runner declarativo para matrices de balance.

Mantiene escenarios/datos separados del motor. No contiene valores legacy.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable
import csv

from sim_core import ActorStats, Technique, monte_carlo_hit, as_dict


@dataclass(frozen=True)
class Scenario:
    id: str
    provenance: str  # CANON | PROVISIONAL | LAB
    attacker: ActorStats
    target: ActorStats
    technique: Technique
    target_count: int = 1
    iterations: int = 100_000
    seed: int = 20260929


def run_scenario(s: Scenario) -> dict:
    out = as_dict(monte_carlo_hit(
        attacker=s.attacker,
        target=s.target,
        technique=s.technique,
        iterations=s.iterations,
        seed=s.seed,
        target_count=s.target_count,
    ))
    return {
        "scenario_id": s.id,
        "provenance": s.provenance,
        "technique": s.technique.name,
        "target_count": s.target_count,
        **out,
    }


def run_matrix(scenarios: Iterable[Scenario]) -> list[dict]:
    return [run_scenario(s) for s in scenarios]


def export_csv(rows: list[dict], path: str) -> None:
    if not rows:
        raise ValueError("No hay filas para exportar")
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
