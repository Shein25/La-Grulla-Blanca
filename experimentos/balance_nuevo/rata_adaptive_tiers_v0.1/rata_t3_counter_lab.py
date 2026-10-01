"""Rata T3 species-counter combat LAB.

Frozen:
- T1 Reflejo +40 EVA / CD5 / REACTIVO_1 / BASE.
- T2 R2_SHORT: memory 2 / repeat 2 / EFECTIVA / +8.

T3 tests trigger semantics only. Counter damage is fixed to the canonical T0
basic reference 2d4 and resolves through the normal monster direct pipeline.

A T3 counter may arm ONLY when Reflejo actually caused the player's miss:
the same hit roll must have connected against the individual's natural EVA but
failed after the +40 EVA Reflejo bonus.

No canonical write. T4 forbidden.
"""
from __future__ import annotations

import argparse
from collections import Counter
from contextlib import contextmanager
from dataclasses import dataclass, field
import gzip
import json
from pathlib import Path
import random
import statistics
import sys
import zipfile

HERE=Path(__file__).resolve().parent
BALANCE=HERE.parent
STAGE1=BALANCE/"stage1_integral_t0_optuna"
VARIANCE=BALANCE/"individual_variance_v0.1"
T1LAB=BALANCE/"rata_t1_variance_interaction_v0.1"
PARALLEL=BALANCE/"parallel_arc1_pipeline"
for p in (HERE,BALANCE,STAGE1,VARIANCE,T1LAB,PARALLEL):
    if str(p) not in sys.path:
        sys.path.insert(0,str(p))

import etapa19b_combat_engine as engine
from contexts import PRIMARY_CONTEXTS,ROOTS
from individual_variance import instantiate
from individual_variance_lab import profile_from_instance
from monster_new_engine_guard import load_registry,require_ready_profile
from player_policy_veteran import (
    DEFAULT_VETERAN_CONFIG,
    VETERAN_BASIC,
    choose_veteran_action,
)
from seeds import stable_seed
from streaming import StreamingAggregate,percentile
from telemetry import fight_once_observed
from decision_kernel_mirror import Mulberry32,SURVIVAL_ID
from recognition_kernel import classify_player_action,observe,recognize_recent_pattern
from t2_decision_kernel import choose_rata_t2_intent

RATA_ID="rata_qi"
BASIC_PROXY_SENTINEL_COST=10**9
TECHNIQUES=engine.load_json(BALANCE/"techniques_arc1_catalog.json")
EQUIPMENT=engine.load_json(BALANCE/"equipment_arc1_catalog.json")
CONTRACT=json.loads((HERE/"RATA_ADAPTIVE_TIER_CONTRACT_V0_1.json").read_text(encoding="utf-8"))
INPUT=json.loads((HERE/"RATA_T3_COUNTER_INPUT_V0_1.json").read_text(encoding="utf-8"))

T1=CONTRACT["t1"]
T2=CONTRACT["t2"]["recognition"]
BASE_ARM=T1["selector"]["selected_signal_arm"]
COUNTER_DICE=INPUT["damage_reference"]["expression"]

FROZEN_T2={
    "memory_window":int(T2["memory_window"]),
    "repeated_same_category_required":int(T2["repeated_same_category_required"]),
    "preemptive_survival_bonus":float(T2["preemptive_survival_bonus"]),
    "count_results":list(T2["count_results"]),
}

PRESETS={
    "smoke":{"natural_fights":2,"mutant_fights":1},
    "directed":{"natural_fights":500,"mutant_fights":100},
    "heavy":{"natural_fights":2000,"mutant_fights":500},
}


def paths_for(root):
    return {tid:() for tid in engine.ROOT_TECHNIQUES[root]}


