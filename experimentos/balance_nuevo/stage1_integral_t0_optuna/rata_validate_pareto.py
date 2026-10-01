"""Revalidación high-fidelity del frente Pareto de Rata T0.

Usa common random numbers: todos los candidatos enfrentan exactamente las
mismas seeds por contexto/raíz/índice de pelea. No selecciona CANON.
"""
from __future__ import annotations

import argparse
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
from objective_eval import objective_values
from proposal import candidate_from_params
from runner import fight_candidate_once
from seeds import stable_seed

REGISTRY_PATH=PARENT/"monster_arc1_registry.json"
TECHNIQUES_PATH=PARENT/"techniques_arc1_catalog.json"
EQUIPMENT_PATH=PARENT/"equipment_arc1_catalog.json"


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def base_paths(root: str) -> dict[str,tuple]:
    return {tid:() for tid in engine.ROOT_TECHNIQUES[root]}


def dominates(a,b) -> bool:
    # Objective 0 maximize pressure; objective 1 minimize budget.
    return (
        a["values"][0]>=b["values"][0]
        and a["values"][1]<=b["values"][1]
        and (
            a["values"][0]>b["values"][0]
            or a["values"][1]<b["values"][1]
        )
    )


def pareto_front(rows):
    return [
        row for i,row in enumerate(rows)
        if not any(dominates(other,row) for j,other in enumerate(rows) if i!=j)
    ]


def evaluate_common(
    candidate,
    *,
    trial_number: int,
    canonical_profile: dict,
    techniques: dict,
    equipment: dict,
    fights_per_context: int,
    seed_namespace: str,
):
    rows=[]
    for ctx in PRIMARY_CONTEXTS:
        item_ids=equipment["simulation_loadouts"][ctx.loadout_profile]["LianQi_I"]
        for root in ROOTS:
            for fight_index in range(fights_per_context):
                # Deliberadamente independiente de candidato/trial.
                seed=stable_seed(
                    "rata_qi",
                    seed_namespace,
                    ctx.context_id,
                    root,
                    fight_index,
                )
                row=fight_candidate_once(
                    candidate=candidate,
                    canonical_profile=canonical_profile,
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
    return aggregate_fights(rows)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--source",required=True)
    ap.add_argument("--outdir",required=True)
    ap.add_argument("--fights-per-context",type=int,default=500)
    ap.add_argument("--seed-namespace",default="PARETO_500_COMMON_V01")
    args=ap.parse_args()

    source=load_json(args.source)
    if not isinstance(source,list) or not source:
        raise ValueError("source Pareto must be a non-empty JSON list")

    registry=load_json(REGISTRY_PATH)
    techniques=load_json(TECHNIQUES_PATH)
    equipment=load_json(EQUIPMENT_PATH)
    canonical=registry["profiles"]["rata_qi"]

    out=[]
    for idx,item in enumerate(source,1):
        trial_number=int(item["number"])
        candidate=candidate_from_params("rata_qi",dict(item["params"]))
        aggregate=evaluate_common(
            candidate,
            trial_number=trial_number,
            canonical_profile=canonical,
            techniques=techniques,
            equipment=equipment,
            fights_per_context=args.fights_per_context,
            seed_namespace=args.seed_namespace,
        )
        values=list(objective_values("rata_qi",candidate,aggregate))
        row={
            "number":trial_number,
            "candidate_id":item.get("candidate_id"),
            "candidate_hash":item.get("candidate_hash"),
            "params":item["params"],
            "source_values":item["values"],
            "values":values,
            "delta_pressure":values[0]-float(item["values"][0]),
            "aggregate_summary":aggregate,
        }
        out.append(row)
        print(json.dumps({
            "validated":idx,
            "total":len(source),
            "number":trial_number,
            "pressure":values[0],
            "budget":values[1],
            "win_rate":aggregate["win_rate"],
        },sort_keys=True))

    front=sorted(pareto_front(out),key=lambda x:(x["values"][1],-x["values"][0]))
    outdir=Path(args.outdir)
    outdir.mkdir(parents=True,exist_ok=True)
    (outdir/"rata_pareto_500_all.json").write_text(
        json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+"\n",
        encoding="utf-8",
    )
    (outdir/"rata_pareto_500_front.json").write_text(
        json.dumps(front,ensure_ascii=False,indent=2,sort_keys=True)+"\n",
        encoding="utf-8",
    )
    report={
        "status":"PARETO_REVALIDATED_NOT_CANON",
        "source_candidates":len(source),
        "revalidated_candidates":len(out),
        "surviving_pareto_candidates":len(front),
        "fights_per_context":args.fights_per_context,
        "contexts":len(PRIMARY_CONTEXTS)*len(ROOTS),
        "fights_per_candidate":args.fights_per_context*len(PRIMARY_CONTEXTS)*len(ROOTS),
        "total_fights":len(out)*args.fights_per_context*len(PRIMARY_CONTEXTS)*len(ROOTS),
        "seed_policy":"COMMON_RANDOM_NUMBERS",
        "seed_namespace":args.seed_namespace,
        "selection_performed":False,
        "canonical_promotion_performed":False,
    }
    (outdir/"rata_pareto_500_report.json").write_text(
        json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True)+"\n",
        encoding="utf-8",
    )
    print(json.dumps(report,ensure_ascii=False,indent=2))


if __name__=="__main__":
    main()
