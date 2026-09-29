"""Variantes de progresión para probar ascensos de LianQi.

El contrato actual usa RESOURCES_ONLY como control conceptual, pero este módulo
permite experimentar con otras recompensas de etapa SIN volverlas canon.

Nunca contiene valores heredados de ver74.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict, replace
from typing import Dict, Iterable, Mapping

from sim_core import ActorStats


@dataclass(frozen=True)
class StageGrant:
    hp_max: float = 0.0
    qi_max: float = 0.0
    precision: float = 0.0
    evasion: float = 0.0
    defense: float = 0.0
    percent_penetration: float = 0.0
    flat_penetration: float = 0.0
    crit_chance: float = 0.0
    crit_damage: float = 0.0
    control: float = 0.0
    tenacity: float = 0.0
    damage_done_percent: float = 0.0


@dataclass(frozen=True)
class ProgressionPolicy:
    name: str
    provenance: str  # CANON | PROVISIONAL | LAB
    grants: Mapping[str, StageGrant]
    notes: str = ""


STAGES = ("LianQi_I", "LianQi_II", "LianQi_III", "LianQi_IV")


def cumulative_grant(policy: ProgressionPolicy, stage: str) -> StageGrant:
    if stage not in STAGES:
        raise ValueError(f"Etapa desconocida: {stage}")
    totals = {k: 0.0 for k in StageGrant.__dataclass_fields__}
    for s in STAGES[: STAGES.index(stage) + 1]:
        g = policy.grants.get(s, StageGrant())
        for k, v in asdict(g).items():
            totals[k] += v
    return StageGrant(**totals)


def apply_grant(base: ActorStats, grant: StageGrant) -> ActorStats:
    return replace(
        base,
        hp_max=base.hp_max + grant.hp_max,
        qi_max=base.qi_max + grant.qi_max,
        precision=base.precision + grant.precision,
        evasion=base.evasion + grant.evasion,
        defense=base.defense + grant.defense,
        percent_penetration=base.percent_penetration + grant.percent_penetration,
        flat_penetration=base.flat_penetration + grant.flat_penetration,
        crit_chance=base.crit_chance + grant.crit_chance,
        crit_damage=base.crit_damage + grant.crit_damage,
        control=base.control + grant.control,
        tenacity=base.tenacity + grant.tenacity,
        damage_done_percent=base.damage_done_percent + grant.damage_done_percent,
    )


# CONTROL: refleja la dirección hoy cerrada del contrato (sólo recursos/acceso).
# HP/Qi siguen en cero hasta que se definan sus incrementos nuevos.
RESOURCES_ONLY = ProgressionPolicy(
    name="resources_only",
    provenance="PROVISIONAL",
    grants={s: StageGrant() for s in STAGES},
    notes="Control: sólo HP/Qi/acceso cuando sus valores sean definidos; sin stats de combate automáticos.",
)


# Barridos LAB: no prescriben una política, generan candidatos comparables.
EXTRA_STAT_SWEEPS = {
    # incrementos POR ASCENSO II/III/IV
    "precision_per_stage": (0.0, 2.0, 5.0),
    "evasion_per_stage": (0.0, 2.0, 5.0),
    "defense_per_stage": (0.0, 0.5, 1.0),
    "crit_chance_per_stage": (0.0, 1.0, 2.0),
    "crit_damage_per_stage": (0.0, 0.025, 0.05),
    "control_per_stage": (0.0, 2.0, 5.0),
    "tenacity_per_stage": (0.0, 2.0, 5.0),
    "damage_done_percent_per_stage": (0.0, 2.5, 5.0),
}


def uniform_extra_policy(
    *,
    name: str,
    hp_per_stage: float = 0.0,
    qi_per_stage: float = 0.0,
    precision_per_stage: float = 0.0,
    evasion_per_stage: float = 0.0,
    defense_per_stage: float = 0.0,
    crit_chance_per_stage: float = 0.0,
    crit_damage_per_stage: float = 0.0,
    control_per_stage: float = 0.0,
    tenacity_per_stage: float = 0.0,
    damage_done_percent_per_stage: float = 0.0,
) -> ProgressionPolicy:
    """Crea una política LAB que aplica el mismo premio en cada ascenso II/III/IV."""
    step = StageGrant(
        hp_max=hp_per_stage,
        qi_max=qi_per_stage,
        precision=precision_per_stage,
        evasion=evasion_per_stage,
        defense=defense_per_stage,
        crit_chance=crit_chance_per_stage,
        crit_damage=crit_damage_per_stage,
        control=control_per_stage,
        tenacity=tenacity_per_stage,
        damage_done_percent=damage_done_percent_per_stage,
    )
    return ProgressionPolicy(
        name=name,
        provenance="LAB",
        grants={
            "LianQi_I": StageGrant(),
            "LianQi_II": step,
            "LianQi_III": step,
            "LianQi_IV": step,
        },
        notes="Candidato de sensibilidad. No convertir en canon por existir aquí.",
    )


def policy_signature(policy: ProgressionPolicy, stage: str) -> dict:
    return {
        "policy": policy.name,
        "provenance": policy.provenance,
        "stage": stage,
        **asdict(cumulative_grant(policy, stage)),
    }
