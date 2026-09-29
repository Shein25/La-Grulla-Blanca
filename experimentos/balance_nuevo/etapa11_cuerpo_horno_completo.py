"""ETAPA 11 — Respiración del Cuerpo-Horno completa.

Rebenchmark de base + Tramos I-III con 27 combinaciones mixables.

Guardias:
- LAB runner; no toca runtime.
- base candidata: 25% HP Absorción / 2 turnos / coste7.
- Barrera conserva incrementos de +5 pp.
- Conversión usa la recalibración candidata definida aquí.
- Eficiencia conserva coste/duración y se evalúa también por umbrales de Qi.

Semántica LAB de Calor usada para el benchmark:
- se almacena al absorber daño;
- se consume al usar una técnica ofensiva de Fuego posterior;
- comparte el acierto/fallo de esa técnica; no hace una tirada de precisión propia;
- si la técnica portadora falla, el Calor se consume sin causar daño;
- si impacta, el Calor se resuelve como porción secundaria separada:
  no crit, no escalado ofensivo, no penetración, sí DEF/Absorción.
"""
from __future__ import annotations

import argparse
import csv
import itertools
import math
import random
import statistics


BASE_HP = 30.0
BASE_QI = 31
PLAYER_DEF = 1.0
PLAYER_EVA = 5.0
PLAYER_PREC = 100.0
PLAYER_CRIT = 10.0
PLAYER_CRIT_DAMAGE = 1.50
PLAYER_DAMAGE_PERCENT = 10.0

ENEMY_TOTAL_HP = 28
ENEMY_EVA = 20.0
ENEMY_DEF = 2.0
ENEMY_CRIT = 5.0
ENEMY_CRIT_DAMAGE = 1.50

BASE_ABSORPTION = 0.25
BASE_DURATION = 2
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
    if code == "2d4+5":
        return rng.randint(1, 4) + rng.randint(1, 4) + 5
    if code == "1d4+4":
        return rng.randint(1, 4) + 4
    if code == "2d4+1":
        return rng.randint(1, 4) + rng.randint(1, 4) + 1
    if code == "1d6+3":
        return rng.randint(1, 6) + 3
    raise ValueError(code)


def direct_hit(
    rng: random.Random,
    attacker_precision: float,
    target_evasion: float,
    dice: str,
    damage_percent: float,
    crit_chance: float,
    target_def: float,
    crit_damage: float = 1.50,
) -> tuple[bool, int]:
    p_hit = max(5.0, min(100.0, attacker_precision - target_evasion)) / 100.0
    if rng.random() >= p_hit:
        return False, 0

    damage = roll(rng, dice) * (1.0 + damage_percent / 100.0)
    if rng.random() < crit_chance / 100.0:
        damage *= crit_damage

    return True, round_half_up(max(0.0, damage - target_def))


def path_config(t1: str, t2: str, t3: str) -> dict:
    """Config candidata completa.

    B = Barrera
    C = Conversión
    E = Eficiencia
    """
    absorption = BASE_ABSORPTION
    duration = BASE_DURATION
    cost = float(BASE_COST)
    heat_rate = 0.0
    heat_cap = 0.0
    conversion_nodes = 0

    # Tramo I
    if t1 == "B":
        absorption += 0.05
    elif t1 == "C":
        heat_rate = 0.40
        heat_cap = 0.10
        conversion_nodes = 1
    elif t1 == "E":
        cost = 6.0

    # Tramo II
    if t2 == "B":
        absorption += 0.05
        if t1 == "B":
            absorption += 0.05
    elif t2 == "C":
        if conversion_nodes == 0:
            heat_rate = 0.50
            heat_cap = 0.10
        else:
            heat_rate = 0.60
            heat_cap = 0.15
        conversion_nodes += 1
    elif t2 == "E":
        cost *= 0.90
        if t1 == "E":
            duration = 3

    # Tramo III
    if t3 == "B":
        absorption += 0.05
    elif t3 == "C":
        if conversion_nodes == 0:
            heat_rate = 0.50
            heat_cap = 0.10
        elif conversion_nodes == 1:
            heat_rate = 0.70
            heat_cap = 0.15
        else:
            heat_rate = 0.80
            heat_cap = 0.20
        conversion_nodes += 1
    elif t3 == "E":
        cost *= 0.90
        if t1 == "E" and t2 == "E":
            duration = 4
            absorption += 0.05

    return {
        "absorption_pct": absorption,
        "duration": duration,
        "cost": round_half_up(cost),
        "heat_rate": heat_rate,
        "heat_cap_pct": heat_cap,
    }


def split_hp(count: int) -> list[float]:
    q, r = divmod(ENEMY_TOTAL_HP, count)
    return [float(q + (1 if i < r else 0)) for i in range(count)]


