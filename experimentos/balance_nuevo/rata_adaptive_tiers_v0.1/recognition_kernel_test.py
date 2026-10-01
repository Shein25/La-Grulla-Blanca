import json
from pathlib import Path
from recognition_kernel import classify_player_action,observe,recognize_recent_pattern

HERE=Path(__file__).resolve().parent
cfg=json.loads((HERE/"RATA_T2_RECOGNITION_INPUT_V0_1.json").read_text(encoding="utf-8"))
cands={c["label"]:c for c in cfg["candidates"]}

assert classify_player_action(None,basic=True)=="PLAYER_BASIC"
assert classify_player_action({"role":"DEFENSIVE","targeting":"SELF"})=="PLAYER_DEFENSIVE_TECHNIQUE"
assert classify_player_action({"role":"OFFENSIVE","targeting":"AOE"})=="PLAYER_AOE_TECHNIQUE"
assert classify_player_action({"role":"OFFENSIVE","targeting":"UNITARGET"})=="PLAYER_UNITARGET_TECHNIQUE"

m=[
 observe("PLAYER_UNITARGET_TECHNIQUE","EFECTIVA"),
 observe("PLAYER_UNITARGET_TECHNIQUE","EFECTIVA"),
]
assert recognize_recent_pattern(m,cands["R2_SHORT"])["recognized"] is True
assert recognize_recent_pattern(m,cands["R2_CENTRAL"])["recognized"] is True
assert recognize_recent_pattern(m,cands["R3_CONSERVATIVE"])["recognized"] is False

m3=m+[observe("PLAYER_UNITARGET_TECHNIQUE","EFECTIVA")]
assert recognize_recent_pattern(m3,cands["R3_CONSERVATIVE"])["recognized"] is True

mixed=[
 observe("PLAYER_BASIC","EFECTIVA"),
 observe("PLAYER_UNITARGET_TECHNIQUE","EFECTIVA"),
 observe("PLAYER_BASIC","EFECTIVA"),
]
assert recognize_recent_pattern(mixed,cands["R2_CENTRAL"])["recognized"] is False

failed=[
 observe("PLAYER_BASIC","FALLIDA"),
 observe("PLAYER_BASIC","FALLIDA"),
 observe("PLAYER_BASIC","FALLIDA"),
]
for c in cands.values():
    assert recognize_recent_pattern(failed,c)["recognized"] is False

# Hidden fields cannot affect the pure recognizer because they are not read.
polluted=[
 {"category":"PLAYER_BASIC","result":"EFECTIVA","player.root":"fuego","player.build_id":"secret"},
 {"category":"PLAYER_BASIC","result":"EFECTIVA","future_rng":0.99},
]
assert recognize_recent_pattern(polluted,cands["R2_SHORT"])["recognized"] is True

print("PASS: T2 recognizer uses observable repeated action categories only")
print("PASS: T1 numbers are not present in or mutable by recognition kernel")
