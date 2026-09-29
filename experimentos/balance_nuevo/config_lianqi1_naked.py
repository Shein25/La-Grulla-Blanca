"""Configuración estricta para el benchmark LianQi I NAKED.

Impide que una simulación seria complete parámetros ausentes con defaults
silenciosos o cifras legacy.

NAKED = cultivo + raíz principal + técnica, sin equipo, injerto, Concordancias,
consumibles ni Tramos I-III.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from config_arc1_provisional import BASE_OFFENSIVE, DICE_CANDIDATES_LAB


VALID_PROVENANCE = {"CANON", "PROVISIONAL", "LAB", "PENDIENTE"}


@dataclass(frozen=True)
class Parameter:
    value: Any | None
    provenance: str
    source: str
    note: str = ""

    def __post_init__(self) -> None:
        if self.provenance not in VALID_PROVENANCE:
            raise ValueError(f"Procedencia inválida: {self.provenance}")

    @property
    def ready(self) -> bool:
        return self.provenance != "PENDIENTE" and self.value is not None


def P(value: Any | None, provenance: str, source: str, note: str = "") -> Parameter:
    return Parameter(value=value, provenance=provenance, source=source, note=note)


PLAYER_BASE = {
    "hp_max": P(None, "PENDIENTE", "HANDOFF_BALANCE_NUEVO_SISTEMA_2026-09-29.md",
                "HP inicial nuevo de LianQi I no cerrado."),
    "qi_max": P(None, "PENDIENTE", "HANDOFF_BALANCE_NUEVO_SISTEMA_2026-09-29.md",
                "Qi máximo inicial nuevo de LianQi I no cerrado."),
    "precision": P(100.0, "CANON", "CONTRATO_COMBATE_ESTADISTICAS_DOT_V0_1.md §3",
                   "Precisión normal de referencia."),
    "evasion": P(None, "PENDIENTE", "COLAB_BALANCE_NUEVO.ipynb §1",
                 "No asumir 0: el notebook serio la deja sin cerrar."),
    "defense": P(None, "PENDIENTE", "COLAB_BALANCE_NUEVO.ipynb §1",
                 "DEF base desnuda pendiente."),
    "control": P(None, "PENDIENTE", "COLAB_BALANCE_NUEVO.ipynb §1",
                 "Control base no-root pendiente."),
    "tenacity": P(None, "PENDIENTE", "COLAB_BALANCE_NUEVO.ipynb §1",
                  "Tenacidad base no-root pendiente."),
    "crit_chance": P(5.0, "CANON", "CONTRATO_COMBATE_ESTADISTICAS_DOT_V0_1.md §5",
                     "Probabilidad crítica base."),
    "crit_damage": P(1.50, "CANON", "CONTRATO_COMBATE_ESTADISTICAS_DOT_V0_1.md §5",
                     "Multiplicador crítico base."),
    "percent_penetration": P(0.0, "CANON", "NAKED + contrato de progresión §25",
                             "Sin fuente desnuda adicional; raíz/técnica pueden añadirla."),
    "flat_penetration": P(0.0, "CANON", "NAKED + contrato de progresión §25",
                          "Sin fuente desnuda adicional."),
    "damage_done_percent": P(0.0, "CANON", "NAKED + contrato de progresión §25",
                             "Sin fuente desnuda adicional; Fuego añade su rasgo."),
}


QI_COST_FLOOR = P(
    None, "PENDIENTE",
    "CONTRATO_COMBATE_ESTADISTICAS_DOT_V0_1.md §25 / Motor §38.23",
    "Piso global exacto de coste de Qi pendiente de benchmark.",
)


ROOT_TO_INITIAL_TECHNIQUE = {
    "fuego": "palma_ardiente",
    "metal": "destello_plata",
    "agua": "latigazo_marea",
    "tierra": "golpe_montana",
    "viento": "lanza_nubes",
}


DAMAGE_MODEL_SELECTION = {
    tech_id: P(
        None,
        "PENDIENTE",
        "config_arc1_provisional.py::DICE_CANDIDATES_LAB",
        f"Elegir distribución nueva; media objetivo provisional={cfg['nominal_damage']}. "
        f"Candidatos LAB={DICE_CANDIDATES_LAB[cfg['nominal_damage']]}",
    )
    for tech_id, cfg in BASE_OFFENSIVE.items()
}


LIANQI_I_REFERENCE_ENEMY = {
    "hp_max": P(None, "PENDIENTE", "checkpoint LianQi I NAKED",
                "Necesario para TTK; debe nacer del sistema nuevo."),
    "qi_max": P(None, "PENDIENTE", "checkpoint LianQi I NAKED",
                "Sólo necesario si el perfil usa técnicas/costes de Qi."),
    "precision": P(None, "PENDIENTE", "HANDOFF_BALANCE_NUEVO_SISTEMA_2026-09-29.md",
                   "Precisión enemiga nueva de Etapa I."),
    "evasion": P(None, "PENDIENTE", "HANDOFF_BALANCE_NUEVO_SISTEMA_2026-09-29.md",
                 "Evasión enemiga nueva de Etapa I."),
    "defense": P(None, "PENDIENTE", "HANDOFF_BALANCE_NUEVO_SISTEMA_2026-09-29.md",
                 "DEF enemiga nueva de Etapa I."),
    "control": P(None, "PENDIENTE", "checkpoint LianQi I NAKED",
                 "Sólo si el enemigo intenta Control."),
    "tenacity": P(None, "PENDIENTE", "HANDOFF_BALANCE_NUEVO_SISTEMA_2026-09-29.md",
                  "Tenacidad enemiga nueva de Etapa I."),
    "crit_chance": P(5.0, "CANON", "CONTRATO_COMBATE_ESTADISTICAS_DOT_V0_1.md §5",
                     "Base universal salvo override explícito."),
    "crit_damage": P(1.50, "CANON", "CONTRATO_COMBATE_ESTADISTICAS_DOT_V0_1.md §5",
                     "Base universal salvo override explícito."),
    "damage_model": P(None, "PENDIENTE", "HANDOFF_BALANCE_NUEVO_SISTEMA_2026-09-29.md",
                      "Distribución nueva de daño recibido por acción."),
}


ARRASTRE_BASE_CONTROL = P(
    None, "PENDIENTE",
    "HANDOFF_BALANCE_NUEVO_SISTEMA_2026-09-29.md",
    "Latigazo no puede valorarse completo sin potencia base de Arrastre.",
)


def pending_parameters(group: dict[str, Parameter]) -> list[str]:
    return [name for name, param in group.items() if not param.ready]
