"""Intra-species monster variance v0.3 — LAB prototype.

Defensive and offensive axes roll independently inside measured envelopes.
Rare convergence is classified as Mutante (<1%) with x1.5 loot and XP.
"""
from __future__ import annotations
import json,random
from pathlib import Path

HERE=Path(__file__).resolve().parent
CONFIG=json.loads((HERE/"monster_individual_variance_v0.1.json").read_text(encoding="utf-8"))

def lerp_int(a,b,q):
    return int(round(a+q*(b-a)))

def discrete_ladder(ladder,q):
    if len(ladder)==1:
        return ladder[0]
    idx=min(len(ladder)-1,int(q*len(ladder)))
    return ladder[idx]

def _axis_count(spec):
    n=sum(1 for k in CONFIG["variable_stats"] if spec["base"][k]!=spec["upper_envelope"][k])
    n+=sum(1 for a in spec["attacks"].values() if len(a["ladder"])>1)
    return n

def instantiate(species_id:str,seed:int)->dict:
    spec=CONFIG["species"][species_id]
    rng=random.Random(seed)
    q_by_axis={}
    stats={}
    attacks={}

    for key in CONFIG["variable_stats"]:
        a=spec["base"][key]; b=spec["upper_envelope"][key]
        if a==b:
            stats[key]=a
            continue
        q=rng.random()
        q_by_axis[key]=q
        stats[key]=lerp_int(a,b,q)

    for key,rule in spec["attacks"].items():
        ladder=rule["ladder"]
        if len(ladder)==1:
            attacks[key]=ladder[0]
            continue
        q=rng.random()
        q_by_axis[key]=q
        attacks[key]=discrete_ladder(ladder,q)

    n=_axis_count(spec)
    if n:
        power_score=sum(q_by_axis.values())/n
        threshold=CONFIG["mutant"]["threshold_by_variable_axis_count"][str(n)]
        mutant=power_score>=threshold
    else:
        power_score=0.0
        threshold=None
        mutant=False

    return {
        "species_id":species_id,
        "stats":stats,
        "attacks":attacks,
        "fixed_technique":spec.get("fixed_technique"),
        "individual_axis_quality":q_by_axis,
        "individual_power_score":power_score,
        "mutant":mutant,
        "suffix":CONFIG["mutant"]["suffix"] if mutant else None,
        "loot_multiplier":CONFIG["mutant"]["loot_multiplier"] if mutant else 1.0,
        "xp_multiplier":CONFIG["mutant"]["xp_multiplier"] if mutant else 1.0,
    }

def selfcheck(samples=50000):
    rates={}
    for species_id,spec in CONFIG["species"].items():
        mutants=0
        for seed in range(samples):
            x=instantiate(species_id,seed)
            for k in CONFIG["variable_stats"]:
                lo=min(spec["base"][k],spec["upper_envelope"][k])
                hi=max(spec["base"][k],spec["upper_envelope"][k])
                assert lo<=x["stats"][k]<=hi,(species_id,k,x)
            for key,rule in spec["attacks"].items():
                assert x["attacks"][key] in rule["ladder"],(species_id,key,x)
            if x["mutant"]:
                mutants+=1
                assert x["suffix"]=="Mutante"
                assert x["loot_multiplier"]==1.5
                assert x["xp_multiplier"]==1.5
            else:
                assert x["suffix"] is None
                assert x["loot_multiplier"]==1.0
                assert x["xp_multiplier"]==1.0
        rate=mutants/samples
        rates[species_id]=rate
        assert rate<CONFIG["mutant"]["maximum_incidence"],(species_id,rate)

    # explicit offensive variance guards
    assert len(CONFIG["species"]["rata_qi"]["attacks"]["basic_damage"]["ladder"])>1
    assert len(CONFIG["species"]["avispa_jade"]["attacks"]["poison_ticks"]["ladder"])>1
    assert len(CONFIG["species"]["serpiente_qi"]["attacks"]["poison_damage"]["ladder"])>1
    assert len(CONFIG["species"]["lobo_espiritual"]["attacks"]["technique_direct_damage"]["ladder"])>1
    assert len(CONFIG["species"]["mono_pildoras"]["attacks"]["basic_damage"]["ladder"])>1
    assert len(CONFIG["species"]["mono_pildoras"]["attacks"]["technique_direct_damage"]["ladder"])>1
    assert CONFIG["species"]["mono_pildoras"]["fixed_technique"]["qi_drain"]==5

    print("PASS: defensive and offensive individual variance stays inside measured envelopes")
    print("PASS: Mutante incidence <1%; loot and XP multipliers are exactly 1.5")
    print(json.dumps(rates,ensure_ascii=False,sort_keys=True))

if __name__=="__main__":
    selfcheck()
