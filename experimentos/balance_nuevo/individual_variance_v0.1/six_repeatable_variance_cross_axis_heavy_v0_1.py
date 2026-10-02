from __future__ import annotations

from collections import defaultdict, deque
from concurrent.futures import ProcessPoolExecutor, as_completed
from copy import deepcopy
from pathlib import Path
import hashlib, json, math, random, statistics, sys, zipfile

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
STAGE1=ROOT/"stage1_integral_t0_optuna"
for p in (str(ROOT),str(STAGE1)):
    if p not in sys.path:
        sys.path.insert(0,p)

import etapa19b_combat_engine as engine
import etapa19_skill_buildspace as skillspace
import player_policy_veteran as veteran

EXPERIMENT="SIX_REPEATABLE_VARIANCE_CROSS_AXIS_HEAVY_V01"
MASTER_SEED=20261001
POLICIES=("VETERAN","UNITARGET_FIRST","DEFENSE_OPEN","ROTATION","AOE_FIRST")
GATE_POLICIES={"VETERAN","UNITARGET_FIRST","DEFENSE_OPEN"}
LOADOUTS=("MANDATORY_ENTRY","EXPECTED_STAGE","HIGH_ROLL_STRESS")
ROOTS=tuple(engine.ROOT_TECHNIQUES)
MAX_ROUNDS=150

# Per species: 5k floor T0 + 5k floor T4 + 25k natural T0 + 25k natural T4
# + 5k conditional-mutant T0 + 5k conditional-mutant T4 = 70k.
COUNTS={
    "FLOOR_T0":5000,
    "FLOOR_T4":5000,
    "NATURAL_T0":25000,
    "NATURAL_T4":25000,
    "MUTANT_T0":5000,
    "MUTANT_T4":5000,
}

PROPOSAL=json.loads((HERE/"SIX_REPEATABLE_VARIANCE_ENVELOPE_PROPOSAL_V0_1.json").read_text(encoding="utf-8"))
ADAPTIVE=json.loads((ROOT/"monster_adaptive_six_v0.1/MONSTER_ADAPTIVE_SIX_CONTRACT_V0_1.json").read_text(encoding="utf-8"))
REGISTRY=json.loads((ROOT/"monster_arc1_registry.json").read_text(encoding="utf-8"))
EQUIPMENT=json.loads((ROOT/"equipment_arc1_catalog.json").read_text(encoding="utf-8"))
TECHNIQUES=json.loads((ROOT/"techniques_arc1_catalog.json").read_text(encoding="utf-8"))
VAR_BASE=json.loads((HERE/"monster_individual_variance_v0.1.json").read_text(encoding="utf-8"))

IDS=tuple(PROPOSAL["scope"]["include"])

def _seed(*parts):
    s="|".join([str(MASTER_SEED),*(str(x) for x in parts)])
    return int.from_bytes(hashlib.sha256(s.encode()).digest()[:8],"big")

def _dice_mean(s):
    total=0.0
    import re
    for token in re.findall(r"[+-]?[^+-]+",s.replace(" ","")):
        sign=-1 if token.startswith("-") else 1
        body=token[1:] if token[:1] in "+-" else token
        if "d" in body.lower():
            n_s,sides_s=body.lower().split("d",1)
            n=int(n_s) if n_s else 1
            sides=int(sides_s)
            total+=sign*n*(sides+1)/2
        else:
            total+=sign*int(body)
    return total

def _numeric_features(obj,prefix=""):
    out={}
    if isinstance(obj,dict):
        for k,v in obj.items():
            if k in {"choices","families","technique_id","name","root","role","targeting","model"}:
                continue
            out.update(_numeric_features(v,f"{prefix}.{k}" if prefix else k))
    elif isinstance(obj,(list,tuple)):
        for i,v in enumerate(obj):
            out.update(_numeric_features(v,f"{prefix}[{i}]"))
    elif isinstance(obj,(int,float)) and not isinstance(obj,bool):
        x=float(obj)
        if math.isfinite(x):
            out[prefix]=x
    return out

