"""PHASE C LAB — traducción de Arrastre a Control/Tenacidad.

Este laboratorio NO fija valores canónicos. Explora combinaciones nuevas de
base_control y Tenacidad que produzcan la banda efectiva de Arrastre detectada
en el duelo LianQi I.

Fórmula CANON:
P(Control) = clamp(base_control + Control_atacante - Tenacidad_objetivo, 5, 100)

Agua principal aporta +5 Control.
"""
from __future__ import annotations

import argparse
import csv

from sim_core import clamp
from phase_c_water_earth_utility_lab import run_water

BASE_CONTROL_CANDIDATES_LAB = (55.0, 65.0, 75.0)
TENACITY_CANDIDATES_LAB = (10.0, 20.0, 30.0, 40.0)
WATER_CONTROL_CANON = 5.0


def effective_chance(base_control: float, tenacity: float) -> float:
    return clamp(base_control + WATER_CONTROL_CANON - tenacity, 5.0, 100.0) / 100.0


def run(fights: int, seed: int) -> list[dict]:
    rows: list[dict] = []
    serial = 0
    for base_control in BASE_CONTROL_CANDIDATES_LAB:
        for tenacity in TENACITY_CANDIDATES_LAB:
            chance = effective_chance(base_control, tenacity)
            duel = run_water(chance, fights, seed + serial)
            serial += 1
            rows.append({
                "provenance": "LAB",
                "base_control": base_control,
                "water_control": WATER_CONTROL_CANON,
                "enemy_tenacity": tenacity,
                "effective_arrastre_chance": chance,
                "win_rate": duel["win_rate"],
                "mean_turns": duel["mean_turns"],
                "mean_hp_remaining_percent": duel["mean_hp_remaining_percent"],
                "mean_enemy_actions_skipped": duel["mean_enemy_actions_skipped"],
                "mean_enemy_actions_completed": duel["mean_enemy_actions_completed"],
            })
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
    ap.add_argument("--csv", default="lianqi1_control_tenacity_lab.csv")
    args = ap.parse_args()

    rows = run(args.fights, args.seed)
    export(rows, args.csv)

    print("base_control,tenacity,chance,win,skipped")
    for row in rows:
        print(
            f'{row["base_control"]:.0f},'
            f'{row["enemy_tenacity"]:.0f},'
            f'{row["effective_arrastre_chance"]:.2%},'
            f'{row["win_rate"]:.4f},'
            f'{row["mean_enemy_actions_skipped"]:.4f}'
        )
    print(f"CSV: {args.csv} ({len(rows)} escenarios)")
