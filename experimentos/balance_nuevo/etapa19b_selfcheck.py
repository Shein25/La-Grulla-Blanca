"""Self-check reproducible de ETAPA19B bajo el motor nuevo.

Valida técnicas, buildspace y el esquema único de los 18 monstruos.
Los perfiles T0 pendientes deben quedar bloqueados; no se ejecuta combate con
estadísticas incompletas.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

from etapa19b_combat_engine import (
    ROOT_TECHNIQUES, load_json, validate_catalog, compile_build, build_monster,
    TECHNIQUE_CATALOG_PATH, MONSTER_CATALOG_PATH,
)
from etapa19_skill_buildspace import enumerate_skill_builds, skill_build_count

EXPECTED_SKILL_COUNTS={"LianQi_I":1,"LianQi_II":37,"LianQi_III":739,"LianQi_IV":11512}


def paths_of(build):
    return {p.technique_id:p.choices for p in build.paths}


def run(iterations: int=0, seed: int=20260930) -> dict:
    techniques=load_json(TECHNIQUE_CATALOG_PATH)
    monsters=load_json(MONSTER_CATALOG_PATH)
    errors=validate_catalog(techniques)

    counts={}
    compiled=0
    for root in ROOT_TECHNIQUES:
        counts[root]={}
        for stage,expected in EXPECTED_SKILL_COUNTS.items():
            count=skill_build_count(root,stage)
            counts[root][stage]=count
            if count!=expected:
                errors.append(f"SKILL_COUNT:{root}:{stage}:{count}!={expected}")
        for build in enumerate_skill_builds(root,"LianQi_IV"):
            compile_build(root,paths_of(build),techniques)
            compiled+=1

    if monsters.get("schema_version")!="arc1-monsters-v1":
        errors.append("MONSTER_SCHEMA")
    if monsters.get("status")!="NEW_ENGINE_ONLY":
        errors.append("MONSTER_STATUS")
    if monsters.get("engine_contract")!="NEW_COMBAT_STATS_V0_1":
        errors.append("MONSTER_ENGINE_CONTRACT")

    profiles=monsters.get("profiles",{})
    if len(profiles)!=18:
        errors.append(f"MONSTER_COUNT:{len(profiles)}!=18")
    native_li=[p for p in profiles.values() if p.get("native_stage")=="LianQi_I"]
    if len(native_li)!=5:
        errors.append(f"LI_MONSTER_COUNT:{len(native_li)}!=5")

    blocked=0
    for monster_id,profile in profiles.items():
        if profile.get("id")!=monster_id:
            errors.append(f"MONSTER_ID_MISMATCH:{monster_id}")
        if profile.get("engine_contract")!="NEW_COMBAT_STATS_V0_1":
            errors.append(f"MONSTER_CONTRACT:{monster_id}")
        try:
            build_monster(profile,"T0")
        except ValueError as exc:
            if "not READY" in str(exc):
                blocked+=1
            else:
                errors.append(f"MONSTER_GUARD:{monster_id}:{exc}")

    if blocked!=18:
        errors.append(f"PENDING_BLOCKED:{blocked}!=18")

    return {
        "status":"PASS" if not errors else "FAIL",
        "validation_errors":errors,
        "techniques":len(techniques["techniques"]),
        "monsters":len(profiles),
        "pending_monsters_blocked":blocked,
        "compiled_liv_skill_builds_all_roots":compiled,
        "skill_counts_per_root":counts,
        "monster_combat_status":"BLOCKED_PENDING_T0",
        "smoke_cells":0,
        "seed":seed,
    }


if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--iterations",type=int,default=0)
    ap.add_argument("--seed",type=int,default=20260930)
    ap.add_argument("--json",default="")
    args=ap.parse_args()
    out=run(args.iterations,args.seed)
    print(json.dumps(out,ensure_ascii=False,indent=2))
    if args.json:
        Path(args.json).write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    if out["validation_errors"]:
        raise SystemExit(1)
