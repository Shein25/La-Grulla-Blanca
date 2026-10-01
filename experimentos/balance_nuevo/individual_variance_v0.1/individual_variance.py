"""Prototype generator for intra-species monster variance v0.1.

LAB only. One species id, one q roll, coordinated stats.
Does not alter technique params or adaptive tier.
"""
from __future__ import annotations
import json,random
from pathlib import Path

HERE=Path(__file__).resolve().parent
CONFIG=json.loads((HERE/"monster_individual_variance_v0.1.json").read_text(encoding="utf-8"))

def roll_q(rng:random.Random)->float:
    x=rng.random()
    acc=0.0
    for band in CONFIG["quality_distribution"]:
        acc+=band["probability"]
        if x<=acc:
            return rng.uniform(band["q_min"],band["q_max"])
    return 1.0

def lerp_int(a,b,q):
    return int(round(a+q*(b-a)))

def discrete_ladder(ladder,q):
    if not ladder:return None
    if len(ladder)==1:return ladder[0]
    idx=min(len(ladder)-1,int(q*len(ladder)))
    return ladder[idx]

def instantiate(species_id:str,seed:int)->dict:
    spec=CONFIG["species"][species_id]
    if spec.get("status")=="BLOCKED_UNTIL_T0_LOCAL_REFINEMENT_READY":
        raise RuntimeError(f"{species_id}: variance blocked until T0 READY")
    rng=random.Random(seed)
    q=roll_q(rng)
    base=spec["base"];ceil=spec["natural_ceiling"]
    stats={}
    for key in CONFIG["coordinated_stats"]:
        stats[key]=lerp_int(base[key],ceil[key],q)
    stats["basic_damage"]=discrete_ladder(spec["basic_damage_ladder"],q)
    return {
        "species_id":species_id,
        "individual_quality":q,
        "stats":stats,
        "source_base_trial":base["source_trial"],
        "source_ceiling_trial":ceil["source_trial"],
    }

def selfcheck():
    for species_id,spec in CONFIG["species"].items():
        if spec.get("status")=="BLOCKED_UNTIL_T0_LOCAL_REFINEMENT_READY":
            continue
        for seed in range(1000):
            x=instantiate(species_id,seed)
            assert 0<=x["individual_quality"]<=1
            for k in CONFIG["coordinated_stats"]:
                lo=min(spec["base"][k],spec["natural_ceiling"][k])
                hi=max(spec["base"][k],spec["natural_ceiling"][k])
                assert lo<=x["stats"][k]<=hi,(species_id,k,x)
            assert x["stats"]["basic_damage"] in spec["basic_damage_ladder"]
    print("PASS: coordinated intra-species variance bounds hold for 4 READY species")

if __name__=="__main__":
    selfcheck()
