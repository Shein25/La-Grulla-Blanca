"""ETAPA 15C — Screen conjunto final de las cinco defensivas completas.

Este archivo NO vuelve a simular las cinco técnicas.
Agrega los rangos ya cerrados por sus runners autoritativos:

- ETAPA 11 Cuerpo-Horno
- ETAPA 12 Espejo de Luna
- ETAPA 13 Paso de Nube
- ETAPA 14 Armadura de Plata
- ETAPA 15B Piel de Cobre

Objetivo:
comparar estructura/nichos sin fingir que los porcentajes absolutos de rutas
LianQi II-IV contra enemigos LianQi I constituyen balance final por etapa.

No modifica runtime.
"""
from __future__ import annotations

import csv

SOURCES = {
    "fuego": "ETAPA11_CUERPO_HORNO_COMPLETO_2026-09-29.md",
    "metal": "ETAPA14_ARMADURA_PLATA_COMPLETA_2026-09-29.md",
    "agua": "ETAPA12_ESPEJO_LUNA_COMPLETO_2026-09-29.md",
    "tierra": "ETAPA15B_PIEL_COBRE_COMPLETA_2026-09-29.md",
    "viento": "ETAPA13_PASO_NUBE_COMPLETO_2026-09-29.md",
}

# Rangos 27/27 ya registrados en los documentos fuente.
# Para Fuego, los documentos sólo publican rango 27/27 de COMMON/2EN/3EN;
# los otros perfiles tienen muestras representativas, por lo que no se
# inventan rangos completos.
RANGES = {
    "COMMON": {
        "fuego": (95.86, 97.23),
        "metal": (93.19, 98.55),
        "agua": (89.74, 92.84),
        "tierra": (95.71, 99.11),
        "viento": (90.31, 93.45),
    },
    "2EN": {
        "fuego": (68.76, 80.05),
        "metal": (56.94, 83.20),
        "agua": (40.33, 59.28),
        "tierra": (84.84, 96.16),
        "viento": (65.35, 78.30),
    },
    "3EN": {
        "fuego": (30.03, 50.18),
        "metal": (11.38, 34.03),
        "agua": (4.60, 12.44),
        "tierra": (59.06, 87.01),
        "viento": (31.24, 50.33),
    },
}

STRUCTURAL_GUARDS = {
    "fuego": [
        "absorption_pool_finite",
        "heat_cap_finite",
        "heat_no_recursive_scaling",
        "efficiency_qi_rebenchmark_future",
    ],
    "metal": [
        "plates_sequential_not_stacked",
        "finite_plate_count",
        "duration_4_cap",
        "control_adaptation_requires_real_control_retest",
    ],
    "agua": [
        "finite_absorption_pool",
        "reflow_requires_surviving_pool",
        "reconstruction_once_per_activation",
        "qi_refund_explicit_not_passive_regen",
    ],
    "tierra": [
        "DEF_CAP2",
        "estrato_max_1",
        "roca_max_1_guard_per_turn",
        "AGUANTE_DUR_CAP1",
        "heals_once_per_activation",
        "multiimpact_watch",
    ],
    "viento": [
        "global_hit_clamp_preserved",
        "corriente_once_per_activation",
        "no_second_dodge_roll",
        "no_movement_speed_stat",
    ],
}

NICHE = {
    "fuego": "reserva finita / conversión a tempo ofensivo / eficiencia",
    "metal": "cargas secuenciales / resistencia / anti-Control / cantidad",
    "agua": "pool regenerativo / reconstrucción / economía",
    "tierra": "asentamiento reactivo / Tenacidad / curación limitada",
    "viento": "Evasión / respuesta ofensiva / continuidad",
}

WATCH = {
    "fuego": "cerrar semántica exacta de consumo de Calor en hit/miss y Qi II-IV",
    "metal": "Adaptación con enemigos reales de Control y multihit real",
    "agua": "stress de presión espaciada y Qi II-IV; burst múltiple es debilidad identitaria",
    "tierra": "multiimpacto y mezclas Fortificación+Aguante con enemigos II-IV",
    "viento": "Precisión enemiga II-IV y economía/duración con Qi futuro",
}


def rows() -> list[dict]:
    out = []
    for profile, by_root in RANGES.items():
        for root, (lo, hi) in by_root.items():
            out.append({
                "profile": profile,
                "root": root,
                "win_min_percent": lo,
                "win_max_percent": hi,
                "spread_pp": round(hi - lo, 2),
                "source": SOURCES[root],
                "niche": NICHE[root],
                "watch": WATCH[root],
            })
    return out


def export(path: str = "etapa15c_defensivas_completas_summary.csv") -> None:
    data = rows()
    fields = list(data[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)


if __name__ == "__main__":
    export()
    print("ETAPA 15C — agregado de benchmarks completos")
    for profile, by_root in RANGES.items():
        print(profile)
        for root, limits in by_root.items():
            print(" ", root, limits)
    print("No se promueve ni modifica ningún número desde este agregador.")
