"""Rata T2 recognition combat LAB.

Compares frozen human-ratified T1 against three T2 recognition hypotheses on
the same variable individuals and combat seeds.

T1 +40 EVA / CD5 / BASE is immutable.
T3-T4 are forbidden.
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
T1LAB=BALANCE/"rata_t1_variance_interaction_v0.1"
PARALLEL=BALANCE/"parallel_arc1_pipeline"
for p in (HERE,BALANCE,STAGE1,VARIANCE,T1LAB,PARALLEL):
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
from decision_kernel_mirror import Mulberry32,BASIC_ID,SURVIVAL_ID,choose_rata_t1_intent
from recognition_kernel import classify_player_action,observe,recognize_recent_pattern
from t2_decision_kernel import choose_rata_t2_intent

RATA_ID="rata_qi"
BASIC_PROXY_SENTINEL_COST=10**9
TECHNIQUES=engine.load_json(BALANCE/"techniques_arc1_catalog.json")
EQUIPMENT=engine.load_json(BALANCE/"equipment_arc1_catalog.json")
CONTRACT=json.loads((HERE/"RATA_ADAPTIVE_TIER_CONTRACT_V0_1.json").read_text(encoding="utf-8"))
INPUT=json.loads((HERE/"RATA_T2_RECOGNITION_INPUT_V0_1.json").read_text(encoding="utf-8"))
T1_CFG=CONTRACT["t1"]["ability"]
BASE_ARM=CONTRACT["t1"]["selector"]["selected_signal_arm"]
PRESETS={
    "smoke":{"natural_fights":2,"mutant_fights":1},
    "directed":{"natural_fights":500,"mutant_fights":100},
    "heavy":{"natural_fights":2000,"mutant_fights":500},
}

def paths_for(root):return {tid:() for tid in engine.ROOT_TECHNIQUES[root]}

class ObservationState:
    def __init__(self):
        self.memory=[]
        self.pending_prediction=None
        self.predictions=0
        self.predictions_correct=0
        self.predictions_false=0

    def append_action(self,category,result):
        if self.pending_prediction is not None:
            self.predictions+=1
            if category==self.pending_prediction:self.predictions_correct+=1
            else:self.predictions_false+=1
            self.pending_prediction=None
        self.memory.append(observe(category,result))
        if len(self.memory)>8:self.memory=self.memory[-8:]

@contextmanager
def player_observation_runtime(obs:ObservationState):
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
    def choose_action(state,policy):
        if policy!="VETERAN":return originals["choose_player_action"](state,policy)
        return choose_veteran_action(state,DEFAULT_VETERAN_CONFIG)
    def execute_action(state,rng,c):
        if c.get("technique_id")==VETERAN_BASIC:
            engine.execute_basic(state,rng)
            result="EFECTIVA" if state.last_player_hp_damage_to_monster>0 else "FALLIDA"
            obs.append_action("PLAYER_BASIC",result)
            return True
        ok=originals["execute_player_technique"](state,rng,c)
        category=classify_player_action(c)
        if c.get("role")=="DEFENSIVE":
            result="EFECTIVA" if ok else "FALLIDA"
        else:
            result="EFECTIVA" if ok and state.last_player_hp_damage_to_monster>0 else "FALLIDA"
        obs.append_action(category,result)
        return ok
    engine.compile_build=compile_build
    engine.choose_player_action=choose_action
    engine.execute_player_technique=execute_action
    try:yield
    finally:
        for k,v in originals.items():setattr(engine,k,v)

@contextmanager
def adaptive_runtime(*,tier,candidate,decision_seed,obs,counters):
    originals={"build_monster":engine.build_monster,"execute_monster_turn":engine.execute_monster_turn}
    rng_ai=Mulberry32(decision_seed)

    def build_monster(profile,requested_tier):
        if profile.get("id")!=RATA_ID or requested_tier!=tier:
            raise RuntimeError("Rata adaptive recognition LAB tier mismatch")
        return originals["build_monster"](profile,"T0")

    def execute_monster_turn(state,rng):
        low=float(BASE_ARM["self_low_hp_ratio"])
        heavy_ratio=float(BASE_ARM["heavy_hit_ratio"])
        self_low=(state.monster.hp/state.monster.hp_max)<=low
        heavy=float(state.last_player_hp_damage_to_monster)>=heavy_ratio*state.monster.hp_max
        player_low=(state.player.hp/state.player.hp_max)<=low
        signals={"SELF_LOW_HP":self_low,"TOOK_HEAVY_HIT":heavy,"PLAYER_LOW_HP":player_low}

        recog={"recognized":False,"category":None,"support":0}
        if tier=="T2":
            recog=recognize_recent_pattern(obs.memory,candidate)
            counters["recognition_checks"]+=1
            counters["recognition_triggers"]+=int(recog["recognized"])

        if tier=="T1":
            decision=choose_rata_t1_intent(
                signals=signals,recent_actions=list(state.monster_recent_actions),
                survival_on_cooldown=state.monster_survival_cd>0,rng=rng_ai,
            )
            applied=0.0
        else:
            decision=choose_rata_t2_intent(
                signals=signals,recent_actions=list(state.monster_recent_actions),
                survival_on_cooldown=state.monster_survival_cd>0,
                recognition_active=bool(recog["recognized"]),
                recognition_bonus=float(candidate["preemptive_survival_bonus"]),
                rng=rng_ai,
            )
            applied=float(decision.recognition_bonus)
            counters["recognition_bonus_applied"]+=int(applied>0)
            if recog["recognized"]:
                obs.pending_prediction=recog["category"]

        counters["decisions"]+=1
        counters["self_low"]+=int(self_low)
        counters["heavy_hit"]+=int(heavy)
        counters["player_low"]+=int(player_low)

        if decision.ability_id==SURVIVAL_ID:
            counters["survival"]+=1
            if tier=="T2" and applied>0:counters["survival_with_recognition"]+=1
            state.monster_survival={"kind":"EVADE_NEXT","evasion_bonus":40.0}
            state.monster_survival_cd=6
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

def sample_mutant(ctx,root,index,namespace):
    for attempt in range(30000):
        seed=stable_seed("RATA_T2_RECOGNITION_V01","MUTANT_INSTANCE",namespace,ctx,root,index,attempt)
        inst=instantiate(RATA_ID,seed)
        if inst["mutant"]:return inst
    raise RuntimeError("Mutante sampler exhausted")

def run_once(profile,root,items,combat_seed,tier,candidate,ai_seed):
    obs=ObservationState();counters=Counter()
    kwargs=dict(
        stage="LianQi_I",root=root,item_ids=items,paths=paths_for(root),
        monster_profile=profile,tier=tier,policy="VETERAN",seed=combat_seed,
        technique_catalog=TECHNIQUES,equipment_catalog=EQUIPMENT,max_rounds=100,
        signal_bridge=engine.LabSignalBridge(
            low_hp_ratio=float(BASE_ARM["self_low_hp_ratio"]),
            heavy_hit_ratio=float(BASE_ARM["heavy_hit_ratio"]),
        ),
    )
    with player_observation_runtime(obs):
        with adaptive_runtime(tier=tier,candidate=candidate,decision_seed=ai_seed,obs=obs,counters=counters):
            row=fight_once_observed(**kwargs)
    counters["predictions"]=obs.predictions
    counters["predictions_correct"]=obs.predictions_correct
    counters["predictions_false"]=obs.predictions_false
    return row,counters

def add_counter(dst,src):
    for k,v in src.items():dst[k]+=v

def eval_tier(canonical,*,tier,candidate,natural_n,mutant_n,namespace):
    natural=StreamingAggregate();normal=StreamingAggregate();observed_mut=StreamingAggregate();forced_mut=StreamingAggregate()
    c_nat=Counter();c_mut=Counter()
    for ctx in PRIMARY_CONTEXTS:
        items=EQUIPMENT["simulation_loadouts"][ctx.loadout_profile]["LianQi_I"]
        for root in ROOTS:
            for i in range(natural_n):
                inst=instantiate(RATA_ID,stable_seed("RATA_T2_RECOGNITION_V01","NATURAL_INSTANCE",namespace,ctx.context_id,root,i))
                profile=profile_from_instance(canonical,inst)
                combat_seed=stable_seed("RATA_T2_RECOGNITION_V01","NATURAL_COMBAT",namespace,ctx.context_id,root,i)
                ai_seed=stable_seed("RATA_T2_RECOGNITION_V01","AI",namespace,ctx.context_id,root,i)&0xFFFFFFFF
                row,cnt=run_once(profile,root,items,combat_seed,tier,candidate,ai_seed)
                row["loadout_profile"]=ctx.loadout_profile
                natural.add(row);add_counter(c_nat,cnt)
                (observed_mut if inst["mutant"] else normal).add(row)
            for i in range(mutant_n):
                inst=sample_mutant(ctx.context_id,root,i,namespace)
                profile=profile_from_instance(canonical,inst)
                combat_seed=stable_seed("RATA_T2_RECOGNITION_V01","MUTANT_COMBAT",namespace,ctx.context_id,root,i)
                ai_seed=stable_seed("RATA_T2_RECOGNITION_V01","MUTANT_AI",namespace,ctx.context_id,root,i)&0xFFFFFFFF
                row,cnt=run_once(profile,root,items,combat_seed,tier,candidate,ai_seed)
                row["loadout_profile"]=ctx.loadout_profile
                forced_mut.add(row);add_counter(c_mut,cnt)

    def done(a):return a.finish() if a.n else None
    def counter_metrics(c,fights):
        checks=float(c["recognition_checks"])
        preds=float(c["predictions"])
        decisions=float(c["decisions"])
        return {
            "decisions":c["decisions"],
            "survival_choices":c["survival"],
            "survival_per_fight":c["survival"]/fights if fights else 0.0,
            "recognition_checks":c["recognition_checks"],
            "recognition_triggers":c["recognition_triggers"],
            "recognition_trigger_rate":c["recognition_triggers"]/checks if checks else 0.0,
            "survival_with_recognition":c["survival_with_recognition"],
            "prediction_count":c["predictions"],
            "prediction_accuracy":c["predictions_correct"]/preds if preds else 0.0,
            "false_positive_anticipation_rate":c["predictions_false"]/preds if preds else 0.0,
            "self_low_rate":c["self_low"]/decisions if decisions else 0.0,
            "heavy_hit_rate":c["heavy_hit"]/decisions if decisions else 0.0,
        }
    return {
        "natural_all":done(natural),"natural_normal":done(normal),
        "natural_mutant_observed":done(observed_mut),"mutant_conditional":done(forced_mut),
        "decision_natural":counter_metrics(c_nat,natural.n),"decision_mutant":counter_metrics(c_mut,forced_mut.n),
    }

def delta(a,b):
    return {
        "win_rate_delta":float(a["win_rate"])-float(b["win_rate"]),
        "rounds_delta":float(a["rounds_mean"])-float(b["rounds_mean"]),
        "hp_pressure_delta":(1-float(a["hp_final_pct_mean"]))-(1-float(b["hp_final_pct_mean"])),
        "qi_spent_delta":float(a["qi_spent_mean"])-float(b["qi_spent_mean"]),
        "monster_damage_delta":float(a["monster_damage_total_mean"])-float(b["monster_damage_total_mean"]),
        "monster_evades_delta":float(a["monster_evades_mean"])-float(b["monster_evades_mean"]),
    }

def write_json(path,obj):Path(path).write_text(json.dumps(obj,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
def write_gz(path,obj):
    with gzip.open(path,"wt",encoding="utf-8",compresslevel=9) as f:json.dump(obj,f,ensure_ascii=False,sort_keys=True,separators=(",",":"))
def zip_results(outdir):
    z=outdir/"RESULTADOS_RATA_T2_RECOGNITION_V01.zip"
    with zipfile.ZipFile(z,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as zz:
        for p in outdir.rglob("*"):
            if p.is_file() and p!=z:zz.write(p,p.relative_to(outdir))
    return z

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--preset",choices=PRESETS,default="heavy")
    ap.add_argument("--natural-fights",type=int)
    ap.add_argument("--mutant-fights",type=int)
    ap.add_argument("--outdir",default="RATA_T2_RECOGNITION_V01")
    ap.add_argument("--namespace",default="RUN")
    args=ap.parse_args()
    cfg=dict(PRESETS[args.preset])
    if args.natural_fights is not None:cfg["natural_fights"]=args.natural_fights
    if args.mutant_fights is not None:cfg["mutant_fights"]=args.mutant_fights

    registry=load_registry();canonical=require_ready_profile(RATA_ID,registry)
    if canonical["adaptive"]["status"]!="T1_READY_FOR_T2_CALIBRATION":
        raise RuntimeError("T2 gate is not open")
    if CONTRACT["t1"]["ability"]["evasion_bonus"]!=40 or CONTRACT["t1"]["ability"]["cooldown_rounds"]!=5:
        raise RuntimeError("frozen T1 contract drift")

    outdir=Path(args.outdir);outdir.mkdir(parents=True,exist_ok=True)
    neutral={"memory_window":2,"repeated_same_category_required":2,"preemptive_survival_bonus":0,"count_results":["EFECTIVA"]}
    print("Frozen T1 baseline",flush=True)
    t1=eval_tier(canonical,tier="T1",candidate=neutral,natural_n=cfg["natural_fights"],mutant_n=cfg["mutant_fights"],namespace=args.namespace)

    rows=[]
    for cand in INPUT["candidates"]:
        cand=dict(cand)
        cand.setdefault("count_results",["EFECTIVA"])
        print(cand["label"],flush=True)
        t2=eval_tier(canonical,tier="T2",candidate=cand,natural_n=cfg["natural_fights"],mutant_n=cfg["mutant_fights"],namespace=args.namespace)
        rows.append({
            "candidate":cand,
            "result":t2,
            "delta_vs_frozen_t1":{
                "natural_all":delta(t2["natural_all"],t1["natural_all"]),
                "natural_normal":delta(t2["natural_normal"],t1["natural_normal"]),
                "mutant_conditional":delta(t2["mutant_conditional"],t1["mutant_conditional"]),
            }
        })
    write_gz(outdir/"frozen_t1_baseline.json.gz",t1)
    write_gz(outdir/"t2_results.json.gz",rows)
    write_json(outdir/"SUMMARY.json",{
        "experiment":"RATA_T2_RECOGNITION_V01",
        "status":"LAB_RESULTS_AWAITING_HUMAN_REVIEW",
        "natural_fights_per_context":cfg["natural_fights"],
        "mutant_fights_per_context":cfg["mutant_fights"],
        "contexts":10,
        "t1_frozen":True,
        "t1_evasion_bonus":40,
        "t1_cooldown_rounds":5,
        "t2_candidates":INPUT["candidates"],
        "canonical_write":False,
        "t3_t4_executed":False,
    })
    write_json(outdir/"MANIFEST.json",{
        "observable_categories_only":True,
        "hidden_root_build_forbidden":True,
        "same_instance_distribution":True,
        "same_combat_rng_namespace":True,
        "separate_ai_rng":True,
        "t1_numeric_changes":False,
        "canonical_write":False,
        "t3_t4_forbidden":True,
    })
    print("DONE",zip_results(outdir),flush=True)

if __name__=="__main__":main()
