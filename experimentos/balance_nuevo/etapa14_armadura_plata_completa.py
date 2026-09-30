"""ETAPA 14 — Armadura de Plata completa.

Benchmark integral de base + Tramos I-III + 27 rutas mixables.

Códigos:
R = Resistencia
A = Adaptación
Q = Cantidad

Semántica:
- Placas secuenciales, nunca suman DEF entre sí;
- una Placa activa modifica sólo el impacto directo actual;
- impacto conectado consume 1 Placa salvo regla explícita de Adaptación;
- evasión no consume;
- DOT no consume;
- duración máxima base4.

Recalibración por cantidad de nodos de familia:
R:
  0 -> +3 DEF/Placa
  1 -> +4
  2 -> +6
  3 -> +8
A:
  1 -> +5 Tenacidad tras romper Placa hasta próximo turno
  2 -> +10 Tenacidad y daño0 por DEF no consume Placa
  3 -> +15 Tenacidad; conserva no-consumo; primer Control fallido por
       activación recupera 1 Placa rota, sin superar máximo inicial
Q:
  0 -> 3 Placas
  1 -> 4
  2 -> 6
  3 -> 8

La definición por conteo hace válidas las 27 rutas mixables.

No modifica runtime.
"""
from __future__ import annotations

import argparse
import csv
import itertools
import math
import random
import statistics


PLAYER_HP = 30.0
PLAYER_QI = 31
PLAYER_DEF = 1.0
PLAYER_EVA = 5.0
PLAYER_PREC = 105.0  # 100 + raíz Metal
PLAYER_CRIT = 5.0
PLAYER_CRIT_DAMAGE = 1.50

ENEMY_TOTAL_HP = 28
ENEMY_EVA = 20.0
ENEMY_DEF = 2.0

BASE_PLATES = 3
BASE_PLATE_DEF = 3.0
BASE_DURATION = 4
BASE_COST = 7

PROFILES = {
    "COMMON": (1, 90.0, "2d4+1"),
    "PRECISE": (1, 100.0, "2d4+1"),
    "HEAVY": (1, 90.0, "1d6+3"),
    "DANGEROUS": (1, 100.0, "1d6+3"),
    "2EN": (2, 90.0, "2d4+1"),
    "3EN": (3, 90.0, "2d4+1"),
}


def round_half_up(x: float) -> int:
    return int(math.floor(x + 0.5))


def roll(rng: random.Random, code: str) -> float:
    if code == "2d4+4":
        return rng.randint(1, 4) + rng.randint(1, 4) + 4
    if code == "1d4+4":
        return rng.randint(1, 4) + 4
    if code == "2d4+1":
        return rng.randint(1, 4) + rng.randint(1, 4) + 1
    if code == "1d6+3":
        return rng.randint(1, 6) + 3
    raise ValueError(code)


def direct_hit(
    rng: random.Random,
    precision: float,
    target_evasion: float,
    dice: str,
    target_def: float,
    crit_chance: float = 5.0,
    crit_damage: float = 1.50,
    penetration_pct: float = 0.0,
) -> tuple[bool, int]:
    p_hit = max(5.0, min(100.0, precision - target_evasion)) / 100.0
    if rng.random() >= p_hit:
        return False, 0

    damage = roll(rng, dice)
    if rng.random() < crit_chance / 100.0:
        damage *= crit_damage

    effective_def = target_def * (1.0 - penetration_pct / 100.0)
    return True, round_half_up(max(0.0, damage - effective_def))


def split_hp(count: int) -> list[float]:
    q, r = divmod(ENEMY_TOTAL_HP, count)
    return [float(q + (1 if i < r else 0)) for i in range(count)]


def path_config(path: str) -> dict:
    r = path.count("R")
    a = path.count("A")
    q = path.count("Q")

    plate_def = {0: 3.0, 1: 4.0, 2: 6.0, 3: 8.0}[r]
    plates = {0: 3, 1: 4, 2: 6, 3: 8}[q]

    return {
        "plate_def": plate_def,
        "plates": plates,
        "adapt_nodes": a,
        "reactive_tenacity": 5.0 * a,
        "zero_damage_no_consume": a >= 2,
        "recover_plate_on_control_fail": a >= 3,
        "duration": BASE_DURATION,
        "cost": BASE_COST,
    }


