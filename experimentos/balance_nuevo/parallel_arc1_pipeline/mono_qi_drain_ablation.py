"""Paired QI_DRAIN ablation for Mono Ladrón de Píldoras.

A = original candidate.
B = identical candidate with qi_drain=0.
Common random numbers isolate the causal resource-pressure contribution.
"""
from __future__ import annotations
import argparse,gzip,json,sys,zipfile
from pathlib import Path

HERE=Path(__file__).resolve().parent
BALANCE=HERE.parent
STAGE1=BALANCE/"stage1_integral_t0_optuna"
for p in (BALANCE,STAGE1,HERE):
    if str(p) not in sys.path:sys.path.insert(0,str(p))

from contexts import PRIMARY_CONTEXTS,ROOTS
from proposal import candidate_from_params
from runner import fight_candidate_once
from seeds import stable_seed
from streaming import StreamingAggregate
import etapa19b_combat_engine as engine

PRESETS={"smoke":5,"directed":2000,"heavy":10000}

def load_json(path):return json.loads(Path(path).read_text(encoding="utf-8"))
def write_json(path,obj):Path(path).write_text(json.dumps(obj,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
def write_gz(path,obj):
    with gzip.open(path,"wt",encoding="utf-8",compresslevel=9) as f:json.dump(obj,f,ensure_ascii=False,sort_keys=True,separators=(",",":"))
def base_paths(root):return {tid:() for tid in engine.ROOT_TECHNIQUES[root]}

def eval_arm(entry,params,label,registry,techniques,equipment,n):
    candidate=candidate_from_params("mono_pildoras",params)
    canonical=registry["profiles"]["mono_pildoras"]
    agg=StreamingAggregate()
    for ctx in PRIMARY_CONTEXTS:
        items=equipment["simulation_loadouts"][ctx.loadout_profile]["LianQi_I"]
        for root in ROOTS:
            for i in range(n):
                seed=stable_seed("MONO_QI_ABLATION_V01",entry["trial"],ctx.context_id,root,i)
                row=fight_candidate_once(
                    candidate=candidate,canonical_profile=canonical,trial_number=int(entry["trial"]),
                    root=root,item_ids=items,paths=base_paths(root),seed=seed,policy="VETERAN",
                    technique_catalog=techniques,equipment_catalog=equipment,
                )
                row["loadout_profile"]=ctx.loadout_profile
                agg.add(row)
    return agg.finish()

def deltas(a,b):
    return {
        "qi_final_delta_with_drain":a["qi_final_mean"]-b["qi_final_mean"],
        "qi_drained_delta":a["qi_drained_mean"]-b["qi_drained_mean"],
        "forced_basic_delta":a["forced_basic_due_to_qi_mean"]-b["forced_basic_due_to_qi_mean"],
        "rounds_delta":a["rounds_mean"]-b["rounds_mean"],
        "hp_pressure_delta":(1-a["hp_final_pct_mean"])-(1-b["hp_final_pct_mean"]),
        "win_rate_delta":a["win_rate"]-b["win_rate"],
        "monster_damage_delta":a["monster_damage_total_mean"]-b["monster_damage_total_mean"],
    }

def zip_results(outdir):
    zpath=outdir/"RESULTADOS_MONO_QI_DRAIN_ABLATION.zip"
    with zipfile.ZipFile(zpath,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in outdir.rglob("*"):
            if p.is_file() and p!=zpath:z.write(p,p.relative_to(outdir))
    return zpath

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--preset",choices=PRESETS,default="directed")
    ap.add_argument("--fights-per-context",type=int)
    ap.add_argument("--outdir",default="MONO_QI_DRAIN_ABLATION")
    args=ap.parse_args()
    n=args.fights_per_context or PRESETS[args.preset]
    outdir=Path(args.outdir);outdir.mkdir(parents=True,exist_ok=True)

    sets=load_json(HERE/"candidate_sets.json")["species"]["mono_pildoras"]
    registry=load_json(BALANCE/"monster_arc1_registry.json")
    techniques=load_json(BALANCE/"techniques_arc1_catalog.json")
    equipment=load_json(BALANCE/"equipment_arc1_catalog.json")
    rows=[]
    for idx,entry in enumerate(sets,1):
        print(f"Mono {idx}/5 trial {entry['trial']}",flush=True)
        a_params=dict(entry["params"])
        b_params=dict(entry["params"]);b_params["qi_drain"]=0
        a=eval_arm(entry,a_params,"WITH_DRAIN",registry,techniques,equipment,n)
        b=eval_arm(entry,b_params,"NO_DRAIN",registry,techniques,equipment,n)
        rows.append({
            "trial":entry["trial"],"params_with_drain":a_params,"params_no_drain":b_params,
            "with_drain":a,"no_drain":b,"causal_delta":deltas(a,b),
        })
    write_gz(outdir/"mono_qi_drain_ablation.json.gz",rows)
    write_json(outdir/"SUMMARY.json",{
        "experiment":"MONO_QI_DRAIN_ABLATION_V01",
        "fights_per_context_per_arm":n,"contexts":10,"arms":2,
        "candidates":[x["trial"] for x in rows],
        "fights_total":len(rows)*2*10*n,
        "selection_performed":False,
    })
    write_json(outdir/"MANIFEST.json",{
        "paired_common_random_numbers":True,
        "only_changed_parameter":"qi_drain -> 0",
        "raw_fights_persisted":False,
        "canonical_write":False,
        "automatic_selection":False,
        "t1_t4_executed":False,
    })
    print("DONE",zip_results(outdir),flush=True)

if __name__=="__main__":main()
