"""PHASE C LAB — defensivas base de Agua y Tierra.

Objetivo:
- comprobar si Espejo de Luna y Piel de Cobre justifican gastar un turno;
- identificar sensibilidad a magnitud/coste sin canonizar números.

Baseline LAB:
jugador HP30 / Qi30 / DEF1 / EVA5;
enemigo HP28 / PREC90 / EVA20 / DEF2 / 2d4+1;
Arrastre efectivo 50%;
Peso STACK_REFRESH.

Políticas:
- OFFENSE_ONLY
- DEFENSE_OPENING
- DEFENSE_REACTIVE_50

Guardias:
- no modifica runtime;
- no modifica contratos;
- no toca equipo/Concordancias/injerto/Tramos.
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

PLAYER_HP_LAB = 30.0
PLAYER_QI_LAB = 30
PLAYER_DEF_LAB = 1.0
PLAYER_EVASION_LAB = 5.0

ENEMY_HP_LAB = 28.0
ENEMY_PRECISION_LAB = 90.0
ENEMY_EVASION_LAB = 20.0
ENEMY_DEF_LAB = 2.0
ENEMY_DAMAGE_LAB = "2d4+1"

ARRASTRE_EFFECTIVE_LAB = 0.50
PESO_STACKING_LAB = "STACK_REFRESH"

MIRROR_ABSORPTION_PCT_LAB = (0.12, 0.17, 0.20, 0.21, 0.22, 0.23, 0.24, 0.25, 0.30)
MIRROR_REFLOW_LAB = 0.25
MIRROR_BASE_COST = 7.0

PIEL_COST_CANDIDATES_LAB = (6, 7)
POLICIES = ("OFFENSE_ONLY", "DEFENSE_OPENING", "DEFENSE_REACTIVE_50")


def round_half_up(x: float) -> int:
    return int(math.floor(x + 0.5))


def base_player(root: str) -> ActorStats:
    hp = PLAYER_HP_LAB
    evasion = PLAYER_EVASION_LAB
    tenacity = 0.0
    control = 0.0

    if root == "tierra":
        hp = float(round_half_up(hp * 1.10))
        tenacity += ROOTS["tierra"]["tenacity"]
    elif root == "viento":
        evasion += ROOTS["viento"]["evasion"]
    elif root == "agua":
        control += ROOTS["agua"]["control"]

    return ActorStats(
        hp_max=hp,
        qi_max=PLAYER_QI_LAB,
        precision=100.0,
        evasion=evasion,
        defense=PLAYER_DEF_LAB,
        crit_chance=5.0,
        crit_damage=1.50,
        control=control,
        tenacity=tenacity,
    )


def foe() -> ActorStats:
    return ActorStats(
        hp_max=ENEMY_HP_LAB,
        qi_max=0.0,
        precision=ENEMY_PRECISION_LAB,
        evasion=ENEMY_EVASION_LAB,
        defense=ENEMY_DEF_LAB,
        crit_chance=5.0,
        crit_damage=1.50,
    )


def basic() -> Technique:
    return Technique("ataque_basico", 0.0, Dice(str(BASIC_ATTACK_SELECTION.value)))


def water_attack() -> Technique:
    return Technique(
        "latigazo_marea",
        7.0,
        Dice(str(DAMAGE_MODEL_SELECTION["latigazo_marea"].value)),
    )


def earth_attack() -> Technique:
    return Technique(
        "golpe_montana",
        6.0,
        Dice(str(DAMAGE_MODEL_SELECTION["golpe_montana"].value)),
    )


def effective_water_cost(base_cost: float) -> int:
    return round_half_up(base_cost * 0.90)


def should_defend(policy: str, turn: int, hp: float, hp_max: float, used: bool) -> bool:
    if used or policy == "OFFENSE_ONLY":
        return False
    if policy == "DEFENSE_OPENING":
        return turn == 1
    if policy == "DEFENSE_REACTIVE_50":
        return hp <= hp_max * 0.50
    raise ValueError(policy)


def run_water(
    mirror_pct: float,
    policy: str,
    fights: int,
    seed: int,
) -> dict:
    rng = random.Random(seed)
    player = base_player("agua")
    enemy = foe()
    tech = water_attack()
    basic_attack = basic()
    enemy_attack = Technique("enemy_basic_lab", 0.0, Dice(ENEMY_DAMAGE_LAB))

    wins = 0
    turns = []
    hp_remaining = []
    fallback = 0
    mirror_use = 0
    absorbed_total = []

    for _ in range(fights):
        hp = player.hp_max
        enemy_hp = enemy.hp_max
        qi = PLAYER_QI_LAB
        turn = 0
        mirror_used = False
        used_basic = False

        arrastre_eligible = True

        shield = 0.0
        shield_max = 0.0
        shield_responses_left = 0
        absorbed_this_fight = 0.0

        while hp > 0 and enemy_hp > 0:
            turn += 1

            if shield_responses_left > 0 and shield > 0:
                shield = min(
                    shield_max,
                    shield + MIRROR_REFLOW_LAB * shield_max,
                )

            use_mirror = should_defend(
                policy, turn, hp, player.hp_max, mirror_used
            )

            skip_enemy = False

            if use_mirror and qi >= effective_water_cost(MIRROR_BASE_COST):
                qi -= effective_water_cost(MIRROR_BASE_COST)
                mirror_used = True
                mirror_use += 1
                shield_max = mirror_pct * player.hp_max
                shield = shield_max
                shield_responses_left = 3
            else:
                if qi >= effective_water_cost(tech.qi_cost):
                    result = resolve_direct_hit(rng, player, enemy, tech)
                    qi -= effective_water_cost(tech.qi_cost)

                    if (
                        result.hit
                        and arrastre_eligible
                        and rng.random() < ARRASTRE_EFFECTIVE_LAB
                    ):
                        skip_enemy = True
                        arrastre_eligible = False
                else:
                    result = resolve_direct_hit(rng, player, enemy, basic_attack)
                    used_basic = True

                enemy_hp -= result.damage_after_def
                if enemy_hp <= 0:
                    break

            if not skip_enemy:
                incoming = resolve_direct_hit(rng, enemy, player, enemy_attack)
                hp_damage = float(incoming.damage_after_def)

                if shield_responses_left > 0 and shield > 0:
                    absorbed = min(shield, hp_damage)
                    shield -= absorbed
                    hp_damage -= absorbed
                    absorbed_this_fight += absorbed
                    if shield <= 0:
                        shield = 0.0

                hp -= hp_damage

                if not arrastre_eligible:
                    arrastre_eligible = True

            if shield_responses_left > 0:
                shield_responses_left -= 1
                if shield_responses_left <= 0:
                    shield = 0.0

            if turn > 100:
                raise RuntimeError("duelo excedió 100 turnos")

        wins += int(enemy_hp <= 0 and hp > 0)
        fallback += int(used_basic)
        turns.append(turn)
        hp_remaining.append(max(0.0, hp))
        absorbed_total.append(absorbed_this_fight)

    return {
        "provenance": "LAB",
        "root": "agua",
        "policy": policy,
        "mirror_absorption_pct": mirror_pct,
        "mirror_effective_cost": effective_water_cost(MIRROR_BASE_COST),
        "fights": fights,
        "win_rate": wins / fights,
        "mean_turns": statistics.fmean(turns),
        "mean_hp_remaining_percent": statistics.fmean(hp_remaining) / player.hp_max,
        "fallback_rate": fallback / fights,
        "defense_use_rate": mirror_use / fights,
        "mean_absorbed": statistics.fmean(absorbed_total),
    }


def run_earth(
    piel_cost: int,
    policy: str,
    fights: int,
    seed: int,
) -> dict:
    rng = random.Random(seed)
    player = base_player("tierra")
    enemy = foe()
    tech = earth_attack()
    basic_attack = basic()
    enemy_attack = Technique("enemy_basic_lab", 0.0, Dice(ENEMY_DAMAGE_LAB))

    wins = 0
    turns = []
    hp_remaining = []
    fallback = 0
    piel_use = 0

    for _ in range(fights):
        hp = player.hp_max
        enemy_hp = enemy.hp_max
        qi = PLAYER_QI_LAB
        turn = 0
        piel_used = False
        used_basic = False

        peso_stacks = 0
        peso_duration = 0

        piel_active = False
        piel_responses_left = 0
        arraigo = 0
        large_trigger_used = False
        max_extension_used = False

        while hp > 0 and enemy_hp > 0:
            turn += 1

            use_piel = should_defend(
                policy, turn, hp, player.hp_max, piel_used
            )

            if use_piel and qi >= piel_cost:
                qi -= piel_cost
                piel_used = True
                piel_use += 1
                piel_active = True
                piel_responses_left = 3
                arraigo = 1
                large_trigger_used = False
                max_extension_used = False
            else:
                dynamic_enemy = replace(
                    enemy,
                    evasion=ENEMY_EVASION_LAB - 3.0 * peso_stacks,
                )

                if qi >= int(tech.qi_cost):
                    result = resolve_direct_hit(rng, player, dynamic_enemy, tech)
                    qi -= int(tech.qi_cost)

                    if result.hit:
                        peso_stacks = min(2, peso_stacks + 1)
                        peso_duration = 2
                else:
                    result = resolve_direct_hit(
                        rng, player, dynamic_enemy, basic_attack
                    )
                    used_basic = True

                enemy_hp -= result.damage_after_def
                if enemy_hp <= 0:
                    break

            current_def = player.defense
            if piel_active and piel_responses_left > 0:
                current_def += 2.0 + arraigo

            incoming_target = replace(player, defense=current_def)
            incoming = resolve_direct_hit(
                rng, enemy, incoming_target, enemy_attack
            )
            hp_damage = float(incoming.damage_after_def)
            hp -= hp_damage

            if (
                piel_active
                and piel_responses_left > 0
                and hp_damage > 0
            ):
                gain = 1
                threshold = 0.10 * player.hp_max

                if (
                    not large_trigger_used
                    and hp_damage >= threshold
                ):
                    gain = 2
                    large_trigger_used = True

                old_arraigo = arraigo
                arraigo = min(3, arraigo + gain)

                if (
                    old_arraigo < 3
                    and arraigo == 3
                    and not max_extension_used
                ):
                    piel_responses_left += 1
                    max_extension_used = True

            if piel_active and piel_responses_left > 0:
                piel_responses_left -= 1
                if piel_responses_left <= 0:
                    piel_active = False
                    arraigo = 0

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
        "root": "tierra",
        "policy": policy,
        "piel_cost": piel_cost,
        "fights": fights,
        "win_rate": wins / fights,
        "mean_turns": statistics.fmean(turns),
        "mean_hp_remaining_percent": statistics.fmean(hp_remaining) / player.hp_max,
        "fallback_rate": fallback / fights,
        "defense_use_rate": piel_use / fights,
    }


def run(fights: int, seed: int) -> list[dict]:
    rows: list[dict] = []
    serial = 0

    for pct in MIRROR_ABSORPTION_PCT_LAB:
        for policy in POLICIES:
            rows.append(run_water(pct, policy, fights, seed + serial))
            serial += 1

    for cost in PIEL_COST_CANDIDATES_LAB:
        for policy in POLICIES:
            rows.append(run_earth(cost, policy, fights, seed + serial))
            serial += 1

    return rows


def export(rows: list[dict], path: str) -> None:
    fields = sorted({key for row in rows for key in row})
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--fights", type=int, default=100_000)
    ap.add_argument("--seed", type=int, default=20260929)
    ap.add_argument("--csv", default="lianqi1_defensives_lab.csv")
    args = ap.parse_args()

    rows = run(args.fights, args.seed)
    export(rows, args.csv)
    print(f"CSV: {args.csv} ({len(rows)} escenarios)")