def base_config() -> dict:
    return {
        "plate_def": 3.0,
        "plates": 3,
        "adapt_nodes": 0,
        "reactive_tenacity": 0.0,
        "zero_damage_no_consume": False,
        "recover_plate_on_control_fail": False,
        "duration": BASE_DURATION,
        "cost": BASE_COST,
    }


def run_variant(
    cfg: dict,
    enemy_count: int,
    enemy_precision: float,
    enemy_damage: str,
    fights: int,
    seed: int,
    use_defensive: bool = True,
) -> dict:
    rng = random.Random(seed)

    wins = 0
    rounds = []
    hp_remaining = []
    fallback = 0
    plates_consumed = []
    zero_plate_impacts = []
    zero_saved = []

    for _ in range(fights):
        hp = PLAYER_HP
        qi = PLAYER_QI
        enemy_hps = split_hp(enemy_count)
        round_no = 0
        defense_used = False
        used_basic = False

        plates = 0
        armor_left = 0

        fight_consumed = 0
        fight_zero = 0
        fight_saved = 0

        while hp > 0 and any(value > 0 for value in enemy_hps):
            round_no += 1

            if use_defensive and not defense_used and round_no == 1:
                qi -= cfg["cost"]
                defense_used = True
                plates = cfg["plates"]
                armor_left = cfg["duration"]
            else:
                target = next(
                    i for i, value in enumerate(enemy_hps)
                    if value > 0
                )

                if qi >= 6:
                    _, damage = direct_hit(
                        rng,
                        PLAYER_PREC,
                        ENEMY_EVA,
                        "2d4+4",
                        ENEMY_DEF,
                        PLAYER_CRIT,
                        PLAYER_CRIT_DAMAGE,
                        penetration_pct=20.0,  # raíz10 + Destello10
                    )
                    qi -= 6
                else:
                    _, damage = direct_hit(
                        rng,
                        PLAYER_PREC,
                        ENEMY_EVA,
                        "1d4+4",
                        ENEMY_DEF,
                        PLAYER_CRIT,
                        PLAYER_CRIT_DAMAGE,
                        penetration_pct=10.0,
                    )
                    used_basic = True

                enemy_hps[target] -= damage

            for index, enemy_hp in enumerate(enemy_hps):
                if enemy_hp <= 0 or hp <= 0:
                    continue

                plate_active = armor_left > 0 and plates > 0
                target_def = PLAYER_DEF + (
                    cfg["plate_def"] if plate_active else 0.0
                )

                hit, incoming = direct_hit(
                    rng,
                    enemy_precision,
                    PLAYER_EVA,
                    enemy_damage,
                    target_def,
                )

                hp -= float(incoming)

                if plate_active and hit:
                    if incoming == 0:
                        fight_zero += 1

                    if (
                        cfg["zero_damage_no_consume"]
                        and incoming == 0
                    ):
                        fight_saved += 1
                    else:
                        plates -= 1
                        fight_consumed += 1

            if armor_left > 0:
                armor_left -= 1

            if round_no > 100:
                raise RuntimeError("combate excedió 100 rondas")

        wins += int(
            all(value <= 0 for value in enemy_hps) and hp > 0
        )
        fallback += int(used_basic)
        rounds.append(round_no)
        hp_remaining.append(max(0.0, hp))
        plates_consumed.append(fight_consumed)
        zero_plate_impacts.append(fight_zero)
        zero_saved.append(fight_saved)

    return {
        "win_rate": wins / fights,
        "mean_rounds": statistics.fmean(rounds),
        "mean_hp_remaining_percent": (
            statistics.fmean(hp_remaining) / PLAYER_HP
        ),
        "fallback_rate": fallback / fights,
        "mean_plates_consumed": statistics.fmean(plates_consumed),
        "mean_zero_plate_impacts": statistics.fmean(zero_plate_impacts),
        "mean_zero_saved": statistics.fmean(zero_saved),
    }