@dataclass
class ObservationState:
    memory:list[dict]=field(default_factory=list)
    pending_prediction:str|None=None
    predictions:int=0
    predictions_correct:int=0
    predictions_false:int=0
    current_action_category:str|None=None
    actual_categories:list[str]=field(default_factory=list)

    def finish_action(self,category:str,result:str)->None:
        if self.pending_prediction is not None:
            self.predictions+=1
            if category==self.pending_prediction:
                self.predictions_correct+=1
            else:
                self.predictions_false+=1
            self.pending_prediction=None
        self.actual_categories.append(category)
        self.memory.append(observe(category,result))
        if len(self.memory)>8:
            self.memory=self.memory[-8:]


@dataclass
class CounterFightState:
    queued:dict|None=None
    counter_used:bool=False
    counter_rounds:set[int]=field(default_factory=set)
    reflejo_caused_misses:int=0
    recognition_reflejo_misses:int=0
    confirmed_reflejo_misses:int=0
    candidate_eligible:int=0
    counter_activations:int=0
    counter_damage_events:list[float]=field(default_factory=list)
    false_counters:int=0
    duplicate_same_round_attempts:int=0

    def metrics(self,obs:ObservationState)->dict:
        return {
            "reflejo_caused_misses":self.reflejo_caused_misses,
            "recognition_reflejo_misses":self.recognition_reflejo_misses,
            "confirmed_reflejo_misses":self.confirmed_reflejo_misses,
            "candidate_eligible":self.candidate_eligible,
            "counter_activations":self.counter_activations,
            "counter_damage_events":list(self.counter_damage_events),
            "counter_damage_total":sum(self.counter_damage_events),
            "false_counters":self.false_counters,
            "duplicate_same_round_attempts":self.duplicate_same_round_attempts,
            "prediction_count":obs.predictions,
            "prediction_accuracy":(
                obs.predictions_correct/obs.predictions if obs.predictions else 0.0
            ),
            "action_diversity":len(set(obs.actual_categories)),
            "player_actions":len(obs.actual_categories),
        }


def _base_monster_evasion_without_reflejo(state)->float:
    e=float(state.monster.effective("evasion"))
    if state.peso["duration"]>0:
        e-=float(state.peso["stacks"])*float(state.peso["per_stack"])
    return e


def _player_precision_for_action(state,c,basic:bool)->float:
    p=state.player
    if basic:
        precision_mod=0.0
    else:
        precision_mod=float(c["precision_mod"])
        if state.resonance and c["root"]=="tierra":
            precision_mod+=float(state.resonance["precision"])
        if state.player_next_wind and c["root"]=="viento":
            precision_mod+=float(state.player_next_wind["precision"])
        if c["technique_id"]=="golpe_montana":
            precision_mod+=float(state.player_next_golpe_precision)
        if c["technique_id"]=="latigazo_marea":
            precision_mod+=float(state.next_latigazo_precision)
    return float(p.effective("precision"))+precision_mod


def _counter_damage_dice(state,candidate:dict|None)->str:
    if candidate is None:
        return COUNTER_DICE
    mode=candidate.get("counter_damage_mode","FIXED")
    if mode=="INSTANCE_BASIC":
        return str(state.monster_profile["stats"]["basic_damage"])
    if mode=="FIXED":
        return str(candidate.get("counter_damage_expression",COUNTER_DICE))
    raise ValueError(f"unsupported counter_damage_mode: {mode}")


def _candidate_allows(candidate:dict,*,recognition:bool,confirmed:bool,
                      caused_miss:bool,counter_used:bool)->bool:
    if not caused_miss:
        return False
    if candidate.get("requires_t2_recognition_active") and not recognition:
        return False
    if candidate.get("requires_prediction_confirmed") and not confirmed:
        return False
    if candidate.get("counter_limit")=="ONCE_PER_FIGHT" and counter_used:
        return False
    return True


