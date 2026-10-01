"""Contrato multiobjetivo por especie.

Declara QUÉ observará Optuna, no un target de win rate ni una función de
selección final. Las fórmulas se conectarán cuando el agregador de métricas
por ronda esté implementado.
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
        Objective("player_hp_pressure","maximize","amenaza real sin convertirla en esponja"),
        Objective("monster_hp","minimize","preservar cuerpo pequeño"),
        Objective("monster_defense","minimize","evitar tanque artificial"),
        Objective("combat_duration","minimize","amenaza simple e instintiva"),
    ),
    "avispa_jade":(
        Objective("player_hp_pressure","maximize","la picadura debe importar"),
        Objective("monster_dot_fraction","maximize","identidad de veneno"),
        Objective("monster_hp","minimize","movilidad antes que bulk"),
        Objective("monster_defense","minimize","movilidad antes que armadura"),
    ),
    "serpiente_qi":(
        Objective("late_pressure","maximize","alargar el combate debe empeorar la situación"),
        Objective("monster_dot_fraction","maximize","veneno como fuente identitaria"),
        Objective("early_burst","minimize","no convertir presión sostenida en burst"),
        Objective("monster_hp","minimize","evitar resolver identidad sólo con HP"),
    ),
    "mono_pildoras":(
        Objective("player_qi_pressure","maximize","presión sobre Dantian/recursos"),
        Objective("forced_basic_due_to_qi","maximize","el drenaje debe cambiar decisiones"),
        Objective("player_hp_pressure","maximize","sigue siendo amenaza física"),
        Objective("monster_hp","minimize","evitar bruto inflado"),
    ),
    "lobo_espiritual":(
        Objective("player_hp_pressure","maximize","apex/puente de examen"),
        Objective("offensive_tail_risk","maximize","capacidad de castigar errores"),
        Objective("monster_hp","minimize","evitar depender sólo de HP"),
        Objective("monster_defense","minimize","evitar depender sólo de DEF"),
    ),
}


def objective_directions(species_id: str) -> tuple[str,...]:
    try:
        return tuple(x.direction for x in OBJECTIVES_BY_SPECIES[species_id])
    except KeyError as exc:
        raise KeyError(f"unknown Stage1 species: {species_id}") from exc
