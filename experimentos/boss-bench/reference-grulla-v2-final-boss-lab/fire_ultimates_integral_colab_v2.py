#!/usr/bin/env python3
"""
La Grulla Blanca — Definitivas de Fuego · benchmark integral I→II→III
LAB ONLY / NO RUNTIME / NO MERGE / NO CANON.

Designed for Google Colab. It imports the current ETAPA19B engine and the Grulla
boss lab, then compares each Fire-family ultimate against a PAIRED no-ultimate
baseline using the same root/build/loadout/consumables/policy.

Important LAB bridge: the current Arc-1 engine compiles one normal-technique root
at a time. Combination ultimates are therefore tested in the secondary root's
native ecosystem (Tierra/Metal/Agua/Viento) while the ultimate supplies the Fire
half. Conclusions are based on uplift vs the paired baseline, not raw cross-root
win-rate ranking.
"""
from __future__ import annotations

import argparse, copy, csv, json, math, os, random, statistics, subprocess
from collections import Counter
from concurrent.futures import ProcessPoolExecutor, as_completed

try:
    from tqdm.auto import tqdm
except Exception:
    tqdm = None
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import etapa19b_combat_engine as eng
import grulla_v2_final_boss_lab as gb

HERE = Path(__file__).resolve().parent
CONFIG_PATH = HERE / "grulla_v2_candidateA_final_fire.json"
RESULTS_DIR = HERE / "resultados_definitivas_fuego_final"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

DANGEROUS_F3 = {"CAMPANA_F3", "ROMPER_F3"}
DIRECT_BOSS = {"GOLPE_F1","TORMENTA_F1","GOLPE_F2","TORMENTA_F2","PICOTAZO_F3","CAMPANA_F3","ROMPER_F3"}


def rhu(x: float) -> int:
    return int(math.floor(float(x) + 0.5))

def clamp(x,a,b): return max(a,min(b,x))

def load_cfg():
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def apply_ultimate_packet(lab, state, amount: float, *, ignore_def: bool, pct_pen: float=0.0,
                          bypass_absorption: float=0.0) -> float:
    """Non-crit/non-DOT ultimate packet. Respects boss mitigation and absorption unless bypassed."""
    if amount <= 0 or not state.monster.alive():
        return 0.0
    dmg=float(amount)
    if lab.boss_mitigation > 0:
        dmg *= max(0.0, 1-lab.boss_mitigation)
    if not ignore_def:
        real_def=max(0.0,eng._monster_dynamic_defense(state))
        eff=max(0.0,real_def*(1-clamp(pct_pen,0,100)/100))
        dmg=max(0.0,dmg-eff)
    dmg=float(rhu(dmg))
    # Candidate Aguja can bypass already-melted absorption without deleting that bypassed reserve.
    if state.monster.absorption>0 and dmg>0:
        cap=lab.phase_absorption_cap if lab.phase==3 else lab.close_absorption_cap
        if cap<=0: cap=state.monster.absorption
        available=max(0.0,state.monster.absorption-max(0.0,bypass_absorption))
        used=min(dmg,available,cap)
        state.monster.absorption-=used
        state.metrics.monster_absorbed+=used
        if lab.phase==3: lab.counters.f3_shield_absorbed+=used
        dmg-=used
    actual=min(state.monster.hp,dmg)
    state.monster.hp-=actual
    state.metrics.player_damage_direct+=actual
    return actual


def monster_turn_start_plumage(state, rng, ash: dict) -> None:
    """Candidate Plumaje de Ceniza: nullifies ~1/5 recognized BURN ticks; no action cost."""
    t=state.monster
    if not t.dots: return
    kept=[]
    for d in t.dots:
        if d.get("flat") is not None: dmg=float(d["flat"])
        else: dmg=eng.roll_dice(rng,d["dice"])*float(d.get("mult",1.0))
        cancel=False
        if d.get("family")=="BURN":
            ash["burn_seen"]+=1
            # LAB candidate: reactive cadence memory; every 5th burn tick is discarded.
            if ash["burn_seen"] % 5 == 0:
                cancel=True; ash["prevented_ticks"]+=1; ash["prevented_raw"]+=dmg
        packet=0 if cancel else eng.round_half_up(max(0,dmg))
        packet,_=eng._absorb(t,float(packet),state.metrics,False)
        actual=min(t.hp,float(packet));t.hp-=actual;state.metrics.player_damage_dot+=actual
        d=dict(d);d["ticks_left"]-=1
        if d["ticks_left"]>0: kept.append(d)
        if t.hp<=0: break
    t.dots=kept


def expected_boss_damage(lab, state, intent: str) -> float:
    if intent not in DIRECT_BOSS: return 0.0
    a=lab.ability(intent)
    raw=gb.mean_dice(a["dice"])
    real_def=max(0.0,eng._player_dynamic_defense(state))
    eff=max(0.0,real_def*(1-clamp(float(a.get("percent_penetration",0)),0,100)/100)-max(0,float(a.get("flat_penetration",0))))
    return max(0.0,raw-eff)



ULT_QI_COST = {"RENACER":14, "CORAZON":12, "AGUJA":13, "LOTO":12, "BRASA":12}

def ultimate_reserve_cost(name: str) -> int:
    return int(ULT_QI_COST.get(name, 0))

def _action_qi_cost(state, action: dict) -> int:
    if action.get("kind") != "TECH":
        return 0
    tid = action.get("tid")
    if tid not in state.compiled:
        return 0
    return int(state.compiled[tid].get("qi_cost", 0))

