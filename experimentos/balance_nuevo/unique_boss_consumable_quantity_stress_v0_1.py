from __future__ import annotations
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed
from copy import deepcopy
from pathlib import Path
import hashlib, json, math, random, statistics, sys, zipfile

HERE=Path(__file__).resolve().parent
STAGE1=HERE/"stage1_integral_t0_optuna"
for p in (str(HERE),str(STAGE1)):
    if p not in sys.path: sys.path.insert(0,p)

import etapa19b_combat_engine as engine
import etapa19_skill_buildspace as skillspace
import player_policy_veteran as veteran

EXPERIMENT="UNIQUE_BOSSES_CONSUMABLE_QUANTITY_STRESS_V01"
MASTER_SEED=20261001
POLICIES=("VETERAN",)
LOADOUTS=("MANDATORY_ENTRY","EXPECTED_STAGE","HIGH_ROLL_STRESS")
ROOTS=tuple(engine.ROOT_TECHNIQUES)
FIGHTS_PER_CONTEXT=60

EQUIPMENT=json.loads((HERE/"equipment_arc1_catalog.json").read_text(encoding="utf-8"))
TECHNIQUES=json.loads((HERE/"techniques_arc1_catalog.json").read_text(encoding="utf-8"))
HP_CONTRACT=json.loads((HERE/"alchemy_consumables_v0.1/ALCHEMY_VITALITY_HP_CONTRACT_V0_1.json").read_text(encoding="utf-8"))
QI_CONTRACT=json.loads((HERE/"alchemy_consumables_v0.1/ALCHEMY_QI_RECOVERY_CONTRACT_V0_2.json").read_text(encoding="utf-8"))

BOSSES={
 "sapo_caldera":{
  "candidate_id":"sapo_caldera-b00-b43e088b51","stage":"LianQi_II","role":"BOSS","element":"fuego",
  "stats":{"hp":83,"qi_max":None,"precision":99,"evasion":27,"defense":4,"tenacity":23,"control":0,"crit_chance":5,"crit_damage":1.5,"basic_damage":"1d2+7"},
  "technique":{"name":"Eructo del Horno Hundido","mechanics":["DIRECT_DAMAGE","BURN_DOT"],"params":{"cadence":3,"direct_damage":"1d3+7","burn":{"damage":"1d2+2","ticks":4}}},
 },
 "rey_escarabajo":{
  "candidate_id":"rey_escarabajo-b07-52c54baab4","stage":"LianQi_II","role":"BOSS","element":"metal",
  "stats":{"hp":87,"qi_max":None,"precision":97,"evasion":13,"defense":4,"tenacity":23,"control":0,"crit_chance":5,"crit_damage":1.5,"basic_damage":"1d2+6"},
  "technique":{"name":"Mandíbula de Yunque","mechanics":["DIRECT_DAMAGE"],"params":{"cadence":3,"direct_damage":"1d10+9"}},
 },
 "guardian_coral":{
  "candidate_id":"guardian_coral-b10-22f01b55e7","stage":"LianQi_III","role":"BOSS","element":"agua",
  "stats":{"hp":80,"qi_max":None,"precision":103,"evasion":39,"defense":5,"tenacity":18,"control":0,"crit_chance":5,"crit_damage":1.5,"basic_damage":"1d2+7"},
  "technique":{"name":"Marea de los Nombres Hundidos","mechanics":["DIRECT_DAMAGE","QI_DRAIN"],"params":{"cadence":2,"direct_damage":"1d3+8","qi_drain":12}},
 },
 "mantis_nube":{
  "candidate_id":"mantis_nube-b08-04e4ccc69a","stage":"LianQi_IV","role":"BOSS","element":"viento",
  "stats":{"hp":72,"qi_max":None,"precision":103,"evasion":44,"defense":7,"tenacity":7,"control":0,"crit_chance":5,"crit_damage":1.5,"basic_damage":"1d5+9"},
  "technique":{"name":"Tijera del Horizonte","mechanics":["DIRECT_DAMAGE"],"params":{"cadence":4,"direct_damage":"3d10+9"}},
 },
 "centinela_pluma":{
  "candidate_id":"centinela_pluma-b01-e3ffe23c9c","stage":"LianQi_IV","role":"BOSS","element":"metal",
  "stats":{"hp":123,"qi_max":None,"precision":99,"evasion":36,"defense":5,"tenacity":37,"control":0,"crit_chance":5,"crit_damage":1.5,"basic_damage":"2d8+8"},
  "technique":{"name":"Aleteo de Cuchillas","mechanics":["DIRECT_DAMAGE"],"params":{"cadence":3,"direct_damage":"2d6+9"}},
 },
}
PREV_STAGE={"LianQi_II":"LianQi_I","LianQi_III":"LianQi_II","LianQi_IV":"LianQi_III"}

