"""NPC equipment assignment v0.1.

Uses the player equipment catalog as an allowed-item vocabulary, but never
duplicates unique player items and never applies item stats to NPC combat.
"""
from __future__ import annotations
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
CATALOG=ROOT/"experimentos"/"balance_nuevo"/"equipment_arc1_catalog.json"

STAGE_INDEX={"LianQi_I":1,"LianQi_II":2,"LianQi_III":3,"LianQi_IV":4}

def load_json(path):return json.loads(Path(path).read_text(encoding="utf-8"))

def eligible_items(catalog,stage):
    return [
        x for x in catalog["items"].values()
        if not x["unique"]
        and STAGE_INDEX[x["min_stage"]]<=STAGE_INDEX[stage]
        and x["availability"]!="ORIGIN_ONLY"
        and x["source_type"]!="STARTING_ISSUE"
    ]

def score(item,preferences):
    weights={tag:(len(preferences)-i)*10 for i,tag in enumerate(preferences)}
    tag_score=sum(weights.get(tag,0) for tag in item.get("build_tags",[]))
    return tag_score+min(5.0,float(item.get("power_budget",0)))

def assign(actor,stage,catalog,policy):
    prefs=policy["family_preferences"][actor["equipment_family"]]
    cap=policy["group_item_caps"][actor["a079_group"]][stage]
    slot_caps=policy["slot_caps"]
    ranked=sorted(eligible_items(catalog,stage),key=lambda x:(-score(x,prefs),x["item_id"]))
    used={};selected=[]
    for item in ranked:
        slot=item["slot"]
        if used.get(slot,0)>=slot_caps.get(slot,0):continue
        selected.append(item["item_id"]);used[slot]=used.get(slot,0)+1
        if len(selected)>=cap:break
    return selected

def validate(assignments,actors,catalog,policy):
    assert len(actors)==32
    item_by_id={x["item_id"]:x for x in catalog["items"].values()}
    for actor in actors:
        out=assignments["actors"][actor["actor_id"]]
        for stage,item_ids in out["by_story_stage"].items():
            used={}
            for item_id in item_ids:
                item=item_by_id[item_id]
                assert not item["unique"],(actor["actor_id"],item_id,"unique")
                assert STAGE_INDEX[item["min_stage"]]<=STAGE_INDEX[stage]
                slot=item["slot"];used[slot]=used.get(slot,0)+1
                assert used[slot]<=policy["slot_caps"][slot]
    return True

def build():
    actors=load_json(HERE/"npc_equipment_actor_registry.json")["actors"]
    policy=load_json(HERE/"npc_equipment_policy.json")
    catalog=load_json(CATALOG)
    result={"schema_version":"npc-equipment-assignments-v0.1","status":"LAB_PROPOSAL_NOT_CANON",
            "rules":{"unique_items_excluded":True,"source_npc_does_not_imply_worn":True,
                     "combat_stats_applied":False,"story_stage_gate":True},"actors":{}}
    for actor in actors:
        result["actors"][actor["actor_id"]]={
            "display_name":actor["display_name"],"role":actor["role"],
            "a079_group":actor["a079_group"],"equipment_family":actor["equipment_family"],
            "by_story_stage":{s:assign(actor,s,catalog,policy) for s in STAGE_INDEX},
        }
    validate(result,actors,catalog,policy)
    return result

if __name__=="__main__":
    result=build()
    out=HERE/"npc_equipment_assignments_proposal.generated.json"
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(f"PASS: 32/32 NPC equipment proposals -> {out}")
