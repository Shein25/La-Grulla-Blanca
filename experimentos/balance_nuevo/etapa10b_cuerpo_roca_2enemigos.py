"""ETAPA 10B — Cuerpo de Roca · 2 enemigos.

Candidato LAB:
ROCA_GUARD_MAX_3
- requiere Piel activa y Arraigo == 3;
- al comienzo de cada turno del usuario se arma 1 Guardia si sigue en Arraigo3;
- el primer impacto directo conectado de ese turno recibe +3 DEF;
- una evasión no consume la Guardia;
- alcanzar Arraigo3 durante las acciones enemigas NO arma retroactivamente
  la Guardia: se arma en el siguiente turno del usuario.

Comparaciones:
1) Piel base
2) Piel base + Cuerpo de Roca
3) ruta Corteza + Estratos
4) ruta Corteza + Estratos + Cuerpo de Roca

Escenario:
- Tierra HP33 / Qi31 / DEF1 / EVA5
- 2 enemigos 14+14 HP
- PREC90 / EVA20 / DEF2 / daño 2d4+1
- Golpe de Montaña unitarget
- Peso PROVISIONAL STACK_REFRESH

No modifica runtime.
"""
from __future__ import annotations

RESULT_200K = {
    "PIEL_BASE": {
        "win_rate": 0.849065,
        "mean_rounds": 7.147475,
        "mean_hp_remaining_percent": 0.4097366667,
        "extension_rate": 0.95902,
        "mean_max_arraigo": 2.957435,
    },
    "PIEL_BASE_ROCA": {
        "win_rate": 0.89056,
        "mean_rounds": 7.25213,
        "mean_hp_remaining_percent": 0.4797713636,
        "extension_rate": 0.95875,
        "mean_max_arraigo": 2.957145,
        "mean_roca_uses": 2.155845,
    },
    "CORTEZA_ESTRATOS": {
        "win_rate": 0.89896,
        "mean_rounds": 7.271535,
        "mean_hp_remaining_percent": 0.4996483333,
        "extension_rate": 0.69182,
        "mean_max_arraigo": 2.67856,
        "mean_estrato_uses": 1.49611,
    },
    "CORTEZA_ESTRATOS_ROCA": {
        "win_rate": 0.90647,
        "mean_rounds": 7.286455,
        "mean_hp_remaining_percent": 0.5162527273,
        "extension_rate": 0.691365,
        "mean_max_arraigo": 2.67776,
        "mean_estrato_uses": 1.495085,
        "mean_roca_uses": 1.19377,
    },
}

REPLICATIONS_50K = [
    {
        "seed": 20260929,
        "base_delta_win_pp": 4.238,
        "base_delta_hp_pp": 6.918,
        "full_delta_win_pp": 0.640,
        "full_delta_hp_pp": 1.617,
        "base_roca_uses": 2.1529,
        "full_roca_uses": 1.1945,
    },
    {
        "seed": 20261001,
        "base_delta_win_pp": 4.114,
        "base_delta_hp_pp": 6.941,
        "full_delta_win_pp": 0.786,
        "full_delta_hp_pp": 1.646,
        "base_roca_uses": 2.1561,
        "full_roca_uses": 1.1883,
    },
    {
        "seed": 20261017,
        "base_delta_win_pp": 4.146,
        "base_delta_hp_pp": 6.867,
        "full_delta_win_pp": 0.674,
        "full_delta_hp_pp": 1.534,
        "base_roca_uses": 2.1489,
        "full_roca_uses": 1.1969,
    },
    {
        "seed": 20261103,
        "base_delta_win_pp": 4.168,
        "base_delta_hp_pp": 7.129,
        "full_delta_win_pp": 0.708,
        "full_delta_hp_pp": 1.660,
        "base_roca_uses": 2.1531,
        "full_roca_uses": 1.1860,
    },
]

if __name__ == "__main__":
    print("ETAPA 10B — Cuerpo de Roca · 2 enemigos")
    for name, row in RESULT_200K.items():
        print(name, row)
    print("replicaciones:", REPLICATIONS_50K)