def _farthest(rows,k):
    if len(rows)<=k:
        return rows
    keys=sorted({key for row in rows for key in row["features"]})
    mins={key:min(r["features"].get(key,0.0) for r in rows) for key in keys}
    maxs={key:max(r["features"].get(key,0.0) for r in rows) for key in keys}
    def vec(r):
        return tuple(
            0.0 if maxs[key]<=mins[key]
            else (r["features"].get(key,0.0)-mins[key])/(maxs[key]-mins[key])
            for key in keys
        )
    vs=[vec(r) for r in rows]
    centroid=tuple(statistics.fmean(v[j] for v in vs) for j in range(len(keys)))
    def dist(a,b):
        return math.sqrt(sum((x-y)**2 for x,y in zip(a,b)))
    first=min(range(len(rows)),key=lambda i:(dist(vs[i],centroid),rows[i]["signature"]))
    chosen=[first]
    while len(chosen)<k:
        nxt=max(
            (i for i in range(len(rows)) if i not in chosen),
            key=lambda i:min(dist(vs[i],vs[j]) for j in chosen)
        )
        chosen.append(nxt)
    return [rows[i] for i in chosen]

_REPS={}
def _skill_reps(stage,root,k=2):
    key=(stage,root,k)
    if key in _REPS:
        return _REPS[key]
    points=skillspace.STAGES[stage]["points"]
    builds=[b for b in skillspace.enumerate_skill_builds(root,stage) if b.points_spent==points]
    rows=[]
    for b in builds:
        paths={x.technique_id:x.choices for x in b.paths}
        comp=engine.compile_build(root,paths,TECHNIQUES)
        feats={}
        for tid,c in sorted(comp.items()):
            for fk,fv in _numeric_features(c).items():
                feats[f"{tid}:{fk}"]=fv
        rows.append({"signature":b.signature,"paths":paths,"features":feats})
    reps=_farthest(rows,k)
    for i,r in enumerate(reps):
        r["coverage_id"]=f"SKILL_COVERAGE_{i}"
    _REPS[key]=reps
    return reps

def _lerp_int(a,b,q):
    return int(round(a+q*(b-a)))

def _discrete(ladder,q):
    if len(ladder)==1:
        return ladder[0]
    return ladder[min(len(ladder)-1,int(q*len(ladder)))]

def _axis_names(spec):
    axes=[]
    for k in ("hp","defense","evasion","precision","tenacity"):
        if spec["base"][k] != spec["upper_envelope"][k]:
            axes.append(k)
    for k,v in spec["attacks"].items():
        if len(v["ladder"])>1:
            axes.append(k)
    return axes

def _threshold(spec):
    n=len(_axis_names(spec))
    return VAR_BASE["mutant"]["threshold_by_variable_axis_count"][str(n)]

def _draw_qs(spec,rng,conditional_mutant=False):
    axes=_axis_names(spec)
    threshold=_threshold(spec)
    while True:
        q={a:rng.random() for a in axes}
        score=sum(q.values())/len(axes) if axes else 0.0
        if not conditional_mutant or score>=threshold:
            return q,score,threshold

def _instantiate(sid,mode,seed):
    spec=PROPOSAL["species"][sid]
    reg=REGISTRY["profiles"][sid]
    if mode=="FLOOR":
        return deepcopy(reg),False,0.0,None,{}
    rng=random.Random(seed)
    conditional=(mode=="MUTANT")
    q,score,threshold=_draw_qs(spec,rng,conditional_mutant=conditional)
    p=deepcopy(reg)
    for k in ("hp","defense","evasion","precision","tenacity"):
        a=spec["base"][k];b=spec["upper_envelope"][k]
        p["stats"][k]=a if a==b else _lerp_int(a,b,q[k])
    p["stats"]["basic_damage"]=_discrete(spec["attacks"]["basic_damage"]["ladder"],q.get("basic_damage",0.0))

    tech=spec["fixed_technique"]
    params=p["technique"]["params"]
    if "technique_direct_damage" in spec["attacks"]:
        params["direct_damage"]=_discrete(
            spec["attacks"]["technique_direct_damage"]["ladder"],
            q.get("technique_direct_damage",0.0)
        )
    if "burn_damage" in spec["attacks"] and "burn" in params:
        params["burn"]["damage"]=_discrete(
            spec["attacks"]["burn_damage"]["ladder"],
            q.get("burn_damage",0.0)
        )
    if "burn_ticks" in spec["attacks"] and "burn" in params:
        params["burn"]["ticks"]=_discrete(
            spec["attacks"]["burn_ticks"]["ladder"],
            q.get("burn_ticks",0.0)
        )
    params["cadence"]=tech["cadence"]
    if "qi_drain" in tech:
        params["qi_drain"]=tech["qi_drain"]

    mutant=(score>=threshold) if threshold is not None else False
    if conditional and not mutant:
        raise AssertionError("conditional mutant sampler returned non-mutant")
    return p,mutant,score,threshold,q

