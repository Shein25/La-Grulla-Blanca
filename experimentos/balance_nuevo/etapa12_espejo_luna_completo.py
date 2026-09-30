"""ETAPA 12 — Espejo de Luna completo.

Benchmark integral de base + Tramos I-III + 27 rutas mixables.

Semántica del benchmark:
- raíz Agua: -10% coste global y +5 Control;
- Latigazo: Arrastre 50% efectivo de referencia;
- anti-lock por objetivo: después de sufrir Arrastre debe completar una acción
  normal antes de volver a ser elegible;
- Reflujo ocurre en TURN_START si queda Absorción;
- si la reserva llega a 0, Reflujo normal deja de funcionar;
- reconstrucción explícita puede recrear el pool una vez por activación.

Códigos:
R = Reserva
G = Regeneración / Reflujo
E = Eficiencia

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
PLAYER_PREC = 100.0

ENEMY_TOTAL_HP = 28
ENEMY_EVA = 20.0
ENEMY_DEF = 2.0

BASE_RESERVE = 0.24
BASE_REFLOW = 0.25
BASE_DURATION = 3
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


def water_cost(base_cost: float, branch_multiplier: float = 1.0) -> int:
    return round_half_up(base_cost * branch_multiplier * 0.90)


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
) -> tuple[bool, int]:
    p_hit = max(5.0, min(100.0, precision - target_evasion)) / 100.0
    if rng.random() >= p_hit:
        return False, 0

    damage = roll(rng, dice)
    if rng.random() < 0.05:
        damage *= 1.50

    return True, round_half_up(max(0.0, damage - target_def))


def split_hp(count: int) -> list[float]:
    q, r = divmod(ENEMY_TOTAL_HP, count)
    return [float(q + (1 if i < r else 0)) for i in range(count)]


def path_config(t1: str, t2: str, t3: str) -> dict:
    reserve = BASE_RESERVE
    reflow = BASE_REFLOW
    duration = BASE_DURATION
    base_cost = BASE_COST
    cost_multiplier = 1.0
    reconstruct = 0.0
    qi_restore_on_natural_expire = 0

    # Tramo I
    if t1 == "R":
        reserve += 0.05
    elif t1 == "G":
        reflow += 0.10
    elif t1 == "E":
        base_cost = 6.0

    # Tramo II
    if t2 == "R":
        reserve += 0.05
        if t1 == "R":
            reserve += 0.03
    elif t2 == "G":
        reflow = min(0.50, reflow + 0.10)
        if t1 == "G":
            reconstruct = 0.40
    elif t2 == "E":
        # 10% era redondeado a cero junto a la raíz Agua.
        # 15% es el primer escalón limpio que lleva coste efectivo 6 -> 5.
        cost_multiplier *= 0.85
        if t1 == "E":
            duration = 4

    # Tramo III
    if t3 == "R":
        reserve += 0.05
    elif t3 == "G":
        reflow = min(0.50, reflow + 0.10)
        if reconstruct > 0:
            reconstruct = 0.50
    elif t3 == "E":
        cost_multiplier *= 0.85
        qi_restore_on_natural_expire = 1
        if t1 == "E" and t2 == "E":
            duration = 5

    return {
        "reserve_pct": reserve,
        "reflow_pct": reflow,
        "duration": duration,
        "effective_cost": water_cost(base_cost, cost_multiplier),
        "reconstruct_pct": reconstruct,
        "qi_restore_on_natural_expire": qi_restore_on_natural_expire,
    }


def base12_config() -> dict:
    return {
        "reserve_pct": 0.12,
        "reflow_pct": 0.25,
        "duration": 3,
        "effective_cost": 6,
        "reconstruct_pct": 0.0,
        "qi_restore_on_natural_expire": 0,
    }


def base24_config() -> dict:
    return {
        "reserve_pct": 0.24,
        "reflow_pct": 0.25,
        "duration": 3,
        "effective_cost": 6,
        "reconstruct_pct": 0.0,
        "qi_restore_on_natural_expire": 0,
    }


def run_variant(
    cfg: dict,
    enemy_count: int,
    enemy_precision: float,
    enemy_damage: str,
    fights: int,
    seed: int,
    qi_max: int = PLAYER_QI,
) -> dict:
    rng = random.Random(seed)

    wins = 0
    rounds = []
    hp_remaining = []
    fallback = 0
    reflow_amount = []
    reconstruction = 0
    breaks = 0
    arrastre_skips = []
    qi_restored = []

    for _ in range(fights):
        hp = PLAYER_HP
        qi = qi_max
        enemy_hps = split_hp(enemy_count)
        round_no = 0
        defense_used = False
        used_basic = False

        reserve = 0.0
        reserve_max = 0.0
        turns_left = 0
        active = False
        reconstruction_used = False

        eligible = [True] * enemy_count
        skip_pending = [False] * enemy_count
        needs_normal_action = [False] * enemy_count

        total_reflow = 0.0
        fight_broke = False
        skips = 0
        restored_qi = 0

        while hp > 0 and any(value > 0 for value in enemy_hps):
            round_no += 1

            # TURN_START: restauración defensiva antes de DOT/acción.
            if active and turns_left > 0:
                if reserve > 0:
                    restored = min(
                        reserve_max - reserve,
                        cfg["reflow_pct"] * reserve_max,
                    )
                    if restored > 0:
                        reserve += restored
                        total_reflow += restored
                elif (
                    cfg["reconstruct_pct"] > 0
                    and not reconstruction_used
                ):
                    reserve = cfg["reconstruct_pct"] * reserve_max
                    reconstruction_used = True
                    reconstruction += 1

            if not defense_used and round_no == 1:
                qi -= cfg["effective_cost"]
                defense_used = True
                active = True
                turns_left = cfg["duration"]
                reserve_max = cfg["reserve_pct"] * PLAYER_HP
                reserve = reserve_max
            else:
                target = next(
                    i for i, value in enumerate(enemy_hps)
                    if value > 0
                )

                offensive_cost = water_cost(7.0)
                if qi >= offensive_cost:
                    hit, damage = direct_hit(
                        rng,
                        PLAYER_PREC,
                        ENEMY_EVA,
                        "2d4+3",
                        ENEMY_DEF,
                    )
                    qi -= offensive_cost

                    if (
                        hit
                        and eligible[target]
                        and rng.random() < 0.50
                    ):
                        skip_pending[target] = True
                        eligible[target] = False
                        needs_normal_action[target] = True
                else:
                    hit, damage = direct_hit(
                        rng,
                        PLAYER_PREC,
                        ENEMY_EVA,
                        "1d4+4",
                        ENEMY_DEF,
                    )
                    used_basic = True

                enemy_hps[target] -= damage

            for index, enemy_hp in enumerate(enemy_hps):
                if enemy_hp <= 0 or hp <= 0:
                    continue

                if skip_pending[index]:
                    skip_pending[index] = False
                    skips += 1
                    continue

                _, incoming = direct_hit(
                    rng,
                    enemy_precision,
                    PLAYER_EVA,
                    enemy_damage,
                    PLAYER_DEF,
                )
                hp_damage = float(incoming)

                if active and turns_left > 0 and reserve > 0:
                    absorbed = min(reserve, hp_damage)
                    reserve -= absorbed
                    hp_damage -= absorbed

                    if reserve <= 0 and not fight_broke:
                        fight_broke = True
                        breaks += 1

                hp -= hp_damage

                # Anti-lock: sólo una acción normal completada
                # vuelve a habilitar Arrastre.
                if needs_normal_action[index]:
                    needs_normal_action[index] = False
                    eligible[index] = True

            if active and turns_left > 0:
                turns_left -= 1
                if turns_left <= 0:
                    if (
                        reserve > 0
                        and cfg["qi_restore_on_natural_expire"] > 0
                    ):
                        qi += cfg["qi_restore_on_natural_expire"]
                        restored_qi += cfg["qi_restore_on_natural_expire"]

                    active = False
                    reserve = 0.0

            if round_no > 100:
                raise RuntimeError("combate excedió 100 rondas")

        wins += int(
            all(value <= 0 for value in enemy_hps) and hp > 0
        )
        fallback += int(used_basic)
        rounds.append(round_no)
        hp_remaining.append(max(0.0, hp))
        reflow_amount.append(total_reflow)
        arrastre_skips.append(skips)
        qi_restored.append(restored_qi)

    return {
        "win_rate": wins / fights,
        "mean_rounds": statistics.fmean(rounds),
        "mean_hp_remaining_percent": (
            statistics.fmean(hp_remaining) / PLAYER_HP
        ),
        "fallback_rate": fallback / fights,
        "mean_reflow_amount": statistics.fmean(reflow_amount),
        "reconstruction_rate": reconstruction / fights,
        "break_rate": breaks / fights,
        "mean_arrastre_skips": statistics.fmean(arrastre_skips),
        "mean_qi_restored": statistics.fmean(qi_restored),
    }


def run_offense_only(
    enemy_count: int,
    enemy_precision: float,
    enemy_damage: str,
    fights: int,
    seed: int,
    qi_max: int = PLAYER_QI,
) -> dict:
    # Usa exactamente el mismo anti-lock, pero sin Espejo.
    cfg = {
        "reserve_pct": 0.0,
        "reflow_pct": 0.0,
        "duration": 0,
        "effective_cost": 0,
        "reconstruct_pct": 0.0,
        "qi_restore_on_natural_expire": 0,
    }

    rng = random.Random(seed)
    wins = 0
    hp_remaining = []
    rounds = []
    fallback = 0

    for _ in range(fights):
        hp = PLAYER_HP
        qi = qi_max
        enemy_hps = split_hp(enemy_count)
        round_no = 0
        used_basic = False

        eligible = [True] * enemy_count
        skip_pending = [False] * enemy_count
        needs_normal_action = [False] * enemy_count

        while hp > 0 and any(value > 0 for value in enemy_hps):
            round_no += 1
            target = next(
                i for i, value in enumerate(enemy_hps)
                if value > 0
            )

            offensive_cost = water_cost(7.0)
            if qi >= offensive_cost:
                hit, damage = direct_hit(
                    rng,
                    PLAYER_PREC,
                    ENEMY_EVA,
                    "2d4+3",
                    ENEMY_DEF,
                )
                qi -= offensive_cost

                if (
                    hit
                    and eligible[target]
                    and rng.random() < 0.50
                ):
                    skip_pending[target] = True
                    eligible[target] = False
                    needs_normal_action[target] = True
            else:
                hit, damage = direct_hit(
                    rng,
                    PLAYER_PREC,
                    ENEMY_EVA,
                    "1d4+4",
                    ENEMY_DEF,
                )
                used_basic = True

            enemy_hps[target] -= damage

            for index, enemy_hp in enumerate(enemy_hps):
                if enemy_hp <= 0 or hp <= 0:
                    continue

                if skip_pending[index]:
                    skip_pending[index] = False
                    continue

                _, incoming = direct_hit(
                    rng,
                    enemy_precision,
                    PLAYER_EVA,
                    enemy_damage,
                    PLAYER_DEF,
                )
                hp -= float(incoming)

                if needs_normal_action[index]:
                    needs_normal_action[index] = False
                    eligible[index] = True

            if round_no > 100:
                raise RuntimeError("combate excedió 100 rondas")

        wins += int(
            all(value <= 0 for value in enemy_hps) and hp > 0
        )
        fallback += int(used_basic)
        rounds.append(round_no)
        hp_remaining.append(max(0.0, hp))

    return {
        "win_rate": wins / fights,
        "mean_rounds": statistics.fmean(rounds),
        "mean_hp_remaining_percent": (
            statistics.fmean(hp_remaining) / PLAYER_HP
        ),
        "fallback_rate": fallback / fights,
    }


def full_screen(fights: int, seed: int) -> list[dict]:
    rows = []
    serial = 0

    for t1, t2, t3 in itertools.product("RGE", repeat=3):
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
            "espejo_base_cost": 6,
            "one_or_two_efficiency_nodes_cost": 5,
            "full_EEE_cost": 4,
            "base_offenses_after_def": max(0, (qi - 6) // 6),
            "E_partial_offenses_after_def": max(0, (qi - 5) // 6),
            "EEE_offenses_after_def": max(0, (qi - 4) // 6),
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
    ap.add_argument("--csv", default="etapa12_espejo_luna_27_paths.csv")
    ap.add_argument("--qi-csv", default="etapa12_espejo_luna_qi_lattice.csv")
    args = ap.parse_args()

    rows = full_screen(args.fights, args.seed)
    export(rows, args.csv)
    export(qi_lattice(), args.qi_csv)

    print(f"CSV paths: {args.csv} ({len(rows)} escenarios)")
    print(f"CSV Qi: {args.qi_csv}")
