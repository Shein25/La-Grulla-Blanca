from __future__ import annotations
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
P=json.loads((HERE/"ARC1_COMMERCE_BALANCE_V0_2.json").read_text(encoding="utf-8"))
EQ=json.loads((ROOT/"equipment_arc1_catalog.json").read_text(encoding="utf-8"))

BANDS={
 "LianQi_I":(2,4),
 "LianQi_II":(7,12),
 "LianQi_III":(16,22),
 "LianQi_IV":(24,30),
}
CUM=P["contribution_working_curve"]["cumulative_by_mission"]
BY_ID={x["item_id"]:x for x in EQ["items"]}

assert P["hard_economic_decisions"]["currency"]=="SPIRIT_STONES"
assert P["hard_economic_decisions"]["contribution"]=="NON_SPENDABLE_CUMULATIVE_INSTITUTIONAL_ACCESS_GATE"
assert P["guards"]["contribution_never_decremented"] is True
assert P["a07_boundary"]["freeAiText"] is False
assert len(P["equipment"])==68
assert len({x["item_id"] for x in P["equipment"]})==68

counts={}
for x in P["equipment"]:
    src=BY_ID[x["item_id"]]
    ch=x["commerce_channel"]
    counts[ch]=counts.get(ch,0)+1
    assert x["contribution_spent"] is False
    if ch=="NO_SALE":
        assert x["stone_price"] is None
        assert x["contribution_required"]==0
    elif ch.startswith("PUBLIC_"):
        assert isinstance(x["stone_price"],int) and x["stone_price"]>0,(x["item_id"],x["stone_price"])
        assert x["contribution_required"]==0
    elif ch=="INSTITUTIONAL_STONES_GATE":
        assert isinstance(x["stone_price"],int) and x["stone_price"]>0,(x["item_id"],x["stone_price"])
        assert x["contribution_required"]==CUM[src["source_mission"]],(x["item_id"],x["contribution_required"],src["source_mission"])
        lo,hi=BANDS[x["stage"]]
        assert lo<=x["stone_price"]<=hi,(x["item_id"],x["stone_price"],(lo,hi))
        assert src["required_permission"] is not None or src["accessibility"]=="INSTITUCIONAL"

# Hard public/institutional semantic examples.
for iid in ["sable_anillo_gris","vestidura_flujo_ligero","calzas_trama_sello"]:
    assert next(x for x in P["equipment"] if x["item_id"]==iid)["commerce_channel"]=="INSTITUTIONAL_STONES_GATE"
for iid in ["capucha_observador_valle","botas_piedra_humeda","anillo_corriente_clara","anillo_reserva_menor","calzas_paso_silencioso"]:
    assert next(x for x in P["equipment"] if x["item_id"]==iid)["commerce_channel"]=="PUBLIC_OPEN_STONES"
for iid in ["tunica_ruta_sauces","sandalias_corriente_ligera","amuleto_sauce_sereno","pulsera_cauce_trenzado"]:
    assert next(x for x in P["equipment"] if x["item_id"]==iid)["commerce_channel"]=="PUBLIC_CONTEXTUAL_STONES"

# Mission/origin/exploration/treasure outputs remain non-commercial.
for x in P["equipment"]:
    src=BY_ID[x["item_id"]]
    if src["source_type"] in {"STARTING_ISSUE","ORIGIN_START","MISSION_REWARD","EXPLORATION_UNIQUE"}:
        assert x["commerce_channel"]=="NO_SALE",(x["item_id"],src["source_type"])

# Non-equipment economy hard guards.
n=P["non_equipment_balance"]
assert n["consumables"]["routine_public"][0]["price_stones"]==5
assert "Superior/Exceptional crafted qualities" in n["consumables"]["craft_primary_not_routine_unlimited"]
assert n["materials"]["extraction_and_herboristery"]["universal_resale"] is False
assert n["mission_and_unique_objects"]["commerce"]=="NO_SALE"

print("PASS: 68/68 equipment items classified")
print("PASS: Contribution is access-only and never spent")
print("PASS: permission-aware public/institutional split")
print("PASS: institutional stone prices stay inside stage bands")
print("PASS: mission/origin/exploration uniques remain non-commercial")
print("COUNTS",json.dumps(counts,sort_keys=True))
