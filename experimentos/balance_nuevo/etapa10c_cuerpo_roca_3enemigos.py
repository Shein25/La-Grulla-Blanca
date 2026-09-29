"""ETAPA 10C — Cuerpo de Roca · 3 enemigos.

Candidato:
ROCA_GUARD_MAX_3
- Piel activa y Arraigo == 3;
- al comienzo de cada turno del usuario se arma 1 Guardia;
- primer impacto directo conectado del turno recibe +3 DEF;
- evasión no consume;
- alcanzar Arraigo3 durante las acciones enemigas no arma retroactivamente.

Escenario:
- Tierra HP33 / Qi31 / DEF1 / EVA5
- 3 enemigos 10+9+9 HP
- PREC90 / EVA20 / DEF2 / daño 2d4+1
- Golpe de Montaña unitarget
- Peso PROVISIONAL STACK_REFRESH

No modifica runtime.
"""
from __future__ import annotations

RESULT_200K = {
    "PIEL_BASE": {
        "win_rate": 0.579035,
        "mean_rounds": 7.188095,
        "mean_hp_remaining_percent": 0.1949569697,
        "extension_rate": 0.99420,
        "mean_max_arraigo": 2.99415,
    },
    "PIEL_BASE_ROCA": {
        "win_rate": 0.66348,
        "mean_rounds": 7.46668,
        "mean_hp_remaining_percent": 0.2567454545,
        "extension_rate": 0.994345,
        "mean_max_arraigo": 2.99428,
        "mean_roca_uses": 2.64790,
    },
    "CORTEZA_ESTRATOS": {
        "win_rate": 0.717135,
        "mean_rounds": 7.65474,
        "mean_hp_remaining_percent": 0.3053227273,
        "extension_rate": 0.885905,
        "mean_max_arraigo": 2.88413,
        "mean_estrato_uses": 1.73611,
    },
    "CORTEZA_ESTRATOS_ROCA": {
        "win_rate": 0.73873,
        "mean_rounds": 7.72526,
        "mean_hp_remaining_percent": 0.3289363636,
        "extension_rate": 0.885195,
        "mean_max_arraigo": 2.88330,
        "mean_estrato_uses": 1.735785,
        "mean_roca_uses": 1.870145,
    },
}

REPLICATIONS_50K = [
    {
        "seed": 20260929,
        "base_delta_win_pp": 8.388,
        "base_delta_hp_pp": 6.1472,
        "full_delta_win_pp": 2.562,
        "full_delta_hp_pp": 2.4567,
        "base_roca_uses": 2.6437,
        "full_roca_uses": 1.8709,
    },
    {
        "seed": 20261001,
        "base_delta_win_pp": 8.506,
        "base_delta_hp_pp": 6.1292,
        "full_delta_win_pp": 2.100,
        "full_delta_hp_pp": 2.3754,
        "base_roca_uses": 2.6462,
        "full_roca_uses": 1.8745,
    },
    {
        "seed": 20261017,
        "base_delta_win_pp": 8.098,
        "base_delta_hp_pp": 5.9990,
        "full_delta_win_pp": 2.088,
        "full_delta_hp_pp": 2.3456,
        "base_roca_uses": 2.6509,
        "full_roca_uses": 1.8756,
    },
    {
        "seed": 20261103,
        "base_delta_win_pp": 8.256,
        "base_delta_hp_pp": 6.0713,
        "full_delta_win_pp": 2.256,
        "full_delta_hp_pp": 2.4581,
        "base_roca_uses": 2.6494,
        "full_roca_uses": 1.8779,
    },
]

if __name__ == "__main__":
    print("ETAPA 10C — Cuerpo de Roca · 3 enemigos")
    for name, row in RESULT_200K.items():
        print(name, row)
    print("replicaciones:", REPLICATIONS_50K)
