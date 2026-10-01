import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
a=json.loads((HERE/"RATA_ADAPTIVE_TIER_CONTRACT_V0_1.json").read_text(encoding="utf-8"))
d=json.loads((HERE/"RATA_T4_MORDISCO_INPUT_V0_1.json").read_text(encoding="utf-8"))

assert a["status"]=="ADAPTIVE_CHAIN_T0_T4_HUMAN_RATIFIED_CLOSED"
assert a["t3"]["status"]=="READY_HUMAN_RATIFIED"
assert a["t3"]["trigger"]["label"]=="CONFIRMED_PATTERN_REFLEJO_MISS"
assert a["t3"]["damage"]["mode"]=="INSTANCE_BASIC"
assert a["t4"]["status"]=="READY_HUMAN_RATIFIED"
assert a["t4"]["identity"]=="MORDISCO_FRENETICO"

assert d["identity"]["source_damage"]=="canonical T0 basic 2d4"
assert d["identity"]["activation_rule"]=="REPLACE_BASIC_WHEN_READY"
f=d["phase_a_geometry"]["fixed_axes"]
assert f["precision_rule"]=="INDEPENDENT_PER_HIT"
assert f["critical_rule"]=="INDEPENDENT_PER_HIT"
assert f["cooldown_rounds"]==5
assert f["dice"]=="2d4"
assert f["direct_pipeline_per_hit"] is True
assert [x["label"] for x in d["phase_a_geometry"]["candidates"]]==[
    "CONTROL_1X100","FRENZY_2X050","FRENZY_2X075","FRENZY_3X050"
]
assert d["guards"]["t1_t3_frozen"] is True
assert d["guards"]["flat_def_per_hit"] is True
assert d["guards"]["absorption_per_hit"] is True
assert d["guards"]["no_tier_above_t4"] is True
print("PASS: Rata T4 Phase A isolates Mordisco Frenetico multi-hit geometry")
