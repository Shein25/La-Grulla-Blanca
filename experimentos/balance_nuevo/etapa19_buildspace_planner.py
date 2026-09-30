"""ETAPA 19 — planificador exacto del espacio de builds.

Cuenta todas las combinaciones estructurales sin materializar billones de filas.
No ejecuta combate. Se usa para dimensionar el barrido de Colab y decidir
compresión/muestreo sin perder trazabilidad.
"""
from __future__ import annotations

from collections import Counter
from math import comb
import json
from pathlib import Path

from etapa19_skill_buildspace import TECHNIQUE_TREES, skill_build_count

ROOT = Path(__file__).resolve().parent
CATALOG = json.loads((ROOT / "equipment_arc1_catalog.json").read_text(encoding="utf-8"))

STAGE_ORDER = {"LianQi_I": 1, "LianQi_II": 2, "LianQi_III": 3, "LianQi_IV": 4}
NATIVE_MONSTERS = {"LianQi_I": 5, "LianQi_II": 5, "LianQi_III": 4, "LianQi_IV": 4}


def equipment_combination_count(stage: str) -> tuple[int, dict[str, int]]:
    rank=STAGE_ORDER[stage]
    available=[x for x in CATALOG["items"] if STAGE_ORDER[x["min_stage"]] <= rank]
    by_slot=Counter(x["slot"] for x in available)

    factors={}
    total=1
    for slot, capacity in CATALOG["slots"].items():
        n=by_slot[slot]
        # 0..capacity objetos distintos de ese slot.
        choices=sum(comb(n, k) for k in range(0, min(capacity, n) + 1))
        factors[slot]=choices
        total*=choices
    return total, factors


def stage_space(stage: str) -> dict:
    equipment, factors=equipment_combination_count(stage)
    per_root=skill_build_count(next(iter(TECHNIQUE_TREES)), stage)
    all_roots=per_root * len(TECHNIQUE_TREES)
    player_builds=equipment * all_roots
    native_t0_t1=player_builds * NATIVE_MONSTERS[stage] * 2
    return {
        "stage": stage,
        "equipment_combinations_raw": equipment,
        "equipment_slot_choice_factors": factors,
        "skill_builds_per_root": per_root,
        "skill_builds_all_roots": all_roots,
        "player_builds_raw": player_builds,
        "native_monsters": NATIVE_MONSTERS[stage],
        "native_T0_T1_scenarios_raw": native_t0_t1,
    }


def all_spaces() -> list[dict]:
    return [stage_space(stage) for stage in STAGE_ORDER]


if __name__ == "__main__":
    for row in all_spaces():
        print(row)
