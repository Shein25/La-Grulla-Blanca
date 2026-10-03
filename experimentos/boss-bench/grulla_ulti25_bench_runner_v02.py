#!/usr/bin/env python3
"""
GRULLA_ULTI25_BENCH_RUNNER_V0_2

Scaffold pareado para Grulla F1->F2->F3 con equipo LIV aprobado.
Técnicas normales: DESHABILITADAS.
Consumibles: DESHABILITADOS.

Estado: LAB / NO CANON / NO MAIN / NO MERGE / NO PUSH
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from hashlib import sha256
from typing import Any, Iterable
import json


class Window(str, Enum):
    F1_EARLY = "F1_EARLY"
    F2_ENTRY = "F2_ENTRY"
    F3_ENTRY = "F3_ENTRY"
    PREPARED_OPPORTUNITY = "PREPARED_OPPORTUNITY"


class PlayerState(str, Enum):
    FULL = "FULL"
    BALANCED = "BALANCED"
    DISADVANTAGE = "DISADVANTAGE"
    NEAR_DEATH = "NEAR_DEATH"


class EquipmentProfile(str, Enum):
    MANDATORY_ENTRY = "MANDATORY_ENTRY"
    EXPECTED_STAGE = "EXPECTED_STAGE"
    HIGH_ROLL_STRESS = "HIGH_ROLL_STRESS"


PRIMARY_EQUIPMENT_PROFILES = tuple(x.value for x in EquipmentProfile)
CONTROL_EQUIPMENT_PROFILE = "NAKED"
NORMAL_TECHNIQUES_ENABLED = False
CONSUMABLES_ENABLED = False
ENCOUNTER_STAGE = "LianQi_IV"

ULTIMATES_25 = (
    "Renacer del Sol Carmesí",
    "Corazón de la Montaña Ardiente",
    "Aguja del Crisol Rojo",
    "Loto de Vapor Concordante 1.1",
    "Brasa del Vendaval 0.4",
    "Sentencia del Filo Celestial",
    "Forja de la Espada Carmesí",
    "Espejo del Acero Fluido",
    "Mandato de la Montaña de Hierro",
    "Tormenta del Horizonte Partido",
    "Océano Invertido 0.5",
    "Caldera del Sol Sumergido 0.2",
    "Luna de Acero sobre el Lago Inmóvil",
    "Delta de las Diez Mil Corrientes",
    "Dominio del Mar sin Horizonte 0.4",
    "Sepulcro de las Diez Mil Montañas",
    "Trono del Volcán Sepultado 0.2",
    "Ciudadela de la Espada Inamovible 0.2",
    "Presa de los Nueve Mares 1.0",
    "Horizonte de las Montañas Errantes",
    "Danza del Viento sin Huella",
    "Cometa Carmesí de los Nueve Cielos 0.3",
    "Vendaval de las Mil Heridas 0.2",
    "Río Celeste sin Orillas 0.2",
    "Desierto Suspendido de las Mil Dunas 0.2",
)


@dataclass(frozen=True)
class ScenarioKey:
    player_state: str
    equipment_profile: str
    seed_index: int
    ultimate: str | None
    window: str

    @property
    def pair_id(self) -> str:
        return (
            f"{self.player_state}:"
            f"{self.equipment_profile}:"
            f"{self.seed_index:06d}"
        )


@dataclass
class FightResult:
    pair_id: str
    player_state: str
    equipment_profile: str
    ultimate: str | None
    window: str
    win: bool
    death_phase: int | None
    total_player_actions: int
    total_boss_actions: int
    f1_boss_actions: int
    f2_boss_actions: int
    f3_boss_actions: int
    player_hp_end: float
    player_qi_end: float
    f3_skip_attempted: bool
    f3_lethal_preventions: int
    f3_prevented_lethal_damage: float
    f3_max_single_overkill_prevented: float
    f3_first_real_action_resolved: bool
    player_actions_after_gate_release_to_kill: int | None
    ulti_activated: bool
    ulti_activation_failure: str | None
    ulti_climax_reached: bool | None
    telemetry: dict[str, Any]


def master_seed(
    player_state: str,
    equipment_profile: str,
    seed_index: int,
    base_seed: int = 2026100201,
) -> int:
    payload = (
        f"{base_seed}|{player_state}|{equipment_profile}|{seed_index}"
    ).encode("utf-8")
    return int.from_bytes(sha256(payload).digest()[:8], "big")


class RngStreams:
    DOMAINS = (
        "boss_decision",
        "boss_accuracy",
        "boss_crit",
        "player_normal_accuracy",
        "player_normal_crit",
        "control",
        "status",
        "ultimate",
        "equipment_effect",
        "aux_neutral_action",
    )

    def __init__(self, master_seed_value: int):
        self.master_seed = int(master_seed_value)

    def seed_for(self, domain: str, *coords: Any) -> int:
        if domain not in self.DOMAINS:
            raise ValueError(f"RNG domain no autorizado: {domain}")
        payload = "|".join(
            map(str, (self.master_seed, domain, *coords))
        ).encode("utf-8")
        return int.from_bytes(sha256(payload).digest()[:8], "big")


def iter_ulti_scenarios(
    seeds: int,
    *,
    equipment_profiles: tuple[str, ...] = PRIMARY_EQUIPMENT_PROFILES,
) -> Iterable[ScenarioKey]:
    for player_state in PlayerState:
        for equipment_profile in equipment_profiles:
            for seed_index in range(seeds):
                for ultimate in ULTIMATES_25:
                    for window in Window:
                        yield ScenarioKey(
                            player_state=player_state.value,
                            equipment_profile=equipment_profile,
                            seed_index=seed_index,
                            ultimate=ultimate,
                            window=window.value,
                        )


def iter_baselines(
    seeds: int,
    *,
    equipment_profiles: tuple[str, ...] = PRIMARY_EQUIPMENT_PROFILES,
) -> Iterable[ScenarioKey]:
    for player_state in PlayerState:
        for equipment_profile in equipment_profiles:
            for seed_index in range(seeds):
                yield ScenarioKey(
                    player_state=player_state.value,
                    equipment_profile=equipment_profile,
                    seed_index=seed_index,
                    ultimate=None,
                    window="BASELINE_NO_ULTI",
                )


def expected_counts(
    seeds: int,
    *,
    equipment_profiles: tuple[str, ...] = PRIMARY_EQUIPMENT_PROFILES,
) -> dict[str, int]:
    baselines = len(PlayerState) * len(equipment_profiles) * seeds
    ulti = (
        len(PlayerState)
        * len(equipment_profiles)
        * seeds
        * len(ULTIMATES_25)
        * len(Window)
    )
    return {
        "seeds_per_state_and_equipment": seeds,
        "equipment_profiles": len(equipment_profiles),
        "baseline_encounters": baselines,
        "ulti_encounters": ulti,
        "total_encounters": baselines + ulti,
    }


def validate_pair(baseline: FightResult, ulti: FightResult) -> None:
    if baseline.pair_id != ulti.pair_id:
        raise ValueError("PAIR_ID_MISMATCH")
    if baseline.equipment_profile != ulti.equipment_profile:
        raise ValueError("PAIR_EQUIPMENT_MISMATCH")
    if baseline.player_state != ulti.player_state:
        raise ValueError("PAIR_PLAYER_STATE_MISMATCH")


def paired_delta(baseline: FightResult, ulti: FightResult) -> dict[str, Any]:
    validate_pair(baseline, ulti)
    return {
        "pair_id": baseline.pair_id,
        "player_state": ulti.player_state,
        "equipment_profile": ulti.equipment_profile,
        "ultimate": ulti.ultimate,
        "window": ulti.window,
        "baseline_win": baseline.win,
        "ulti_win": ulti.win,
        "loss_to_win_flip": (not baseline.win) and ulti.win,
        "win_to_loss_flip": baseline.win and (not ulti.win),
        "delta_player_hp_end": ulti.player_hp_end - baseline.player_hp_end,
        "delta_player_qi_end": ulti.player_qi_end - baseline.player_qi_end,
        "delta_player_actions": (
            ulti.total_player_actions - baseline.total_player_actions
        ),
        "f3_skip_attempted": ulti.f3_skip_attempted,
        "f3_prevented_lethal_damage": ulti.f3_prevented_lethal_damage,
    }


def self_check_design() -> dict[str, Any]:
    failures: list[str] = []
    smoke = expected_counts(20)
    pilot = expected_counts(200)

    if len(ULTIMATES_25) != 25:
        failures.append("ULTIMATE_COUNT_NOT_25")
    if len(PRIMARY_EQUIPMENT_PROFILES) != 3:
        failures.append("PRIMARY_EQUIPMENT_PROFILE_COUNT_NOT_3")
    if NORMAL_TECHNIQUES_ENABLED:
        failures.append("NORMAL_TECHNIQUES_MUST_BE_DISABLED")
    if CONSUMABLES_ENABLED:
        failures.append("CONSUMABLES_MUST_BE_DISABLED")
    if smoke["ulti_encounters"] != 24000:
        failures.append("SMOKE_COUNT_WRONG")
    if pilot["ulti_encounters"] != 240000:
        failures.append("PILOT_COUNT_WRONG")

    return {
        "pass": not failures,
        "failures": failures,
        "encounter_stage": ENCOUNTER_STAGE,
        "normal_techniques_enabled": NORMAL_TECHNIQUES_ENABLED,
        "consumables_enabled": CONSUMABLES_ENABLED,
        "equipment_profiles": list(PRIMARY_EQUIPMENT_PROFILES),
        "control_equipment_profile": CONTROL_EQUIPMENT_PROFILE,
        "smoke": smoke,
        "pilot": pilot,
    }


if __name__ == "__main__":
    result = self_check_design()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not result["pass"]:
        raise SystemExit(1)
    print()
    print("GRULLA_ULTI25_EQUIPMENT_BENCH_SCAFFOLD: PASS")
    print("Combat execution remains gated until Grulla numeric authority is synced.")
