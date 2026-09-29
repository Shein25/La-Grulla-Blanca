"""ETAPA 4 — Piel CURRENT vs DEF_CAP2 · 2 enemigos.

Escenario:
- HP enemigo total ~= 28, dividido 14 + 14;
- cada enemigo vivo actúa una vez por ronda;
- PREC90 / EVA20 / DEF2 / daño 2d4+1;
- jugador Tierra HP33 / Qi31 / DEF1 / EVA5;
- Piel como apertura;
- Golpe de Montaña unitarget;
- Peso PROVISIONAL STACK_REFRESH.

Única pregunta:
¿cuánto recorta DEF_CAP2 el escalado de Piel al recibir dos acciones enemigas?

No modifica runtime ni valores autoritativos.
"""

ETAPA = 4
PROVENANCE = "LAB"

RESULT_200K = {
    "CURRENT": {
        "win_rate": 0.88831,
        "mean_rounds": 7.246745,
        "mean_hp_remaining_percent": 0.4651618182,
        "fallback_rate": 0.820555,
        "mean_max_arraigo": 2.957395,
        "mean_enemy_hits": 7.872935,
        "mean_damage_received": 17.88901,
        "extension_rate": 0.95888,
    },
    "DEF_CAP2": {
        "win_rate": 0.849065,
        "mean_rounds": 7.147475,
        "mean_hp_remaining_percent": 0.4097366667,
        "fallback_rate": 0.81935,
        "mean_max_arraigo": 2.957435,
        "mean_enemy_hits": 7.817555,
        "mean_damage_received": 19.80753,
        "extension_rate": 0.95902,
    },
}

SEED_REPLICATIONS_100K = [
    {"seed": 20260929, "delta_win_pp": -4.040, "delta_hp_pp": -5.535},
    {"seed": 20261001, "delta_win_pp": -3.947, "delta_hp_pp": -5.490},
    {"seed": 20261017, "delta_win_pp": -3.766, "delta_hp_pp": -5.440},
    {"seed": 20261103, "delta_win_pp": -3.882, "delta_hp_pp": -5.578},
]

if __name__ == "__main__":
    print("ETAPA 4 — CURRENT vs DEF_CAP2 · 2 enemigos")
    print("CURRENT:", RESULT_200K["CURRENT"])
    print("DEF_CAP2:", RESULT_200K["DEF_CAP2"])
    print("replicaciones:", SEED_REPLICATIONS_100K)