def run_variant(
    cfg: dict,
    enemy_count: int,
    enemy_precision: float,
    enemy_damage: str,
    fights: int,
    seed: int,
    qi_max: int = BASE_QI,
) -> dict:
    rng = random.Random(seed)

    wins = 0
    rounds = []
    hp_remaining = []
    fallback = 0
    absorption_used = []
    heat_generated = []
    heat_damage = []
    enemy_hits = []

    for _ in range(fights):
        hp = BASE_HP
        qi = qi_max
        enemy_hps = split_hp(enemy_count)
        round_no = 0
        defense_used = False
        used_basic = False

        reserve = 0.0
        turns_left = 0
        heat = 0.0

        total_absorbed = 0.0
        total_heat_generated = 0.0
        total_heat_damage = 0.0
        total_enemy_hits = 0

        while hp > 0 and any(value > 0 for value in enemy_hps):
            round_no += 1

            if not defense_used and round_no == 1:
                qi -= cfg["cost"]
                defense_used = True
                reserve = cfg["absorption_pct"] * BASE_HP
                turns_left = cfg["duration"]
            else:
                target = next(i for i, value in enumerate(enemy_hps) if value > 0)

                if qi >= 6:
                    hit, damage = direct_hit(
                        rng,
                        PLAYER_PREC,
                        ENEMY_EVA,
                        "2d4+5",
                        PLAYER_DAMAGE_PERCENT,
                        PLAYER_CRIT,
                        ENEMY_DEF,
                        PLAYER_CRIT_DAMAGE,
                    )
                    qi -= 6
                    enemy_hps[target] -= damage

                    # Calor se consume con la técnica portadora.
                    if heat > 0:
                        stored = heat
                        heat = 0.0
                        if hit and enemy_hps[target] > 0:
                            secondary = round_half_up(max(0.0, stored - ENEMY_DEF))
                            enemy_hps[target] -= secondary
                            total_heat_damage += secondary
                else:
                    _, damage = direct_hit(
                        rng,
                        PLAYER_PREC,
                        ENEMY_EVA,
                        "1d4+4",
                        PLAYER_DAMAGE_PERCENT,
                        PLAYER_CRIT,
                        ENEMY_DEF,
                        PLAYER_CRIT_DAMAGE,
                    )
                    enemy_hps[target] -= damage
                    used_basic = True

            for index, enemy_hp in enumerate(enemy_hps):
                if enemy_hp <= 0 or hp <= 0:
                    continue

                hit, damage = direct_hit(
                    rng,
                    enemy_precision,
                    PLAYER_EVA,
                    enemy_damage,
                    0.0,
                    ENEMY_CRIT,
                    PLAYER_DEF,
                    ENEMY_CRIT_DAMAGE,
                )
                total_enemy_hits += int(hit)
                hp_damage = float(damage)

                if turns_left > 0 and reserve > 0:
                    absorbed = min(reserve, hp_damage)
                    reserve -= absorbed
                    hp_damage -= absorbed
                    total_absorbed += absorbed

                    if cfg["heat_rate"] > 0 and absorbed > 0:
                        cap = cfg["heat_cap_pct"] * BASE_HP
                        new_heat = min(cap, heat + absorbed * cfg["heat_rate"])
                        total_heat_generated += new_heat - heat
                        heat = new_heat

                hp -= hp_damage

            if turns_left > 0:
                turns_left -= 1
                if turns_left <= 0:
                    reserve = 0.0

            if round_no > 100:
                raise RuntimeError("combate excedió 100 rondas")

        wins += int(all(value <= 0 for value in enemy_hps) and hp > 0)
        fallback += int(used_basic)
        rounds.append(round_no)
        hp_remaining.append(max(0.0, hp))
        absorption_used.append(total_absorbed)
        heat_generated.append(total_heat_generated)
        heat_damage.append(total_heat_damage)
        enemy_hits.append(total_enemy_hits)

    return {
        "win_rate": wins / fights,
        "mean_rounds": statistics.fmean(rounds),
        "mean_hp_remaining_percent": statistics.fmean(hp_remaining) / BASE_HP,
        "fallback_rate": fallback / fights,
        "mean_absorption_used": statistics.fmean(absorption_used),
        "mean_heat_generated": statistics.fmean(heat_generated),
        "mean_heat_damage": statistics.fmean(heat_damage),
        "mean_enemy_hits": statistics.fmean(enemy_hits),
    }


def full_screen(fights: int, seed: int) -> list[dict]:
    rows = []
    serial = 0

    for t1, t2, t3 in itertools.product("BCE", repeat=3):
        path = t1 + t2 + t3
        cfg = path_config(t1, t2, t3)

        for profile, (enemy_count, precision, damage) in PROFILES.items():
            result = run_variant(
                cfg,
                enemy_count,
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


def qi_lattice() -> list[dict]:
    rows = []
    for qi in range(25, 61):
        rows.append({
            "qi": qi,
            "def_cost_7_offenses": max(0, (qi - 7) // 6),
            "def_cost_6_offenses": max(0, (qi - 6) // 6),
            "def_cost_5_offenses": max(0, (qi - 5) // 6),
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
    ap.add_argument("--fights", type=int, default=10_000)
    ap.add_argument("--seed", type=int, default=20260929)
    ap.add_argument("--csv", default="etapa11_cuerpo_horno_27_paths.csv")
    ap.add_argument("--qi-csv", default="etapa11_cuerpo_horno_qi_lattice.csv")
    args = ap.parse_args()

    rows = full_screen(args.fights, args.seed)
    export(rows, args.csv)
    export(qi_lattice(), args.qi_csv)
    print(f"CSV paths: {args.csv} ({len(rows)} escenarios)")
    print(f"CSV Qi: {args.qi_csv}")
