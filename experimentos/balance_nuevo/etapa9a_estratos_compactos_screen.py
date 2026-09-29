"""ETAPA 9A — Estratos Compactos · screen estructural 1v1.

Objetivo:
evitar una escalera permanente hacia DEF7+ y probar una fortificación por
ventanas que funcione con o sin Corteza Endurecida.

Candidato LAB: ESTRATO_REACTIVO_2
- Piel debe estar activa.
- Cuando Arraigo aumenta y el nuevo valor es 2 o 3, gana/refresca 1 Estrato.
- Máximo 1 Estrato almacenado.
- El siguiente impacto directo conectado recibe +2 DEF sólo para ese impacto.
- Después del impacto conectado, el Estrato se consume.
- Una evasión no consume Estrato.
- Si el trigger fuerte salta 1 -> 3, crea un solo Estrato.
- No modifica Tenacidad, duración ni máximo de Arraigo.
- No modifica la curva permanente DEF_CAP2/Corteza.

Este runner es LAB y no modifica runtime.
"""

PROVENANCE = "LAB"
CANDIDATE = "ESTRATO_REACTIVO_2"

CURVES = {
    "PIEL_BASE": [1, 2, 2],
    "PIEL_CORTEZA": [2, 3, 3],
}

# Resultados del screen reproducible inicial, 50.000 combates,
# seed 20260929. Se conservan aquí como checkpoint del experimento.
RESULTS_50K = {
    "COMMON_2d4+1": {
        "PIEL_BASE": {
            "without_estratos_win": 0.95602,
            "with_estratos_win": 0.96100,
            "without_estratos_hp": 0.5842969697,
            "with_estratos_hp": 0.6056945455,
            "mean_estrato_uses": 1.16428,
        },
        "PIEL_CORTEZA": {
            "without_estratos_win": 0.96374,
            "with_estratos_win": 0.96306,
            "without_estratos_hp": 0.6162454545,
            "with_estratos_hp": 0.6170709091,
            "mean_estrato_uses": 0.91738,
        },
    },
    "HEAVY_1d6+3": {
        "PIEL_BASE": {
            "without_estratos_win": 0.92990,
            "with_estratos_win": 0.93918,
            "without_estratos_hp": 0.5297521212,
            "with_estratos_hp": 0.5607121212,
            "mean_estrato_uses": 1.18300,
        },
        "PIEL_CORTEZA": {
            "without_estratos_win": 0.94306,
            "with_estratos_win": 0.94552,
            "without_estratos_hp": 0.5721418182,
            "with_estratos_hp": 0.5841848485,
            "mean_estrato_uses": 1.01358,
        },
    },
}

if __name__ == "__main__":
    print("ETAPA 9A — Estratos Compactos")
    print("Candidato:", CANDIDATE)
    for profile, variants in RESULTS_50K.items():
        print(profile)
        for name, row in variants.items():
            print(" ", name, row)
