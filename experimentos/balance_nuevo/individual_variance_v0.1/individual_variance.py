"""Intra-species monster variance v0.2 — LAB prototype.

Independent per-axis rolls are allowed. Rare convergence of high rolls is
classified as Mutante and receives loot_multiplier=1.5.

No new species ids, no adaptive tier grant, no runtime activation here.
"""
from __future__ import annotations
import json,random
from pathlib import Path

HERE=Path(__file__).resolve().parent
CONFIG=json.loads((HERE/"monster_individual_variance_v0.1.json").read_text(encoding="utf-8"))

def lerp_int(a,b,q):
    return int(round(a+q*(b-a)))

def discrete_ladder(ladder,q):
    if not ladder:return None
    if len(ladder)==1:return ladder[0]
    idx=min(len(ladder)-1,int(q*len(ladder)))
    return ladder[idx]

def _variable_axes(spec):
    axes=[k for k in CONFIG["variable_stats"] if spec["base"][k]!=spec["upper_envelope"][k]]
    if len(spec["basic_damage_ladder"])>1:
        axes.append("basic_damage")
    return axes

def instantiate(species_id:str,seed:int)->dict:
    spec=CONFIG["species"][species_id]
    if spec.get("status")=="BLOCKED_UNTIL_T0_LOCAL_REFINEMENT_READY":
        raise RuntimeError(f"{species_id}: variance blocked until T0 READY")

    rng=random.Random(seed)
    base=spec["base"];ceil=spec["upper_envelope"]
    q_by_axis={}
    stats={}

    for key in CONFIG["variable_stats"]:
        if base[key]==ceil[key]:
            stats[key]=base[key]
            continue
        q=rng.random()
        q_by_axis[key]=q
        stats[key]=lerp_int(base[key],ceil[key],q)

    ladder=spec["basic_damage_ladder"]
    if len(ladder)>1:
        q=rng.random()
        q_by_axis["basic_damage"]=q
        stats["basic_damage"]=discrete_ladder(ladder,q)
    else:
        stats["basic_damage"]=ladder[0]

    axes=_variable_axes(spec)
    if not axes:
        power_score=0.0
        mutant=False
        threshold=None
    else:
        power_score=sum(q_by_axis[a] for a in axes)/len(axes)
        threshold=CONFIG["mutant"]["threshold_by_variable_axis_count"][str(len(axes))]
        mutant=power_score>=threshold

    return {
        "species_id":species_id,
        "stats":stats,
        "individual_axis_quality":q_by_axis,
        "individual_power_score":power_score,
        "mutant":mutant,
        "suffix":CONFIG["mutant"]["suffix"] if mutant else None,
        "loot_multiplier":CONFIG["mutant"]["loot_multiplier"] if mutant else 1.0,
        "xp_multiplier":CONFIG["mutant"]["xp_multiplier"],
        "source_base_trial":base["source_trial"],
        "source_upper_trial":ceil["source_trial"],
    }

def selfcheck(samples=50000):
    rates={}
    for species_id,spec in CONFIG["species"].items():
        if spec.get("status")=="BLOCKED_UNTIL_T0_LOCAL_REFINEMENT_READY":
            continue
        mutants=0
        for seed in range(samples):
            x=instantiate(species_id,seed)
            assert x["species_id"]==species_id
            for k in CONFIG["variable_stats"]:
                lo=min(spec["base"][k],spec["upper_envelope"][k])
                hi=max(spec["base"][k],spec["upper_envelope"][k])
                assert lo<=x["stats"][k]<=hi,(species_id,k,x)
            assert x["stats"]["basic_damage"] in spec["basic_damage_ladder"]
            if x["mutant"]:
                mutants+=1
                assert x["suffix"]=="Mutante"
                assert x["loot_multiplier"]==1.5
                assert x["xp_multiplier"]==1.0
            else:
                assert x["suffix"] is None
                assert x["loot_multiplier"]==1.0
        rate=mutants/samples
        rates[species_id]=rate
        assert rate < CONFIG["mutant"]["maximum_incidence"],(species_id,rate)
    print("PASS: independent intra-species rolls stay inside tested envelopes")
    print("PASS: Mutante incidence <1% and loot multiplier is exactly 1.5")
    print(json.dumps(rates,ensure_ascii=False,sort_keys=True))

if __name__=="__main__":
    selfcheck()
