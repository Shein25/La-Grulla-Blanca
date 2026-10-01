"""Rata de Qi T1 — Reflejo de Madriguera calibration lab.

Exhaustive grid, common random numbers, no raw fight persistence.
T0 is canonical READY. T1 remains LAB-only; engine T1 gate is bypassed only
inside this scoped context manager.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from dataclasses import dataclass,asdict
import gzip
import json
import math
from pathlib import Path
import statistics
import sys
import zipfile

HERE=Path(__file__).resolve().parent
BALANCE=HERE.parent
STAGE1=BALANCE/"stage1_integral_t0_optuna"
for p in (BALANCE,STAGE1):
    if str(p) not in sys.path:
        sys.path.insert(0,str(p))

import etapa19b_combat_engine as engine
from contexts import PRIMARY_CONTEXTS,ROOTS
from monster_new_engine_guard import load_registry,require_ready_profile
from player_policy_veteran import DEFAULT_VETERAN_CONFIG,VETERAN_BASIC,choose_veteran_action
from seeds import stable_seed
from stream_aggregate import StreamingFightAggregate
from telemetry import fight_once_observed

RATA_ID="rata_qi"
LAB_STATUS="T1_REFLEJO_LAB_ONLY"
BASIC_PROXY_SENTINEL_COST=10**9
BONUSES=tuple(range(5,51,5))
COOLDOWNS=(1,2,3,4,5)
SIGNAL_ARMS={
    "EARLY":{"low_hp_ratio":0.40,"heavy_hit_ratio":0.15},
    "BASE":{"low_hp_ratio":0.30,"heavy_hit_ratio":0.20},
    "LATE":{"low_hp_ratio":0.20,"heavy_hit_ratio":0.25},
}
PRESETS={
    "smoke":{"search_fights":2,"final_cap":3,"high_fights":5},
    "overnight":{"search_fights":500,"final_cap":7,"high_fights":10000},
    "heavy":{"search_fights":1000,"final_cap":7,"high_fights":20000},
}
TECHNIQUES=engine.load_json(BALANCE/"techniques_arc1_catalog.json")
EQUIPMENT=engine.load_json(BALANCE/"equipment_arc1_catalog.json")

@dataclass(frozen=True)
class T1Config:
    evasion_bonus:int
    cooldown_rounds:int

    def validate(self):
        if self.evasion_bonus not in BONUSES:
            raise ValueError("evasion_bonus outside LAB grid")
        if self.cooldown_rounds not in COOLDOWNS:
            raise ValueError("cooldown outside LAB grid")

def paths_for(root):
    return {tid:() for tid in engine.ROOT_TECHNIQUES[root]}

@contextmanager
def _player_veteran_runtime():
    originals={
        "compile_build":engine.compile_build,
        "choose_player_action":engine.choose_player_action,
        "execute_player_technique":engine.execute_player_technique,
    }
    def compile_build(root,paths,catalog=None):
        compiled=dict(originals["compile_build"](root,paths,catalog))
        compiled[VETERAN_BASIC]={
            "technique_id":VETERAN_BASIC,"name":"Ataque básico","root":root,
            "role":"BASIC_PROXY","targeting":"UNITARGET",
            "qi_cost":BASIC_PROXY_SENTINEL_COST,
        }
        return compiled
    def choose_player_action(state,policy):
        if policy!="VETERAN":
            return originals["choose_player_action"](state,policy)
        return choose_veteran_action(state,DEFAULT_VETERAN_CONFIG)
    def execute_player_technique(state,rng,c):
        if c.get("technique_id")==VETERAN_BASIC:
            engine.execute_basic(state,rng)
            return True
        return originals["execute_player_technique"](state,rng,c)
    engine.compile_build=compile_build
    engine.choose_player_action=choose_player_action
    engine.execute_player_technique=execute_player_technique
    try:
        yield
    finally:
        for k,v in originals.items():
            setattr(engine,k,v)

@contextmanager
def _t1_reflejo_runtime(config:T1Config,arm:dict,counters:dict):
    config.validate()
    originals={
        "build_monster":engine.build_monster,
        "execute_monster_turn":engine.execute_monster_turn,
    }

    def build_monster(profile,tier):
        if profile.get("id")!=RATA_ID or tier!="T1":
            raise RuntimeError("T1 Reflejo LAB accepts only rata_qi at T1")
        # Reuse exact canonical T0 actor. No adaptive stat synthesis.
        return originals["build_monster"](profile,"T0")

    def execute_monster_turn(state,rng):
        hp_ratio=state.monster.hp/state.monster.hp_max if state.monster.hp_max else 0.0
        last_hit=float(state.last_player_hp_damage_to_monster)
        low_hp=hp_ratio<=float(arm["low_hp_ratio"])
        heavy_hit=last_hit>=float(arm["heavy_hit_ratio"])*state.monster.hp_max

        eligible=(
            state.monster.alive()
            and state.monster_survival is None
            and state.monster_survival_cd<=0
            and (low_hp or heavy_hit)
        )
        if eligible:
            state.monster_survival={
                "kind":"EVADE_NEXT",
                "evasion_bonus":float(config.evasion_bonus),
            }
            # end_round decrements immediately; +1 preserves the requested
            # number of complete future cooldown rounds.
            state.monster_survival_cd=int(config.cooldown_rounds)+1
            state.metrics.adaptation_procs+=1
            state.monster_recent_actions.append("SURVIVAL")
            counters["activations"]+=1
            counters["low_hp_signals"]+=int(low_hp)
            counters["heavy_hit_signals"]+=int(heavy_hit)
            if state.arrastre_locked:
                state.arrastre_locked=False
                state.arrastre_precision_debuff=0.0
            return
        return originals["execute_monster_turn"](state,rng)

    engine.build_monster=build_monster
    engine.execute_monster_turn=execute_monster_turn
    try:
        yield
    finally:
        for k,v in originals.items():
            setattr(engine,k,v)

def _run_once(profile,root,item_ids,seed,tier,config=None,arm=None):
    counters={"activations":0,"low_hp_signals":0,"heavy_hit_signals":0}
    kwargs=dict(
        stage="LianQi_I",root=root,item_ids=item_ids,paths=paths_for(root),
        monster_profile=profile,tier=tier,policy="VETERAN",seed=seed,
        technique_catalog=TECHNIQUES,equipment_catalog=EQUIPMENT,max_rounds=100,
    )
    with _player_veteran_runtime():
        if tier=="T0":
            row=fight_once_observed(**kwargs)
        else:
            with _t1_reflejo_runtime(config,arm,counters):
                row=fight_once_observed(
                    **kwargs,
                    signal_bridge=engine.LabSignalBridge(
                        low_hp_ratio=float(arm["low_hp_ratio"]),
                        heavy_hit_ratio=float(arm["heavy_hit_ratio"]),
                    ),
                )
    row["loadout_profile"]="UNKNOWN"
    row["t1_activations"]=counters["activations"]
    row["t1_low_hp_signals"]=counters["low_hp_signals"]
    row["t1_heavy_hit_signals"]=counters["heavy_hit_signals"]
    return row

def _evaluate(profile,tier,fights_per_context,namespace,config=None,arm=None):
    agg=StreamingFightAggregate()
    extra={
        "activations":0.0,"low_hp_signals":0.0,"heavy_hit_signals":0.0,
        "monster_evades":0.0,
    }
    for ctx in PRIMARY_CONTEXTS:
        item_ids=EQUIPMENT["simulation_loadouts"][ctx.loadout_profile]["LianQi_I"]
        for root in ROOTS:
            for i in range(int(fights_per_context)):
                seed=stable_seed("RATA_T1_REFLEJO",namespace,ctx.context_id,root,i)
                row=_run_once(profile,root,item_ids,seed,tier,config,arm)
                row["loadout_profile"]=ctx.loadout_profile
                agg.add(row)
                extra["activations"]+=row["t1_activations"]
                extra["low_hp_signals"]+=row["t1_low_hp_signals"]
                extra["heavy_hit_signals"]+=row["t1_heavy_hit_signals"]
                extra["monster_evades"]+=float(row["metrics"].get("monster_evades",0))
    out=agg.finish()
    n=float(out["fights"])
    out.update({
        "t1_activation_rate":extra["activations"]/n,
        "t1_low_hp_signal_rate":extra["low_hp_signals"]/n,
        "t1_heavy_hit_signal_rate":extra["heavy_hit_signals"]/n,
        "monster_evades_per_fight":extra["monster_evades"]/n,
    })
    return out

def _budget(cfg:T1Config):
    bonus=(cfg.evasion_bonus-min(BONUSES))/(max(BONUSES)-min(BONUSES))
    cooldown=(max(COOLDOWNS)-cfg.cooldown_rounds)/(max(COOLDOWNS)-min(COOLDOWNS))
    return (bonus+cooldown)/2.0

def _delta(t1,base):
    base_pressure=1.0-float(base["hp_final_pct_mean"])
    t1_pressure=1.0-float(t1["hp_final_pct_mean"])
    base_dmg=float(base["monster_damage_total_mean"])
    return {
        "round_extension":float(t1["rounds_mean"])-float(base["rounds_mean"]),
        "monster_evades_delta":float(t1["monster_evades_per_fight"])-float(base["monster_evades_per_fight"]),
        "player_hp_pressure_delta":t1_pressure-base_pressure,
        "monster_damage_retention":(
            float(t1["monster_damage_total_mean"])/base_dmg if base_dmg else 0.0
        ),
        "player_win_rate_delta":float(t1["win_rate"])-float(base["win_rate"]),
    }

def _compact(a):
    keys=(
        "fights","win_rate","timeout_rate","rounds_mean","hp_final_pct_mean",
        "hp_final_pct_p10","hp_min_pct_mean","monster_damage_total_mean",
        "player_hit_rate","monster_hit_rate","monster_evades_per_fight",
        "t1_activation_rate","t1_low_hp_signal_rate","t1_heavy_hit_signal_rate",
        "root_breakdown","loadout_breakdown",
    )
    return {k:a[k] for k in keys if k in a}

def _combined_row(cfg,arm_rows):
    def mean(path):
        vals=[float(r[path]) for r in arm_rows.values()]
        return statistics.fmean(vals)
    objectives=[
        mean("monster_evades_delta"),
        mean("round_extension"),
        _budget(cfg),
    ]
    return {
        "config":asdict(cfg),
        "status":LAB_STATUS,
        "objectives":{
            "monster_evades_delta_max":objectives[0],
            "round_extension_max":objectives[1],
            "adaptive_budget_min":objectives[2],
        },
        "objective_values":objectives,
        "descriptive":{
            "player_hp_pressure_delta_mean":mean("player_hp_pressure_delta"),
            "monster_damage_retention_mean":mean("monster_damage_retention"),
            "player_win_rate_delta_mean":mean("player_win_rate_delta"),
            "activation_rate_mean":statistics.fmean(
                float(r["t1"]["t1_activation_rate"]) for r in arm_rows.values()
            ),
        },
        "arms":arm_rows,
    }

def _dominates(a,b):
    av=a["objective_values"];bv=b["objective_values"]
    # max, max, min
    ok=av[0]>=bv[0] and av[1]>=bv[1] and av[2]<=bv[2]
    strict=av[0]>bv[0] or av[1]>bv[1] or av[2]<bv[2]
    return ok and strict

def _pareto(rows):
    return [r for i,r in enumerate(rows) if not any(
        _dominates(o,r) for j,o in enumerate(rows) if i!=j
    )]

def _coverage(rows,count):
    if len(rows)<=count:return list(rows)
    coords=[]
    cols=[[float(r["objective_values"][j]) for r in rows] for j in range(3)]
    mins=[min(c) for c in cols];maxs=[max(c) for c in cols]
    for r in rows:
        v=[]
        for j,x in enumerate(r["objective_values"]):
            z=0.0 if maxs[j]<=mins[j] else (float(x)-mins[j])/(maxs[j]-mins[j])
            if j==2:z=1.0-z
            v.append(z)
        coords.append(tuple(v))
    chosen=[]
    for j in range(3):
        idx=max(range(len(rows)),key=lambda i:coords[i][j])
        if idx not in chosen:chosen.append(idx)
        if len(chosen)>=count:break
    while len(chosen)<count:
        remaining=[i for i in range(len(rows)) if i not in chosen]
        idx=max(remaining,key=lambda i:min(math.dist(coords[i],coords[j]) for j in chosen))
        chosen.append(idx)
    return [rows[i] for i in chosen[:count]]

def _write_json(path,obj):
    Path(path).write_text(json.dumps(obj,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")

def _write_gz(path,obj):
    with gzip.open(path,"wt",encoding="utf-8",compresslevel=9) as f:
        json.dump(obj,f,ensure_ascii=False,sort_keys=True,separators=(",",":"))

def _zip(outdir):
    path=outdir/"RESULTADOS_RATA_T1_REFLEJO_HEAVY.zip"
    with zipfile.ZipFile(path,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in outdir.rglob("*"):
            if p.is_file() and p!=path:
                z.write(p,p.relative_to(outdir))
    return path

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--preset",choices=PRESETS,default="heavy")
    ap.add_argument("--outdir",default="RATA_T1_REFLEJO_HEAVY")
    ap.add_argument("--search-fights",type=int)
    ap.add_argument("--high-fights",type=int)
    ap.add_argument("--final-cap",type=int)
    args=ap.parse_args()
    cfg=dict(PRESETS[args.preset])
    for k in tuple(cfg):
        v=getattr(args,k)
        if v is not None:cfg[k]=v

    outdir=Path(args.outdir);outdir.mkdir(parents=True,exist_ok=True)
    registry=load_registry()
    rata=require_ready_profile(RATA_ID,registry)
    if rata["adaptive"]["status"]!="READY_FOR_T1_RECALIBRATION":
        raise RuntimeError("Rata T0 is not authorized for T1 recalibration")
    if rata["stats"]["basic_damage"]!="2d4" or rata["stats"]["hp"]!=21:
        raise RuntimeError("Rata T0 drifted from selected trial 4254")

    print("Computing common T0 baseline...",flush=True)
    base_search=_evaluate(rata,"T0",cfg["search_fights"],"SEARCH")
    base_search["monster_evades_per_fight"]=float(base_search.get("monster_evades_per_fight",0.0))

    rows=[]
    total=len(BONUSES)*len(COOLDOWNS)
    done=0
    for bonus in BONUSES:
        for cd in COOLDOWNS:
            tc=T1Config(bonus,cd)
            arm_rows={}
            for arm_name,arm in SIGNAL_ARMS.items():
                t1=_evaluate(rata,"T1",cfg["search_fights"],"SEARCH",tc,arm)
                d=_delta(t1,base_search)
                arm_rows[arm_name]={**d,"t1":_compact(t1)}
            rows.append(_combined_row(tc,arm_rows))
            done+=1
            print(f"SEARCH {done}/{total}: EVA+{bonus} CD{cd}",flush=True)

    front=_pareto(rows)
    selected=_coverage(front,int(cfg["final_cap"]))
    _write_gz(outdir/"search_grid.json.gz",rows)
    _write_gz(outdir/"search_pareto.json.gz",front)
    _write_gz(outdir/"high_precision_input.json.gz",selected)

    print("Computing independent high-precision T0 baseline...",flush=True)
    base_high=_evaluate(rata,"T0",cfg["high_fights"],"HIGH_PRECISION")
    base_high["monster_evades_per_fight"]=float(base_high.get("monster_evades_per_fight",0.0))

    high=[]
    for idx,item in enumerate(selected,1):
        tc=T1Config(**item["config"])
        arm_rows={}
        for arm_name,arm in SIGNAL_ARMS.items():
            t1=_evaluate(rata,"T1",cfg["high_fights"],"HIGH_PRECISION",tc,arm)
            d=_delta(t1,base_high)
            arm_rows[arm_name]={**d,"t1":_compact(t1)}
        high.append(_combined_row(tc,arm_rows))
        print(f"HIGH {idx}/{len(selected)}: {tc}",flush=True)

    high_front=_pareto(high)
    _write_gz(outdir/"high_precision_all.json.gz",high)
    _write_gz(outdir/"high_precision_pareto.json.gz",high_front)
    _write_json(outdir/"SUMMARY.json",{
        "experiment":"RATA_T1_REFLEJO_CALIBRATION_V01",
        "status":"LAB_RESULTS_AWAITING_HUMAN_SELECTION",
        "t0_source":"rata_qi READY trial 4254",
        "t1_identity":"Reflejo de Madriguera / EVADE_NEXT",
        "config":cfg,
        "grid":{"evasion_bonus":list(BONUSES),"cooldown_rounds":list(COOLDOWNS)},
        "signal_arms":SIGNAL_ARMS,
        "search_configs":len(rows),
        "search_pareto":len(front),
        "high_precision_configs":len(high),
        "high_precision_pareto":len(high_front),
        "t0_baseline_search":_compact(base_search),
        "t0_baseline_high_precision":_compact(base_high),
        "objectives":[
            "maximize additional monster evades per fight vs T0",
            "maximize round extension vs T0",
            "minimize normalized adaptive budget",
        ],
        "descriptive_not_targets":[
            "player win rate","player HP pressure delta","monster damage retention"
        ],
        "canonical_t1_selected":False,
        "t2_t4_executed":False,
        "raw_fights_persisted":False,
    })
    _write_json(outdir/"MANIFEST.json",{
        "engine_contract":"NEW_COMBAT_STATS_V0_1",
        "resource_model":"NONE",
        "canonical_t0":{"hp":21,"precision":80,"basic_damage":"2d4"},
        "t1_lab_only":True,
        "t2_t4_forbidden":True,
        "definitives_forbidden":True,
        "common_random_numbers":True,
        "raw_fights_persisted":False,
    })
    z=_zip(outdir)
    print(f"DONE: {z}",flush=True)

if __name__=="__main__":
    main()
