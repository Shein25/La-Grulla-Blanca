import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
hp=json.loads((HERE/"ALCHEMY_VITALITY_HP_CONTRACT_V0_1.json").read_text(encoding="utf-8"))
qi=json.loads((HERE/"ALCHEMY_QI_RECOVERY_PROPOSAL_V0_1.json").read_text(encoding="utf-8"))
eco=json.loads((HERE/"ALCHEMY_RECIPE_ECONOMY_PROPOSAL_V0_1.json").read_text(encoding="utf-8"))

assert hp["status"]=="READY_HUMAN_RATIFIED"
assert qi["status"]=="NUMERIC_PROPOSAL_AWAITING_HUMAN_REVIEW"
assert eco["status"]=="STRUCTURAL_PROPOSAL_AWAITING_HUMAN_REVIEW"

pools=qi["player_base_qi"]
for stage,data in qi["pure_qi_formulations"].items():
    vals=list(data["quality"].values())
    assert vals==sorted(vals)
    assert vals[-1] < pools[stage]

assert qi["pure_qi_formulations"]["LianQi_I"]["quality"]["excepcional"]==20
assert qi["pure_qi_formulations"]["LianQi_II"]["quality"]["superior"]==20
assert qi["pure_qi_formulations"]["LianQi_III"]["quality"]["excepcional"] > qi["pure_qi_formulations"]["LianQi_IV"]["quality"]["superior"]

for recipe in eco["vitality_progression"]:
    assert recipe["base_material_units_per_attempt"]<=4
    assert recipe["valid_crafts_to_exceptional_ceiling"] in (2,3,6)
assert eco["guards"]["no_unique_material_for_core_mastery"] is True
print("PASS: HP contract frozen; Qi/economy proposals respect progression guards")
