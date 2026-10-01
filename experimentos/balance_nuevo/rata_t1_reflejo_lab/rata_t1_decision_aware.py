"""Decision-aware Rata T1 revalidation.

Three magnitudes only (+25/+40/+50 EVA, CD5), with Monster Combat AI v0.1
decision scoring mirrored and parity-checked against the original JS kernel.
No automatic CANON promotion. T2 remains blocked.
"""
from __future__ import annotations
import argparse,gzip,json,statistics,sys,zipfile
from contextlib import contextmanager
from pathlib import Path

HERE=Path(__file__).resolve().parent
BALANCE=HERE.parent
STAGE1=BALANCE/"stage1_integral_t0_optuna"
for p in (BALANCE,STAGE1,HERE):
    if str(p) not in sys.path:sys.path.insert(0,str(p))

import etapa19b_combat_engine as engine
from contexts import PRIMARY_CONTEXTS,ROOTS
from monster_new_engine_guard import load_registry,require_ready_profile
from player_policy_veteran import DEFAULT_VETERAN_CONFIG,VETERAN_BASIC,choose_veteran_action
from seeds import stable_seed
from stream_aggregate import StreamingFightAggregate
from telemetry import fight_once_observed
from decision_kernel_mirror import (
    BASIC_ID,SURVIVAL_ID,Mulberry32,choose_rata_t1_intent
)

RATA_ID="rata_qi"
BASIC_PROXY_SENTINEL_COST=10**9
TECHNIQUES=engine.load_json(BALANCE/"techniques_arc1_catalog.json")
EQUIPMENT=engine.load_json(BALANCE/"equipment_arc1_catalog.json")
INPUT=engine.load_json(HERE/"rata_t1_decision_aware_input_v0.1.json")

ARMS={
    "EARLY":{"low_hp_ratio":0.40,"heavy_hit_ratio":0.15},
    "BASE":{"low_hp_ratio":0.30,"heavy_hit_ratio":0.20},
    "LATE":{"low_hp_ratio":0.20,"heavy_hit_ratio":0.25},
}
PRESETS={
    "smoke":{"fights_per_context":3},
    "directed":{"fights_per_context":2000},
    "heavy":{"fights_per_context":10000},
}

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
            engine.execute_basic(state,rng);return True
        return originals["execute_player_technique"](state,rng,c)
    engine.compile_build=compile_build
    engine.choose_player_action=choose_player_action
    engine.execute_player_technique=execute_player_technique
    try:yield
    finally:
        for k,v in originals.items():setattr(engine,k,v)

@contextmanager
def _decision_runtime(*,config,arm,decision_seed,counters):
    originals={
        "build_monster":engine.build_monster,
        "execute_monster_turn":engine.execute_monster_turn,
    }
    decision_rng=Mulberry32(decision_seed)

    def build_monster(profile,tier):
        if profile.get("id")!=RATA_ID or tier!="T1":
            raise RuntimeError("decision-aware lab accepts only rata_qi T1")
        return originals["build_monster"](profile,"T0")

    def execute_monster_turn(state,rng):
        self_low=(state.monster.hp/state.monster.hp_max)<=float(arm["low_hp_ratio"])
        heavy=float(state.last_player_hp_damage_to_monster)>=float(arm["heavy_hit_ratio"])*state.monster.hp_max
        # LabSignalBridge historically exposes one low-HP threshold; use it
        # symmetrically for PLAYER_LOW_HP sensitivity. It remains LAB-only.
        player_low=(state.player.hp/state.player.hp_max)<=float(arm["low_hp_ratio"])
        signals={
            "SELF_LOW_HP":self_low,
            "TOOK_HEAVY_HIT":heavy,
            "PLAYER_LOW_HP":player_low,
        }
        cooldown=state.monster_survival_cd>0
        recent=list(state.monster_recent_actions)
        decision=choose_rata_t1_intent(
            signals=signals,
            recent_actions=recent,
            survival_on_cooldown=cooldown,
            rng=decision_rng,
        )
        counters["decisions"]+=1
        counters["self_low"]+=int(self_low)
        counters["heavy_hit"]+=int(heavy)
        counters["player_low"]+=int(player_low)
        counters["both_self_heavy"]+=int(self_low and heavy)
        if decision.ability_id==SURVIVAL_ID:
            counters["survival_choices"]+=1
            counters["survival_score_sum"]+=float(decision.survival_score)
            counters["basic_score_when_survival_sum"]+=float(decision.basic_score)
            state.monster_survival={"kind":"EVADE_NEXT","evasion_bonus":float(config["evasion_bonus"])}
            state.monster_survival_cd=int(config["cooldown_rounds"])+1
            state.metrics.adaptation_procs+=1
            state.monster_recent_actions.append("SURVIVAL")
            if state.arrastre_locked:
                state.arrastre_locked=False
                state.arrastre_precision_debuff=0.0
            return
        counters["basic_choices"]+=1
        return originals["execute_monster_turn"](state,rng)

    engine.build_monster=build_monster
    engine.execute_monster_turn=execute_monster_turn
    try:yield
    finally:
        for k,v in originals.items():setattr(engine,k,v)

