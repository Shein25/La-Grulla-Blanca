"""ETAPA 9C — Estratos Compactos · 3 enemigos.

Compara ESTRATO_REACTIVO_2 con/sin Corteza:
- Piel base PROVISIONAL: contribución Arraigo [1,2,2]
- Piel + Corteza PROVISIONAL: [2,3,3]

Estrato:
- al aumentar Arraigo y quedar en 2 o 3: gana/refresca 1 Estrato;
- máximo 1;
- siguiente impacto directo conectado: +2 DEF sólo para ese impacto;
- se consume al conectar;
- evasión no consume;
- salto 1->3 genera un solo Estrato.

Escenario:
- Tierra HP33 / Qi31 / DEF1 / EVA5
- 3 enemigos 10+9+9 HP
- PREC90 / EVA20 / DEF2 / daño 2d4+1
- Piel de apertura
- Golpe de Montaña unitarget
- Peso PROVISIONAL STACK_REFRESH

No modifica runtime.
"""
from __future__ import annotations

RESULT_200K = {
    "PIEL_BASE": {
        "win_rate": 0.579035,
        "mean_hp_remaining_percent": 0.1949569697,
        "extension_rate": 0.99420,
    },
    "PIEL_BASE_ESTRATOS": {
        "win_rate": 0.62430,
        "mean_hp_remaining_percent": 0.2273087879,
        "extension_rate": 0.98819,
        "mean_estrato_uses": 1.72118,
        "mean_estrato_generated": 1.72263,
    },
    "CORTEZA": {
        "win_rate": 0.700335,
        "mean_hp_remaining_percent": 0.2882540909,
        "extension_rate": 0.923355,
    },
    "CORTEZA_ESTRATOS": {
        "win_rate": 0.717135,
        "mean_hp_remaining_percent": 0.3053227273,
        "extension_rate": 0.885905,
        "mean_estrato_uses": 1.73611,
        "mean_estrato_generated": 1.742005,
    },
}

REPLICATIONS_50K = [
    {
        "seed": 20260929,
        "base_delta_win_pp": 4.546,
        "base_delta_hp_pp": 3.254,
        "corteza_delta_win_pp": 1.546,
        "corteza_delta_hp_pp": 1.681,
    },
    {
        "seed": 20261001,
        "base_delta_win_pp": 4.624,
        "base_delta_hp_pp": 3.118,
        "corteza_delta_win_pp": 1.728,
        "corteza_delta_hp_pp": 1.667,
    },
    {
        "seed": 20261017,
        "base_delta_win_pp": 4.534,
        "base_delta_hp_pp": 3.279,
        "corteza_delta_win_pp": 1.904,
        "corteza_delta_hp_pp": 1.857,
    },
    {
        "seed": 20261103,
        "base_delta_win_pp": 4.056,
        "base_delta_hp_pp": 2.999,
        "corteza_delta_win_pp": 1.730,
        "corteza_delta_hp_pp": 1.762,
    },
]

if __name__ == "__main__":
    print("ETAPA 9C — Estratos Compactos · 3 enemigos")
    for name, row in RESULT_200K.items():
        print(name, row)
    print("replicaciones:", REPLICATIONS_50K)
