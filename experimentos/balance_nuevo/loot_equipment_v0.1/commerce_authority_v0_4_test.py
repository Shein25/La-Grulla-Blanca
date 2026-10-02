from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
P=json.loads((HERE/"ARC1_COMMERCE_AUTHORITY_V0_4.json").read_text(encoding="utf-8"))

assert P["schema_version"]=="arc1-commerce-balance-v0.4"
assert P["status"]=="HUMAN_RATIFIED_DESIGN_AUTHORITY__PRE_IMPLEMENTATION"

H=P["human_decisions_2026_10_02"]
assert H["extraction_authority"]["probabilities"]=={
    "simple":0.60,"normal":0.45,"dificil":0.30,"muy_dificil":0.18
}
assert H["extraction_authority"]["yields_overrides"]["branquia_lunar"]==2
assert H["extraction_authority"]["yields_overrides"]["sedimento_niebla"]==2

assert H["contribution"]["authority"]=="NON_SPENDABLE_CUMULATIVE_GATE"
assert H["contribution"]["deprecate_runtime_spending"] is True
assert H["contribution"]["migration_required"] is False
assert H["legacy_replacement"]["authority"]=="PURGE_LEGACY_NO_COMPATIBILITY"
assert H["legacy_replacement"]["save_compatibility_required"] is False
assert H["legacy_replacement"]["aliases_allowed_in_final_runtime"] is False
assert P["hard_economic_decisions"]["contribution"]=="NON_SPENDABLE_CUMULATIVE_INSTITUTIONAL_ACCESS_GATE"
assert all(x["contribution_spent"] is False for x in P["equipment"])

assert H["legacy_replacement"]["authority"]=="NEW_ARC1_CATALOGS_ONLY"
assert H["legacy_replacement"]["no_silent_coexistence"] is True
assert P["legacy_policy"]["runtime_integration"]=="PURGE_AND_REPLACE"
assert P["legacy_policy"]["save_compatibility_required"] is False
assert P["legacy_policy"]["aliases_in_runtime"]=="FORBIDDEN"

assert H["dialogue_entry"]["authority"]=="DIALOGUE_ONLY"
for cmd in ["comprar <item>","vender <item>","comerciar <npc>"]:
    assert cmd in H["dialogue_entry"]["public_commands_forbidden"]
assert P["a07_boundary"]["no_new_public_commands"] is True

routes={x["equipment_id"]:x for x in P["material_exchange_policy"]["routes"]}
assert routes["bandana_cuero_reforzada"]["contribution_required"]==3
assert routes["amuleto_colmillo_montado"]["full_stone_price"] is None
assert routes["amuleto_colmillo_montado"]["material_only"] is True

am=next(x for x in P["equipment"] if x["item_id"]=="amuleto_colmillo_montado")
assert am["commerce_channel"]=="MATERIAL_SERVICE_ONLY"
assert am["stone_price"] is None

assert P["readiness"]["runtime_implementation"]=="BLOCKED_UNTIL_ASTRA_REQUIRED_CHANGES_RESOLVED"

print("PASS: Arc1 Commerce Authority v0.4")
print("PASS: redesign Extraction authority fixed")
print("PASS: Contribution is non-spendable")
print("PASS: legacy is purged with no compatibility layer")
print("PASS: Commerce entry is dialogue-only")
print("PASS: Astra inconsistencies fixed")