def _actor(profile):
    s=profile["stats"]
    return engine.Actor(
        hp_max=float(s["hp"]),hp=float(s["hp"]),qi_max=0.0,qi=0.0,
        precision=float(s["precision"]),evasion=float(s["evasion"]),
        defense=float(s["defense"]),tenacity=float(s["tenacity"]),
        control=float(s["control"]),crit_chance=float(s["crit_chance"]),
        crit_damage=float(s["crit_damage"])
    )

def _category(c,basic=False):
    if basic:
        return "PLAYER_BASIC"
    if c.get("role")=="DEFENSIVE":
        return "PLAYER_DEFENSIVE_TECHNIQUE"
    if c.get("targeting")=="AOE":
        return "PLAYER_AOE_TECHNIQUE"
    return "PLAYER_UNITARGET_TECHNIQUE"

def _recognize(memory):
    visible=[x for x in list(memory)[-2:] if x["result"]=="EFECTIVA"]
    if len(visible)<2:
        return None
    cat=visible[-1]["category"]
    return cat if all(x["category"]==cat for x in visible[-2:]) else None

def _t1_from_contract(sid):
    a=ADAPTIVE["species"][sid]["t1"]["ability"]
    out={"kind":a["kind"],"cooldown":int(a["cooldown_rounds"])}
    if a["kind"]=="EVADE_NEXT":
        out["evasion_bonus"]=float(a["evasion_bonus"])
    elif a["kind"]=="MITIGATE_NEXT":
        out["damage_reduction_pct"]=float(a["damage_reduction_pct"])
    elif a["kind"]=="DEFENSE_UP":
        out["defense_bonus"]=float(a["defense_bonus"])
    else:
        raise ValueError(a["kind"])
    return out

def _activate_survival(state,t1):
    if t1["kind"]=="EVADE_NEXT":
        state.monster_survival={"kind":"EVADE_NEXT","evasion_bonus":t1["evasion_bonus"]}
    elif t1["kind"]=="MITIGATE_NEXT":
        state.monster_survival={"kind":"MITIGATE_NEXT","damage_reduction_pct":t1["damage_reduction_pct"]}
    elif t1["kind"]=="DEFENSE_UP":
        state.monster_survival={"kind":"DEFENSE_UP","defense_bonus":t1["defense_bonus"]}
    else:
        raise ValueError(t1)
    state.monster_survival_cd=t1["cooldown"]

def _execute_t0_technique(state,rng):
    profile=state.monster_profile
    tech=profile["technique"]
    params=tech["params"]
    direct=params.get("direct_damage")
    connected=True
    if direct:
        connected=engine.resolve_monster_direct(state,rng,direct)["hit"]
    else:
        state.metrics.monster_attempts+=1
        precision=state.monster.effective("precision")+float(params.get("precision_mod",0))
        connected=rng.random()<engine.clamp(
            precision-engine._player_dynamic_evasion(state),5,100
        )/100
        if connected:
            state.metrics.monster_hits+=1
        else:
            state.metrics.player_evades+=1
    if connected and state.player.alive():
        dot=params.get("poison") or params.get("burn")
        if dot:
            state.player.dots.append({
                "family":"MONSTER_DOT","source":profile["id"],
                "dice":dot["damage"],"mult":1.0,"ticks_left":int(dot["ticks"])
            })
        q=float(params.get("qi_drain",0))
        if q>0:
            amt=min(state.player.qi,q)
            state.player.qi-=amt
            state.metrics.qi_drained+=amt
    state.monster_recent_actions.append("TECHNIQUE")

