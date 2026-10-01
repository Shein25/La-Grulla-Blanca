"""Colab overnight runner for all five LianQi I monsters.

NO raw fight rows are persisted. Each fight is aggregated and discarded.
Canonical registry remains untouched; all outputs are LAB only.
"""
from __future__ import annotations

import argparse
import gzip
import json
import math
import os
from pathlib import Path
import shutil
import sys
import time
import zipfile

HERE=Path(__file__).resolve().parent
PARENT=HERE.parent
if str(PARENT) not in sys.path:
    sys.path.insert(0,str(PARENT))

import optuna
import etapa19b_combat_engine as engine

from candidate import candidate_id
from contexts import PRIMARY_CONTEXTS,ROOTS
from objective_contract import objective_directions,OBJECTIVES_BY_SPECIES
from objective_eval import objective_values
from optuna_study import create_species_study
from proposal import suggest_candidate,candidate_from_params
from runner import fight_candidate_once
from seeds import stable_seed
from stream_aggregate import StreamingFightAggregate

SPECIES=("rata_qi","avispa_jade","serpiente_qi","mono_pildoras","lobo_espiritual")

PRESETS={
    "smoke":{"trials":4,"search_fights":2,"pareto_cap":4,"revalidate_fights":5,"final_cap":3,"final_fights":10},
    "overnight":{"trials":1500,"search_fights":100,"pareto_cap":50,"revalidate_fights":1000,"final_cap":5,"final_fights":5000},
    "deep":{"trials":3000,"search_fights":150,"pareto_cap":75,"revalidate_fights":2000,"final_cap":7,"final_fights":10000},
}

