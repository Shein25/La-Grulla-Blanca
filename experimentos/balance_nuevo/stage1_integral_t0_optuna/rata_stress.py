"""Stress/control validation for neutral Rata Pareto representatives.

Evaluates HIGH_ROLL_STRESS with VETERAN and MANDATORY/EXPECTED with the original
UNITARGET_FIRST policy. Uses common random numbers within each context/root.
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
from contexts import ROOTS,STRESS_CONTEXTS
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


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--source",required=True)
    ap.add_argument("--outdir",required=True)
    ap.add_argument("--fights-per-context",type=int,default=1000)
    ap.add_argument("--seed-namespace",default="STRESS_1000_COMMON_V01")
    args=ap.parse_args()

    selected=load_json(args.source)
    if not isinstance(selected,list) or not selected:
        raise ValueError("coverage source must be a non-empty JSON list")

    registry=load_json(REGISTRY_PATH)
    techniques=load_json(TECHNIQUES_PATH)
    equipment=load_json(EQUIPMENT_PATH)
    canonical=registry["profiles"]["rata_qi"]

    output=[]
    for item in selected:
        candidate=candidate_from_params("rata_qi",dict(item["params"]))
        trial_number=int(item["number"])
        contexts={}
        for ctx in STRESS_CONTEXTS:
            if not ctx.enabled:
                continue
            rows=[]
            item_ids=equipment["simulation_loadouts"][ctx.loadout_profile]["LianQi_I"]
            for root in ROOTS:
                for fight_index in range(args.fights_per_context):
                    seed=stable_seed(
                        "rata_qi",
                        args.seed_namespace,
                        ctx.context_id,
                        root,
                        fight_index,
                    )
                    row=fight_candidate_once(
                        candidate=candidate,
                        canonical_profile=canonical,
                        trial_number=trial_number,
                        root=root,
                        item_ids=item_ids,
                        paths=base_paths(root),
                        seed=seed,
                        policy=ctx.player_policy,
                        technique_catalog=techniques,
                        equipment_catalog=equipment,
                    )
                    row["context_id"]=ctx.context_id
                    row["loadout_profile"]=ctx.loadout_profile
                    rows.append(row)
            contexts[ctx.context_id]={
                "policy":ctx.player_policy,
                "loadout_profile":ctx.loadout_profile,
                "role":ctx.role,
                "aggregate":aggregate_fights(rows),
            }

        output.append({
            "number":trial_number,
            "coverage_fraction":item.get("coverage_fraction"),
            "coverage_arc_position":item.get("coverage_arc_position"),
            "params":item["params"],
            "primary_1000_values":item["values"],
            "primary_1000_aggregate":item.get("aggregate_summary"),
            "stress_contexts":contexts,
        })

    outdir=Path(args.outdir)
    outdir.mkdir(parents=True,exist_ok=True)
    (outdir/"rata_stress_1000.json").write_text(
        json.dumps(output,ensure_ascii=False,indent=2,sort_keys=True)+"\n",
        encoding="utf-8",
    )
    report={
        "status":"STRESS_COMPLETE_NOT_CANON",
        "representatives":len(output),
        "stress_contexts_per_candidate":len([x for x in STRESS_CONTEXTS if x.enabled]),
        "roots_per_context":len(ROOTS),
        "fights_per_context_root":args.fights_per_context,
        "total_fights":(
            len(output)
            * len([x for x in STRESS_CONTEXTS if x.enabled])
            * len(ROOTS)
            * args.fights_per_context
        ),
        "seed_policy":"COMMON_RANDOM_NUMBERS",
        "seed_namespace":args.seed_namespace,
        "selection_performed":False,
        "canonical_promotion_performed":False,
    }
    (outdir/"rata_stress_1000_report.json").write_text(
        json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True)+"\n",
        encoding="utf-8",
    )
    print(json.dumps(report,ensure_ascii=False,indent=2))


if __name__=="__main__":
    main()
