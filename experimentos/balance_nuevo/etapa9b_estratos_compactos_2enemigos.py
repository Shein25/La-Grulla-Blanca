"""ETAPA 9B — Estratos Compactos · 2 enemigos.

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
- 2 enemigos 14+14 HP
- PREC90 / EVA20 / DEF2 / daño 2d4+1
- Piel de apertura
- Golpe de Montaña unitarget
- Peso PROVISIONAL STACK_REFRESH

No modifica runtime.
"""
from __future__ import annotations

RESULT_200K = {
    "PIEL_BASE": {
        "win_rate": 0.849065,
        "mean_hp_remaining_percent": 0.4097366667,
        "extension_rate": 0.95902,
    },
    "PIEL_BASE_ESTRATOS": {
        "win_rate": 0.873005,
        "mean_hp_remaining_percent": 0.4500751515,
        "extension_rate": 0.918035,
        "mean_estrato_uses": 1.62744,
        "mean_estrato_generated": 1.648105,
    },
    "CORTEZA": {
        "win_rate": 0.894085,
        "mean_hp_remaining_percent": 0.4854942424,
        "extension_rate": 0.78441,
    },
    "CORTEZA_ESTRATOS": {
        "win_rate": 0.89896,
        "mean_hp_remaining_percent": 0.4996483333,
        "extension_rate": 0.69182,
        "mean_estrato_uses": 1.49611,
        "mean_estrato_generated": 1.53770,
    },
}

REPLICATIONS_50K = [
    {
        "seed": 20260929,
        "base_delta_win_pp": 2.410,
        "base_delta_hp_pp": 4.046,
        "corteza_delta_win_pp": 0.654,
        "corteza_delta_hp_pp": 1.460,
    },
    {
        "seed": 20261001,
        "base_delta_win_pp": 2.386,
        "base_delta_hp_pp": 4.081,
        "corteza_delta_win_pp": 0.518,
        "corteza_delta_hp_pp": 1.493,
    },
    {
        "seed": 20261017,
        "base_delta_win_pp": 2.478,
        "base_delta_hp_pp": 4.019,
        "corteza_delta_win_pp": 0.722,
        "corteza_delta_hp_pp": 1.740,
    },
    {
        "seed": 20261103,
        "base_delta_win_pp": 2.510,
        "base_delta_hp_pp": 4.243,
        "corteza_delta_win_pp": 0.374,
        "corteza_delta_hp_pp": 1.327,
    },
]

if __name__ == "__main__":
    print("ETAPA 9B — Estratos Compactos · 2 enemigos")
    for name, row in RESULT_200K.items():
        print(name, row)
    print("replicaciones:", REPLICATIONS_50K)
