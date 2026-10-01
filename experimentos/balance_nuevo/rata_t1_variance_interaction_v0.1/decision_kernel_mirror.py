"""Exact Rata T1 BASIC vs SURVIVAL decision mirror.

Copied without numeric changes from experiment/rata-t1-reflejo-calibration-v0.1
commit c64b08764db28e327dbb05bb04e9466cc3ca2182.
"""
from __future__ import annotations
from dataclasses import dataclass

TIE_TOLERANCE=1e-9
REPETITION_PENALTY=5.0
JITTER=3.0
BASIC_ID="rata_qi__basic"
SURVIVAL_ID="rata_qi__survival_1"

class Mulberry32:
    def __init__(self,seed:int): self.a=int(seed)&0xFFFFFFFF
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
    basic_score=40.0
    if signals.get("PLAYER_LOW_HP",False): basic_score+=5.0
    basic_score-=REPETITION_PENALTY*sum(1 for x in recent_actions if x=="BASIC")
    basic_score+=_jitter(rng)

    survival_score=None
    if not survival_on_cooldown:
        survival_score=18.0
        if signals.get("SELF_LOW_HP",False): survival_score+=22.0
        if signals.get("TOOK_HEAVY_HIT",False): survival_score+=10.0
        if signals.get("PLAYER_LOW_HP",False): survival_score+=3.0
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
        idx=min(int(rng.random()*len(candidates)),len(candidates)-1)
        chosen=sorted(candidates)[idx];tie=True
    return Decision(chosen,basic_score,survival_score,tie)
