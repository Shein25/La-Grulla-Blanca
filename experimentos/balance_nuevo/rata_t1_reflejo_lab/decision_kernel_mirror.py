"""Exact scoring mirror for Rata T1 decision-aware Monte Carlo.

This mirrors Monster Combat AI v0.1 for the *specific* T1 Rata choice:
BASIC vs Reflejo de Madriguera. It does not replace the generic JS kernel.

CI parity tests compare this module against the original JS selector on the
adaptive branch. Any divergence must fail before Monte Carlo is trusted.
"""
from __future__ import annotations
from dataclasses import dataclass

TIE_TOLERANCE=1e-9
REPETITION_PENALTY=5.0
JITTER=3.0

BASIC_ID="rata_qi__basic"
SURVIVAL_ID="rata_qi__survival_1"
SURVIVAL_COOLDOWN_KEY=f"{SURVIVAL_ID}__cooldown"

class Mulberry32:
    def __init__(self,seed:int):
        self.a=int(seed)&0xFFFFFFFF
    def random(self)->float:
        self.a=(self.a+0x6D2B79F5)&0xFFFFFFFF
        t=self.a
        t=((t ^ (t>>15)) * (1|t)) & 0xFFFFFFFF
        t=(t + (((t ^ (t>>7)) * (61|t)) & 0xFFFFFFFF)) ^ t
        t&=0xFFFFFFFF
        return ((t ^ (t>>14)) & 0xFFFFFFFF) / 4294967296.0

@dataclass(frozen=True)
class Decision:
    ability_id:str
    basic_score:float|None
    survival_score:float|None
    tie_broken_by_rng:bool

def _jitter(rng:Mulberry32)->float:
    return (rng.random()*2.0-1.0)*JITTER

def choose_rata_t1_intent(*,signals:dict,recent_actions:list[str],survival_on_cooldown:bool,rng:Mulberry32)->Decision:
    # Exact canonical ability-id order: BASIC sorts before SURVIVAL.
    basic_score=40.0
    if signals.get("PLAYER_LOW_HP",False):
        basic_score+=5.0
    basic_score-=REPETITION_PENALTY*sum(1 for x in recent_actions if x=="BASIC")
    basic_score+=_jitter(rng)

    survival_score=None
    if not survival_on_cooldown:
        survival_score=18.0
        if signals.get("SELF_LOW_HP",False):
            survival_score+=22.0
        if signals.get("TOOK_HEAVY_HIT",False):
            survival_score+=10.0
        if signals.get("PLAYER_LOW_HP",False):
            survival_score+=3.0
        survival_score-=REPETITION_PENALTY*sum(1 for x in recent_actions if x=="SURVIVAL")
        survival_score+=_jitter(rng)

    if survival_score is None:
        return Decision(BASIC_ID,basic_score,None,False)

    top=max(basic_score,survival_score)
    candidates=[]
    if abs(basic_score-top)<=TIE_TOLERANCE:candidates.append(BASIC_ID)
    if abs(survival_score-top)<=TIE_TOLERANCE:candidates.append(SURVIVAL_ID)
    if len(candidates)==1:
        chosen=candidates[0];tie=False
    else:
        idx=int(rng.random()*len(candidates))
        idx=min(idx,len(candidates)-1)
        chosen=sorted(candidates)[idx]
        tie=True
    return Decision(chosen,basic_score,survival_score,tie)

PARITY_CASES=[
    {"name":"neutral","signals":{},"recent_actions":[],"cooldown":False,"seed":1},
    {"name":"heavy_only","signals":{"TOOK_HEAVY_HIT":True},"recent_actions":[],"cooldown":False,"seed":2},
    {"name":"self_low","signals":{"SELF_LOW_HP":True},"recent_actions":[],"cooldown":False,"seed":3},
    {"name":"self_low_heavy","signals":{"SELF_LOW_HP":True,"TOOK_HEAVY_HIT":True},"recent_actions":[],"cooldown":False,"seed":4},
    {"name":"all_signals","signals":{"SELF_LOW_HP":True,"TOOK_HEAVY_HIT":True,"PLAYER_LOW_HP":True},"recent_actions":[],"cooldown":False,"seed":5},
    {"name":"recent_basic","signals":{"SELF_LOW_HP":True},"recent_actions":["BASIC","BASIC"],"cooldown":False,"seed":6},
    {"name":"recent_survival","signals":{"SELF_LOW_HP":True,"TOOK_HEAVY_HIT":True},"recent_actions":["SURVIVAL"],"cooldown":False,"seed":7},
    {"name":"cooldown","signals":{"SELF_LOW_HP":True,"TOOK_HEAVY_HIT":True},"recent_actions":[],"cooldown":True,"seed":8},
    {"name":"player_low_only","signals":{"PLAYER_LOW_HP":True},"recent_actions":[],"cooldown":False,"seed":9},
    {"name":"mixed_recent","signals":{"SELF_LOW_HP":True,"PLAYER_LOW_HP":True},"recent_actions":["BASIC","SURVIVAL","BASIC"],"cooldown":False,"seed":10},
]

def parity_results():
    out=[]
    for case in PARITY_CASES:
        d=choose_rata_t1_intent(
            signals=case["signals"],
            recent_actions=case["recent_actions"],
            survival_on_cooldown=case["cooldown"],
            rng=Mulberry32(case["seed"]),
        )
        out.append({
            **case,
            "ability_id":d.ability_id,
            "basic_score":d.basic_score,
            "survival_score":d.survival_score,
            "tie_broken_by_rng":d.tie_broken_by_rng,
        })
    return out

if __name__=="__main__":
    import argparse,json
    ap=argparse.ArgumentParser()
    ap.add_argument("--parity-out")
    args=ap.parse_args()
    data=parity_results()
    if args.parity_out:
        with open(args.parity_out,"w",encoding="utf-8") as f:
            json.dump(data,f,ensure_ascii=False,indent=2,sort_keys=True)
    else:
        print(json.dumps(data,ensure_ascii=False,indent=2,sort_keys=True))
