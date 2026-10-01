"""Rata T3 trigger generalization across five player policies.

Frozen T1/T2. T3 uses canonical 2d4 reference and varies trigger semantics only.
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
from rata_t3_counter_lab import INPUT,RATA_ID,evaluate,delta

POLICIES=("VETERAN","UNITARGET_FIRST","AOE_FIRST","DEFENSE_OPEN","ROTATION")

def write_json(path,obj):
    Path(path).write_text(json.dumps(obj,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")

def write_gz(path,obj):
    with gzip.open(path,"wt",encoding="utf-8",compresslevel=9) as f:
        json.dump(obj,f,ensure_ascii=False,sort_keys=True,separators=(",",":"))

def zip_results(outdir):
    z=outdir/"RESULTADOS_RATA_T3_POLICY_GENERALIZATION_V01.zip"
    with zipfile.ZipFile(z,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as zz:
        for p in outdir.rglob("*"):
            if p.is_file() and p!=z:
                zz.write(p,p.relative_to(outdir))
    return z

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--natural-fights",type=int,default=200)
    ap.add_argument("--mutant-fights",type=int,default=50)
    ap.add_argument("--outdir",default="RATA_T3_POLICY_GENERALIZATION_V01")
    ap.add_argument("--namespace",default="RUN")
    args=ap.parse_args()
    if args.natural_fights<1 or args.mutant_fights<1:
        raise ValueError("fight counts must be >=1")

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
        for candidate in INPUT["candidate_triggers"]:
            print("POLICY",policy,candidate["label"],flush=True)
            t3=evaluate(
                canonical,tier="T3",candidate=candidate,
                natural_n=args.natural_fights,mutant_n=args.mutant_fights,
                namespace=args.namespace,policy=policy,
            )
            rows.append({
                "policy":policy,
                "candidate":candidate,
                "frozen_t2":t2,
                "t3":t3,
                "delta_vs_frozen_t2":{
                    "natural_normal":delta(t3["natural_normal"],t2["natural_normal"]),
                    "mutant_conditional":delta(t3["mutant_conditional"],t2["mutant_conditional"]),
                },
            })

    outdir=Path(args.outdir);outdir.mkdir(parents=True,exist_ok=True)
    write_gz(outdir/"policy_generalization_results.json.gz",rows)
    fights_per_arm=10*(args.natural_fights+args.mutant_fights)
    total_arms=len(POLICIES)*(1+len(INPUT["candidate_triggers"]))
    write_json(outdir/"SUMMARY.json",{
        "experiment":"RATA_T3_POLICY_GENERALIZATION_V01",
        "status":"LAB_RESULTS_AWAITING_HUMAN_REVIEW",
        "policies":list(POLICIES),
        "policy_count":len(POLICIES),
        "candidate_count":len(INPUT["candidate_triggers"]),
        "contexts":10,
        "natural_fights_per_context":args.natural_fights,
        "mutant_fights_per_context":args.mutant_fights,
        "fights_per_arm":fights_per_arm,
        "total_arms":total_arms,
        "total_fights":fights_per_arm*total_arms,
        "t1_frozen":True,
        "t2_frozen":True,
        "counter_damage_reference":"2d4",
        "canonical_write":False,
        "t4_executed":False,
    })
    write_json(outdir/"MANIFEST.json",{
        "purpose":"separate T3 trigger semantics under player pattern changes",
        "same_instance_seed_namespace_across_policies":True,
        "reflejo_causal_miss_detection":True,
        "t1_t2_frozen":True,
        "damage_scaling_tested":False,
        "canonical_write":False,
        "t4_forbidden":True,
    })
    print("DONE",zip_results(outdir),flush=True)

if __name__=="__main__":main()
