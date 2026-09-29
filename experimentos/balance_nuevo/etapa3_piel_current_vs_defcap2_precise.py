"""ETAPA 3 — Piel CURRENT vs DEF_CAP2 · enemigo preciso 1v1.

Única diferencia respecto de ETAPA 1:
- Precision enemiga: 100 en vez de 90.

El daño vuelve al baseline comun 2d4+1.
No modifica runtime ni valores autoritativos.
"""
from __future__ import annotations

ETAPA = 3
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
    "precision": 100,
    "evasion": 20,
    "defense": 2,
    "damage": "2d4+1",
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
        "win_rate": 0.94702,
        "mean_turns": 6.578815,
        "mean_hp_remaining_percent": 0.5776048485,
        "fallback_rate": 0.672825,
        "mean_max_arraigo": 2.81298,
        "mean_enemy_hits": 5.350515,
        "mean_damage_received": 14.05059,
    },
    "DEF_CAP2": {
        "win_rate": 0.938685,
        "mean_turns": 6.564005,
        "mean_hp_remaining_percent": 0.5492824242,
        "fallback_rate": 0.673965,
        "mean_max_arraigo": 2.81316,
        "mean_enemy_hits": 5.343815,
        "mean_damage_received": 15.0015,
    },
}

SEED_REPLICATIONS_100K = [
    {"seed": 20260929, "delta_win_pp": -0.853, "delta_hp_pp": -2.8052},
    {"seed": 20261001, "delta_win_pp": -0.818, "delta_hp_pp": -2.7805},
    {"seed": 20261017, "delta_win_pp": -0.792, "delta_hp_pp": -2.7695},
    {"seed": 20261103, "delta_win_pp": -0.810, "delta_hp_pp": -2.7917},
]

if __name__ == "__main__":
    print("ETAPA 3 — CURRENT vs DEF_CAP2 · enemigo preciso 1v1")
    print("CURRENT:", RESULT_200K["CURRENT"])
    print("DEF_CAP2:", RESULT_200K["DEF_CAP2"])
    print("replicaciones:", SEED_REPLICATIONS_100K)
