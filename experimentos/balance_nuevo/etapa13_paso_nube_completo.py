"""ETAPA 13 — Paso de Nube Ligera completo.

Benchmark integral de base + Tramos I-III + 27 rutas mixables.

Códigos de rama:
V = Evasión
R = Respuesta / CORRIENTE_CLARA
E = Eficiencia

Semántica:
- Paso no introduce movimiento/Velocidad ni segunda tirada;
- raíz Viento aporta +10 EVA y +5 pp daño crítico;
- Lanza que Parte Nubes usa +5 Precisión y +5 pp crítico;
- primera evasión válida durante Paso puede crear CORRIENTE_CLARA si hay
  al menos un nodo R;
- CORRIENTE_CLARA se consume por la siguiente técnica pura de Viento;
- el ataque básico no la consume.

Candidatos recalibrados:
BASE = +35 EVA / 4 turnos / coste7.
V: +5 EVA por nodo.
R: 1 nodo +5 Precisión; 2 nodos +10; 3 nodos +15 y +5 pp crítico.
E:
  T1 Respiración Ligera: coste7->6.
  T2: -10% coste; con E previa, +1 duración.
  T3: -10% coste; con cualquier E previa, +1 duración.
  EEE = coste efectivo5 / duración6.

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
PLAYER_BASE_EVA = 5.0
ROOT_EVA = 10.0
PLAYER_PREC = 100.0
PLAYER_CRIT = 5.0
PLAYER_CRIT_DAMAGE = 1.55

ENEMY_TOTAL_HP = 28
ENEMY_EVA = 20.0
ENEMY_DEF = 2.0

BASE_PASO_EVA = 35.0
BASE_DURATION = 4
BASE_COST = 7.0

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
    if code == "2d4+3":
        return rng.randint(1, 4) + rng.randint(1, 4) + 3
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
    crit_chance: float,
    crit_damage: float,
) -> tuple[bool, bool, int]:
    p_hit = max(5.0, min(100.0, precision - target_evasion)) / 100.0
    if rng.random() >= p_hit:
        return False, False, 0

    damage = roll(rng, dice)
    critical = rng.random() < crit_chance / 100.0
    if critical:
        damage *= crit_damage

    return True, critical, round_half_up(max(0.0, damage - target_def))


def split_hp(count: int) -> list[float]:
    q, r = divmod(ENEMY_TOTAL_HP, count)
    return [float(q + (1 if i < r else 0)) for i in range(count)]


def path_config(t1: str, t2: str, t3: str) -> dict:
    evasion = BASE_PASO_EVA
    duration = BASE_DURATION
    cost = BASE_COST
    response_nodes = 0

    if t1 == "V":
        evasion += 5.0
    elif t1 == "R":
        response_nodes += 1
    elif t1 == "E":
        cost = 6.0

    if t2 == "V":
        evasion += 5.0
    elif t2 == "R":
        response_nodes += 1
    elif t2 == "E":
        cost *= 0.90
        if t1 == "E":
            duration += 1

    if t3 == "V":
        evasion += 5.0
    elif t3 == "R":
        response_nodes += 1
    elif t3 == "E":
        cost *= 0.90
        if t1 == "E" or t2 == "E":
            duration += 1

    return {
        "evasion_granted": evasion,
        "duration": duration,
        "effective_cost": round_half_up(cost),
        "response_nodes": response_nodes,
        "corriente_precision": 5.0 * response_nodes,
        "corriente_crit_pp": 5.0 if response_nodes == 3 else 0.0,
    }


def base_old_config() -> dict:
    return {
        "evasion_granted": 15.0,
        "duration": 2,
        "effective_cost": 7,
        "response_nodes": 0,
        "corriente_precision": 0.0,
        "corriente_crit_pp": 0.0,
    }


def base_new_config() -> dict:
    return {
        "evasion_granted": 35.0,
        "duration": 4,
        "effective_cost": 7,
        "response_nodes": 0,
        "corriente_precision": 0.0,
        "corriente_crit_pp": 0.0,
    }


def run_variant(
    cfg: dict,
    enemy_count: int,
    enemy_precision: float,
    enemy_damage: str,
    fights: int,
    seed: int,
    use_defensive: bool = True,
    qi_max: int = PLAYER_QI,
) -> dict:
    rng = random.Random(seed)

    wins = 0
    rounds = []
    hp_remaining = []
    fallback = 0
    evades = []
    enemy_hits = []
    corriente_triggers = []
    corriente_consumes = []

    for _ in range(fights):
        hp = PLAYER_HP
        qi = qi_max
        enemy_hps = split_hp(enemy_count)
        round_no = 0
        defense_used = False
        used_basic = False

        paso_left = 0
        corriente_ready = False
        corriente_triggered = False

        fight_evades = 0
        fight_hits = 0
        fight_triggers = 0
        fight_consumes = 0

        while hp > 0 and any(value > 0 for value in enemy_hps):
            round_no += 1

            if use_defensive and not defense_used and round_no == 1:
                qi -= cfg["effective_cost"]
                defense_used = True
                paso_left = cfg["duration"]
            else:
                target = next(
                    i for i, value in enumerate(enemy_hps)
                    if value > 0
                )

                if qi >= 6:
                    precision = (
                        PLAYER_PREC
                        + 5.0
                        + (
                            cfg["corriente_precision"]
                            if corriente_ready
                            else 0.0
                        )
                    )
                    crit = (
                        PLAYER_CRIT
                        + 5.0
                        + (
                            cfg["corriente_crit_pp"]
                            if corriente_ready
                            else 0.0
                        )
                    )
                    _, _, damage = direct_hit(
                        rng,
                        precision,
                        ENEMY_EVA,
                        "2d4+3",
                        ENEMY_DEF,
                        crit,
                        PLAYER_CRIT_DAMAGE,
                    )
                    qi -= 6

                    if corriente_ready:
                        corriente_ready = False
                        fight_consumes += 1
                else:
                    _, _, damage = direct_hit(
                        rng,
                        PLAYER_PREC,
                        ENEMY_EVA,
                        "1d4+4",
                        ENEMY_DEF,
                        PLAYER_CRIT,
                        PLAYER_CRIT_DAMAGE,
                    )
                    used_basic = True

                enemy_hps[target] -= damage

            for index, enemy_hp in enumerate(enemy_hps):
                if enemy_hp <= 0 or hp <= 0:
                    continue

                target_evasion = (
                    PLAYER_BASE_EVA
                    + ROOT_EVA
                    + (
                        cfg["evasion_granted"]
                        if paso_left > 0
                        else 0.0
                    )
                )

                hit, _, incoming = direct_hit(
                    rng,
                    enemy_precision,
                    target_evasion,
                    enemy_damage,
                    PLAYER_DEF,
                    5.0,
                    1.50,
                )

                if hit:
                    fight_hits += 1
                else:
                    fight_evades += 1

                    if (
                        paso_left > 0
                        and cfg["response_nodes"] > 0
                        and not corriente_triggered
                    ):
                        corriente_ready = True
                        corriente_triggered = True
                        fight_triggers += 1

                hp -= float(incoming)

            if paso_left > 0:
                paso_left -= 1

            if round_no > 100:
                raise RuntimeError("combate excedió 100 rondas")

        wins += int(
            all(value <= 0 for value in enemy_hps) and hp > 0
        )
        fallback += int(used_basic)
        rounds.append(round_no)
        hp_remaining.append(max(0.0, hp))
        evades.append(fight_evades)
        enemy_hits.append(fight_hits)
        corriente_triggers.append(fight_triggers)
        corriente_consumes.append(fight_consumes)

    return {
        "win_rate": wins / fights,
        "mean_rounds": statistics.fmean(rounds),
        "mean_hp_remaining_percent": (
            statistics.fmean(hp_remaining) / PLAYER_HP
        ),
        "fallback_rate": fallback / fights,
        "mean_evades": statistics.fmean(evades),
        "mean_enemy_hits": statistics.fmean(enemy_hits),
        "corriente_trigger_rate": statistics.fmean(corriente_triggers),
        "corriente_consume_rate": statistics.fmean(corriente_consumes),
    }


def full_screen(fights: int, seed: int) -> list[dict]:
    rows = []
    serial = 0

    for t1, t2, t3 in itertools.product("VRE", repeat=3):
        path = t1 + t2 + t3
        cfg = path_config(t1, t2, t3)

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


def qi_lattice() -> list[dict]:
    rows = []
    for qi in range(25, 61):
        rows.append({
            "qi": qi,
            "offensive_cost": 6,
            "paso_cost_7_offenses": max(0, (qi - 7) // 6),
            "paso_cost_6_offenses": max(0, (qi - 6) // 6),
            "paso_cost_5_offenses": max(0, (qi - 5) // 6),
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
    ap.add_argument("--csv", default="etapa13_paso_nube_27_paths.csv")
    ap.add_argument("--qi-csv", default="etapa13_paso_nube_qi_lattice.csv")
    args = ap.parse_args()

    rows = full_screen(args.fights, args.seed)
    export(rows, args.csv)
    export(qi_lattice(), args.qi_csv)

    print(f"CSV paths: {args.csv} ({len(rows)} escenarios)")
    print(f"CSV Qi: {args.qi_csv}")
