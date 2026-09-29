"""PHASE C LAB — presión enemiga en duelo LianQi I.

Este runner introduce por primera vez respuesta enemiga, pero sigue siendo LAB:
- no usa utilidades de Agua/Tierra;
- no usa defensivas;
- no usa equipo, Concordancias, injerto ni Tramos;
- no fija todavía HP/DEF/Evasión del jugador ni daño enemigo.

Política:
jugador actúa primero;
usa técnica mientras alcance Qi;
después usa ataque básico;
enemigo responde con ataque directo simple si sigue vivo.
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

DUEL_MODES_LAB = {
    "COMPACT": {"enemy_hp": 20, "qi_max": 24},
    "EXTENDED": {"enemy_hp": 28, "qi_max": 30},
}

PLAYER_PROFILES_LAB = {
    "P24_D1_E0": {"hp": 24, "defense": 1, "evasion": 0},
    "P28_D1_E0": {"hp": 28, "defense": 1, "evasion": 0},
    "P28_D1_E10": {"hp": 28, "defense": 1, "evasion": 10},
    "P28_D2_E0": {"hp": 28, "defense": 2, "evasion": 0},
    "P30_D0_E0": {"hp": 30, "defense": 0, "evasion": 0},
    "P30_D0_E5": {"hp": 30, "defense": 0, "evasion": 5},
    "P30_D1_E0": {"hp": 30, "defense": 1, "evasion": 0},
    "P30_D1_E5": {"hp": 30, "defense": 1, "evasion": 5},
    "P30_D1_E10": {"hp": 30, "defense": 1, "evasion": 10},
}

ENEMY_PRECISION_LAB = 100.0
ENEMY_DAMAGE_MODELS_LAB = {
    "LOW_STABLE": "1d4+3",   # media 5.5
    "MID_BELL": "2d4+1",     # media 6.0
    "HIGH_MEDIUM": "1d6+3",  # media 6.5
}


def base_player(profile: dict[str, float], qi_max: int) -> ActorStats:
    return ActorStats(
        hp_max=float(profile["hp"]),
        qi_max=float(qi_max),
        precision=100.0,
        evasion=float(profile["evasion"]),
        defense=float(profile["defense"]),
        crit_chance=5.0,
        crit_damage=1.50,
        control=0.0,
        tenacity=0.0,
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
        return replace(stats, control=stats.control + r["control"])
    if root == "tierra":
        return replace(
            stats,
            hp_max=float(math.floor(stats.hp_max * (1.0 + r["hp_max_percent"] / 100.0) + 0.5)),
            tenacity=stats.tenacity + r["tenacity"],
        )
    if root == "viento":
        return replace(
            stats,
            evasion=stats.evasion + r["evasion"],
            crit_damage=stats.crit_damage + r["crit_damage"],
        )
    raise ValueError(root)


def enemy(enemy_hp: int, damage_model: str) -> tuple[ActorStats, Technique]:
    actor = ActorStats(
        hp_max=float(enemy_hp),
        qi_max=0.0,
        precision=ENEMY_PRECISION_LAB,
        evasion=float(LIANQI_I_REFERENCE_ENEMY["evasion"].value),
        defense=float(LIANQI_I_REFERENCE_ENEMY["defense"].value),
        crit_chance=5.0,
        crit_damage=1.50,
    )
    attack = Technique(
        name="enemy_basic_lab",
        qi_cost=0.0,
        damage=Dice(damage_model),
    )
    return actor, attack


def player_technique(root: str) -> Technique:
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


def effective_cost(root: str, technique: Technique) -> int:
    reduction = float(ROOTS["agua"]["qi_cost_percent"]) if root == "agua" else 0.0
    decimal = technique.qi_cost * (1.0 + reduction / 100.0)
    return int(math.floor(decimal + 0.5))


def run_fights(
    mode_id: str,
    profile_id: str,
    damage_id: str,
    root: str,
    fights: int,
    seed: int,
) -> dict:
    mode = DUEL_MODES_LAB[mode_id]
    profile = PLAYER_PROFILES_LAB[profile_id]

    player = apply_root(base_player(profile, mode["qi_max"]), root)
    foe, foe_attack = enemy(mode["enemy_hp"], ENEMY_DAMAGE_MODELS_LAB[damage_id])
    technique = player_technique(root)
    basic = basic_attack()
    cost = effective_cost(root, technique)

    rng = random.Random(seed)
    wins = 0
    turns = []
    hp_remaining = []
    basic_actions = []
    technique_actions = []

    for _ in range(fights):
        p_hp = player.hp_max
        e_hp = foe.hp_max
        qi = int(mode["qi_max"])
        n_turns = 0
        n_basic = 0
        n_technique = 0

        while p_hp > 0 and e_hp > 0:
            n_turns += 1

            if qi >= cost:
                result = resolve_direct_hit(rng, player, foe, technique)
                qi -= cost
                n_technique += 1
            else:
                result = resolve_direct_hit(rng, player, foe, basic)
                n_basic += 1

            e_hp -= result.damage_after_def
            if e_hp <= 0:
                break

            incoming = resolve_direct_hit(rng, foe, player, foe_attack)
            p_hp -= incoming.damage_after_def

            if n_turns > 100:
                raise RuntimeError("duelo excedió 100 turnos")

        wins += int(e_hp <= 0 and p_hp > 0)
        turns.append(n_turns)
        hp_remaining.append(max(0.0, p_hp))
        basic_actions.append(n_basic)
        technique_actions.append(n_technique)

    return {
        "provenance": "LAB",
        "mode": mode_id,
        "profile": profile_id,
        "root": root,
        "enemy_hp": mode["enemy_hp"],
        "qi_max": mode["qi_max"],
        "player_hp_effective": player.hp_max,
        "player_defense": player.defense,
        "player_evasion_effective": player.evasion,
        "enemy_precision": foe.precision,
        "enemy_damage_id": damage_id,
        "enemy_damage_dice": ENEMY_DAMAGE_MODELS_LAB[damage_id],
        "fights": fights,
        "win_rate": wins / fights,
        "mean_turns": statistics.fmean(turns),
        "mean_hp_remaining_percent": statistics.fmean(hp_remaining) / player.hp_max,
        "fallback_rate": sum(x > 0 for x in basic_actions) / fights,
        "mean_basic_actions": statistics.fmean(basic_actions),
        "mean_technique_actions": statistics.fmean(technique_actions),
    }


def run(fights: int, seed: int) -> list[dict]:
    rows = []
    serial = 0
    for mode_id in DUEL_MODES_LAB:
        for profile_id in PLAYER_PROFILES_LAB:
            for damage_id in ENEMY_DAMAGE_MODELS_LAB:
                for root in ("fuego", "metal", "agua", "tierra", "viento"):
                    rows.append(
                        run_fights(
                            mode_id,
                            profile_id,
                            damage_id,
                            root,
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
    ap.add_argument("--fights", type=int, default=10_000)
    ap.add_argument("--seed", type=int, default=20260929)
    ap.add_argument("--csv", default="lianqi1_phase_c_pressure_lab.csv")
    args = ap.parse_args()
    rows = run(args.fights, args.seed)
    export(rows, args.csv)
    print(f"CSV: {args.csv} ({len(rows)} escenarios)")
