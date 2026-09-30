"""ETAPA 15A — Screen conjunto de las cinco defensivas BASE.

Objetivo:
comparar en un único runner las cinco bases ya recalibradas bajo los mismos
perfiles, usando las reglas actuales de raíz y ofensiva.

IMPORTANTE:
- no intenta igualar win rates entre raíces;
- compara cada defensiva contra la ofensiva de SU propia raíz;
- 2/3 enemigos son stress mecánico unitarget, no balance final de encuentros;
- Piel usa DEF_CAP2 PROVISIONAL, no la curva legacy;
- no modifica runtime.

Bases:
Fuego  Cuerpo-Horno: 25% HP Absorción /2t /7Qi
Metal  Armadura: 3 Placas, +3 DEF/Placa /4t /7Qi
Agua   Espejo: 24% HP Absorción / Reflujo25% /3t /7Qi nominal
Tierra Piel: DEF_CAP2 /3t /7Qi
Viento Paso: +35 EVA /4t /7Qi
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
from config_lianqi1_naked import BASIC_ATTACK_SELECTION

QI_MAX_LAB = 31
PLAYER_HP = 30.0
PLAYER_DEF = 1.0
PLAYER_EVA = 5.0

ENEMY_HP = 28
ENEMY_EVA = 20.0
ENEMY_DEF = 2.0

PROFILES = {
    "COMMON": (1, 90.0, "2d4+1"),
    "PRECISE": (1, 100.0, "2d4+1"),
    "HEAVY": (1, 90.0, "1d6+3"),
    "DANGEROUS": (1, 100.0, "1d6+3"),
    "2EN": (2, 90.0, "2d4+1"),
    "3EN": (3, 90.0, "2d4+1"),
}

OFFENSE = {
    "fuego": {"dice": "2d4+5", "cost": 6, "precision": 0, "crit": 0, "pen": 0},
    "metal": {"dice": "2d4+4", "cost": 6, "precision": 0, "crit": 0, "pen": 10},
    "agua": {"dice": "2d4+3", "cost": 7, "precision": 0, "crit": 0, "pen": 0},
    "tierra": {"dice": "2d4+4", "cost": 6, "precision": 0, "crit": 0, "pen": 0},
    "viento": {"dice": "2d4+3", "cost": 6, "precision": 5, "crit": 5, "pen": 0},
}

DEFENSIVE = {
    "fuego": {"cost": 7, "absorption_pct": 0.25, "duration": 2},
    "metal": {"cost": 7, "plates": 3, "plate_def": 3.0, "duration": 4},
    "agua": {"cost": 7, "absorption_pct": 0.24, "reflow": 0.25, "duration": 3},
    "tierra": {"cost": 7, "duration": 3},
    "viento": {"cost": 7, "evasion": 35.0, "duration": 4},
}

ARRASTRE_CHANCE = 0.50


def round_half_up(x: float) -> int:
    return int(math.floor(x + 0.5))


def effective_cost(root: str, base: float) -> int:
    if root == "agua":
        base *= 0.90
    return round_half_up(base)


def split_hp(total: int, count: int) -> list[float]:
    q, r = divmod(total, count)
    return [float(q + (1 if i < r else 0)) for i in range(count)]


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


def run_one(
    root: str,
    use_defensive: bool,
    enemy_count: int,
    enemy_precision: float,
    enemy_damage: str,
    fights: int,
    seed: int,
) -> dict:
    rng = random.Random(seed)
    p = player(root)
    tech = offense(root)
    basic_attack = basic()
    dcfg = DEFENSIVE[root]

    wins = 0
    rounds = []
    hp_remaining = []
    fallback = 0

    for _ in range(fights):
        hp = p.hp_max
        qi = QI_MAX_LAB
        enemy_hps = split_hp(ENEMY_HP, enemy_count)
        round_no = 0
        defense_used = False
        used_basic = False

        arrastre_eligible = [True] * enemy_count
        arrastre_skip = [False] * enemy_count
        arrastre_needs_action = [False] * enemy_count

        peso_stacks = [0] * enemy_count
        peso_duration = [0] * enemy_count

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

        while hp > 0 and any(value > 0 for value in enemy_hps):
            round_no += 1

            # TURN_START: Reflujo antes de DOT/acción.
            if root == "agua" and water_left > 0 and water_abs > 0:
                water_abs = min(
                    water_abs_max,
                    water_abs + dcfg["reflow"] * water_abs_max,
                )

            if use_defensive and not defense_used and round_no == 1:
                qi -= effective_cost(root, dcfg["cost"])
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
                target_index = next(
                    i for i, value in enumerate(enemy_hps) if value > 0
                )

                target_evasion = ENEMY_EVA
                if root == "tierra":
                    target_evasion -= 3.0 * peso_stacks[target_index]

                enemy_target = ActorStats(
                    hp_max=enemy_hps[target_index],
                    qi_max=0.0,
                    precision=enemy_precision,
                    evasion=target_evasion,
                    defense=ENEMY_DEF,
                    crit_chance=5.0,
                    crit_damage=1.50,
                )

                attack_cost = effective_cost(root, tech.qi_cost)

                if qi >= attack_cost:
                    result = resolve_direct_hit(rng, p, enemy_target, tech)
                    qi -= attack_cost

                    if (
                        root == "agua"
                        and result.hit
                        and arrastre_eligible[target_index]
                        and rng.random() < ARRASTRE_CHANCE
                    ):
                        arrastre_skip[target_index] = True
                        arrastre_eligible[target_index] = False
                        arrastre_needs_action[target_index] = True

                    if root == "tierra" and result.hit:
                        peso_stacks[target_index] = min(
                            2, peso_stacks[target_index] + 1
                        )
                        peso_duration[target_index] = 2
                else:
                    result = resolve_direct_hit(
                        rng, p, enemy_target, basic_attack
                    )
                    used_basic = True

                enemy_hps[target_index] -= result.damage_after_def

            for index, enemy_hp in enumerate(enemy_hps):
                if enemy_hp <= 0 or hp <= 0:
                    continue

                if root == "agua" and arrastre_skip[index]:
                    arrastre_skip[index] = False
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
                    # DEF_CAP2:
                    # Piel inmediata +2; Arraigo acumulado 1/2/2.
                    arraigo_def = {1: 1.0, 2: 2.0, 3: 2.0}[arraigo]
                    target_def += 2.0 + arraigo_def

                player_target = replace(
                    p,
                    evasion=target_evasion,
                    defense=target_def,
                )
                enemy_actor = ActorStats(
                    hp_max=enemy_hp,
                    qi_max=0.0,
                    precision=enemy_precision,
                    evasion=ENEMY_EVA,
                    defense=ENEMY_DEF,
                    crit_chance=5.0,
                    crit_damage=1.50,
                )
                enemy_attack = Technique(
                    "enemy_basic_lab", 0.0, Dice(enemy_damage)
                )

                incoming = resolve_direct_hit(
                    rng, enemy_actor, player_target, enemy_attack
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

                    old_arraigo = arraigo
                    arraigo = min(3, arraigo + gain)

                    if (
                        old_arraigo < 3
                        and arraigo == 3
                        and not piel_extended
                    ):
                        piel_left += 1
                        piel_extended = True

                if root == "agua" and arrastre_needs_action[index]:
                    arrastre_needs_action[index] = False
                    arrastre_eligible[index] = True

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

            for index in range(enemy_count):
                if peso_duration[index] > 0:
                    peso_duration[index] -= 1
                    if peso_duration[index] <= 0:
                        peso_stacks[index] = 0

            if round_no > 100:
                raise RuntimeError("combate excedió 100 rondas")

        wins += int(
            all(value <= 0 for value in enemy_hps) and hp > 0
        )
        fallback += int(used_basic)
        rounds.append(round_no)
        hp_remaining.append(max(0.0, hp))

    return {
        "provenance": "LAB",
        "root": root,
        "use_defensive": use_defensive,
        "enemy_count": enemy_count,
        "enemy_precision": enemy_precision,
        "enemy_damage": enemy_damage,
        "fights": fights,
        "win_rate": wins / fights,
        "mean_rounds": statistics.fmean(rounds),
        "mean_hp_remaining_percent": (
            statistics.fmean(hp_remaining) / p.hp_max
        ),
        "fallback_rate": fallback / fights,
    }


def run(fights: int, seed: int) -> list[dict]:
    rows = []
    serial = 0

    for profile, (count, precision, damage) in PROFILES.items():
        for root in ("fuego", "metal", "agua", "tierra", "viento"):
            for use_defensive in (False, True):
                rows.append(
                    {
                        "profile": profile,
                        **run_one(
                            root,
                            use_defensive,
                            count,
                            precision,
                            damage,
                            fights,
                            seed + serial,
                        ),
                    }
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
    ap.add_argument("--fights", type=int, default=10_000)
    ap.add_argument("--seed", type=int, default=20260929)
    ap.add_argument("--csv", default="etapa15a_defensivas_base.csv")
    args = ap.parse_args()

    rows = run(args.fights, args.seed)
    export(rows, args.csv)
    print(f"CSV: {args.csv} ({len(rows)} escenarios)")
