import json,re
from pathlib import Path

HERE=Path(__file__).resolve().parent
d=json.loads((HERE/"ALCHEMY_VITALITY_HP_CONTRACT_V0_1.json").read_text(encoding="utf-8"))

assert d["status"]=="READY_HUMAN_RATIFIED"
assert d["guards"]["hp_healing_numbers_frozen"] is True
assert d["guards"]["qi_recovery_not_ratified_here"] is True
assert d["guards"]["runtime_write"] is False

def stats(expr):
    m=re.fullmatch(r"(\d+)d(\d+)\+(\d+)",expr)
    assert m,expr
    n,s,b=map(int,m.groups())
    return n+b, n*(s+1)/2+b, n*s+b

rows=[d["common_potion"]]
for stage in d["formulations"].values():
    rows.extend(stage["qualities"].values())

assert len(rows)==17
for x in rows:
    mn,mean,mx=stats(x["formula"])
    assert mn==x["min"],x
    assert abs(mean-x["mean"])<1e-9,x
    assert mx==x["max"],x

assert d["formulations"]["LianQi_III"]["qualities"]["excepcional"]["mean"]==33.0
assert d["formulations"]["LianQi_IV"]["qualities"]["impura"]["mean"]==22.5
assert d["formulations"]["LianQi_IV"]["qualities"]["estable"]["mean"]==29.5
assert d["formulations"]["LianQi_IV"]["qualities"]["superior"]["mean"]==37.0

print("PASS: 17 ratified HP-healing formulas and their min/mean/max values are exact")