def choose_player_action_ultaware(u, reserve_name: str | None, lab, state, policy: str,
                                  intent: str, inv: list[dict]) -> dict:
    """Veteran resource policy for one-use ultimates.

    The normal PREPARED_MASTER policy remains authoritative for tactical choices.
    This wrapper only prevents it from accidentally spending the Qi that the
    player explicitly intends to reserve for the unique Definitiva.

    Survival overrides reservation: if a defensive technique is needed to avoid
    a near-lethal visible packet, it may spend below the reserve.
    """
    action = gb.choose_player_action(lab, state, policy, intent, inv)
    if not reserve_name or u.used:
        return action

    reserve = ultimate_reserve_cost(reserve_name)
    if reserve <= 0:
        return action

    p = state.player
    dangerous = intent in DANGEROUS_F3 or intent in {"TORMENTA_F1","TORMENTA_F2"}
    qipot = gb.consumable_available(inv, "QI")
    action_cost = _action_qi_cost(state, action)

    # If the normal policy already chose Qi recovery, preserve that decision.
    if action.get("kind") == "QI":
        return action

    # Maintain enough Qi for the unique ultimate plus the selected action.
    needed = reserve + action_cost

    if p.qi < needed:
        # Top up before surrendering the reserve when the visible turn is not
        # itself an emergency. Avoid drinking into severe recovery suppression.
        if qipot and not dangerous and lab.qi_recovery_mult >= 0.75:
            missing = p.qi_max - p.qi
            expected = float(qipot.get("amount", 0)) * lab.qi_recovery_mult
            if missing >= min(expected * 0.35, reserve):
                return {"kind":"QI","item":qipot}

        if action.get("kind") == "TECH":
            tid = action.get("tid")
            c = state.compiled.get(tid, {})
            if c.get("role") == "DEFENSIVE" and dangerous:
                # Survival > hoarding. If generic guard would still leave this
                # visible packet near-lethal, spend the defensive technique.
                expected = expected_boss_damage(lab, state, intent)
                guard = float(lab.config["lab_bridges"]["generic_defend_mitigation"])
                after_guard = expected * max(0.0, 1.0-guard)
                if p.hp <= max(after_guard*1.15, p.hp_max*0.18):
                    return action
                return {"kind":"DEFEND"}
            # Do not burn the unique reserve on routine offense.
            return {"kind":"BASIC"}

    return action

def resolved_git_sha() -> str:
    try:
        return subprocess.check_output(
            ["git","rev-parse","HEAD"], cwd=str(HERE), text=True, stderr=subprocess.DEVNULL
        ).strip()
    except Exception:
        return "UNKNOWN"

@dataclass
class UltState:
    name: str
    used: bool=False
    used_phase: int=0
    used_intent: str=""
    climax: bool=False
    partial: bool=False
    damage: float=0.0
    prevented: float=0.0
    qi_restored: float=0.0
    died_unused: bool=False
    data: dict=field(default_factory=dict)


def maybe_activate_reaction(u: UltState, lab, state, intent: str, cfg: dict) -> bool:
    """Returns True if this reaction cancels the current boss intent (Loto only)."""
    if u.name=="NONE" or u.used: return False
    p=state.player
    # Loto 1.1 — reserve the unique use for major F3 casts.
    if u.name=="LOTO" and lab.phase==3 and intent in DANGEROUS_F3 and p.qi>=12:
        # Timing: use when the cast is consequential, not simply on first availability.
        if p.hp/p.hp_max <= 0.72 or intent=="ROMPER_F3" or lab.last_breath_turns>0:
            p.qi-=12; state.metrics.qi_spent+=12
            u.used=True;u.used_phase=lab.phase;u.used_intent=intent
            power=gb.mean_dice(lab.ability(intent)["dice"])
            # Immediate Water petal uses separate gear-like reserve so normal defense may still be chosen.
            reserve=rhu(power*0.35)
            state.gear_absorption += reserve
            restore=min(10.0,p.qi_max-p.qi);p.qi+=restore;state.metrics.qi_restored+=restore
            u.qi_restored+=restore;u.prevented+=power
            u.data.update(power=power,budget=power*1.25,pending_actions=2,route=None,
                          echo_packets=[],defense_counter=0.0,flowering=False,free_next_tech=False)
            return True
    # Brasa 0.4 — reaction, no action cost.
    if u.name=="BRASA" and lab.phase==3 and intent in DANGEROUS_F3 and p.qi>=12:
        if p.hp/p.hp_max <= 0.82 or lab.last_breath_turns>0:
            p.qi-=12;state.metrics.qi_spent+=12
            u.used=True;u.used_phase=lab.phase;u.used_intent=intent
            u.data.update(active=True,direct_left=3,evades=0,evasion_bonus=35.0,
                          damages=[],pending_partial=False)
    return False


def maybe_activate_aguja_on_action(u: UltState,lab,state,intent: str,action: dict):
    if u.name!="AGUJA" or u.used or lab.phase!=3 or state.player.qi<13:
        return
    offensive = action.get("kind")=="BASIC" or (action.get("kind")=="TECH" and state.compiled[action["tid"]].get("role")!="DEFENSIVE")
    if not offensive or not (state.monster.absorption>0 or state.monster.defense>=5):
        return
    state.player.qi-=13;state.metrics.qi_spent+=13
    u.used=True;u.used_phase=lab.phase;u.used_intent=intent
    u.data.update(active=True,offensive_left=4,hits=0,defmax=0.0,absmelt=0.0)


def should_activate_action_ultimate(u: UltState, lab, state, intent: str) -> bool:
    if u.used or u.name not in {"RENACER","CORAZON"}: return False
    p=state.player
    if lab.phase!=3 or intent not in DANGEROUS_F3: return False
    if u.name=="RENACER":
        if p.qi<14:return False
        exp=expected_boss_damage(lab,state,intent)
        # Veteran timing: reserve it for a genuinely lethal/near-lethal visible packet.
        return p.hp <= max(exp*1.15, p.hp_max*0.24)
    if u.name=="CORAZON":
        if p.qi<12:return False
        # Corazon wants a high-pressure cast and enough HP to survive overflow.
        return p.hp/p.hp_max <=0.72 or intent=="ROMPER_F3" or lab.last_breath_turns>0
    return False


