"""LAB ofensivo — cruce HP enemigo × Qi máximo para LianQi I.

El objetivo es medir cuándo aparece el ataque básico por agotamiento de Qi.
El enemigo no actúa: esto NO es un duelo completo.

Todos los HP/Qi barridos son LAB.
"""
from __future__ import annotations

from dataclasses import replace
import argparse
import csv
import math
import random
import statistics

from sim_core import ActorStats, Dice, Technique, resolve_direct_hit
from config_arc1_provisional import BASE_OFFENSIVE, ROOTS
from config_lianqi1_naked import (
    BASIC_ATTACK_SELECTION,
    DAMAGE_MODEL_SELECTION,
    LIANQI_I_REFERENCE_ENEMY,
    ROOT_TO_INITIAL_TECHNIQUE,
)

QI_MAX_CANDIDATES_LAB = (24, 30)
ENEMY_HP_CANDIDATES_LAB = (20, 24, 28, 30, 32, 36)


def base_player() -> ActorStats:
    return ActorStats(
        hp_max=math.nan,
        qi_max=math.nan,
        precision=100.0,
        evasion=math.nan,
        defense=math.nan,
        crit_chance=5.0,
        crit_damage=1.50,
        control=math.nan,
        tenacity=math.nan,
        percent_penetration=0.0,
        flat_penetration=0.0,
        damage_done_percent=0.0,
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
        return replace(stats, control=r["control"])
    if root == "tierra":
        return stats
    if root == "viento":
        return replace(stats, crit_damage=stats.crit_damage + r["crit_damage"])
    raise ValueError(root)


def target(hp: float) -> ActorStats:
    return ActorStats(
        hp_max=hp,
        qi_max=math.nan,
        precision=math.nan,
        evasion=float(LIANQI_I_REFERENCE_ENEMY["evasion"].value),
        defense=float(LIANQI_I_REFERENCE_ENEMY["defense"].value),
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
    hp: int,
    qi_max: int,
    fights: int,
    seed: int,
) -> dict:
    rng = random.Random(seed)
    actor = apply_root(base_player(), root)
    tgt = target(float(hp))
    tech = technique(root)
    basic = basic_attack()
    cost = effective_cost(root, tech)

    turns: list[int] = []
    basic_actions: list[int] = []
    technique_actions: list[int] = []
    fallback_fights = 0

    for _ in range(fights):
        remaining_hp = float(hp)
        qi = int(qi_max)
        turn_count = 0
        n_basic = 0
        n_tech = 0

        while remaining_hp > 0:
            if qi >= cost:
                result = resolve_direct_hit(rng, actor, tgt, tech)
                qi -= cost
                n_tech += 1
            else:
                result = resolve_direct_hit(rng, actor, tgt, basic)
                n_basic += 1

            remaining_hp -= result.damage_after_def
            turn_count += 1

            if turn_count > 100:
                raise RuntimeError("fight exceeded 100 actions")

        turns.append(turn_count)
        basic_actions.append(n_basic)
        technique_actions.append(n_tech)
        fallback_fights += int(n_basic > 0)

    ordered = sorted(turns)
    p90 = ordered[int((len(ordered) - 1) * 0.90)]

    return {
        "provenance": "LAB",
        "root": root,
        "enemy_hp": hp,
        "qi_max": qi_max,
        "effective_technique_cost": cost,
        "fights": fights,
        "mean_turns": statistics.fmean(turns),
        "median_turns": statistics.median(turns),
        "p90_turns": p90,
        "fallback_rate": fallback_fights / fights,
        "mean_basic_actions": statistics.fmean(basic_actions),
        "mean_technique_actions": statistics.fmean(technique_actions),
    }


def run(fights: int, seed: int) -> list[dict]:
    rows: list[dict] = []
    serial = 0
    for qi_max in QI_MAX_CANDIDATES_LAB:
        for hp in ENEMY_HP_CANDIDATES_LAB:
            for root in ("fuego", "metal", "agua", "tierra", "viento"):
                rows.append(
                    run_fights(
                        root,
                        hp,
                        qi_max,
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
    ap.add_argument("--csv", default="lianqi1_hp_qi_offense_lab.csv")
    args = ap.parse_args()

    rows = run(args.fights, args.seed)
    export(rows, args.csv)
    print(f"CSV: {args.csv} ({len(rows)} escenarios)")
