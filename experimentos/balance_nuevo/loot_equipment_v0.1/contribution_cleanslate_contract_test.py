from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
P=json.loads((HERE/"ARC1_CONTRIBUTION_CLEANSLATE_V0_1.json").read_text(encoding="utf-8"))
assert P["status"]=="HUMAN_RATIFIED_DESIGN_AUTHORITY__PRE_IMPLEMENTATION"
assert P["ratification"]["human_approved"] is True
assert P["ratification"]["implementation_authorized"] is False

assert P["target_model"]["sole_authority"]=="player.facciones[factionId].contribucion"
assert P["target_model"]["remove_fields"]==["saldo","gastos"]
assert P["target_model"]["remove_mirrors"]==["player.contribucion"]
assert P["semantics"]["increment_only"] is True
assert P["semantics"]["decrement_forbidden"] is True
assert P["semantics"]["contribution_never_in_transaction_delta"] is True
assert "gastarContribucion()" in P["runtime_api"]["delete"]
assert "cmd_canjear()" in P["runtime_api"]["delete"]
assert P["save_contract"]["SAVE_SCHEMA_VERSION"]==3
assert P["save_contract"]["facciones_version"]==2
assert P["save_contract"]["old_save_support"] is False
assert P["save_contract"]["migration"] is False
assert P["arc1_expected_awards"]["cumulative_after"]=={
    "P":0,"M01":0,"M02":1,"M03":1,"M04":3,"M05":6,"M06":8,"M07":12
}
print("PASS: clean-slate cumulative Contribution proposal is internally consistent")
