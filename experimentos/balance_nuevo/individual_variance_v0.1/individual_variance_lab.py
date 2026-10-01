"""INDIVIDUAL_VARIANCE_LAB — LianQi I, five-species CPU Monte Carlo.

Purpose
-------
Validate natural intra-species defensive/offensive variance around the five
human-ratified T0 profiles, plus the rare Mutante tail.

This LAB never writes canonical monster profiles and never executes T1-T4.
Natural spawn incidence and conditional-Mutante combat are measured separately.
Raw fight rows are not persisted.

Parallelism is process-based (one species per worker), because the telemetry and
VETERAN policy use temporary monkey patches that must remain isolated.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from contextlib import contextmanager
from copy import deepcopy
from concurrent.futures import ProcessPoolExecutor, as_completed
import gzip
import json
import math
import os
from pathlib import Path
import statistics
import sys
import zipfile

HERE=Path(__file__).resolve().parent
BALANCE=HERE.parent
STAGE1=BALANCE/"stage1_integral_t0_optuna"
PARALLEL=BALANCE/"parallel_arc1_pipeline"
for p in (HERE,BALANCE,STAGE1,PARALLEL):
    if str(p) not in sys.path:
        sys.path.insert(0,str(p))

import etapa19b_combat_engine as engine
from contexts import PRIMARY_CONTEXTS,ROOTS
from individual_variance import CONFIG,instantiate
from player_policy_veteran import (
    DEFAULT_VETERAN_CONFIG,
    VETERAN_BASIC,
    choose_veteran_action,
)
from seeds import stable_seed
from streaming import StreamingAggregate,percentile
from telemetry import fight_once_observed
from guards import validate_action_space

SPECIES=("rata_qi","avispa_jade","serpiente_qi","mono_pildoras","lobo_espiritual")
PRESETS={
    "smoke":{"natural_fights":2,"mutant_fights":1},
    "directed":{"natural_fights":1000,"mutant_fights":250},
    "heavy":{"natural_fights":5000,"mutant_fights":1000},
}
BASIC_PROXY_SENTINEL_COST=10**9


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path,obj):
    Path(path).write_text(
        json.dumps(obj,ensure_ascii=False,indent=2,sort_keys=True)+"\n",
        encoding="utf-8",
    )


def write_gz(path,obj):
    with gzip.open(path,"wt",encoding="utf-8",compresslevel=9) as f:
        json.dump(obj,f,ensure_ascii=False,sort_keys=True,separators=(",",":"))


def base_paths(root):
    return {tid:() for tid in engine.ROOT_TECHNIQUES[root]}


@contextmanager
def veteran_runtime():
    """Enable the observable-only VETERAN policy without touching monster stats."""
    originals={
        "compile_build":engine.compile_build,
        "choose_player_action":engine.choose_player_action,
        "execute_player_technique":engine.execute_player_technique,
    }

    def compile_build(root,paths,catalog=None):
        compiled=originals["compile_build"](root,paths,catalog)
        compiled=dict(compiled)
        compiled[VETERAN_BASIC]={
            "technique_id":VETERAN_BASIC,
            "name":"Ataque básico",
            "root":root,
            "role":"BASIC_PROXY",
            "targeting":"UNITARGET",
            "qi_cost":BASIC_PROXY_SENTINEL_COST,
        }
        return compiled

    def choose_player_action(state,policy):
        if policy!="VETERAN":
            return originals["choose_player_action"](state,policy)
        action=choose_veteran_action(state,DEFAULT_VETERAN_CONFIG)
        validate_action_space([action])
        return action

    def execute_player_technique(state,rng,c):
        if c.get("technique_id")==VETERAN_BASIC:
            engine.execute_basic(state,rng)
            return True
        return originals["execute_player_technique"](state,rng,c)

    engine.compile_build=compile_build
    engine.choose_player_action=choose_player_action
    engine.execute_player_technique=execute_player_technique
    try:
        yield
    finally:
        for name,fn in originals.items():
            setattr(engine,name,fn)


class InstanceAggregate:
    def __init__(self):
        self.n=0
        self.mutants=0
        self.power=[]
        self.stats=defaultdict(lambda:{"sum":0.0,"min":None,"max":None})
        self.attacks=defaultdict(Counter)

    def add(self,inst):
        self.n+=1
        self.mutants+=int(bool(inst["mutant"]))
        self.power.append(float(inst["individual_power_score"]))
        for key,value in inst["stats"].items():
            x=float(value)
            s=self.stats[key]
            s["sum"]+=x
            s["min"]=x if s["min"] is None else min(s["min"],x)
            s["max"]=x if s["max"] is None else max(s["max"],x)
        for key,value in inst["attacks"].items():
            self.attacks[key][str(value)]+=1

    def finish(self):
        if not self.n:
            return None
        return {
            "instances":self.n,
            "mutants":self.mutants,
            "mutant_incidence":self.mutants/self.n,
            "power_score_mean":statistics.fmean(self.power),
            "power_score_p90":percentile(self.power,.90),
            "power_score_p99":percentile(self.power,.99),
            "stats":{
                key:{
                    "mean":v["sum"]/self.n,
                    "min":v["min"],
                    "max":v["max"],
                }
                for key,v in self.stats.items()
            },
            "attack_distribution":{
                key:{k:v/self.n for k,v in sorted(counts.items())}
                for key,counts in self.attacks.items()
            },
        }


def finish_or_none(agg):
    return None if agg.n==0 else agg.finish()


def profile_from_instance(canonical,inst):
    """Build an ephemeral READY-shaped profile; canonical registry is untouched."""
    p=deepcopy(canonical)
    for key,value in inst["stats"].items():
        p["stats"][key]=value

    attacks=inst["attacks"]
    if "basic_damage" in attacks:
        p["stats"]["basic_damage"]=attacks["basic_damage"]

    tech=p.get("technique")
    if tech is not None:
        params=tech["params"]
        if "technique_direct_damage" in attacks:
            params["direct_damage"]=attacks["technique_direct_damage"]
        if "poison_damage" in attacks:
            params["poison"]["damage"]=attacks["poison_damage"]
        if "poison_ticks" in attacks:
            params["poison"]["ticks"]=int(attacks["poison_ticks"])

    # Engine performs its normal READY/schema validation on this in-memory copy.
    return p


def fight_instance(profile,root,items,techniques,equipment,seed):
    row=fight_once_observed(
        stage="LianQi_I",
        root=root,
        item_ids=items,
        paths=base_paths(root),
        monster_profile=profile,
        tier="T0",
        policy="VETERAN",
        seed=seed,
        technique_catalog=techniques,
        equipment_catalog=equipment,
    )
    return row


def sample_mutant(species,namespace,context_id,root,index,max_attempts=20000):
    """Exact rejection sample from the natural generator conditional on Mutante."""
    for attempt in range(max_attempts):
        seed=stable_seed(
            "INDIVIDUAL_VARIANCE_LAB_V01",
            "MUTANT_CONDITIONAL",
            namespace,species,context_id,root,index,attempt,
        )
        inst=instantiate(species,seed)
        if inst["mutant"]:
            return inst,attempt+1
    raise RuntimeError(
        f"{species}: failed to sample Mutante after {max_attempts} attempts"
    )


def evaluate_species(species,natural_n,mutant_n,namespace):
    registry=load_json(BALANCE/"monster_arc1_registry.json")
    techniques=load_json(BALANCE/"techniques_arc1_catalog.json")
    equipment=load_json(BALANCE/"equipment_arc1_catalog.json")
    canonical=registry["profiles"][species]
    if canonical["stats_status"]!="READY":
        raise RuntimeError(f"{species}: canonical T0 must be READY")

    natural_all=StreamingAggregate()
    natural_normal=StreamingAggregate()
    natural_mutant=StreamingAggregate()
    conditional_mutant=StreamingAggregate()

    natural_instances=InstanceAggregate()
    conditional_instances=InstanceAggregate()
    rejection_attempts=0
    conditional_accepted=0

    with veteran_runtime():
        for ctx in PRIMARY_CONTEXTS:
            items=equipment["simulation_loadouts"][ctx.loadout_profile]["LianQi_I"]
            for root in ROOTS:
                for i in range(natural_n):
                    instance_seed=stable_seed(
                        "INDIVIDUAL_VARIANCE_LAB_V01",
                        "NATURAL",namespace,species,ctx.context_id,root,i,"INSTANCE",
                    )
                    combat_seed=stable_seed(
                        "INDIVIDUAL_VARIANCE_LAB_V01",
                        "NATURAL",namespace,species,ctx.context_id,root,i,"COMBAT",
                    )
                    inst=instantiate(species,instance_seed)
                    profile=profile_from_instance(canonical,inst)
                    row=fight_instance(profile,root,items,techniques,equipment,combat_seed)
                    row["loadout_profile"]=ctx.loadout_profile
                    natural_all.add(row)
                    natural_instances.add(inst)
                    if inst["mutant"]:
                        natural_mutant.add(row)
                    else:
                        natural_normal.add(row)

                for i in range(mutant_n):
                    inst,attempts=sample_mutant(
                        species,namespace,ctx.context_id,root,i
                    )
                    rejection_attempts+=attempts
                    conditional_accepted+=1
                    combat_seed=stable_seed(
                        "INDIVIDUAL_VARIANCE_LAB_V01",
                        "MUTANT_CONDITIONAL",namespace,species,ctx.context_id,root,i,"COMBAT",
                    )
                    profile=profile_from_instance(canonical,inst)
                    row=fight_instance(profile,root,items,techniques,equipment,combat_seed)
                    row["loadout_profile"]=ctx.loadout_profile
                    conditional_mutant.add(row)
                    conditional_instances.add(inst)

    return {
        "species_id":species,
        "canonical_t0_stats":canonical["stats"],
        "canonical_t0_technique":canonical["technique"],
        "natural":{
            "combat_all":natural_all.finish(),
            "combat_normal":finish_or_none(natural_normal),
            "combat_mutant_observed":finish_or_none(natural_mutant),
            "instances":natural_instances.finish(),
        },
        "mutant_conditional":{
            "combat":conditional_mutant.finish(),
            "instances":conditional_instances.finish(),
            "accepted":conditional_accepted,
            "generation_attempts":rejection_attempts,
            "acceptance_rate":(
                conditional_accepted/rejection_attempts if rejection_attempts else 0.0
            ),
            "sampling":"exact rejection sampling from natural generator; not used to estimate natural incidence",
        },
    }


def zip_results(outdir):
    z=outdir/"RESULTADOS_INDIVIDUAL_VARIANCE_LAB_LIANQI_I_V01.zip"
    with zipfile.ZipFile(z,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as zz:
        for p in sorted(outdir.rglob("*")):
            if p.is_file() and p!=z:
                zz.write(p,p.relative_to(outdir))
    return z


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--preset",choices=PRESETS,default="heavy")
    ap.add_argument("--natural-fights",type=int)
    ap.add_argument("--mutant-fights",type=int)
    ap.add_argument("--workers",type=int,default=min(5,max(1,os.cpu_count() or 1)))
    ap.add_argument("--species",choices=SPECIES,default=None,help="optional one-species focused run")
    ap.add_argument("--outdir",default="INDIVIDUAL_VARIANCE_LAB_LIANQI_I_V01")
    ap.add_argument("--namespace",default="RUN")
    args=ap.parse_args()

    cfg=dict(PRESETS[args.preset])
    if args.natural_fights is not None:
        cfg["natural_fights"]=args.natural_fights
    if args.mutant_fights is not None:
        cfg["mutant_fights"]=args.mutant_fights
    if cfg["natural_fights"]<1 or cfg["mutant_fights"]<1:
        raise ValueError("fight counts must be >=1")

    outdir=Path(args.outdir)
    outdir.mkdir(parents=True,exist_ok=True)

    selected_species=(args.species,) if args.species else SPECIES
    results={}
    workers=max(1,min(int(args.workers),len(selected_species)))
    if workers==1:
        for species in selected_species:
            print(f"RUN {species}",flush=True)
            results[species]=evaluate_species(
                species,cfg["natural_fights"],cfg["mutant_fights"],args.namespace
            )
    else:
        with ProcessPoolExecutor(max_workers=workers) as pool:
            futs={
                pool.submit(
                    evaluate_species,s,cfg["natural_fights"],cfg["mutant_fights"],args.namespace
                ):s
                for s in selected_species
            }
            for fut in as_completed(futs):
                species=futs[fut]
                results[species]=fut.result()
                print(f"DONE {species}",flush=True)

    ordered={s:results[s] for s in selected_species}
    for species,data in ordered.items():
        write_gz(outdir/f"{species}.json.gz",data)

    natural_instances=sum(
        x["natural"]["instances"]["instances"] for x in ordered.values()
    )
    natural_mutants=sum(
        x["natural"]["instances"]["mutants"] for x in ordered.values()
    )
    summary={
        "experiment":"INDIVIDUAL_VARIANCE_LAB_LIANQI_I_V01",
        "status":"LAB_RESULTS_AWAITING_HUMAN_REVIEW",
        "species":list(selected_species),
        "species_count":len(selected_species),
        "expanded_contexts_per_species":len(PRIMARY_CONTEXTS)*len(ROOTS),
        "natural_fights_per_expanded_context":cfg["natural_fights"],
        "conditional_mutant_fights_per_expanded_context":cfg["mutant_fights"],
        "natural_fights_total":natural_instances,
        "conditional_mutant_fights_total":sum(
            x["mutant_conditional"]["accepted"] for x in ordered.values()
        ),
        "natural_mutants_observed":natural_mutants,
        "natural_mutant_incidence":natural_mutants/natural_instances,
        "mutant_target_incidence":CONFIG["mutant"]["target_incidence"],
        "mutant_maximum_incidence":CONFIG["mutant"]["maximum_incidence"],
        "mutant_rewards":{
            "loot_multiplier":CONFIG["mutant"]["loot_multiplier"],
            "xp_multiplier":CONFIG["mutant"]["xp_multiplier"],
        },
        "automatic_runtime_activation":False,
        "canonical_write":False,
        "t1_t4_executed":False,
        "raw_fights_persisted":False,
        "workers":workers,
    }
    write_json(outdir/"SUMMARY.json",summary)
    write_json(outdir/"MANIFEST.json",{
        "engine_contract":"NEW_COMBAT_STATS_V0_1",
        "canonical_t0_required":True,
        "all_five_lianqi_i_ready":True,
        "natural_spawn_sampling":"independent per-axis uniform rolls",
        "conditional_mutant_sampling":"rejection sampling from same natural generator",
        "mutant_incidence_source":"natural arm only",
        "mutant_suffix":"Mutante",
        "loot_multiplier":1.5,
        "xp_multiplier":1.5,
        "no_new_species_ids":True,
        "identity_mechanics_fixed":True,
        "t1_t4_executed":False,
        "canonical_write":False,
        "raw_fights_persisted":False,
    })
    z=zip_results(outdir)
    print("DONE",z,flush=True)


if __name__=="__main__":
    main()
