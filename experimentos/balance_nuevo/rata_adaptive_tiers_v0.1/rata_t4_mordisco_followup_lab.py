"""Rata T4 Mordisco Frenético — Phase A2 followup geometry.

Uses frozen T3 baseline and tests:
individual BASIC opening + canonical 2d4 followup packets.
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

CFG=json.loads((HERE/"RATA_T4_MORDISCO_FOLLOWUP_INPUT_V0_1.json").read_text(encoding="utf-8"))
PRESETS={
    "smoke":{"natural_fights":2,"mutant_fights":1},
    "directed":{"natural_fights":500,"mutant_fights":100},
    "heavy":{"natural_fights":2000,"mutant_fights":500},
}

def write_json(path,obj):
    Path(path).write_text(json.dumps(obj,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")

def write_gz(path,obj):
    with gzip.open(path,"wt",encoding="utf-8",compresslevel=9) as f:
        json.dump(obj,f,ensure_ascii=False,sort_keys=True,separators=(",",":"))

def zip_results(outdir):
    z=outdir/"RESULTADOS_RATA_T4_MORDISCO_FOLLOWUP_V01.zip"
    with zipfile.ZipFile(z,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as zz:
        for p in outdir.rglob("*"):
            if p.is_file() and p!=z:zz.write(p,p.relative_to(outdir))
    return z

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--preset",choices=PRESETS,default="directed")
    ap.add_argument("--natural-fights",type=int)
    ap.add_argument("--mutant-fights",type=int)
    ap.add_argument("--outdir",default="RATA_T4_MORDISCO_FOLLOWUP_V01")
    ap.add_argument("--namespace",default="RUN")
    ap.add_argument("--policy",choices=["VETERAN","UNITARGET_FIRST","AOE_FIRST","DEFENSE_OPEN","ROTATION"],default="VETERAN")
    args=ap.parse_args()
    cfg=dict(PRESETS[args.preset])
    if args.natural_fights is not None:cfg["natural_fights"]=args.natural_fights
    if args.mutant_fights is not None:cfg["mutant_fights"]=args.mutant_fights

    registry=load_registry()
    canonical=require_ready_profile(RATA_ID,registry)
    if canonical["adaptive"]["status"]!="T3_READY_FOR_T4_CALIBRATION":
        raise RuntimeError("T4 calibration gate is not open")

    baseline=evaluate(
        canonical,tier="T3",candidate=None,
        natural_n=cfg["natural_fights"],mutant_n=cfg["mutant_fights"],
        namespace=args.namespace,policy=args.policy,
    )
    rows=[]
    for candidate in CFG["candidates"]:
        print(candidate["label"],flush=True)
        result=evaluate(
            canonical,tier="T4",candidate=candidate,
            natural_n=cfg["natural_fights"],mutant_n=cfg["mutant_fights"],
            namespace=args.namespace,policy=args.policy,
        )
        rows.append({
            "candidate":candidate,
            "result":result,
            "delta_vs_frozen_t3":{
                "natural_normal":delta(result["natural_normal"],baseline["natural_normal"]),
                "mutant_conditional":delta(result["mutant_conditional"],baseline["mutant_conditional"]),
            },
        })

    outdir=Path(args.outdir);outdir.mkdir(parents=True,exist_ok=True)
    write_gz(outdir/"frozen_t3_baseline.json.gz",baseline)
    write_gz(outdir/"followup_results.json.gz",rows)
    write_json(outdir/"SUMMARY.json",{
        "experiment":"RATA_T4_MORDISCO_FOLLOWUP_V01",
        "status":"PHASE_A2_FOLLOWUP_RESULTS_AWAITING_REVIEW",
        "player_policy":args.policy,
        "contexts":10,
        "natural_fights_per_context":cfg["natural_fights"],
        "mutant_fights_per_context":cfg["mutant_fights"],
        "model":CFG["model"],
        "candidate_count":len(rows),
        "t1_t3_frozen":True,
        "canonical_write":False,
        "tier_above_t4_executed":False,
    })
    write_json(outdir/"MANIFEST.json",{
        "individual_basic_opening":True,
        "canonical_2d4_followups":True,
        "independent_precision_per_hit":True,
        "independent_crit_per_hit":True,
        "cooldown_rounds":5,
        "direct_pipeline_per_hit":True,
        "no_qi_drain":True,
        "no_dot":True,
        "no_control":True,
        "canonical_write":False,
        "no_t5":True,
    })
    print("DONE",zip_results(outdir),flush=True)

if __name__=="__main__":main()
