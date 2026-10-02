from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
T=json.loads((HERE/"ARC1_COMMERCE_TRANSACTION_CONTRACT_V0_1.json").read_text(encoding="utf-8"))
U=json.loads((HERE/"ARC1_COMMERCE_CATALOG_UI_V0_1.json").read_text(encoding="utf-8"))

assert T["status"]=="HUMAN_RATIFIED_DESIGN_AUTHORITY__PRE_IMPLEMENTATION"
assert T["principles"]["engine_separate_from_a07"] is True
assert T["principles"]["engine_separate_from_ui"] is True
assert T["principles"]["ui_is_never_authority"] is True
assert set(T["request_contract"]["allowed_types"])=={"BUY","SELL","SERVICE"}

for forbidden in ["price","contributionRequired","requiredPermission","stock","materials","buybackValue","availability","discount","currencyBalance"]:
    assert forbidden in T["request_contract"]["forbidden_client_authority_fields"]

phases=[x["phase"] for x in T["pipeline"]]
assert phases==["EVALUATE","CONFIRM","REVALIDATE","BUILD_DELTA","COMMIT","RECEIPT"]
assert T["atomicity"]["strategy"]=="VALIDATE_ALL_BEFORE_FIRST_MUTATION"
assert T["atomicity"]["ui_double_click_guard"] is True
assert T["atomicity"]["engine_duplicate_guard"] is True

assert T["delta_models"]["SELL"]["rule"].startswith("Merchant BUY is a sink")
assert T["buy_interests"]["universal_buy"] is False
assert T["buy_interests"]["sold_goods_feed_sell_stock"] is False

assert T["delta_models"]["SERVICE"]["example"]["contributionDelta"]==0
assert T["turn_contract"]["slice1"]=={"open":0,"navigate":0,"buy":0,"sell":0,"service":0,"close":0}
assert T["slice1"]["npcId"]=="ning_cai"
assert T["slice1"]["itemId"]=="calzas_sendero_pinos"
assert T["slice1"]["priceStones"]==8

assert U["surface"]=="CATALOG_INSIDE_CURRENT_MUD_STYLE"
assert U["entry"]=="DIALOGUE_OPTION_ONLY"
assert U["catalog"]["no_drag_drop"] is True
assert U["catalog"]["no_cart"] is True
assert U["catalog"]["select_opens_detail"] is True
assert U["service_view"]["contribution_display"]=="Requirement only, never a cost."
assert U["exits"]["return_to_conversation_label"]=="Volver a la conversación"
assert U["exits"]["close_label"]=="Cerrar"
assert U["exits"]["movement_closes_catalog"] is True

print("PASS: commerce transaction contract v0.1")
print("PASS: UI is display-only, engine owns authority")
print("PASS: sold goods are economic sinks by default")
print("PASS: service Contribution is gate-only")
print("PASS: text catalog UI contract v0.1")
