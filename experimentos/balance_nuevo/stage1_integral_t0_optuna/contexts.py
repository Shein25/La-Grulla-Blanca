"""Contextos Monte Carlo de Stage1 T0.

NONE es el contexto natural principal. BLOOD_1 permanece declarado como
BLOCKED hasta disponer de contrato autoritativo compatible con el motor nuevo.
"""
from __future__ import annotations

from dataclasses import dataclass

ROOTS=("fuego","metal","agua","tierra","viento")


@dataclass(frozen=True)
class CombatContext:
    context_id: str
    loadout_profile: str
    consumable_arm: str
    player_policy: str
    role: str
    enabled: bool
    reason: str=""


PRIMARY_CONTEXTS=(
    CombatContext(
        "MANDATORY_ENTRY__NONE__VETERAN",
        "MANDATORY_ENTRY","NONE","VETERAN","PRIMARY",True,
    ),
    CombatContext(
        "EXPECTED_STAGE__NONE__VETERAN",
        "EXPECTED_STAGE","NONE","VETERAN","PRIMARY",True,
    ),
)

STRESS_CONTEXTS=(
    CombatContext(
        "HIGH_ROLL_STRESS__NONE__VETERAN",
        "HIGH_ROLL_STRESS","NONE","VETERAN","STRESS",True,
    ),
    CombatContext(
        "MANDATORY_ENTRY__NONE__UNITARGET_FIRST",
        "MANDATORY_ENTRY","NONE","UNITARGET_FIRST","CONTROL",True,
    ),
    CombatContext(
        "EXPECTED_STAGE__NONE__UNITARGET_FIRST",
        "EXPECTED_STAGE","NONE","UNITARGET_FIRST","CONTROL",True,
    ),
)

BLOCKED_CONTEXTS=(
    CombatContext(
        "EXPECTED_STAGE__BLOOD_1__VETERAN",
        "EXPECTED_STAGE","BLOOD_1","VETERAN","PREPARATION_STRESS",False,
        "BLOOD_1 lacks an authoritative new-engine consumable contract",
    ),
)


def expanded_primary_context_ids() -> tuple[str,...]:
    return tuple(
        f"{ctx.context_id}__ROOT_{root.upper()}"
        for ctx in PRIMARY_CONTEXTS
        for root in ROOTS
    )
