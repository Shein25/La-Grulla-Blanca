"""PHASE C LAB — screen de las cinco defensivas base LianQi I.

Baseline:
- Qi máximo LAB: 31 (candidato de economía mixta);
- enemigo HP28 / PREC90 / EVA20 / DEF2 / daño 2d4+1;
- jugador HP30 / DEF1 / EVA5 antes de raíz;
- jugador actúa primero;
- política defensiva: apertura.

Se comparan:
- sólo ofensiva;
- defensiva base actual.

Agua usa Arrastre PROVISIONAL (base_control65 vs Tenacidad20 = 50%).
Tierra usa Peso PROVISIONAL STACK_REFRESH.
"""
from __future__ import annotations

from dataclasses import replace
import argparse
import csv
import math
import random
import statistics

from sim_core import ActorStats, Dice, Technique, resolve_direct_hit
from config_arc1_provisional import ROOTS
from config_lianqi1_naked import BASIC_ATTACK_SELECTION, DAMAGE_MODEL_SELECTION

QI_MAX_LAB = 31
PLAYER_HP = 30.0
PLAYER_DEF = 1.0
PLAYER_EVA = 5.0

ENEMY_HP = 28.0
ENEMY_PREC = 90.0
ENEMY_EVA = 20.0
ENEMY_DEF = 2.0
ENEMY_DAMAGE = "2d4+1"

ARRASTRE_CHANCE = 0.50

DEFENSIVE_CURRENT = {
    "fuego": {"cost": 7, "absorption_pct": 0.15, "duration": 2},
    "metal": {"cost": 7, "plates": 3, "plate_def": 3.0, "duration": 4},
    "agua": {"cost": 7, "absorption_pct": 0.12, "reflow": 0.25, "duration": 3},
    "tierra": {"cost": 7, "duration": 3},
    "viento": {"cost": 7, "evasion": 15.0, "duration": 2},
}

OFFENSE = {
    "fuego": {"dice": "2d4+5", "cost": 6, "precision": 0, "crit": 0, "pen": 0},
    "metal": {"dice": "2d4+4", "cost": 6, "precision": 0, "crit": 0, "pen": 10},
    "agua": {"dice": "2d4+3", "cost": 7, "precision": 0, "crit": 0, "pen": 0},
    "tierra": {"dice": "2d4+4", "cost": 6, "precision": 0, "crit": 0, "pen": 0},
    "viento": {"dice": "2d4+3", "cost": 6, "precision": 5, "crit": 5, "pen": 0},
}


def round_half_up(x: float) -> int:
    return int(math.floor(x + 0.5))


def effective_cost(root: str, base: float) -> int:
    if root == "agua":
        base *= 0.90
    return round_half_up(base)


def player(root: str) -> ActorStats:
    hp = PLAYER_HP
    precision = 100.0
    evasion = PLAYER_EVA
    crit_chance = 5.0
    crit_damage = 1.50
    control = 0.0
    tenacity = 0.0
    damage_done = 0.0
    penetration = 0.0

    r = ROOTS[root]
    if root == "fuego":
        damage_done += r["damage_direct_percent"]
        crit_chance += r["crit_chance"]
    elif root == "metal":
        penetration += r["percent_penetration"]
        precision += r["precision"]
    elif root == "agua":
        control += r["control"]
    elif root == "tierra":
        hp = float(round_half_up(hp * 1.10))
        tenacity += r["tenacity"]
    elif root == "viento":
        evasion += r["evasion"]
        crit_damage += r["crit_damage"]

    return ActorStats(
        hp_max=hp,
        qi_max=QI_MAX_LAB,
        precision=precision,
        evasion=evasion,
        defense=PLAYER_DEF,
        crit_chance=crit_chance,
        crit_damage=crit_damage,
        control=control,
        tenacity=tenacity,
        percent_penetration=penetration,
        damage_done_percent=damage_done,
    )