PREP_ARMS=(
 "HP1_EXCEPTIONAL",
 "HP2_EXCEPTIONAL",
 "HP3_EXCEPTIONAL",
 "HP1_QI1_EXCEPTIONAL",
 "HP2_QI1_EXCEPTIONAL",
 "HP3_QI1_EXCEPTIONAL",
)

def seed(*parts):
    s="|".join([str(MASTER_SEED),*(str(x) for x in parts)])
    return int.from_bytes(hashlib.sha256(s.encode()).digest()[:8],"big")

def numeric_features(obj,prefix=""):
    out={}
    if isinstance(obj,dict):
        for k,v in obj.items():
            if k in {"choices","families","technique_id","name","root","role","targeting","model"}: continue
            out.update(numeric_features(v,f"{prefix}.{k}" if prefix else k))
    elif isinstance(obj,(list,tuple)):
        for i,v in enumerate(obj):out.update(numeric_features(v,f"{prefix}[{i}]"))
    elif isinstance(obj,(int,float)) and not isinstance(obj,bool):
        x=float(obj)
        if math.isfinite(x):out[prefix]=x
    return out

def farthest(rows,k):
    if len(rows)<=k:return rows
    keys=sorted({key for row in rows for key in row["features"]})
    mins={key:min(r["features"].get(key,0.0) for r in rows) for key in keys}
    maxs={key:max(r["features"].get(key,0.0) for r in rows) for key in keys}
    def vec(r):
        return tuple(0.0 if maxs[k]<=mins[k] else (r["features"].get(k,0.0)-mins[k])/(maxs[k]-mins[k]) for k in keys)
    vs=[vec(r) for r in rows]
    centroid=tuple(statistics.fmean(v[j] for v in vs) for j in range(len(keys)))
    def dist(a,b):return math.sqrt(sum((x-y)**2 for x,y in zip(a,b)))
    first=min(range(len(rows)),key=lambda i:(dist(vs[i],centroid),rows[i]["signature"]))
    chosen=[first]
    while len(chosen)<k:
        nxt=max((i for i in range(len(rows)) if i not in chosen),key=lambda i:min(dist(vs[i],vs[j]) for j in chosen))
        chosen.append(nxt)
    return [rows[i] for i in chosen]

_REPS={}
def skill_reps(stage,root,k=2):
    key=(stage,root,k)
    if key in _REPS:return _REPS[key]
    points=skillspace.STAGES[stage]["points"]
    builds=[b for b in skillspace.enumerate_skill_builds(root,stage) if b.points_spent==points]
    rows=[]
    for b in builds:
        paths={x.technique_id:x.choices for x in b.paths}
        comp=engine.compile_build(root,paths,TECHNIQUES)
        feats={}
        for tid,c in sorted(comp.items()):
            for fk,fv in numeric_features(c).items():feats[f"{tid}:{fk}"]=fv
        rows.append({"signature":b.signature,"paths":paths,"features":feats})
    reps=farthest(rows,k)
    for i,r in enumerate(reps):r["coverage_id"]=f"SKILL_COVERAGE_{i}"
    _REPS[key]=reps
    return reps

