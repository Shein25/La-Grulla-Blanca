"""LAB PHASE B — presupuesto de Qi LianQi I.

No fija Qi máximo ni piso de coste. Barre candidatos nuevos y calcula
costes efectivos/cantidad de lanzamientos desde Qi lleno.

No usa HP, daño enemigo, equipo, Concordancias ni regeneración pasiva.
"""
from __future__ import annotations

import argparse
import csv

from config_arc1_provisional import BASE_OFFENSIVE, ROOTS
from config_lianqi1_naked import ROOT_TO_INITIAL_TECHNIQUE
from sim_core import round_half_up


QI_MAX_CANDIDATES_LAB = (18, 24, 30, 36, 42)
QI_COST_FLOOR_CANDIDATES_LAB = (1.0, 3.0, 5.0, 6.0)


def effective_cost(root: str, tech_id: str, floor: float) -> dict:
    base_cost = float(BASE_OFFENSIVE[tech_id]["qi_cost"])
    qi_cost_percent = float(ROOTS["agua"]["qi_cost_percent"]) if root == "agua" else 0.0
    cost_decimal = base_cost * (1.0 + qi_cost_percent / 100.0)
    cost_final = round_half_up(max(float(floor), cost_decimal))
    return {
        "base_cost": base_cost,
        "qi_cost_percent": qi_cost_percent,
        "cost_decimal": cost_decimal,
        "cost_final": cost_final,
    }


def run() -> list[dict]:
    rows: list[dict] = []
    for floor in QI_COST_FLOOR_CANDIDATES_LAB:
        for qi_max in QI_MAX_CANDIDATES_LAB:
            for root, tech_id in ROOT_TO_INITIAL_TECHNIQUE.items():
                cost = effective_cost(root, tech_id, floor)
                final = cost["cost_final"]
                rows.append({
                    "provenance": "LAB",
                    "qi_max": qi_max,
                    "qi_cost_floor": floor,
                    "root": root,
                    "technique": tech_id,
                    **cost,
                    "casts_from_full_qi": qi_max // final if final > 0 else None,
                    "qi_left_after_max_casts": qi_max % final if final > 0 else None,
                })
    return rows


def export(rows: list[dict], path: str) -> None:
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default="lianqi1_phase_b_qi_budget_lab.csv")
    args = ap.parse_args()

    rows = run()
    export(rows, args.csv)
    print("qi_max,floor,root,base_cost,cost_decimal,cost_final,casts,leftover")
    for row in rows:
        if row["qi_cost_floor"] == 1.0:
            print(
                f'{row["qi_max"]},{row["qi_cost_floor"]},{row["root"]},'
                f'{row["base_cost"]:.1f},{row["cost_decimal"]:.1f},{row["cost_final"]},'
                f'{row["casts_from_full_qi"]},{row["qi_left_after_max_casts"]}'
            )
    print(f"CSV: {args.csv} ({len(rows)} escenarios)")
