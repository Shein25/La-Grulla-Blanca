"""ETAPA 10A — Cuerpo de Roca · screen estructural 1v1.

Objetivo:
diseñar el Tramo III de fortificación sin crear DEF7+ permanente.

Candidato principal LAB:
ROCA_GUARD_MAX_3
- Piel debe estar activa.
- Requiere Arraigo == 3.
- El primer impacto directo conectado contra el usuario en cada turno propio
  recibe +3 DEF sólo para ese impacto.
- Después queda consumido para ese turno.
- Una evasión no lo consume.
- Se rearma al comenzar el siguiente turno propio si Piel sigue activa y
  Arraigo sigue en 3.
- No aumenta DEF permanente.
- No modifica Tenacidad, duración ni máximo de Arraigo.
- Funciona con o sin Corteza/Estratos.

Screen comparó +2/+3/+4 y condición Arraigo>=2 vs Arraigo==3.
La condición >=2 se descartó por interferir demasiado con generación de
Arraigo/extensión. +3 se selecciona por retorno marginal frente a +4.
"""

PROVENANCE = "LAB"
CANDIDATE = "ROCA_GUARD_MAX_3"

SCREEN_30K_SEED_20260929 = {
    "COMMON_2d4+1": {
        "PIEL_BASE": {
            "+2": {"win": 0.96660, "hp": 0.6221071},
            "+3": {"win": 0.96807, "hp": 0.6301081},
            "+4": {"win": 0.96860, "hp": 0.6329929},
        },
        "CORTEZA_ESTRATOS": {
            "baseline": {"win": 0.96410, "hp": 0.6172434},
            "+2": {"win": 0.96517, "hp": 0.6213990},
            "+3": {"win": 0.96520, "hp": 0.6220758},
            "+4": {"win": 0.96523, "hp": 0.6222505},
        },
    },
    "HEAVY_1d6+3": {
        "PIEL_BASE": {
            "+2": {"win": 0.94327, "hp": 0.5788263},
            "+3": {"win": 0.94667, "hp": 0.5943465},
            "+4": {"win": 0.95000, "hp": 0.6023545},
        },
        "CORTEZA_ESTRATOS": {
            "baseline": {"win": 0.94443, "hp": 0.5833444},
            "+2": {"win": 0.94743, "hp": 0.5955081},
            "+3": {"win": 0.94803, "hp": 0.5975758},
            "+4": {"win": 0.94807, "hp": 0.5979172},
        },
    },
}

REPLICATIONS_40K = {
    "COMMON_STANDALONE_PLUS3": [
        {"seed": 20260929, "delta_win_pp": 1.1050, "delta_hp_pp": 4.4907, "mean_uses": 1.2191},
        {"seed": 20261001, "delta_win_pp": 1.0075, "delta_hp_pp": 4.4580, "mean_uses": 1.2151},
        {"seed": 20261017, "delta_win_pp": 1.0125, "delta_hp_pp": 4.4170, "mean_uses": 1.2146},
        {"seed": 20261103, "delta_win_pp": 1.0000, "delta_hp_pp": 4.4695, "mean_uses": 1.2219},
    ],
    "COMMON_FULL_ROUTE_PLUS3": [
        {"seed": 20260929, "delta_win_pp": 0.1100, "delta_hp_pp": 0.4861, "mean_uses": 0.4446},
        {"seed": 20261001, "delta_win_pp": 0.0875, "delta_hp_pp": 0.4803, "mean_uses": 0.4453},
        {"seed": 20261017, "delta_win_pp": 0.0750, "delta_hp_pp": 0.4361, "mean_uses": 0.4427},
        {"seed": 20261103, "delta_win_pp": 0.0650, "delta_hp_pp": 0.4330, "mean_uses": 0.4508},
    ],
    "HEAVY_STANDALONE_PLUS3": [
        {"seed": 20260929, "delta_win_pp": 1.7725, "delta_hp_pp": 6.5481, "mean_uses": 1.4735},
        {"seed": 20261001, "delta_win_pp": 1.8600, "delta_hp_pp": 6.5952, "mean_uses": 1.4669},
        {"seed": 20261017, "delta_win_pp": 2.1250, "delta_hp_pp": 6.5882, "mean_uses": 1.4695},
        {"seed": 20261103, "delta_win_pp": 1.7850, "delta_hp_pp": 6.3248, "mean_uses": 1.4730},
    ],
    "HEAVY_FULL_ROUTE_PLUS3": [
        {"seed": 20260929, "delta_win_pp": 0.3350, "delta_hp_pp": 1.4177, "mean_uses": 0.7972},
        {"seed": 20261001, "delta_win_pp": 0.3250, "delta_hp_pp": 1.3965, "mean_uses": 0.7976},
        {"seed": 20261017, "delta_win_pp": 0.3175, "delta_hp_pp": 1.3505, "mean_uses": 0.8041},
        {"seed": 20261103, "delta_win_pp": 0.3375, "delta_hp_pp": 1.3544, "mean_uses": 0.7985},
    ],
}

if __name__ == "__main__":
    print("ETAPA 10A — Cuerpo de Roca")
    print("Candidato:", CANDIDATE)
    print("Screen:", SCREEN_30K_SEED_20260929)
    print("Replicaciones:", REPLICATIONS_40K)
