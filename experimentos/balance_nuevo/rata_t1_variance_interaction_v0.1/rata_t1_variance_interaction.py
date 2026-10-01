"""Rata T1 × individual-variance interaction LAB.

Uses the human-ratified natural Rata variance envelope, freezes each generated
individual before combat, then compares T0 vs decision-aware T1 on that same
individual. Mutante classification/rewards never change because of T1.

No canonical write. No T2-T4.
"""
from __future__ import annotations
import argparse,gzip,json,sys,zipfile
from collections import Counter
from contextlib import contextmanager
from pathlib import Path

HERE=Path(__file__).resolve().parent
BALANCE=HERE.parent
STAGE1=BALANCE/"stage1_integral_t0_optuna"
VARIANCE=BALANCE/"individual_variance_v0.1"
PARALLEL=BALANCE/"parallel_arc1_pipeline"
for p in (HERE,BALANCE,STAGE1,VARIANCE,PARALLEL):
    if str(p) not in sys.path:sys.path.insert(0,str(p))

import etapa19b_combat_engine as engine
from contexts import PRIMARY_CONTEXTS,ROOTS
from individual_variance import instantiate
from individual_variance_lab import profile_from_instance
from monster_new_engine_guard import load_registry,require_ready_profile
from player_policy_veteran import DEFAULT_VETERAN_CONFIG,VETERAN_BASIC,choose_veteran_action
from seeds import stable_seed
from streaming import StreamingAggregate
from telemetry import fight_once_observed
from decision_kernel_mirror import BASIC_ID,SURVIVAL_ID,Mulberry32,choose_rata_t1_intent

INPUT=json.loads((HERE/"input_v0.1.json").read_text(encoding="utf-8"))
RATA_ID="rata_qi"
BASIC_PROXY_SENTINEL_COST=10**9
TECHNIQUES=engine.load_json(BALANCE/"techniques_arc1_catalog.json")
EQUIPMENT=engine.load_json(BALANCE/"equipment_arc1_catalog.json")
PRESETS={
    "smoke":{"natural_fights":2,"mutant_fights":1},
    "directed":{"natural_fights":500,"mutant_fights":100},
    "heavy":{"natural_fights":2000,"mutant_fights":500},
}

def paths_for(root): return {tid:() for tid in engine.ROOT_TECHNIQUES[root]}

@contextmanager
def player_veteran_runtime():
    originals={
        "compile_build":engine.compile_build,
        "choose_player_action":engine.choose_player_action,
        "execute_player_technique":engine.execute_player_technique,
    }
    def compile_build(root,paths,catalog=None):
        compiled=dict(originals["compile_build"](root,paths,catalog))
        compiled[VETERAN_BASIC]={
            "technique_id":VETERAN_BASIC,"name":"Ataque básico","root":root,
            "role":"BASIC_PROXY","targeting":"UNITARGET","qi_cost":BASIC_PROXY_SENTINEL_COST,
        }
        return compiled
    def choose_player_action_fn(state,policy):
        if policy!="VETERAN": return originals["choose_player_action"](state,policy)
        return choose_veteran_action(state,DEFAULT_VETERAN_CONFIG)
    def execute_player(state,rng,c):
        if c.get("technique_id")==VETERAN_BASIC:
            engine.execute_basic(state,rng);return True
        return originals["execute_player_technique"](state,rng,c)
    engine.compile_build=compile_build
    engine.choose_player_action=choose_player_action_fn
    engine.execute_player_technique=execute_player
    try: yield
    finally:
        for k,v in originals.items():setattr(engine,k,v)

@contextmanager
def t1_runtime(*,config,arm,decision_seed,counters):
    originals={"build_monster":engine.build_monster,"execute_monster_turn":engine.execute_monster_turn}
    decision_rng=Mulberry32(decision_seed)

    def build_monster(profile,tier):
        if profile.get("id")!=RATA_ID or tier!="T1":
            raise RuntimeError("Rata T1 variance LAB accepts only rata_qi T1")
        return originals["build_monster"](profile,"T0")

    def execute_monster_turn(state,rng):
        self_low=(state.monster.hp/state.monster.hp_max)<=float(arm["low_hp_ratio"])
        heavy=float(state.last_player_hp_damage_to_monster)>=float(arm["heavy_hit_ratio"])*state.monster.hp_max
        player_low=(state.player.hp/state.player.hp_max)<=float(arm["low_hp_ratio"])
        signals={"SELF_LOW_HP":self_low,"TOOK_HEAVY_HIT":heavy,"PLAYER_LOW_HP":player_low}
        decision=choose_rata_t1_intent(
            signals=signals,
            recent_actions=list(state.monster_recent_actions),
            survival_on_cooldown=state.monster_survival_cd>0,
            rng=decision_rng,
        )
        counters["decisions"]+=1
        counters["self_low"]+=int(self_low);counters["heavy_hit"]+=int(heavy);counters["player_low"]+=int(player_low)
        if decision.ability_id==SURVIVAL_ID:
            counters["survival"]+=1
            state.monster_survival={"kind":"EVADE_NEXT","evasion_bonus":float(config["evasion_bonus"])}
            state.monster_survival_cd=int(config["cooldown_rounds"])+1
            state.metrics.adaptation_procs+=1
            state.monster_recent_actions.append("SURVIVAL")
            if state.arrastre_locked:
                state.arrastre_locked=False;state.arrastre_precision_debuff=0.0
            return
        counters["basic"]+=1
        return originals["execute_monster_turn"](state,rng)

    engine.build_monster=build_monster
    engine.execute_monster_turn=execute_monster_turn
    try:yield
    finally:
        for k,v in originals.items():setattr(engine,k,v)

