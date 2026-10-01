"""Contrato multiobjetivo por especie para Stage1 T0."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Objective:
    name: str
    direction: str
    rationale: str

OBJECTIVES_BY_SPECIES={
    "rata_qi":(
        Objective("player_hp_pressure","maximize","desgaste natural"),
        Objective("normalized_candidate_budget","minimize","evitar inflación estadística"),
    ),
    "avispa_jade":(
        Objective("player_hp_pressure","maximize","la picadura debe importar"),
        Objective("monster_dot_fraction","maximize","veneno como identidad"),
        Objective("normalized_candidate_budget","minimize","movilidad/veneno antes que bulk"),
    ),
    "serpiente_qi":(
        Objective("monster_dot_damage_mean","maximize","presión sostenida real por veneno"),
        Objective("monster_dot_fraction","maximize","el veneno debe explicar parte relevante del daño"),
        Objective("normalized_candidate_budget","minimize","evitar resolver identidad con inflación general"),
    ),
    "mono_pildoras":(
        Objective("qi_drained_mean","maximize","presión sobre Dantian/recursos"),
        Objective("forced_basic_due_to_qi_mean","maximize","el drenaje debe cambiar decisiones"),
        Objective("player_hp_pressure","maximize","seguir siendo amenaza física"),
        Objective("normalized_candidate_budget","minimize","evitar bruto inflado"),
    ),
    "lobo_espiritual":(
        Objective("player_hp_pressure","maximize","amenaza apex/bridge"),
        Objective("monster_damage_total_p90","maximize","cola ofensiva capaz de castigar errores"),
        Objective("normalized_candidate_budget","minimize","evitar depender sólo de stats infladas"),
    ),
}

def objective_directions(species_id: str) -> tuple[str,...]:
    try:
        return tuple(x.direction for x in OBJECTIVES_BY_SPECIES[species_id])
    except KeyError as exc:
        raise KeyError(f"unknown Stage1 species: {species_id}") from exc
