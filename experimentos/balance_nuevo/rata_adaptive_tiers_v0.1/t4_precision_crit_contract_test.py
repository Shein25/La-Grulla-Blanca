import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
d=json.loads((HERE/"RATA_T4_PRECISION_CRIT_INPUT_V0_1.json").read_text(encoding="utf-8"))
g=d["frozen_geometry"]
assert g["opening_instance_basic"] is True
assert g["followup_hit_count"]==1
assert g["followup_scalar_per_hit"]==0.5
assert g["followup_dice"]=="2d4"
assert g["cooldown_rounds"]==5
assert {x["precision_rule"] for x in d["candidates"]}=={"INDEPENDENT_PER_HIT","FOLLOWUP_REQUIRES_OPENING_HIT"}
assert {x["critical_rule"] for x in d["candidates"]}=={"INDEPENDENT_PER_HIT","OPENING_ONLY"}
assert len(d["candidates"])==4
assert d["guards"]["no_precision_bonus_or_penalty"] is True
assert d["guards"]["no_crit_bonus"] is True
print("PASS: T4 Phase B changes only precision gating and followup critical eligibility")