def boss_profile(sid):
    b=BOSSES[sid]
    return {
      "id":sid,"name":sid,"native_stage":b["stage"],
      "native_stage_index":{"LianQi_II":2,"LianQi_III":3,"LianQi_IV":4}[b["stage"]],
      "role":"BOSS","region":"LAB","element":b["element"],"unique":True,
      "engine_contract":"NEW_COMBAT_STATS_V0_1","stats_status":"LAB_CANDIDATE",
      "stats":deepcopy(b["stats"]),
      "technique":{"name":b["technique"]["name"],"mechanics":deepcopy(b["technique"]["mechanics"]),"params_status":"LAB_CANDIDATE","params":deepcopy(b["technique"]["params"])},
      "ai":{"cognition":"LAB","social":"LAB"},
      "adaptive":{"status":"UNIQUE_NO_T1_T4","rule":"Unique boss stress only"},
      "resource_model":"NONE",
    }

def boss_actor(sid):
    s=BOSSES[sid]["stats"]
    return engine.Actor(
      hp_max=float(s["hp"]),hp=float(s["hp"]),qi_max=0.0,qi=0.0,
      precision=float(s["precision"]),evasion=float(s["evasion"]),
      defense=float(s["defense"]),tenacity=float(s["tenacity"]),
      control=float(s["control"]),crit_chance=float(s["crit_chance"]),
      crit_damage=float(s["crit_damage"])
    )

def prep_inventory(stage,arm):
    inv={"hp":None,"hp_count":0,"qi":None,"qi_count":0}
    if arm not in PREP_ARMS:
        raise KeyError(arm)
    hp_count=int(arm[2])
    qi_count=1 if "_QI1_" in arm else 0
    h=HP_CONTRACT["formulations"][stage]["qualities"]["excepcional"]
    q=QI_CONTRACT["formulations"][stage]["qualities"]["excepcional"]
    inv["hp"]={"stage":stage,"quality":"excepcional",**h}
    inv["hp_count"]=hp_count
    if qi_count:
        inv["qi"]={"stage":stage,"quality":"excepcional","restore":float(q)}
        inv["qi_count"]=qi_count
    return inv

def maybe_consume(state,rng,inv):
    # Observable-state veteran rule. Drinking itself is the entire player action.
    if inv["hp_count"]>0 and inv["hp"]:
        h=inv["hp"]
        deficit=state.player.hp_max-state.player.hp
        if state.player.hp/state.player.hp_max<=0.60 and deficit>=float(h["min"]):
            rolled=float(engine.roll_dice(rng,h["formula"]))
            actual=min(deficit,rolled)
            state.player.hp+=actual
            state.metrics.overheal+=max(0.0,rolled-actual)
            inv["hp_count"]-=1
            return ("HP",actual)
    if inv["qi_count"]>0 and inv["qi"]:
        offensive=[c for c in state.compiled.values() if c.get("role")!="DEFENSIVE"]
        cheapest=min((float(c["qi_cost"]) for c in offensive),default=0.0)
        missing=state.player.qi_max-state.player.qi
        if state.player.qi<cheapest and missing>0:
            actual=min(missing,float(inv["qi"]["restore"]))
            state.player.qi+=actual
            state.metrics.qi_restored+=actual
            inv["qi_count"]-=1
            return ("QI",actual)
    return (None,0.0)

def choose_action(state,policy):
    if policy=="VETERAN":return veteran.choose_veteran_action(state)
    return engine.choose_player_action(state,policy)

