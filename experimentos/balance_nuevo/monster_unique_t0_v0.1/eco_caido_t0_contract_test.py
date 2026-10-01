from __future__ import annotations
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
C=json.loads((HERE/"ECO_CAIDO_T0_CONTRACT_V0_1.json").read_text(encoding="utf-8"))
R=json.loads((ROOT/"monster_arc1_registry.json").read_text(encoding="utf-8"))

assert C["status"]=="ECO_CAIDO_T0_HUMAN_RATIFIED_CLOSED"
e=C["species"]["eco_caido"]
p=R["profiles"]["eco_caido"]

assert e["unique"] is True
assert e["adaptive_tiers_allowed"] is False
assert p["unique"] is True
assert p["stats_status"]=="READY"
assert p["stats"]==e["t0"]["stats"]
assert p["technique"] is None
assert p["adaptive"]["status"]=="UNIQUE_T0_CLOSED_NO_T1_T4"

m=C["strict_1v1_policy_gate"]
assert m["status"]=="HUMAN_RATIFIED_METHOD_RULE"
assert m["observed_engine_scalar"]==0.65
assert m["hard_policy_gate"]==["VETERAN","UNITARGET_FIRST","DEFENSE_OPEN"]
assert m["diagnostic_stress_only"]==["ROTATION","AOE_FIRST"]
assert m["no_target_win_rate"] is True

assert C["guards"]["no_t1_t4_for_unique"] is True
assert C["guards"]["no_t5"] is True

print("PASS: Eco del Caido T0 is human-ratified and frozen")
print("PASS: unique encounter has no persistent T1-T4")
print("PASS: strict-1v1 AOE_FIRST diagnostic-only rule is frozen")
