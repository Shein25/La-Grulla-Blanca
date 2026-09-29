"""Cross-check determinístico de PHASE A LianQi I.

Enumera exactamente las tiradas posibles de los dados seleccionados y calcula
valor esperado, probabilidad de impacto y tasa de impactos reducidos a 0.
Sirve como control independiente del Monte Carlo.

No modifica CANON ni runtime.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import replace
import math
import re

from sim_core import ActorStats, Dice, Technique, clamp, effective_def, hit_probability, round_half_up
from config_arc1_provisional import BASE_OFFENSIVE, ROOTS
from config_lianqi1_naked import (
    BASIC_ATTACK_SELECTION,
    DAMAGE_MODEL_SELECTION,
    LIANQI_I_REFERENCE_ENEMY,
    PLAYER_BASE,
    ROOT_TO_INITIAL_TECHNIQUE,
)


def _dice_pmf(notation: str) -> dict[float, float]:
    pmf: dict[float, float] = {0.0: 1.0}
    expr = notation.replace(" ", "")
    for token in re.findall(r"[+-]?[^+-]+", expr):
        sign = -1 if token.startswith("-") else 1
        body = token[1:] if token[:1] in "+-" else token
        term: dict[float, float]
        if "d" in body.lower():
            n_s, sides_s = body.lower().split("d", 1)
            n = int(n_s) if n_s else 1
            sides = int(sides_s)
            counts = Counter({0: 1})
            for _ in range(n):
                nxt = Counter()
                for acc, count in counts.items():
                    for face in range(1, sides + 1):
                        nxt[acc + face] += count
                counts = nxt
            total = sides ** n
            term = {float(sign * value): count / total for value, count in counts.items()}
        else:
            term = {float(sign * int(body)): 1.0}

        nxt_pmf: dict[float, float] = {}
        for a, pa in pmf.items():
            for b, pb in term.items():
                nxt_pmf[a + b] = nxt_pmf.get(a + b, 0.0) + pa * pb
        pmf = nxt_pmf
    return pmf


def _base_player() -> ActorStats:
    return ActorStats(
        hp_max=math.nan,
        qi_max=math.nan,
        precision=float(PLAYER_BASE["precision"].value),
        evasion=math.nan,
        defense=math.nan,
        percent_penetration=float(PLAYER_BASE["percent_penetration"].value),
        flat_penetration=float(PLAYER_BASE["flat_penetration"].value),
        crit_chance=float(PLAYER_BASE["crit_chance"].value),
        crit_damage=float(PLAYER_BASE["crit_damage"].value),
        control=math.nan,
        tenacity=math.nan,
        damage_done_percent=float(PLAYER_BASE["damage_done_percent"].value),
    )


def _apply_root(stats: ActorStats, root: str) -> ActorStats:
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


def _target() -> ActorStats:
    return ActorStats(
        hp_max=math.nan,
        qi_max=math.nan,
        precision=math.nan,
        evasion=float(LIANQI_I_REFERENCE_ENEMY["evasion"].value),
        defense=float(LIANQI_I_REFERENCE_ENEMY["defense"].value),
    )


def _technique(root: str) -> Technique:
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


def _basic() -> Technique:
    return Technique(
        name="ataque_basico",
        qi_cost=0.0,
        damage=Dice(str(BASIC_ATTACK_SELECTION.value)),
    )


def exact_summary(attacker: ActorStats, target: ActorStats, technique: Technique) -> dict:
    hit_p = hit_probability(attacker, target, technique)
    crit_p = clamp(attacker.crit_chance + technique.crit_chance_mod, 0.0, 100.0) / 100.0
    edef = effective_def(attacker, target, technique)
    mean = 0.0
    zero_on_hit = 0.0

    for roll, roll_p in _dice_pmf(technique.damage.notation).items():
        modified = roll * max(
            0.0,
            1.0 + (attacker.damage_done_percent + technique.damage_percent) / 100.0,
        )

        normal = round_half_up(max(0.0, modified - edef))
        critical = round_half_up(
            max(
                0.0,
                modified * max(0.0, attacker.crit_damage + technique.crit_damage_mod) - edef,
            )
        )

        mean += hit_p * roll_p * ((1.0 - crit_p) * normal + crit_p * critical)
        zero_on_hit += roll_p * (
            (1.0 - crit_p) * (1.0 if normal == 0 else 0.0)
            + crit_p * (1.0 if critical == 0 else 0.0)
        )

    return {
        "hit_rate": hit_p,
        "mean_damage_after_def": mean,
        "zero_damage_rate_on_hit": zero_on_hit,
    }


if __name__ == "__main__":
    tgt = _target()
    print("root,action,dice,hit_rate,mean_damage_after_def,zero_damage_rate_on_hit,premium_vs_basic")
    for root in ("fuego", "metal", "agua", "tierra", "viento"):
        actor = _apply_root(_base_player(), root)
        basic = _basic()
        tech = _technique(root)
        b = exact_summary(actor, tgt, basic)
        t = exact_summary(actor, tgt, tech)
        premium = t["mean_damage_after_def"] / b["mean_damage_after_def"]
        print(
            f'{root},BASIC,{basic.damage.notation},{b["hit_rate"]:.6f},'
            f'{b["mean_damage_after_def"]:.6f},{b["zero_damage_rate_on_hit"]:.6f},1.000000'
        )
        print(
            f'{root},TECHNIQUE,{tech.damage.notation},{t["hit_rate"]:.6f},'
            f'{t["mean_damage_after_def"]:.6f},{t["zero_damage_rate_on_hit"]:.6f},{premium:.6f}'
        )