def sample_mutant(context_id,root,index,namespace):
    for attempt in range(30000):
        seed=stable_seed("RATA_T1_VARIANCE_V01","MUTANT_INSTANCE",namespace,context_id,root,index,attempt)
        inst=instantiate(RATA_ID,seed)
        if inst["mutant"]: return inst
    raise RuntimeError("Mutante rejection sampler exhausted")

def run_fight(profile,root,items,combat_seed,tier,config=None,arm=None,ai_seed=None):
    counters=Counter()
    kwargs=dict(
        stage="LianQi_I",root=root,item_ids=items,paths=paths_for(root),
        monster_profile=profile,tier=tier,policy="VETERAN",seed=combat_seed,
        technique_catalog=TECHNIQUES,equipment_catalog=EQUIPMENT,max_rounds=100,
    )
    with player_veteran_runtime():
        if tier=="T0":
            row=fight_once_observed(**kwargs)
        else:
            with t1_runtime(config=config,arm=arm,decision_seed=ai_seed,counters=counters):
                row=fight_once_observed(
                    **kwargs,
                    signal_bridge=engine.LabSignalBridge(
                        low_hp_ratio=float(arm["low_hp_ratio"]),
                        heavy_hit_ratio=float(arm["heavy_hit_ratio"]),
                    ),
                )
    return row,counters

def add_decision(total,c):
    for k,v in c.items(): total[k]+=v

def eval_arm(canonical,*,tier,natural_n,mutant_n,namespace,config=None,arm=None):
    nat=StreamingAggregate();normal=StreamingAggregate();observed_mut=StreamingAggregate();forced_mut=StreamingAggregate()
    dec_nat=Counter();dec_mut=Counter()
    for ctx in PRIMARY_CONTEXTS:
        items=EQUIPMENT["simulation_loadouts"][ctx.loadout_profile]["LianQi_I"]
        for root in ROOTS:
            for i in range(natural_n):
                inst=instantiate(RATA_ID,stable_seed("RATA_T1_VARIANCE_V01","NATURAL_INSTANCE",namespace,ctx.context_id,root,i))
                profile=profile_from_instance(canonical,inst)
                combat_seed=stable_seed("RATA_T1_VARIANCE_V01","NATURAL_COMBAT",namespace,ctx.context_id,root,i)
                ai_seed=stable_seed("RATA_T1_VARIANCE_V01","AI",namespace,ctx.context_id,root,i)&0xFFFFFFFF
                row,counters=run_fight(profile,root,items,combat_seed,tier,config,arm,ai_seed)
                row["loadout_profile"]=ctx.loadout_profile
                nat.add(row);add_decision(dec_nat,counters)
                (observed_mut if inst["mutant"] else normal).add(row)
            for i in range(mutant_n):
                inst=sample_mutant(ctx.context_id,root,i,namespace)
                profile=profile_from_instance(canonical,inst)
                combat_seed=stable_seed("RATA_T1_VARIANCE_V01","MUTANT_COMBAT",namespace,ctx.context_id,root,i)
                ai_seed=stable_seed("RATA_T1_VARIANCE_V01","MUTANT_AI",namespace,ctx.context_id,root,i)&0xFFFFFFFF
                row,counters=run_fight(profile,root,items,combat_seed,tier,config,arm,ai_seed)
                row["loadout_profile"]=ctx.loadout_profile
                forced_mut.add(row);add_decision(dec_mut,counters)

    def done(a): return a.finish() if a.n else None
    def decisions(c,fights):
        d=float(c["decisions"])
        return {
            "decisions":c["decisions"],
            "survival_choices":c["survival"],
            "survival_per_fight":c["survival"]/fights if fights else 0.0,
            "survival_rate_per_decision":c["survival"]/d if d else 0.0,
            "self_low_rate":c["self_low"]/d if d else 0.0,
            "heavy_hit_rate":c["heavy_hit"]/d if d else 0.0,
            "player_low_rate":c["player_low"]/d if d else 0.0,
        }
    return {
        "natural_all":done(nat),
        "natural_normal":done(normal),
        "natural_mutant_observed":done(observed_mut),
        "mutant_conditional":done(forced_mut),
        "decision_natural":decisions(dec_nat,nat.n),
        "decision_mutant":decisions(dec_mut,forced_mut.n),
    }

