"""Smoke REAL de Optuna para Rata de Qi T0.

Default: 32 trials × 10 contextos primarios × 20 peleas = 6.400 peleas.
No promueve candidatos ni modifica monster_arc1_registry.json.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
PARENT=HERE.parent
if str(PARENT) not in sys.path:
    sys.path.insert(0,str(PARENT))

import etapa19b_combat_engine as engine

from aggregate import aggregate_fights
from contexts import PRIMARY_CONTEXTS,ROOTS
from optuna_study import DegenerateCandidate,create_species_study,run_species_study
from runner import fight_candidate_once
from seeds import MASTER_SEED,stable_seed

REGISTRY_PATH=PARENT/"monster_arc1_registry.json"
TECHNIQUES_PATH=PARENT/"techniques_arc1_catalog.json"
EQUIPMENT_PATH=PARENT/"equipment_arc1_catalog.json"


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def base_paths(root: str) -> dict[str,tuple]:
    return {tid:() for tid in engine.ROOT_TECHNIQUES[root]}


def make_evaluator(*,fights_per_context: int):
    registry=load_json(REGISTRY_PATH)
    techniques=load_json(TECHNIQUES_PATH)
    equipment=load_json(EQUIPMENT_PATH)
    canonical=registry["profiles"]["rata_qi"]

    def evaluate(candidate,trial_number: int):
        rows=[]
        for ctx in PRIMARY_CONTEXTS:
            item_ids=equipment["simulation_loadouts"][ctx.loadout_profile]["LianQi_I"]
            for root in ROOTS:
                for fight_index in range(fights_per_context):
                    seed=stable_seed(
                        "rata_qi",trial_number,ctx.context_id,root,fight_index
                    )
                    row=fight_candidate_once(
                        candidate=candidate,
                        canonical_profile=canonical,
                        trial_number=trial_number,
                        root=root,
                        item_ids=item_ids,
                        paths=base_paths(root),
                        seed=seed,
                        technique_catalog=techniques,
                        equipment_catalog=equipment,
                    )
                    row["context_id"]=ctx.context_id
                    row["loadout_profile"]=ctx.loadout_profile
                    rows.append(row)
        aggregate=aggregate_fights(rows)
        if aggregate["timeout_rate"]>0:
            raise DegenerateCandidate("timeout detected in Rata smoke")
        return aggregate
    return evaluate


def export_trials(study,outdir: Path) -> None:
    outdir.mkdir(parents=True,exist_ok=True)
    fields=[
        "number","state","values","params","candidate_id","candidate_hash",
        "win_rate_observed","timeout_rate","hp_final_pct_mean","fights",
    ]
    with (outdir/"rata_smoke_trials.csv").open("w",newline="",encoding="utf-8") as fh:
        w=csv.DictWriter(fh,fieldnames=fields);w.writeheader()
        for t in study.trials:
            w.writerow({
                "number":t.number,
                "state":t.state.name,
                "values":json.dumps(t.values),
                "params":json.dumps(t.params,sort_keys=True),
                "candidate_id":t.user_attrs.get("candidate_id"),
                "candidate_hash":t.user_attrs.get("candidate_hash"),
                "win_rate_observed":t.user_attrs.get("win_rate_observed"),
                "timeout_rate":t.user_attrs.get("timeout_rate"),
                "hp_final_pct_mean":t.user_attrs.get("hp_final_pct_mean"),
                "fights":t.user_attrs.get("fights"),
            })
    with (outdir/"rata_smoke_trials.jsonl").open("w",encoding="utf-8") as fh:
        for t in study.trials:
            fh.write(json.dumps({
                "number":t.number,
                "state":t.state.name,
                "values":t.values,
                "params":t.params,
                "user_attrs":t.user_attrs,
            },ensure_ascii=False,sort_keys=True)+"\n")


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--trials",type=int,default=32)
    ap.add_argument("--fights-per-context",type=int,default=20)
    ap.add_argument("--outdir",default="stage1_rata_smoke_output")
    ap.add_argument("--storage",default="stage1_rata_smoke_output/rata_qi.sqlite3")
    ap.add_argument("--sampler-seed",type=int,default=MASTER_SEED)
    args=ap.parse_args()

    study=create_species_study(
        "rata_qi",
        storage_path=args.storage,
        sampler_seed=args.sampler_seed,
        study_name="STAGE1_INTEGRAL_T0_OPTUNA::rata_qi::SMOKE_V01",
    )
    run_species_study(
        "rata_qi",
        study=study,
        evaluator=make_evaluator(fights_per_context=args.fights_per_context),
        n_trials=args.trials,
    )
    export_trials(study,Path(args.outdir))
    print(json.dumps({
        "status":"SMOKE_COMPLETE_NOT_CANON",
        "species":"rata_qi",
        "trials_total":len(study.trials),
        "fights_per_context":args.fights_per_context,
        "primary_contexts":len(PRIMARY_CONTEXTS)*len(ROOTS),
        "canonical_registry_modified":False,
    },ensure_ascii=False,indent=2))


if __name__=="__main__":
    main()