def activate_action_ultimate(u: UltState, lab, state, intent: str):
    p=state.player
    if u.name=="RENACER":
        p.qi-=14;state.metrics.qi_spent+=14
        u.used=True;u.used_phase=lab.phase;u.used_intent=intent
        u.data.update(brasa_active=True,enemy_turns=3,triggered=False,dawn_actions=0,
                      safeguard=False,first_dawn_offense=True)
    elif u.name=="CORAZON":
        p.qi-=12;state.metrics.qi_spent+=12
        u.used=True;u.used_phase=lab.phase;u.used_intent=intent
        reserve=rhu(p.hp_max*.35)
        # Technique barriers cannot coexist. Gear absorption remains independent.
        if state.player_defense and state.player_defense.get("kind") in {"FIRE_BARRIER","WATER_MIRROR"}:
            state.player_defense=None; p.absorption=0;p.absorption_max=0
        p.absorption=float(reserve);p.absorption_max=float(reserve)
        u.data.update(active=True,reserve_initial=float(reserve),enemy_turns=2,pressure=0.0,
                      prev_abs=float(reserve),broken=False)


def trigger_renacer(u: UltState, lab, state):
    if u.name!="RENACER" or not u.data.get("brasa_active") or u.data.get("triggered") or state.player.hp>0:
        return False
    p=state.player
    u.data["triggered"]=True;u.data["brasa_active"]=False;u.climax=True
    p.hp=float(rhu(p.hp_max*.30));p.dots=[];p.stat_effects=[]
    lab.heal_mult=1.0;lab.heal_mult_turns=0;lab.qi_recovery_mult=1.0;lab.qi_recovery_mult_turns=0
    p.absorption=max(p.absorption,float(rhu(p.hp_max*.20)));p.absorption_max=max(p.absorption_max,p.absorption)
    flare=rhu(8+p.hp_max*.15)
    u.damage+=apply_ultimate_packet(lab,state,flare,ignore_def=False)
    u.data["dawn_actions"]=2;u.data["safeguard"]=True;u.data["first_dawn_offense"]=True
    return True


def corazon_after_boss(u: UltState, lab, state):
    if u.name!="CORAZON" or not u.data.get("active"): return
    p=state.player
    prev=float(u.data.get("prev_abs",0.0));now=max(0.0,p.absorption)
    absorbed=max(0.0,prev-now)
    u.data["pressure"]+=absorbed;u.prevented+=absorbed;u.data["prev_abs"]=now
    if prev>0 and now<=0:
        u.data["broken"]=True
        if p.alive():
            dmg=rhu((6+u.data["pressure"]*1.35)*1.20)
            u.damage+=apply_ultimate_packet(lab,state,dmg,ignore_def=False,pct_pen=25)
            u.climax=True
        u.data["active"]=False
    if u.data.get("active"):
        u.data["enemy_turns"]-=1
        if u.data["enemy_turns"]<=0:
            dmg=rhu(6+u.data["pressure"]*1.35)
            if p.alive():
                u.damage+=apply_ultimate_packet(lab,state,dmg,ignore_def=False,pct_pen=25);u.climax=True
            # Remove only leftover Corazon technique pool.
            p.absorption=0.0;p.absorption_max=0.0;u.data["active"]=False


def apply_dawn_before_action(u: UltState,state,action):
    """Temporary Renacer buffs; returns restoration metadata."""
    if u.name!="RENACER" or u.data.get("dawn_actions",0)<=0 or action.get("kind")!="TECH": return None
    c=state.compiled[action["tid"]]
    if c.get("root")!="fuego": return None
    first=bool(u.data.get("first_dawn_offense")) and c.get("role")!="DEFENSIVE"
    old=(state.player.precision,state.player.percent_penetration)
    state.player.precision += 100 if first else 20
    state.player.percent_penetration += 15
    return {"old":old,"first":first,"qi_before":state.player.qi}


def finish_dawn_after_action(u: UltState,state,meta,action,rec):
    if not meta:return
    state.player.precision,state.player.percent_penetration=meta["old"]
    spent=max(0.0,meta["qi_before"]-state.player.qi)
    desired=rhu(spent*.5)
    refund=max(0.0,spent-desired)
    state.player.qi=min(state.player.qi_max,state.player.qi+refund)
    state.metrics.qi_spent=max(0.0,state.metrics.qi_spent-refund)
    u.data["dawn_actions"]-=1
    if meta["first"]:u.data["first_dawn_offense"]=False


def execute_player_action_ext(lab,state,rng,action):
    q0=state.player.qi
    real_def_before=max(0.0,eng._monster_dynamic_defense(state))
    abs_before=state.monster.absorption
    if action["kind"]=="HEAL":
        out=gb.use_heal(lab,state,rng,action["item"])
    elif action["kind"]=="QI":
        out=gb.use_qi(lab,state,action["item"])
    elif action["kind"]=="DEFEND":
        lab.generic_guard_pct=float(lab.config["lab_bridges"]["generic_defend_mitigation"]);lab.counters.generic_defends+=1
        out={"kind":"DEFEND","damage":0.0,"qi_spent":0.0,"hit":False}
    elif action["kind"]=="TECH":
        c=state.compiled[action["tid"]];rr=gb.execute_player_technique_lab(lab,state,rng,c)
        out={"kind":"TECH","technique_id":action["tid"],"element":c["root"],"role":c["role"],
             "damage":float(rr.get("actual_hp_damage",0)),"qi_spent":q0-state.player.qi,
             "hit":bool(rr.get("hit",False)),"critical":bool(rr.get("critical",False)),
             "effective_def":rr.get("effective_def"),"absorbed":float(rr.get("absorbed",0.0))}
    else:
        rr=gb.execute_basic_lab(lab,state,rng)
        out={"kind":"BASIC","damage":float(rr.get("actual_hp_damage",0)),"qi_spent":0.0,"hit":bool(rr.get("hit",False)),
             "critical":bool(rr.get("critical",False)),"effective_def":rr.get("effective_def"),"absorbed":float(rr.get("absorbed",0.0))}
    out["real_def_before"]=real_def_before;out["boss_abs_before"]=abs_before
    if out.get("damage",0)>=float(lab.config["lab_bridges"]["heavy_hit_ratio"])*state.monster.hp_max: out["damage_band"]="HEAVY"
    elif out.get("damage",0)>0:out["damage_band"]="NORMAL"
    else:out["damage_band"]="NONE"
    return out