REGISTRY_PATH=PARENT/"monster_arc1_registry.json"
TECHNIQUES_PATH=PARENT/"techniques_arc1_catalog.json"
EQUIPMENT_PATH=PARENT/"equipment_arc1_catalog.json"


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path,obj):
    Path(path).write_text(json.dumps(obj,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")


def write_json_gz(path,obj):
    with gzip.open(path,"wt",encoding="utf-8",compresslevel=9) as fh:
        json.dump(obj,fh,ensure_ascii=False,sort_keys=True,separators=(",",":"))


def base_paths(root):
    return {tid:() for tid in engine.ROOT_TECHNIQUES[root]}


def evaluate_candidate(candidate,trial_number,canonical,techniques,equipment,fights_per_context,namespace):
    agg=StreamingFightAggregate()
    for ctx in PRIMARY_CONTEXTS:
        item_ids=equipment["simulation_loadouts"][ctx.loadout_profile]["LianQi_I"]
        for root in ROOTS:
            paths=base_paths(root)
            for fight_index in range(fights_per_context):
                seed=stable_seed(candidate.species_id,namespace,ctx.context_id,root,fight_index,trial_number if namespace.startswith("SEARCH") else "COMMON")
                row=fight_candidate_once(
                    candidate=candidate,
                    canonical_profile=canonical,
                    trial_number=trial_number,
                    root=root,
                    item_ids=item_ids,
                    paths=paths,
                    seed=seed,
                    policy="VETERAN",
                    technique_catalog=techniques,
                    equipment_catalog=equipment,
                )
                row["context_id"]=ctx.context_id
                row["loadout_profile"]=ctx.loadout_profile
                agg.add(row)
    return agg.finish()


def compact_summary(a):
    keys=(
        "fights","win_rate","loss_rate","timeout_rate","rounds_mean",
        "hp_final_pct_mean","hp_final_pct_p10","hp_min_pct_mean",
        "qi_final_mean","qi_spent_mean","qi_drained_mean",
        "player_hit_rate","monster_hit_rate","control_success_rate",
        "defensive_activation_mean","monster_skill_use_mean","monster_basic_use_mean",
        "monster_skipped_action_mean","forced_basic_due_to_qi_mean",
        "monster_damage_total_mean","monster_damage_total_p90",
        "monster_dot_damage_mean","monster_direct_damage_mean","monster_dot_fraction",
    )
    return {k:a[k] for k in keys if k in a}


def trial_row(t):
    return {
        "number":t.number,
        "state":t.state.name,
        "values":t.values,
        "params":t.params,
        "candidate_id":t.user_attrs.get("candidate_id"),
        "candidate_hash":t.user_attrs.get("candidate_hash"),
        "metrics":t.user_attrs.get("compact_metrics"),
    }


def dominates_values(a,b,directions):
    all_ok=True; strict=False
    for av,bv,d in zip(a,b,directions):
        if d=="maximize":
            if av < bv: all_ok=False
            if av > bv: strict=True
        else:
            if av > bv: all_ok=False
            if av < bv: strict=True
    return all_ok and strict


def pareto_rows(rows,directions):
    return [
        r for i,r in enumerate(rows)
        if not any(dominates_values(o["values"],r["values"],directions) for j,o in enumerate(rows) if i!=j)
    ]


def select_coverage(rows,count):
    """Farthest-point coverage in normalized objective space; no ranking."""
    if len(rows)<=count: return list(rows)
    dims=len(rows[0]["values"])
    cols=[[float(r["values"][j]) for r in rows] for j in range(dims)]
    mins=[min(c) for c in cols]; maxs=[max(c) for c in cols]
    coords=[]
    for r in rows:
        coords.append(tuple(0.0 if maxs[j]<=mins[j] else (float(r["values"][j])-mins[j])/(maxs[j]-mins[j]) for j in range(dims)))
    chosen=[]
    for j in range(dims):
        for fn in (min,max):
            idx=fn(range(len(rows)),key=lambda i:coords[i][j])
            if idx not in chosen: chosen.append(idx)
            if len(chosen)>=count: break
        if len(chosen)>=count: break
    while len(chosen)<count:
        remaining=[i for i in range(len(rows)) if i not in chosen]
        idx=max(remaining,key=lambda i:min(math.dist(coords[i],coords[j]) for j in chosen))
        chosen.append(idx)
    return [rows[i] for i in chosen[:count]]


def export_trials_gz(study,path):
    with gzip.open(path,"wt",encoding="utf-8",compresslevel=9) as fh:
        for t in study.trials:
            fh.write(json.dumps(trial_row(t),ensure_ascii=False,sort_keys=True,separators=(",",":"))+"\n")


def run_search(species,cfg,outdir,registry,techniques,equipment):
    sdir=outdir/species
    sdir.mkdir(parents=True,exist_ok=True)
    db=sdir/f"{species}.sqlite3"
    sampler_seed=stable_seed("OPTUNA",species)%(2**32)
    study=create_species_study(
        species,
        storage_path=db,
        sampler_seed=sampler_seed,
        study_name=f"STAGE1_COLAB_ALL::{species}::V01",
    )
    canonical=registry["profiles"][species]
    target=int(cfg["trials"])
    existing=len(study.trials)
    remaining=max(0,target-existing)
    started=time.time()

    def objective(trial):
        candidate=suggest_candidate(trial,species)
        trial.set_user_attr("candidate_id",candidate_id(candidate,trial.number))
        a=evaluate_candidate(
            candidate,trial.number,canonical,techniques,equipment,
            int(cfg["search_fights"]),f"SEARCH_{cfg['search_fights']}_V01",
        )
        if a["timeout_rate"]>0:
            raise optuna.TrialPruned("timeout")
        trial.set_user_attr("compact_metrics",compact_summary(a))
        return objective_values(species,candidate,a)

    def progress(study,trial):
        done=len(study.trials)
        if done%50==0 or done==target:
            print(f"[{species}] {done}/{target} trials",flush=True)

    if remaining:
        study.optimize(objective,n_trials=remaining,n_jobs=1,callbacks=[progress])
    export_trials_gz(study,sdir/"trials.jsonl.gz")

    search_pareto=[trial_row(t) for t in study.best_trials]
    write_json_gz(sdir/"pareto_search.json.gz",search_pareto)
    coverage=select_coverage(search_pareto,int(cfg["pareto_cap"]))
    write_json_gz(sdir/"pareto_search_coverage.json.gz",coverage)

    summary={
        "species":species,"stage":"SEARCH_COMPLETE_NOT_CANON",
        "target_trials":target,"trials_total":len(study.trials),
        "search_fights_per_context":int(cfg["search_fights"]),
        "contexts_per_trial":len(PRIMARY_CONTEXTS)*len(ROOTS),
        "search_pareto":len(search_pareto),"search_coverage":len(coverage),
        "elapsed_seconds":time.time()-started,
        "sampler":"NSGAIISampler","sampler_seed":sampler_seed,
        "objective_names":[o.name for o in OBJECTIVES_BY_SPECIES[species]],
        "directions":list(objective_directions(species)),
        "canonical_modified":False,
    }
    write_json(sdir/"search_summary.json",summary)
    return study,coverage,summary


def revalidate(species,source,cfg,outdir,registry,techniques,equipment,stage,fights_per_context):
    canonical=registry["profiles"][species]
    rows=[]
    for idx,item in enumerate(source,1):
        candidate=candidate_from_params(species,dict(item["params"]))
        a=evaluate_candidate(
            candidate,int(item["number"]),canonical,techniques,equipment,
            int(fights_per_context),f"{stage}_{fights_per_context}_V01",
        )
        rows.append({
            "number":int(item["number"]),
            "candidate_id":item.get("candidate_id"),
            "candidate_hash":item.get("candidate_hash"),
            "params":item["params"],
            "values":list(objective_values(species,candidate,a)),
            "aggregate":a,
        })
        if idx%10==0 or idx==len(source):
            print(f"[{species}] {stage}: {idx}/{len(source)}",flush=True)
    front=pareto_rows(rows,objective_directions(species))
    return rows,front


def make_share_zip(outdir):
    zip_path=outdir/"RESULTADOS_PARA_ANALIZAR.zip"
    with zipfile.ZipFile(zip_path,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in outdir.rglob("*"):
            if not p.is_file() or p==zip_path: continue
            if p.suffix==".sqlite3": continue
            if p.name.endswith(".sqlite3-wal") or p.name.endswith(".sqlite3-shm"): continue
            z.write(p,p.relative_to(outdir))
    return zip_path


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--preset",choices=sorted(PRESETS),default="overnight")
    ap.add_argument("--outdir",default="STAGE1_COLAB_ALL_RESULTS")
    ap.add_argument("--species",default=",".join(SPECIES))
    ap.add_argument("--trials",type=int)
    ap.add_argument("--search-fights",type=int)
    ap.add_argument("--pareto-cap",type=int)
    ap.add_argument("--revalidate-fights",type=int)
    ap.add_argument("--final-cap",type=int)
    ap.add_argument("--final-fights",type=int)
    args=ap.parse_args()

    cfg=dict(PRESETS[args.preset])
    for key in tuple(cfg):
        val=getattr(args,key)
        if val is not None: cfg[key]=val

    selected=tuple(x.strip() for x in args.species.split(",") if x.strip())
    unknown=set(selected)-set(SPECIES)
    if unknown: raise ValueError(f"unknown species: {sorted(unknown)}")

    outdir=Path(args.outdir)
    outdir.mkdir(parents=True,exist_ok=True)
    registry=load_json(REGISTRY_PATH); techniques=load_json(TECHNIQUES_PATH); equipment=load_json(EQUIPMENT_PATH)
    global_summary={"preset":args.preset,"config":cfg,"species":list(selected),"results":{},"canonical_modified":False}

    optuna.logging.set_verbosity(optuna.logging.WARNING)

    for species in selected:
        print(f"\n=== {species} SEARCH ===",flush=True)
        study,coverage,search_summary=run_search(species,cfg,outdir,registry,techniques,equipment)

        print(f"=== {species} REVALIDATE ===",flush=True)
        all_reval,reval_front=revalidate(
            species,coverage,cfg,outdir,registry,techniques,equipment,
            "REVALIDATE",int(cfg["revalidate_fights"]),
        )
        sdir=outdir/species
        write_json_gz(sdir/"revalidate_all.json.gz",all_reval)
        write_json_gz(sdir/"revalidate_pareto.json.gz",reval_front)

        final_source=select_coverage(reval_front,int(cfg["final_cap"]))
        write_json_gz(sdir/"final_coverage_input.json.gz",final_source)

        print(f"=== {species} HIGH PRECISION COVERAGE ===",flush=True)
        high_all,high_front=revalidate(
            species,final_source,cfg,outdir,registry,techniques,equipment,
            "HIGH_PRECISION",int(cfg["final_fights"]),
        )
        write_json_gz(sdir/"high_precision_all.json.gz",high_all)
        write_json_gz(sdir/"high_precision_pareto.json.gz",high_front)

        final_summary={
            **search_summary,
            "revalidate_input":len(coverage),
            "revalidate_pareto":len(reval_front),
            "revalidate_fights_per_context":int(cfg["revalidate_fights"]),
            "high_precision_input":len(final_source),
            "high_precision_pareto":len(high_front),
            "high_precision_fights_per_context":int(cfg["final_fights"]),
            "status":"LAB_RESULTS_AWAITING_HUMAN_REVIEW",
            "selection_performed":False,
            "canonical_promotion_performed":False,
        }
        write_json(sdir/"summary.json",final_summary)
        global_summary["results"][species]=final_summary

    write_json(outdir/"GLOBAL_SUMMARY.json",global_summary)
    write_json(outdir/"MANIFEST.json",{
        "experiment":"STAGE1_INTEGRAL_T0_COLAB_ALL_V01",
        "engine_contract":"NEW_COMBAT_STATS_V0_1",
        "preset":args.preset,
        "config":cfg,
        "species":list(selected),
        "optuna_version":optuna.__version__,
        "python":sys.version,
        "no_raw_fight_rows_persisted":True,
        "sqlite_excluded_from_share_zip":True,
        "canonical_registry_modified":False,
        "t1_t4_executed":False,
        "definitives_executed":False,
        "blood_1_executed":False,
    })
    share=make_share_zip(outdir)
    print("\nDONE")
    print(f"Share this file for analysis: {share}")
    print("SQLite checkpoints remain outside the share ZIP for resume/recovery.")


if __name__=="__main__":
    main()
