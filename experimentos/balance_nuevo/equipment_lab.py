"""Modelo de disponibilidad y estadísticas de equipo para Arco 1.

Las identidades/fuentes actuales pueden auditarse desde el runtime histórico,
pero sus estadísticas legacy NO se importan. Cada objeto rediseñado deberá
declarar sus stats nuevas y etapa mínima de obtención.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Mapping, Iterable


STAGE_ORDER = {
    "LianQi_I": 1,
    "LianQi_II": 2,
    "LianQi_III": 3,
    "LianQi_IV": 4,
}


@dataclass(frozen=True)
class EquipmentItem:
    item_id: str
    name: str
    slot: str
    provenance: str  # CANON | PROVISIONAL | LAB
    min_stage: str | None
    source_type: str
    source_id: str | None = None
    obtainable_now: bool = False
    stats: Mapping[str, float] = field(default_factory=dict)
    notes: str = ""


# AUDITORÍA DE FUENTES ACTUALES.
# Sólo conserva identidad/ubicación, NUNCA stats legacy.
CURRENT_SOURCE_AUDIT = {
    "espada_madera": EquipmentItem(
        "espada_madera", "espada de madera", "mano", "PROVISIONAL",
        "LianQi_I", "STARTING_INVENTORY", obtainable_now=True,
        notes="Se entrega a todos al crear personaje. Stats legacy descartadas."
    ),
    "cuchillo_hueso": EquipmentItem(
        "cuchillo_hueso", "cuchillo de hueso", "mano", "PROVISIONAL",
        "LianQi_I", "ORIGIN_START", "callejero", True,
        notes="Exclusivo del origen callejero en el runtime actual. Stats legacy descartadas."
    ),
    "uniforme": EquipmentItem(
        "uniforme", "uniforme de discípulo externo", "torso", "PROVISIONAL",
        "LianQi_I", "STARTING_INVENTORY", obtainable_now=True,
        notes="Se entrega a todos al crear personaje. Stats legacy descartadas."
    ),
    "anillo": EquipmentItem(
        "anillo", "anillo herrumbroso", "dedo", "PROVISIONAL",
        "LianQi_I", "ROOM_ITEM", "camino", True,
        notes="Está en Camino de la Montaña, dentro del mundo inicialmente accesible."
    ),
    "amuleto_diente": EquipmentItem(
        "amuleto_diente", "amuleto de colmillo", "cuello", "PROVISIONAL",
        "LianQi_I", "MOB_DROP", "lobo_espiritual", True,
        notes="Drop del lobo; al menos una sala/territorio del lobo es inicialmente accesible."
    ),
    "espada_hierro": EquipmentItem(
        "espada_hierro", "espada de hierro", "mano", "PROVISIONAL",
        None, "NO_LIVE_SOURCE", obtainable_now=False,
        notes="Existe como dato, pero CATALOGO está vacío y comercio está pendiente."
    ),
    "tunica_reforzada": EquipmentItem(
        "tunica_reforzada", "túnica reforzada", "torso", "PROVISIONAL",
        None, "NO_LIVE_SOURCE", obtainable_now=False,
        notes="Existe como dato, sin fuente jugable actual."
    ),
    "bandana_cuero": EquipmentItem(
        "bandana_cuero", "bandana de cuero", "cabeza", "PROVISIONAL",
        None, "NO_LIVE_SOURCE", obtainable_now=False,
        notes="Existe como dato, sin fuente jugable actual."
    ),
    "sandalias_viento": EquipmentItem(
        "sandalias_viento", "sandalias de viento", "piernas", "PROVISIONAL",
        None, "NO_LIVE_SOURCE", obtainable_now=False,
        notes="Existe como dato, sin fuente jugable actual."
    ),
    "uniforme_interno": EquipmentItem(
        "uniforme_interno", "uniforme de discípulo interno", "torso", "PROVISIONAL",
        None, "NO_LIVE_SOURCE", obtainable_now=False,
        notes="Existe como dato, sin fuente jugable actual."
    ),
}


def stage_reached(stage: str, min_stage: str | None) -> bool:
    return min_stage is not None and STAGE_ORDER[stage] >= STAGE_ORDER[min_stage]


def available_items(catalog: Iterable[EquipmentItem], stage: str) -> list[EquipmentItem]:
    return [x for x in catalog if x.obtainable_now and stage_reached(stage, x.min_stage)]


def validate_catalog(catalog: Iterable[EquipmentItem]) -> list[str]:
    errors = []
    ids = set()
    for item in catalog:
        if item.item_id in ids:
            errors.append(f"ID duplicado: {item.item_id}")
        ids.add(item.item_id)
        if item.min_stage is not None and item.min_stage not in STAGE_ORDER:
            errors.append(f"{item.item_id}: etapa inválida {item.min_stage}")
    return errors
