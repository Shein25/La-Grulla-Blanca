"""ETAPA 8C — Corteza Endurecida · 3 enemigos.

Compara:
- Piel base PROVISIONAL DEF_CAP2: contribución de Arraigo [1,2,2]
- Piel + Corteza candidata: [2,3,3]

Escenario:
- Tierra HP33 / Qi31 / DEF1 / EVA5
- tres enemigos 10+9+9 HP
- PREC90 / EVA20 / DEF2 / daño 2d4+1
- Piel de apertura
- Golpe de Montaña unitarget
- Peso PROVISIONAL STACK_REFRESH

No modifica runtime ni valores autoritativos.
"""
from __future__ import annotations

RESULT_200K = {
    "BASE_DEF_CAP2": {
        "win_rate": 0.579035,
        "mean_rounds": 7.188095,
        "mean_hp_remaining_percent": 0.1949569697,
        "fallback_rate": 0.931455,
        "mean_max_arraigo": 2.99415,
        "extension_rate": 0.99420,
        "mean_enemy_hits": 11.420085,
        "mean_damage_received": 27.51308,
    },
    "CORTEZA_PLUS1_CAP": {
        "win_rate": 0.700335,
        "mean_rounds": 7.59935,
        "mean_hp_remaining_percent": 0.2882540909,
        "fallback_rate": 0.95857,
        "mean_max_arraigo": 2.921595,
        "extension_rate": 0.923355,
        "mean_enemy_hits": 11.739965,
        "mean_damage_received": 24.16059,
    },
}

SEED_REPLICATIONS_100K = [
    {
        "seed": 20260929,
        "delta_win_pp": 12.239,
        "delta_hp_pp": 9.4034,
        "delta_extension_pp": -7.048,
    },
    {
        "seed": 20261001,
        "delta_win_pp": 12.117,
        "delta_hp_pp": 9.0539,
        "delta_extension_pp": -7.094,
    },
    {
        "seed": 20261017,
        "delta_win_pp": 11.862,
        "delta_hp_pp": 9.0295,
        "delta_extension_pp": -7.156,
    },
    {
        "seed": 20261103,
        "delta_win_pp": 11.947,
        "delta_hp_pp": 9.0913,
        "delta_extension_pp": -7.217,
    },
]

if __name__ == "__main__":
    print("ETAPA 8C — Corteza Endurecida · 3 enemigos")
    print("BASE:", RESULT_200K["BASE_DEF_CAP2"])
    print("CORTEZA:", RESULT_200K["CORTEZA_PLUS1_CAP"])
    print("replicaciones:", SEED_REPLICATIONS_100K)
