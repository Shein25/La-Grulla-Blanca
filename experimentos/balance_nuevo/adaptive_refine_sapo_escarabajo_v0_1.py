from __future__ import annotations
from collections import defaultdict, deque
from concurrent.futures import ProcessPoolExecutor, as_completed
from copy import deepcopy
from pathlib import Path
import hashlib, json, math, os, random, statistics, sys, zipfile

HERE=Path(__file__).resolve().parent
STAGE1=HERE/"stage1_integral_t0_optuna"
for p in (str(HERE),str(STAGE1)):
    if p not in sys.path: sys.path.insert(0,p)

import etapa19b_combat_engine as engine
import etapa19_skill_buildspace as skillspace
import player_policy_veteran as veteran

EXPERIMENT="REFINEMENT_SAPO_ESCARABAJO_T1_T4_V01"
MASTER_SEED=20261001
POLICIES=("VETERAN","UNITARGET_FIRST","AOE_FIRST","DEFENSE_OPEN","ROTATION")
LOADOUTS=("MANDATORY_ENTRY","EXPECTED_STAGE","HIGH_ROLL_STRESS")
ROOTS=tuple(engine.ROOT_TECHNIQUES)
T2_WINDOW=2
T2_REQUIRED=2

SPECS={
 "sapo_ceniza":{
  "stage":"LianQi_II",
  "role":"NORMAL",
  "stats":{"hp":49,"qi_max":None,"precision":97,"evasion":11,"defense":0,"tenacity":5,"control":0,"crit_chance":5,"crit_damage":1.5,"basic_damage":"1d2+5"},
  "technique":{"name":"Nube de Hollín","mechanics":["DIRECT_DAMAGE","BURN_DOT"],"params":{"cadence":3,"direct_damage":"1d2+4","burn":{"damage":"1d2+2","ticks":3}}},
 },
 "escarabajo_hierro":{
  "stage":"LianQi_II",
  "role":"TANK",
  "stats":{"hp":75,"qi_max":None,"precision":90,"evasion":14,"defense":2,"tenacity":24,"control":0,"crit_chance":5,"crit_damage":1.5,"basic_damage":"1d2+3"},
  "technique":{"name":"Carga de Caparazón","mechanics":["DIRECT_DAMAGE"],"params":{"cadence":3,"direct_damage":"1d2+8"}},
 },
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
            for fk,fv in numeric_features(c).items(): feats[f"{tid}:{fk}"]=fv
        rows.append({"signature":b.signature,"paths":paths,"features":feats})
    reps=farthest(rows,k)
    for i,r in enumerate(reps):r["coverage_id"]=f"SKILL_COVERAGE_{i}"
    _REPS[key]=reps
    return reps

def lab_profile(sid):
    s=SPECS[sid]
    return {
      "id":sid,"name":sid,"native_stage":s["stage"],"native_stage_index":2,
      "role":s["role"],"region":"LAB","element":None,"unique":False,
      "engine_contract":"NEW_COMBAT_STATS_V0_1","stats_status":"LAB_CANDIDATE",
      "stats":deepcopy(s["stats"]),
      "technique":{"name":s["technique"]["name"],"mechanics":deepcopy(s["technique"]["mechanics"]),"params_status":"LAB_CANDIDATE","params":deepcopy(s["technique"]["params"])},
      "ai":{"cognition":"LAB","social":"LAB"},"adaptive":{"status":"LAB"},"resource_model":"NONE",
    }

def monster_actor(sid):
    s=SPECS[sid]["stats"]
    return engine.Actor(hp_max=float(s["hp"]),hp=float(s["hp"]),qi_max=math.nan,qi=math.nan,
        precision=float(s["precision"]),evasion=float(s["evasion"]),defense=float(s["defense"]),
        tenacity=float(s["tenacity"]),control=0.0,crit_chance=5.0,crit_damage=1.5)

def category(c,basic=False):
    if basic:return "PLAYER_BASIC"
    if c.get("role")=="DEFENSIVE":return "PLAYER_DEFENSIVE_TECHNIQUE"
    if c.get("targeting")=="AOE":return "PLAYER_AOE_TECHNIQUE"
    return "PLAYER_UNITARGET_TECHNIQUE"

def recognize(memory):
    visible=[x for x in list(memory)[-T2_WINDOW:] if x["result"]=="EFECTIVA"]
    if len(visible)<T2_REQUIRED:return None
    tail=visible[-T2_REQUIRED:];cat=tail[-1]["category"]
    return cat if all(x["category"]==cat for x in tail) else None

def activate_survival(state,t1):
    if t1["kind"]=="MITIGATE_NEXT":
        state.monster_survival={"kind":"MITIGATE_NEXT","damage_reduction_pct":float(t1["value"])}
    elif t1["kind"]=="DEFENSE_UP":
        state.monster_survival={"kind":"DEFENSE_UP","defense_bonus":float(t1["value"])}
    else:raise ValueError(t1)
    state.monster_survival_cd=5

def execute_t0_technique(state,rng):
    p=state.monster_profile;params=p["technique"]["params"];connected=True
    direct=params.get("direct_damage")
    if direct:
        connected=engine.resolve_monster_direct(state,rng,direct)["hit"]
    else:
        state.metrics.monster_attempts+=1
        precision=state.monster.effective("precision")+float(params.get("precision_mod",0))
        connected=rng.random()<engine.clamp(precision-engine._player_dynamic_evasion(state),5,100)/100
        if connected:state.metrics.monster_hits+=1
        else:state.metrics.player_evades+=1
    if connected and state.player.alive():
        dot=params.get("poison") or params.get("burn")
        if dot:state.player.dots.append({"family":"MONSTER_DOT","source":p["id"],"dice":dot["damage"],"mult":1.0,"ticks_left":int(dot["ticks"])})
        q=float(params.get("qi_drain",0))
        if q>0:
            amt=min(state.player.qi,q);state.player.qi-=amt;state.metrics.qi_drained+=amt
    state.monster_recent_actions.append("TECHNIQUE")

def choose_action(state,policy):
    if policy=="VETERAN":return veteran.choose_veteran_action(state)
    return engine.choose_player_action(state,policy)

def fight_one(sid,arm,loadout,root,rep,policy,i):
    spec=SPECS[sid];stage=spec["stage"]
    item_ids=EQUIPMENT["simulation_loadouts"][loadout][stage]
    player,meta=engine.build_player(stage,root,item_ids,EQUIPMENT)
    monster=monster_actor(sid)
    compiled=engine.compile_build(root,engine.normalize_paths(rep["paths"]),TECHNIQUES)
    profile=lab_profile(sid)
    state=engine.FightState(player=player,monster=monster,player_root=root,stage=stage,tier=arm["tier"],
        player_basic_dice=engine.STAGES[stage]["basic_attack"],tech_scalar=engine.STAGES[stage]["tech_scalar"],
        compiled=compiled,monster_profile=profile,signal_bridge=engine.LabSignalBridge(),equipment_effects=meta["equipment_effects"])
    rng=random.Random(seed(sid,arm["arm_id"],loadout,root,rep["coverage_id"],policy,i))
    memory=deque(maxlen=3);t4_cd=0
    stats={"survival":0,"recognition":0,"confirmed":0,"counter":0,"t4":0}
    while player.alive() and monster.alive() and state.round_no<150:
        state.round_no+=1;engine.player_turn_start(state,rng)
        if not player.alive():break
        predicted=recognize(memory) if arm["tier"] in {"T2","T3","T4"} else None
        if predicted:stats["recognition"]+=1
        aid=choose_action(state,policy)
        hp_before=monster.hp;def_before=state.metrics.monster_def_prevented;abs_before=state.metrics.monster_absorbed
        surv_before=deepcopy(state.monster_survival)
        if aid==veteran.VETERAN_BASIC:
            cat="PLAYER_BASIC";engine.execute_basic(state,rng);executed=True
        else:
            c=compiled[aid];cat=category(c);executed=engine.execute_player_technique(state,rng,c)
            if not executed:
                engine.execute_basic(state,rng);cat="PLAYER_BASIC"
        actual=max(0.0,hp_before-monster.hp)
        effective=(actual>0) or (aid!=veteran.VETERAN_BASIC and executed and compiled[aid].get("role")=="DEFENSIVE")
        memory.append({"category":cat,"result":"EFECTIVA" if effective else "FALLIDA"})
        if predicted and predicted==cat and effective:stats["confirmed"]+=1

        if arm["tier"] in {"T3","T4"} and predicted and predicted==cat and cat!="PLAYER_DEFENSIVE_TECHNIQUE" and surv_before and player.alive() and monster.alive():
            causal=False
            if surv_before["kind"]=="MITIGATE_NEXT":causal=(actual>0)
            elif surv_before["kind"]=="DEFENSE_UP":
                causal=(actual>0 and state.metrics.monster_def_prevented>def_before)
            if causal:
                engine.resolve_monster_direct(state,rng,state.monster_profile["stats"]["basic_damage"]);stats["counter"]+=1
                if not player.alive():break

        if not monster.alive():break
        engine.monster_turn_start(state,rng)
        if not monster.alive():break
        low=(monster.hp/max(1.0,monster.hp_max))<=0.35
        heavy=(actual/max(1.0,monster.hp_max))>=0.20
        can=(state.monster_survival_cd<=0 and state.monster_survival is None)
        preempt=bool(predicted) and arm["tier"] in {"T2","T3","T4"}
        if can and (low or heavy or preempt):
            activate_survival(state,arm["t1"]);stats["survival"]+=1
        else:
            if arm["tier"]=="T4" and t4_cd<=0:
                execute_t0_technique(state,rng);stats["t4"]+=1;t4_cd=int(arm["t4_cd"])
            else:
                engine.execute_monster_turn(state,rng)
        engine.end_round(state)
        if t4_cd>0:t4_cd-=1
    return {"win":monster.hp<=0 and player.hp>0,"timeout":state.round_no>=150 and player.alive() and monster.alive(),
        "rounds":state.round_no,"hp_final_pct":max(0.0,player.hp)/player.hp_max,**stats}

def worker(args):
    sid,arm,loadout,root,rep,policy,fights=args
    rows=[fight_one(sid,arm,loadout,root,rep,policy,i) for i in range(fights)]
    return {"species_id":sid,"arm_id":arm["arm_id"],"tier":arm["tier"],"loadout":loadout,"root":root,
      "policy":policy,"skill_rep":rep["coverage_id"],"fights":fights,
      "win_rate":sum(x["win"] for x in rows)/fights,"timeout_rate":sum(x["timeout"] for x in rows)/fights,
      "rounds_mean":statistics.fmean(x["rounds"] for x in rows),"hp_final_pct_mean":statistics.fmean(x["hp_final_pct"] for x in rows),
      "survival_mean":statistics.fmean(x["survival"] for x in rows),"recognition_mean":statistics.fmean(x["recognition"] for x in rows),
      "confirmed_mean":statistics.fmean(x["confirmed"] for x in rows),"counter_mean":statistics.fmean(x["counter"] for x in rows),
      "t4_mean":statistics.fmean(x["t4"] for x in rows)}

def weighted(rows,key):
    n=sum(r["fights"] for r in rows)
    return sum(r[key]*r["fights"] for r in rows)/n

def spread(rows,key):
    g=defaultdict(list)
    for r in rows:g[r[key]].append(r)
    vals={k:weighted(v,"win_rate") for k,v in g.items()}
    return vals,max(vals.values())-min(vals.values())

def summarize(arm,rows):
    rb,rs=spread(rows,"root");lb,ls=spread(rows,"loadout");pb,ps=spread(rows,"policy")
    flags=[]
    if weighted(rows,"timeout_rate")>0.02:flags.append("TIMEOUT_GT_2PCT")
    if rs>0.75:flags.append("ROOT_POLARIZATION_GT_75PP")
    if ls>0.75:flags.append("LOADOUT_POLARIZATION_GT_75PP")
    if ps>0.75:flags.append("POLICY_POLARIZATION_GT_75PP")
    hard=bool(flags)
    if not hard:
        if rs>0.50:flags.append("ROOT_SPREAD_GT_50PP")
        if ls>0.50:flags.append("LOADOUT_SPREAD_GT_50PP")
        if ps>0.50:flags.append("POLICY_SPREAD_GT_50PP")
    cls="OUTLIER" if hard else "REVIEW" if flags else "CLEAN"
    return {"arm_id":arm["arm_id"],"tier":arm["tier"],"t1":arm["t1"],"t4_cd":arm.get("t4_cd"),
      "screen_class":cls,"flags":flags,"fights":sum(r["fights"] for r in rows),
      "win_rate":weighted(rows,"win_rate"),"player_hp_pressure":1-weighted(rows,"hp_final_pct_mean"),
      "root_win_spread":rs,"loadout_win_spread":ls,"policy_win_spread":ps,
      "survival_mean":weighted(rows,"survival_mean"),"recognition_mean":weighted(rows,"recognition_mean"),
      "confirmed_mean":weighted(rows,"confirmed_mean"),"counter_mean":weighted(rows,"counter_mean"),
      "t4_mean":weighted(rows,"t4_mean"),"policy_breakdown":pb,"root_breakdown":rb,"loadout_breakdown":lb}

def run_arms(sid,arms,fights,workers=2):
    tasks=[]
    for arm in arms:
      for loadout in LOADOUTS:
       for root in ROOTS:
        for rep in skill_reps(SPECS[sid]["stage"],root,2):
         for policy in POLICIES:tasks.append((sid,arm,loadout,root,rep,policy,fights))
    rows=[]
    with ProcessPoolExecutor(max_workers=workers) as ex:
        fs=[ex.submit(worker,t) for t in tasks]
        for f in as_completed(fs):rows.append(f.result())
    by=defaultdict(list)
    for r in rows:by[r["arm_id"]].append(r)
    amap={a["arm_id"]:a for a in arms}
    return [summarize(amap[k],v) for k,v in sorted(by.items())],rows

def main():
    out=Path(EXPERIMENT);out.mkdir(exist_ok=True)
    # Phase A: directed T1.
    sapo_t1=[{"arm_id":f"sapo_T1_MIT_{v:02d}","tier":"T1","t1":{"kind":"MITIGATE_NEXT","value":v}} for v in (5,10,15,20)]
    esc_t1=[{"arm_id":"escarabajo_T1_DEF2_CONFIRM","tier":"T1","t1":{"kind":"DEFENSE_UP","value":2}}]
    sapo_a,sapo_ctx=run_arms("sapo_ceniza",sapo_t1,20)
    esc_a,esc_ctx=run_arms("escarabajo_hierro",esc_t1,40)
    # Select Sapo T1 for downstream only by robustness, never by win rate.
    eligible=[x for x in sapo_a if x["screen_class"]!="OUTLIER"]
    sapo_pick=min(eligible,key=lambda x:(x["policy_win_spread"],x["loadout_win_spread"],x["root_win_spread"]))["t1"]
    # Phase B: sequential expression + slower T4.
    def downstream(sid,t1):
        prefix="sapo" if sid=="sapo_ceniza" else "escarabajo"
        return [
          {"arm_id":f"{prefix}_T2_SELECTED","tier":"T2","t1":t1},
          {"arm_id":f"{prefix}_T3_SELECTED","tier":"T3","t1":t1},
          *[{"arm_id":f"{prefix}_T4_SELECTED_CD{cd}","tier":"T4","t1":t1,"t4_cd":cd} for cd in (8,10,12)]
        ]
    sapo_b,sapo_ctx2=run_arms("sapo_ceniza",downstream("sapo_ceniza",sapo_pick),15)
    esc_pick={"kind":"DEFENSE_UP","value":2}
    esc_b,esc_ctx2=run_arms("escarabajo_hierro",downstream("escarabajo_hierro",esc_pick),15)
    arms=[{"species_id":"sapo_ceniza",**x} for x in sapo_a+sapo_b]+[{"species_id":"escarabajo_hierro",**x} for x in esc_a+esc_b]
    contexts=sapo_ctx+sapo_ctx2+esc_ctx+esc_ctx2
    summary={"experiment":EXPERIMENT,"status":"LAB_COMPLETE_NOT_CANON","total_fights":sum(x["fights"] for x in arms),
      "sapo_selected_t1_for_downstream":sapo_pick,"escarabajo_selected_t1_for_downstream":esc_pick,
      "guards":{"canonical_write":False,"main_used":False,"merge_performed":False,"target_win_rate_objective_used":False,
        "rata_modified":False,"t5_exists":False},
      "arms":arms}
    (out/"SUMMARY.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    with (out/"arm_aggregates.jsonl").open("w",encoding="utf-8") as f:
        for r in arms:f.write(json.dumps(r,ensure_ascii=False,sort_keys=True)+"\n")
    with (out/"context_aggregates.jsonl").open("w",encoding="utf-8") as f:
        for r in contexts:f.write(json.dumps(r,ensure_ascii=False,sort_keys=True)+"\n")
    md=["# Refinement Sapo Ceniza + Escarabajo de Hierro","",f"Total fights: **{summary['total_fights']:,}**","",
        f"Sapo downstream T1 selected by stability only: {sapo_pick}.",""]
    for r in arms:
        md.append(f"- {r['species_id']} / {r['arm_id']}: **{r['screen_class']}**; policy {r['policy_win_spread']:.1%}; loadout {r['loadout_win_spread']:.1%}; root {r['root_win_spread']:.1%}.")
    (out/"SUMMARY.md").write_text("\n".join(md)+"\n",encoding="utf-8")
    zp=Path(f"RESULTADOS_{EXPERIMENT}.zip")
    with zipfile.ZipFile(zp,"w",zipfile.ZIP_DEFLATED) as z:
        for p in sorted(out.rglob("*")):
            if p.is_file():z.write(p,p.relative_to(out.parent))
    print(json.dumps({"zip":str(zp),"total_fights":summary["total_fights"],"sapo_pick":sapo_pick,
      "classes":{r["arm_id"]:r["screen_class"] for r in arms}},ensure_ascii=False,indent=2))

if __name__=="__main__":main()
