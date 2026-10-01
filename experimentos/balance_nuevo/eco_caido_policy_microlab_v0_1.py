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

EXPERIMENT="MICROLAB_ECO_CAIDO_POLICY_CAUSAL_V01"
MASTER_SEED=20261001
STAGE="LianQi_II"
POLICIES=("VETERAN","UNITARGET_FIRST","AOE_FIRST","DEFENSE_OPEN","ROTATION")
LOADOUTS=("MANDATORY_ENTRY","EXPECTED_STAGE","HIGH_ROLL_STRESS")
ROOTS=tuple(engine.ROOT_TECHNIQUES)

CANDIDATES={
 "b06_selected":{
   "candidate_id":"eco_caido-b06-a11ec42a75",
   "stats":{"hp":51,"qi_max":None,"precision":102,"evasion":24,"defense":1,"tenacity":24,"control":0,"crit_chance":5,"crit_damage":1.5,"basic_damage":"1d3+6"},
 },
 "b08_softer":{
   "candidate_id":"eco_caido-b08-1fc8d46b0a",
   "stats":{"hp":48,"qi_max":None,"precision":100,"evasion":22,"defense":0,"tenacity":22,"control":0,"crit_chance":5,"crit_damage":1.5,"basic_damage":"1d2+6"},
 },
 "b10_defense_heavy":{
   "candidate_id":"eco_caido-b10-f43b8b07c8",
   "stats":{"hp":46,"qi_max":None,"precision":98,"evasion":19,"defense":4,"tenacity":20,"control":0,"crit_chance":5,"crit_damage":1.5,"basic_damage":"1d3+5"},
 },
}

ARMS={
 "BASELINE":{"aoe_scalar":None,"qi_mode":"BASELINE"},
 "SCALAR_1":{"aoe_scalar":1.0,"qi_mode":"BASELINE"},
 "COST_EQ_UNIT":{"aoe_scalar":None,"qi_mode":"EQUAL_UNITARGET"},
 "SCALAR_1_COST_EQ_UNIT":{"aoe_scalar":1.0,"qi_mode":"EQUAL_UNITARGET"},
}

def seed(*parts):
    s="|".join([str(MASTER_SEED),*(str(x) for x in parts)])
    return int.from_bytes(hashlib.sha256(s.encode()).digest()[:8],"big")

def load_json(p): return json.loads(Path(p).read_text(encoding="utf-8"))
EQUIPMENT=load_json(HERE/"equipment_arc1_catalog.json")
TECHNIQUES=load_json(HERE/"techniques_arc1_catalog.json")

def numeric_features(obj,prefix=""):
    out={}
    if isinstance(obj,dict):
        for k,v in obj.items():
            if k in {"choices","families","technique_id","name","root","role","targeting","model"}: continue
            out.update(numeric_features(v,f"{prefix}.{k}" if prefix else k))
    elif isinstance(obj,(list,tuple)):
        for i,v in enumerate(obj): out.update(numeric_features(v,f"{prefix}[{i}]"))
    elif isinstance(obj,(int,float)) and not isinstance(obj,bool):
        x=float(obj)
        if math.isfinite(x): out[prefix]=x
    return out

def farthest(rows,k):
    if len(rows)<=k:return rows
    keys=sorted({key for row in rows for key in row["features"]})
    mins={key:min(r["features"].get(key,0.0) for r in rows) for key in keys}
    maxs={key:max(r["features"].get(key,0.0) for r in rows) for key in keys}
    def vec(r):
        return tuple(0.0 if maxs[key]<=mins[key] else (r["features"].get(key,0.0)-mins[key])/(maxs[key]-mins[key]) for key in keys)
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
def skill_reps(root,k=3):
    key=(root,k)
    if key in _REPS:return _REPS[key]
    points=skillspace.STAGES[STAGE]["points"]
    builds=[b for b in skillspace.enumerate_skill_builds(root,STAGE) if b.points_spent==points]
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