def _run_once(profile,root,item_ids,seed,tier,config=None,arm=None,decision_seed=None):
    counters={
        "decisions":0,"survival_choices":0,"basic_choices":0,
        "self_low":0,"heavy_hit":0,"player_low":0,"both_self_heavy":0,
        "survival_score_sum":0.0,"basic_score_when_survival_sum":0.0,
    }
    kwargs=dict(
        stage="LianQi_I",root=root,item_ids=item_ids,paths=paths_for(root),
        monster_profile=profile,tier=tier,policy="VETERAN",seed=seed,
        technique_catalog=TECHNIQUES,equipment_catalog=EQUIPMENT,max_rounds=100,
    )
    with _player_veteran_runtime():
        if tier=="T0":
            row=fight_once_observed(**kwargs)
        else:
            with _decision_runtime(config=config,arm=arm,decision_seed=decision_seed,counters=counters):
                row=fight_once_observed(
                    **kwargs,
                    signal_bridge=engine.LabSignalBridge(
                        low_hp_ratio=float(arm["low_hp_ratio"]),
                        heavy_hit_ratio=float(arm["heavy_hit_ratio"]),
                    ),
                )
    row["loadout_profile"]="UNKNOWN"
    for k,v in counters.items():row[f"decision_{k}"]=v
    return row

def evaluate(profile,tier,n,namespace,config=None,arm=None):
    agg=StreamingFightAggregate()
    extra={k:0.0 for k in [
        "decisions","survival_choices","basic_choices","self_low","heavy_hit",
        "player_low","both_self_heavy","survival_score_sum","basic_score_when_survival_sum"
    ]}
    for ctx in PRIMARY_CONTEXTS:
        items=EQUIPMENT["simulation_loadouts"][ctx.loadout_profile]["LianQi_I"]
        for root in ROOTS:
            for i in range(n):
                combat_seed=stable_seed("RATA_T1_DECISION_COMBAT",namespace,ctx.context_id,root,i)
                decision_seed=stable_seed("RATA_T1_DECISION_AI",namespace,ctx.context_id,root,i)&0xFFFFFFFF
                row=_run_once(profile,root,items,combat_seed,tier,config,arm,decision_seed)
                row["loadout_profile"]=ctx.loadout_profile
                agg.add(row)
                for k in extra:extra[k]+=float(row[f"decision_{k}"])
    out=agg.finish()
    fights=float(out["fights"])
    decisions=extra["decisions"]
    survival=extra["survival_choices"]
    out.update({
        "decision_count":decisions,
        "survival_choices_total":survival,
        "basic_choices_total":extra["basic_choices"],
        "survival_choices_per_fight":survival/fights,
        "survival_choice_rate_per_decision":survival/decisions if decisions else 0.0,
        "self_low_signal_rate_per_decision":extra["self_low"]/decisions if decisions else 0.0,
        "heavy_hit_signal_rate_per_decision":extra["heavy_hit"]/decisions if decisions else 0.0,
        "player_low_signal_rate_per_decision":extra["player_low"]/decisions if decisions else 0.0,
        "self_low_and_heavy_rate_per_decision":extra["both_self_heavy"]/decisions if decisions else 0.0,
        "survival_score_mean_when_chosen":extra["survival_score_sum"]/survival if survival else None,
        "basic_score_mean_when_survival_chosen":extra["basic_score_when_survival_sum"]/survival if survival else None,
    })
    return out

def deltas(t1,t0):
    return {
        "round_extension":float(t1["rounds_mean"])-float(t0["rounds_mean"]),
        "player_hp_pressure_delta":(
            (1-float(t1["hp_final_pct_mean"]))-(1-float(t0["hp_final_pct_mean"]))
        ),
        "monster_damage_retention":(
            float(t1["monster_damage_total_mean"])/float(t0["monster_damage_total_mean"])
            if float(t0["monster_damage_total_mean"]) else 0.0
        ),
        "player_win_rate_delta":float(t1["win_rate"])-float(t0["win_rate"]),
        "monster_evades_delta":float(t1["monster_evades_per_fight"])-float(t0["monster_evades_per_fight"]),
    }

