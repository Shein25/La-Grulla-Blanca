"""Rata T4 Mordisco Frenético — Phase A geometry lab.

Frozen:
- T1 Reflejo +40 EVA / CD5 / REACTIVO_1 / BASE
- T2 R2_SHORT memory2/repeat2/EFECTIVA/+8
- T3 CONFIRMED_PATTERN_REFLEJO_MISS + INSTANCE_BASIC

T4 integration:
T2 chooses SURVIVAL -> keep Reflejo.
T2 chooses BASIC:
    Mordisco ready -> replace that BASIC with Mordisco Frenético.
    otherwise      -> ordinary BASIC.

Phase A changes only hit_count and scalar_per_hit.
Precision: independent per hit.
Critical: independent per hit.
Cooldown: 5 rounds.
Source dice: canonical 2d4.
"""
from __future__ import annotations

import argparse
from collections import Counter
from contextlib import contextmanager
from dataclasses import dataclass,field
import gzip,json,statistics,sys,zipfile
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
from seeds import stable_seed
from streaming import StreamingAggregate,percentile
from telemetry import fight_once_observed
from decision_kernel_mirror import Mulberry32,SURVIVAL_ID
from recognition_kernel import recognize_recent_pattern
from t2_decision_kernel import choose_rata_t2_intent
from rata_t3_counter_lab import (
    ObservationState,
    CounterFightState,
    player_runtime,
    paths_for,
    _counter_damage_dice,
)

RATA_ID="rata_qi"
TECHNIQUES=engine.load_json(BALANCE/"techniques_arc1_catalog.json")
EQUIPMENT=engine.load_json(BALANCE/"equipment_arc1_catalog.json")
CONTRACT=json.loads((HERE/"RATA_ADAPTIVE_TIER_CONTRACT_V0_1.json").read_text(encoding="utf-8"))
INPUT=json.loads((HERE/"RATA_T4_MORDISCO_INPUT_V0_1.json").read_text(encoding="utf-8"))

T1=CONTRACT["t1"]
T2=CONTRACT["t2"]["recognition"]
BASE_ARM=T1["selector"]["selected_signal_arm"]
FROZEN_T2={
    "memory_window":int(T2["memory_window"]),
    "repeated_same_category_required":int(T2["repeated_same_category_required"]),
    "preemptive_survival_bonus":float(T2["preemptive_survival_bonus"]),
    "count_results":list(T2["count_results"]),
}
T3_CANDIDATE={
    "label":"CONFIRMED_PATTERN_REFLEJO_MISS_INSTANCE_BASIC",
    "requires_t2_recognition_active":True,
    "requires_prediction_confirmed":True,
    "requires_t1_reflejo_active":True,
    "requires_player_attack_miss":True,
    "counter_limit":"NO_EXTRA_LIMIT_BEYOND_T1_GATE",
    "counter_damage_mode":"INSTANCE_BASIC",
}
FIXED=INPUT["phase_a_geometry"]["fixed_axes"]

PRESETS={
    "smoke":{"natural_fights":2,"mutant_fights":1},
    "directed":{"natural_fights":500,"mutant_fights":100},
    "heavy":{"natural_fights":2000,"mutant_fights":500},
}


@dataclass
class T4FightState:
    next_ready_round:int=1
    uses:int=0
    packets:int=0
    hits:int=0
    crits:int=0
    damage:float=0.0
    use_damage:list[float]=field(default_factory=list)
    use_packets:list[int]=field(default_factory=list)

    def as_dict(self):
        return {
            "uses":self.uses,
            "packets":self.packets,
            "hits":self.hits,
            "crits":self.crits,
            "damage":self.damage,
            "use_damage":list(self.use_damage),
            "use_packets":list(self.use_packets),
        }


def _scaled_direct_packet(state,rng,scalar:float,dice_expr:str)->dict:
    """Use the authoritative direct resolver while scaling only the chosen roll."""
    original_roll=engine.roll_dice
    def scaled_roll(inner_rng,dice):
        if dice!=dice_expr:
            raise AssertionError(f"T4 packet expected {dice_expr}, got {dice}")
        return original_roll(inner_rng,dice)*float(scalar)
    engine.roll_dice=scaled_roll
    try:
        return engine.resolve_monster_direct(state,rng,dice_expr)
    finally:
        engine.roll_dice=original_roll


