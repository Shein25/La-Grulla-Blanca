"""PHASE C LAB — Arrastre + Peso bajo Precisión enemiga variable.

Objetivo:
- valorar la utilidad real de Agua/Tierra sin alterar su daño;
- mantener el contrato hit cap=100;
- barrer Precisión enemiga 85/90/95/100;
- explorar Arrastre por probabilidad efectiva y Peso por dos modos de stacking.

Todo es LAB. No modifica runtime ni contrato CANON.
"""
from __future__ import annotations

from dataclasses import replace
import argparse
import csv
import math
import random
import statistics

from sim_core import ActorStats, Dice, Technique, clamp, resolve_direct_hit
from config_arc1_provisional import BASE_OFFENSIVE, ROOTS
from config_lianqi1_naked import (
    BASIC_ATTACK_SELECTION,
    DAMAGE_MODEL_SELECTION,
    LIANQI_I_REFERENCE_ENEMY,
    ROOT_TO_INITIAL_TECHNIQUE,
)

PLAYER_HP_LAB = 30.0
PLAYER_QI_LAB = 30
PLAYER_DEF_LAB = 1.0
PLAYER_EVASION_LAB = 5.0

ENEMY_HP_LAB = 28.0
ENEMY_DEF_LAB = 2.0
ENEMY_EVASION_LAB = 20.0
ENEMY_DAMAGE_LAB = "2d4+1"

ENEMY_PRECISION_LAB = (85.0, 90.0, 95.0, 100.0)
ENEMY_TENACITY_LAB = (0.0, 10.0, 20.0)
ARRASTRE_BASE_CONTROL_LAB = (40.0, 50.0, 60.0, 70.0, 80.0)

PESO_MODES_LAB = ("STACK_REFRESH", "INDEPENDENT")
PESO_FUTURE_ACTIONS_LAB = (1, 2)


def base_player(root: str) -> ActorStats:
    stats = ActorStats(
        hp_max=PLAYER_HP_LAB,
        qi_max=float(PLAYER_QI_LAB),
        precision=100.0,
        evasion=PLAYER_EVASION_LAB,
        defense=PLAYER_DEF_LAB,
        crit_chance=5.0,
        crit_damage=1.50,
        control=0.0,
        tenacity=0.0,
        percent_penetration=0.0,
        flat_penetration=0.0,
        damage_done_percent=0.0,
    )
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


def enemy(precision: float, tenacity: float) -> ActorStats:
    return ActorStats(
        hp_max=ENEMY_HP_LAB,
        qi_max=0.0,
        precision=precision,
        evasion=ENEMY_EVASION_LAB,
        defense=ENEMY_DEF_LAB,
        crit_chance=5.0,
        crit_damage=1.50,
        tenacity=tenacity,
    )


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


def enemy_attack() -> Technique:
    return Technique(
        name="enemy_basic_lab",
        qi_cost=0.0,
        damage=Dice(ENEMY_DAMAGE_LAB),
    )


def effective_cost(root: str, technique: Technique) -> int:
    reduction = float(ROOTS["agua"]["qi_cost_percent"]) if root == "agua" else 0.0
    value = technique.qi_cost * (1.0 + reduction / 100.0)
    return int(math.floor(value + 0.5))


