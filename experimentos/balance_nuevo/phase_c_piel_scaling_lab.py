"""PHASE C LAB — escalado multi-impacto de Piel de Cobre.

Compara alternativas LAB de contribución de DEF por Arraigo manteniendo:
- +2 DEF inmediata;
- 1 Arraigo al activar;
- máximo 3;
- Tenacidad conceptual por stack;
- trigger reactivo por acción;
- extensión al alcanzar máximo, salvo variante explícita.

No modifica la técnica autoritativa.
"""
from __future__ import annotations

import argparse
import csv
import math

# Este laboratorio parte del runner multi-enemigo y se implementa como una
# matriz declarativa para reproducir las variantes de diseño.
VARIANTS_LAB = {
    "CURRENT": {
        "arraigo_def_curve": [0, 1, 2, 3],
        "extend_on_max": True,
    },
    "DEF_CAP2": {
        # Arraigo 1 => +1 DEF; Arraigo 2/3 => máximo +2 DEF.
        "arraigo_def_curve": [0, 1, 2, 2],
        "extend_on_max": True,
    },
    "DEF_DIMINISHING": {
        # Arraigo 1/2 => +1 DEF; Arraigo 3 => +2 DEF.
        "arraigo_def_curve": [0, 1, 1, 2],
        "extend_on_max": True,
    },
    "NO_EXTENSION": {
        "arraigo_def_curve": [0, 1, 2, 3],
        "extend_on_max": False,
    },
    "DIMINISHING_NO_EXTENSION": {
        "arraigo_def_curve": [0, 1, 1, 2],
        "extend_on_max": False,
    },
}

ENEMY_COUNTS = (1, 2, 3)
TOTAL_ENEMY_HP = 28


def expected_defense(base_def: float, immediate_def: float, stacks: int, variant: str) -> float:
    curve = VARIANTS_LAB[variant]["arraigo_def_curve"]
    return base_def + immediate_def + curve[stacks]


def describe() -> list[dict]:
    rows = []
    for variant, cfg in VARIANTS_LAB.items():
        for stacks in (1, 2, 3):
            rows.append({
                "provenance": "LAB",
                "variant": variant,
                "stacks": stacks,
                "base_def": 1.0,
                "immediate_def": 2.0,
                "arraigo_def": cfg["arraigo_def_curve"][stacks],
                "total_def": expected_defense(1.0, 2.0, stacks, variant),
                "extend_on_max": cfg["extend_on_max"],
            })
    return rows


def export(rows: list[dict], path: str) -> None:
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default="lianqi1_piel_scaling_variants_lab.csv")
    args = ap.parse_args()

    rows = describe()
    export(rows, args.csv)

    print("Este archivo declara las curvas a usar junto al runner multi-enemigo.")
    for row in rows:
        print(row)
