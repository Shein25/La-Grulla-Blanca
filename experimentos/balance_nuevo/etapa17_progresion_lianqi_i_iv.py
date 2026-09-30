"""ETAPA 17 — Progresión estructural LianQi I–IV.

No simula enemigos futuros porque todavía no existen perfiles numéricos
autoritativos LianQi II–IV.

Valida:
- baseline fijo;
- curva HP/Qi;
- presupuesto discreto de acciones;
- puntos de técnica;
- escalado natural de efectos %HP;
- ausencia de multiplicador global oculto por etapa.
"""
from __future__ import annotations

import csv

STAGES = [
    {"stage":"LianQi_I","name":"Percepcion","hp":30,"qi":31,"tech_points_gained":0,"tech_points_total":0,"tramo_cap":"BASE"},
    {"stage":"LianQi_II","name":"Circulacion","hp":36,"qi":37,"tech_points_gained":2,"tech_points_total":2,"tramo_cap":"TRAMO_I"},
    {"stage":"LianQi_III","name":"Consolidacion","hp":42,"qi":43,"tech_points_gained":2,"tech_points_total":4,"tramo_cap":"TRAMO_II"},
    {"stage":"LianQi_IV","name":"Refinamiento","hp":48,"qi":49,"tech_points_gained":2,"tech_points_total":6,"tramo_cap":"TRAMO_III"},
]

def budget(qi: int) -> dict:
    return {
        "pure_offense_cost6": qi // 6,
        "def7_plus_offense6_total": 1 + (qi - 7) // 6,
        "def6_plus_offense6_total": 1 + (qi - 6) // 6,
        "pure_aoe_cost9": qi // 9,
        "one_aoe9_plus_offense6_total": 1 + (qi - 9) // 6,
        "def7_plus_aoe9_plus_offense6_total": 2 + (qi - 16) // 6,
    }

def skill_scaling(hp: int) -> dict:
    return {
        "horno_base_25pct": hp * 0.25,
        "horno_barrera_45pct": hp * 0.45,
        "espejo_base_24pct": hp * 0.24,
        "espejo_reserva_42pct": hp * 0.42,
        "piel_heal_5pct": hp * 0.05,
        "piel_large_hit_threshold_10pct": hp * 0.10,
        "piel_low_hp_threshold_30pct": hp * 0.30,
    }

def rows() -> list[dict]:
    return [{**stage, **budget(stage["qi"]), **skill_scaling(stage["hp"])} for stage in STAGES]

def export(path: str = "etapa17_progresion_lianqi_i_iv.csv") -> None:
    data = rows()
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(data[0].keys()))
        writer.writeheader()
        writer.writerows(data)

if __name__ == "__main__":
    export()
    for row in rows():
        print(row)
