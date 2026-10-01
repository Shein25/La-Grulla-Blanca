"""Final validation for the provisional complete Rata T3 candidate.

Candidate:
- trigger: CONFIRMED_PATTERN_REFLEJO_MISS
- damage: INSTANCE_BASIC
- direct-damage pipeline
- T1/T2 frozen
- T4 forbidden

Runs across five player policies and compares against frozen T2.
"""
from __future__ import annotations
import argparse,gzip,json,sys,zipfile
from pathlib import Path

HERE=Path(__file__).resolve().parent
BALANCE=HERE.parent
STAGE1=BALANCE/"stage1_integral_t0_optuna"
VARIANCE=BALANCE/"individual_variance_v0.1"
T1LAB=BALANCE/"rata_t1_variance_interaction_v0.1"
PARALLEL=BALANCE/"parallel_arc1_pipeline"
for p in (HERE,BALANCE,STAGE1,VARIANCE,T1LAB,PARALLEL):
    if str(p) not in sys.path:sys.path.insert(0,str(p))

from monster_new_engine_guard import load_registry,require_ready_profile
from rata_t3_counter_lab import RATA_ID,evaluate,delta

POLICIES=("VETERAN","UNITARGET_FIRST","AOE_FIRST","DEFENSE_OPEN","ROTATION")
CANDIDATE={
    "label":"CONFIRMED_PATTERN_REFLEJO_MISS_INSTANCE_BASIC",
    "requires_t2_recognition_active":True,
    "requires_prediction_confirmed":True,
    "requires_t1_reflejo_active":True,
    "requires_player_attack_miss":True,
    "counter_limit":"NO_EXTRA_LIMIT_BEYOND_T1_GATE",
    "counter_damage_mode":"INSTANCE_BASIC",
    "damage_label":"INSTANCE_BASIC",
}

def write_json(path,obj):
    Path(path).write_text(json.dumps(obj,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")

def write_gz(path,obj):
    with gzip.open(path,"wt",encoding="utf-8",compresslevel=9) as f:
        json.dump(obj,f,ensure_ascii=False,sort_keys=True,separators=(",",":"))

def zip_results(outdir):
    z=outdir/"RESULTADOS_RATA_T3_FINAL_VALIDATION_V01.zip"
    with zipfile.ZipFile(z,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as zz:
        for p in outdir.rglob("*"):
            if p.is_file() and p!=z:
                zz.write(p,p.relative_to(outdir))
    return z

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--natural-fights",type=int,default=1000)
    ap.add_argument("--mutant-fights",type=int,default=250)
    ap.add_argument("--outdir",default="RATA_T3_FINAL_VALIDATION_V01")
    ap.add_argument("--namespace",default="RUN")
    args=ap.parse_args()

    registry=load_registry()
    canonical=require_ready_profile(RATA_ID,registry)
    if canonical["adaptive"]["status"]!="T2_READY_FOR_T3_CALIBRATION":
        raise RuntimeError("T3 calibration gate is not open")

    rows=[]
    for policy in POLICIES:
        print("POLICY",policy,"T2 baseline",flush=True)
        t2=evaluate(
            canonical,tier="T2",candidate=None,
            natural_n=args.natural_fights,mutant_n=args.mutant_fights,
            namespace=args.namespace,policy=policy,
        )
        print("POLICY",policy,"T3 final candidate",flush=True)
        t3=evaluate(
            canonical,tier="T3",candidate=CANDIDATE,
            natural_n=args.natural_fights,mutant_n=args.mutant_fights,
            namespace=args.namespace,policy=policy,
        )
        rows.append({
            "policy":policy,
            "candidate":CANDIDATE,
            "frozen_t2":t2,
            "t3":t3,
            "delta_vs_frozen_t2":{
                "natural_normal":delta(t3["natural_normal"],t2["natural_normal"]),
                "mutant_conditional":delta(t3["mutant_conditional"],t2["mutant_conditional"]),
            },
        })

    outdir=Path(args.outdir);outdir.mkdir(parents=True,exist_ok=True)
    write_gz(outdir/"final_validation_results.json.gz",rows)
    fights_per_arm=10*(args.natural_fights+args.mutant_fights)
    write_json(outdir/"SUMMARY.json",{
        "experiment":"RATA_T3_FINAL_VALIDATION_V01",
        "status":"FINAL_T3_CANDIDATE_AWAITING_HUMAN_RATIFICATION",
        "candidate":CANDIDATE,
        "policies":list(POLICIES),
        "contexts":10,
        "natural_fights_per_context":args.natural_fights,
        "mutant_fights_per_context":args.mutant_fights,
        "fights_per_arm":fights_per_arm,
        "total_arms":10,
        "total_fights":fights_per_arm*10,
        "t1_frozen":True,
        "t2_frozen":True,
        "canonical_write":False,
        "t4_executed":False,
    })
    write_json(outdir/"MANIFEST.json",{
        "trigger":"CONFIRMED_PATTERN_REFLEJO_MISS",
        "damage":"INSTANCE_BASIC",
        "counter_damage_uses_individual_variance":True,
        "causal_reflejo_miss_detection":True,
        "normal_direct_damage_pipeline":True,
        "no_qi_drain":True,
        "no_dot":True,
        "no_control":True,
        "no_once_per_fight_artificial_limit":True,
        "canonical_write":False,
        "t4_forbidden":True,
    })
    print("DONE",zip_results(outdir),flush=True)

if __name__=="__main__":main()
