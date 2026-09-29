"""ETAPA 2 — Piel CURRENT vs DEF_CAP2 · enemigo pesado 1v1.

Única diferencia respecto de ETAPA 1:
- ataque enemigo: 1d6+3 en vez de 2d4+1.

El resto del baseline se conserva.
Este archivo documenta el escenario reproducible; no modifica runtime.
"""
from __future__ import annotations

ETAPA = 2
PROVENANCE = "LAB"

PLAYER = {
    "root": "tierra",
    "hp_base": 30,
    "hp_effective": 33,
    "qi_max": 31,
    "defense": 1,
    "evasion": 5,
}

ENEMY = {
    "hp": 28,
    "precision": 90,
    "evasion": 20,
    "defense": 2,
    "damage": "1d6+3",
}

PIEL_CURRENT = {
    "immediate_defense": 2,
    "initial_arraigo": 1,
    "max_arraigo": 3,
    "def_per_arraigo": [0, 1, 2, 3],
    "extend_on_max": True,
}

PIEL_DEF_CAP2 = {
    "immediate_defense": 2,
    "initial_arraigo": 1,
    "max_arraigo": 3,
    "def_per_arraigo": [0, 1, 2, 2],
    "extend_on_max": True,
}

RESULT_200K = {
    "CURRENT": {
        "win_rate": 0.93913,
        "mean_turns": 6.559705,
        "mean_hp_remaining_percent": 0.5592351515,
        "fallback_rate": 0.67279,
        "mean_max_arraigo": 2.79917,
        "mean_enemy_hits": 4.77741,
        "mean_damage_received": 14.687815,
    },
    "DEF_CAP2": {
        "win_rate": 0.92961,
        "mean_turns": 6.53461,
        "mean_hp_remaining_percent": 0.5314548485,
        "fallback_rate": 0.671655,
        "mean_max_arraigo": 2.798485,
        "mean_enemy_hits": 4.76212,
        "mean_damage_received": 15.625345,
    },
}

SEED_REPLICATIONS_100K = [
    {"seed": 20260929, "delta_win_pp": -0.8980, "delta_hp_pp": -2.7552},
    {"seed": 20261001, "delta_win_pp": -0.8950, "delta_hp_pp": -2.8505},
    {"seed": 20261017, "delta_win_pp": -1.0130, "delta_hp_pp": -2.8672},
    {"seed": 20261103, "delta_win_pp": -1.0130, "delta_hp_pp": -2.7909},
]

if __name__ == "__main__":
    print("ETAPA 2 — CURRENT vs DEF_CAP2 · enemigo pesado 1v1")
    print("CURRENT:", RESULT_200K["CURRENT"])
    print("DEF_CAP2:", RESULT_200K["DEF_CAP2"])
    print("replicaciones:", SEED_REPLICATIONS_100K)