@contextmanager
def player_runtime(obs:ObservationState,cstate:CounterFightState,candidate:dict|None):
    originals={
        "compile_build":engine.compile_build,
        "choose_player_action":engine.choose_player_action,
        "execute_player_technique":engine.execute_player_technique,
        "execute_basic":engine.execute_basic,
        "resolve_player_direct":engine.resolve_player_direct,
    }

    def compile_build(root,paths,catalog=None):
        compiled=dict(originals["compile_build"](root,paths,catalog))
        compiled[VETERAN_BASIC]={
            "technique_id":VETERAN_BASIC,
            "name":"Ataque básico",
            "root":root,
            "role":"BASIC_PROXY",
            "targeting":"UNITARGET",
            "qi_cost":BASIC_PROXY_SENTINEL_COST,
        }
        return compiled

    def choose_action(state,policy):
        if policy!="VETERAN":
            return originals["choose_player_action"](state,policy)
        return choose_veteran_action(state,DEFAULT_VETERAN_CONFIG)

    def resolve_player(state,rng,c,basic=False):
        survival=state.monster_survival
        reflejo=bool(survival and survival.get("kind")=="EVADE_NEXT")
        recognition=bool(reflejo and survival.get("t2_recognition_active",False))
        predicted=survival.get("predicted_category") if reflejo else None
        actual_category=obs.current_action_category

        caused_miss=False
        if reflejo:
            shadow=random.Random()
            shadow.setstate(rng.getstate())
            hit_roll=shadow.random()
            precision=_player_precision_for_action(state,c,basic)
            base_eva=_base_monster_evasion_without_reflejo(state)
            boosted_eva=base_eva+float(survival["evasion_bonus"])
            base_phit=engine.clamp(precision-base_eva,5,100)/100
            boosted_phit=engine.clamp(precision-boosted_eva,5,100)/100
            would_hit_base=hit_roll<base_phit
            would_hit_boosted=hit_roll<boosted_phit
        else:
            would_hit_base=None
            would_hit_boosted=None

        out=originals["resolve_player_direct"](state,rng,c,basic)

        if reflejo:
            if bool(out["hit"])!=bool(would_hit_boosted):
                raise AssertionError("Reflejo causal mirror drifted from combat resolver")
            caused_miss=bool(would_hit_base and not out["hit"])

        if caused_miss:
            cstate.reflejo_caused_misses+=1
            if recognition:
                cstate.recognition_reflejo_misses+=1
            confirmed=bool(
                recognition
                and predicted is not None
                and actual_category is not None
                and actual_category==predicted
            )
            if confirmed:
                cstate.confirmed_reflejo_misses+=1

            if candidate is not None and _candidate_allows(
                candidate,
                recognition=recognition,
                confirmed=confirmed,
                caused_miss=True,
                counter_used=cstate.counter_used,
            ):
                cstate.candidate_eligible+=1
                if state.round_no in cstate.counter_rounds:
                    cstate.duplicate_same_round_attempts+=1
                else:
                    cstate.queued={
                        "round":int(state.round_no),
                        "predicted_category":predicted,
                        "actual_category":actual_category,
                        "prediction_confirmed":confirmed,
                    }
        return out

    def execute_basic_observed(state,rng):
        prior=obs.current_action_category
        obs.current_action_category="PLAYER_BASIC"
        try:
            originals["execute_basic"](state,rng)
            result="EFECTIVA" if state.last_player_hp_damage_to_monster>0 else "FALLIDA"
            obs.finish_action("PLAYER_BASIC",result)
        finally:
            obs.current_action_category=prior

    def execute_action(state,rng,c):
        if c.get("technique_id")==VETERAN_BASIC:
            execute_basic_observed(state,rng)
            return True

        category=classify_player_action(c)
        prior=obs.current_action_category
        obs.current_action_category=category
        try:
            ok=originals["execute_player_technique"](state,rng,c)
            if not ok:
                return False
            if c.get("role")=="DEFENSIVE":
                result="EFECTIVA"
            else:
                result="EFECTIVA" if state.last_player_hp_damage_to_monster>0 else "FALLIDA"
            obs.finish_action(category,result)
            return True
        finally:
            obs.current_action_category=prior

    engine.compile_build=compile_build
    engine.choose_player_action=choose_action
    engine.resolve_player_direct=resolve_player
    engine.execute_player_technique=execute_action
    engine.execute_basic=execute_basic_observed
    try:
        yield
    finally:
        for k,v in originals.items():
            setattr(engine,k,v)


