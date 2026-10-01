"""Contrato multiobjetivo por especie.

Declara QUÉ observará Optuna, no un target de win rate ni una función de
selección final.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Objective:
    name: str
    direction: str
    rationale: str


OBJECTIVES_BY_SPECIES={
    "rata_qi":(
        Objective(
            "player_hp_pressure","maximize",
            "observar cuánta presión natural produce la criatura"
        ),
        Objective(
            "normalized_candidate_budget","minimize",
            "crear un Pareto presión/potencia sin empujar todas las stats al máximo"
        ),
    ),
    "avispa_jade":(
        Objective("player_hp_pressure","maximize","la picadura debe importar"),
        Objective("monster_dot_fraction","maximize","identidad de veneno"),
        Objective("normalized_candidate_budget","minimize","movilidad/veneno antes que inflación general"),
    ),
    "serpiente_qi":(
        Objective("late_pressure","maximize","alargar el combate debe empeorar la situación"),
        Objective("monster_dot_fraction","maximize","veneno como fuente identitaria"),
        Objective("normalized_candidate_budget","minimize","evitar resolver identidad con inflación general"),
    ),
    "mono_pildoras":(
        Objective("player_qi_pressure","maximize","presión sobre Dantian/recursos"),
        Objective("forced_basic_due_to_qi","maximize","el drenaje debe cambiar decisiones"),
        Objective("normalized_candidate_budget","minimize","evitar bruto inflado"),
    ),
    "lobo_espiritual":(
        Objective("player_hp_pressure","maximize","apex/puente de examen"),
        Objective("offensive_tail_risk","maximize","capacidad de castigar errores"),
        Objective("normalized_candidate_budget","minimize","evitar depender sólo de stats infladas"),
    ),
}


def objective_directions(species_id: str) -> tuple[str,...]:
    try:
        return tuple(x.direction for x in OBJECTIVES_BY_SPECIES[species_id])
    except KeyError as exc:
        raise KeyError(f"unknown Stage1 species: {species_id}") from exc