def aguja_after_action(u: UltState,lab,state,rec):
    if u.name!="AGUJA" or not u.data.get("active"):return
    if rec.get("kind") not in {"TECH","BASIC"}:return
    u.data["offensive_left"]-=1
    if rec.get("hit"):
        u.data["hits"]+=1
        eff=rec.get("effective_def")
        if eff is not None:
            defeated=max(0.0,float(rec.get("real_def_before",0))-float(eff))
            u.data["defmax"]=max(u.data["defmax"],min(10.0,defeated))
        u.data["absmelt"]=min(14.0,u.data["absmelt"]+float(rec.get("absorbed",0)))
    if u.data["hits"]>=2:
        matter=u.data["defmax"]+u.data["absmelt"];packet=rhu(matter*1.50)
        u.damage+=apply_ultimate_packet(lab,state,packet,ignore_def=True,bypass_absorption=u.data["absmelt"])
        # DEF_MELTED is not normal shred; represent as distinct temporary effect in LAB.
        melt=min(10.0,u.data["defmax"])
        if melt>0:eng._replace_effect(state.monster,"defense",-melt,2,"AGUJA:DEF_MELTED")
        u.climax=True;u.data["active"]=False
    elif u.data["offensive_left"]<=0:
        if u.data["hits"]==1:
            matter=u.data["defmax"]+u.data["absmelt"];packet=rhu(matter*1.50*.50)
            u.damage+=apply_ultimate_packet(lab,state,packet,ignore_def=True,bypass_absorption=u.data["absmelt"]*.5)
            u.partial=True
        u.data["active"]=False


def loto_after_player_action(u: UltState,lab,state,action,rec):
    if u.name!="LOTO" or not u.used or not u.data.get("pending_actions",0):return
    if u.data.get("route") is not None:return
    budget=float(u.data["budget"])
    if action.get("kind")=="TECH":
        c=state.compiled[action["tid"]]
        if c.get("role")=="DEFENSIVE":
            u.data["route"]="DEFENSE";u.data["defense_counter"]=budget;u.data["flowering"]=True;u.data["free_next_tech"]=True;u.climax=True
            return
        if c.get("control") is not None:
            # Loto's inversion window bypasses normal resistance/anti-lock for this one stored action.
            state.monster.skip_next_action=False;state.arrastre_locked=False
            u.data["cancel_next_boss"]=True
            u.data["route"]="CONTROL";u.data["echo_packets"]=[budget*.5,budget*.5]
            u.data["flowering"]=True;u.data["free_next_tech"]=True;u.climax=True
            return
    if rec.get("kind") in {"TECH","BASIC"} and rec.get("hit"):
        u.data["route"]="OFFENSE"
        u.damage+=apply_ultimate_packet(lab,state,budget,ignore_def=True)
        u.data["flowering"]=True;u.data["free_next_tech"]=True;u.climax=True
        return
    u.data["pending_actions"]-=1


def loto_echo_after_offense(u: UltState,lab,state,rec):
    if u.name!="LOTO" or u.data.get("route")!="CONTROL" or not u.data.get("echo_packets"):return
    if rec.get("kind") in {"TECH","BASIC"} and rec.get("hit"):
        packet=u.data["echo_packets"].pop(0)
        u.damage+=apply_ultimate_packet(lab,state,packet,ignore_def=True)


def maybe_refund_flowering(u: UltState,state,action,qi_before):
    if u.name!="LOTO" or not u.data.get("free_next_tech") or action.get("kind")!="TECH":return
    spent=max(0.0,qi_before-state.player.qi)
    if spent>0:
        state.player.qi=min(state.player.qi_max,state.player.qi+spent)
        state.metrics.qi_spent=max(0.0,state.metrics.qi_spent-spent)
    u.data["free_next_tech"]=False


def loto_defense_counter_after_boss(u: UltState,lab,state,boss_result,abs_before):
    if u.name!="LOTO" or u.data.get("route")!="DEFENSE" or u.data.get("defense_counter",0)<=0:return
    absorbed=max(0.0,abs_before-state.player.absorption)
    if boss_result and boss_result.get("hit") and (absorbed>0 or state.player_defense is not None):
        packet=u.data["defense_counter"];u.data["defense_counter"]=0
        u.damage+=apply_ultimate_packet(lab,state,packet,ignore_def=True)


def brasa_before_boss(u: UltState,state):
    if u.name=="BRASA" and u.data.get("active"):
        old=state.player.evasion;state.player.evasion+=u.data.get("evasion_bonus",0);return old
    return None

def brasa_after_boss(u: UltState,lab,state,boss_result,old_evasion,rng):
    if old_evasion is not None:state.player.evasion=old_evasion
    if u.name!="BRASA" or not u.data.get("active") or boss_result is None:return
    u.data["direct_left"]-=1
    if not boss_result.get("hit") and u.data["evades"]<2 and state.monster.alive():
        u.data["evades"]+=1
        pb=10 if u.data["evades"]==1 else 25
        off=gb.primary_offensive(state);c=state.compiled[off]
        oldp=state.player.precision;state.player.precision+=pb
        rr=gb.resolve_player_direct_lab(lab,state,rng,c,False)
        state.player.precision=oldp
        d=float(rr.get("actual_hp_damage",0));u.data["damages"].append(d);u.damage+=d
        if u.data["evades"]==1:u.data["evasion_bonus"]+=10
        if u.data["evades"]==2:
            climax=rhu(sum(u.data["damages"][:2])*.35)
            u.damage+=apply_ultimate_packet(lab,state,climax,ignore_def=True);u.climax=True;u.data["active"]=False
    if u.data.get("active") and u.data["direct_left"]<=0:
        if u.data["evades"]==1:
            partial=rhu((u.data["damages"][0] if u.data["damages"] else 0)*.15)
            u.damage+=apply_ultimate_packet(lab,state,partial,ignore_def=True);u.partial=True
        u.data["active"]=False


