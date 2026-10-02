from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
P=json.loads((HERE/"ARC1_EQUIPMENT_RUNTIME_BINDING_V0_1.json").read_text(encoding="utf-8"))
assert P["clean_slate"]["no_legacy_stat_bridge"] is True
assert P["clean_slate"]["no_legacy_slot_translation_runtime"] is True
caps=P["slot_capacity"]
assert len(caps)==11
assert caps["ANILLO"]==2 and caps["TESORO_ESPIRITUAL"]==2
assert all(v==1 for k,v in caps.items() if k not in {"ANILLO","TESORO_ESPIRITUAL"})
assert P["recommended_equipped_shape"]["representation"]=="ARRAY_PER_SLOT"
assert "ataque" not in P["stat_aggregation"]["flat_additive"]
assert "daño" not in P["stat_aggregation"]["flat_additive"]
assert P["save"]["recommended_SAVE_SCHEMA_VERSION"]==3
assert P["slice1_dependency"]["item"]=="calzas_sendero_pinos"
assert P["slice1_dependency"]["slot"]=="PIERNAS"
print("PASS: clean-slate equipment runtime binding proposal is internally consistent")