def fight_one(sid,prep_arm,loadout,root,rep,policy,i):
    stage=BOSSES[sid]["stage"]
    item_ids=EQUIPMENT["simulation_loadouts"][loadout][stage]
    player,meta=engine.build_player(stage,root,item_ids,EQUIPMENT)
    monster=boss_actor(sid)
    compiled=engine.compile_build(root,engine.normalize_paths(rep["paths"]),TECHNIQUES)
    profile=boss_profile(sid)
    state=engine.FightState(
      player=player,monster=monster,player_root=root,stage=stage,tier="T0",
      player_basic_dice=engine.STAGES[stage]["basic_attack"],
      tech_scalar=engine.STAGES[stage]["tech_scalar"],compiled=compiled,
      monster_profile=profile,signal_bridge=engine.LabSignalBridge(),
      equipment_effects=meta["equipment_effects"]
    )
    rng=random.Random(seed(sid,prep_arm,loadout,root,rep["coverage_id"],policy,i))
    inv=prep_inventory(stage,prep_arm)
    telemetry={"hp_uses":0,"qi_uses":0,"hp_restored":0.0,"qi_restored":0.0}
    while player.alive() and monster.alive() and state.round_no<150:
        state.round_no+=1
        engine.player_turn_start(state,rng)
        if not player.alive():break

        kind,amount=maybe_consume(state,rng,inv)
        if kind:
            telemetry[kind.lower()+"_uses"]+=1
            telemetry[kind.lower()+"_restored"]+=amount
        else:
            aid=choose_action(state,policy)
            if aid==veteran.VETERAN_BASIC:
                engine.execute_basic(state,rng)
            else:
                c=compiled[aid]
                if not engine.execute_player_technique(state,rng,c):
                    engine.execute_basic(state,rng)

        if not monster.alive():break
        engine.monster_turn_start(state,rng)
        if not monster.alive():break
        engine.execute_monster_turn(state,rng)
        engine.end_round(state)

    win=monster.hp<=0 and player.hp>0
    return {
      "win":win,
      "timeout":state.round_no>=150 and player.alive() and monster.alive(),
      "rounds":state.round_no,
      "player_hp_final_pct":max(0.0,player.hp)/player.hp_max,
      "monster_hp_final_pct":max(0.0,monster.hp)/monster.hp_max,
      "qi_final":max(0.0,player.qi),
      "qi_spent":state.metrics.qi_spent,
      "qi_drained":state.metrics.qi_drained,
      "boss_skill_uses":state.metrics.monster_attempts,
      **telemetry,
    }

def worker(args):
    sid,prep_arm,loadout,root,rep,policy,fights=args
    rows=[fight_one(sid,prep_arm,loadout,root,rep,policy,i) for i in range(fights)]
    keys=("rounds","player_hp_final_pct","monster_hp_final_pct","qi_final","qi_spent","qi_drained","boss_skill_uses","hp_uses","qi_uses","hp_restored","qi_restored")
    return {
      "species_id":sid,"candidate_id":BOSSES[sid]["candidate_id"],"stage":BOSSES[sid]["stage"],
      "prep_arm":prep_arm,"loadout":loadout,"root":root,"policy":policy,
      "skill_rep":rep["coverage_id"],"fights":fights,
      "win_rate":sum(x["win"] for x in rows)/fights,
      "timeout_rate":sum(x["timeout"] for x in rows)/fights,
      **{k+"_mean":statistics.fmean(float(x[k]) for x in rows) for k in keys}
    }

def weighted(rows,key):
    n=sum(r["fights"] for r in rows)
    return sum(r[key]*r["fights"] for r in rows)/n

def breakdown(rows,key):
    g=defaultdict(list)
    for r in rows:g[r[key]].append(r)
    vals={k:weighted(v,"win_rate") for k,v in g.items()}
    return vals,max(vals.values())-min(vals.values())

def summarize(sid,prep_arm,rows):
    pb,ps=breakdown(rows,"policy")
    rb,rs=breakdown(rows,"root")
    lb,ls=breakdown(rows,"loadout")
    return {
      "species_id":sid,"candidate_id":BOSSES[sid]["candidate_id"],"stage":BOSSES[sid]["stage"],
      "prep_arm":prep_arm,"fights":sum(r["fights"] for r in rows),
      "player_win_rate":weighted(rows,"win_rate"),
      "timeout_rate":weighted(rows,"timeout_rate"),
      "rounds_mean":weighted(rows,"rounds_mean"),
      "player_hp_pressure":1-weighted(rows,"player_hp_final_pct_mean"),
      "monster_hp_final_pct_mean":weighted(rows,"monster_hp_final_pct_mean"),
      "policy_breakdown":pb,"policy_win_spread":ps,
      "root_breakdown":rb,"root_win_spread":rs,
      "loadout_breakdown":lb,"loadout_win_spread":ls,
      "hp_uses_mean":weighted(rows,"hp_uses_mean"),
      "qi_uses_mean":weighted(rows,"qi_uses_mean"),
      "hp_restored_mean":weighted(rows,"hp_restored_mean"),
      "qi_restored_mean":weighted(rows,"qi_restored_mean"),
      "qi_drained_mean":weighted(rows,"qi_drained_mean"),
    }

