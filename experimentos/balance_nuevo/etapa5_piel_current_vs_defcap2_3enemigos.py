"""ETAPA 5 — Piel CURRENT vs DEF_CAP2 · 3 enemigos.

Escenario aislado:
- HP enemigo total 28, dividido 10 + 9 + 9;
- cada enemigo vivo actúa una vez por ronda;
- PREC90 / EVA20 / DEF2 / daño 2d4+1;
- jugador Tierra HP33 / Qi31 / DEF1 / EVA5;
- Piel como apertura;
- Golpe de Montaña unitarget;
- Peso PROVISIONAL STACK_REFRESH.

Compara únicamente la curva de DEF de Piel:
CURRENT  -> contribución de Arraigo 1/2/3
DEF_CAP2 -> contribución de Arraigo 1/2/2
"""
from __future__ import annotations

from dataclasses import replace
import argparse
import csv
import random
import statistics

import phase_c_all_defensives_lab as base


ENEMY_HPS = (10.0, 9.0, 9.0)
FIGHTS_DEFAULT = 200_000


def run_variant(variant: str, fights: int, seed: int) -> dict:
    if variant not in {"CURRENT", "DEF_CAP2"}:
        raise ValueError(variant)

    rng = random.Random(seed)
    old_qi = base.QI_MAX_LAB
    base.QI_MAX_LAB = 31

    player = base.player("tierra")
    offense = base.offense("tierra")
    basic_attack = base.basic()
    enemy_attack = base.Technique(
        "enemy_basic_lab", 0.0, base.Dice("2d4+1")
    )

    wins = 0
    rounds = []
    hp_remaining = []
    fallback = 0
    max_arraigo_values = []
    enemy_hits_values = []
    damage_received_values = []
    extension_count = 0

    try:
        for _ in range(fights):
            hp = player.hp_max
            qi = 31
            enemy_hps = list(ENEMY_HPS)
            peso_stacks = [0, 0, 0]
            peso_duration = [0, 0, 0]

            round_no = 0
            defense_used = False
            used_basic = False

            piel_active = False
            piel_left = 0
            arraigo = 0
            large_trigger_used = False
            extension_used = False

            max_arraigo = 0
            enemy_hits = 0
            damage_received = 0.0

            while hp > 0 and any(value > 0 for value in enemy_hps):
                round_no += 1

                if not defense_used and round_no == 1:
                    qi -= 7
                    defense_used = True
                    piel_active = True
                    piel_left = 3
                    arraigo = 1
                    max_arraigo = 1
                else:
                    target_index = next(
                        i for i, value in enumerate(enemy_hps)
                        if value > 0
                    )
                    target = base.ActorStats(
                        hp_max=enemy_hps[target_index],
                        qi_max=0.0,
                        precision=90.0,
                        evasion=20.0 - 3.0 * peso_stacks[target_index],
                        defense=2.0,
                        crit_chance=5.0,
                        crit_damage=1.50,
                    )

                    if qi >= 6:
                        result = base.resolve_direct_hit(
                            rng, player, target, offense
                        )
                        qi -= 6
                        if result.hit:
                            peso_stacks[target_index] = min(
                                2, peso_stacks[target_index] + 1
                            )
                            peso_duration[target_index] = 2
                    else:
                        result = base.resolve_direct_hit(
                            rng, player, target, basic_attack
                        )
                        used_basic = True

                    enemy_hps[target_index] -= result.damage_after_def

                for index, enemy_hp in enumerate(enemy_hps):
                    if enemy_hp <= 0 or hp <= 0:
                        continue

                    target_def = player.defense
                    if piel_active and piel_left > 0:
                        arraigo_def = (
                            arraigo
                            if variant == "CURRENT"
                            else min(arraigo, 2)
                        )
                        target_def += 2.0 + arraigo_def

                    target_player = replace(player, defense=target_def)
                    enemy_actor = base.ActorStats(
                        hp_max=enemy_hp,
                        qi_max=0.0,
                        precision=90.0,
                        evasion=20.0,
                        defense=2.0,
                        crit_chance=5.0,
                        crit_damage=1.50,
                    )

                    incoming = base.resolve_direct_hit(
                        rng, enemy_actor, target_player, enemy_attack
                    )
                    enemy_hits += int(incoming.hit)
                    hp_damage = float(incoming.damage_after_def)
                    hp -= hp_damage
                    damage_received += hp_damage

                    if (
                        piel_active
                        and piel_left > 0
                        and hp_damage > 0
                    ):
                        gain = 1
                        if (
                            not large_trigger_used
                            and hp_damage >= 0.10 * player.hp_max
                        ):
                            gain = 2
                            large_trigger_used = True

                        old = arraigo
                        arraigo = min(3, arraigo + gain)
                        max_arraigo = max(max_arraigo, arraigo)

                        if (
                            old < 3
                            and arraigo == 3
                            and not extension_used
                        ):
                            piel_left += 1
                            extension_used = True

                if piel_active and piel_left > 0:
                    piel_left -= 1
                    if piel_left <= 0:
                        piel_active = False
                        arraigo = 0

                for index in range(3):
                    if peso_duration[index] > 0:
                        peso_duration[index] -= 1
                        if peso_duration[index] <= 0:
                            peso_stacks[index] = 0

                if round_no > 100:
                    raise RuntimeError("combate excedió 100 rondas")

            wins += int(
                all(value <= 0 for value in enemy_hps) and hp > 0
            )
            fallback += int(used_basic)
            rounds.append(round_no)
            hp_remaining.append(max(0.0, hp))
            max_arraigo_values.append(max_arraigo)
            enemy_hits_values.append(enemy_hits)
            damage_received_values.append(damage_received)
            extension_count += int(extension_used)
    finally:
        base.QI_MAX_LAB = old_qi

    return {
        "provenance": "LAB",
        "variant": variant,
        "fights": fights,
        "win_rate": wins / fights,
        "mean_rounds": statistics.fmean(rounds),
        "mean_hp_remaining_percent": (
            statistics.fmean(hp_remaining) / player.hp_max
        ),
        "fallback_rate": fallback / fights,
        "mean_max_arraigo": statistics.fmean(max_arraigo_values),
        "mean_enemy_hits": statistics.fmean(enemy_hits_values),
        "mean_damage_received": statistics.fmean(damage_received_values),
        "extension_rate": extension_count / fights,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fights", type=int, default=FIGHTS_DEFAULT)
    ap.add_argument("--seed", type=int, default=20260929)
    ap.add_argument("--csv", default="etapa5_piel_3enemigos.csv")
    args = ap.parse_args()

    rows = [
        run_variant("CURRENT", args.fights, args.seed),
        run_variant("DEF_CAP2", args.fights, args.seed),
    ]

    with open(args.csv, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    for row in rows:
        print(row)


if __name__ == "__main__":
    main()
