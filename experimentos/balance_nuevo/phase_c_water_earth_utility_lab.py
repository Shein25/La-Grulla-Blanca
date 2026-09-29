"""PHASE C LAB — utilidad base de Agua y Tierra.

Objetivo:
- valorar Arrastre de Latigazo de Marea sin fijar todavía base_control/Tenacidad;
- valorar Peso de Golpe de Montaña;
- usar el duelo extendido con PREC enemiga 90 como centro LAB.

Guardias:
- no modifica CANON;
- no modifica sim_core.py;
- no inventa base_control ni Tenacidad;
- Arrastre se barre como probabilidad EFECTIVA post-fórmula;
- Peso conserva -3 EVA/carga, duración 2, máximo 2.

El test compara dos semánticas LAB de duración de Peso porque el documento de
técnica no especifica todavía si las cargas comparten/refrescan una duración o
si cada carga conserva duración independiente.
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

PLAYER_HP_LAB = 30
PLAYER_QI_LAB = 30
PLAYER_DEF_LAB = 1
PLAYER_EVASION_LAB = 5

ENEMY_HP_LAB = 28
ENEMY_PRECISION_LAB = 90
ENEMY_EVASION_LAB = 20
ENEMY_DEF_LAB = 2
ENEMY_DAMAGE_LAB = "2d4+1"

ARRASTRE_EFFECTIVE_CHANCE_LAB = (0.25, 0.35, 0.45, 0.50, 0.55, 0.65, 0.75)
PESO_SEMANTICS_LAB = ("REFRESH_SHARED", "INDEPENDENT")


def base_player() -> ActorStats:
    return ActorStats(
        hp_max=PLAYER_HP_LAB,
        qi_max=PLAYER_QI_LAB,
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


def enemy() -> ActorStats:
    return ActorStats(
        hp_max=ENEMY_HP_LAB,
        qi_max=0.0,
        precision=ENEMY_PRECISION_LAB,
        evasion=ENEMY_EVASION_LAB,
        defense=ENEMY_DEF_LAB,
        crit_chance=5.0,
        crit_damage=1.50,
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


def effective_cost(root: str, technique: Technique) -> int:
    reduction = float(ROOTS["agua"]["qi_cost_percent"]) if root == "agua" else 0.0
    decimal = technique.qi_cost * (1.0 + reduction / 100.0)
    return int(math.floor(decimal + 0.5))


def run_water(
    effective_arrastre_chance: float | None,
    fights: int,
    seed: int,
) -> dict:
    """Arrastre respeta anti-bloqueo.

    Tras un Arrastre exitoso:
    - el enemigo pierde su próxima acción;
    - no puede volver a sufrir Arrastre;
    - debe completar una acción normal para quedar elegible otra vez.

    effective_arrastre_chance es la probabilidad POST fórmula Control/Tenacidad.
    """
    rng = random.Random(seed)
    player = apply_root(base_player(), "agua")
    foe = enemy()
    tech = player_technique("agua")
    basic = basic_attack()
    foe_attack = Technique("enemy_basic_lab", 0.0, Dice(ENEMY_DAMAGE_LAB))
    cost = effective_cost("agua", tech)

    wins = 0
    turns = []
    hp_remaining = []
    skipped_actions = []
    enemy_actions = []
    fallback = 0
    attempts = 0
    successes = 0

    for _ in range(fights):
        p_hp = player.hp_max
        e_hp = foe.hp_max
        qi = PLAYER_QI_LAB
        n_turns = 0
        skipped = 0
        enemy_acts = 0
        used_basic = False
        arrastre_eligible = True

        while p_hp > 0 and e_hp > 0:
            n_turns += 1
            skip_enemy = False

            if qi >= cost:
                result = resolve_direct_hit(rng, player, foe, tech)
                qi -= cost

                if (
                    effective_arrastre_chance is not None
                    and result.hit
                    and arrastre_eligible
                ):
                    attempts += 1
                    if rng.random() < effective_arrastre_chance:
                        successes += 1
                        skip_enemy = True
                        arrastre_eligible = False
            else:
                result = resolve_direct_hit(rng, player, foe, basic)
                used_basic = True

            e_hp -= result.damage_after_def
            if e_hp <= 0:
                break

            if skip_enemy:
                skipped += 1
            else:
                incoming = resolve_direct_hit(rng, foe, player, foe_attack)
                p_hp -= incoming.damage_after_def
                enemy_acts += 1
                if not arrastre_eligible:
                    arrastre_eligible = True

            if n_turns > 100:
                raise RuntimeError("duelo excedió 100 turnos")

        wins += int(e_hp <= 0 and p_hp > 0)
        fallback += int(used_basic)
        turns.append(n_turns)
        hp_remaining.append(max(0.0, p_hp))
        skipped_actions.append(skipped)
        enemy_actions.append(enemy_acts)

    return {
        "provenance": "LAB",
        "root": "agua",
        "variant": (
            "NO_ARRASTRE"
            if effective_arrastre_chance is None
            else f"ARRASTRE_{effective_arrastre_chance:.2f}"
        ),
        "arrastre_effective_chance": effective_arrastre_chance,
        "fights": fights,
        "win_rate": wins / fights,
        "mean_turns": statistics.fmean(turns),
        "mean_hp_remaining_percent": statistics.fmean(hp_remaining) / player.hp_max,
        "fallback_rate": fallback / fights,
        "mean_enemy_actions_skipped": statistics.fmean(skipped_actions),
        "mean_enemy_actions_completed": statistics.fmean(enemy_actions),
        "observed_arrastre_success_rate": (
            successes / attempts if attempts else None
        ),
    }


def run_earth(
    peso_semantics: str | None,
    fights: int,
    seed: int,
) -> dict:
    """Peso:
    -3 EVA por carga, duración 2 turnos, máximo 2.

    REFRESH_SHARED:
      el estado comparte duración; cada aplicación añade carga y refresca a 2.

    INDEPENDENT:
      cada carga conserva duración 2; al máximo, una nueva aplicación refresca
      la carga con menor duración.
    """
    rng = random.Random(seed)
    player = apply_root(base_player(), "tierra")
    foe = enemy()
    tech = player_technique("tierra")
    basic = basic_attack()
    foe_attack = Technique("enemy_basic_lab", 0.0, Dice(ENEMY_DAMAGE_LAB))
    cost = effective_cost("tierra", tech)

    wins = 0
    turns = []
    hp_remaining = []
    fallback = 0
    enemy_actions = []

    for _ in range(fights):
        p_hp = player.hp_max
        e_hp = foe.hp_max
        qi = PLAYER_QI_LAB
        n_turns = 0
        used_basic = False
        enemy_acts = 0

        shared_stacks = 0
        shared_duration = 0
        independent_durations: list[int] = []

        while p_hp > 0 and e_hp > 0:
            n_turns += 1

            if peso_semantics == "REFRESH_SHARED":
                active_stacks = shared_stacks
            elif peso_semantics == "INDEPENDENT":
                active_stacks = len(independent_durations)
            else:
                active_stacks = 0

            dynamic_foe = replace(
                foe,
                evasion=ENEMY_EVASION_LAB - 3.0 * active_stacks,
            )

            if qi >= cost:
                result = resolve_direct_hit(rng, player, dynamic_foe, tech)
                qi -= cost

                if result.hit and peso_semantics == "REFRESH_SHARED":
                    shared_stacks = min(2, shared_stacks + 1)
                    shared_duration = 2
                elif result.hit and peso_semantics == "INDEPENDENT":
                    if len(independent_durations) < 2:
                        independent_durations.append(2)
                    else:
                        idx = min(
                            range(len(independent_durations)),
                            key=lambda i: independent_durations[i],
                        )
                        independent_durations[idx] = 2
            else:
                result = resolve_direct_hit(rng, player, dynamic_foe, basic)
                used_basic = True

            e_hp -= result.damage_after_def
            if e_hp <= 0:
                break

            incoming = resolve_direct_hit(rng, foe, player, foe_attack)
            p_hp -= incoming.damage_after_def
            enemy_acts += 1

            if peso_semantics == "REFRESH_SHARED":
                if shared_duration > 0:
                    shared_duration -= 1
                    if shared_duration <= 0:
                        shared_stacks = 0
            elif peso_semantics == "INDEPENDENT":
                independent_durations = [
                    duration - 1
                    for duration in independent_durations
                    if duration - 1 > 0
                ]

            if n_turns > 100:
                raise RuntimeError("duelo excedió 100 turnos")

        wins += int(e_hp <= 0 and p_hp > 0)
        fallback += int(used_basic)
        turns.append(n_turns)
        hp_remaining.append(max(0.0, p_hp))
        enemy_actions.append(enemy_acts)

    return {
        "provenance": "LAB",
        "root": "tierra",
        "variant": peso_semantics or "NO_PESO",
        "fights": fights,
        "win_rate": wins / fights,
        "mean_turns": statistics.fmean(turns),
        "mean_hp_remaining_percent": statistics.fmean(hp_remaining) / player.hp_max,
        "fallback_rate": fallback / fights,
        "mean_enemy_actions_completed": statistics.fmean(enemy_actions),
    }


def run(fights: int, seed: int) -> list[dict]:
    rows: list[dict] = []

    rows.append(run_water(None, fights, seed))
    for i, chance in enumerate(ARRASTRE_EFFECTIVE_CHANCE_LAB, 1):
        rows.append(run_water(chance, fights, seed + i))

    rows.append(run_earth(None, fights, seed + 100))
    for i, semantics in enumerate(PESO_SEMANTICS_LAB, 1):
        rows.append(run_earth(semantics, fights, seed + 100 + i))

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
    ap.add_argument("--csv", default="lianqi1_water_earth_utility_lab.csv")
    args = ap.parse_args()

    rows = run(args.fights, args.seed)
    export(rows, args.csv)
    for row in rows:
        print(row)
    print(f"CSV: {args.csv} ({len(rows)} escenarios)")
