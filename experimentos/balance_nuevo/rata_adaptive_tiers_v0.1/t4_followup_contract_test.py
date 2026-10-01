import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
d=json.loads((HERE/"RATA_T4_MORDISCO_FOLLOWUP_INPUT_V0_1.json").read_text(encoding="utf-8"))
assert d["model"]=="INSTANCE_BASIC_OPENING_PLUS_CANONICAL_2D4_FOLLOWUPS"
assert d["fixed_axes"]["followup_dice"]=="2d4"
assert d["fixed_axes"]["cooldown_rounds"]==5
assert [x["label"] for x in d["candidates"]]==[
    "FOLLOWUP_1X025","FOLLOWUP_1X050","FOLLOWUP_2X025","FOLLOWUP_1X075"
]
for x in d["candidates"]:
    assert x["opening_instance_basic"] is True
assert d["candidates"][1]["extra_raw_expected_multiplier_vs_canonical"]==d["candidates"][2]["extra_raw_expected_multiplier_vs_canonical"]==0.5
assert d["guards"]["t1_t3_frozen"] is True
assert d["guards"]["followups_use_canonical_2d4"] is True
print("PASS: T4 Phase A2 preserves individual opening and canonical followups")