def fight_once(cfg: dict, scenario: dict, ultimate: str, seed: int, max_rounds:int=120, reserve_name: str | None=None) -> dict:
    state,lab=gb.build_fight(cfg,scenario["root"],scenario["build"],scenario["loadout"])
    inv=gb.make_consumables(cfg,scenario["consumables"]);rng=random.Random(seed)
    u=UltState(ultimate);ash={"burn_seen":0,"prevented_ticks":0,"prevented_raw":0.0}
    qi_reserve_breaches=0
    win=False;double_ko=False

    while state.player.alive() and lab.total_round<max_rounds:
        if lab.phase>3:win=True;break
        lab.total_round+=1;lab.phase_round+=1;lab.phase_rounds[lab.phase]+=1;state.round_no+=1

        # Last Breath candidate: DEF -3 during the player's action window.
        # The previous runner applied the penalty only around player_turn_start,
        # restoring it before the attack; that made the intended DEF penalty a no-op.
        eng.player_turn_start(state,rng)
        if not state.player.alive():
            if u.name=="RENACER" and u.data.get("dawn_actions",0)>0 and u.data.get("safeguard"):
                state.player.hp=1.0;u.data["safeguard"]=False
            elif trigger_renacer(u,lab,state):
                pass
            else:
                break

        intent=gb.choose_boss_intent(lab,state,rng);gb.pre_player_intent(lab,state,intent)
        boss_hp_before=state.monster.hp

        def_penalty=3.0 if lab.phase==3 and lab.last_breath_turns>0 else 0.0
        if def_penalty:
            state.monster.defense-=def_penalty

        cancel_boss=maybe_activate_reaction(u,lab,state,intent,cfg)
        action_is_ultimate=should_activate_action_ultimate(u,lab,state,intent)
        if action_is_ultimate:
            activate_action_ultimate(u,lab,state,intent)
            action={"kind":"ULTIMATE"};rec={"kind":"ULTIMATE","damage":0.0,"qi_spent":0.0,"hit":False,"technique_id":None,"element":None,"damage_band":"NONE"}
        else:
            effective_reserve = reserve_name or (u.name if u.name!="NONE" else None)
            action=choose_player_action_ultaware(u,effective_reserve,lab,state,scenario["policy"],intent,inv)
            # Aguja must be able to pay both the 13-Qi activation and the chosen offensive action.
            if u.name=="AGUJA" and not u.used and lab.phase==3:
                ac=_action_qi_cost(state,action)
                if action.get("kind")=="TECH" and state.player.qi < 13 + ac:
                    action={"kind":"BASIC"}
            maybe_activate_aguja_on_action(u,lab,state,intent,action)
            qi_before=state.player.qi
            dawn=apply_dawn_before_action(u,state,action)
            rec=execute_player_action_ext(lab,state,rng,action)
            finish_dawn_after_action(u,state,dawn,action,rec)
            maybe_refund_flowering(u,state,action,qi_before)
            aguja_after_action(u,lab,state,rec)
            loto_after_player_action(u,lab,state,action,rec)
            loto_echo_after_offense(u,lab,state,rec)

        if def_penalty:
            state.monster.defense+=def_penalty

        rec.setdefault("technique_id",None);rec.setdefault("element",None);rec["phase"]=lab.phase;rec["intent"]=intent
        gb.tick_recovery_debuffs_after_player_action(lab)

        boss_result=None
        if not cancel_boss and u.name=="LOTO" and u.data.get("cancel_next_boss"):
            cancel_boss=True;u.data["cancel_next_boss"]=False
        if not cancel_boss:
            old_eva=brasa_before_boss(u,state)
            abs_before=state.player.absorption
            boss_result=gb.post_player_intent(lab,state,rng,intent,rec)
            brasa_after_boss(u,lab,state,boss_result,old_eva,rng)
            loto_defense_counter_after_boss(u,lab,state,boss_result,abs_before)
            corazon_after_boss(u,lab,state)
            if state.player.hp<=0:
                if u.name=="RENACER" and u.data.get("dawn_actions",0)>0 and u.data.get("safeguard"):
                    state.player.hp=1.0;u.data["safeguard"]=False
                else:trigger_renacer(u,lab,state)
        # Loto confiscation still counts as boss intent/history, but has no resolution.

        lab.player_history.append(dict(rec));lab.recent_boss_intents.append(intent)

        if state.player.alive() and state.monster.alive():
            had_abs=state.monster.absorption>0
            monster_turn_start_plumage(state,rng,ash)
            gb.trigger_last_breath_if_needed(lab,state,had_abs)

        if state.player.hp<=0 and state.monster.hp<=0:double_ko=True;break
        if state.player.hp<=0:break
        if state.monster.hp<=0:
            if lab.phase==3:lab.phase=4;win=True;break
            gb.enter_phase(lab,state,lab.phase+1);continue

        if state.arrastre_locked:
            # Preserve next-action control only when Loto explicitly armed it this round.
            if not (u.name=="LOTO" and u.data.get("route")=="CONTROL" and state.monster.skip_next_action):
                state.arrastre_locked=False;state.arrastre_precision_debuff=0.0

        eng.end_round(state);lab.boss_evasion_bonus=0;lab.boss_mitigation=0;lab.reflect_active=False
        lab.close_absorption_cap=lab.close_absorption_cap if state.monster.absorption>0 else 0.0
        if lab.last_breath_turns>0:lab.last_breath_turns-=1

        # Renacer active-window duration counts enemy turns.
        if u.name=="RENACER" and u.data.get("brasa_active"):
            u.data["enemy_turns"]-=1
            if u.data["enemy_turns"]<=0 and not u.data.get("triggered"):
                u.data["brasa_active"]=False
                state.player.hp=min(state.player.hp_max,state.player.hp+rhu(state.player.hp_max*.10))
                state.player.qi=min(state.player.qi_max,state.player.qi+5);u.qi_restored+=5

    if u.name!="NONE" and not win and not u.used:u.died_unused=True
    return {
        "scenario":scenario["id"],"ultimate":ultimate,"root":scenario["root"],"build":scenario["build"],
        "win":bool(win and state.player.hp>0),"double_ko":double_ko,"timeout":lab.total_round>=max_rounds and state.player.alive() and lab.phase<=3,
        "rounds":lab.total_round,"reach_f2":lab.phase_entries[2],"reach_f3":lab.phase_entries[3],
        "f1_rounds":lab.phase_rounds[1],"f2_rounds":lab.phase_rounds[2],"f3_rounds":lab.phase_rounds[3],
        "hp_final":max(0.0,state.player.hp),"hp_max":state.player.hp_max,"qi_final":max(0.0,state.player.qi),
        "ult_used":u.used,"ult_used_phase":u.used_phase,"ult_used_intent":u.used_intent,"ult_climax":u.climax,"ult_partial":u.partial,
        "ult_damage":u.damage,"ult_prevented":u.prevented,"ult_qi_restored":u.qi_restored,"died_unused":u.died_unused,
        "plumage_prevented_ticks":ash["prevented_ticks"],"plumage_prevented_raw":ash["prevented_raw"],
        "player_direct":state.metrics.player_damage_direct,"player_dot":state.metrics.player_damage_dot,
        "hp_potions":lab.counters.potions_hp_used,"qi_potions":lab.counters.potions_qi_used,
        "campana":lab.counters.campana_casts,"romper":lab.counters.romper_casts,
        "reserve_name":reserve_name or "NONE","reserve_cost":ultimate_reserve_cost(reserve_name or (u.name if u.name!="NONE" else "NONE")),
    }


