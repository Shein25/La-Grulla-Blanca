from __future__ import annotations
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
P=json.loads((HERE/"SIX_REPEATABLE_VARIANCE_ENVELOPE_PROPOSAL_V0_1.json").read_text(encoding="utf-8"))
R=json.loads((HERE.parent/"monster_arc1_registry.json").read_text(encoding="utf-8"))

IDS=["sapo_ceniza","escarabajo_hierro","pez_lunar","anguila_estelar","devorador_niebla","halcon_tormenta"]
assert P["status"]=="LAB_PROPOSAL_AWAITING_CROSS_AXIS_VALIDATION"
assert P["scope"]["exclude_unique_true"] is True
assert P["derivation_rules"]["unique_species_variance_forbidden"] is True
assert set(P["scope"]["include"])==set(IDS)
assert all(R["profiles"][sid]["unique"] is False for sid in IDS)
assert all(R["profiles"][sid]["stats_status"]=="READY" for sid in IDS)
assert all(R["profiles"][sid]["adaptive"]["status"]=="ADAPTIVE_CHAIN_T0_T4_CLOSED" for sid in IDS)

for sid in IDS:
    s=P["species"][sid]
    reg=R["profiles"][sid]
    for k in ("hp","defense","evasion","precision","tenacity"):
        assert s["base"][k]==reg["stats"][k],(sid,k,"base != T0")
        assert s["upper_envelope"][k]>=s["base"][k],(sid,k,"upper below T0")
    assert s["attacks"]["basic_damage"]["ladder"][0]==reg["stats"]["basic_damage"],sid
    assert s["fixed_technique"]["name"]==reg["technique"]["name"],sid
    assert s["fixed_technique"]["cadence"]==reg["technique"]["params"]["cadence"],sid
    if "qi_drain" in s["fixed_technique"]:
        assert s["fixed_technique"]["qi_drain"]==reg["technique"]["params"]["qi_drain"],sid

assert P["species"]["anguila_estelar"]["upper_envelope"]["hp"]==P["species"]["anguila_estelar"]["base"]["hp"]
assert P["species"]["anguila_estelar"]["upper_envelope"]["tenacity"]==P["species"]["anguila_estelar"]["base"]["tenacity"]
assert P["mutant_policy_inherited"]["maximum_incidence"]==0.01
assert P["mutant_policy_inherited"]["loot_multiplier"]==1.5
assert P["mutant_policy_inherited"]["xp_multiplier"]==1.5
assert P["next_gate"]["t1_t4_interaction_validation"] is True

print("PASS: six repeatable variance envelope proposal is T0-floored and identity-safe")
print("PASS: unique:true species are explicitly excluded")
print("PASS: proposal remains LAB-only pending cross-axis and adaptive validation")
