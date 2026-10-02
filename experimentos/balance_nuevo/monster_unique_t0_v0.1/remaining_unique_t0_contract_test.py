from __future__ import annotations
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
C=json.loads((HERE/"REMAINING_UNIQUE_T0_CONTRACT_V0_1.json").read_text(encoding="utf-8"))
R=json.loads((ROOT/"monster_arc1_registry.json").read_text(encoding="utf-8"))
IDS=["sapo_caldera","rey_escarabajo","sombra_ahogada","guardian_coral","mantis_nube","centinela_pluma"]
assert C["status"]=="ALL_REMAINING_UNIQUE_T0_HUMAN_RATIFIED_CLOSED"
for sid in IDS:
    c=C["species"][sid]
    p=R["profiles"][sid]
    assert c["unique"] is True
    assert p["unique"] is True
    assert p["stats_status"]=="READY"
    assert p["stats"]==c["stats"]
    assert p["adaptive"]["status"]=="UNIQUE_T0_CLOSED_NO_T1_T4"
    assert p["technique"]["params_status"]=="READY"
    assert p["technique"]["name"]==c["technique"]["name"]
    assert p["technique"]["mechanics"]==c["technique"]["mechanics"]
    assert p["technique"]["params"]==c["technique"]["params"]
assert C["evidence"]["boss_consumable_quality_stress"]["fights"]==126000
assert C["evidence"]["boss_consumable_quantity_stress"]["fights"]==54000
assert C["guards"]["unique_species_have_no_persistent_t1_t4"] is True
assert C["guards"]["target_win_rate_objective_used"] is False
print("PASS: remaining six unique T0 profiles are human-ratified and frozen")
print("PASS: five bosses retain consumable-preparation stress evidence")
print("PASS: unique encounters have no persistent T1-T4")
