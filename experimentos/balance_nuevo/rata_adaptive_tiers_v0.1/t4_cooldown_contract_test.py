import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
d=json.loads((HERE/"RATA_T4_COOLDOWN_INPUT_V0_1.json").read_text(encoding="utf-8"))
m=d["frozen_mechanics"]
assert m["opening_instance_basic"] is True
assert m["followup_hit_count"]==1
assert m["followup_scalar_per_hit"]==0.5
assert m["followup_dice"]=="2d4"
assert m["precision_rule"]=="INDEPENDENT_PER_HIT"
assert m["critical_rule"]=="INDEPENDENT_PER_HIT"
assert [x["cooldown_rounds"] for x in d["candidates"]]==[3,5,7]
assert d["guards"]["no_other_axis_changes"] is True
print("PASS: T4 Phase C varies cooldown only")