def main():
    out=Path(EXPERIMENT);out.mkdir(exist_ok=True)
    tasks=[]
    for sid,b in BOSSES.items():
      stage=b["stage"]
      for prep in PREP_ARMS:
       for loadout in LOADOUTS:
        for root in ROOTS:
         for rep in skill_reps(stage,root,2):
          for policy in POLICIES:
           tasks.append((sid,prep,loadout,root,rep,policy,FIGHTS_PER_CONTEXT))

    rows=[]
    with ProcessPoolExecutor(max_workers=4) as ex:
        fs=[ex.submit(worker,t) for t in tasks]
        for f in as_completed(fs):rows.append(f.result())

    grouped=defaultdict(list)
    for r in rows:grouped[(r["species_id"],r["prep_arm"])].append(r)
    summaries=[summarize(s,p,v) for (s,p),v in sorted(grouped.items())]

    for sid in BOSSES:
        base=next(x for x in summaries if x["species_id"]==sid and x["prep_arm"]=="HP1_EXCEPTIONAL")
        for x in summaries:
            if x["species_id"]==sid:
                x["delta_win_vs_hp1_pp"]=(x["player_win_rate"]-base["player_win_rate"])*100
                x["delta_rounds_vs_none"]=x["rounds_mean"]-base["rounds_mean"]

    manifest={
      "experiment":EXPERIMENT,"status":"COMPLETE_LAB_NOT_CANON",
      "source_branch":"experiment/boss-consumable-stress-v0.1",
      "boss_count":len(BOSSES),"prep_arms":list(PREP_ARMS),"quantity_stress":True,
      "policies":list(POLICIES),"loadouts":list(LOADOUTS),"roots":list(ROOTS),
      "skill_reps":2,"fights_per_context":FIGHTS_PER_CONTEXT,
      "total_fights":sum(x["fights"] for x in summaries),
      "consumable_policy":{
        "hp_quantity_axis":[1,2,3],"qi_quantity_axis":[0,1],
        "hp_trigger":"HP <= 60% max AND missing HP >= potion minimum",
        "qi_trigger":"current Qi below cheapest offensive technique cost",
        "drinking_consumes_full_player_action":True,
        "monster_gets_normal_response_turn":True,
        "no_artificial_potion_cooldown":True
      },
      "guards":{
        "canonical_write":False,"boss_t0_modified":False,"main_used":False,
        "merge_performed":False,"target_win_rate_objective_used":False,
        "t1_t4_executed":False
      }
    }

    payload={"manifest":manifest,"summaries":summaries}
    (out/"SUMMARY.json").write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    with (out/"context_aggregates.jsonl").open("w",encoding="utf-8") as f:
        for r in sorted(rows,key=lambda x:(x["species_id"],x["prep_arm"],x["loadout"],x["root"],x["skill_rep"],x["policy"])):
            f.write(json.dumps(r,ensure_ascii=False,sort_keys=True)+"\n")

    md=["# Unique bosses — prepared consumable stress v0.1","",f"Total fights: **{manifest['total_fights']:,}**",""]
    for sid in BOSSES:
        md.append(f"## {sid}")
        for x in [y for y in summaries if y["species_id"]==sid]:
            md.append(
              f"- {x['prep_arm']}: win {x['player_win_rate']:.2%}; Δ {x['delta_win_vs_hp1_pp']:+.2f} pp; "
              f"rounds {x['rounds_mean']:.2f}; HP uses {x['hp_uses_mean']:.2f}; Qi uses {x['qi_uses_mean']:.2f}; "
              f"policy spread {x['policy_win_spread']:.2%}; root spread {x['root_win_spread']:.2%}; loadout spread {x['loadout_win_spread']:.2%}."
            )
        md.append("")
    (out/"SUMMARY.md").write_text("\n".join(md)+"\n",encoding="utf-8")

    zp=Path(f"RESULTADOS_{EXPERIMENT}.zip")
    with zipfile.ZipFile(zp,"w",zipfile.ZIP_DEFLATED) as z:
        for p in sorted(out.rglob("*")):
            if p.is_file():z.write(p,p.relative_to(out.parent))
    print(json.dumps({"zip":str(zp),"manifest":manifest,"summaries":summaries},ensure_ascii=False,indent=2))

if __name__=="__main__":main()
