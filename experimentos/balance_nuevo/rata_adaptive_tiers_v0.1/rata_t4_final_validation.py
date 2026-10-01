"""Final validation of the complete provisional Rata T4 candidate.

125k default fights:
5 policies × (frozen T3 baseline + T4 candidate)
× 10 contexts × (1000 natural + 250 conditional Mutant).
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
from rata_t4_mordisco_geometry_lab import RATA_ID,evaluate,delta

CFG=json.loads((HERE/"RATA_T4_FINAL_CANDIDATE_V0_1.json").read_text(encoding="utf-8"))
POLICIES=("VETERAN","UNITARGET_FIRST","AOE_FIRST","DEFENSE_OPEN","ROTATION")

CANDIDATE={
    "label":"MORDISCO_FRENETICO_FINAL",
    "opening_instance_basic":True,
    "followup_hit_count":1,
    "followup_scalar_per_hit":0.5,
    "precision_rule":"INDEPENDENT_PER_HIT",
    "critical_rule":"INDEPENDENT_PER_HIT",
    "cooldown_rounds":5,
}

def write_json(path,obj):
    Path(path).write_text(json.dumps(obj,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")

def write_gz(path,obj):
    with gzip.open(path,"wt",encoding="utf-8",compresslevel=9) as f:
        json.dump(obj,f,ensure_ascii=False,sort_keys=True,separators=(",",":"))

def zip_results(outdir):
    z=outdir/"RESULTADOS_RATA_T4_FINAL_VALIDATION_V01.zip"
    with zipfile.ZipFile(z,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as zz:
        for p in outdir.rglob("*"):
            if p.is_file() and p!=z:zz.write(p,p.relative_to(outdir))
    return z

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--natural-fights",type=int,default=1000)
    ap.add_argument("--mutant-fights",type=int,default=250)
    ap.add_argument("--outdir",default="RATA_T4_FINAL_VALIDATION_V01")
    ap.add_argument("--namespace",default="RUN")
    args=ap.parse_args()

    registry=load_registry()
    canonical=require_ready_profile(RATA_ID,registry)
    if canonical["adaptive"]["status"]!="T3_READY_FOR_T4_CALIBRATION":
        raise RuntimeError("T4 calibration gate is not open")

    rows=[]
    for policy in POLICIES:
        print("POLICY",policy,"T3 baseline",flush=True)
        baseline=evaluate(
            canonical,tier="T3",candidate=None,
            natural_n=args.natural_fights,mutant_n=args.mutant_fights,
            namespace=args.namespace,policy=policy,
        )
        print("POLICY",policy,"T4 final",flush=True)
        result=evaluate(
            canonical,tier="T4",candidate=CANDIDATE,
            natural_n=args.natural_fights,mutant_n=args.mutant_fights,
            namespace=args.namespace,policy=policy,
        )
        rows.append({
            "policy":policy,
            "candidate":CANDIDATE,
            "frozen_t3":baseline,
            "t4":result,
            "delta_vs_frozen_t3":{
                "natural_normal":delta(result["natural_normal"],baseline["natural_normal"]),
                "mutant_conditional":delta(result["mutant_conditional"],baseline["mutant_conditional"]),
            },
        })

    outdir=Path(args.outdir);outdir.mkdir(parents=True,exist_ok=True)
    write_gz(outdir/"final_validation_results.json.gz",rows)
    fights_per_arm=10*(args.natural_fights+args.mutant_fights)
    write_json(outdir/"SUMMARY.json",{
        "experiment":"RATA_T4_FINAL_VALIDATION_V01",
        "status":"T4_FULL_CANDIDATE_AWAITING_HUMAN_RATIFICATION",
        "candidate":CANDIDATE,
        "policies":list(POLICIES),
        "contexts":10,
        "natural_fights_per_context":args.natural_fights,
        "mutant_fights_per_context":args.mutant_fights,
        "fights_per_arm":fights_per_arm,
        "total_arms":10,
        "total_fights":fights_per_arm*10,
        "effective_tier_required":"T4",
        "decay_below_t4_disables":True,
        "t1_t3_frozen":True,
        "canonical_write":False,
        "tier_above_t4_executed":False,
    })
    write_json(outdir/"MANIFEST.json",{
        "name":"Mordisco Frenético",
        "opening":"INSTANCE_BASIC x1.0",
        "followup":"1 x canonical 2d4 x0.50",
        "precision":"independent per hit",
        "critical":"normal independent per hit",
        "cooldown_rounds":5,
        "activation":"replace BASIC when ready",
        "skip_next_action_respected":True,
        "normal_direct_pipeline_per_packet":True,
        "effective_tier_required":"T4",
        "decay_below_t4_disables":True,
        "no_qi_drain":True,
        "no_dot":True,
        "no_control":True,
        "canonical_write":False,
        "no_t5":True,
    })
    print("DONE",zip_results(outdir),flush=True)

if __name__=="__main__":main()
