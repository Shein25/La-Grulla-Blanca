from __future__ import annotations
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
CONTRACT=json.loads((HERE/"MONSTER_ADAPTIVE_SIX_CONTRACT_V0_1.json").read_text(encoding="utf-8"))
REG=json.loads((ROOT/"monster_arc1_registry.json").read_text(encoding="utf-8"))

IDS=["sapo_ceniza","escarabajo_hierro","pez_lunar","anguila_estelar","devorador_niebla","halcon_tormenta"]

assert CONTRACT["status"]=="ADAPTIVE_CHAINS_T0_T4_HUMAN_RATIFIED_CLOSED"
assert CONTRACT["guards"]["no_t5"] is True
assert CONTRACT["guards"]["rata_chain_unchanged"] is True
assert CONTRACT["methodology"]["target_win_rate_objective"] is False
assert CONTRACT["methodology"]["paired_t0_relative_review"] is True

assert set(IDS).issubset(set(REG["rules"]["ready_profiles"]))

for sid in IDS:
    c=CONTRACT["species"][sid]
    p=REG["profiles"][sid]
    assert p["unique"] is False
    assert p["stats_status"]=="READY"
    assert p["stats"]==c["t0"]["stats"]
    assert p["technique"]["params_status"]=="READY"
    assert p["technique"]["params"]==c["t0"]["technique"]["params"]
    assert p["technique"]["name"]==c["t0"]["technique"]["name"]
    assert p["technique"]["mechanics"]==c["t0"]["technique"]["mechanics"]
    assert p["adaptive"]["status"]=="ADAPTIVE_CHAIN_T0_T4_CLOSED"
    for tier in ("t0","t1","t2","t3","t4"):
        assert c[tier]["status"] in {"READY_HUMAN_RATIFIED","ADAPTIVE_CHAIN_T0_T4_CLOSED"}
    assert c["t2"]["memory_window"]==2
    assert c["t2"]["repeated_same_category_required"]==2
    assert c["t2"]["count_results"]==["EFECTIVA"]
    assert c["t3"]["damage"]["mode"]=="INSTANCE_T0_BASIC"
    assert c["t4"]["numeric_buff"] is False
    assert c["t4"]["guards"]["no_t5"] is True

assert CONTRACT["species"]["sapo_ceniza"]["t1"]["ability"]=={
    "kind":"MITIGATE_NEXT","damage_reduction_pct":10,"cooldown_rounds":5
}
assert CONTRACT["species"]["sapo_ceniza"]["t4"]["cooldown_rounds"]==12
assert CONTRACT["species"]["escarabajo_hierro"]["t1"]["ability"]=={
    "kind":"DEFENSE_UP","defense_bonus":2,"cooldown_rounds":5
}
assert CONTRACT["species"]["escarabajo_hierro"]["t4"]["cooldown_rounds"]==8

for sid,bonus in {
    "pez_lunar":20,
    "anguila_estelar":35,
    "devorador_niebla":20,
    "halcon_tormenta":35,
}.items():
    assert CONTRACT["species"][sid]["t1"]["ability"]=={
        "kind":"EVADE_NEXT","evasion_bonus":bonus,"cooldown_rounds":5
    }
    assert CONTRACT["species"][sid]["t4"]["cooldown_rounds"]==5

print("PASS: six repeatable monster T0-T4 chains are human-ratified and frozen")
print("PASS: paired-T0 adaptive review rule is frozen")
print("PASS: no T5; unique encounters excluded; Rata untouched")
