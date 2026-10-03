#!/usr/bin/env python3
"""
GRULLA BENCH ENTRYPOINT V0.4

Actual:
- ULTIS_EQUIPMENT

Preparado pero bloqueado:
- TECHNIQUES_EQUIPMENT
- FULL_LOADOUT
"""
from __future__ import annotations
import argparse,json
from pathlib import Path

HERE=Path(__file__).resolve().parent
STAGES=HERE/"GRULLA_BENCH_EXECUTION_STAGES_V0_4.json"
CONSUMABLES=HERE/"GRULLA_CONSUMABLE_BENCH_AUTHORITY_V0_1.json"

MODES=("ULTIS_EQUIPMENT","TECHNIQUES_EQUIPMENT","FULL_LOADOUT")
CONSUMABLE_ARMS=(
 "NONE","HP1_EXCEPTIONAL","HP2_EXCEPTIONAL","HP3_EXCEPTIONAL",
 "HP1_QI1_EXCEPTIONAL","HP2_QI1_EXCEPTIONAL","HP3_QI1_EXCEPTIONAL"
)

def read(path:Path): return json.loads(path.read_text(encoding="utf-8"))

def validate(mode:str,consumable_arm:str)->dict:
    stages=read(STAGES)
    if mode not in MODES: raise RuntimeError("UNKNOWN_MODE")
    cfg=stages["modes"][mode]
    if cfg.get("enabled") is not True:
        raise RuntimeError(f"MODE_BLOCKED:{mode}")
    if consumable_arm not in CONSUMABLE_ARMS:
        raise RuntimeError(f"UNKNOWN_CONSUMABLE_ARM:{consumable_arm}")
    c=read(CONSUMABLES)
    if c["hp_contract"]["status"]!="READY_HUMAN_RATIFIED":
        raise RuntimeError("HP_CONSUMABLE_AUTHORITY_NOT_RATIFIED")
    if c["qi_contract"]["status"]!="READY_HUMAN_RATIFIED":
        raise RuntimeError("QI_CONSUMABLE_AUTHORITY_NOT_RATIFIED")
    return {
      "pass":True,"mode":mode,"consumable_arm":consumable_arm,
      "consumable_quantity_is_canon":False if consumable_arm!="NONE" else None,
      "techniques_enabled":cfg["normal_techniques_enabled"],
      "ultimates_enabled":cfg["ultimates_enabled"],
      "equipment_enabled":cfg["equipment_enabled"]
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--mode",choices=MODES,default="ULTIS_EQUIPMENT")
    p.add_argument("--consumable-arm",choices=CONSUMABLE_ARMS,default="NONE")
    p.add_argument("--check-only",action="store_true")
    a=p.parse_args()
    try: out=validate(a.mode,a.consumable_arm)
    except RuntimeError as e:
        print(json.dumps({"pass":False,"error":str(e)},indent=2));return 2
    print(json.dumps(out,ensure_ascii=False,indent=2))
    if a.check_only:return 0
    raise RuntimeError("COMBAT_EXECUTION_NOT_WIRED_YET")
if __name__=="__main__":raise SystemExit(main())
