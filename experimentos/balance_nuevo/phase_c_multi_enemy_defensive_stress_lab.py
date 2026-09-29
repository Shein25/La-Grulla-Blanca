"""PHASE C LAB — stress multi-enemigo real de defensivas.

A diferencia del stress anterior, aquí existen 2 o 3 enemigos con HP propio.
El HP total enemigo se mantiene aproximadamente en 28 para aislar el efecto de
recibir varias acciones enemigas por ronda.

El jugador usa su técnica inicial unitarget sobre el primer enemigo vivo.
No se usan AOE: éste es un stress de supervivencia/acción, no balance de grupo
final.

Candidatos LAB:
- Qi31
- Fuego Horno 25%
- Agua Espejo 24%
- Viento Paso +35 EVA / 4 turnos
- Metal/Tierra actuales
"""
from __future__ import annotations

from dataclasses import replace
import argparse
import csv
import math
import random
import statistics

import phase_c_all_defensives_lab as base


QI_MAX_LAB = 31

SELECTED_DEFENSIVES_LAB = {
    "fuego": {"absorption_pct": 0.25, "duration": 2},
    "metal": {"plates": 3, "plate_def": 3.0, "duration": 4},
    "agua": {"absorption_pct": 0.24, "reflow": 0.25, "duration": 3},
    "tierra": {"duration": 3},
    "viento": {"evasion": 35.0, "duration": 4},
}


def split_hp(total_hp: int, enemies: int) -> list[float]:
    q, r = divmod(total_hp, enemies)
    return [float(q + (1 if i < r else 0)) for i in range(enemies)]


def run_one(
    root: str,
    use_defensive: bool,
    enemy_count: int,
    fights: int,
    seed: int,
) -> dict:
    rng = random.Random(seed)

    old_qi = base.QI_MAX_LAB
    base.QI_MAX_LAB = QI_MAX_LAB
    for key, value in SELECTED_DEFENSIVES_LAB[root].items():
        base.DEFENSIVE_CURRENT[root][key] = value

    p = base.player(root)
    offense = base.offense(root)
    basic_attack = base.basic()
    defensive = base.DEFENSIVE_CURRENT[root]

    wins = 0
    rounds = []
    hp_remaining = []
    fallback = 0

    for _ in range(fights):
        hp = p.hp_max
        qi = QI_MAX_LAB
        enemy_hps = split_hp(int(base.ENEMY_HP), enemy_count)
        round_no = 0
        defense_used = False
        used_basic = False

        arrastre_eligible = [True] * enemy_count
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

            if root == "agua" and water_left > 0 and water_abs > 0:
                water_abs = min(
                    water_abs_max,
                    water_abs + defensive["reflow"] * water_abs_max,
                )

            if use_defensive and not defense_used and round_no == 1:
                dcost = base.effective_cost(root, defensive["cost"])
                qi -= dcost
                defense_used = True

                if root == "fuego":
                    fire_abs = defensive["absorption_pct"] * p.hp_max
                    fire_left = defensive["duration"]
                elif root == "metal":
                    metal_plates = defensive["plates"]
                    metal_left = defensive["duration"]
                elif root == "agua":
                    water_abs_max = defensive["absorption_pct"] * p.hp_max
                    water_abs = water_abs_max
                    water_left = defensive["duration"]
                elif root == "tierra":
                    piel_active = True
                    piel_left = defensive["duration"]
                    arraigo = 1
                elif root == "viento":
                    wind_left = defensive["duration"]
            else:
                target_index = next(
                    i for i, value in enumerate(enemy_hps) if value > 0
                )

                dynamic_evasion = base.ENEMY_EVA
                if root == "tierra":
                    dynamic_evasion -= 3.0 * peso_stacks[target_index]

                target = base.ActorStats(
                    hp_max=enemy_hps[target_index],
                    qi_max=0.0,
                    precision=base.ENEMY_PREC,
                    evasion=dynamic_evasion,
                    defense=base.ENEMY_DEF,
                    crit_chance=5.0,
                    crit_damage=1.50,
                )

                attack_cost = base.effective_cost(root, offense.qi_cost)

                if qi >= attack_cost:
                    result = base.resolve_direct_hit(rng, p, target, offense)
                    qi -= attack_cost

                    if (
                        root == "agua"
                        and result.hit
                        and arrastre_eligible[target_index]
                        and rng.random() < base.ARRASTRE_CHANCE
                    ):
                        arrastre_eligible[target_index] = False

                    if root == "tierra" and result.hit:
                        peso_stacks[target_index] = min(
                            2, peso_stacks[target_index] + 1
                        )
                        peso_duration[target_index] = 2
                else:
                    result = base.resolve_direct_hit(
                        rng, p, target, basic_attack
                    )
                    used_basic = True

                enemy_hps[target_index] -= result.damage_after_def

            # Cada enemigo vivo resuelve su propia acción.
            for index, enemy_hp in enumerate(enemy_hps):
                if enemy_hp <= 0 or hp <= 0:
                    continue

                if root == "agua" and not arrastre_eligible[index]:
                    arrastre_eligible[index] = True
                    continue

                target_evasion = p.evasion + (
                    defensive.get("evasion", 0.0)
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
                    target_def += defensive["plate_def"]

                if root == "tierra" and piel_active and piel_left > 0:
                    target_def += 2.0 + arraigo

                target_player = replace(
                    p,
                    evasion=target_evasion,
                    defense=target_def,
                )

                enemy_actor = base.ActorStats(
                    hp_max=enemy_hp,
                    qi_max=0.0,
                    precision=base.ENEMY_PREC,
                    evasion=base.ENEMY_EVA,
                    defense=base.ENEMY_DEF,
                    crit_chance=5.0,
                    crit_damage=1.50,
                )
                enemy_attack = base.Technique(
                    "enemy_basic_lab",
                    0.0,
                    base.Dice(base.ENEMY_DAMAGE),
                )

                incoming = base.resolve_direct_hit(
                    rng, enemy_actor, target_player, enemy_attack
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

            # Duraciones por turno/ronda del propietario, no por cada impacto.
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

        wins += int(all(value <= 0 for value in enemy_hps) and hp > 0)
        fallback += int(used_basic)
        rounds.append(round_no)
        hp_remaining.append(max(0.0, hp))

    base.QI_MAX_LAB = old_qi

    return {
        "provenance": "LAB",
        "root": root,
        "use_defensive": use_defensive,
        "enemy_count": enemy_count,
        "enemy_total_hp": int(base.ENEMY_HP),
        "qi_max": QI_MAX_LAB,
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

    for enemy_count in (1, 2, 3):
        for root in ("fuego", "metal", "agua", "tierra", "viento"):
            for use_defensive in (False, True):
                rows.append(
                    run_one(
                        root,
                        use_defensive,
                        enemy_count,
                        fights,
                        seed + serial,
                    )
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
    ap.add_argument("--fights", type=int, default=50_000)
    ap.add_argument("--seed", type=int, default=20260929)
    ap.add_argument("--csv", default="lianqi1_multi_enemy_defensive_stress_lab.csv")
    args = ap.parse_args()

    rows = run(args.fights, args.seed)
    export(rows, args.csv)
    print(f"CSV: {args.csv} ({len(rows)} escenarios)")
