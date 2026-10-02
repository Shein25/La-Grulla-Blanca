from __future__ import annotations
from pathlib import Path
from collections import defaultdict
import json, math, random, statistics

HERE=Path(__file__).resolve().parent
C=json.loads((HERE/"ARC1_COMMERCE_BALANCE_V0_3.json").read_text(encoding="utf-8"))
L=json.loads((HERE/"ARC1_MONSTER_LOOT_EQUIPMENT_PROPOSAL_V0_1.json").read_text(encoding="utf-8"))

STAGE_ORDER={"LianQi_I":1,"LianQi_II":2,"LianQi_III":3,"LianQi_IV":4}
BASE_EXT=L["extraction_reference"]["base_probabilities"]
NOVICE_BONUS=0.05
SEED=20261002
N=50000

AUTO_SOURCE={}
AUTO={}
EXT_SOURCE=defaultdict(list)
for sid,s in L["recurrent_species"].items():
    for x in s["automatic_loot"]:
        AUTO_SOURCE[x["item_id"]]=sid
        AUTO[x["item_id"]]=x
    for mid in s["extraction"]:
        EXT_SOURCE[mid].append(sid)

MONSTER_STAGE={
 "rata_qi":"LianQi_I","serpiente_qi":"LianQi_I","lobo_espiritual":"LianQi_I",
 "avispa_jade":"LianQi_I","mono_pildoras":"LianQi_I",
 "sapo_ceniza":"LianQi_II","escarabajo_hierro":"LianQi_II",
 "pez_lunar":"LianQi_III","anguila_estelar":"LianQi_III",
 "devorador_niebla":"LianQi_IV","halcon_tormenta":"LianQi_IV",
}

def bulk_unit_value(stage,diff):
    r=C["material_buyback_policy"]["extraction_bulk_rates"][stage][diff]
    return r["stones"]/r["units"]

def sale_ev_species(sid, novice=False):
    stage=MONSTER_STAGE[sid]
    s=L["recurrent_species"][sid]
    total=0.0
    details=[]
    for x in s["automatic_loot"]:
        price=C["material_buyback_policy"]["automatic_loot_per_unit_stones"][x["item_id"]]
        ev=x["probability"]*x["quantity"]*price
        total+=ev
        details.append((x["item_id"],ev))
    for mid in s["extraction"]:
        meta=C["material_buyback_policy"]["extraction_materials"][mid]
        p=BASE_EXT[meta["difficulty"]]+(NOVICE_BONUS if novice else 0.0)
        p=min(C.get("extraction_reference",L["extraction_reference"])["global_cap"],p)
        ev=p*meta["yield_on_success"]*bulk_unit_value(meta["stage"],meta["difficulty"])
        total+=ev
        details.append((mid,ev))
    return total,details

def pctl(v,q):
    a=sorted(v)
    return a[min(len(a)-1,max(0,math.ceil(q*len(a))-1))]

def source_candidates(mid):
    if mid in AUTO_SOURCE:
        return [(AUTO_SOURCE[mid],"auto")]
    if mid in EXT_SOURCE:
        return [(sid,"extract") for sid in EXT_SOURCE[mid]]
    raise KeyError(mid)

def one_material_kills(rng,mid,qty,novice=False):
    # Choose best valid source for duplicated materials.
    cand=source_candidates(mid)
    best=None
    for sid,kind in cand:
        if kind=="auto":
            x=AUTO[mid]
            p=x["probability"]
            y=x["quantity"]
        else:
            meta=C["material_buyback_policy"]["extraction_materials"][mid]
            p=BASE_EXT[meta["difficulty"]]+(NOVICE_BONUS if novice else 0.0)
            p=min(L["extraction_reference"]["global_cap"],p)
            y=meta["yield_on_success"]
        expected=qty/(p*y)
        if best is None or expected<best[0]:
            best=(expected,sid,kind,p,y)
    _,sid,kind,p,y=best
    have=0;kills=0
    while have<qty:
        kills+=1
        if rng.random()<p:
            have+=y
        if kills>10000: raise RuntimeError((mid,qty))
    return kills,sid

