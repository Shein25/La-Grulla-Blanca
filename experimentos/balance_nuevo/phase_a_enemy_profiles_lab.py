"""PHASE A LAB — perfiles abstractos de resistencia LianQi I.

Todos los valores son LAB. No representan criaturas concretas ni fijan CANON.
Compara:
- ataque básico candidato 1d4+4;
- cinco técnicas iniciales;
- dados narrow/wide actuales;
- cuatro perfiles abstractos Evasión/DEF.

No usa HP, Qi máximo, daño enemigo, equipo, Concordancias ni Tramos.
"""
from __future__ import annotations

from dataclasses import replace
import argparse
import csv
import math

from sim_core import ActorStats, Dice, Technique, as_dict, monte_carlo_hit
from config_arc1_provisional import BASE_OFFENSIVE, DICE_CANDIDATES_LAB, ROOTS

PROFILES_LAB = {
    "L1_SOFT": {"evasion": 10.0, "defense": 1.0},
    "L1_STANDARD": {"evasion": 20.0, "defense": 2.0},
    "L1_ARMORED": {"evasion": 20.0, "defense": 4.0},
    "L1_EVASIVE": {"evasion": 35.0, "defense": 2.0},
}

BASIC_ATTACK_LAB = "1d4+4"


def base_player() -> ActorStats:
    return ActorStats(
        hp_max=math.nan,
        qi_max=math.nan,
        precision=100.0,
        evasion=math.nan,
        defense=math.nan,
        crit_chance=5.0,
        crit_damage=1.50,
        percent_penetration=0.0,
        flat_penetration=0.0,
        control=math.nan,
        tenacity=math.nan,
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


def target(profile: dict[str, float]) -> ActorStats:
    return ActorStats(
        hp_max=math.nan,
        qi_max=math.nan,
        precision=math.nan,
        evasion=profile["evasion"],
        defense=profile["defense"],
    )


def build_technique(root: str, variant: str) -> Technique:
    tech_id = {
        "fuego": "palma_ardiente",
        "metal": "destello_plata",
        "agua": "latigazo_marea",
        "tierra": "golpe_montana",
        "viento": "lanza_nubes",
    }[root]
    cfg = BASE_OFFENSIVE[tech_id]
    notation = DICE_CANDIDATES_LAB[cfg["nominal_damage"]][variant]
    return Technique(
        name=tech_id,
        qi_cost=float(cfg["qi_cost"]),
        damage=Dice(notation),
        precision_mod=float(cfg["precision"]),
        crit_chance_mod=float(cfg["crit_chance"]),
        percent_penetration=float(cfg["percent_penetration"]),
    )


def build_basic() -> Technique:
    return Technique(name="ataque_basico", qi_cost=0.0, damage=Dice(BASIC_ATTACK_LAB))


def run(iterations: int, seed: int) -> list[dict]:
    rows: list[dict] = []
    serial = 0
    for profile_id, profile in PROFILES_LAB.items():
        tgt = target(profile)
        for root in ("fuego", "metal", "agua", "tierra", "viento"):
            actor = apply_root(base_player(), root)
            basic = build_basic()
            basic_summary = monte_carlo_hit(
                actor, tgt, basic, iterations=iterations, seed=seed + serial
            )
            serial += 1
            rows.append({
                "provenance": "LAB",
                "profile": profile_id,
                "enemy_evasion": profile["evasion"],
                "enemy_defense": profile["defense"],
                "root": root,
                "action": "BASIC",
                "model": "B6_5_STABLE",
                "dice": BASIC_ATTACK_LAB,
                **as_dict(basic_summary),
            })

            for variant in ("narrow", "wide"):
                tech = build_technique(root, variant)
                summary = monte_carlo_hit(
                    actor, tgt, tech, iterations=iterations, seed=seed + serial
                )
                serial += 1
                rows.append({
                    "provenance": "LAB",
                    "profile": profile_id,
                    "enemy_evasion": profile["evasion"],
                    "enemy_defense": profile["defense"],
                    "root": root,
                    "action": "TECHNIQUE",
                    "model": variant,
                    "dice": tech.damage.notation,
                    **as_dict(summary),
                })
    return rows


def export(rows: list[dict], path: str) -> None:
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--iterations", type=int, default=200_000)
    ap.add_argument("--seed", type=int, default=20260929)
    ap.add_argument("--csv", default="lianqi1_phase_a_enemy_profiles_lab.csv")
    args = ap.parse_args()
    rows = run(args.iterations, args.seed)
    export(rows, args.csv)
    print(f"CSV: {args.csv} ({len(rows)} escenarios)")
