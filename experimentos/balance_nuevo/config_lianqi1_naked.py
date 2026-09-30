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
    "qi_max": P(31, "PROVISIONAL", "ETAPA16_QI31_VALIDACION_FINAL_2026-09-29.md",
                "Qi31 es la frontera mínima que iguala ofensiva pura y apertura defensiva coste7/6."),
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
        DICE_CANDIDATES_LAB[cfg["nominal_damage"]]["narrow"],
        "PROVISIONAL",
        "LAB_PERFILES_ENEMIGO_LIANQI_I_PHASE_A_2026-09-29.md",
        f"Distribución narrow promovida para PHASE A; media objetivo={cfg['nominal_damage']}.",
    )
    for tech_id, cfg in BASE_OFFENSIVE.items()
}

BASIC_ATTACK_SELECTION = P(
    "1d4+4",
    "PROVISIONAL",
    "LAB_GOLPE_SIMPLE_LIANQI_I_NAKED_2026-09-29.md",
    "Ataque básico de coste 0 Qi promovido para PHASE A; media 6.5, rango 5-8.",
)


LIANQI_I_REFERENCE_ENEMY = {
    "hp_max": P(None, "PENDIENTE", "checkpoint LianQi I NAKED",
                "Necesario para TTK; debe nacer del sistema nuevo."),
    "qi_max": P(None, "PENDIENTE", "checkpoint LianQi I NAKED",
                "Sólo necesario si el perfil usa técnicas/costes de Qi."),
    "precision": P(None, "PENDIENTE", "HANDOFF_BALANCE_NUEVO_SISTEMA_2026-09-29.md",
                   "Precisión enemiga nueva de Etapa I."),
    "evasion": P(20.0, "PROVISIONAL", "LAB_PERFILES_ENEMIGO_LIANQI_I_PHASE_A_2026-09-29.md",
                 "Perfil ordinario de referencia PHASE A; no representa a todos los enemigos."),
    "defense": P(2.0, "PROVISIONAL", "LAB_PERFILES_ENEMIGO_LIANQI_I_PHASE_A_2026-09-29.md",
                 "Perfil ordinario de referencia PHASE A; DEF 4 queda como stress resistente."),
    "control": P(None, "PENDIENTE", "checkpoint LianQi I NAKED",
                 "Sólo si el enemigo intenta Control."),
    "tenacity": P(20.0, "PROVISIONAL", "LAB_LIANQI_I_CONTROL_TENACIDAD_ARRASTRE_2026-09-29.md",
                  "Referencia ordinaria LianQi I para benchmark de Control; no universal para todos los enemigos."),
    "crit_chance": P(5.0, "CANON", "CONTRATO_COMBATE_ESTADISTICAS_DOT_V0_1.md §5",
                     "Base universal salvo override explícito."),
    "crit_damage": P(1.50, "CANON", "CONTRATO_COMBATE_ESTADISTICAS_DOT_V0_1.md §5",
                     "Base universal salvo override explícito."),
    "damage_model": P(None, "PENDIENTE", "HANDOFF_BALANCE_NUEVO_SISTEMA_2026-09-29.md",
                      "Distribución nueva de daño recibido por acción."),
}


ARRASTRE_BASE_CONTROL = P(
    65.0, "PROVISIONAL",
    "LAB_LIANQI_I_CONTROL_TENACIDAD_ARRASTRE_2026-09-29.md",
    "Con Agua principal (+5 Control) vs Tenacidad ordinaria 20 produce 50% efectivo; sujeto a rebenchmark.",
)


def pending_parameters(group: dict[str, Parameter]) -> list[str]:
    return [name for name, param in group.items() if not param.ready]
