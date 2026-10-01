"""Bandas LAB para la futura búsqueda Optuna T0.

No son stats finales ni baseline canónico. Todas las mecánicas activas se
resolverán simultáneamente cuando el runner integral exista.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

Provenance = Literal["LAB_SEARCH_RANGE", "FIXED_IDENTITY", "UNRESOLVED"]


@dataclass(frozen=True)
class NumericRange:
    low: float
    high: float
    step: float = 1.0
    provenance: Provenance = "LAB_SEARCH_RANGE"
    rationale: str = ""


@dataclass(frozen=True)
class MeanDamageRange:
    low: float
    high: float
    provenance: Provenance = "LAB_SEARCH_RANGE"
    rationale: str = (
        "La futura capa de dados debe mapear esta banda a notaciones explícitas; "
        "no se permiten floats de daño ocultos en el resolver."
    )


@dataclass(frozen=True)
class SpeciesSearchSpace:
    free: dict
    fixed: dict
    unresolved: dict
    identity: str


COMMON_FIXED = {
    "control": 0.0,
    "crit_chance": 5.0,
    "crit_damage": 1.50,
    "tier": "T0",
    "definitives": False,
}

LIANQI_I_T0_SEARCH_SPACES = {
    "rata_qi": SpeciesSearchSpace(
        free={
            "hp": NumericRange(8, 22),
            "defense": NumericRange(0, 2),
            "evasion": NumericRange(0, 20),
            "tenacity": NumericRange(0, 20),
            "precision": NumericRange(80, 105),
            "basic_damage_mean": MeanDamageRange(3.5, 7.0),
        },
        fixed={
            **COMMON_FIXED,
            "technique": None,
            "cognition": "INSTINTIVO",
            "social": "COLONIA",
        },
        unresolved={"qi_max": "semantic decision required before canonical READY"},
        identity="amenaza sobrenatural más baja; sencilla e instintiva; sin técnica T0 inventada",
    ),
    "avispa_jade": SpeciesSearchSpace(
        free={
            "hp": NumericRange(7, 20),
            "defense": NumericRange(0, 2),
            "evasion": NumericRange(20, 55),
            "tenacity": NumericRange(0, 25),
            "precision": NumericRange(85, 110),
            "basic_damage_mean": MeanDamageRange(2.5, 6.0),
            "poison_damage_per_tick_mean": MeanDamageRange(1.0, 4.0),
            "poison_ticks": NumericRange(2, 4),
            "technique_cadence": NumericRange(2, 4),
        },
        fixed={
            **COMMON_FIXED,
            "technique_mechanics": ("POISON_DOT",),
            "cognition": "INSTINTIVO",
            "social": "COLONIA",
        },
        unresolved={"qi_max": "semantic decision required before canonical READY"},
        identity="movilidad/evasión + picadura + veneno; no convertirla en tanque",
    ),
    "serpiente_qi": SpeciesSearchSpace(
        free={
            "hp": NumericRange(12, 30),
            "defense": NumericRange(0, 3),
            "evasion": NumericRange(5, 30),
            "tenacity": NumericRange(5, 35),
            "precision": NumericRange(85, 110),
            "basic_damage_mean": MeanDamageRange(3.5, 7.0),
            "poison_damage_per_tick_mean": MeanDamageRange(2.0, 6.0),
            "poison_ticks": NumericRange(3, 5),
            "technique_cadence": NumericRange(2, 4),
        },
        fixed={
            **COMMON_FIXED,
            "technique_mechanics": ("POISON_DOT",),
            "cognition": "REACTIVO_1",
            "social": "SOLITARIO",
        },
        unresolved={"qi_max": "semantic decision required before canonical READY"},
        identity="presión sostenida por veneno; prolongar el combate debe ser peligroso",
    ),
    "mono_pildoras": SpeciesSearchSpace(
        free={
            "hp": NumericRange(14, 34),
            "defense": NumericRange(0, 3),
            "evasion": NumericRange(15, 45),
            "tenacity": NumericRange(10, 40),
            "precision": NumericRange(90, 115),
            "basic_damage_mean": MeanDamageRange(4.5, 8.0),
            "technique_direct_damage_mean": MeanDamageRange(4.5, 9.0),
            "qi_drain": NumericRange(1, 8),
            "technique_cadence": NumericRange(2, 4),
        },
        fixed={
            **COMMON_FIXED,
            "technique_mechanics": ("DIRECT_DAMAGE", "QI_DRAIN"),
            "cognition": "CAZADOR_2",
            "social": "OPORTUNISTA",
        },
        unresolved={"qi_max": "semantic decision required before canonical READY"},
        identity="presión sobre Qi/Dantian y oportunismo; no balancear como bruto de daño",
    ),
    "lobo_espiritual": SpeciesSearchSpace(
        free={
            "hp": NumericRange(24, 60),
            "defense": NumericRange(1, 5),
            "evasion": NumericRange(10, 35),
            "tenacity": NumericRange(20, 55),
            "precision": NumericRange(95, 120),
            "basic_damage_mean": MeanDamageRange(6.5, 11.0),
            "technique_direct_damage_mean": MeanDamageRange(8.0, 14.0),
            "technique_cadence": NumericRange(2, 5),
        },
        fixed={
            **COMMON_FIXED,
            "technique_mechanics": ("DIRECT_DAMAGE",),
            "cognition": "CAZADOR_2",
            "social": "MANADA",
        },
        unresolved={"qi_max": "semantic decision required before canonical READY"},
        identity="APEX_BRIDGE; enfrentarlo puede ser una mala decisión aunque aparezca",
    ),
}