def run_control_stress(
    cfg: dict,
    enemy_count: int,
    fights: int,
    seed: int,
    effective_control: float = 65.0,
) -> dict:
    """LAB ilustrativo, NO perfil enemigo canónico.

    Después de cada impacto directo conectado el enemigo intenta SKIP_ACTION.
    La Tenacidad reactiva se activa sólo cuando una Placa se rompe y permanece
    hasta el comienzo del siguiente turno del usuario.
    """

    rng = random.Random(seed)
    control_attempts = 0
    control_success = 0
    plate_recoveries = 0
    skipped_actions = 0
    wins = 0

    for _ in range(fights):
        hp = PLAYER_HP
        qi = PLAYER_QI
        enemy_hps = split_hp(enemy_count)
        round_no = 0
        defense_used = False

        plates = 0
        armor_left = 0
        reactive_tenacity = 0.0
        recovery_used = False
        skip_next_action = False

        while hp > 0 and any(value > 0 for value in enemy_hps):
            round_no += 1
            reactive_tenacity = 0.0

            if skip_next_action:
                skip_next_action = False
                skipped_actions += 1
            elif not defense_used and round_no == 1:
                qi -= cfg["cost"]
                defense_used = True
                plates = cfg["plates"]
                armor_left = cfg["duration"]
            else:
                target = next(
                    i for i, value in enumerate(enemy_hps)
                    if value > 0
                )
                if qi >= 6:
                    _, damage = direct_hit(
                        rng, PLAYER_PREC, ENEMY_EVA,
                        "2d4+4", ENEMY_DEF,
                        penetration_pct=20.0,
                    )
                    qi -= 6
                else:
                    _, damage = direct_hit(
                        rng, PLAYER_PREC, ENEMY_EVA,
                        "1d4+4", ENEMY_DEF,
                        penetration_pct=10.0,
                    )
                enemy_hps[target] -= damage

            for index, enemy_hp in enumerate(enemy_hps):
                if enemy_hp <= 0 or hp <= 0:
                    continue

                plate_active = armor_left > 0 and plates > 0
                target_def = PLAYER_DEF + (
                    cfg["plate_def"] if plate_active else 0.0
                )
                hit, incoming = direct_hit(
                    rng, 90.0, PLAYER_EVA,
                    "2d4+1", target_def,
                )
                hp -= float(incoming)

                if not hit:
                    continue

                if plate_active:
                    if not (
                        cfg["zero_damage_no_consume"]
                        and incoming == 0
                    ):
                        plates -= 1
                        if cfg["adapt_nodes"] > 0:
                            reactive_tenacity = cfg["reactive_tenacity"]

                control_attempts += 1
                p_control = max(
                    5.0,
                    min(
                        100.0,
                        effective_control - reactive_tenacity,
                    ),
                ) / 100.0

                if rng.random() < p_control:
                    control_success += 1
                    skip_next_action = True
                elif (
                    cfg["recover_plate_on_control_fail"]
                    and not recovery_used
                    and plates < cfg["plates"]
                ):
                    plates += 1
                    recovery_used = True
                    plate_recoveries += 1

            if armor_left > 0:
                armor_left -= 1

            if round_no > 100:
                break

        wins += int(
            all(value <= 0 for value in enemy_hps) and hp > 0
        )

    return {
        "win_rate": wins / fights,
        "control_success_rate": (
            control_success / control_attempts
            if control_attempts else 0.0
        ),
        "mean_skipped_actions": skipped_actions / fights,
        "plate_recovery_rate": plate_recoveries / fights,
    }


def full_screen(fights: int, seed: int) -> list[dict]:
    rows = []
    serial = 0

    for path_tuple in itertools.product("RAQ", repeat=3):
        path = "".join(path_tuple)
        cfg = path_config(path)

        for profile, (count, precision, damage) in PROFILES.items():
            result = run_variant(
                cfg,
                count,
                precision,
                damage,
                fights,
                seed + serial,
            )
            serial += 1
            rows.append({
                "provenance": "LAB",
                "path": path,
                "profile": profile,
                **cfg,
                **result,
            })

    return rows


def export(rows: list[dict], path: str) -> None:
    fields = sorted({key for row in rows for key in row})
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--fights", type=int, default=8_000)
    ap.add_argument("--seed", type=int, default=20260929)
    ap.add_argument("--csv", default="etapa14_armadura_plata_27_paths.csv")
    args = ap.parse_args()

    rows = full_screen(args.fights, args.seed)
    export(rows, args.csv)

    print(f"CSV paths: {args.csv} ({len(rows)} escenarios)")
