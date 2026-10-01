"""Mono T0 local refinement around causal QI_DRAIN anchor 1068.

Only HP/DEF/EVA vary. All identity-bearing offensive/resource parameters are
frozen to the ablation-validated anchor. Every config is tested paired:
A = QI_DRAIN 5, B = identical config with QI_DRAIN 0.

No raw fight persistence, no target win rate, no automatic promotion.
"""
from __future__ import annotations
import argparse,gzip,json,math,sys,zipfile
from pathlib import Path

HERE=Path(__file__).resolve().parent
BALANCE=HERE.parent
STAGE1=BALANCE/"stage1_integral_t0_optuna"
for p in (HERE,BALANCE,STAGE1):
    if str(p) not in sys.path:sys.path.insert(0,str(p))

from contexts import PRIMARY_CONTEXTS,ROOTS
from proposal import candidate_from_params
from runner import fight_candidate_once
from seeds import stable_seed
from streaming import StreamingAggregate
import etapa19b_combat_engine as engine

INPUT=json.loads((HERE/"mono_t0_local_refinement_input_v0.1.json").read_text(encoding="utf-8"))
PRESETS={
    "smoke":{"search_fights":2,"final_cap":3,"final_fights":5},
    "directed":{"search_fights":250,"final_cap":7,"final_fights":2000},
    "heavy":{"search_fights":500,"final_cap":7,"final_fights":5000},
}

