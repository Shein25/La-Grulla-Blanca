"""LAB — comparación de techo de impacto 95 vs 100.

Objetivo:
- comparar el contrato actual cap=100 contra un cap=95;
- barrer Precisión enemiga;
- comprobar cuánto valor real conserva Evasión/Viento.

No modifica sim_core.py ni el contrato. Todo es LAB.
"""
from __future__ import annotations

from dataclasses import replace
import argparse
import csv
import math
import random
import statistics

from sim_core import ActorStats, Dice, Technique, clamp, effective_def, round_half_up
from config_arc1_provisional import BASE_OFFENSIVE, ROOTS
from config_lianqi1_naked import (
    BASIC_ATTACK_SELECTION,
    DAMAGE_MODEL_SELECTION,
    LIANQI_I_REFERENCE_ENEMY,
    ROOT_TO_INITIAL_TECHNIQUE,
)

HIT_CAPS_LAB = (95.0, 100.0)
ENEMY_PRECISION_LAB = (80.0, 85.0, 90.0, 95.0, 100.0, 105.0)
PLAYER_BASE_EVASION_LAB = (0.0, 5.0, 10.0)

PLAYER_HP_LAB = 30.0
PLAYER_QI_LAB = 30
PLAYER_DEF_LAB = 1.0
ENEMY_HP_LAB = 28.0
ENEMY_DAMAGE_LAB = "2d4+1"


def hit_probability_cap(precision: float, evasion: float, cap: float, mod: float = 0.0) -> float:
    return clamp(precision + mod - evasion, 5.0, cap) / 100.0


def resolve_direct_hit_cap(
    rng: random.Random,
    attacker: ActorStats,
    target: ActorStats,
    technique: Technique,
    hit_cap: float,
):
    if technique.damage is None:
        return 0, False

    p = hit_probability_cap(
        attacker.precision,
        target.evasion,
        hit_cap,
        technique.precision_mod,
    )
    if rng.random() >= p:
        return 0, False

    rolled = technique.damage.roll(rng)
    modified = rolled * max(
        0.0,
        1.0 + (attacker.damage_done_percent + technique.damage_percent) / 100.0,
    )

    crit_chance = clamp(attacker.crit_chance + technique.crit_chance_mod, 0.0, 100.0)
    if rng.random() < crit_chance / 100.0:
        modified *= max(0.0, attacker.crit_damage + technique.crit_damage_mod)

    edef = effective_def(attacker, target, technique)
    return round_half_up(max(0.0, modified - edef)), True


def base_player(base_evasion: float) -> ActorStats:
    return ActorStats(
        hp_max=PLAYER_HP_LAB,
        qi_max=float(PLAYER_QI_LAB),
        precision=100.0,
        evasion=base_evasion,
        defense=PLAYER_DEF_LAB,
        crit_chance=5.0,
        crit_damage=1.50,
    )


def apply_root(stats: ActorStats, root: str) -> ActorStats:
    r = ROOTS[root]
    if root == "fuego":
        return replace(
            stats,
            damage_done_percent=stats.damage_done_percent + r["damage_direct_percent"],
            crit_chance=stats.crit_chance + r["crit_chance"],
        )
    if root == "metal":
        return replace(
            stats,
            percent_penetration=stats.percent_penetration + r["percent_penetration"],
            precision=stats.precision + r["precision"],
        )
    if root == "agua":
        return replace(stats, control=stats.control + r["control"])
    if root == "tierra":
        return replace(
            stats,
            hp_max=float(math.floor(stats.hp_max * 1.10 + 0.5)),
            tenacity=stats.tenacity + r["tenacity"],
        )
    if root == "viento":
        return replace(
            stats,
            evasion=stats.evasion + r["evasion"],
            crit_damage=stats.crit_damage + r["crit_damage"],
        )
    raise ValueError(root)


def enemy(precision: float) -> ActorStats:
    return ActorStats(
        hp_max=ENEMY_HP_LAB,
        qi_max=0.0,
        precision=precision,
        evasion=float(LIANQI_I_REFERENCE_ENEMY["evasion"].value),
        defense=float(LIANQI_I_REFERENCE_ENEMY["defense"].value),
        crit_chance=5.0,
        crit_damage=1.50,
    )


