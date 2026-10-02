from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
P=json.loads((HERE/"ARC1_COMMERCE_SLICE1_A07_PREFLIGHT_V0_1.json").read_text(encoding="utf-8"))

assert P["status"]=="HUMAN_RATIFIED_DESIGN_AUTHORITY__PRE_IMPLEMENTATION"
assert P["ratification"]["human_approved"] is True
assert P["ratification"]["implementation_authorized"] is False

A=P["fixed_authorities"]["a07"]
assert A["interaction_terminal"] is True
assert A["freeAiText"] is False

M=P["fixed_authorities"]["merchant"]
assert M["actorId"]=="ning_cai"
assert M["room"]=="taller_ning_cai"
assert M["mobility"]=="ANCLADO"
assert set(M["capabilities"])=={"SELL","FULFILL"}

O=P["fixed_authorities"]["offer"]
assert O["itemId"]=="calzas_sendero_pinos"
assert O["priceStones"]==8
assert O["contributionRequired"]==0
assert O["sourceMission"]=="M04"
assert O["slot"]=="PIERNAS"
assert O["stats"]=={"hp_max":3,"evasion":1}

D=P["integration_shape"]["domain_option"]
assert D["counted_as_a07_authored_entry"] is False
assert D["creates_a07_intent"] is False
assert D["creates_npc_utterance"] is False

assert P["recommended_availability"]["status"]=="RATIFIED"
assert P["recommended_availability"]["sourceMission"]=="M04"
assert P["hp_current_semantics"]["status"]=="RATIFIED"
assert "do not increase current HP" in P["hp_current_semantics"]["equip"]
assert "min(current HP, new max HP)" in P["hp_current_semantics"]["unequip"]

assert P["persistence_boundary"]["save_schema"]==3
assert P["equipment_dependency"]["slot"]=="PIERNAS"
assert P["equipment_dependency"]["item_effects"]=={"hp_max":3,"evasion":1}

print("PASS: Ning Cai Slice 1 A07 preflight is ratified and internally consistent")