def _choose_action(state,policy):
    if policy=="VETERAN":
        return veteran.choose_veteran_action(state)
    return engine.choose_player_action(state,policy)

def _fight(sid,arm,index):
    stage=REGISTRY["profiles"][sid]["native_stage"]
    mode="FLOOR" if arm.startswith("FLOOR") else "MUTANT" if arm.startswith("MUTANT") else "NATURAL"
    tier="T4" if arm.endswith("T4") else "T0"
    rng_context=random.Random(_seed("ctx",sid,arm,index))
    loadout=LOADOUTS[index % len(LOADOUTS)]
    root=ROOTS[(index // len(LOADOUTS)) % len(ROOTS)]
    reps=_skill_reps(stage,root,2)
    rep=reps[(index // (len(LOADOUTS)*len(ROOTS))) % len(reps)]
    policy=POLICIES[(index // (len(LOADOUTS)*len(ROOTS)*len(reps))) % len(POLICIES)]

    profile,mutant,score,threshold,q=_instantiate(sid,mode,_seed("var",sid,arm,index))
    item_ids=EQUIPMENT["simulation_loadouts"][loadout][stage]
    player,meta=engine.build_player(stage,root,item_ids,EQUIPMENT)
    monster=_actor(profile)
    compiled=engine.compile_build(root,engine.normalize_paths(rep["paths"]),TECHNIQUES)
    state=engine.FightState(
        player=player,monster=monster,player_root=root,stage=stage,tier=tier,
        player_basic_dice=engine.STAGES[stage]["basic_attack"],
        tech_scalar=engine.STAGES[stage]["tech_scalar"],compiled=compiled,
        monster_profile=profile,signal_bridge=engine.LabSignalBridge(),
        equipment_effects=meta["equipment_effects"]
    )
    rng=random.Random(_seed("fight",sid,arm,index))
    memory=deque(maxlen=3)
    t4_cd=0
    t1=_t1_from_contract(sid)
    t4_cooldown=int(ADAPTIVE["species"][sid]["t4"]["cooldown_rounds"])
    tele={"survival":0,"recognition":0,"confirmed":0,"counter":0,"t4":0}

    while player.alive() and monster.alive() and state.round_no<MAX_ROUNDS:
        state.round_no+=1
        engine.player_turn_start(state,rng)
        if not player.alive():
            break

        predicted=_recognize(memory) if tier=="T4" else None
        if predicted:
            tele["recognition"]+=1

        aid=_choose_action(state,policy)
        hp_before=monster.hp
        def_before=state.metrics.monster_def_prevented
        abs_before=state.metrics.monster_absorbed
        surv_before=deepcopy(state.monster_survival)

        if aid==veteran.VETERAN_BASIC:
            cat="PLAYER_BASIC"
            engine.execute_basic(state,rng)
            executed=True
            defensive=False
        else:
            c=compiled[aid]
            cat=_category(c)
            defensive=c.get("role")=="DEFENSIVE"
            executed=engine.execute_player_technique(state,rng,c)
            if not executed:
                engine.execute_basic(state,rng)
                cat="PLAYER_BASIC"
                defensive=False

        actual=max(0.0,hp_before-monster.hp)
        effective=(actual>0) or (executed and defensive)
        memory.append({"category":cat,"result":"EFECTIVA" if effective else "FALLIDA"})
        if predicted and predicted==cat and effective:
            tele["confirmed"]+=1

        if tier=="T4" and predicted and predicted==cat and cat!="PLAYER_DEFENSIVE_TECHNIQUE" and surv_before and player.alive() and monster.alive():
            causal=False
            if surv_before["kind"]=="EVADE_NEXT":
                causal=(actual<=0)
            elif surv_before["kind"]=="MITIGATE_NEXT":
                causal=(actual>0)
            elif surv_before["kind"]=="DEFENSE_UP":
                causal=(actual>0 and state.metrics.monster_def_prevented>def_before)
            if causal:
                engine.resolve_monster_direct(state,rng,state.monster_profile["stats"]["basic_damage"])
                tele["counter"]+=1
                if not player.alive():
                    break

        if not monster.alive():
            break
        engine.monster_turn_start(state,rng)
        if not monster.alive():
            break

        if tier=="T4":
            low=(monster.hp/max(1.0,monster.hp_max))<=0.35
            heavy=(actual/max(1.0,monster.hp_max))>=0.20
            can_survive=(state.monster_survival_cd<=0 and state.monster_survival is None)
            preempt=bool(predicted)
            if can_survive and (low or heavy or preempt):
                _activate_survival(state,t1)
                tele["survival"]+=1
            elif t4_cd<=0:
                _execute_t0_technique(state,rng)
                tele["t4"]+=1
                t4_cd=t4_cooldown
            else:
                engine.execute_monster_turn(state,rng)
        else:
            engine.execute_monster_turn(state,rng)

        engine.end_round(state)
        if t4_cd>0:
            t4_cd-=1

    win=monster.hp<=0 and player.hp>0
    return {
        "species_id":sid,"arm":arm,"tier":tier,"loadout":loadout,"root":root,
        "policy":policy,"skill_rep":rep["coverage_id"],"win":win,
        "timeout":state.round_no>=MAX_ROUNDS and player.alive() and monster.alive(),
        "rounds":state.round_no,"hp_final_pct":max(0.0,player.hp)/player.hp_max,
        "monster_hp_final_pct":max(0.0,monster.hp)/monster.hp_max,
        "mutant":mutant,"power_score":score,"threshold":threshold,
        "q":q,"survival":tele["survival"],"recognition":tele["recognition"],
        "confirmed":tele["confirmed"],"counter":tele["counter"],"t4":tele["t4"],
    }

def _worker(args):
    sid,arm,start,count=args
    rows=[_fight(sid,arm,start+i) for i in range(count)]
    return rows

def _weighted(rows,key):
    return statistics.fmean(float(r[key]) for r in rows) if rows else 0.0

def _spread(rows,key,policy_filter=None):
    groups=defaultdict(list)
    for r in rows:
        if policy_filter and r["policy"] not in policy_filter:
            continue
        groups[r[key]].append(r)
    vals={k:sum(x["win"] for x in v)/len(v) for k,v in groups.items()}
    return vals,(max(vals.values())-min(vals.values()) if vals else 0.0)

def _summary(sid,arm,rows):
    pb,ps=_spread(rows,"policy")
    gpb,gps=_spread(rows,"policy",GATE_POLICIES)
    rb,rs=_spread(rows,"root")
    lb,ls=_spread(rows,"loadout")
    mutants=sum(1 for r in rows if r["mutant"])
    return {
        "species_id":sid,"arm":arm,"fights":len(rows),
        "player_win_rate":sum(r["win"] for r in rows)/len(rows),
        "timeout_rate":sum(r["timeout"] for r in rows)/len(rows),
        "rounds_mean":_weighted(rows,"rounds"),
        "player_hp_pressure":1-_weighted(rows,"hp_final_pct"),
        "monster_hp_final_pct_mean":_weighted(rows,"monster_hp_final_pct"),
        "mutant_rate":mutants/len(rows),
        "power_score_mean":_weighted(rows,"power_score"),
        "policy_breakdown":pb,"policy_spread_all":ps,
        "gate_policy_breakdown":gpb,"gate_policy_spread":gps,
        "root_breakdown":rb,"root_spread":rs,
        "loadout_breakdown":lb,"loadout_spread":ls,
        "survival_mean":_weighted(rows,"survival"),
        "counter_mean":_weighted(rows,"counter"),
        "t4_mean":_weighted(rows,"t4"),
    }

def main():
    out=Path(EXPERIMENT);out.mkdir(exist_ok=True)
    tasks=[]
    chunk=250
    for sid in IDS:
        for arm,total in COUNTS.items():
            for start in range(0,total,chunk):
                tasks.append((sid,arm,start,min(chunk,total-start)))

    rows=[]
    with ProcessPoolExecutor(max_workers=4) as ex:
        futs=[ex.submit(_worker,t) for t in tasks]
        for f in as_completed(futs):
            rows.extend(f.result())

    grouped=defaultdict(list)
    for r in rows:
        grouped[(r["species_id"],r["arm"])].append(r)
    summaries=[_summary(s,a,v) for (s,a),v in sorted(grouped.items())]

    # Relative diagnostics against same-tier floor.
    by={(x["species_id"],x["arm"]):x for x in summaries}
    for x in summaries:
        sid=x["species_id"]
        floor="FLOOR_T4" if x["arm"].endswith("T4") else "FLOOR_T0"
        b=by[(sid,floor)]
        x["delta_win_vs_floor_pp"]=(x["player_win_rate"]-b["player_win_rate"])*100
        x["delta_pressure_vs_floor_pp"]=(x["player_hp_pressure"]-b["player_hp_pressure"])*100
        x["delta_rounds_vs_floor"]=x["rounds_mean"]-b["rounds_mean"]

    # Mutant incidence is meaningful only in NATURAL arms.
    natural_rates={}
    for sid in IDS:
        n=[r for r in rows if r["species_id"]==sid and r["arm"] in {"NATURAL_T0","NATURAL_T4"}]
        natural_rates[sid]=sum(r["mutant"] for r in n)/len(n)

    manifest={
        "experiment":EXPERIMENT,
        "status":"COMPLETE_LAB_NOT_RATIFIED",
        "source_head":"45c3a9c240ea74208a0d8fd4d5be187bc817df35",
        "species":list(IDS),
        "total_fights":len(rows),
        "counts_per_species":COUNTS,
        "natural_mutant_rates":natural_rates,
        "guards":{
            "canonical_write":False,
            "unique_species_executed":False,
            "below_t0_variance":False,
            "main_used":False,
            "merge_performed":False,
            "target_win_rate_objective_used":False,
            "t5_exists":False
        }
    }

    # Hard mechanical guards.
    assert all(rate<VAR_BASE["mutant"]["maximum_incidence"] for rate in natural_rates.values()),natural_rates
    assert not any(r["species_id"] in PROPOSAL["scope"]["excluded_unique"] for r in rows)
    assert all(x["timeout_rate"]<=0.02 for x in summaries)

    payload={"manifest":manifest,"summaries":summaries}
    (out/"SUMMARY.json").write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    with (out/"fight_rows.jsonl").open("w",encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r,ensure_ascii=False,sort_keys=True)+"\n")

    md=["# Six repeatable variance cross-axis heavy v0.1","",f"Total fights: **{len(rows):,}**",""]
    for sid in IDS:
        md.append(f"## {sid}")
        for arm in COUNTS:
            x=by[(sid,arm)]
            md.append(
                f"- {arm}: win {x['player_win_rate']:.2%}; Δwin {x['delta_win_vs_floor_pp']:+.2f} pp; "
                f"pressure {x['player_hp_pressure']:.2%}; gate-policy spread {x['gate_policy_spread']:.2%}; "
                f"root {x['root_spread']:.2%}; loadout {x['loadout_spread']:.2%}; mutant {x['mutant_rate']:.3%}."
            )
        md.append("")
    (out/"SUMMARY.md").write_text("\n".join(md)+"\n",encoding="utf-8")

    zp=Path(f"RESULTADOS_{EXPERIMENT}.zip")
    with zipfile.ZipFile(zp,"w",zipfile.ZIP_DEFLATED) as z:
        for p in sorted(out.rglob("*")):
            if p.is_file():
                z.write(p,p.relative_to(out.parent))
    print(json.dumps({"zip":str(zp),"manifest":manifest,"summaries":summaries},ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
