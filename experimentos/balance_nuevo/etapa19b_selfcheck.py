"""Self-check reproducible de ETAPA19B.

Valida el catálogo de 15 técnicas, compila todo el espacio legal de habilidades
y ejecuta un smoke 1v1 LianQi I sobre los cinco monstruos nativos en T0/T1.
No modifica datos ni runtime.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

from etapa19b_combat_engine import (
    ROOT_TECHNIQUES, LabSignalBridge, load_json, validate_catalog,
    compile_build, monte_carlo,
    TECHNIQUE_CATALOG_PATH, MONSTER_CATALOG_PATH, EQUIPMENT_CATALOG_PATH,
)
from etapa19_skill_buildspace import enumerate_skill_builds, skill_build_count

EXPECTED_SKILL_COUNTS={"LianQi_I":1,"LianQi_II":37,"LianQi_III":739,"LianQi_IV":11512}


def paths_of(build):
    return {p.technique_id:p.choices for p in build.paths}


def run(iterations: int=50, seed: int=20260930) -> dict:
    techniques=load_json(TECHNIQUE_CATALOG_PATH)
    monsters=load_json(MONSTER_CATALOG_PATH)
    equipment=load_json(EQUIPMENT_CATALOG_PATH)
    errors=validate_catalog(techniques)

    counts={}
    compiled=0
    for root in ROOT_TECHNIQUES:
        counts[root]={}
        for stage,expected in EXPECTED_SKILL_COUNTS.items():
            count=skill_build_count(root,stage)
            counts[root][stage]=count
            if count!=expected:errors.append(f"SKILL_COUNT:{root}:{stage}:{count}!={expected}")
        # Exhaustive compiler check at the largest stage. If every legal LIV
        # build compiles, all shorter-stage paths are a subset of the same grammar.
        for build in enumerate_skill_builds(root,"LianQi_IV"):
            compile_build(root,paths_of(build),techniques)
            compiled+=1

    profiles=monsters["profiles"]
    if len(profiles)!=18:errors.append(f"MONSTER_COUNT:{len(profiles)}!=18")
    native_li=[p for p in profiles.values() if p["native_stage"]=="LianQi_I"]
    if len(native_li)!=5:errors.append(f"LI_MONSTER_COUNT:{len(native_li)}!=5")

    mandatory=equipment["simulation_loadouts"]["MANDATORY_ENTRY"]["LianQi_I"]
    smoke=[]
    for root in ROOT_TECHNIQUES:
        li_build=next(enumerate_skill_builds(root,"LianQi_I"))
        paths=paths_of(li_build)
        for mon in native_li:
            for tier in ("T0","T1"):
                for policy in ("UNITARGET_FIRST","DEFENSE_OPEN","AOE_FIRST"):
                    row=monte_carlo(
                        iterations=iterations, seed=seed,
                        stage="LianQi_I",root=root,item_ids=mandatory,paths=paths,
                        monster_profile=mon,tier=tier,policy=policy,
                        signal_bridge=LabSignalBridge(),technique_catalog=techniques,
                        equipment_catalog=equipment,
                    )
                    smoke.append({k:row[k] for k in (
                        "root","monster_id","tier","policy","win_rate","mean_rounds",
                        "mean_hp_final_pct","mean_qi_final","hit_rate","control_success_rate"
                    )})
    # Determinism: identical seeded call must be byte-equivalent as a dict.
    root="fuego";build=next(enumerate_skill_builds(root,"LianQi_I"));mon=native_li[0]
    kwargs=dict(iterations=25,seed=seed,stage="LianQi_I",root=root,item_ids=mandatory,
                paths=paths_of(build),monster_profile=mon,tier="T1",policy="DEFENSE_OPEN",
                signal_bridge=LabSignalBridge(),technique_catalog=techniques,equipment_catalog=equipment)
    if monte_carlo(**kwargs)!=monte_carlo(**kwargs):errors.append("NON_DETERMINISTIC_SMOKE")

    return {
        "status":"PASS" if not errors else "FAIL",
        "validation_errors":errors,
        "techniques":len(techniques["techniques"]),
        "monsters":len(profiles),
        "compiled_liv_skill_builds_all_roots":compiled,
        "skill_counts_per_root":counts,
        "smoke_iterations_per_cell":iterations,
        "smoke_cells":len(smoke),
        "signal_bridge":LabSignalBridge().__dict__,
        "smoke":smoke,
    }


if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--iterations",type=int,default=50)
    ap.add_argument("--seed",type=int,default=20260930)
    ap.add_argument("--json",default="")
    args=ap.parse_args()
    out=run(args.iterations,args.seed)
    print(json.dumps({k:v for k,v in out.items() if k!="smoke"},ensure_ascii=False,indent=2))
    if args.json:Path(args.json).write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    if out["validation_errors"]:raise SystemExit(1)