def profile(candidate_key):
    c=CANDIDATES[candidate_key]
    return {
      "id":"eco_caido","name":"eco del caído","native_stage":STAGE,"native_stage_index":2,
      "role":"ELITE","region":"LAB","element":None,"unique":True,
      "engine_contract":"NEW_COMBAT_STATS_V0_1","stats_status":"READY",
      "stats":deepcopy(c["stats"]),"technique":None,
      "ai":{"cognition":"INSTINTIVO","social":"SOLITARIO"},
      "adaptive":{"status":"UNIQUE_NO_T1_T4","rule":"LAB unique encounter"},
      "resource_model":"NONE",
    }

def build_monster_actor(candidate_key):
    s=CANDIDATES[candidate_key]["stats"]
    return engine.Actor(
      hp_max=float(s["hp"]),hp=float(s["hp"]),qi_max=0.0,qi=0.0,
      precision=float(s["precision"]),evasion=float(s["evasion"]),
      defense=float(s["defense"]),tenacity=float(s["tenacity"]),
      control=0.0,crit_chance=5.0,crit_damage=1.5
    )

def apply_arm(compiled,root,arm_name):
    cfg=ARMS[arm_name]
    offensive,defensive,aoe=engine.ROOT_TECHNIQUES[root]
    if cfg["aoe_scalar"] is not None:
        compiled[aoe]["aoe_scalar"]=float(cfg["aoe_scalar"])
    if cfg["qi_mode"]=="EQUAL_UNITARGET":
        compiled[aoe]["qi_cost"]=float(compiled[offensive]["qi_cost"])
    return compiled

def choose_action(state,policy):
    if policy=="VETERAN":return veteran.choose_veteran_action(state)
    return engine.choose_player_action(state,policy)

def fight_one(candidate_key,arm_name,loadout,root,rep,policy,i):
    item_ids=EQUIPMENT["simulation_loadouts"][loadout][STAGE]
    player,meta=engine.build_player(STAGE,root,item_ids,EQUIPMENT)
    monster=build_monster_actor(candidate_key)
    compiled=engine.compile_build(root,engine.normalize_paths(rep["paths"]),TECHNIQUES)
    compiled=apply_arm(compiled,root,arm_name)
    prof=profile(candidate_key)
    state=engine.FightState(
      player=player,monster=monster,player_root=root,stage=STAGE,tier="T0",
      player_basic_dice=engine.STAGES[STAGE]["basic_attack"],
      tech_scalar=engine.STAGES[STAGE]["tech_scalar"],compiled=compiled,
      monster_profile=prof,signal_bridge=engine.LabSignalBridge(),
      equipment_effects=meta["equipment_effects"]
    )
    rng=random.Random(seed(candidate_key,loadout,root,rep["coverage_id"],policy,i))
    initial_qi=player.qi
    aoe_id=engine.ROOT_TECHNIQUES[root][2]
    unit_id=engine.ROOT_TECHNIQUES[root][0]
    while player.alive() and monster.alive() and state.round_no<150:
        state.round_no+=1
        engine.player_turn_start(state,rng)
        if not player.alive():break
        action=choose_action(state,policy)
        if action==veteran.VETERAN_BASIC:
            engine.execute_basic(state,rng)
        else:
            c=compiled[action]
            if not engine.execute_player_technique(state,rng,c):
                engine.execute_basic(state,rng)
        if not monster.alive():break
        engine.monster_turn_start(state,rng)
        if not monster.alive():break
        engine.execute_monster_turn(state,rng)
        engine.end_round(state)
    return {
      "win":monster.hp<=0 and player.hp>0,
      "timeout":state.round_no>=150 and player.alive() and monster.alive(),
      "rounds":state.round_no,
      "hp_final_pct":max(0.0,player.hp)/player.hp_max,
      "qi_final":max(0.0,player.qi),
      "qi_spent":state.metrics.qi_spent,
      "basic_usage":state.metrics.basic_usage,
      "aoe_usage":state.metrics.skill_usage.get(aoe_id,0),
      "unit_usage":state.metrics.skill_usage.get(unit_id,0),
      "monster_basic_usage":state.metrics.monster_attempts,
    }

