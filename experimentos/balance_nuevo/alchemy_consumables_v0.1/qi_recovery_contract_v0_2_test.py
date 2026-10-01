from __future__ import annotations
import json
from pathlib import Path
P=Path(__file__).resolve().parent/"ALCHEMY_QI_RECOVERY_CONTRACT_V0_2.json"
d=json.loads(P.read_text(encoding="utf-8"))
assert d["status"]=="READY_HUMAN_RATIFIED"
assert d["player_base_qi"]=={"LianQi_I":37,"LianQi_II":43,"LianQi_III":49,"LianQi_IV":55}
assert d["formulations"]["LianQi_I"]["qualities"]=={"impura":8,"estable":12,"superior":16,"excepcional":20}
assert d["formulations"]["LianQi_II"]["qualities"]=={"impura":20,"estable":22,"superior":24,"excepcional":26}
assert d["formulations"]["LianQi_III"]["qualities"]=={"impura":26,"estable":28,"superior":30,"excepcional":32}
assert d["formulations"]["LianQi_IV"]["qualities"]=={"impura":32,"estable":34,"superior":36,"excepcional":38}
assert d["combat_use"]["consumes_full_action"] is True
assert d["combat_use"]["cap_at_qi_max"] is True
assert d["combat_use"]["no_artificial_potion_cooldown"] is True
print("PASS: ratified pure-Qi recovery curve v0.2")
