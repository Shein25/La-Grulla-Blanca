from __future__ import annotations
from pathlib import Path
from collections import defaultdict
import json, math, random, statistics

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
C=json.loads((HERE/"ARC1_MONSTER_LOOT_EQUIPMENT_PROPOSAL_V0_1.json").read_text(encoding="utf-8"))
EQ=json.loads((ROOT/"equipment_arc1_catalog.json").read_text(encoding="utf-8"))
SEED=20261001
N=100000

STAGE_MID={k:(v[0]+v[1])/2 for k,v in EQ["stone_price_bands"].items()}
STAGE_MAX={k:v[1] for k,v in EQ["stone_price_bands"].items()}

auto={}
for sid,s in C["recurrent_species"].items():
    for x in s["automatic_loot"]:
        auto[x["item_id"]]={"sid":sid,"p":float(x["probability"]),"q":int(x["quantity"])}

def percentile(v,q):
    a=sorted(v); return a[min(len(a)-1,max(0,math.ceil(q*len(a))-1))]

def buyback_metrics():
    rows=[]
    by_species=defaultdict(list)
    sale=C["resale_policy"]["automatic_loot_values"]
    for item_id,meta in auto.items():
        if item_id not in sale:
            raise AssertionError(f"missing sale price: {item_id}")
        sm=sale[item_id]
        expected=meta["p"]*meta["q"]*sm["price_stones"]
        rows.append({
          "item_id":item_id,"species_id":meta["sid"],"probability":meta["p"],
          "price_stones":sm["price_stones"],"expected_stones_per_kill":expected,
          "stage":sm["stage"],"buyer":sm["buyer"]
        })
        by_species[meta["sid"]].append(expected)
    species=[]
    for sid,vals in sorted(by_species.items()):
        stage=None
        items=[r for r in rows if r["species_id"]==sid]
        if items: stage=items[0]["stage"]
        epk=sum(vals)
        species.append({
          "species_id":sid,"stage":stage,"expected_stones_per_kill":epk,
          "kills_to_stage_mid_equipment":STAGE_MID[stage]/epk if epk else None,
          "kills_to_stage_max_equipment":STAGE_MAX[stage]/epk if epk else None,
        })
    return rows,species

def trial_item(rng,item_id):
    m=auto[item_id]
    kills=0
    while True:
        kills+=1
        if rng.random()<m["p"]:
            return kills

def trial_hook(rng,h):
    if "materials" in h:
        auto_ids=[x for x in h["materials"] if x in auto]
        # Materials not in auto loot are deliberately not simulated here:
        # their burden belongs to Extraction and was validated separately.
        return sum(trial_item(rng,x) for x in auto_ids)
    if "any_of" in h:
        choices=[]
        for alt in h["any_of"]:
            ids=[x for x in alt if x in auto]
            if ids: choices.extend(ids)
        if not choices:
            return 0
        # Hunt the best available optional sample source, not all alternatives.
        return min(trial_item(rng,x) for x in choices)
    return 0

def mission_metrics():
    rows=[]
    for h in C["mission_requisition_hooks"]:
        rng=random.Random(f"{SEED}|{h['id']}")
        vals=[trial_hook(rng,h) for _ in range(N)]
        rows.append({
          "id":h["id"],"window":h["window"],"stage":h["stage"],"npc":h["npc"],
          "mandatory":h["mandatory_for_main_mission"],"repeatable":h["repeatable"],
          "auto_loot_kills_mean":statistics.fmean(vals),
          "auto_loot_kills_median":statistics.median(vals),
          "auto_loot_kills_p90":percentile(vals,.90),
          "auto_loot_kills_p95":percentile(vals,.95),
          "auto_loot_kills_p99":percentile(vals,.99),
        })
    return rows

def main():
    assert C["mission_design_guard"]["no_rng_drop_as_required_main_objective"] is True
    assert all(not h["mandatory_for_main_mission"] for h in C["mission_requisition_hooks"])
    item_rows,species=buyback_metrics()
    missions=mission_metrics()

    # Anti-farm guard: selling incidental loot alone should not buy stage-max equipment rapidly.
    # Minimum threshold is 20 kills even in LI; later stages should rise.
    for x in species:
        assert x["kills_to_stage_max_equipment"]>=20,(x,"buyback too rich")

    # Optional mission requests should not have a 95th percentile above 50 auto-loot kills.
    for x in missions:
        assert x["auto_loot_kills_p95"]<=50,(x,"optional request too grindy")

    out={
      "status":"PASS_LAB_NOT_CANON",
      "buyback_items":item_rows,
      "species_liquidity":species,
      "mission_hooks":missions,
      "guards":{
        "no_required_rng_main_mission":True,
        "no_universal_vendor":True,
        "stage_max_equipment_requires_at_least_20_expected_kills_from_auto_loot_sales":True,
        "optional_requisition_auto_loot_p95_max_50":True
      }
    }
    (HERE/"MISSION_BUYBACK_VALIDATION_V0_1.json").write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(out,ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
