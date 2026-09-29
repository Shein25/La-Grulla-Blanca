"""Laboratorio exploratorio PHASE A: ataque básico vs técnicas de LianQi I.

Todos los números de este archivo son LAB. No fija valores CANON/PROVISIONAL.
No usa estadísticas legacy.

Objetivo:
- encontrar una zona útil para el ataque básico de coste 0 Qi;
- medir el premium de las cinco técnicas iniciales;
- observar cuándo la DEF plana empieza a anular el fallback sin Qi.

Por defecto valida dos puntos centrales de sensibilidad:
  EVA 20 / DEF 2
  EVA 20 / DEF 3

Use --full-grid para barrer EVA 0..40 y DEF 0..6.
"""
from __future__ import annotations

from dataclasses import replace
import argparse
import csv
import math

from sim_core import ActorStats, Dice, Technique, as_dict, monte_carlo_hit
from config_arc1_provisional import BASE_OFFENSIVE, DICE_CANDIDATES_LAB, ROOTS


BASIC_ATTACK_CANDIDATES_LAB = {
    "B5_NARROW": "2d4",       # media 5.0
    "B6_NARROW": "2d4+1",     # media 6.0
    "B6_5_NARROW": "3d4-1",   # media 6.5
    "B7_NARROW": "2d4+2",     # media 7.0
}

CENTRAL_TARGETS_LAB = [
    ("E20_D2", 20.0, 2.0),
    ("E20_D3", 20.0, 3.0),
]


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


def target(evasion: float, defense: float) -> ActorStats:
    return ActorStats(
        hp_max=math.nan,
        qi_max=math.nan,
        precision=math.nan,
        evasion=evasion,
        defense=defense,
    )


def technique(root: str, variant: str) -> Technique:
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


def basic_attack(model: str) -> Technique:
    return Technique(
        name="ataque_basico",
        qi_cost=0.0,
        damage=Dice(BASIC_ATTACK_CANDIDATES_LAB[model]),
    )


def target_grid(full: bool):
    if not full:
        return CENTRAL_TARGETS_LAB
    return [
        (f"E{e}_D{d}", float(e), float(d))
        for e in (0, 10, 20, 30, 40)
        for d in range(0, 7)
    ]


def run(iterations: int, seed: int, full: bool) -> list[dict]:
    rows = []
    serial = 0
    for target_id, evasion, defense in target_grid(full):
        tgt = target(evasion, defense)
        for root in ("fuego", "metal", "agua", "tierra", "viento"):
            actor = apply_root(base_player(), root)

            for variant in ("narrow", "wide"):
                t = technique(root, variant)
                summary = monte_carlo_hit(
                    actor, tgt, t,
                    iterations=iterations,
                    seed=seed + serial,
                )
                serial += 1
                rows.append({
                    "provenance": "LAB",
                    "target": target_id,
                    "enemy_evasion": evasion,
                    "enemy_defense": defense,
                    "root": root,
                    "action": "TECHNIQUE",
                    "model": variant,
                    "dice": t.damage.notation,
                    **as_dict(summary),
                })

            for model in BASIC_ATTACK_CANDIDATES_LAB:
                t = basic_attack(model)
                summary = monte_carlo_hit(
                    actor, tgt, t,
                    iterations=iterations,
                    seed=seed + serial,
                )
                serial += 1
                rows.append({
                    "provenance": "LAB",
                    "target": target_id,
                    "enemy_evasion": evasion,
                    "enemy_defense": defense,
                    "root": root,
                    "action": "BASIC",
                    "model": model,
                    "dice": t.damage.notation,
                    **as_dict(summary),
                })
    return rows


def export(rows: list[dict], path: str) -> None:
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def print_central_premium(rows: list[dict]) -> None:
    print("target,root,basic_model,basic_mean,tech_narrow_mean,technique_premium,zero_action,zero_on_hit")
    for target_id, _, _ in CENTRAL_TARGETS_LAB:
        for root in ("fuego", "metal", "agua", "tierra", "viento"):
            tech = next(
                r for r in rows
                if r["target"] == target_id
                and r["root"] == root
                and r["action"] == "TECHNIQUE"
                and r["model"] == "narrow"
            )
            for model in BASIC_ATTACK_CANDIDATES_LAB:
                basic = next(
                    r for r in rows
                    if r["target"] == target_id
                    and r["root"] == root
                    and r["action"] == "BASIC"
                    and r["model"] == model
                )
                premium = tech["mean_damage_after_def"] / basic["mean_damage_after_def"]
                print(
                    f'{target_id},{root},{model},'
                    f'{basic["mean_damage_after_def"]:.4f},'
                    f'{tech["mean_damage_after_def"]:.4f},'
                    f'{premium:.4f},'
                    f'{basic["zero_damage_rate_per_action"]:.4f},'
                    f'{basic["zero_damage_rate_on_hit"]:.4f}'
                )


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--iterations", type=int, default=100_000)
    ap.add_argument("--seed", type=int, default=20260929)
    ap.add_argument("--full-grid", action="store_true")
    ap.add_argument("--csv", default="lianqi1_basic_attack_lab.csv")
    args = ap.parse_args()

    rows = run(args.iterations, args.seed, args.full_grid)
    export(rows, args.csv)
    if not args.full_grid:
        print_central_premium(rows)
    print(f"CSV: {args.csv} ({len(rows)} escenarios)")