def load_json(path):return json.loads(Path(path).read_text(encoding="utf-8"))
def paths_for(root):return {tid:() for tid in engine.ROOT_TECHNIQUES[root]}
def write_json(path,obj):Path(path).write_text(json.dumps(obj,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
def write_gz(path,obj):
    with gzip.open(path,"wt",encoding="utf-8",compresslevel=9) as f:
        json.dump(obj,f,ensure_ascii=False,sort_keys=True,separators=(",",":"))

def grid():
    fixed=INPUT["identity_anchor"]["fixed"]
    out=[]
    idx=0
    for hp in INPUT["survival_grid"]["hp"]:
        for defense in INPUT["survival_grid"]["defense"]:
            for evasion in INPUT["survival_grid"]["evasion"]:
                idx+=1
                out.append({
                    "grid_id":idx,
                    "params":{
                        "hp":hp,"defense":defense,"evasion":evasion,
                        "precision":fixed["precision"],"tenacity":fixed["tenacity"],
                        "basic_damage":fixed["basic_damage"],
                        "technique_direct_damage":fixed["technique_direct_damage"],
                        "qi_drain":fixed["qi_drain"],
                        "technique_cadence":fixed["technique_cadence"],
                    }
                })
    if len(out)!=INPUT["grid_size"]:raise RuntimeError("grid size drift")
    return out

def evaluate(params,registry,techniques,equipment,n,namespace):
    arms={}
    for label,drain in (("WITH_DRAIN",params["qi_drain"]),("NO_DRAIN",0)):
        p=dict(params);p["qi_drain"]=drain
        cand=candidate_from_params("mono_pildoras",p)
        canonical=registry["profiles"]["mono_pildoras"]
        agg=StreamingAggregate()
        for ctx in PRIMARY_CONTEXTS:
            items=equipment["simulation_loadouts"][ctx.loadout_profile]["LianQi_I"]
            for root in ROOTS:
                for i in range(n):
                    seed=stable_seed("MONO_QI_LOCAL_REFINEMENT_V01",namespace,ctx.context_id,root,i)
                    row=fight_candidate_once(
                        candidate=cand,canonical_profile=canonical,trial_number=0,
                        root=root,item_ids=items,paths=paths_for(root),seed=seed,policy="VETERAN",
                        technique_catalog=techniques,equipment_catalog=equipment,
                    )
                    row["loadout_profile"]=ctx.loadout_profile
                    agg.add(row)
        arms[label]=agg.finish()
    a=arms["WITH_DRAIN"];b=arms["NO_DRAIN"]
    causal={
        "forced_basic_delta":a["forced_basic_due_to_qi_mean"]-b["forced_basic_due_to_qi_mean"],
        "qi_drained_mean":a["qi_drained_mean"],
        "qi_final_delta":a["qi_final_mean"]-b["qi_final_mean"],
        "rounds_delta":a["rounds_mean"]-b["rounds_mean"],
        "hp_pressure_delta":(1-a["hp_final_pct_mean"])-(1-b["hp_final_pct_mean"]),
        "win_rate_delta":a["win_rate"]-b["win_rate"],
        "monster_damage_delta":a["monster_damage_total_mean"]-b["monster_damage_total_mean"],
        "no_drain_player_hp_pressure":1-b["hp_final_pct_mean"],
    }
    return {"with_drain":a,"no_drain":b,"causal":causal}

def dominates(a,b):
    # objective 0 max forced-basic causal delta; objective 1 min no-drain pressure
    ax=(a["causal"]["forced_basic_delta"],a["causal"]["no_drain_player_hp_pressure"])
    bx=(b["causal"]["forced_basic_delta"],b["causal"]["no_drain_player_hp_pressure"])
    return ax[0]>=bx[0] and ax[1]<=bx[1] and (ax[0]>bx[0] or ax[1]<bx[1])

def pareto(rows):
    return [r for i,r in enumerate(rows) if not any(dominates(o,r) for j,o in enumerate(rows) if i!=j)]

def coverage(rows,count):
    if len(rows)<=count:return list(rows)
    xs=[r["causal"]["forced_basic_delta"] for r in rows]
    ys=[r["causal"]["no_drain_player_hp_pressure"] for r in rows]
    xmin,xmax=min(xs),max(xs);ymin,ymax=min(ys),max(ys)
    pts=[]
    for r in rows:
        x=0 if xmax==xmin else (r["causal"]["forced_basic_delta"]-xmin)/(xmax-xmin)
        y=0 if ymax==ymin else (ymax-r["causal"]["no_drain_player_hp_pressure"])/(ymax-ymin)
        pts.append((x,y))
    chosen=[]
    for dim in (0,1):
        i=max(range(len(rows)),key=lambda k:pts[k][dim])
        if i not in chosen:chosen.append(i)
    while len(chosen)<count:
        rem=[i for i in range(len(rows)) if i not in chosen]
        i=max(rem,key=lambda k:min(math.dist(pts[k],pts[j]) for j in chosen))
        chosen.append(i)
    return [rows[i] for i in chosen[:count]]

def compact(row):
    return {
        "grid_id":row["grid_id"],"params":row["params"],"causal":row["causal"],
        "with_drain":row["with_drain"],"no_drain":row["no_drain"],
    }

def zip_results(outdir):
    z=outdir/"RESULTADOS_MONO_T0_LOCAL_REFINEMENT.zip"
    with zipfile.ZipFile(z,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as zz:
        for p in outdir.rglob("*"):
            if p.is_file() and p!=z:zz.write(p,p.relative_to(outdir))
    return z

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--preset",choices=PRESETS,default="heavy")
    ap.add_argument("--search-fights",type=int)
    ap.add_argument("--final-fights",type=int)
    ap.add_argument("--final-cap",type=int)
    ap.add_argument("--outdir",default="MONO_T0_LOCAL_REFINEMENT")
    args=ap.parse_args()
    cfg=dict(PRESETS[args.preset])
    for k in tuple(cfg):
        v=getattr(args,k)
        if v is not None:cfg[k]=v

    outdir=Path(args.outdir);outdir.mkdir(parents=True,exist_ok=True)
    registry=load_json(BALANCE/"monster_arc1_registry.json")
    techniques=load_json(BALANCE/"techniques_arc1_catalog.json")
    equipment=load_json(BALANCE/"equipment_arc1_catalog.json")

    rows=[]
    configs=grid()
    for i,g in enumerate(configs,1):
        print(f"SEARCH {i}/{len(configs)} grid {g['grid_id']} {g['params']}",flush=True)
        r=evaluate(g["params"],registry,techniques,equipment,cfg["search_fights"],"SEARCH")
        rows.append({"grid_id":g["grid_id"],"params":g["params"],**r})
    front=pareto(rows)
    selected=coverage(front,cfg["final_cap"])
    write_gz(outdir/"search_grid.json.gz",[compact(x) for x in rows])
    write_gz(outdir/"search_pareto.json.gz",[compact(x) for x in front])
    write_gz(outdir/"final_input.json.gz",[{"grid_id":x["grid_id"],"params":x["params"]} for x in selected])

    final=[]
    for i,x in enumerate(selected,1):
        print(f"FINAL {i}/{len(selected)} grid {x['grid_id']}",flush=True)
        r=evaluate(x["params"],registry,techniques,equipment,cfg["final_fights"],"FINAL")
        final.append({"grid_id":x["grid_id"],"params":x["params"],**r})
    final_front=pareto(final)
    write_gz(outdir/"final_all.json.gz",[compact(x) for x in final])
    write_gz(outdir/"final_pareto.json.gz",[compact(x) for x in final_front])
    write_json(outdir/"SUMMARY.json",{
        "experiment":"MONO_T0_LOCAL_REFINEMENT_V01",
        "status":"LAB_RESULTS_AWAITING_HUMAN_SELECTION",
        "identity_anchor_trial":1068,
        "fixed_identity":INPUT["identity_anchor"]["fixed"],
        "grid_size":len(configs),
        "search_fights_per_context_per_arm":cfg["search_fights"],
        "search_pareto":len(front),
        "final_candidates":len(final),
        "final_fights_per_context_per_arm":cfg["final_fights"],
        "final_pareto":len(final_front),
        "objectives":[
            "maximize causal forced_basic_delta from QI_DRAIN",
            "minimize NO_DRAIN player HP pressure",
        ],
        "automatic_selection":False,
        "canonical_write":False,
    })
    write_json(outdir/"MANIFEST.json",{
        "engine_contract":"NEW_COMBAT_STATS_V0_1",
        "species":"mono_pildoras",
        "paired_common_random_numbers":True,
        "only_survival_axes_varied":["hp","defense","evasion"],
        "fixed_qi_drain":5,
        "fixed_cadence":2,
        "fixed_basic_damage":"1d2+3",
        "fixed_technique_direct_damage":"1d2+3",
        "target_win_rate":False,
        "raw_fights_persisted":False,
        "canonical_write":False,
        "t1_t4_executed":False,
    })
    print("DONE",zip_results(outdir),flush=True)

if __name__=="__main__":main()