def technique(root: str) -> Technique:
    tech_id = ROOT_TO_INITIAL_TECHNIQUE[root]
    cfg = BASE_OFFENSIVE[tech_id]
    return Technique(
        name=tech_id,
        qi_cost=float(cfg["qi_cost"]),
        damage=Dice(str(DAMAGE_MODEL_SELECTION[tech_id].value)),
        precision_mod=float(cfg["precision"]),
        crit_chance_mod=float(cfg["crit_chance"]),
        percent_penetration=float(cfg["percent_penetration"]),
    )


def basic_attack() -> Technique:
    return Technique(
        name="ataque_basico",
        qi_cost=0.0,
        damage=Dice(str(BASIC_ATTACK_SELECTION.value)),
    )


def effective_cost(root: str, tech: Technique) -> int:
    reduction = float(ROOTS["agua"]["qi_cost_percent"]) if root == "agua" else 0.0
    decimal = tech.qi_cost * (1.0 + reduction / 100.0)
    return int(math.floor(decimal + 0.5))


def run_fights(
    root: str,
    base_evasion: float,
    enemy_precision: float,
    enemy_hit_cap: float,
    fights: int,
    seed: int,
) -> dict:
    rng = random.Random(seed)
    player = apply_root(base_player(base_evasion), root)
    foe = enemy(enemy_precision)
    tech = technique(root)
    basic = basic_attack()
    foe_attack = Technique(name="enemy_basic_lab", qi_cost=0.0, damage=Dice(ENEMY_DAMAGE_LAB))
    cost = effective_cost(root, tech)

    wins = 0
    enemy_attacks = 0
    enemy_hits = 0
    turns = []
    hp_remaining = []

    for _ in range(fights):
        p_hp = player.hp_max
        e_hp = foe.hp_max
        qi = PLAYER_QI_LAB
        n_turns = 0

        while p_hp > 0 and e_hp > 0:
            n_turns += 1

            if qi >= cost:
                damage, _ = resolve_direct_hit_cap(rng, player, foe, tech, 100.0)
                qi -= cost
            else:
                damage, _ = resolve_direct_hit_cap(rng, player, foe, basic, 100.0)

            e_hp -= damage
            if e_hp <= 0:
                break

            enemy_attacks += 1
            incoming, hit = resolve_direct_hit_cap(
                rng, foe, player, foe_attack, enemy_hit_cap
            )
            enemy_hits += int(hit)
            p_hp -= incoming

            if n_turns > 100:
                raise RuntimeError("duelo excedió 100 turnos")

        wins += int(e_hp <= 0 and p_hp > 0)
        turns.append(n_turns)
        hp_remaining.append(max(0.0, p_hp))

    return {
        "provenance": "LAB",
        "root": root,
        "base_evasion": base_evasion,
        "effective_evasion": player.evasion,
        "enemy_precision": enemy_precision,
        "enemy_hit_cap": enemy_hit_cap,
        "fights": fights,
        "enemy_hit_rate": enemy_hits / enemy_attacks if enemy_attacks else 0.0,
        "win_rate": wins / fights,
        "mean_turns": statistics.fmean(turns),
        "mean_hp_remaining_percent": statistics.fmean(hp_remaining) / player.hp_max,
    }


def run(fights: int, seed: int) -> list[dict]:
    rows = []
    serial = 0
    for base_evasion in PLAYER_BASE_EVASION_LAB:
        for hit_cap in HIT_CAPS_LAB:
            for enemy_precision in ENEMY_PRECISION_LAB:
                for root in ("fuego", "metal", "agua", "tierra", "viento"):
                    rows.append(
                        run_fights(
                            root,
                            base_evasion,
                            enemy_precision,
                            hit_cap,
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
    ap.add_argument("--fights", type=int, default=20_000)
    ap.add_argument("--seed", type=int, default=20260929)
    ap.add_argument("--csv", default="lianqi1_accuracy_cap_ab_lab.csv")
    args = ap.parse_args()
    rows = run(args.fights, args.seed)
    export(rows, args.csv)
    print(f"CSV: {args.csv} ({len(rows)} escenarios)")
