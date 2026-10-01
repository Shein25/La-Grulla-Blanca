"""Rata T2 decision mirror: frozen T1 + recognition score bonus.

T1 numerical contract is immutable. T2 may only add a recognition-derived
bonus to the existing survival ability score.
"""
from __future__ import annotations
from dataclasses import dataclass
from decision_kernel_mirror import Mulberry32,BASIC_ID,SURVIVAL_ID

TIE_TOLERANCE=1e-9
REPETITION_PENALTY=5.0
JITTER=3.0

@dataclass(frozen=True)
class Decision:
    ability_id:str
    basic_score:float
    survival_score:float|None
    recognition_bonus:float
    tie_broken_by_rng:bool

def _jitter(rng:Mulberry32)->float:
    return (rng.random()*2.0-1.0)*JITTER

def choose_rata_t2_intent(*,signals:dict,recent_actions:list[str],survival_on_cooldown:bool,
                          recognition_active:bool,recognition_bonus:float,rng:Mulberry32)->Decision:
    basic_score=40.0
    if signals.get("PLAYER_LOW_HP",False): basic_score+=5.0
    basic_score-=REPETITION_PENALTY*sum(1 for x in recent_actions if x=="BASIC")
    basic_score+=_jitter(rng)

    survival_score=None
    applied=0.0
    if not survival_on_cooldown:
        survival_score=18.0
        if signals.get("SELF_LOW_HP",False): survival_score+=22.0
        if signals.get("TOOK_HEAVY_HIT",False): survival_score+=10.0
        if signals.get("PLAYER_LOW_HP",False): survival_score+=3.0
        if recognition_active:
            applied=float(recognition_bonus)
            survival_score+=applied
        survival_score-=REPETITION_PENALTY*sum(1 for x in recent_actions if x=="SURVIVAL")
        survival_score+=_jitter(rng)

    if survival_score is None:
        return Decision(BASIC_ID,basic_score,None,0.0,False)

    top=max(basic_score,survival_score)
    candidates=[]
    if abs(basic_score-top)<=TIE_TOLERANCE:candidates.append(BASIC_ID)
    if abs(survival_score-top)<=TIE_TOLERANCE:candidates.append(SURVIVAL_ID)
    if len(candidates)==1:
        chosen=candidates[0];tie=False
    else:
        idx=min(int(rng.random()*len(candidates)),len(candidates)-1)
        chosen=sorted(candidates)[idx];tie=True
    return Decision(chosen,basic_score,survival_score,applied,tie)
