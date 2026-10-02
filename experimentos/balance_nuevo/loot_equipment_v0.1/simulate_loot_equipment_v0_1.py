from __future__ import annotations
from collections import defaultdict
from pathlib import Path
import json, math, random, statistics

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
C=json.loads((HERE/"ARC1_MONSTER_LOOT_EQUIPMENT_PROPOSAL_V0_1.json").read_text(encoding="utf-8"))
EQ=json.loads((ROOT/"equipment_arc1_catalog.json").read_text(encoding="utf-8"))

SEED=20261001
FARM_SIZES=(100,1000,10000)
SESSION_N=100000

EXTRACTION_ITEM_DIFFICULTY={
 "grasa_qi_roida":"simple",
 "aguijon_jade":"normal",
 "membrana_serpentina":"dificil",
 "medula_viento":"normal",
 "tendon_tres_colas":"dificil",
 "camara_jade":"dificil",
 "vesicula_medicinal":"normal",
 "glandula_termica":"normal",
 "saco_hollin":"dificil",
 "caparazon_hierro":"normal",
 "membrana_ferrea":"dificil",
 "fluido_lunar":"normal",
 "branquia_lunar":"dificil",
 "conducto_estelar":"normal",
 "saco_residual_estelar":"dificil",
 "bolsa_niebla":"normal",
 "sedimento_niebla":"muy_dificil",
 "fibra_tempestad":"normal",
 "saco_pulmonar_tormenta":"dificil",
}
BASE=C["extraction_reference"]["base_probabilities"]

AUTO_TO_SPECIES={}
AUTO_PROB={}
RARE_REQUIRED=set()
EXTRACT_TO_SPECIES=defaultdict(list)
for sid,s in C["recurrent_species"].items():
    for x in s["automatic_loot"]:
        AUTO_TO_SPECIES[x["item_id"]]=sid
        AUTO_PROB[x["item_id"]]=float(x["probability"])
        if x["equipment_required"] and x["category"] in {"RARE","EXCEPTIONAL"}:
            RARE_REQUIRED.add(x["item_id"])
    for mid in s["extraction"]:
        EXTRACT_TO_SPECIES[mid].append(sid)

def pct(xs,q):
    ys=sorted(xs)
    i=min(len(ys)-1,max(0,math.ceil(q*len(ys))-1))
    return ys[i]

def farm_sim():
    out=[]
    for sid,s in C["recurrent_species"].items():
        rng=random.Random(f"{SEED}|farm|{sid}")
        for n in FARM_SIZES:
            counts={x["item_id"]:0 for x in s["automatic_loot"]}
            for _ in range(n):
                for x in s["automatic_loot"]:
                    if rng.random()<x["probability"]:
                        counts[x["item_id"]]+=x["quantity"]
            out.append({"species_id":sid,"kills":n,"drops":counts})
    return out

def route_species(route):
    auto=[mid for mid in route["materials"] if mid in AUTO_TO_SPECIES]
    if len(auto)!=1:
        raise AssertionError((route["equipment_id"],"must require exactly one auto-loot material",auto))
    sid=AUTO_TO_SPECIES[auto[0]]
    ext=[mid for mid in route["materials"] if mid in EXTRACTION_ITEM_DIFFICULTY]
    for mid in ext:
        if sid not in EXTRACT_TO_SPECIES[mid]:
            raise AssertionError((route["equipment_id"],mid,"extraction source differs from auto-loot species"))
    return sid,auto[0],ext

def one_session(rng,pdrop,ext_probs):
    have_drop=False
    ext_have=[False]*len(ext_probs)
    kills=0
    while not (have_drop and all(ext_have)):
        kills+=1
        if not have_drop and rng.random()<pdrop:
            have_drop=True
        for i,p in enumerate(ext_probs):
            if not ext_have[i] and rng.random()<p:
                ext_have[i]=True
        if kills>10000:
            raise RuntimeError("session runaway")
    return kills

def route_sim():
    rows=[]
    for route in C["equipment_material_routes"]:
        sid,auto,ext=route_species(route)
        pdrop=AUTO_PROB[auto]
        for rank,bonus in (("INICIADO",0.0),("NOVICIO",0.05)):
            ext_probs=[min(C["extraction_reference"]["global_cap"],BASE[EXTRACTION_ITEM_DIFFICULTY[mid]]+bonus) for mid in ext]
            rng=random.Random(f"{SEED}|route|{route['equipment_id']}|{rank}")
            vals=[one_session(rng,pdrop,ext_probs) for _ in range(SESSION_N)]
            rows.append({
              "equipment_id":route["equipment_id"],"species_id":sid,"rank":rank,
              "sessions":SESSION_N,"auto_item":auto,"auto_probability":pdrop,
              "extraction_items":ext,"extraction_probabilities":ext_probs,
              "kills_mean":statistics.fmean(vals),"kills_median":statistics.median(vals),
              "kills_p90":pct(vals,.90),"kills_p95":pct(vals,.95),"kills_p99":pct(vals,.99)
            })
    return rows

def validate():
    item_ids={x["item_id"] for x in EQ["items"]}
    assert not RARE_REQUIRED,RARE_REQUIRED
    assert C["guards"]["no_same_species_auto_loot_extraction_duplicate"] is True
    for sid,s in C["recurrent_species"].items():
        auto={x["item_id"] for x in s["automatic_loot"]}
        ext=set(s["extraction"])
        assert auto.isdisjoint(ext),(sid,auto&ext)
        for x in s["automatic_loot"]:
            p=float(x["probability"])
            if x["equipment_required"]:
                assert .08<=p<=.15,(sid,x["item_id"],p)
    for r in C["equipment_material_routes"]:
        assert r["equipment_id"] in item_ids,r["equipment_id"]
        assert r["existing_route_preserved"] is True
    assert C["mutant_loot"]["probability_scaling"] is False
    assert C["mutant_loot"]["expected_quantity_multiplier"]==1.5
    assert C["mutant_loot"]["extraction_affected"] is False

def main():
    validate()
    farms=farm_sim()
    routes=route_sim()
    max_p95=max(r["kills_p95"] for r in routes if r["rank"]=="INICIADO")
    summary={
      "status":"LAB_COMPLETE_NOT_RATIFIED",
      "farm_sizes":FARM_SIZES,
      "route_sessions_per_rank":SESSION_N,
      "max_iniciado_p95_kills":max_p95,
      "farm_results":farms,
      "equipment_route_results":routes,
      "guards":{
        "all_required_auto_drops_in_8_15pct_band":True,
        "rare_required_for_equipment":False,
        "same_species_auto_extraction_overlap":False,
        "existing_equipment_routes_preserved":True,
        "equipment_stats_modified":False,
        "mutant_probability_scaled":False
      }
    }
    (HERE/"LOOT_EQUIPMENT_SIMULATION_V0_1.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    lines=["# Loot + equipment economy simulation v0.1","",f"Routes: {len(C['equipment_material_routes'])}; sessions/rank: {SESSION_N:,}.",""]
    for r in routes:
        if r["rank"]=="INICIADO":
            lines.append(f"- {r['equipment_id']}: mean {r['kills_mean']:.2f}; median {r['kills_median']:.0f}; P90 {r['kills_p90']}; P95 {r['kills_p95']}; P99 {r['kills_p99']}.")
    (HERE/"LOOT_EQUIPMENT_SIMULATION_V0_1.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    print(json.dumps({"status":summary["status"],"max_iniciado_p95_kills":max_p95,"routes":routes},ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