SCENARIOS=[
    {"id":"FIRE_DIRECT_RENACER","root":"fuego","build":"burst_guard","loadout":"veteran_balanced","consumables":"max_reasonable","policy":"PREPARED_MASTER","ultimate":"RENACER"},
    {"id":"FIRE_DOT_RENACER","root":"fuego","build":"dot_guard","loadout":"veteran_balanced","consumables":"max_reasonable","policy":"PREPARED_MASTER","ultimate":"RENACER"},
    {"id":"EARTH_DIRECT_CORAZON","root":"tierra","build":"direct_guard","loadout":"veteran_balanced","consumables":"max_reasonable","policy":"PREPARED_MASTER","ultimate":"CORAZON"},
    {"id":"EARTH_PRESSURE_CORAZON","root":"tierra","build":"pressure_guard","loadout":"veteran_balanced","consumables":"max_reasonable","policy":"PREPARED_MASTER","ultimate":"CORAZON"},
    {"id":"METAL_PEN_AGUJA","root":"metal","build":"pen_guard","loadout":"max_penetration","consumables":"max_reasonable","policy":"PREPARED_MASTER","ultimate":"AGUJA"},
    {"id":"METAL_SHRED_AGUJA","root":"metal","build":"pen_shred","loadout":"max_penetration","consumables":"max_reasonable","policy":"PREPARED_MASTER","ultimate":"AGUJA"},
    {"id":"WATER_DIRECT_LOTO","root":"agua","build":"direct_guard","loadout":"veteran_balanced","consumables":"max_reasonable","policy":"PREPARED_MASTER","ultimate":"LOTO"},
    {"id":"WATER_CONTROL_LOTO","root":"agua","build":"control_guard","loadout":"veteran_balanced","consumables":"max_reasonable","policy":"PREPARED_MASTER","ultimate":"LOTO"},
    {"id":"WIND_DIRECT_BRASA","root":"viento","build":"direct_guard","loadout":"veteran_balanced","consumables":"max_reasonable","policy":"PREPARED_MASTER","ultimate":"BRASA"},
    {"id":"WIND_PRECISION_BRASA","root":"viento","build":"precision_guard","loadout":"veteran_balanced","consumables":"max_reasonable","policy":"PREPARED_MASTER","ultimate":"BRASA"},
]


def summarize(rows):
    """Reference summarizer retained for small direct tests."""
    n=len(rows);r3=[r for r in rows if r["reach_f3"]];used=[r for r in rows if r["ult_used"]];cl=[r for r in rows if r["ult_climax"]]
    def mean(key,seq=rows):return statistics.fmean(float(r[key]) for r in seq) if seq else 0.0
    return {
        "n":n,"win_rate":mean("win"),"reach_f3":mean("reach_f3"),"rounds":mean("rounds"),
        "f3_rounds_if_reached":mean("f3_rounds",r3),"hp_final_pct":statistics.fmean(r["hp_final"]/r["hp_max"] for r in rows),"qi_final":mean("qi_final"),
        "ult_used_rate":mean("ult_used"),"ult_climax_rate":mean("ult_climax"),"climax_if_used":sum(r["ult_climax"] for r in used)/len(used) if used else 0,
        "win_if_used":sum(r["win"] for r in used)/len(used) if used else 0,"win_if_climax":sum(r["win"] for r in cl)/len(cl) if cl else 0,
        "died_unused":mean("died_unused"),"ult_damage":mean("ult_damage"),"ult_prevented":mean("ult_prevented"),"ult_qi_restored":mean("ult_qi_restored"),
        "plumage_prevented_ticks":mean("plumage_prevented_ticks"),"hp_potions":mean("hp_potions"),"qi_potions":mean("qi_potions"),
    }


