"""ETAPA 16 — Validación final de Qi31 LianQi I.

Reutiliza el runner autoritativo de ETAPA15A para barrer Qi29–37
sin cambiar daño, DEF, EVA ni las defensivas.

Objetivo:
- validar la frontera discreta de Qi;
- demostrar la meseta 31–35;
- mostrar los acantilados 30/36/37.

No modifica runtime.
"""
from __future__ import annotations

import argparse
import csv

import etapa15a_screen_conjunto_defensivas_base as base


QI_CANDIDATES = tuple(range(29, 38))
PROFILES = {
    "COMMON": (1, 90.0, "2d4+1"),
    "2EN": (2, 90.0, "2d4+1"),
    "3EN": (3, 90.0, "2d4+1"),
}


def budget(qi: int) -> dict:
    return {
        "qi": qi,
        "pure_offense_6": qi // 6,
        "normal_def7_plus_offense6": (qi - 7) // 6,
        "water_def6_plus_offense6": (qi - 6) // 6,
        "normal_total_actions": 1 + (qi - 7) // 6,
        "water_total_actions": 1 + (qi - 6) // 6,
    }


def run(fights: int, seed: int) -> list[dict]:
    rows = []
    serial = 0

    for qi in QI_CANDIDATES:
        base.QI_MAX_LAB = qi

        for profile, (count, precision, damage) in PROFILES.items():
            for root in ("fuego", "metal", "agua", "tierra", "viento"):
                result = base.run_one(
                    root=root,
                    use_defensive=True,
                    enemy_count=count,
                    enemy_precision=precision,
                    enemy_damage=damage,
                    fights=fights,
                    seed=seed + serial,
                )
                serial += 1
                rows.append({
                    "provenance": "LAB",
                    "qi": qi,
                    "profile": profile,
                    **result,
                })

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
    ap.add_argument("--csv", default="etapa16_qi29_37.csv")
    args = ap.parse_args()

    print("BUDGET")
    for qi in QI_CANDIDATES:
        print(budget(qi))

    rows = run(args.fights, args.seed)
    export(rows, args.csv)
    print(f"CSV: {args.csv} ({len(rows)} escenarios)")
