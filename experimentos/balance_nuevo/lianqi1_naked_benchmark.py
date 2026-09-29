"""Runner por fases para LianQi I NAKED.

No fija números pendientes. Cada fase se niega a ejecutar si le falta una
magnitud explícita del sistema nuevo.
"""
from __future__ import annotations

from dataclasses import replace
import math

from sim_core import ActorStats, Dice, Technique, round_half_up
from run_matrix import Scenario, run_matrix
from config_arc1_provisional import BASE_OFFENSIVE, ROOTS
from config_lianqi1_naked import (
    PLAYER_BASE,
    QI_COST_FLOOR,
    ROOT_TO_INITIAL_TECHNIQUE,
    DAMAGE_MODEL_SELECTION,
    LIANQI_I_REFERENCE_ENEMY,
    ARRASTRE_BASE_CONTROL,
    Parameter,
)


def _value(param: Parameter, name: str):
    if not param.ready:
        raise ValueError(
            f"{name}: parámetro {param.provenance}; defínalo explícitamente "
            f"antes de ejecutar esta fase. Fuente: {param.source}"
        )
    return param.value


def readiness_report() -> dict:
    phase_a = []
    for key in ("evasion", "defense"):
        if not LIANQI_I_REFERENCE_ENEMY[key].ready:
            phase_a.append(f"enemy.{key}")
    for tech_id, p in DAMAGE_MODEL_SELECTION.items():
        if not p.ready:
            phase_a.append(f"damage_model.{tech_id}")

    phase_b = []
    if not PLAYER_BASE["qi_max"].ready:
        phase_b.append("player.qi_max")
    if not QI_COST_FLOOR.ready:
        phase_b.append("qi_cost_floor")

    phase_c = []
    for key in ("hp_max", "evasion", "defense", "control", "tenacity"):
        if not PLAYER_BASE[key].ready:
            phase_c.append(f"player.{key}")
    for key in ("hp_max", "precision", "evasion", "defense", "tenacity", "damage_model"):
        if not LIANQI_I_REFERENCE_ENEMY[key].ready:
            phase_c.append(f"enemy.{key}")
    if not ARRASTRE_BASE_CONTROL.ready:
        phase_c.append("arrastre.base_control")
    phase_c.extend(phase_b)
    phase_c.extend([
        "combat_policy.turn_order",
        "combat_policy.enemy_action",
        "combat_policy.player_action",
        "engine.full_duel_loop",
    ])

    return {
        "PHASE_A_DIRECT_PACKET": phase_a,
        "PHASE_B_QI_BUDGET": phase_b,
        "PHASE_C_FULL_DUEL": sorted(set(phase_c)),
    }


def _base_player_for_direct_packet() -> ActorStats:
    return ActorStats(
        hp_max=math.nan,
        qi_max=math.nan,
        precision=float(_value(PLAYER_BASE["precision"], "player.precision")),
        evasion=math.nan,
        defense=math.nan,
        percent_penetration=float(
            _value(PLAYER_BASE["percent_penetration"], "player.percent_penetration")
        ),
        flat_penetration=float(
            _value(PLAYER_BASE["flat_penetration"], "player.flat_penetration")
        ),
        crit_chance=float(_value(PLAYER_BASE["crit_chance"], "player.crit_chance")),
        crit_damage=float(_value(PLAYER_BASE["crit_damage"], "player.crit_damage")),
        control=math.nan,
        tenacity=math.nan,
        damage_done_percent=float(
            _value(PLAYER_BASE["damage_done_percent"], "player.damage_done_percent")
        ),
    )


def apply_main_root_for_direct_packet(stats: ActorStats, root: str) -> ActorStats:
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
    raise ValueError(f"Raíz desconocida: {root}")


def build_initial_technique(root: str) -> Technique:
    tech_id = ROOT_TO_INITIAL_TECHNIQUE[root]
    cfg = BASE_OFFENSIVE[tech_id]
    notation = str(_value(DAMAGE_MODEL_SELECTION[tech_id], f"damage_model.{tech_id}"))
    dice = Dice(notation)
    if abs(dice.mean() - float(cfg["nominal_damage"])) > 1e-9:
        raise ValueError(
            f"{tech_id}: {notation} tiene media {dice.mean()}, "
            f"pero el presupuesto nominal provisional es {cfg['nominal_damage']}. "
            "Si cambia la media, cambie primero el presupuesto explícito."
        )
    return Technique(
        name=tech_id,
        qi_cost=float(cfg["qi_cost"]),
        damage=dice,
        precision_mod=float(cfg["precision"]),
        crit_chance_mod=float(cfg["crit_chance"]),
        percent_penetration=float(cfg["percent_penetration"]),
    )


def build_phase_a_target() -> ActorStats:
    return ActorStats(
        hp_max=math.nan,
        qi_max=math.nan,
        precision=math.nan,
        evasion=float(_value(LIANQI_I_REFERENCE_ENEMY["evasion"], "enemy.evasion")),
        defense=float(_value(LIANQI_I_REFERENCE_ENEMY["defense"], "enemy.defense")),
    )


def build_phase_a_scenarios(iterations: int = 200_000, seed: int = 20260929) -> list[Scenario]:
    blocked = readiness_report()["PHASE_A_DIRECT_PACKET"]
    if blocked:
        raise ValueError("PHASE_A bloqueada: " + ", ".join(blocked))

    target = build_phase_a_target()
    scenarios = []
    for offset, (root, tech_id) in enumerate(ROOT_TO_INITIAL_TECHNIQUE.items()):
        player = apply_main_root_for_direct_packet(_base_player_for_direct_packet(), root)
        technique = build_initial_technique(root)
        scenarios.append(Scenario(
            id=f"L1_NAKED_A_{root.upper()}_{tech_id.upper()}",
            provenance="PROVISIONAL",
            attacker=player,
            target=target,
            technique=technique,
            iterations=iterations,
            seed=seed + offset,
        ))
    return scenarios


def run_phase_a(iterations: int = 200_000, seed: int = 20260929) -> list[dict]:
    return run_matrix(build_phase_a_scenarios(iterations=iterations, seed=seed))


def effective_qi_cost(root: str, tech_id: str) -> dict:
    qi_max = float(_value(PLAYER_BASE["qi_max"], "player.qi_max"))
    floor = float(_value(QI_COST_FLOOR, "qi_cost_floor"))
    base_cost = float(BASE_OFFENSIVE[tech_id]["qi_cost"])
    qi_cost_percent = float(ROOTS["agua"]["qi_cost_percent"]) if root == "agua" else 0.0
    cost_decimal = base_cost * (1.0 + qi_cost_percent / 100.0)
    cost_final = round_half_up(max(floor, cost_decimal))
    return {
        "root": root,
        "technique": tech_id,
        "base_cost": base_cost,
        "cost_decimal": cost_decimal,
        "cost_final": cost_final,
        "casts_from_full_qi": int(qi_max // cost_final) if cost_final > 0 else None,
    }


if __name__ == "__main__":
    report = readiness_report()
    for phase, blocked in report.items():
        print(phase, "READY" if not blocked else "BLOCKED")
        for item in blocked:
            print(" -", item)