def worker(args):
    candidate_key,arm_name,loadout,root,rep,policy,fights=args
    rows=[fight_one(candidate_key,arm_name,loadout,root,rep,policy,i) for i in range(fights)]
    return {
      "candidate_key":candidate_key,
      "candidate_id":CANDIDATES[candidate_key]["candidate_id"],
      "arm":arm_name,"loadout":loadout,"root":root,"policy":policy,
      "skill_rep":rep["coverage_id"],"fights":fights,
      "win_rate":sum(x["win"] for x in rows)/fights,
      "timeout_rate":sum(x["timeout"] for x in rows)/fights,
      "rounds_mean":statistics.fmean(x["rounds"] for x in rows),
      "hp_final_pct_mean":statistics.fmean(x["hp_final_pct"] for x in rows),
      "qi_final_mean":statistics.fmean(x["qi_final"] for x in rows),
      "qi_spent_mean":statistics.fmean(x["qi_spent"] for x in rows),
      "basic_usage_mean":statistics.fmean(x["basic_usage"] for x in rows),
      "aoe_usage_mean":statistics.fmean(x["aoe_usage"] for x in rows),
      "unit_usage_mean":statistics.fmean(x["unit_usage"] for x in rows),
      "monster_basic_usage_mean":statistics.fmean(x["monster_basic_usage"] for x in rows),
    }

def weighted(rows,key):
    n=sum(r["fights"] for r in rows)
    return sum(r[key]*r["fights"] for r in rows)/n

def breakdown(rows,key):
    g=defaultdict(list)
    for r in rows:g[r[key]].append(r)
    vals={k:weighted(v,"win_rate") for k,v in g.items()}
    return vals,max(vals.values())-min(vals.values())

def summarize(candidate_key,arm_name,rows):
    pb,ps=breakdown(rows,"policy")
    rb,rs=breakdown(rows,"root")
    lb,ls=breakdown(rows,"loadout")
    flags=[]
    if weighted(rows,"timeout_rate")>0.02:flags.append("TIMEOUT_GT_2PCT")
    if ps>0.75:flags.append("POLICY_POLARIZATION_GT_75PP")
    if rs>0.75:flags.append("ROOT_POLARIZATION_GT_75PP")
    if ls>0.75:flags.append("LOADOUT_POLARIZATION_GT_75PP")
    cls="OUTLIER" if flags else "REVIEW" if max(ps,rs,ls)>0.50 else "CLEAN"
    return {
      "candidate_key":candidate_key,"candidate_id":CANDIDATES[candidate_key]["candidate_id"],
      "arm":arm_name,"screen_class":cls,"flags":flags,
      "fights":sum(r["fights"] for r in rows),
      "win_rate":weighted(rows,"win_rate"),
      "policy_breakdown":pb,"policy_win_spread":ps,
      "root_breakdown":rb,"root_win_spread":rs,
      "loadout_breakdown":lb,"loadout_win_spread":ls,
      "player_hp_pressure":1-weighted(rows,"hp_final_pct_mean"),
      "rounds_mean":weighted(rows,"rounds_mean"),
      "qi_final_mean":weighted(rows,"qi_final_mean"),
      "qi_spent_mean":weighted(rows,"qi_spent_mean"),
      "basic_usage_mean":weighted(rows,"basic_usage_mean"),
      "aoe_usage_mean":weighted(rows,"aoe_usage_mean"),
      "unit_usage_mean":weighted(rows,"unit_usage_mean"),
    }

