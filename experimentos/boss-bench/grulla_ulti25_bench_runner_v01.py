#!/usr/bin/env python3
"""
GRULLA_ULTI25_BENCH_RUNNER_V0_1

Scaffold contractual para benchmark pareado Grulla F1->F2->F3.
NO ejecuta peleas con fixtures inventados. Aborta hasta recibir adapters reales.

Estado: DESIGN_LAB / NO_CANON / NO_RUNTIME / NO_MERGE / NO_PUSH
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
from hashlib import sha256
from typing import Protocol, Any, Iterable
import json


class Window(str, Enum):
    F1_EARLY = "F1_EARLY"
    F2_ENTRY = "F2_ENTRY"
    F3_ENTRY = "F3_ENTRY"
    PREPARED_OPPORTUNITY = "PREPARED_OPPORTUNITY"


class PlayerProfile(str, Enum):
    FULL = "FULL"
    BALANCED = "BALANCED"
    DISADVANTAGE = "DISADVANTAGE"
    NEAR_DEATH = "NEAR_DEATH"


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
    profile: str
    seed_index: int
    ultimate: str | None
    window: str

    @property
    def pair_id(self) -> str:
        # baseline y ramas Ulti comparten profile + seed_index
        return f"{self.profile}:{self.seed_index:06d}"


@dataclass
class FightResult:
    pair_id: str
    profile: str
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


class GrullaAdapter(Protocol):
    """Debe envolver la IA/estado REAL del jefe, no un saco sintético de HP."""

    authority_id: str
    pacto_contract: str

    def new_encounter(self, *, profile: str, rng: "RngStreams") -> Any:
        ...

    def is_finished(self, encounter: Any) -> bool:
        ...

    def snapshot(self, encounter: Any) -> dict[str, Any]:
        ...


class UltimateAdapter(Protocol):
    """Debe ejecutar las 25 Ultis cerradas y técnicas auxiliares reales."""

    authority_id: str

    def can_activate(self, encounter: Any, ultimate: str, window: str) -> tuple[bool, str | None]:
        ...

    def activate(self, encounter: Any, ultimate: str, rng: "RngStreams") -> None:
        ...


class PlayerPolicy(Protocol):
    authority_id: str

    def choose_normal_action(self, encounter: Any, rng: "RngStreams") -> Any:
        ...


class RngStreams:
    """
    Common-random-number scaffold.

    No usa una única secuencia consumible por toda la pelea, porque una Ulti
    introduciría tiradas adicionales y desalinearía baseline vs rama.

    Cada dominio deriva una seed estable del master seed. El adapter real puede
    subdividir todavía más por turno/evento sin cambiar la autoridad del bench.
    """

    DOMAINS = (
        "boss_decision",
        "boss_accuracy",
        "boss_crit",
        "player_normal_accuracy",
        "player_normal_crit",
        "control",
        "status",
        "ultimate",
        "aux_technique",
    )

    def __init__(self, master_seed: int):
        self.master_seed = int(master_seed)

    def seed_for(self, domain: str, *coords: Any) -> int:
        if domain not in self.DOMAINS:
            raise ValueError(f"RNG domain no autorizado: {domain}")
        payload = "|".join(map(str, (self.master_seed, domain, *coords))).encode("utf-8")
        return int.from_bytes(sha256(payload).digest()[:8], "big")


def master_seed(profile: str, seed_index: int, base_seed: int = 2026100201) -> int:
    payload = f"{base_seed}|{profile}|{seed_index}".encode("utf-8")
    return int.from_bytes(sha256(payload).digest()[:8], "big")


def iter_ulti_scenarios(seeds: int) -> Iterable[ScenarioKey]:
    for profile in PlayerProfile:
        for seed_index in range(seeds):
            for ultimate in ULTIMATES_25:
                for window in Window:
                    yield ScenarioKey(
                        profile=profile.value,
                        seed_index=seed_index,
                        ultimate=ultimate,
                        window=window.value,
                    )


def iter_baselines(seeds: int) -> Iterable[ScenarioKey]:
    for profile in PlayerProfile:
        for seed_index in range(seeds):
            yield ScenarioKey(
                profile=profile.value,
                seed_index=seed_index,
                ultimate=None,
                window="BASELINE_NO_ULTI",
            )


def expected_counts(seeds: int) -> dict[str, int]:
    baselines = len(PlayerProfile) * seeds
    ulti = len(PlayerProfile) * seeds * len(ULTIMATES_25) * len(Window)
    return {
        "seeds_per_profile": seeds,
        "baseline_encounters": baselines,
        "ulti_encounters": ulti,
        "total_encounters": baselines + ulti,
    }


def validate_result(result: FightResult) -> list[str]:
    failures: list[str] = []

    if result.f3_boss_actions == 0 and result.telemetry.get("reached_f3") and result.telemetry.get("boss_killed"):
        failures.append("F3_KILL_BEFORE_FIRST_REAL_ACTION")

    if result.telemetry.get("pact_released_by_prevented_action"):
        failures.append("PACT_RELEASED_BY_PREVENTED_ACTION")

    if result.telemetry.get("multihit_bypassed_f3_gate"):
        failures.append("MULTIHIT_BYPASSED_F3_GATE")

    if result.f3_skip_attempted and result.f3_lethal_preventions < 1:
        failures.append("SKIP_ATTEMPT_WITHOUT_LETHAL_PREVENTION")

    return failures


def paired_delta(baseline: FightResult, ulti: FightResult) -> dict[str, Any]:
    if baseline.pair_id != ulti.pair_id:
        raise ValueError("PAIR_ID_MISMATCH")

    return {
        "pair_id": baseline.pair_id,
        "ultimate": ulti.ultimate,
        "window": ulti.window,
        "baseline_win": baseline.win,
        "ulti_win": ulti.win,
        "loss_to_win_flip": (not baseline.win) and ulti.win,
        "win_to_loss_flip": baseline.win and (not ulti.win),
        "delta_player_hp_end": ulti.player_hp_end - baseline.player_hp_end,
        "delta_player_qi_end": ulti.player_qi_end - baseline.player_qi_end,
        "delta_player_actions": ulti.total_player_actions - baseline.total_player_actions,
        "f3_skip_attempted": ulti.f3_skip_attempted,
        "f3_prevented_lethal_damage": ulti.f3_prevented_lethal_damage,
    }


def self_check_design() -> dict[str, Any]:
    smoke = expected_counts(20)
    pilot = expected_counts(200)
    failures = []

    if len(ULTIMATES_25) != 25:
        failures.append("ULTIMATE_COUNT_NOT_25")
    if smoke["ulti_encounters"] != 8000:
        failures.append("SMOKE_COUNT_WRONG")
    if pilot["ulti_encounters"] != 80000:
        failures.append("PILOT_COUNT_WRONG")
    if "F3_ENTRY" not in {w.value for w in Window}:
        failures.append("MISSING_F3_ENTRY")
    if len(set(RngStreams.DOMAINS)) != len(RngStreams.DOMAINS):
        failures.append("DUPLICATE_RNG_DOMAIN")

    return {
        "pass": not failures,
        "failures": failures,
        "smoke": smoke,
        "pilot": pilot,
        "ultimate_count": len(ULTIMATES_25),
        "windows": [w.value for w in Window],
        "profiles": [p.value for p in PlayerProfile],
    }


def require_real_adapters(*, grulla: GrullaAdapter | None, ultis: UltimateAdapter | None,
                          player: PlayerPolicy | None) -> None:
    missing = []
    if grulla is None:
        missing.append("EXECUTABLE_GRULLA_F1_F2_F3_SOURCE")
    if ultis is None:
        missing.append("ULTIMATE_AUTHORITY_ADAPTER")
    if player is None:
        missing.append("AUTHORITATIVE_PLAYER_FIXTURE_AND_POLICY")
    if missing:
        raise RuntimeError(
            "BENCH_BLOCKED_NO_SYNTHETIC_FALLBACK: " + ", ".join(missing)
        )


if __name__ == "__main__":
    # Por diseño, este archivo sólo valida el scaffold hasta recibir adapters reales.
    result = self_check_design()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not result["pass"]:
        raise SystemExit(1)

    print()
    print("GRULLA_ULTI25_BENCH_SCAFFOLD: PASS")
    print("Mass combat execution: BLOCKED hasta conectar adapters autoritativos.")
