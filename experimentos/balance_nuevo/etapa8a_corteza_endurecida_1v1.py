"""ETAPA 8A — Corteza Endurecida · selección de curva 1v1 común.

Pregunta única:
¿qué curva de DEF para Corteza mejora Piel sobre DEF_CAP2 sin reabrir
el problema de la tercera carga ni volver a la progresión antigua?

Se prueban:
- BASE_DEF_CAP2: contribución Arraigo [1,2,2]
- CORTEZA_PLUS1_CAP: [2,3,3]
- CORTEZA_DOUBLE_CAP: [2,4,4]
- CORTEZA_PROGRESSIVE: [2,3,4]

Escenario:
Tierra HP33 / Qi31 / DEF1 / EVA5
vs enemigo común HP28 / PREC90 / EVA20 / DEF2 / 2d4+1.
"""
from __future__ import annotations

CURVES_LAB = {
    "BASE_DEF_CAP2": [0, 1, 2, 2],
    "CORTEZA_PLUS1_CAP": [0, 2, 3, 3],
    "CORTEZA_DOUBLE_CAP": [0, 2, 4, 4],
    "CORTEZA_PROGRESSIVE": [0, 2, 3, 4],
}

RESULT_100K_SEED_20260929 = {
    "BASE_DEF_CAP2": {
        "win_rate": 0.95556,
        "mean_hp_remaining_percent": 0.5839415,
        "mean_max_arraigo": 2.72101,
        "extension_rate": 0.74850,
    },
    "CORTEZA_PLUS1_CAP": {
        "win_rate": 0.96320,
        "mean_hp_remaining_percent": 0.6152667,
        "mean_max_arraigo": 2.36951,
        "extension_rate": 0.46304,
    },
    "CORTEZA_DOUBLE_CAP": {
        "win_rate": 0.96374,
        "mean_hp_remaining_percent": 0.6185673,
        "mean_max_arraigo": 2.23076,
        "extension_rate": 0.32502,
    },
    "CORTEZA_PROGRESSIVE": {
        "win_rate": 0.96546,
        "mean_hp_remaining_percent": 0.6243376,
        "mean_max_arraigo": 2.36810,
        "extension_rate": 0.46248,
    },
}

REPLICATION_PLUS1_CAP = [
    {"seed": 20260929, "delta_win_pp": +0.764, "delta_hp_pp": +3.133},
    {"seed": 20261001, "delta_win_pp": +0.563, "delta_hp_pp": +2.987},
    {"seed": 20261017, "delta_win_pp": +0.659, "delta_hp_pp": +3.044},
    {"seed": 20261103, "delta_win_pp": +0.535, "delta_hp_pp": +3.048},
]

if __name__ == "__main__":
    print("ETAPA 8A — Corteza Endurecida · 1v1 común")
    for name, row in RESULT_100K_SEED_20260929.items():
        print(name, row)
    print("Replicaciones CORTEZA_PLUS1_CAP vs BASE:", REPLICATION_PLUS1_CAP)