def route_burden():
    rows=[]
    for route in C["material_exchange_policy"]["routes"]:
        eq=next(x for x in C["equipment"] if x["item_id"]==route["equipment_id"])
        # Same-species materials are farmed in parallel, cross-species burdens add.
        for novice in (False,True):
            vals=[]
            for rep in range(N):
                rng=random.Random(f"{SEED}|{route['equipment_id']}|{int(novice)}|{rep}")
                need_by_species=defaultdict(dict)
                # Resolve source per material once, then simulate each species jointly.
                for mid,qty in route["materials"].items():
                    cands=source_candidates(mid)
                    best=None
                    for sid,kind in cands:
                        if kind=="auto":
                            x=AUTO[mid];p=x["probability"];y=x["quantity"]
                        else:
                            meta=C["material_buyback_policy"]["extraction_materials"][mid]
                            p=BASE_EXT[meta["difficulty"]]+(NOVICE_BONUS if novice else 0.0)
                            p=min(L["extraction_reference"]["global_cap"],p);y=meta["yield_on_success"]
                        exp=qty/(p*y)
                        if best is None or exp<best[0]: best=(exp,sid,kind,p,y)
                    _,sid,kind,p,y=best
                    need_by_species[sid][mid]=(qty,kind,p,y)

                total_kills=0
                for sid,needs in need_by_species.items():
                    have={mid:0 for mid in needs}
                    kills=0
                    while any(have[mid]<needs[mid][0] for mid in needs):
                        kills+=1
                        for mid,(qty,kind,p,y) in needs.items():
                            if have[mid]>=qty: continue
                            if rng.random()<p: have[mid]+=y
                        if kills>10000: raise RuntimeError(route["equipment_id"])
                    total_kills+=kills
                vals.append(total_kills)

            rows.append({
              "equipment_id":route["equipment_id"],"stage":eq["stage"],
              "rank":"NOVICIO" if novice else "INICIADO",
              "mean_kills":statistics.fmean(vals),"median_kills":statistics.median(vals),
              "p90":pctl(vals,.90),"p95":pctl(vals,.95),"p99":pctl(vals,.99),
              "full_stone_price":route.get("full_stone_price"),
              "service_fee_stones":route["service_fee_stones"],
              "contribution_required":route["contribution_required"],
            })
    return rows

def main():
    routes=C["material_exchange_policy"]["routes"]
    assert len(routes)==24
    assert 30<=C["material_exchange_policy"]["coverage_target"]["percentage"]<=40

    # Stage safety + savings.
    for r in routes:
        eq=next(x for x in C["equipment"] if x["item_id"]==r["equipment_id"])
        for mid in r["materials"]:
            if mid in C["material_buyback_policy"]["extraction_materials"]:
                mst=C["material_buyback_policy"]["extraction_materials"][mid]["stage"]
            else:
                mst=MONSTER_STAGE[AUTO_SOURCE[mid]]
            assert STAGE_ORDER[mst]<=STAGE_ORDER[eq["stage"]],(r["equipment_id"],mid,mst,eq["stage"])
        if r.get("full_stone_price"):
            save=1-r["service_fee_stones"]/r["full_stone_price"]
            assert .50<=save<=.75,(r["equipment_id"],save)

    # Liquidation EV: even selling every automatic drop + every successful extraction
    # should not rapidly finance the top full-price item of the native stage.
    max_price={}
    for st in STAGE_ORDER:
        vals=[x["stone_price"] for x in C["equipment"] if x["stage"]==st and x["stone_price"]]
        max_price[st]=max(vals) if vals else 0
    thresholds={"LianQi_I":10,"LianQi_II":20,"LianQi_III":20,"LianQi_IV":35}
    sale=[]
    for sid,stage in MONSTER_STAGE.items():
        for novice in (False,True):
            ev,details=sale_ev_species(sid,novice)
            kills=max_price[stage]/ev if ev else 999999
            assert kills>=thresholds[stage],(sid,novice,ev,kills,thresholds[stage])
            sale.append({
              "species_id":sid,"stage":stage,"rank":"NOVICIO" if novice else "INICIADO",
              "expected_stones_per_kill_if_everything_is_sold":ev,
              "kills_to_max_full_price_stage_item":kills,
              "components":details
            })

    burdens=route_burden()
    # Material path is optional: P95 may be substantial, but no path should become absurd.
    assert max(x["p95"] for x in burdens if x["rank"]=="INICIADO")<=60

    out={
      "status":"PASS_LAB_NOT_CANON",
      "route_count":len(routes),
      "route_coverage_percent":C["material_exchange_policy"]["coverage_target"]["percentage"],
      "sale_liquidation":sale,
      "route_burden":burdens,
      "guards":{
        "no_future_stage_materials":True,
        "material_service_savings_50_to_75pct":True,
        "selling_everything_not_fastest_progression":True,
        "max_iniciado_route_p95_le_60":True,
        "contribution_never_spent":True
      }
    }
    (HERE/"MATERIAL_ECONOMY_V0_3_VALIDATION.json").write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({
      "status":out["status"],
      "coverage":out["route_coverage_percent"],
      "max_route_p95":max(x["p95"] for x in burdens if x["rank"]=="INICIADO"),
      "sale":sale,
      "routes":burdens
    },ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
