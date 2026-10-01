"""Rata T4 Mordisco Frenético — Phase C cooldown calibration."""
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

CFG=json.loads((HERE/"RATA_T4_COOLDOWN_INPUT_V0_1.json").read_text(encoding="utf-8"))
POLICIES=("VETERAN","UNITARGET_FIRST","AOE_FIRST","DEFENSE_OPEN","ROTATION")

def build_candidate(spec):
    return {
        "label":spec["label"],
        "opening_instance_basic":True,
        "followup_hit_count":1,
        "followup_scalar_per_hit":0.5,
        "precision_rule":"INDEPENDENT_PER_HIT",
        "critical_rule":"INDEPENDENT_PER_HIT",
        "cooldown_rounds":int(spec["cooldown_rounds"]),
    }

def write_json(path,obj):
    Path(path).write_text(json.dumps(obj,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")

def write_gz(path,obj):
    with gzip.open(path,"wt",encoding="utf-8",compresslevel=9) as f:
        json.dump(obj,f,ensure_ascii=False,sort_keys=True,separators=(",",":"))

def zip_results(outdir):
    z=outdir/"RESULTADOS_RATA_T4_COOLDOWN_V01.zip"
    with zipfile.ZipFile(z,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as zz:
        for p in outdir.rglob("*"):
            if p.is_file() and p!=z:zz.write(p,p.relative_to(outdir))
    return z

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--natural-fights",type=int,default=200)
    ap.add_argument("--mutant-fights",type=int,default=50)
    ap.add_argument("--outdir",default="RATA_T4_COOLDOWN_V01")
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
        for spec in CFG["candidates"]:
            candidate=build_candidate(spec)
            print("POLICY",policy,candidate["label"],flush=True)
            result=evaluate(
                canonical,tier="T4",candidate=candidate,
                natural_n=args.natural_fights,mutant_n=args.mutant_fights,
                namespace=args.namespace,policy=policy,
            )
            rows.append({
                "policy":policy,
                "candidate":candidate,
                "frozen_t3":baseline,
                "result":result,
                "delta_vs_frozen_t3":{
                    "natural_normal":delta(result["natural_normal"],baseline["natural_normal"]),
                    "mutant_conditional":delta(result["mutant_conditional"],baseline["mutant_conditional"]),
                },
            })

    outdir=Path(args.outdir);outdir.mkdir(parents=True,exist_ok=True)
    write_gz(outdir/"cooldown_results.json.gz",rows)
    fights_per_arm=10*(args.natural_fights+args.mutant_fights)
    total_arms=len(POLICIES)*(1+len(CFG["candidates"]))
    write_json(outdir/"SUMMARY.json",{
        "experiment":"RATA_T4_COOLDOWN_V01",
        "status":"PHASE_C_RESULTS_AWAITING_REVIEW",
        "policies":list(POLICIES),
        "candidate_count":len(CFG["candidates"]),
        "contexts":10,
        "fights_per_arm":fights_per_arm,
        "total_arms":total_arms,
        "total_fights":fights_per_arm*total_arms,
        "frozen_mechanics":CFG["frozen_mechanics"],
        "t1_t3_frozen":True,
        "canonical_write":False,
        "tier_above_t4_executed":False,
    })
    write_json(outdir/"MANIFEST.json",{
        "phase":"C_COOLDOWN",
        "geometry_frozen":True,
        "precision_crit_frozen":True,
        "only_cooldown_varies":True,
        "canonical_write":False,
        "no_t5":True,
    })
    print("DONE",zip_results(outdir),flush=True)

if __name__=="__main__":main()