def enemy() -> ActorStats:
    return ActorStats(
        hp_max=ENEMY_HP,
        qi_max=0.0,
        precision=ENEMY_PREC,
        evasion=ENEMY_EVA,
        defense=ENEMY_DEF,
        crit_chance=5.0,
        crit_damage=1.50,
    )


def offense(root: str) -> Technique:
    cfg = OFFENSE[root]
    return Technique(
        name=f"{root}_base_offense",
        qi_cost=float(cfg["cost"]),
        damage=Dice(cfg["dice"]),
        precision_mod=float(cfg["precision"]),
        crit_chance_mod=float(cfg["crit"]),
        percent_penetration=float(cfg["pen"]),
    )


def basic() -> Technique:
    return Technique("ataque_basico", 0.0, Dice(str(BASIC_ATTACK_SELECTION.value)))


def run_one(root: str, use_defensive: bool, fights: int, seed: int) -> dict:
    rng = random.Random(seed)
    p = player(root)
    e = enemy()
    tech = offense(root)
    basic_attack = basic()
    enemy_attack = Technique("enemy_basic_lab", 0.0, Dice(ENEMY_DAMAGE))
    dcfg = DEFENSIVE_CURRENT[root]

    wins = 0
    turns = []
    hp_remaining = []
    fallback = 0

    for _ in range(fights):
        hp = p.hp_max
        enemy_hp = e.hp_max
        qi = QI_MAX_LAB
        turn = 0
        defense_used = False
        used_basic = False
        arrastre_eligible = True

        peso_stacks = 0
        peso_duration = 0

        fire_abs = 0.0
        fire_left = 0

        metal_plates = 0
        metal_left = 0

        water_abs = 0.0
        water_abs_max = 0.0
        water_left = 0

        piel_active = False
        piel_left = 0
        arraigo = 0
        piel_large_used = False
        piel_extended = False

        wind_left = 0

        while hp > 0 and enemy_hp > 0:
            turn += 1

            if root == "agua" and water_left > 0 and water_abs > 0:
                water_abs = min(
                    water_abs_max,
                    water_abs + dcfg["reflow"] * water_abs_max,
                )

            if use_defensive and not defense_used and turn == 1:
                cost = effective_cost(root, dcfg["cost"])
                qi -= cost
                defense_used = True

                if root == "fuego":
                    fire_abs = dcfg["absorption_pct"] * p.hp_max
                    fire_left = dcfg["duration"]
                elif root == "metal":
                    metal_plates = dcfg["plates"]
                    metal_left = dcfg["duration"]
                elif root == "agua":
                    water_abs_max = dcfg["absorption_pct"] * p.hp_max
                    water_abs = water_abs_max
                    water_left = dcfg["duration"]
                elif root == "tierra":
                    piel_active = True
                    piel_left = dcfg["duration"]
                    arraigo = 1
                elif root == "viento":
                    wind_left = dcfg["duration"]
            else:
                dynamic_eva = e.evasion
                if root == "tierra":
                    dynamic_eva -= 3.0 * peso_stacks
                dynamic_enemy = replace(e, evasion=dynamic_eva)

                attack_cost = effective_cost(root, tech.qi_cost)
                skip_enemy = False

                if qi >= attack_cost:
                    result = resolve_direct_hit(rng, p, dynamic_enemy, tech)
                    qi -= attack_cost

                    if (
                        root == "agua"
                        and result.hit
                        and arrastre_eligible
                        and rng.random() < ARRASTRE_CHANCE
                    ):
                        skip_enemy = True
                        arrastre_eligible = False

                    if root == "tierra" and result.hit:
                        peso_stacks = min(2, peso_stacks + 1)
                        peso_duration = 2
                else:
                    result = resolve_direct_hit(rng, p, dynamic_enemy, basic_attack)
                    used_basic = True

                enemy_hp -= result.damage_after_def
                if enemy_hp <= 0:
                    break

                if skip_enemy:
                    if fire_left > 0:
                        fire_left -= 1
                    if metal_left > 0:
                        metal_left -= 1
                    if water_left > 0:
                        water_left -= 1
                    if piel_active and piel_left > 0:
                        piel_left -= 1
                    if wind_left > 0:
                        wind_left -= 1
                    if peso_duration > 0:
                        peso_duration -= 1
                        if peso_duration <= 0:
                            peso_stacks = 0
                    continue

            target_evasion = p.evasion + (
                dcfg.get("evasion", 0.0)
                if root == "viento" and wind_left > 0
                else 0.0
            )
            target_def = p.defense

            plate_active = (
                root == "metal"
                and metal_plates > 0
                and metal_left > 0
            )
            if plate_active:
                target_def += dcfg["plate_def"]

            if root == "tierra" and piel_active and piel_left > 0:
                target_def += 2.0 + arraigo

            incoming_target = replace(
                p,
                evasion=target_evasion,
                defense=target_def,
            )
            incoming = resolve_direct_hit(
                rng, e, incoming_target, enemy_attack
            )

            hp_damage = float(incoming.damage_after_def)

            if plate_active and incoming.hit:
                metal_plates -= 1

            if root == "fuego" and fire_left > 0 and fire_abs > 0:
                absorbed = min(fire_abs, hp_damage)
                fire_abs -= absorbed
                hp_damage -= absorbed

            if root == "agua" and water_left > 0 and water_abs > 0:
                absorbed = min(water_abs, hp_damage)
                water_abs -= absorbed
                hp_damage -= absorbed

            hp -= hp_damage

            if root == "agua" and not arrastre_eligible:
                arrastre_eligible = True

            if (
                root == "tierra"
                and piel_active
                and piel_left > 0
                and hp_damage > 0
            ):
                gain = 1
                if (
                    not piel_large_used
                    and hp_damage >= 0.10 * p.hp_max
                ):
                    gain = 2
                    piel_large_used = True

                old = arraigo
                arraigo = min(3, arraigo + gain)

                if old < 3 and arraigo == 3 and not piel_extended:
                    piel_left += 1
                    piel_extended = True

            if fire_left > 0:
                fire_left -= 1
                if fire_left <= 0:
                    fire_abs = 0.0

            if metal_left > 0:
                metal_left -= 1
                if metal_left <= 0:
                    metal_plates = 0

            if water_left > 0:
                water_left -= 1
                if water_left <= 0:
                    water_abs = 0.0

            if piel_active and piel_left > 0:
                piel_left -= 1
                if piel_left <= 0:
                    piel_active = False
                    arraigo = 0

            if wind_left > 0:
                wind_left -= 1

            if peso_duration > 0:
                peso_duration -= 1
                if peso_duration <= 0:
                    peso_stacks = 0

            if turn > 100:
                raise RuntimeError("duelo excedió 100 turnos")

        wins += int(enemy_hp <= 0 and hp > 0)
        fallback += int(used_basic)
        turns.append(turn)
        hp_remaining.append(max(0.0, hp))

    return {
        "provenance": "LAB",
        "root": root,
        "use_defensive": use_defensive,
        "qi_max": QI_MAX_LAB,
        "fights": fights,
        "win_rate": wins / fights,
        "mean_turns": statistics.fmean(turns),
        "mean_hp_remaining_percent": statistics.fmean(hp_remaining) / p.hp_max,
        "fallback_rate": fallback / fights,
    }


def run(fights: int, seed: int) -> list[dict]:
    rows = []
    serial = 0
    for root in ("fuego", "metal", "agua", "tierra", "viento"):
        for use_defensive in (False, True):
            rows.append(
                run_one(root, use_defensive, fights, seed + serial)
            )
            serial += 1
    return rows


def export(rows: list[dict], path: str) -> None:
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--fights", type=int, default=100_000)
    ap.add_argument("--seed", type=int, default=20260929)
    ap.add_argument("--csv", default="lianqi1_all_defensives_lab.csv")
    args = ap.parse_args()

    rows = run(args.fights, args.seed)
    export(rows, args.csv)
    for row in rows:
        print(row)
    print(f"CSV: {args.csv} ({len(rows)} escenarios)")
