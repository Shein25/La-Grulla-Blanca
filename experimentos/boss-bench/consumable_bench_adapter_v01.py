#!/usr/bin/env python3
"""
CONSUMABLE BENCH ADAPTER V0.1

Authority:
- HP: ALCHEMY_VITALITY_HP_CONTRACT_V0_1.json
- Qi: ALCHEMY_QI_RECOVERY_CONTRACT_V0_2.json

Quantities 1..3 HP and 0/1 Qi are LAB stress axes, NOT inventory canon.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import json
import random
import re

STAGE = "LianQi_IV"
ARMS = (
    "NONE",
    "HP1_EXCEPTIONAL",
    "HP2_EXCEPTIONAL",
    "HP3_EXCEPTIONAL",
    "HP1_QI1_EXCEPTIONAL",
    "HP2_QI1_EXCEPTIONAL",
    "HP3_QI1_EXCEPTIONAL",
)

@dataclass(frozen=True)
class ConsumableInventory:
    arm: str
    hp_count: int
    hp_formula: str | None
    hp_min: float
    qi_count: int
    qi_restore: float

class ConsumableAuthorityError(RuntimeError):
    pass

def _load(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))

def build_inventory(
    arm: str,
    hp_contract: dict[str, Any],
    qi_contract: dict[str, Any],
) -> ConsumableInventory:
    if arm not in ARMS:
        raise ConsumableAuthorityError(f"UNKNOWN_CONSUMABLE_ARM:{arm}")
    if arm == "NONE":
        return ConsumableInventory(arm,0,None,0.0,0,0.0)

    m=re.fullmatch(r"HP([123])(?:_QI1)?_EXCEPTIONAL",arm)
    if not m:
        raise ConsumableAuthorityError(f"INVALID_CONSUMABLE_ARM:{arm}")

    hp_count=int(m.group(1))
    qi_count=1 if "_QI1_" in arm else 0
    hp=hp_contract["formulations"][STAGE]["qualities"]["excepcional"]
    qi=float(qi_contract["formulations"][STAGE]["qualities"]["excepcional"])

    return ConsumableInventory(
        arm=arm,
        hp_count=hp_count,
        hp_formula=hp["formula"],
        hp_min=float(hp["min"]),
        qi_count=qi_count,
        qi_restore=qi,
    )

def roll_dice(rng: random.Random, formula: str) -> float:
    m=re.fullmatch(r"(\d+)d(\d+)([+-]\d+)?",formula.replace(" ",""))
    if not m:
        raise ConsumableAuthorityError(f"BAD_DICE:{formula}")
    n,s,flat=int(m.group(1)),int(m.group(2)),int(m.group(3) or 0)
    return float(sum(rng.randint(1,s) for _ in range(n))+flat)

def should_drink_hp(*, hp: float, hp_max: float, potion_min: float) -> bool:
    if hp_max <= 0:
        return False
    deficit=hp_max-hp
    return hp/hp_max <= 0.60 and deficit >= potion_min

def consume_hp(
    inv: ConsumableInventory,
    *,
    hp: float,
    hp_max: float,
    rng: random.Random,
) -> tuple[ConsumableInventory,float,float]:
    if inv.hp_count <= 0 or not inv.hp_formula:
        return inv,hp,0.0
    if not should_drink_hp(hp=hp,hp_max=hp_max,potion_min=inv.hp_min):
        return inv,hp,0.0
    rolled=roll_dice(rng,inv.hp_formula)
    actual=min(max(0.0,hp_max-hp),rolled)
    return (
        ConsumableInventory(inv.arm,inv.hp_count-1,inv.hp_formula,inv.hp_min,inv.qi_count,inv.qi_restore),
        hp+actual,
        actual,
    )

def should_drink_qi_full_loadout(*, qi: float, cheapest_usable_offense_cost: float) -> bool:
    return cheapest_usable_offense_cost > 0 and qi < cheapest_usable_offense_cost

def should_drink_qi_ulti_stress(
    *,
    qi: float,
    ulti_cost: float,
    ulti_not_activated: bool,
) -> bool:
    """
    BENCH STRESS POLICY ONLY, not gameplay canon.
    Useful in ULTIS_EQUIPMENT resource-starved arms.
    """
    return ulti_not_activated and ulti_cost > 0 and qi < ulti_cost

def consume_qi(
    inv: ConsumableInventory,
    *,
    qi: float,
    qi_max: float,
) -> tuple[ConsumableInventory,float,float]:
    if inv.qi_count <= 0 or inv.qi_restore <= 0:
        return inv,qi,0.0
    actual=min(max(0.0,qi_max-qi),inv.qi_restore)
    return (
        ConsumableInventory(inv.arm,inv.hp_count,inv.hp_formula,inv.hp_min,inv.qi_count-1,inv.qi_restore),
        qi+actual,
        actual,
    )

def validate_contracts(hp_contract: dict[str,Any], qi_contract: dict[str,Any]) -> dict[str,Any]:
    failures=[]
    if hp_contract.get("status")!="READY_HUMAN_RATIFIED":
        failures.append("HP_NOT_RATIFIED")
    if qi_contract.get("status")!="READY_HUMAN_RATIFIED":
        failures.append("QI_NOT_RATIFIED")
    hp=hp_contract["formulations"][STAGE]["qualities"]["excepcional"]
    qi=qi_contract["formulations"][STAGE]["qualities"]["excepcional"]
    if hp.get("formula")!="7d6+20":
        failures.append("LIV_HP_EXCEPTIONAL_CHANGED")
    if float(qi)!=38.0:
        failures.append("LIV_QI_EXCEPTIONAL_CHANGED")
    use=qi_contract.get("combat_use",{})
    if use.get("consumes_full_action") is not True:
        failures.append("POTION_ACTION_RULE_CHANGED")
    if use.get("no_artificial_potion_cooldown") is not True:
        failures.append("POTION_COOLDOWN_RULE_CHANGED")
    return {"pass":not failures,"failures":failures}

if __name__=="__main__":
    here=Path(__file__).resolve().parent
    hp=_load(here.parent/"balance_nuevo"/"alchemy_consumables_v0.1"/"ALCHEMY_VITALITY_HP_CONTRACT_V0_1.json")
    qi=_load(here.parent/"balance_nuevo"/"alchemy_consumables_v0.1"/"ALCHEMY_QI_RECOVERY_CONTRACT_V0_2.json")
    print(json.dumps(validate_contracts(hp,qi),ensure_ascii=False,indent=2))
