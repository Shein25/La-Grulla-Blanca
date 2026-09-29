"""ETAPA 8B — Corteza Endurecida · 2 enemigos.

Compara:
- Piel base PROVISIONAL DEF_CAP2: Arraigo DEF acumulada [1,2,2]
- Piel + Corteza candidata: [2,3,3]

Escenario:
- Tierra HP33 / Qi31 / DEF1 / EVA5
- dos enemigos 14+14 HP
- PREC90 / EVA20 / DEF2 / daño 2d4+1
- Piel se usa de apertura
- Golpe de Montaña unitarget
- Peso PROVISIONAL STACK_REFRESH

No modifica runtime ni valores autoritativos.
"""
from __future__ import annotations

RESULT_200K = {
    "BASE_DEF_CAP2": {
        "win_rate": 0.849065,
        "mean_rounds": 7.147475,
        "mean_hp_remaining_percent": 0.4097366667,
        "fallback_rate": 0.81935,
        "mean_max_arraigo": 2.957435,
        "extension_rate": 0.95902,
        "mean_enemy_hits": 7.817555,
        "mean_damage_received": 19.80753,
    },
    "CORTEZA_PLUS1_CAP": {
        "win_rate": 0.894085,
        "mean_rounds": 7.25981,
        "mean_hp_remaining_percent": 0.4854942424,
        "fallback_rate": 0.82041,
        "mean_max_arraigo": 2.77087,
        "extension_rate": 0.78441,
        "mean_enemy_hits": 7.87863,
        "mean_damage_received": 17.204495,
    },
}

SEED_REPLICATIONS_100K = [
    {
        "seed": 20260929,
        "delta_win_pp": 4.611,
        "delta_hp_pp": 7.539,
        "delta_extension_pp": -17.537,
    },
    {
        "seed": 20261001,
        "delta_win_pp": 4.592,
        "delta_hp_pp": 7.607,
        "delta_extension_pp": -17.223,
    },
    {
        "seed": 20261017,
        "delta_win_pp": 4.531,
        "delta_hp_pp": 7.488,
        "delta_extension_pp": -17.319,
    },
    {
        "seed": 20261103,
        "delta_win_pp": 4.562,
        "delta_hp_pp": 7.584,
        "delta_extension_pp": -17.463,
    },
]

if __name__ == "__main__":
    print("ETAPA 8B — Corteza Endurecida · 2 enemigos")
    print("BASE:", RESULT_200K["BASE_DEF_CAP2"])
    print("CORTEZA:", RESULT_200K["CORTEZA_PLUS1_CAP"])
    print("replicaciones:", SEED_REPLICATIONS_100K)