def _execute_mordisco(state,rng,candidate,t4:T4FightState):
    hit_count=int(candidate["hit_count"])
    scalar=float(candidate["scalar_per_hit"])
    source_mode=candidate.get("source_mode","CANONICAL_2D4")
    if source_mode=="CANONICAL_2D4":
        dice_expr="2d4"
    elif source_mode=="INSTANCE_BASIC":
        dice_expr=str(state.monster_profile["stats"]["basic_damage"])
    else:
        raise ValueError(f"unsupported T4 source_mode: {source_mode}")
    if hit_count<1 or scalar<=0:
        raise ValueError("invalid T4 geometry")

    t4.uses+=1
    t4.next_ready_round=int(state.round_no)+int(FIXED["cooldown_rounds"])
    before=float(state.player.hp)
    packets=0
    for _ in range(hit_count):
        if not state.player.alive():
            break
        out=_scaled_direct_packet(state,rng,scalar,dice_expr)
        packets+=1
        t4.packets+=1
        t4.hits+=int(bool(out.get("hit")))
        t4.crits+=int(bool(out.get("critical",False)))
    dealt=max(0.0,before-float(state.player.hp))
    t4.damage+=dealt
    t4.use_damage.append(dealt)
    t4.use_packets.append(packets)
    state.monster_recent_actions.append("BASIC")
    if state.arrastre_locked:
        state.arrastre_locked=False
        state.arrastre_precision_debuff=0.0


@contextmanager
def adaptive_runtime(*,tier,candidate,decision_seed,obs,cstate,t4,counters):
    originals={
        "build_monster":engine.build_monster,
        "execute_monster_turn":engine.execute_monster_turn,
    }
    rng_ai=Mulberry32(decision_seed)

    def build_monster(profile,requested_tier):
        if profile.get("id")!=RATA_ID or requested_tier!=tier:
            raise RuntimeError("Rata T4 geometry LAB tier mismatch")
        if tier not in {"T3","T4"}:
            raise RuntimeError("T4 geometry LAB supports frozen T3 baseline or T4 only")
        return originals["build_monster"](profile,"T0")

    def execute_monster_turn(state,rng):
        # Frozen ratified T3 reactive counter.
        if cstate.queued is not None and state.player.alive():
            q=cstate.queued
            cstate.queued=None
            cstate.counter_rounds.add(int(state.round_no))
            out=engine.resolve_monster_direct(
                state,rng,_counter_damage_dice(state,T3_CANDIDATE)
            )
            damage=float(out.get("actual_hp_damage",0))
            cstate.counter_activations+=1
            cstate.counter_damage_events.append(damage)
            cstate.counter_used=True
            counters["t3_counter_activations"]+=1
            counters["t3_counter_damage"]+=damage
            if not q["prediction_confirmed"]:
                raise AssertionError("ratified T3 emitted an unconfirmed counter")
            if not state.player.alive():
                return

        # Frozen ratified T2 decision layer.
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
        if recog["recognized"]:
            obs.pending_prediction=recog["category"]

        if decision.ability_id==SURVIVAL_ID:
            counters["survival"]+=1
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

        counters["basic_decisions"]+=1
        if (
            tier=="T4"
            and candidate is not None
            and int(state.round_no)>=int(t4.next_ready_round)
        ):
            counters["t4_replacements"]+=1
            _execute_mordisco(state,rng,candidate,t4)
            return

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
            "RATA_T4_MORDISCO_GEOMETRY_V01","MUTANT_INSTANCE",
            namespace,context_id,root,index,attempt,
        )
        inst=instantiate(RATA_ID,seed)
        if inst["mutant"]:
            return inst
    raise RuntimeError("Mutante sampler exhausted")


def run_once(profile,root,items,combat_seed,tier,candidate,ai_seed,policy="VETERAN"):
    obs=ObservationState()
    cstate=CounterFightState()
    t4=T4FightState()
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
    with player_runtime(obs,cstate,T3_CANDIDATE):
        with adaptive_runtime(
            tier=tier,candidate=candidate,decision_seed=ai_seed,
            obs=obs,cstate=cstate,t4=t4,counters=counters,
        ):
            row=fight_once_observed(**kwargs)
    return row,t4.as_dict(),cstate.metrics(obs),counters