def compact(a):
    keys=(
        "fights","win_rate","timeout_rate","rounds_mean","hp_final_pct_mean","hp_final_pct_p10",
        "monster_damage_total_mean","monster_damage_total_p90","player_hit_rate","monster_hit_rate",
        "monster_evades_per_fight","survival_choices_per_fight","survival_choice_rate_per_decision",
        "self_low_signal_rate_per_decision","heavy_hit_signal_rate_per_decision",
        "player_low_signal_rate_per_decision","self_low_and_heavy_rate_per_decision",
        "survival_score_mean_when_chosen","basic_score_mean_when_survival_chosen",
        "root_breakdown","loadout_breakdown",
    )
    return {k:a[k] for k in keys if k in a}

def write_json(path,obj):
    Path(path).write_text(json.dumps(obj,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
def write_gz(path,obj):
    with gzip.open(path,"wt",encoding="utf-8",compresslevel=9) as f:
        json.dump(obj,f,ensure_ascii=False,sort_keys=True,separators=(",",":"))
def zip_results(outdir):
    zpath=outdir/"RESULTADOS_RATA_T1_DECISION_AWARE.zip"
    with zipfile.ZipFile(zpath,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in outdir.rglob("*"):
            if p.is_file() and p!=zpath:z.write(p,p.relative_to(outdir))
    return zpath

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--preset",choices=PRESETS,default="heavy")
    ap.add_argument("--fights-per-context",type=int)
    ap.add_argument("--outdir",default="RATA_T1_DECISION_AWARE")
    args=ap.parse_args()
    n=args.fights_per_context or PRESETS[args.preset]["fights_per_context"]
    outdir=Path(args.outdir);outdir.mkdir(parents=True,exist_ok=True)

    registry=load_registry();rata=require_ready_profile(RATA_ID,registry)
    if rata["adaptive"]["status"]!="READY_FOR_T1_RECALIBRATION":
        raise RuntimeError("Rata T1 recalibration gate is closed")
    if rata["stats"]["hp"]!=21 or rata["stats"]["precision"]!=80 or rata["stats"]["basic_damage"]!="2d4":
        raise RuntimeError("Rata T0 drifted from trial 4254")

    print("T0 baseline...",flush=True)
    t0=evaluate(rata,"T0",n,"COMMON")
    t0["monster_evades_per_fight"]=float(t0.get("monster_evades_per_fight",0.0))

    rows=[]
    for cfg in INPUT["candidates"]:
        for arm_name,arm in ARMS.items():
            print(f"{cfg['label']} {arm_name}: EVA+{cfg['evasion_bonus']} CD{cfg['cooldown_rounds']}",flush=True)
            t1=evaluate(rata,"T1",n,"COMMON",cfg,arm)
            rows.append({
                "label":cfg["label"],"config":cfg,"arm":arm_name,"signal_thresholds":arm,
                "aggregate":compact(t1),"delta_vs_t0":deltas(t1,t0),
            })
    write_gz(outdir/"decision_aware_results.json.gz",rows)
    write_json(outdir/"SUMMARY.json",{
        "experiment":"RATA_T1_DECISION_AWARE_V01",
        "status":"LAB_RESULTS_AWAITING_HUMAN_SELECTION",
        "t0_source":"rata_qi READY trial 4254",
        "fights_per_context":n,
        "contexts":10,
        "candidates":INPUT["candidates"],
        "signal_arms":ARMS,
        "t0_baseline":compact(t0),
        "selector":{
            "profile":"REACTIVO_1",
            "kernel_contract":"Monster Combat AI v0.1",
            "python_mirror_ci_parity_required":True,
        },
        "canonical_t1_selected":False,
        "t2_t4_executed":False,
        "raw_fights_persisted":False,
    })
    write_json(outdir/"MANIFEST.json",{
        "engine_contract":"NEW_COMBAT_STATS_V0_1",
        "resource_model":"NONE",
        "t0":{"hp":21,"precision":80,"basic_damage":"2d4"},
        "decision_aware":True,
        "survival_forced":False,
        "common_combat_random_numbers":True,
        "separate_deterministic_ai_rng":True,
        "canonical_write":False,
        "t2_t4_forbidden":True,
    })
    print("DONE",zip_results(outdir),flush=True)

if __name__=="__main__":main()
