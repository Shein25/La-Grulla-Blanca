import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
adaptive=json.loads((HERE/"RATA_ADAPTIVE_TIER_CONTRACT_V0_1.json").read_text(encoding="utf-8"))
t3=json.loads((HERE/"RATA_T3_COUNTER_INPUT_V0_1.json").read_text(encoding="utf-8"))

assert adaptive["status"]=="T3_HUMAN_RATIFIED_T4_LAB_ALLOWED"
assert adaptive["t1"]["status"]=="READY_HUMAN_RATIFIED"
assert adaptive["t1"]["ability"]["evasion_bonus"]==40
assert adaptive["t1"]["ability"]["cooldown_rounds"]==5

assert adaptive["t2"]["status"]=="READY_HUMAN_RATIFIED"
assert adaptive["t2"]["candidate"]=="R2_SHORT"
r=adaptive["t2"]["recognition"]
assert r["memory_window"]==2
assert r["repeated_same_category_required"]==2
assert r["count_results"]==["EFECTIVA"]
assert r["preemptive_survival_bonus"]==8

assert adaptive["t3"]["status"]=="READY_HUMAN_RATIFIED"
assert adaptive["t3"]["trigger"]["label"]=="CONFIRMED_PATTERN_REFLEJO_MISS"
assert adaptive["t3"]["damage"]["mode"]=="INSTANCE_BASIC"
assert adaptive["t4"]["status"]=="FULL_CANDIDATE_AWAITING_HUMAN_RATIFICATION"

assert t3["prerequisite"]=="T2_READY_HUMAN_RATIFIED"
assert t3["damage_reference"]=={
    "source":"canonical_t0_basic",
    "expression":"2d4",
    "note":"Trigger semantics are tested before any T3 damage scaling is introduced."
}
assert len(t3["candidate_triggers"])==3
assert {x["label"] for x in t3["candidate_triggers"]}=={
    "RECOGNIZED_REFLEJO_MISS",
    "CONFIRMED_PATTERN_REFLEJO_MISS",
    "CONFIRMED_PATTERN_ONCE_PER_FIGHT",
}
assert t3["guards"]["no_t1_numeric_changes"] is True
assert t3["guards"]["no_t2_numeric_or_memory_changes"] is True
assert t3["guards"]["direct_damage_pipeline_required"] is True
assert t3["guards"]["no_qi_drain"] is True
assert t3["guards"]["no_dot"] is True
assert t3["guards"]["no_control"] is True
assert t3["guards"]["t4_blocked"] is True

for hidden in ("player.root","player.build_id","future RNG","hidden player stats"):
    assert hidden in t3["observable_contract"]["forbidden"]

print("PASS: historical T3 trigger lab input is preserved")
print("PASS: T1-T3 are frozen and T4 awaits human ratification")