class Aggregate:
    def __init__(self):
        self.combat=StreamingAggregate()
        self.fights=0
        self.sum=Counter()
        self.use_damage=[]
        self.uses_per_fight=[]

    def add(self,row,t4,t3,counters):
        self.combat.add(row)
        self.fights+=1
        self.sum["t4_uses"]+=t4["uses"]
        self.sum["t4_packets"]+=t4["packets"]
        self.sum["t4_hits"]+=t4["hits"]
        self.sum["t4_crits"]+=t4["crits"]
        self.sum["t4_damage"]+=t4["damage"]
        self.sum["t3_counters"]+=t3["counter_activations"]
        self.sum["survival"]+=counters["survival"]
        self.sum["basic_decisions"]+=counters["basic_decisions"]
        self.use_damage.extend(float(x) for x in t4["use_damage"])
        self.uses_per_fight.append(float(t4["uses"]))

    def finish(self):
        c=self.combat.finish()
        uses=float(self.sum["t4_uses"])
        packets=float(self.sum["t4_packets"])
        hits=float(self.sum["t4_hits"])
        return {
            **c,
            "t4":{
                "uses_per_fight":uses/self.fights,
                "packets_per_fight":packets/self.fights,
                "packets_per_use":packets/uses if uses else 0.0,
                "packet_hit_rate":hits/packets if packets else 0.0,
                "crit_per_connected_hit":self.sum["t4_crits"]/hits if hits else 0.0,
                "damage_per_fight":self.sum["t4_damage"]/self.fights,
                "damage_per_use":self.sum["t4_damage"]/uses if uses else 0.0,
                "damage_p90_per_use":percentile(self.use_damage,.90) if self.use_damage else 0.0,
                "multi_use_fight_rate":sum(x>1 for x in self.uses_per_fight)/self.fights,
                "max_uses_one_fight":max(self.uses_per_fight,default=0.0),
                "t3_counter_per_fight":self.sum["t3_counters"]/self.fights,
                "survival_choices_per_fight":self.sum["survival"]/self.fights,
                "basic_decisions_per_fight":self.sum["basic_decisions"]/self.fights,
            }
        }


