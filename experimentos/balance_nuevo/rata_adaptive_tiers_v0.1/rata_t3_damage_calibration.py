"""Rata T3 counter damage calibration across five player policies.

Trigger is provisionally frozen to CONFIRMED_PATTERN_REFLEJO_MISS.
Only the damage source changes. No T1/T2 numeric changes. T4 forbidden.
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

CFG=json.loads((HERE/"RATA_T3_DAMAGE_INPUT_V0_1.json").read_text(encoding="utf-8"))
POLICIES=("VETERAN","UNITARGET_FIRST","AOE_FIRST","DEFENSE_OPEN","ROTATION")

def candidate_with_damage(damage):
    out=dict(CFG["frozen_t3_trigger"])
    out.update({
        "counter_damage_mode":damage["counter_damage_mode"],
        "counter_damage_expression":damage.get("counter_damage_expression"),
        "damage_label":damage["label"],
    })
    return out

def write_json(path,obj):
    Path(path).write_text(json.dumps(obj,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")

def write_gz(path,obj):
    with gzip.open(path,"wt",encoding="utf-8",compresslevel=9) as f:
        json.dump(obj,f,ensure_ascii=False,sort_keys=True,separators=(",",":"))

def zip_results(outdir):
    z=outdir/"RESULTADOS_RATA_T3_DAMAGE_CALIBRATION_V01.zip"
    with zipfile.ZipFile(z,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as zz:
        for p in outdir.rglob("*"):
            if p.is_file() and p!=z:
                zz.write(p,p.relative_to(outdir))
    return z

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--natural-fights",type=int,default=200)
    ap.add_argument("--mutant-fights",type=int,default=50)
    ap.add_argument("--outdir",default="RATA_T3_DAMAGE_CALIBRATION_V01")
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
        for damage in CFG["damage_candidates"]:
            candidate=candidate_with_damage(damage)
            print("POLICY",policy,damage["label"],flush=True)
            t3=evaluate(
                canonical,tier="T3",candidate=candidate,
                natural_n=args.natural_fights,mutant_n=args.mutant_fights,
                namespace=args.namespace,policy=policy,
            )
            rows.append({
                "policy":policy,
                "damage_candidate":damage,
                "trigger":CFG["frozen_t3_trigger"],
                "frozen_t2":t2,
                "t3":t3,
                "delta_vs_frozen_t2":{
                    "natural_normal":delta(t3["natural_normal"],t2["natural_normal"]),
                    "mutant_conditional":delta(t3["mutant_conditional"],t2["mutant_conditional"]),
                }
            })

    outdir=Path(args.outdir);outdir.mkdir(parents=True,exist_ok=True)
    write_gz(outdir/"damage_calibration_results.json.gz",rows)
    fights_per_arm=10*(args.natural_fights+args.mutant_fights)
    total_arms=len(POLICIES)*(1+len(CFG["damage_candidates"]))
    write_json(outdir/"SUMMARY.json",{
        "experiment":"RATA_T3_DAMAGE_CALIBRATION_V01",
        "status":"LAB_RESULTS_AWAITING_HUMAN_REVIEW",
        "policies":list(POLICIES),
        "damage_candidates":CFG["damage_candidates"],
        "trigger":CFG["frozen_t3_trigger"],
        "contexts":10,
        "fights_per_arm":fights_per_arm,
        "total_arms":total_arms,
        "total_fights":fights_per_arm*total_arms,
        "t1_frozen":True,
        "t2_frozen":True,
        "trigger_frozen_for_damage_phase":True,
        "canonical_write":False,
        "t4_executed":False,
    })
    write_json(outdir/"MANIFEST.json",{
        "measured_damage_sources_only":True,
        "instance_basic_uses_individual_variance":True,
        "normal_direct_damage_pipeline":True,
        "no_qi_drain":True,
        "no_dot":True,
        "no_control":True,
        "canonical_write":False,
        "t4_forbidden":True,
    })
    print("DONE",zip_results(outdir),flush=True)

if __name__=="__main__":main()
