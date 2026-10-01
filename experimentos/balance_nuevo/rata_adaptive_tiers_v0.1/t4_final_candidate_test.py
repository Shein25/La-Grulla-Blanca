import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
d=json.loads((HERE/"RATA_T4_FINAL_CANDIDATE_V0_1.json").read_text(encoding="utf-8"))

assert d["status"]=="T4_FULL_CANDIDATE_AWAITING_HUMAN_RATIFICATION"
assert d["name"]=="Mordisco Frenético"
assert d["activation"]["rule"]=="REPLACE_BASIC_WHEN_READY"
assert d["activation"]["effective_tier_required"]=="T4"
assert d["activation"]["decay_below_t4_disables"] is True
assert d["activation"]["respects_skip_next_action"] is True
assert d["activation"]["never_displaces_survival_choice"] is True

assert d["packets"][0]["damage_source"]=="INSTANCE_BASIC"
assert d["packets"][0]["scalar"]==1.0
assert d["packets"][1]["damage_source"]=="CANONICAL_T0_BASIC_2D4"
assert d["packets"][1]["scalar"]==0.5
assert all(x["precision_rule"]=="INDEPENDENT_ROLL" for x in d["packets"])
assert all(x["critical_rule"]=="NORMAL_INDEPENDENT_CRIT" for x in d["packets"])
assert d["cooldown_rounds"]==5
assert d["damage_pipeline"]["flat_defense_per_packet"] is True
assert d["damage_pipeline"]["absorption_per_packet"] is True
assert d["human_ratification_required"] is True
assert d["canonical_write"] is False
assert "T5" in d["forbidden"]
assert d["final_validation"]["fights"]==125000
assert d["final_validation"]["conclusion"]=="success"
assert d["final_validation"]["tier_above_t4_executed"] is False
print("PASS: complete T4 candidate is validated and awaiting human ratification")