def evaluate(canonical,*,tier,candidate,natural_n,mutant_n,namespace,policy="VETERAN"):
    natural=Aggregate();normal=Aggregate();observed_mut=Aggregate();forced_mut=Aggregate()

    for ctx in PRIMARY_CONTEXTS:
        items=EQUIPMENT["simulation_loadouts"][ctx.loadout_profile]["LianQi_I"]
        for root in ROOTS:
            for i in range(natural_n):
                inst=instantiate(
                    RATA_ID,
                    stable_seed(
                        "RATA_T4_MORDISCO_GEOMETRY_V01","NATURAL_INSTANCE",
                        namespace,ctx.context_id,root,i,
                    ),
                )
                profile=profile_from_instance(canonical,inst)
                combat_seed=stable_seed(
                    "RATA_T4_MORDISCO_GEOMETRY_V01","NATURAL_COMBAT",
                    namespace,ctx.context_id,root,i,
                )
                ai_seed=stable_seed(
                    "RATA_T4_MORDISCO_GEOMETRY_V01","AI",
                    namespace,ctx.context_id,root,i,
                )&0xFFFFFFFF
                row,t4,t3,cnt=run_once(
                    profile,root,items,combat_seed,tier,candidate,ai_seed,policy
                )
                row["loadout_profile"]=ctx.loadout_profile
                natural.add(row,t4,t3,cnt)
                (observed_mut if inst["mutant"] else normal).add(row,t4,t3,cnt)

            for i in range(mutant_n):
                inst=sample_mutant(ctx.context_id,root,i,namespace)
                profile=profile_from_instance(canonical,inst)
                combat_seed=stable_seed(
                    "RATA_T4_MORDISCO_GEOMETRY_V01","MUTANT_COMBAT",
                    namespace,ctx.context_id,root,i,
                )
                ai_seed=stable_seed(
                    "RATA_T4_MORDISCO_GEOMETRY_V01","MUTANT_AI",
                    namespace,ctx.context_id,root,i,
                )&0xFFFFFFFF
                row,t4,t3,cnt=run_once(
                    profile,root,items,combat_seed,tier,candidate,ai_seed,policy
                )
                row["loadout_profile"]=ctx.loadout_profile
                forced_mut.add(row,t4,t3,cnt)

    def done(a):return a.finish() if a.fights else None
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
            (1-float(a["hp_final_pct_mean"]))-(1-float(b["hp_final_pct_mean"]))
        ),
        "qi_spent_delta":float(a["qi_spent_mean"])-float(b["qi_spent_mean"]),
        "monster_damage_delta":(
            float(a["monster_damage_total_mean"])-float(b["monster_damage_total_mean"])
        ),
        "survival_choices_delta":(
            float(a["t4"]["survival_choices_per_fight"])
            -float(b["t4"]["survival_choices_per_fight"])
        ),
        "t3_counter_delta":(
            float(a["t4"]["t3_counter_per_fight"])
            -float(b["t4"]["t3_counter_per_fight"])
        ),
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
    z=outdir/"RESULTADOS_RATA_T4_MORDISCO_GEOMETRY_V01.zip"
    with zipfile.ZipFile(z,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as zz:
        for p in outdir.rglob("*"):
            if p.is_file() and p!=z:
                zz.write(p,p.relative_to(outdir))
    return z


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--preset",choices=PRESETS,default="directed")
    ap.add_argument("--natural-fights",type=int)
    ap.add_argument("--mutant-fights",type=int)
    ap.add_argument("--outdir",default="RATA_T4_MORDISCO_GEOMETRY_V01")
    ap.add_argument("--namespace",default="RUN")
    ap.add_argument(
        "--policy",
        choices=["VETERAN","UNITARGET_FIRST","AOE_FIRST","DEFENSE_OPEN","ROTATION"],
        default="VETERAN",
    )
    args=ap.parse_args()
    cfg=dict(PRESETS[args.preset])
    if args.natural_fights is not None:cfg["natural_fights"]=args.natural_fights
    if args.mutant_fights is not None:cfg["mutant_fights"]=args.mutant_fights

    registry=load_registry()
    canonical=require_ready_profile(RATA_ID,registry)
    if canonical["adaptive"]["status"]!="T3_READY_FOR_T4_CALIBRATION":
        raise RuntimeError("T4 calibration gate is not open")

    if CONTRACT["t3"]["status"]!="READY_HUMAN_RATIFIED":
        raise RuntimeError("T3 must remain frozen before T4")
    if FIXED["dice"]!="2d4":
        raise RuntimeError("T4 Phase A must use canonical 2d4")
    if FIXED["precision_rule"]!="INDEPENDENT_PER_HIT":
        raise RuntimeError("Phase A precision rule drift")
    if FIXED["critical_rule"]!="INDEPENDENT_PER_HIT":
        raise RuntimeError("Phase A critical rule drift")

    outdir=Path(args.outdir);outdir.mkdir(parents=True,exist_ok=True)

    print("Frozen T3 baseline",flush=True)
    baseline=evaluate(
        canonical,tier="T3",candidate=None,
        natural_n=cfg["natural_fights"],mutant_n=cfg["mutant_fights"],
        namespace=args.namespace,policy=args.policy,
    )

    harness_candidate={
        "label":"HARNESS_INSTANCE_BASIC_1X100",
        "hit_count":1,
        "scalar_per_hit":1.0,
        "source_mode":"INSTANCE_BASIC",
    }
    print("T4 harness control",flush=True)
    harness=evaluate(
        canonical,tier="T4",candidate=harness_candidate,
        natural_n=cfg["natural_fights"],mutant_n=cfg["mutant_fights"],
        namespace=args.namespace,policy=args.policy,
    )

    rows=[]
    for candidate in INPUT["phase_a_geometry"]["candidates"]:
        print("T4",candidate["label"],flush=True)
        result=evaluate(
            canonical,tier="T4",candidate=candidate,
            natural_n=cfg["natural_fights"],mutant_n=cfg["mutant_fights"],
            namespace=args.namespace,policy=args.policy,
        )
        rows.append({
            "candidate":candidate,
            "fixed_axes":FIXED,
            "result":result,
            "delta_vs_frozen_t3":{
                "natural_normal":delta(result["natural_normal"],baseline["natural_normal"]),
                "mutant_conditional":delta(result["mutant_conditional"],baseline["mutant_conditional"]),
            },
        })

    write_gz(outdir/"frozen_t3_baseline.json.gz",baseline)
    write_gz(outdir/"harness_instance_basic_control.json.gz",harness)
    write_gz(outdir/"t4_geometry_results.json.gz",rows)
    write_json(outdir/"SUMMARY.json",{
        "experiment":"RATA_T4_MORDISCO_GEOMETRY_V01",
        "status":"PHASE_A_GEOMETRY_RESULTS_AWAITING_REVIEW",
        "player_policy":args.policy,
        "contexts":10,
        "natural_fights_per_context":cfg["natural_fights"],
        "mutant_fights_per_context":cfg["mutant_fights"],
        "candidate_count":len(rows),
        "harness_control":"HARNESS_INSTANCE_BASIC_1X100",
        "t1_t3_frozen":True,
        "activation_rule":"REPLACE_BASIC_WHEN_READY",
        "canonical_dice":"2d4",
        "precision_rule":"INDEPENDENT_PER_HIT",
        "critical_rule":"INDEPENDENT_PER_HIT",
        "cooldown_rounds":5,
        "canonical_write":False,
        "tier_above_t4_executed":False,
    })
    write_json(outdir/"MANIFEST.json",{
        "t3_baseline_human_ratified":True,
        "t4_phase":"A_GEOMETRY",
        "scalars_are_lab_hypotheses":True,
        "direct_pipeline_per_hit":True,
        "flat_def_per_hit":True,
        "absorption_per_hit":True,
        "no_qi_drain":True,
        "no_dot":True,
        "no_control":True,
        "canonical_write":False,
        "no_t5":True,
    })
    print("DONE",zip_results(outdir),flush=True)


if __name__=="__main__":
    main()