def partial_from_rows(rows):
    """Lossless aggregate for chunked multiprocessing progress.

    Keeping chunk summaries rather than returning every fight through IPC gives us
    a granular progress bar without changing the Monte Carlo seeds or statistics.
    """
    a={
        "n":0,"win":0.0,"reach_f3":0.0,"rounds":0.0,
        "r3_n":0,"f3_rounds":0.0,"hp_final_pct":0.0,"qi_final":0.0,
        "ult_used":0.0,"ult_climax":0.0,"used_n":0,"used_climax":0.0,"used_win":0.0,
        "climax_n":0,"climax_win":0.0,"died_unused":0.0,"ult_damage":0.0,
        "ult_prevented":0.0,"ult_qi_restored":0.0,"plumage_prevented_ticks":0.0,
        "hp_potions":0.0,"qi_potions":0.0,
    }
    for r in rows:
        a["n"]+=1
        a["win"]+=float(r["win"]);a["reach_f3"]+=float(r["reach_f3"]);a["rounds"]+=float(r["rounds"])
        a["hp_final_pct"]+=float(r["hp_final"])/float(r["hp_max"]);a["qi_final"]+=float(r["qi_final"])
        a["ult_used"]+=float(r["ult_used"]);a["ult_climax"]+=float(r["ult_climax"])
        a["died_unused"]+=float(r["died_unused"]);a["ult_damage"]+=float(r["ult_damage"])
        a["ult_prevented"]+=float(r["ult_prevented"]);a["ult_qi_restored"]+=float(r["ult_qi_restored"])
        a["plumage_prevented_ticks"]+=float(r["plumage_prevented_ticks"]);a["hp_potions"]+=float(r["hp_potions"]);a["qi_potions"]+=float(r["qi_potions"])
        if r["reach_f3"]:
            a["r3_n"]+=1;a["f3_rounds"]+=float(r["f3_rounds"])
        if r["ult_used"]:
            a["used_n"]+=1;a["used_climax"]+=float(r["ult_climax"]);a["used_win"]+=float(r["win"])
        if r["ult_climax"]:
            a["climax_n"]+=1;a["climax_win"]+=float(r["win"])
    return a


def add_partial(dst,src):
    for k,v in src.items(): dst[k]=dst.get(k,0)+v
    return dst


def finalize_partial(a,scenario,ultimate):
    n=max(1,int(a["n"]))
    return {
        "n":int(a["n"]),
        "win_rate":a["win"]/n,"reach_f3":a["reach_f3"]/n,"rounds":a["rounds"]/n,
        "f3_rounds_if_reached":a["f3_rounds"]/a["r3_n"] if a["r3_n"] else 0.0,
        "hp_final_pct":a["hp_final_pct"]/n,"qi_final":a["qi_final"]/n,
        "ult_used_rate":a["ult_used"]/n,"ult_climax_rate":a["ult_climax"]/n,
        "climax_if_used":a["used_climax"]/a["used_n"] if a["used_n"] else 0.0,
        "win_if_used":a["used_win"]/a["used_n"] if a["used_n"] else 0.0,
        "win_if_climax":a["climax_win"]/a["climax_n"] if a["climax_n"] else 0.0,
        "died_unused":a["died_unused"]/n,"ult_damage":a["ult_damage"]/n,"ult_prevented":a["ult_prevented"]/n,
        "ult_qi_restored":a["ult_qi_restored"]/n,"plumage_prevented_ticks":a["plumage_prevented_ticks"]/n,
        "hp_potions":a["hp_potions"]/n,"qi_potions":a["qi_potions"]/n,
        "scenario":scenario["id"],"ultimate":ultimate,"root":scenario["root"],"build":scenario["build"],
    }


def run_cell(cfg,scenario,ultimate,runs,seed):
    rows=[fight_once(cfg,scenario,ultimate,seed+i*1009) for i in range(runs)]
    s=summarize(rows);s.update(scenario=scenario["id"],ultimate=ultimate,root=scenario["root"],build=scenario["build"])
    return s,rows


def worker_chunk(args):
    """Execute one deterministic slice of a cell.

    start is the original fight index, preserving exactly the same seed stream as
    an unchunked run: cell_seed + fight_index*1009.
    """
    scenario,ultimate,reserve_name,start,count,cell_seed=args
    cfg=load_cfg()
    rows=[fight_once(cfg,scenario,ultimate,cell_seed+(start+i)*1009,reserve_name=reserve_name) for i in range(count)]
    return scenario["id"],ultimate,reserve_name,partial_from_rows(rows),count