def run(candidate_key,arm_names,fights=60,workers=2):
    tasks=[]
    for arm in arm_names:
      for loadout in LOADOUTS:
       for root in ROOTS:
        for rep in skill_reps(root,3):
         for policy in POLICIES:
          tasks.append((candidate_key,arm,loadout,root,rep,policy,fights))
    rows=[]
    with ProcessPoolExecutor(max_workers=workers) as ex:
        fs=[ex.submit(worker,t) for t in tasks]
        for f in as_completed(fs):rows.append(f.result())
    by=defaultdict(list)
    for r in rows:by[(r["candidate_key"],r["arm"])].append(r)
    sums=[summarize(k,a,v) for (k,a),v in sorted(by.items())]
    return sums,rows

def main():
    out=Path(EXPERIMENT);out.mkdir(exist_ok=True)
    summaries=[];contexts=[]
    s,c=run("b06_selected",tuple(ARMS),60,2);summaries+=s;contexts+=c
    for ck in ("b08_softer","b10_defense_heavy"):
        s,c=run(ck,("BASELINE",),60,2);summaries+=s;contexts+=c

    base=next(x for x in summaries if x["candidate_key"]=="b06_selected" and x["arm"]=="BASELINE")
    for x in summaries:
        x["delta_policy_spread_vs_selected_baseline_pp"]=(x["policy_win_spread"]-base["policy_win_spread"])*100
        x["delta_aoe_win_vs_selected_baseline_pp"]=(
            x["policy_breakdown"].get("AOE_FIRST",0)-base["policy_breakdown"].get("AOE_FIRST",0)
        )*100
        x["delta_veteran_win_vs_selected_baseline_pp"]=(
            x["policy_breakdown"].get("VETERAN",0)-base["policy_breakdown"].get("VETERAN",0)
        )*100

    manifest={
      "experiment":EXPERIMENT,"status":"LAB_COMPLETE_NOT_CANON",
      "source_head":"823bc7a0ea89e6423cfae4835ec4c593736691dd",
      "selected_candidate":"eco_caido-b06-a11ec42a75",
      "fights_total":sum(x["fights"] for x in summaries),
      "common_random_numbers":True,
      "arms":ARMS,
      "guards":{
        "canonical_write":False,"main_used":False,"merge_performed":False,
        "t1_t4_executed":False,"target_win_rate_objective_used":False,
        "unique_status_changed":False
      }
    }
    payload={"manifest":manifest,"summaries":summaries}
    (out/"SUMMARY.json").write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    with (out/"context_aggregates.jsonl").open("w",encoding="utf-8") as f:
        for r in sorted(contexts,key=lambda x:(x["candidate_key"],x["arm"],x["loadout"],x["root"],x["skill_rep"],x["policy"])):
            f.write(json.dumps(r,ensure_ascii=False,sort_keys=True)+"\n")

    md=["# Eco del Caído — causal policy micro-lab","",f"Total fights: **{manifest['fights_total']:,}**",""]
    for x in summaries:
        md.append(
          f"- {x['candidate_key']} / {x['arm']}: **{x['screen_class']}**; "
          f"policy spread {x['policy_win_spread']:.2%}; AOE_FIRST {x['policy_breakdown'].get('AOE_FIRST',0):.2%}; "
          f"VETERAN {x['policy_breakdown'].get('VETERAN',0):.2%}; Qi spent {x['qi_spent_mean']:.2f}; "
          f"AOE uses {x['aoe_usage_mean']:.2f}."
        )
    (out/"SUMMARY.md").write_text("\n".join(md)+"\n",encoding="utf-8")

    zp=Path(f"RESULTADOS_{EXPERIMENT}.zip")
    with zipfile.ZipFile(zp,"w",zipfile.ZIP_DEFLATED) as z:
        for p in sorted(out.rglob("*")):
            if p.is_file():z.write(p,p.relative_to(out.parent))
    print(json.dumps({"zip":str(zp),"manifest":manifest,"summaries":summaries},ensure_ascii=False,indent=2))

if __name__=="__main__":main()
