"""Pure T2 recognition kernel for Rata LAB.

No combat numbers are changed here. It only classifies observable player
actions and decides whether a recent repeated pattern is recognized.
"""
from __future__ import annotations

ALLOWED_CATEGORIES={
    "PLAYER_BASIC",
    "PLAYER_UNITARGET_TECHNIQUE",
    "PLAYER_AOE_TECHNIQUE",
    "PLAYER_DEFENSIVE_TECHNIQUE",
}
ALLOWED_RESULTS={"EFECTIVA","FALLIDA"}

def classify_player_action(compiled:dict|None, *, basic:bool=False)->str:
    if basic:
        return "PLAYER_BASIC"
    if not isinstance(compiled,dict):
        raise TypeError("compiled observable action required")
    role=str(compiled.get("role",""))
    targeting=str(compiled.get("targeting",""))
    if role=="DEFENSIVE":
        return "PLAYER_DEFENSIVE_TECHNIQUE"
    if targeting=="AOE":
        return "PLAYER_AOE_TECHNIQUE"
    return "PLAYER_UNITARGET_TECHNIQUE"

def observe(category:str,result:str)->dict:
    if category not in ALLOWED_CATEGORIES:
        raise ValueError(f"unknown observable category: {category}")
    if result not in ALLOWED_RESULTS:
        raise ValueError(f"unknown observable result: {result}")
    return {"category":category,"result":result}

def recognize_recent_pattern(memory:list[dict],candidate:dict)->dict:
    window=int(candidate["memory_window"])
    required=int(candidate["repeated_same_category_required"])
    accepted=set(candidate.get("count_results",["EFECTIVA"]))
    if window<required or required<2:
        raise ValueError("invalid recognition window")
    visible=[
        ev for ev in memory[-window:]
        if ev.get("category") in ALLOWED_CATEGORIES and ev.get("result") in accepted
    ]
    if len(visible)<required:
        return {"recognized":False,"category":None,"support":0}
    tail=visible[-required:]
    category=tail[-1]["category"]
    same=all(ev["category"]==category for ev in tail)
    return {
        "recognized":same,
        "category":category if same else None,
        "support":required if same else 0,
    }