def _iter_progress(iterable,total,desc):
    if tqdm is not None:
        return tqdm(iterable,total=total,desc=desc,unit="chunk",dynamic_ncols=True,smoothing=0.08)
    return iterable


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--runs",type=int,default=5000)
    ap.add_argument("--jobs",type=int,default=max(1,min(4,os.cpu_count() or 1)))
    ap.add_argument("--seed",type=int,default=20260930)
    ap.add_argument("--smoke",action="store_true")
    ap.add_argument("--chunk-size",type=int,default=500,help="Peleas por bloque de progreso (default 500).")
    ap.add_argument("--shadow-reserve",action="store_true",help="Añade baseline diagnóstico con la misma reserva de Qi pero sin Definitiva.")
    args=ap.parse_args()
    runs=min(args.runs,300) if args.smoke else args.runs
    chunk_size=max(1,min(args.chunk_size,runs))

    # Build deterministic cells.
    # BASE_NATIVE: policy normal, no reserve.
    # BASE_RESERVE (optional): pays the opportunity cost of saving the same Qi, but never casts the ultimate.
    # ULTIMATE: veteran resource-aware policy + actual one-use ultimate.
    cells=[]
    for i,sc in enumerate(SCENARIOS):
        base_seed=args.seed+i*100000
        cells.append((sc,"NONE",None,"BASE_NATIVE",base_seed))
        if args.shadow_reserve:
            cells.append((sc,"NONE",sc["ultimate"],"BASE_RESERVE",base_seed+25000))
        cells.append((sc,sc["ultimate"],sc["ultimate"],"ULTIMATE",base_seed+50000))

    # Split each cell into deterministic chunks. This changes scheduling only,
    # never the seeds or the fights themselves.
    chunk_tasks=[]
    chunks_per_cell={}
    roles={}
    for sc,ultimate,reserve_name,role,cell_seed in cells:
        key=(sc["id"],ultimate,role)
        roles[key]=(reserve_name,role)
        chunks=[]
        for start in range(0,runs,chunk_size):
            count=min(chunk_size,runs-start)
            task=(sc,ultimate,reserve_name,start,count,cell_seed)
            chunk_tasks.append(task);chunks.append(task)
        chunks_per_cell[key]=len(chunks)

    print(f"Benchmark: {len(cells)} celdas × {runs:,} peleas = {len(cells)*runs:,} combates")
    print(f"Workers: {args.jobs} | chunk: {chunk_size} | bloques de progreso: {len(chunk_tasks):,}")

    accum={key:{} for key in chunks_per_cell}
    done_chunks=Counter()
    finished_cells=set()

    if args.jobs<=1:
        iterator=_iter_progress(chunk_tasks,len(chunk_tasks),"Monte Carlo")
        for task in iterator:
            sid,ult,reserve_name,part,count=worker_chunk(task);role="ULTIMATE" if ult!="NONE" else ("BASE_RESERVE" if reserve_name else "BASE_NATIVE");key=(sid,ult,role);add_partial(accum[key],part);done_chunks[key]+=1
            if done_chunks[key]==chunks_per_cell[key] and key not in finished_cells:
                finished_cells.add(key)
                if tqdm is not None: iterator.set_postfix_str(f"celdas {len(finished_cells)}/{len(cells)} · {sid}/{ult}")
    else:
        with ProcessPoolExecutor(max_workers=args.jobs) as ex:
            futs={ex.submit(worker_chunk,t):t for t in chunk_tasks}
            futures=as_completed(futs)
            bar=_iter_progress(futures,len(futs),"Monte Carlo")
            for f in bar:
                sid,ult,reserve_name,part,count=f.result();role="ULTIMATE" if ult!="NONE" else ("BASE_RESERVE" if reserve_name else "BASE_NATIVE");key=(sid,ult,role);add_partial(accum[key],part);done_chunks[key]+=1
                if done_chunks[key]==chunks_per_cell[key] and key not in finished_cells:
                    finished_cells.add(key)
                    if tqdm is not None: bar.set_postfix_str(f"celdas {len(finished_cells)}/{len(cells)} · {sid}/{ult}")

    results=[]
    scenario_by_id={sc["id"]:sc for sc in SCENARIOS}
    for (sid,ult,role),a in accum.items():
        row=finalize_partial(a,scenario_by_id[sid],ult)
        row["comparison_role"]=role
        row["reserve_name"]=scenario_by_id[sid]["ultimate"] if role in {"ULTIMATE","BASE_RESERVE"} else "NONE"
        row["ult_use_given_f3"]=row["ult_used_rate"]/row["reach_f3"] if row["reach_f3"] else 0.0
        row["f3_exposure_n"]=round(row["n"]*row["reach_f3"])
        results.append(row)
    results.sort(key=lambda x:(x["scenario"],x.get("comparison_role",""),x["ultimate"]))

    # Native paired uplift + optional reserve-tax decomposition.
    by_role={(r["scenario"],r["comparison_role"]):r for r in results}
    validity=[]
    for sc in SCENARIOS:
        b=by_role[(sc["id"],"BASE_NATIVE")]
        uu=by_role[(sc["id"],"ULTIMATE")]
        uu["paired_baseline_win"]=b["win_rate"]
        uu["win_uplift_pp"]=(uu["win_rate"]-b["win_rate"])*100
        uu["paired_baseline_reach_f3"]=b["reach_f3"]
        if args.shadow_reserve and (sc["id"],"BASE_RESERVE") in by_role:
            br=by_role[(sc["id"],"BASE_RESERVE")]
            uu["reserve_tax_pp"]=(br["win_rate"]-b["win_rate"])*100
            uu["gross_vs_reserve_pp"]=(uu["win_rate"]-br["win_rate"])*100

        exposure=uu.get("f3_exposure_n",0)
        use_cond=uu.get("ult_use_given_f3",0.0)
        evaluable=exposure>=max(100, int(runs*0.02))
        validity.append({
            "scenario":sc["id"],"f3_exposure_n":exposure,"ult_use_given_f3":use_cond,
            "evaluable_integral":bool(evaluable),
            "resource_gate_pass":bool((not evaluable) or use_cond>=0.02)
        })

    valid_all=all(v["resource_gate_pass"] for v in validity)
    status="LAB_NOT_CANON_VALID" if valid_all else "LAB_INVALID_RESOURCE_POLICY"
    out={"status":status,"candidate":"GRULLA_A_PLUS_PLUMAJE_1_OF_5","runs_per_cell":runs,"results":results,
         "validity":validity,
         "engine_git_sha":resolved_git_sha(),
         "lab_bridge":"Combination ultimate tested in secondary root ecosystem; evaluate paired uplift, not cross-root raw ranking.",
         "method":"ULTIMATE cells use veteran Qi reservation; BASE_NATIVE does not. Optional BASE_RESERVE quantifies opportunity cost.",
         "progress":{"chunk_size":chunk_size,"workers":args.jobs,"total_chunks":len(chunk_tasks)}}
    (RESULTS_DIR/"fire_ultimates_integral_summary.json").write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")
    with (RESULTS_DIR/"fire_ultimates_integral_summary.csv").open("w",newline="",encoding="utf-8") as f:
        keys=sorted({k for r in results for k in r});w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows(results)
    print("\nCOMPLETADO · resultados guardados en", RESULTS_DIR)
    print(json.dumps(out,ensure_ascii=False,indent=2))

if __name__=="__main__":main()
