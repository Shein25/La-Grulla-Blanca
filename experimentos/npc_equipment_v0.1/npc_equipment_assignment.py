"""NPC equipment assignment v0.2.

Gated assignment layer:
- never duplicates unique player items;
- never infers that a seller/source wears an item;
- senior authorities require bespoke NPC-owned gear;
- companions require an authorized personal combat/equipment archetype;
- civil/admin/logistics roles do not receive combat gear by occupational guess;
- only role-grounded actors may receive catalog-backed candidate loadouts.
Item stats remain outside NPC combat until a separate NPC combat-stat contract.
"""
from __future__ import annotations
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
CATALOG=ROOT/"experimentos"/"balance_nuevo"/"equipment_arc1_catalog.json"
STAGE_INDEX={"LianQi_I":1,"LianQi_II":2,"LianQi_III":3,"LianQi_IV":4}
AUTO_MODE="AUTO_CATALOG_ROLE_GUIDED"

def load_json(path):return json.loads(Path(path).read_text(encoding="utf-8"))

def catalog_items(catalog):
    raw=catalog["items"]
    if isinstance(raw,dict):return list(raw.values())
    if isinstance(raw,list):return raw
    raise TypeError("equipment catalog items must be list or dict")

def eligible_items(actor,catalog,stage,policy):
    stage_policy=policy["auto_catalog_stage_policy"]
    if STAGE_INDEX[stage]<STAGE_INDEX[stage_policy["first_story_stage"]]:
        return []
    allowed=set(policy["family_allowed_slots"].get(actor["equipment_family"],[]))
    return [
        x for x in catalog_items(catalog)
        if not x["unique"]
        and x["min_stage"]==stage
        and x["availability"]!="ORIGIN_ONLY"
        and x["source_type"]!="STARTING_ISSUE"
        and x["slot"] in allowed
    ]

def score(item,preferences):
    weights={tag:(len(preferences)-i)*10 for i,tag in enumerate(preferences)}
    return sum(weights.get(tag,0) for tag in item.get("build_tags",[]))+min(5.0,float(item.get("power_budget",0)))

def assign(actor,stage,catalog,policy):
    if actor["assignment_mode"]!=AUTO_MODE:return []
    prefs=policy["family_preferences"][actor["equipment_family"]]
    cap=policy["group_item_caps"][actor["a079_group"]][stage]
    slots=policy["slot_caps"]
    ranked=sorted(eligible_items(actor,catalog,stage,policy),key=lambda x:(-score(x,prefs),x["item_id"]))
    used={};selected=[]
    for item in ranked:
        slot=item["slot"]
        if used.get(slot,0)>=slots.get(slot,0):continue
        selected.append(item["item_id"]);used[slot]=used.get(slot,0)+1
        if len(selected)>=cap:break
    return selected

def validate(result,actors,catalog,policy):
    assert len(actors)==32
    item_by_id={x["item_id"]:x for x in catalog_items(catalog)}
    modes=set(policy["assignment_modes"])
    for actor in actors:
        assert actor["assignment_mode"] in modes
        out=result["actors"][actor["actor_id"]]
        assert out["assignment_mode"]==actor["assignment_mode"]
        if actor["assignment_mode"]!="AUTO_CATALOG_ROLE_GUIDED":
            assert all(not ids for ids in out["by_story_stage"].values()),actor["actor_id"]
        for stage,item_ids in out["by_story_stage"].items():
            used={}
            for item_id in item_ids:
                item=item_by_id[item_id]
                assert not item["unique"],(actor["actor_id"],item_id,"unique")
                assert item["min_stage"]==stage
                assert item["slot"] in policy["family_allowed_slots"][actor["equipment_family"]]
                slot=item["slot"];used[slot]=used.get(slot,0)+1
                assert used[slot]<=policy["slot_caps"][slot]
    return True

def build():
    actors=load_json(HERE/"npc_equipment_actor_registry.json")["actors"]
    policy=load_json(HERE/"npc_equipment_policy.json")
    catalog=load_json(CATALOG)
    result={
        "schema_version":"npc-equipment-assignments-v0.2",
        "status":"LAB_PROPOSAL_GATED_NOT_CANON",
        "rules":{
            "unique_items_excluded":True,
            "source_npc_does_not_imply_worn":True,
            "combat_stats_applied":False,
            "story_stage_gate":True,
            "senior_authorities_not_auto_dressed":True,
            "companions_not_auto_specialized":True,
            "auto_catalog_first_stage":"LianQi_II",
            "auto_catalog_exact_stage_only":True,
        },
        "actors":{}
    }
    for actor in actors:
        result["actors"][actor["actor_id"]]={
            "display_name":actor["display_name"],"role":actor["role"],
            "a079_group":actor["a079_group"],"equipment_family":actor["equipment_family"],
            "assignment_mode":actor["assignment_mode"],"assignment_reason":actor["assignment_reason"],
            "by_story_stage":{s:assign(actor,s,catalog,policy) for s in STAGE_INDEX},
        }
    validate(result,actors,catalog,policy)
    return result

if __name__=="__main__":
    result=build()
    out=HERE/"npc_equipment_assignments_proposal.generated.json"
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    counts={}
    for x in result["actors"].values():counts[x["assignment_mode"]]=counts.get(x["assignment_mode"],0)+1
    print(f"PASS: 32/32 NPC equipment states -> {out}")
    print(json.dumps(counts,ensure_ascii=False,sort_keys=True))
