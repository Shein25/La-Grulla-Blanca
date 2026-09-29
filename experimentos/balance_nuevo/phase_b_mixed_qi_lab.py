"""PHASE B LAB — economía mixta de Qi LianQi I.

Evalúa acantilados aritméticos al mezclar:
- ofensivas de coste efectivo 6;
- defensivas base de coste 7;
- defensivas de Agua, cuyo coste 7 se vuelve 6 por raíz.

No ejecuta combate; mide capacidad de secuencia y residuo.
"""
from __future__ import annotations

import argparse
import csv

QI_MAX_CANDIDATES_LAB = tuple(range(28, 37))
OFFENSIVE_COST = 6
DEFENSIVE_COST_NORMAL = 7
DEFENSIVE_COST_WATER_EFFECTIVE = 6


def sequence(qi_max: int, defensive_cost: int | None) -> dict:
    qi = qi_max
    defense_actions = 0

    if defensive_cost is not None:
        if qi < defensive_cost:
            return {
                "total_technique_actions": 0,
                "defense_actions": 0,
                "offense_actions": 0,
                "qi_left": qi,
            }
        qi -= defensive_cost
        defense_actions = 1

    offense_actions = qi // OFFENSIVE_COST
    qi_left = qi % OFFENSIVE_COST

    return {
        "total_technique_actions": defense_actions + offense_actions,
        "defense_actions": defense_actions,
        "offense_actions": offense_actions,
        "qi_left": qi_left,
    }


def run() -> list[dict]:
    rows = []
    for qi_max in QI_MAX_CANDIDATES_LAB:
        for label, defense_cost in (
            ("PURE_OFFENSE_6", None),
            ("DEFENSE_6_PLUS_OFFENSE_6", DEFENSIVE_COST_WATER_EFFECTIVE),
            ("DEFENSE_7_PLUS_OFFENSE_6", DEFENSIVE_COST_NORMAL),
        ):
            rows.append({
                "provenance": "LAB",
                "qi_max": qi_max,
                "sequence": label,
                "offensive_cost": OFFENSIVE_COST,
                "defensive_cost": defense_cost,
                **sequence(qi_max, defense_cost),
            })
    return rows


def export(rows: list[dict], path: str) -> None:
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default="lianqi1_mixed_qi_budget_lab.csv")
    args = ap.parse_args()

    rows = run()
    export(rows, args.csv)

    for row in rows:
        print(row)
    print(f"CSV: {args.csv} ({len(rows)} escenarios)")