def run_duel(
    root: str,
    enemy_precision: float,
    fights: int,
    seed: int,
    arrastre_base_control: float | None = None,
    enemy_tenacity: float = 0.0,
    peso_mode: str | None = None,
    peso_future_actions: int = 2,
) -> dict:
    rng = random.Random(seed)
    player = base_player(root)
    foe = enemy(enemy_precision, enemy_tenacity)
    tech = player_technique(root)
    basic = basic_attack()
    foe_attack = enemy_attack()
    cost = effective_cost(root, tech)

    wins = 0
    turns = []
    hp_remaining = []
    fallback_fights = 0
    basic_actions = []
    technique_actions = []
    enemy_skips = 0
    control_attempts = 0
    control_successes = 0
    peso_stack_sum = 0
    peso_action_samples = 0

    for _ in range(fights):
        player_hp = player.hp_max
        enemy_hp = foe.hp_max
        qi = PLAYER_QI_LAB
        n_turns = 0
        n_basic = 0
        n_tech = 0

        arrastre_lock = False
        skip_next_enemy_action = False

        peso_stacks: list[int] = []
        peso_stack_count = 0
        peso_remaining = 0

        while player_hp > 0 and enemy_hp > 0:
            n_turns += 1

            # Peso existente afecta ESTA nueva acción; la nueva carga obtenida
            # por el impacto sólo puede beneficiar acciones futuras.
            if root == "tierra" and peso_mode:
                if peso_mode == "INDEPENDENT":
                    peso_stacks = [d for d in peso_stacks if d > 0]
                    active_peso = len(peso_stacks)
                elif peso_mode == "STACK_REFRESH":
                    if peso_remaining <= 0:
                        peso_stack_count = 0
                    active_peso = peso_stack_count
                else:
                    raise ValueError(peso_mode)
                peso_stack_sum += active_peso
                peso_action_samples += 1
            else:
                active_peso = 0

            dynamic_foe = replace(
                foe,
                evasion=max(0.0, foe.evasion - 3.0 * active_peso),
            )

            uses_technique = qi >= cost
            if uses_technique:
                result = resolve_direct_hit(rng, player, dynamic_foe, tech)
                qi -= cost
                n_tech += 1
            else:
                result = resolve_direct_hit(rng, player, dynamic_foe, basic)
                n_basic += 1

            # Consumir una ventana futura de Peso ya existente.
            if root == "tierra" and peso_mode:
                if peso_mode == "INDEPENDENT":
                    peso_stacks = [d - 1 for d in peso_stacks]
                else:
                    if peso_remaining > 0:
                        peso_remaining -= 1
                    if peso_remaining <= 0:
                        peso_stack_count = 0

                # El Golpe actual agrega/refresca Peso DESPUÉS del impacto.
                if uses_technique and result.hit:
                    if peso_mode == "INDEPENDENT":
                        peso_stacks = [d for d in peso_stacks if d > 0]
                        if len(peso_stacks) < 2:
                            peso_stacks.append(peso_future_actions)
                        else:
                            peso_stacks.sort()
                            peso_stacks[0] = peso_future_actions
                    else:
                        peso_stack_count = min(2, peso_stack_count + 1)
                        peso_remaining = peso_future_actions

            # Arrastre sólo se intenta al impactar Latigazo y respeta lockout.
            if (
                root == "agua"
                and uses_technique
                and result.hit
                and arrastre_base_control is not None
                and not arrastre_lock
            ):
                control_attempts += 1
                chance = clamp(
                    arrastre_base_control + player.control - foe.tenacity,
                    5.0,
                    100.0,
                )
                if rng.random() < chance / 100.0:
                    control_successes += 1
                    skip_next_enemy_action = True
                    arrastre_lock = True

            enemy_hp -= result.damage_after_def
            if enemy_hp <= 0:
                break

            if skip_next_enemy_action:
                enemy_skips += 1
                skip_next_enemy_action = False
                # perder acción NO satisface el lockout: debe completar una
                # acción normal antes de volver a sufrir Arrastre.
            else:
                incoming = resolve_direct_hit(rng, foe, player, foe_attack)
                player_hp -= incoming.damage_after_def
                if arrastre_lock:
                    arrastre_lock = False

            if n_turns > 100:
                raise RuntimeError("duelo excedió 100 turnos")

        wins += int(enemy_hp <= 0 and player_hp > 0)
        turns.append(n_turns)
        hp_remaining.append(max(0.0, player_hp))
        fallback_fights += int(n_basic > 0)
        basic_actions.append(n_basic)
        technique_actions.append(n_tech)

    return {
        "provenance": "LAB",
        "root": root,
        "enemy_precision": enemy_precision,
        "enemy_tenacity": enemy_tenacity,
        "arrastre_base_control": arrastre_base_control,
        "arrastre_effective_chance": (
            clamp(arrastre_base_control + player.control - foe.tenacity, 5.0, 100.0)
            if arrastre_base_control is not None else None
        ),
        "peso_mode": peso_mode,
        "peso_future_actions": peso_future_actions if peso_mode else None,
        "fights": fights,
        "win_rate": wins / fights,
        "mean_turns": statistics.fmean(turns),
        "mean_hp_remaining_percent": statistics.fmean(hp_remaining) / player.hp_max,
        "fallback_rate": fallback_fights / fights,
        "mean_basic_actions": statistics.fmean(basic_actions),
        "mean_technique_actions": statistics.fmean(technique_actions),
        "mean_enemy_actions_skipped": enemy_skips / fights,
        "mean_control_attempts": control_attempts / fights,
        "mean_control_successes": control_successes / fights,
        "mean_peso_stacks_on_player_action": (
            peso_stack_sum / peso_action_samples if peso_action_samples else 0.0
        ),
    }


def run(fights: int, seed: int) -> list[dict]:
    rows = []
    serial = 0

    # Baseline sin utilidades para las cinco raíces.
    for precision in ENEMY_PRECISION_LAB:
        for root in ("fuego", "metal", "agua", "tierra", "viento"):
            rows.append(run_duel(root, precision, fights, seed + serial))
            serial += 1

    # Sensibilidad completa de Arrastre.
    for precision in ENEMY_PRECISION_LAB:
        for tenacity in ENEMY_TENACITY_LAB:
            for base_control in ARRASTRE_BASE_CONTROL_LAB:
                rows.append(
                    run_duel(
                        "agua",
                        precision,
                        fights,
                        seed + serial,
                        arrastre_base_control=base_control,
                        enemy_tenacity=tenacity,
                    )
                )
                serial += 1

    # Sensibilidad de Peso.
    for precision in ENEMY_PRECISION_LAB:
        for mode in PESO_MODES_LAB:
            for future_actions in PESO_FUTURE_ACTIONS_LAB:
                rows.append(
                    run_duel(
                        "tierra",
                        precision,
                        fights,
                        seed + serial,
                        peso_mode=mode,
                        peso_future_actions=future_actions,
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
    ap.add_argument("--fights", type=int, default=100_000)
    ap.add_argument("--seed", type=int, default=20260929)
    ap.add_argument("--csv", default="lianqi1_arrastre_peso_lab.csv")
    args = ap.parse_args()
    rows = run(args.fights, args.seed)
    export(rows, args.csv)
    print(f"CSV: {args.csv} ({len(rows)} escenarios)")