@contextmanager
def adaptive_runtime(*,tier:str,candidate:dict|None,decision_seed:int,obs:ObservationState,
                     cstate:CounterFightState,counters:Counter):
    originals={
        "build_monster":engine.build_monster,
        "execute_monster_turn":engine.execute_monster_turn,
    }
    rng_ai=Mulberry32(decision_seed)

    def build_monster(profile,requested_tier):
        if profile.get("id")!=RATA_ID or requested_tier!=tier:
            raise RuntimeError("Rata T3 LAB tier mismatch")
        return originals["build_monster"](profile,"T0")

    def execute_monster_turn(state,rng):
        # T3 is an extra reactive packet before the ordinary T2-governed turn.
        if tier=="T3" and cstate.queued is not None and state.player.alive():
            q=cstate.queued
            cstate.queued=None
            cstate.counter_rounds.add(int(state.round_no))
            counter_dice=_counter_damage_dice(state,candidate)
            out=engine.resolve_monster_direct(state,rng,counter_dice)
            counters[f"counter_dice:{counter_dice}"]+=1
            damage=float(out.get("actual_hp_damage",0))
            cstate.counter_activations+=1
            cstate.counter_damage_events.append(damage)
            cstate.counter_used=True
            counters["counter_activations"]+=1
            counters["counter_damage"]+=damage
            if not q["prediction_confirmed"]:
                cstate.false_counters+=1
                counters["false_counters"]+=1
            if not state.player.alive():
                return

        low=float(BASE_ARM["self_low_hp_ratio"])
        heavy_ratio=float(BASE_ARM["heavy_hit_ratio"])
        self_low=(state.monster.hp/state.monster.hp_max)<=low
        heavy=float(state.last_player_hp_damage_to_monster)>=heavy_ratio*state.monster.hp_max
        player_low=(state.player.hp/state.player.hp_max)<=low
        signals={
            "SELF_LOW_HP":self_low,
            "TOOK_HEAVY_HIT":heavy,
            "PLAYER_LOW_HP":player_low,
        }

        recog=recognize_recent_pattern(obs.memory,FROZEN_T2)
        counters["recognition_checks"]+=1
        counters["recognition_triggers"]+=int(recog["recognized"])

        decision=choose_rata_t2_intent(
            signals=signals,
            recent_actions=list(state.monster_recent_actions),
            survival_on_cooldown=state.monster_survival_cd>0,
            recognition_active=bool(recog["recognized"]),
            recognition_bonus=float(FROZEN_T2["preemptive_survival_bonus"]),
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
            if applied>0:
                counters["survival_with_recognition"]+=1
            state.monster_survival={
                "kind":"EVADE_NEXT",
                "evasion_bonus":40.0,
                "t2_recognition_active":bool(recog["recognized"]),
                "predicted_category":recog["category"] if recog["recognized"] else None,
            }
            state.monster_survival_cd=6
            state.metrics.adaptation_procs+=1
            state.monster_recent_actions.append("SURVIVAL")
            if state.arrastre_locked:
                state.arrastre_locked=False
                state.arrastre_precision_debuff=0.0
            return

        counters["basic"]+=1
        return originals["execute_monster_turn"](state,rng)

    engine.build_monster=build_monster
    engine.execute_monster_turn=execute_monster_turn
    try:
        yield
    finally:
        for k,v in originals.items():
            setattr(engine,k,v)


def sample_mutant(context_id,root,index,namespace):
    for attempt in range(30000):
        seed=stable_seed(
            "RATA_T3_COUNTER_V01","MUTANT_INSTANCE",
            namespace,context_id,root,index,attempt,
        )
        inst=instantiate(RATA_ID,seed)
        if inst["mutant"]:
            return inst
    raise RuntimeError("Mutante sampler exhausted")


def run_once(profile,root,items,combat_seed,tier,candidate,ai_seed,policy="VETERAN"):
    obs=ObservationState()
    cstate=CounterFightState()
    counters=Counter()
    kwargs=dict(
        stage="LianQi_I",
        root=root,
        item_ids=items,
        paths=paths_for(root),
        monster_profile=profile,
        tier=tier,
        policy=policy,
        seed=combat_seed,
        technique_catalog=TECHNIQUES,
        equipment_catalog=EQUIPMENT,
        max_rounds=100,
        signal_bridge=engine.LabSignalBridge(
            low_hp_ratio=float(BASE_ARM["self_low_hp_ratio"]),
            heavy_hit_ratio=float(BASE_ARM["heavy_hit_ratio"]),
        ),
    )
    with player_runtime(obs,cstate,candidate if tier=="T3" else None):
        with adaptive_runtime(
            tier=tier,
            candidate=candidate if tier=="T3" else None,
            decision_seed=ai_seed,
            obs=obs,
            cstate=cstate,
            counters=counters,
        ):
            row=fight_once_observed(**kwargs)
    return row,cstate.metrics(obs),counters


class T3Aggregate:
    def __init__(self):
        self.combat=StreamingAggregate()
        self.fights=0
        self.sum=Counter()
        self.counter_event_damage=[]
        self.action_diversity=[]
        self.counter_count_per_fight=[]

    def add(self,row,extra):
        self.combat.add(row)
        self.fights+=1
        for key in (
            "reflejo_caused_misses",
            "recognition_reflejo_misses",
            "confirmed_reflejo_misses",
            "candidate_eligible",
            "counter_activations",
            "counter_damage_total",
            "false_counters",
            "duplicate_same_round_attempts",
            "prediction_count",
            "player_actions",
        ):
            self.sum[key]+=float(extra[key])
        self.counter_event_damage.extend(float(x) for x in extra["counter_damage_events"])
        self.action_diversity.append(float(extra["action_diversity"]))
        self.counter_count_per_fight.append(float(extra["counter_activations"]))

    def finish(self):
        c=self.combat.finish()
        s=self.sum
        activ=s["counter_activations"]
        eligible=s["candidate_eligible"]
        recognition_miss=s["recognition_reflejo_misses"]
        return {
            **c,
            "t3":{
                "reflejo_caused_miss_mean":s["reflejo_caused_misses"]/self.fights,
                "recognition_reflejo_miss_mean":recognition_miss/self.fights,
                "confirmed_reflejo_miss_mean":s["confirmed_reflejo_misses"]/self.fights,
                "counter_eligibility_per_fight":eligible/self.fights,
                "counter_activation_per_fight":activ/self.fights,
                "counter_activation_per_eligible":activ/eligible if eligible else 0.0,
                "counter_damage_per_fight":s["counter_damage_total"]/self.fights,
                "counter_damage_per_activation":s["counter_damage_total"]/activ if activ else 0.0,
                "counter_damage_p90_per_activation":percentile(self.counter_event_damage,.90) if self.counter_event_damage else 0.0,
                "false_counter_rate":s["false_counters"]/activ if activ else 0.0,
                "prediction_confirmed_rate_at_recognition_miss":(
                    s["confirmed_reflejo_misses"]/recognition_miss if recognition_miss else 0.0
                ),
                "action_diversity_mean":statistics.fmean(self.action_diversity),
                "multi_counter_fight_rate":sum(x>1 for x in self.counter_count_per_fight)/self.fights,
                "max_counters_in_one_fight":max(self.counter_count_per_fight,default=0.0),
                "degenerate_counter_loop_count":int(s["duplicate_same_round_attempts"]),
            }
        }


def evaluate(canonical,*,tier,candidate,natural_n,mutant_n,namespace,policy="VETERAN"):
    natural=T3Aggregate()
    normal=T3Aggregate()
    observed_mut=T3Aggregate()
    forced_mut=T3Aggregate()

    for ctx in PRIMARY_CONTEXTS:
        items=EQUIPMENT["simulation_loadouts"][ctx.loadout_profile]["LianQi_I"]
        for root in ROOTS:
            for i in range(natural_n):
                inst=instantiate(
                    RATA_ID,
                    stable_seed(
                        "RATA_T3_COUNTER_V01","NATURAL_INSTANCE",
                        namespace,ctx.context_id,root,i,
                    ),
                )
                profile=profile_from_instance(canonical,inst)
                combat_seed=stable_seed(
                    "RATA_T3_COUNTER_V01","NATURAL_COMBAT",
                    namespace,ctx.context_id,root,i,
                )
                ai_seed=stable_seed(
                    "RATA_T3_COUNTER_V01","AI",
                    namespace,ctx.context_id,root,i,
                )&0xFFFFFFFF
                row,extra,_=run_once(
                    profile,root,items,combat_seed,tier,candidate,ai_seed,policy
                )
                row["loadout_profile"]=ctx.loadout_profile
                natural.add(row,extra)
                (observed_mut if inst["mutant"] else normal).add(row,extra)

            for i in range(mutant_n):
                inst=sample_mutant(ctx.context_id,root,i,namespace)
                profile=profile_from_instance(canonical,inst)
                combat_seed=stable_seed(
                    "RATA_T3_COUNTER_V01","MUTANT_COMBAT",
                    namespace,ctx.context_id,root,i,
                )
                ai_seed=stable_seed(
                    "RATA_T3_COUNTER_V01","MUTANT_AI",
                    namespace,ctx.context_id,root,i,
                )&0xFFFFFFFF
                row,extra,_=run_once(
                    profile,root,items,combat_seed,tier,candidate,ai_seed,policy
                )
                row["loadout_profile"]=ctx.loadout_profile
                forced_mut.add(row,extra)

    def done(a):
        return a.finish() if a.fights else None

    return {
        "natural_all":done(natural),
        "natural_normal":done(normal),
        "natural_mutant_observed":done(observed_mut),
        "mutant_conditional":done(forced_mut),
    }


def delta(a,b):
    return {
        "win_rate_delta":float(a["win_rate"])-float(b["win_rate"]),
        "rounds_delta":float(a["rounds_mean"])-float(b["rounds_mean"]),
        "hp_pressure_delta":(
            (1-float(a["hp_final_pct_mean"]))
            -(1-float(b["hp_final_pct_mean"]))
        ),
        "qi_spent_delta":float(a["qi_spent_mean"])-float(b["qi_spent_mean"]),
        "monster_damage_delta":(
            float(a["monster_damage_total_mean"])
            -float(b["monster_damage_total_mean"])
        ),
        "counter_damage_per_fight":float(a["t3"]["counter_damage_per_fight"]),
        "counter_activation_per_fight":float(a["t3"]["counter_activation_per_fight"]),
    }


def write_json(path,obj):
    Path(path).write_text(
        json.dumps(obj,ensure_ascii=False,indent=2,sort_keys=True)+"\n",
        encoding="utf-8",
    )


def write_gz(path,obj):
    with gzip.open(path,"wt",encoding="utf-8",compresslevel=9) as f:
        json.dump(obj,f,ensure_ascii=False,sort_keys=True,separators=(",",":"))


def zip_results(outdir):
    z=outdir/"RESULTADOS_RATA_T3_COUNTER_V01.zip"
    with zipfile.ZipFile(z,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as zz:
        for p in outdir.rglob("*"):
            if p.is_file() and p!=z:
                zz.write(p,p.relative_to(outdir))
    return z


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--preset",choices=PRESETS,default="heavy")
    ap.add_argument("--natural-fights",type=int)
    ap.add_argument("--mutant-fights",type=int)
    ap.add_argument("--outdir",default="RATA_T3_COUNTER_V01")
    ap.add_argument("--namespace",default="RUN")
    ap.add_argument(
        "--policy",
        choices=["VETERAN","UNITARGET_FIRST","AOE_FIRST","DEFENSE_OPEN","ROTATION"],
        default="VETERAN",
    )
    args=ap.parse_args()

    cfg=dict(PRESETS[args.preset])
    if args.natural_fights is not None:
        cfg["natural_fights"]=args.natural_fights
    if args.mutant_fights is not None:
        cfg["mutant_fights"]=args.mutant_fights

    registry=load_registry()
    canonical=require_ready_profile(RATA_ID,registry)
    if canonical["adaptive"]["status"]!="T2_READY_FOR_T3_CALIBRATION":
        raise RuntimeError("T3 calibration gate is not open")

    if T1["ability"]["evasion_bonus"]!=40 or T1["ability"]["cooldown_rounds"]!=5:
        raise RuntimeError("frozen T1 drift")
    if (
        FROZEN_T2["memory_window"]!=2
        or FROZEN_T2["repeated_same_category_required"]!=2
        or FROZEN_T2["count_results"]!=["EFECTIVA"]
        or FROZEN_T2["preemptive_survival_bonus"]!=8
    ):
        raise RuntimeError("frozen T2 drift")
    if COUNTER_DICE!="2d4":
        raise RuntimeError("T3 initial damage reference must remain canonical 2d4")

    outdir=Path(args.outdir)
    outdir.mkdir(parents=True,exist_ok=True)

    print("Frozen T2 baseline",flush=True)
    t2=evaluate(
        canonical,
        tier="T2",
        candidate=None,
        natural_n=cfg["natural_fights"],
        mutant_n=cfg["mutant_fights"],
        namespace=args.namespace,
        policy=args.policy,
    )

    rows=[]
    for candidate in INPUT["candidate_triggers"]:
        print("T3",candidate["label"],flush=True)
        t3=evaluate(
            canonical,
            tier="T3",
            candidate=candidate,
            natural_n=cfg["natural_fights"],
            mutant_n=cfg["mutant_fights"],
            namespace=args.namespace,
            policy=args.policy,
        )
        rows.append({
            "candidate":candidate,
            "result":t3,
            "delta_vs_frozen_t2":{
                "natural_normal":delta(t3["natural_normal"],t2["natural_normal"]),
                "mutant_conditional":delta(t3["mutant_conditional"],t2["mutant_conditional"]),
            },
        })

    write_gz(outdir/"frozen_t2_baseline.json.gz",t2)
    write_gz(outdir/"t3_results.json.gz",rows)
    write_json(outdir/"SUMMARY.json",{
        "experiment":"RATA_T3_COUNTER_V01",
        "status":"LAB_RESULTS_AWAITING_HUMAN_REVIEW",
        "player_policy":args.policy,
        "natural_fights_per_context":cfg["natural_fights"],
        "mutant_fights_per_context":cfg["mutant_fights"],
        "contexts":10,
        "t1_frozen":True,
        "t2_frozen":True,
        "t3_candidates":INPUT["candidate_triggers"],
        "counter_damage_reference":"2d4",
        "reflejo_causal_miss_detection":True,
        "canonical_write":False,
        "t4_executed":False,
    })
    write_json(outdir/"MANIFEST.json",{
        "t1":"READY_HUMAN_RATIFIED",
        "t2":"R2_SHORT_READY_HUMAN_RATIFIED",
        "t3":"TRIGGER_SEMANTICS_ONLY",
        "counter_damage_pipeline":"normal monster direct damage",
        "counter_damage_reference":"canonical T0 2d4",
        "causal_reflejo_miss":"same hit roll: natural EVA would hit, +40 EVA misses",
        "no_root_build_inspection":True,
        "no_qi_drain":True,
        "no_dot":True,
        "no_control":True,
        "canonical_write":False,
        "t4_forbidden":True,
    })
    print("DONE",zip_results(outdir),flush=True)


if __name__=="__main__":
    main()