def delta(t1,t0,key):
    return float(t1[key])-float(t0[key])

def compact_delta(t1,t0):
    return {
        "win_rate_delta":delta(t1,t0,"win_rate"),
        "rounds_delta":delta(t1,t0,"rounds_mean"),
        "hp_pressure_delta":(1-float(t1["hp_final_pct_mean"]))-(1-float(t0["hp_final_pct_mean"])),
        "monster_damage_delta":delta(t1,t0,"monster_damage_total_mean"),
        "monster_evades_delta":delta(t1,t0,"monster_evades_mean"),
    }

def write_json(path,obj):Path(path).write_text(json.dumps(obj,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
def write_gz(path,obj):
    with gzip.open(path,"wt",encoding="utf-8",compresslevel=9) as f:json.dump(obj,f,ensure_ascii=False,sort_keys=True,separators=(",",":"))
def zip_results(outdir):
    z=outdir/"RESULTADOS_RATA_T1_VARIANCE_INTERACTION_V01.zip"
    with zipfile.ZipFile(z,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as zz:
        for p in outdir.rglob("*"):
            if p.is_file() and p!=z:zz.write(p,p.relative_to(outdir))
    return z

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--preset",choices=PRESETS,default="heavy")
    ap.add_argument("--natural-fights",type=int)
    ap.add_argument("--mutant-fights",type=int)
    ap.add_argument("--outdir",default="RATA_T1_VARIANCE_INTERACTION_V01")
    ap.add_argument("--namespace",default="RUN")
    args=ap.parse_args()
    cfg=dict(PRESETS[args.preset])
    if args.natural_fights is not None:cfg["natural_fights"]=args.natural_fights
    if args.mutant_fights is not None:cfg["mutant_fights"]=args.mutant_fights

    registry=load_registry();canonical=require_ready_profile(RATA_ID,registry)
    if canonical["adaptive"]["status"]!="READY_FOR_T1_RECALIBRATION":
        raise RuntimeError("Rata T1 gate closed")

    outdir=Path(args.outdir);outdir.mkdir(parents=True,exist_ok=True)
    print("VARIABLE T0 baseline",flush=True)
    t0=eval_arm(canonical,tier="T0",natural_n=cfg["natural_fights"],mutant_n=cfg["mutant_fights"],namespace=args.namespace)

    rows=[]
    for candidate in INPUT["candidates"]:
        for arm_name,arm in INPUT["signal_arms"].items():
            print(candidate["label"],arm_name,flush=True)
            t1=eval_arm(
                canonical,tier="T1",natural_n=cfg["natural_fights"],mutant_n=cfg["mutant_fights"],
                namespace=args.namespace,config=candidate,arm=arm
            )
            rows.append({
                "candidate":candidate,"arm":arm_name,"signal_thresholds":arm,
                "result":t1,
                "delta_vs_variable_t0":{
                    "natural_all":compact_delta(t1["natural_all"],t0["natural_all"]),
                    "natural_normal":compact_delta(t1["natural_normal"],t0["natural_normal"]),
                    "mutant_conditional":compact_delta(t1["mutant_conditional"],t0["mutant_conditional"]),
                },
            })
    write_gz(outdir/"results.json.gz",rows)
    write_gz(outdir/"variable_t0_baseline.json.gz",t0)
    write_json(outdir/"SUMMARY.json",{
        "experiment":"RATA_T1_VARIANCE_INTERACTION_V01",
        "status":"LAB_RESULTS_AWAITING_HUMAN_REVIEW",
        "natural_fights_per_context":cfg["natural_fights"],
        "mutant_fights_per_context":cfg["mutant_fights"],
        "contexts":10,
        "t1_candidates":INPUT["candidates"],
        "signal_arms":INPUT["signal_arms"],
        "same_individual_distribution_across_arms":True,
        "mutant_classification_precedes_t1":True,
        "canonical_write":False,
        "t2_t4_executed":False,
    })
    write_json(outdir/"MANIFEST.json",{
        "source_t1_commit":INPUT["source_t1_commit"],
        "variance_distribution":"UNIFORM_0_1",
        "t0_floor_trial":4254,
        "adaptive_tier":"T1_ONLY",
        "survival_kind":"EVADE_NEXT",
        "separate_ai_rng":True,
        "canonical_write":False,
        "t2_t4_forbidden":True,
    })
    print("DONE",zip_results(outdir),flush=True)

if __name__=="__main__":main()
