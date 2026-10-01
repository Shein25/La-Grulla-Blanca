"""Rata T2 recognition — player-policy generalization LAB.

Runs frozen T1 and all T2 recognition candidates across five player policies.
This is a recognition-generalization test, not a player-balance target.

No canonical write. T1 numerics frozen. T3-T4 forbidden.
"""
from __future__ import annotations
import argparse,gzip,json,zipfile
from pathlib import Path

from monster_new_engine_guard import load_registry,require_ready_profile
from rata_t2_recognition_lab import INPUT,RATA_ID,eval_tier,delta

POLICIES=("VETERAN","UNITARGET_FIRST","AOE_FIRST","DEFENSE_OPEN","ROTATION")
PRESETS={
    "smoke":{"natural_fights":2,"mutant_fights":1},
    "directed":{"natural_fights":500,"mutant_fights":100},
    "heavy":{"natural_fights":1000,"mutant_fights":250},
}

def write_json(path,obj):
    Path(path).write_text(json.dumps(obj,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")

def write_gz(path,obj):
    with gzip.open(path,"wt",encoding="utf-8",compresslevel=9) as f:
        json.dump(obj,f,ensure_ascii=False,sort_keys=True,separators=(",",":"))

def zip_results(outdir):
    z=outdir/"RESULTADOS_RATA_T2_POLICY_GENERALIZATION_V01.zip"
    with zipfile.ZipFile(z,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as zz:
        for p in outdir.rglob("*"):
            if p.is_file() and p!=z:zz.write(p,p.relative_to(outdir))
    return z

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--preset",choices=PRESETS,default="directed")
    ap.add_argument("--natural-fights",type=int)
    ap.add_argument("--mutant-fights",type=int)
    ap.add_argument("--outdir",default="RATA_T2_POLICY_GENERALIZATION_V01")
    ap.add_argument("--namespace",default="RUN")
    args=ap.parse_args()

    cfg=dict(PRESETS[args.preset])
    if args.natural_fights is not None:cfg["natural_fights"]=args.natural_fights
    if args.mutant_fights is not None:cfg["mutant_fights"]=args.mutant_fights

    registry=load_registry()
    canonical=require_ready_profile(RATA_ID,registry)
    if canonical["adaptive"]["status"]!="T1_READY_FOR_T2_CALIBRATION":
        raise RuntimeError("T2 calibration gate is not open")

    neutral={
        "memory_window":2,
        "repeated_same_category_required":2,
        "preemptive_survival_bonus":0,
        "count_results":["EFECTIVA"],
    }

    rows=[]
    for policy in POLICIES:
        print("POLICY",policy,"T1",flush=True)
        t1=eval_tier(
            canonical,tier="T1",candidate=neutral,
            natural_n=cfg["natural_fights"],mutant_n=cfg["mutant_fights"],
            namespace=args.namespace,policy=policy,
        )
        for raw in INPUT["candidates"]:
            cand=dict(raw);cand.setdefault("count_results",["EFECTIVA"])
            print("POLICY",policy,cand["label"],flush=True)
            t2=eval_tier(
                canonical,tier="T2",candidate=cand,
                natural_n=cfg["natural_fights"],mutant_n=cfg["mutant_fights"],
                namespace=args.namespace,policy=policy,
            )
            rows.append({
                "policy":policy,
                "candidate":cand,
                "frozen_t1":t1,
                "t2":t2,
                "delta_vs_frozen_t1":{
                    "natural_normal":delta(t2["natural_normal"],t1["natural_normal"]),
                    "mutant_conditional":delta(t2["mutant_conditional"],t1["mutant_conditional"]),
                },
            })

    outdir=Path(args.outdir);outdir.mkdir(parents=True,exist_ok=True)
    write_gz(outdir/"policy_generalization_results.json.gz",rows)

    fights_per_arm=10*(cfg["natural_fights"]+cfg["mutant_fights"])
    total_arms=len(POLICIES)*(1+len(INPUT["candidates"]))
    write_json(outdir/"SUMMARY.json",{
        "experiment":"RATA_T2_POLICY_GENERALIZATION_V01",
        "status":"LAB_RESULTS_AWAITING_HUMAN_REVIEW",
        "policies":list(POLICIES),
        "policy_count":len(POLICIES),
        "candidates":INPUT["candidates"],
        "natural_fights_per_context":cfg["natural_fights"],
        "mutant_fights_per_context":cfg["mutant_fights"],
        "contexts":10,
        "fights_per_arm":fights_per_arm,
        "total_arms":total_arms,
        "total_fights":fights_per_arm*total_arms,
        "same_instance_seed_namespace_across_policies":True,
        "t1_frozen":True,
        "canonical_write":False,
        "t3_t4_executed":False,
    })
    write_json(outdir/"MANIFEST.json",{
        "purpose":"recognition generalization across player action policies",
        "not_a_win_rate_target":True,
        "observable_action_categories_only":True,
        "fallback_basic_logged_as_actual_action":True,
        "hidden_root_build_forbidden":True,
        "t1_evasion_bonus":40,
        "t1_cooldown_rounds":5,
        "canonical_write":False,
        "t3_t4_forbidden":True,
    })
    print("DONE",zip_results(outdir),flush=True)

if __name__=="__main__":main()
