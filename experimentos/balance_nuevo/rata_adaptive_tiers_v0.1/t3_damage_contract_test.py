import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
d=json.loads((HERE/"RATA_T3_DAMAGE_INPUT_V0_1.json").read_text(encoding="utf-8"))

assert d["frozen_t3_trigger"]["label"]=="CONFIRMED_PATTERN_REFLEJO_MISS"
assert d["frozen_t3_trigger"]["requires_prediction_confirmed"] is True
assert d["frozen_t1"]["evasion_bonus"]==40
assert d["frozen_t1"]["cooldown_rounds"]==5
assert d["frozen_t2"]=={
    "candidate":"R2_SHORT",
    "memory_window":2,
    "repeated_same_category_required":2,
    "count_results":["EFECTIVA"],
    "preemptive_survival_bonus":8,
}
assert [x["label"] for x in d["damage_candidates"]]==[
    "FIXED_CANONICAL_2D4",
    "INSTANCE_BASIC",
    "FIXED_MEASURED_HIGH_2D4_PLUS_2",
]
instance=d["damage_candidates"][1]
assert instance["measured_expressions"]==["2d4","2d4+1","2d3+3","2d4+2"]
assert instance["measured_sources"]==[4254,251,192,240]
assert d["damage_candidates"][2]["counter_damage_expression"]=="2d4+2"
assert d["guards"]["measured_damage_sources_only"] is True
assert d["guards"]["t4_blocked"] is True
print("PASS: T3 damage candidates use only measured Rata offense")
