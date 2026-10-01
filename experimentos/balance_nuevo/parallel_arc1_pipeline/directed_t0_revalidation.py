"""Directed high-fidelity revalidation for Avispa, Serpiente and Lobo.

Uses only the five already-surviving overnight candidates per species.
No new broad search and no automatic selection.
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

SPECIES=("avispa_jade","serpiente_qi","lobo_espiritual")
PRESETS={
    "smoke":{"fights_per_context":5},
    "directed":{"fights_per_context":2000},
    "heavy":{"fights_per_context":10000},
}

def load_json(path):return json.loads(Path(path).read_text(encoding="utf-8"))
def write_json(path,obj):Path(path).write_text(json.dumps(obj,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
def write_gz(path,obj):
    with gzip.open(path,"wt",encoding="utf-8",compresslevel=9) as f:json.dump(obj,f,ensure_ascii=False,sort_keys=True,separators=(",",":"))

def base_paths(root):return {tid:() for tid in engine.ROOT_TECHNIQUES[root]}

def evaluate(species,entry,registry,techniques,equipment,n):
    candidate=candidate_from_params(species,entry["params"])
    canonical=registry["profiles"][species]
    agg=StreamingAggregate()
    for ctx in PRIMARY_CONTEXTS:
        items=equipment["simulation_loadouts"][ctx.loadout_profile]["LianQi_I"]
        for root in ROOTS:
            for i in range(n):
                seed=stable_seed("DIRECTED_T0_V01",species,ctx.context_id,root,i)
                row=fight_candidate_once(
                    candidate=candidate,canonical_profile=canonical,trial_number=int(entry["trial"]),
                    root=root,item_ids=items,paths=base_paths(root),seed=seed,policy="VETERAN",
                    technique_catalog=techniques,equipment_catalog=equipment,
                )
                row["loadout_profile"]=ctx.loadout_profile
                agg.add(row)
    a=agg.finish()
    roots=[x["hp_final_pct_mean"] for x in a["root_breakdown"].values()]
    loads=[x["hp_final_pct_mean"] for x in a["loadout_breakdown"].values()]
    return {
        "trial":entry["trial"],"params":entry["params"],"aggregate":a,
        "derived":{
            "player_hp_pressure":1.0-a["hp_final_pct_mean"],
            "root_hp_spread":max(roots)-min(roots),
            "loadout_hp_spread":max(loads)-min(loads),
        }
    }

def zip_results(outdir):
    zpath=outdir/"RESULTADOS_T0_DIRIGIDOS_AVISPA_SERPIENTE_LOBO.zip"
    with zipfile.ZipFile(zpath,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in outdir.rglob("*"):
            if p.is_file() and p!=zpath:z.write(p,p.relative_to(outdir))
    return zpath

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--preset",choices=PRESETS,default="directed")
    ap.add_argument("--fights-per-context",type=int)
    ap.add_argument("--outdir",default="T0_DIRIGIDOS_AVISPA_SERPIENTE_LOBO")
    args=ap.parse_args()
    n=args.fights_per_context or PRESETS[args.preset]["fights_per_context"]
    outdir=Path(args.outdir);outdir.mkdir(parents=True,exist_ok=True)

    sets=load_json(HERE/"candidate_sets.json")
    registry=load_json(BALANCE/"monster_arc1_registry.json")
    techniques=load_json(BALANCE/"techniques_arc1_catalog.json")
    equipment=load_json(BALANCE/"equipment_arc1_catalog.json")

    summary={"experiment":"T0_DIRECTED_REVALIDATION_V01","fights_per_context":n,"contexts":10,"species":{},"selection_performed":False}
    for species in SPECIES:
        rows=[]
        for idx,entry in enumerate(sets["species"][species],1):
            print(f"{species}: {idx}/5 trial {entry['trial']}",flush=True)
            rows.append(evaluate(species,entry,registry,techniques,equipment,n))
        write_gz(outdir/f"{species}_directed.json.gz",rows)
        summary["species"][species]={
            "candidates":[x["trial"] for x in rows],
            "fights_per_candidate":n*10,
            "timeouts":[x["aggregate"]["timeout_rate"] for x in rows],
        }
    write_json(outdir/"SUMMARY.json",summary)
    write_json(outdir/"MANIFEST.json",{
        "source":"5_MONSTRUOS_OVERNIGHT",
        "common_random_numbers":True,
        "raw_fights_persisted":False,
        "canonical_write":False,
        "automatic_selection":False,
        "t1_t4_executed":False,
        "definitives_executed":False,
    })
    print("DONE",zip_results(outdir),flush=True)

if __name__=="__main__":main()
