"""PHASE C LAB — recalibración fina de defensivas débiles.

Reutiliza el screen de cinco defensivas y barre sólo las magnitudes LAB de:
- Cuerpo-Horno (Fuego)
- Espejo de Luna (Agua)
- Paso de Nube Ligera (Viento)

No modifica los valores autoritativos de técnicas.
"""
from __future__ import annotations

import argparse
import csv

import phase_c_all_defensives_lab as base


FIRE_ABSORPTION_LAB = (0.22, 0.23, 0.24, 0.25)
WATER_ABSORPTION_LAB = (0.21, 0.22, 0.23, 0.24, 0.25)
WIND_EVASION_DURATION_LAB = (
    (25.0, 3),
    (30.0, 3),
    (30.0, 4),
    (32.0, 4),
    (33.0, 4),
    (34.0, 4),
    (35.0, 4),
)

STRESS_PROFILES = {
    "COMMON": (90.0, "2d4+1"),
    "PRECISE": (100.0, "2d4+1"),
    "HEAVY": (90.0, "1d6+3"),
    "DANGEROUS": (100.0, "1d6+3"),
}


def run_common(fights: int, seed: int) -> list[dict]:
    rows = []
    serial = 0

    for pct in FIRE_ABSORPTION_LAB:
        base.DEFENSIVE_CURRENT["fuego"]["absorption_pct"] = pct
        row = base.run_one("fuego", True, fights, seed + serial)
        serial += 1
        row.update({
            "profile": "COMMON",
            "candidate": f"FIRE_ABS_{pct:.2f}",
            "candidate_value": pct,
        })
        rows.append(row)

    for pct in WATER_ABSORPTION_LAB:
        base.DEFENSIVE_CURRENT["agua"]["absorption_pct"] = pct
        row = base.run_one("agua", True, fights, seed + serial)
        serial += 1
        row.update({
            "profile": "COMMON",
            "candidate": f"WATER_ABS_{pct:.2f}",
            "candidate_value": pct,
        })
        rows.append(row)

    for evasion, duration in WIND_EVASION_DURATION_LAB:
        base.DEFENSIVE_CURRENT["viento"]["evasion"] = evasion
        base.DEFENSIVE_CURRENT["viento"]["duration"] = duration
        row = base.run_one("viento", True, fights, seed + serial)
        serial += 1
        row.update({
            "profile": "COMMON",
            "candidate": f"WIND_EVA_{int(evasion)}_DUR_{duration}",
            "candidate_value": evasion,
            "candidate_duration": duration,
        })
        rows.append(row)

    return rows


def run_stress(fights: int, seed: int) -> list[dict]:
    rows = []
    serial = 0

    selected = {
        "fuego": {"absorption_pct": 0.25},
        "agua": {"absorption_pct": 0.24},
        "viento": {"evasion": 35.0, "duration": 4},
    }

    for profile_id, (precision, damage) in STRESS_PROFILES.items():
        old_precision = base.ENEMY_PREC
        old_damage = base.ENEMY_DAMAGE
        base.ENEMY_PREC = precision
        base.ENEMY_DAMAGE = damage

        try:
            for root in ("fuego", "agua", "viento"):
                for key, value in selected[root].items():
                    base.DEFENSIVE_CURRENT[root][key] = value

                offense = base.run_one(root, False, fights, seed + serial)
                serial += 1
                defense = base.run_one(root, True, fights, seed + serial)
                serial += 1

                rows.append({
                    "provenance": "LAB",
                    "profile": profile_id,
                    "root": root,
                    "enemy_precision": precision,
                    "enemy_damage": damage,
                    "offense_win_rate": offense["win_rate"],
                    "defense_win_rate": defense["win_rate"],
                    "delta_win_rate": defense["win_rate"] - offense["win_rate"],
                    "offense_hp_remaining": offense["mean_hp_remaining_percent"],
                    "defense_hp_remaining": defense["mean_hp_remaining_percent"],
                    "delta_hp_remaining": (
                        defense["mean_hp_remaining_percent"]
                        - offense["mean_hp_remaining_percent"]
                    ),
                })
        finally:
            base.ENEMY_PREC = old_precision
            base.ENEMY_DAMAGE = old_damage

    return rows


def export(rows: list[dict], path: str) -> None:
    fields = sorted({key for row in rows for key in row})
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--fights", type=int, default=120_000)
    ap.add_argument("--seed", type=int, default=20260929)
    ap.add_argument("--csv", default="lianqi1_defensive_recalibration_lab.csv")
    args = ap.parse_args()

    rows = run_common(args.fights, args.seed)
    rows.extend(run_stress(args.fights, args.seed + 1000))
    export(rows, args.csv)
    print(f"CSV: {args.csv} ({len(rows)} escenarios)")
