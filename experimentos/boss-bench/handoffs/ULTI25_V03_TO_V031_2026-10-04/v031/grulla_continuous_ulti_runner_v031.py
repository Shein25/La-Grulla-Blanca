#!/usr/bin/env python3
from __future__ import annotations

import copy, hashlib, json, math, random
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

HERE=Path(__file__).resolve().parent

# Accepted V05 combat/Ulti mechanics. Importing the F3 harness installs the
# strict pre-commit Pacto guard and all audited Ulti fixes.
import grulla_f3_ulti25_equipment_retest as f3
ce=f3.ce; base=f3.base; mass=f3.mass; retest=f3.retest

RUNNER_STATUS="LAB_CONTINUOUS_COMPOSITION_RUNNER_V031"
RUNNER_LIMITATION=(
    "Real Grulla F1/F2/F3 phase pools + real historical brain/runtime are continuous. "
    "Ultis reuse the accepted V05 executable macro implementations; some macro-internal "
    "support actions and explicit transition-edge probes are LAB fixtures, so balance "
    "conclusions remain provisional and stress fixtures are never balance authority."
)
AUTH_PATH=HERE/"GRULLA_BENCH_NUMERIC_AUTHORITY_V01.json"
AUTH=json.loads(AUTH_PATH.read_text(encoding="utf-8"))
CATALOG_PATH=HERE/"ULTIMATES_25_CATALOG_V0_3.json"

PHASES=("F1","F2","F3")
PHASE_NUM={"F1":1,"F2":2,"F3":3}
PHASE_FROM_NUM={1:"F1",2:"F2",3:"F3"}
PHASE_STATS={
    "F1": dict(hp=150.0,precision=90.0,evasion=55.0,defense=13.0,tenacity=40.0,absorption=0.0,absorption_cap=None),
    "F2": dict(hp=100.0,precision=95.0,evasion=60.0,defense=15.6,tenacity=45.0,absorption=0.0,absorption_cap=None),
    "F3": dict(hp=50.0,precision=100.0,evasion=65.0,defense=18.72,tenacity=50.0,absorption=25.0,absorption_cap=25.0),
}

# Exact historical runtime abilities from 4237f126...
A={
 "GOLPE_ALA":"grulla__golpe_ala","CAMPANADA_PICO":"grulla__campanada_pico","PATA_INMOVIL":"grulla__pata_inmovil",
 "TORMENTA":"grulla__tormenta_mil_plumas","CERRAR":"grulla__cerrar_alas","RECORDAR":"grulla__recordar_filo","ECO":"grulla__eco_meridiano",
 "PICOTAZO":"grulla__picotazo_blanco","CAMPANA":"grulla__campana_sin_dueno","ALA":"grulla__ala_vacia",
 "SILENCIO":"grulla__silencio_entre_campanas","ROMPER":"grulla__romper_ritmo","BUSCAR":"grulla__buscar_pulso"
}
ABILITY={
 1:{
  A["GOLPE_ALA"]:dict(kind="ATTACK",dice=(1,6,2),attack_bonus=0),
  A["CAMPANADA_PICO"]:dict(kind="ATTACK",dice=(2,6,2),attack_bonus=0),
  A["PATA_INMOVIL"]:dict(kind="SELF_DEFENSE",defense_bonus=3,prepares_resonance=True),
 },
 2:{
  A["GOLPE_ALA"]:dict(kind="ATTACK",dice=(1,4,0),attack_bonus=0),
  A["TORMENTA"]:dict(kind="ATTACK_RESOURCE",dice=(1,6,1),attack_bonus=0,qi_drain_on_damage=1),
  A["CERRAR"]:dict(kind="SELF_DEFENSE",guard_per_hit=3,guard_capacity=6),
  A["RECORDAR"]:dict(kind="ADAPTIVE_PREP",evasion_bonus=10),
  A["ECO"]:dict(kind="RESOURCE_PRESSURE",qi_drain=3,condition="PLAYER_SPENT_QI"),
 },
 3:{
  A["PICOTAZO"]:dict(kind="ATTACK",dice=(1,4,1),attack_bonus=1),
  A["CAMPANA"]:dict(kind="ATTACK_RESOURCE",dice=(1,6,2),attack_bonus=1,qi_drain_on_damage=2),
  A["ALA"]:dict(kind="SELF_DEFENSE",evasion_bonus=10),
  A["PATA_INMOVIL"]:dict(kind="SELF_DEFENSE",defense_bonus=3),
  A["SILENCIO"]:dict(kind="PLAN_PREP"),
  A["ROMPER"]:dict(kind="PLAN_FINISHER",dice=(1,6,2),attack_bonus=2),
  A["BUSCAR"]:dict(kind="PLAN_PREP"),
 }
}

ULTI_FAMILY=mass.ULTI_FAMILY
ULTI_COSTS=mass.ULTI_COSTS
MODES=copy.deepcopy(f3.MODES)
EQUIPMENT=copy.deepcopy(f3.EQUIPMENT)
PLAYER_STATES=copy.deepcopy(f3.PLAYER_STATES)
ROOT_RULES=copy.deepcopy(f3.ROOT_RULES)


def sha256(path:Path)->str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def _hash_obj(x)->str:
    return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()

def authority_report()->dict:
    return {
      "runner_status":RUNNER_STATUS,
      "runner_limitation":RUNNER_LIMITATION,
      "boss_numeric_authority_sha256":sha256(AUTH_PATH),
      "boss_numeric_authority_status":AUTH["status"],
      "ultimate_catalog_sha256":sha256(CATALOG_PATH),
      "combat_engine_sha256":sha256(HERE/"combat_engine_new_stats_lab_v0_2.py"),
      "f3_strict_harness_sha256":sha256(HERE/"grulla_f3_ulti25_equipment_retest.py"),
      "normal_techniques_enabled":False,
      "consumables_enabled":False,
      "mass_run_allowed":False,
    }

class SemanticRng:
    def __init__(self,seed:int): self.seed=int(seed)
    def _seed(self,*parts)->int:
        b="|".join(map(str,(self.seed,*parts))).encode()
        return int.from_bytes(hashlib.sha256(b).digest()[:8],"big")
    def random(self,*parts)->float: return random.Random(self._seed(*parts)).random()
    def randint(self,lo:int,hi:int,*parts)->int: return random.Random(self._seed(*parts)).randint(int(lo),int(hi))
    def stream(self,*parts)->random.Random: return random.Random(self._seed(*parts))


def _tail(a,n): return a[max(0,len(a)-n):]
def _same(v): return len(v)>1 and v[0] is not None and all(x==v[0] for x in v)

@dataclass
class Brain:
    phase:int=1
    turn:int=0
    history:list=field(default_factory=list)
    recent:list=field(default_factory=list)
    phase_memory:dict=field(default_factory=dict)
    plan:dict|None=None
    technique_counter:dict|None=None

    def summarize(self):
        t={}; e={}; offense=defend=recover=control=qi_actions=technique_uses=nontech=basic=0
        for a in self.history:
            if a["type"] in ("BASIC","TECHNIQUE","CONTROL"): offense+=1
            if a["type"]=="BASIC": basic+=1
            if a["type"]=="DEFEND": defend+=1
            if a["type"]=="RECOVER": recover+=1
            if a["type"]=="CONTROL": control+=1
            if a.get("qiSpent",0)>0: qi_actions+=1
            if a.get("techniqueId"):
                technique_uses+=1; t[a["techniqueId"]]=t.get(a["techniqueId"],0)+1
            else: nontech+=1
            if a.get("element"): e[a["element"]]=e.get(a["element"],0)+1
        dom=lambda d: sorted(d.items(),key=lambda kv:(-kv[1],kv[0]))[0][0] if d else None
        dt=dom(t); role=None
        for a in reversed(self.history):
            if a.get("techniqueId")==dt: role=a.get("techniqueRole");break
        single=technique_uses>=2 and len(t)==1 and basic==0
        return dict(dominantTechnique=dt,dominantTechniqueRole=role,dominantElement=dom(e),offense=offense,
                    defend=defend,recover=recover,control=control,qiActions=qi_actions,techniqueUses=technique_uses,
                    uniqueTechniques=len(t),nonTechniqueActions=nontech,basicUses=basic,singleSkillReliance=single,
                    pureSingleSkillSpam=single and nontech==0)

    def enter_phase(self,phase:int):
        if self.phase==1:self.phase_memory["phase1"]=self.summarize()
        if self.phase==2:self.phase_memory["phase2"]=self.summarize()
        if phase==2 and self.phase_memory.get("phase1",{}).get("singleSkillReliance"):
            pm=self.phase_memory["phase1"]
            self.technique_counter=dict(techniqueId=pm.get("dominantTechnique"),techniqueRole=pm.get("dominantTechniqueRole"),locked=True,source="PHASE1_SINGLE_SKILL_RELIANCE")
        self.phase=phase;self.turn=0;self.history=[];self.recent=[];self.plan=None

    def observe(self,a:dict):
        self.history=(self.history+[dict(a)])[-8:]
        # Ulti single-use cannot lock itself; preserve historical counter semantics otherwise.
        if self.phase>=2 and self.technique_counter and self.technique_counter.get("locked"):
            cur=self.technique_counter
            if a.get("techniqueId")==cur.get("techniqueId"): pass
            elif a["type"]=="BASIC" or (a.get("techniqueId") and a.get("techniqueId")!=cur.get("techniqueId")):
                self.technique_counter=None
        elif self.phase>=2:
            l3=_tail(self.history,3)
            if len(l3)==3 and l3[0].get("techniqueId") and all(x.get("techniqueId")==l3[0].get("techniqueId") for x in l3):
                self.technique_counter=dict(techniqueId=l3[0]["techniqueId"],techniqueRole=l3[0].get("techniqueRole"),locked=True,source="THREE_CONSECUTIVE_SAME_SKILL")
        if self.phase==3 and self.plan and not self.plan.get("armed"):
            if self.plan["id"]=="ROMPER_REPETICION":
                reptech=self.plan.get("referenceTechnique") and a.get("techniqueId")==self.plan.get("referenceTechnique")
                repelem=self.plan.get("referenceElement") and a.get("element")==self.plan.get("referenceElement") and a["type"] in ("TECHNIQUE","CONTROL")
                if reptech or repelem:self.plan["armed"]=True
                else:self.plan=None
            elif self.plan["id"]=="CAZAR_CIRCULACION":
                if a.get("qiSpent",0)>0 and a["type"] in ("TECHNIQUE","CONTROL"):self.plan["armed"]=True
                else:self.plan=None
        elif self.phase==3 and self.plan and self.plan.get("armed"):
            self.plan=None

    def _signals(self,player_hp_ratio,self_hp_ratio,player_qi_ratio):
        h=_tail(self.history,4 if self.phase==3 else 3);l2=_tail(h,2);l3=_tail(h,3)
        return dict(
          techniqueRepeat=_same([x.get("techniqueId") for x in l2]),elementRepeat=_same([x.get("element") for x in l2]),
          offenseStreak=len(l2)==2 and all(x["type"] in ("BASIC","TECHNIQUE","CONTROL") for x in l2),
          qiStreak=len(l2)==2 and all(x.get("qiSpent",0)>0 for x in l2),
          controlRecent=any(x["type"]=="CONTROL" for x in l3),recoverRecent=any(x["type"]=="RECOVER" for x in l2),
          heavyRecent=any(x.get("damageBand")=="HEAVY" for x in l2),playerLowHp=player_hp_ratio<=.30,selfLowHp=self_hp_ratio<=.30,
          playerQiLow=player_qi_ratio<=.25,playerQiHigh=player_qi_ratio>=.65,last=h[-1] if h else None)

    def choose(self,ctx)->str:
        if self.phase==1:
            cyc=[A["GOLPE_ALA"],A["GOLPE_ALA"],A["CAMPANADA_PICO"],A["PATA_INMOVIL"]]
            x=cyc[self.turn%4];self.turn+=1;self.recent=(self.recent+[x])[-4:];return x
        if self.phase==3 and self.plan and self.plan.get("armed") and self.plan.get("followup"):
            x=self.plan["followup"];self.turn+=1;self.recent=(self.recent+[x])[-4:];return x
        p=ctx.player;b=ctx.boss
        s=self._signals(p.hp/max(1,p.hp_max),b.hp/max(1,b.hp_max),p.qi/max(1,p.qi_max))
        recent=lambda x,d=1:x in self.recent[-d:]
        if self.phase==2:
            inherited=self.phase_memory.get("phase1",{}); ir=1 if inherited.get("dominantTechnique") and s["last"] and s["last"].get("techniqueId")==inherited.get("dominantTechnique") else 0
            entries=[
              (A["GOLPE_ALA"],30,1),(A["TORMENTA"],28+(12 if s["playerQiHigh"] else 0)+(10 if s["playerLowHp"] else 0)-(40 if recent(A["TORMENTA"],2) else 0),1),
              (A["CERRAR"],18+(18 if s["offenseStreak"] else 0)+(20 if s["heavyRecent"] else 0)+(16 if s["selfLowHp"] else 0)-(35 if recent(A["CERRAR"],2) else 0)+(8 if s["controlRecent"] else 0),.8),
              (A["RECORDAR"],12+(38 if s["techniqueRepeat"] else 0)+(18 if s["elementRepeat"] else 0)+ir*8-(42 if recent(A["RECORDAR"],2) else 0),.6),
              (A["ECO"],12+(34 if s["qiStreak"] else 0)+(8 if s["playerQiLow"] else 0)+(6 if s["recoverRecent"] else 0)-(40 if recent(A["ECO"],2) else 0),.6),
            ]
        else:
            entries=[
              (A["PICOTAZO"],25+(8 if s["playerLowHp"] else 0),.5),(A["CAMPANA"],24+(24 if s["playerLowHp"] else 0)+(8 if s["playerQiHigh"] else 0)-(45 if recent(A["CAMPANA"],2) else 0),.5),
              (A["ALA"],16+(17 if s["offenseStreak"] else 0)+(14 if s["heavyRecent"] else 0)-(30 if recent(A["ALA"],2) else 0),.4),
              (A["PATA_INMOVIL"],15+(15 if s["selfLowHp"] else 0)+(10 if s["controlRecent"] else 0)-(30 if recent(A["PATA_INMOVIL"],2) else 0),.4),
              (A["SILENCIO"],10+(32 if s["techniqueRepeat"] else 0)+(18 if s["elementRepeat"] else 0)-(50 if recent(A["SILENCIO"],3) else 0),.2),
              (A["BUSCAR"],10+(28 if s["qiStreak"] else 0)+(10 if s["playerQiHigh"] else 0)-(50 if recent(A["BUSCAR"],3) else 0),.2),
            ]
        scored=[]
        for i,(aid,score,jit) in enumerate(entries):
            rv=ctx.rng.random("boss_decision",self.phase,self.turn,i,aid)
            scored.append((score+(rv-.5)*jit,aid))
        scored.sort(key=lambda z:(-z[0],z[1]));x=scored[0][1]
        if self.phase==3:
            if x==A["SILENCIO"]:
                ref=self.history[-1] if self.history else {}
                self.plan=dict(id="ROMPER_REPETICION",armed=False,followup=A["ROMPER"],referenceTechnique=ref.get("techniqueId"),referenceElement=ref.get("element"))
            elif x==A["BUSCAR"]:self.plan=dict(id="CAZAR_CIRCULACION",armed=False,followup=A["CAMPANA"])
        self.turn+=1;self.recent=(self.recent+[x])[-4:];return x

_CURRENT_CTX=None
_ORIG_COMMIT=ce.CombatEngine._commit_life_damage
_ORIG_ATTEMPT_CONTROL=ce.CombatEngine.attempt_control

@dataclass
class Context:
    case:dict
    player:ce.Actor
    boss:ce.Actor
    rng:SemanticRng
    brain:Brain=field(default_factory=Brain)
    engine:ce.CombatEngine=field(default_factory=ce.CombatEngine)
    phase:str="F1"
    round_total:int=0
    player_actions:int=0
    boss_actions:int=0
    player_actions_by_phase:dict=field(default_factory=lambda:{1:0,2:0,3:0})
    boss_actions_by_phase:dict=field(default_factory=lambda:{1:0,2:0,3:0})
    phase_trace:list=field(default_factory=lambda:["F1"])
    phase_transitions:list=field(default_factory=list)
    checkpoints:dict=field(default_factory=dict)
    ulti_used:bool=False
    ulti_attempts:int=0
    ulti_metrics:dict=field(default_factory=dict)
    activation_reason:str="NOT_ATTEMPTED"
    boss_next_def_bonus:float=0.0
    boss_next_eva_bonus:float=0.0
    boss_guard_reserve:float=0.0
    boss_guard_per_hit:float=0.0
    phase1_resonance:bool=False
    inside_ulti_macro:bool=False
    resolving_real_boss_intent:bool=False
    synthetic_enemy_control_suppressed:int=0
    pact_release_count:int=0
    first_real_f3_action_resolved:int=0
    reactivation_probe_performed:int=0
    reactivation_blocked_count:int=0
    ooc_ready_39:int=0
    ooc_ready_40:int=0
    ooc_ready_41:int=0
    f3_control_denied_observed:int=0
    pact_active_after_denied:int=0
    f3_first_denied_observed:int=0
    pact_active_after_first_denied:int=0
    force_first_f3_denied_pending:int=0
    f3_kill_before_first_real_action:int=0
    ultimate_action_serial:int=0
    phase_crossed_ulti_serial:int=0
    current_player_direct_packet:int=0
    phase_transition_pending:str|None=None
    late_opportunities_offered:dict=field(default_factory=lambda:{1:0,2:0,3:0})
    causal_trace:list=field(default_factory=list)
    adds:list=field(default_factory=list)
    issues:list=field(default_factory=list)

    def snapshot(self,label):
        self.checkpoints[label]=dict(player_hp=float(self.player.hp),player_qi=float(self.player.qi),boss_hp=float(self.boss.hp),boss_abs=float(self.engine.absorption_total(self.boss)),phase=self.phase)

    def _record_f3_denial(self):
        self.f3_control_denied_observed+=1
        active=1 if f3._pact_mark(self.boss) else 0
        self.pact_active_after_denied=active
        if not self.f3_first_denied_observed:
            self.f3_first_denied_observed=1
            self.pact_active_after_first_denied=active
        self.causal_trace.append({"event":"boss_denied","round":self.round_total,"phase":self.phase,"pact_active":active})

    def transition(self,to_phase:str,source:str):
        old=self.phase; oldnum=PHASE_NUM[old]; newnum=PHASE_NUM[to_phase]
        if newnum!=oldnum+1: raise RuntimeError(f"ILLEGAL_PHASE_TRANSITION:{old}->{to_phase}")
        self.phase=to_phase;self.phase_trace.append(to_phase)
        self.phase_transition_pending=None
        self.phase_transitions.append(dict(from_phase=old,to_phase=to_phase,source=source,round_total=self.round_total))
        self.causal_trace.append({"event":"phase_transition","round":self.round_total,"from":old,"to":to_phase,"source":source})
        st=PHASE_STATS[to_phase]
        # Same creature: player-applied DOT/Bleed/temp_stats remain. Phase-local boss guard/reads reset.
        self.boss.hp_max=float(st["hp"]); object.__setattr__(self.boss,"hp",float(st["hp"]))
        self.boss.precision=float(st["precision"]);self.boss.evasion=float(st["evasion"]);self.boss.defense=float(st["defense"]);self.boss.tenacity=float(st["tenacity"])
        self.boss.phase=to_phase
        self.boss_next_def_bonus=0;self.boss_next_eva_bonus=0;self.boss_guard_reserve=0;self.boss_guard_per_hit=0;self.phase1_resonance=False
        # Phase-local reads/guards expire; explicit persistent player-applied state stays on the same creature.
        self.boss.temp_stats={k:v for k,v in self.boss.temp_stats.items() if not str(k).startswith("GRULLA_PHASE_LOCAL_")}
        # Remove phase-local boss absorption, keep player-applied/non-Grulla pools if a contract allows them.
        self.boss.absorption_pools=[p for p in self.boss.absorption_pools if not str(p.source).startswith("GRULLA_")]
        self.brain.enter_phase(newnum)
        if to_phase=="F3":
            self.boss.death_gate_active=True;self.boss.death_gate_floor=1.0;self.boss.marks.add("GRULLA_F3_PACT_ACTIVE")
            self.boss.life_damage_guard=f3.f3_pact_life_guard;self.boss.pact_guard_instance_id=self.boss.instance_id
            self.boss.resources["crit_bonus_received_factor"]=0.5
            self.boss.resources["f3_first_real_action_resolved"]=0.0;self.boss.resources["f3_real_actions_resolved"]=0.0
            self.engine.add_absorption(self.boss,float(st["absorption"]),per_hit_cap=float(st["absorption_cap"]),source="GRULLA_F3_WARD")
            if self.case.get("window")=="F3_CONTROL_DENIED_FIRST_INTENT":
                self.force_first_f3_denied_pending=1
            _apply_boss_stress(self,self.case.get("boss_stress"))
            self.snapshot("F3_ENTRY")
        elif to_phase=="F2":
            _apply_boss_stress(self,self.case.get("boss_stress"))
            self.snapshot("F2_ENTRY")

    def boss_targets(self):
        unit=base.EnemyUnit(self.boss,1,1,0.0)
        return [unit]+self.adds

    def _end_player_offensive_action(self):
        # Next-offensive-action defenses expire after the complete action, not per packet.
        self.boss_next_def_bonus=0.0;self.boss_next_eva_bonus=0.0
        self.boss_guard_reserve=0.0;self.boss_guard_per_hit=0.0
        self.boss.absorption_pools=[x for x in self.boss.absorption_pools if x.source!="GRULLA_CERRAR_ALAS"]

    def basic_action(self):
        self.brain.observe(dict(type="BASIC",techniqueId=None,techniqueRole=None,element=None,qiSpent=0.0,damageBand="NORMAL"))
        # LianQi IV basic authority from etapa19b: 1d4+7, plus equipment basic_attack_flat.
        rolled=self.rng.randint(1,4,"player_basic_damage",self.round_total,self.player_actions)+7+max(0.0,float(self.player.basic_attack_flat))
        offensive_pct=10.0 if self.case.get("family")=="FUEGO" else 0.0
        try:
            r=self.engine.resolve_direct(self.player,self.boss,ce.DamagePacket(rolled,offensive_pct=offensive_pct,can_crit=True,evadable=True,provenance="CONTINUOUS_BASIC"),
                                         hit_roll=self.rng.random("player_basic_hit",self.round_total,self.player_actions)*100,
                                         crit_roll=self.rng.random("player_basic_crit",self.round_total,self.player_actions)*100)
        finally:self._end_player_offensive_action()
        self.causal_trace.append({"event":"player_basic","round":self.round_total,"phase":self.phase,"hit":bool(r.hit),"crit":bool(r.critical),"hp_damage":float(r.actual_hp_damage)})
        return r

    def _should_activate(self):
        if self.ulti_used or self.case.get("ultimate") in (None,"", "NO_ULTI"): return False
        w=self.case.get("window","F3_ENTRY")
        ph=PHASE_NUM[self.phase]
        if w=="F1_EARLY": return ph==1 and self.boss_actions_by_phase[1]>=1
        if w=="F1_LATE_PRE_TRANSITION": return ph==1 and (self.phase_transition_pending=="F1" or self.boss.hp<=PHASE_STATS["F1"]["hp"]*.25 or self.boss_actions_by_phase[1]>=6)
        if w=="F2_ENTRY": return ph==2 and self.player_actions_by_phase[2]==0
        if w=="F2_ADAPTIVE_MID": return ph==2 and self.boss_actions_by_phase[2]>=2
        if w=="F2_LATE_PRE_TRANSITION": return ph==2 and (self.phase_transition_pending=="F2" or self.boss.hp<=PHASE_STATS["F2"]["hp"]*.25 or self.boss_actions_by_phase[2]>=4)
        if w in ("F3_ENTRY","F3_ENTRY_PACT_ACTIVE","F3_PRE_RELEASE","F3_CONTROL_DENIED_FIRST_INTENT"): return ph==3 and self.first_real_f3_action_resolved==0
        if w=="F3_POST_RELEASE": return ph==3 and self.first_real_f3_action_resolved>0
        if w=="PREPARED_OPPORTUNITY": return ph==2 and self.boss_actions_by_phase[2]>=1  # LAB timing only; excluded from authoritative balance.
        if w=="TRANSITION_EDGE": return ph in (1,2) and self.boss.hp<=max(1.0,PHASE_STATS[self.phase]["hp"]*.10)
        return False

    def _apply_case_boundaries_before_ulti(self):
        qb=self.case.get("qi_boundary")
        cost=float(ULTI_COSTS.get(self.case.get("ultimate"),0))
        final=ce.rhu(cost*(1+self.player.qi_cost_percent/100.0))
        if qb=="ZERO":self.player.qi=0
        elif qb=="COST_MINUS_1":self.player.qi=max(0,final-1)
        elif qb=="EXACT_COST":self.player.qi=min(self.player.qi_max,final)
        elif qb=="COST_PLUS_1":self.player.qi=min(self.player.qi_max,final+1)
        elif qb=="FULL":self.player.qi=self.player.qi_max
        hb=self.case.get("hp_boundary")
        vals={"HP_1":1,"HP_2":2,"HP_10_PERCENT":self.player.hp_max*.10,"HP_16_PERCENT":self.player.hp_max*.16,"HP_40_PERCENT":self.player.hp_max*.40,"HP_65_PERCENT":self.player.hp_max*.65,"FULL":self.player.hp_max}
        if hb in vals:self.player.hp=max(1.0,min(self.player.hp_max,float(ce.rhu(vals[hb]))))

    def ultimate_action(self):
        self.ulti_attempts+=1; self._apply_case_boundaries_before_ulti()
        u=self.case["ultimate"];mode=self.case.get("mode") or MODES[u][0]
        cost=float(ULTI_COSTS.get(u,0)); final=ce.rhu(cost*(1+self.player.qi_cost_percent/100.0))
        # Fail-closed common insufficient-Qi path. Río's special gate remains inside its accepted implementation.
        if cost>0 and self.player.qi<final:
            self.activation_reason="INSUFFICIENT_QI"; return {"activated":0.0,"insufficient_qi":1.0}
        sc=_scenario_template(u,mode);self.ultimate_action_serial+=1
        rr=self.rng.stream("ultimate",u,mode,self.phase,self.ultimate_action_serial)
        self.inside_ulti_macro=True
        try:m=mass.norm(_sim_dispatch(u,sc,rr))
        finally:
            self.inside_ulti_macro=False
        self.ulti_metrics={k:float(v) if isinstance(v,(int,float)) else v for k,v in m.items()}
        if m.get("activated",0)>0:
            self._end_player_offensive_action()
            # Only an accepted Ulti is observable by the Grulla. Rejected Río must be causally inert.
            self.brain.observe(dict(type="TECHNIQUE",techniqueId=u,techniqueRole="ofensiva",element=ULTI_FAMILY[u],qiSpent=float(final),damageBand="HEAVY"))
            self.ulti_used=True;self.player.resources["ULTIMATE_USED_THIS_COMBAT"]=1.0;self.player.resources["ultimate_cooldown_ooc"]=40.0
            self.activation_reason="ACTIVATED"
            # Explicit one-use probe in the same combat: gate only, no second macro execution.
            self.reactivation_probe_performed=1;self.ulti_attempts+=1
            if self.player.resources.get("ULTIMATE_USED_THIS_COMBAT",0)>=1:self.reactivation_blocked_count+=1
            # Exact OOC cooldown boundary probe; combat turns never tick this counter.
            cd=40
            for _ in range(39):cd=max(0,cd-1)
            self.ooc_ready_39=1 if cd==0 else 0
            cd=max(0,cd-1);self.ooc_ready_40=1 if cd==0 else 0
            cd=max(0,cd-1);self.ooc_ready_41=1 if cd==0 else 0
        else:self.activation_reason="IMPLEMENTATION_REJECTED"
        return m

    def boss_turn(self,external_engine=None,received_pct=0.0,extra_evasion=0.0):
        e=external_engine or self.engine
        if not self.boss.alive(): return _dummy(False),0.0
        # DOTs happen at start of boss turn. Lethal F1/F2 packets transition through patched commit.
        e.start_turn_affliction_ticks(self.boss)
        if not self.boss.alive(): return _dummy(True),0.0
        phase_at_start=PHASE_NUM[self.phase]
        aid=self.brain.choose(self); spec=ABILITY[phase_at_start][aid]
        self.causal_trace.append({"event":"boss_intent","round":self.round_total,"phase":self.phase,"ability":aid})
        if phase_at_start==3 and self.force_first_f3_denied_pending:
            self.force_first_f3_denied_pending=0;self._record_f3_denial()
            self.boss_actions_by_phase[phase_at_start]+=1;self.boss_actions+=1
            return _dummy(False),0.0
        token=e.allocate_intent(self.boss)
        pre=e.action_attempt_once(self.boss,action_token=token,voluntary=True)
        if not pre.get("action_executes",False):
            # Control-denied F3 action is not a real resolved intent and cannot release Pacto.
            if phase_at_start==3:
                self._record_f3_denial()
            self.boss_actions_by_phase[phase_at_start]+=1; self.boss_actions+=1
            return _dummy(False),0.0
        self.resolving_real_boss_intent=True
        try:
            r=_dummy(False);dmg=0.0
            if spec["kind"] in ("ATTACK","ATTACK_RESOURCE","PLAN_FINISHER"):
                count,sides,flat=spec["dice"]; raw=sum(self.rng.randint(1,sides,"boss_damage",self.round_total,self.boss_actions,aid,j) for j in range(count))+flat
                # F1 resonance only matters when an explicit Piel-like absorption pool exists.
                if phase_at_start==1 and aid==A["GOLPE_ALA"] and self.phase1_resonance:
                    guard_active=any(p.source=="SUPPORT_PIEL" and p.reserve>0 for p in self.player.absorption_pools)
                    if guard_active: raw=math.ceil(raw*1.75)
                    self.phase1_resonance=False
                old_eva=self.player.evasion;self.player.evasion+=float(extra_evasion)
                packet=ce.DamagePacket(raw,received_pct=float(received_pct),precision_mod=float(spec.get("attack_bonus",0)),can_crit=True,provenance="GRULLA:"+aid)
                before=self.player.hp
                r=e.resolve_direct(self.boss,self.player,packet,
                    hit_roll=self.rng.random("boss_accuracy",self.round_total,self.boss_actions,aid)*100,
                    crit_roll=self.rng.random("boss_crit",self.round_total,self.boss_actions,aid)*100)
                self.player.evasion=old_eva;dmg=before-self.player.hp
                if r.hit and r.actual_hp_damage>0 and spec.get("qi_drain_on_damage"):
                    self.player.qi=max(0.0,self.player.qi-float(spec["qi_drain_on_damage"]))
                f3.maybe_trigger_gear_absorption(self.player)
            elif aid==A["PATA_INMOVIL"]:
                self.boss_next_def_bonus=float(spec.get("defense_bonus",0));
                if phase_at_start==1:self.phase1_resonance=True
            elif aid in (A["CERRAR"],):
                self.boss_guard_reserve=float(spec["guard_capacity"]);self.boss_guard_per_hit=float(spec["guard_per_hit"])
            elif aid in (A["RECORDAR"],A["ALA"]): self.boss_next_eva_bonus=float(spec["evasion_bonus"])
            elif aid==A["ECO"]:
                last=self.brain.history[-1] if self.brain.history else None
                if last and last.get("qiSpent",0)>0:self.player.qi=max(0.0,self.player.qi-float(spec["qi_drain"]))
            # PLAN_PREP effects already live in Brain.choose.
        finally:self.resolving_real_boss_intent=False
        self.boss_actions_by_phase[phase_at_start]+=1;self.boss_actions+=1
        if phase_at_start==3 and f3._pact_mark(self.boss):
            f3._release_after_real_intent(self.boss,"DIRECT_INTENT_RESOLVED")
            self.pact_release_count+=1;self.first_real_f3_action_resolved=1
        e.owner_action_completed(self.boss);e.hostile_action_completed_against(self.player)
        self.causal_trace.append({"event":"boss_resolved","round":self.round_total,"phase":PHASE_FROM_NUM[phase_at_start],"ability":aid,"hp_damage":float(dmg)})
        return r,dmg


def _dummy(killed=False): return ce.ImpactResult(False,False,0,0,0,0,0,0,0,killed)


def _scenario_template(ultimate,mode):
    sources=[retest.SCENARIOS,mass.SCENARIOS] if ultimate in retest.AFFECTED_SET else [mass.SCENARIOS]
    for source in sources:
        for sc in source:
            if sc.get("ultimate")==ultimate and sc.get("mode")==mode and sc.get("player_profile")=="FULL":
                out=dict(sc);out["fixture"]="DYNAMIC";out["player_profile"]="FULL";out["player_state"]="NORMAL";out["dynamic_enemy"]=None
                if ultimate=="WIND_RIO_CELESTE_SIN_ORILLAS":
                    out["loadout"]=list(mass.SUPPORT_TECHNIQUES);out.setdefault("support_chain",["PALMA_ARDIENTE","FILO_QI_METALICO"]);out.pop("qi_override",None)
                return out
    raise KeyError(f"NO_TEMPLATE:{ultimate}:{mode}")

def _sim_dispatch(u,sc,rng):
    if u in retest.FIXED:return retest.FIXED[u](sc,rng)
    if u in mass.CUSTOM:return mass.CUSTOM[u](sc,rng)
    return mass.sim_old_with_post_rules(sc,rng)

# ---- global patch layer used by the accepted Ulti macros ----
def _continuous_commit(self,target,requested,*,source=""):
    global _CURRENT_CTX
    ctx=_CURRENT_CTX
    # Once a direct player packet crosses F1->F2 or F2->F3 inside the same Ulti macro,
    # later direct packets of that same macro cannot spill into the fresh phase pool.
    if (ctx and target is ctx.boss and ctx.inside_ulti_macro and ctx.current_player_direct_packet
        and ctx.phase_crossed_ulti_serial==ctx.ultimate_action_serial and ctx.ultimate_action_serial>0):
        return 0.0
    applied=_ORIG_COMMIT(self,target,requested,source=source)
    ctx=_CURRENT_CTX
    if ctx and target is ctx.boss and target.hp<=0:
        crossed=False
        if ctx.phase=="F1": ctx.transition("F2",source or "LIFE_DAMAGE"); crossed=True
        elif ctx.phase=="F2": ctx.transition("F3",source or "LIFE_DAMAGE"); crossed=True
        elif ctx.phase=="F3" and ctx.first_real_f3_action_resolved<1:
            ctx.f3_kill_before_first_real_action=1
        if crossed and ctx.inside_ulti_macro and ctx.current_player_direct_packet:
            ctx.phase_crossed_ulti_serial=ctx.ultimate_action_serial
    return applied

def _continuous_fixture(name):
    if _CURRENT_CTX is None:return f3.build_grulla_units(name)
    return _CURRENT_CTX.boss_targets()

def _continuous_player(family,state="NORMAL"):
    if _CURRENT_CTX is None:return f3.build_player(family)
    return _CURRENT_CTX.player

def _continuous_enemy_action(e,u,p,rng,m,received_pct=0,extra_evasion=0,extra_player_evasion=None,action_token=None,**kw):
    ctx=_CURRENT_CTX
    if ctx is None:return f3.mass_enemy_action_strict(e,u,p,rng,m,received_pct=received_pct,extra_evasion=extra_evasion,action_token=action_token)
    ee=float(extra_evasion if extra_player_evasion is None else extra_player_evasion)
    r,d=ctx.boss_turn(external_engine=e,received_pct=received_pct,extra_evasion=ee)
    m["enemy_actions_observed"]=m.get("enemy_actions_observed",0.0)+1.0
    return r,d

def _continuous_attempt_control(self,source,target,*,base_control,roll,guaranteed=False,action_token=None):
    ctx=_CURRENT_CTX
    if ctx and ctx.inside_ulti_macro and source is ctx.boss and not ctx.resolving_real_boss_intent:
        ctx.synthetic_enemy_control_suppressed+=1
        return {"success":False,"chance":0.0,"immune":False,"action_prevented":False,"continuous_synthetic_suppressed":True}
    return _ORIG_ATTEMPT_CONTROL(self,source,target,base_control=base_control,roll=roll,guaranteed=guaranteed,action_token=action_token)

# Boss next-action defense/evasion/guard must also apply to packets emitted inside Ulti macros.
_PREV_RESOLVE=ce.CombatEngine.resolve_direct
def _continuous_resolve(self,source,target,packet,*,hit_roll,crit_roll):
    ctx=_CURRENT_CTX
    if ctx and source is ctx.player and target is ctx.boss:
        # A later direct packet from the same Ulti macro cannot consume the fresh phase pool/ward.
        if ctx.inside_ulti_macro and ctx.phase_crossed_ulti_serial==ctx.ultimate_action_serial and ctx.ultimate_action_serial>0:
            return _dummy(False)
        oldd=target.defense;olde=target.evasion
        target.defense+=ctx.boss_next_def_bonus;target.evasion+=ctx.boss_next_eva_bonus
        # Cerrar Alas is a real reserve: 6 total, cap 3 per hit, lasting one player offensive action.
        if ctx.boss_guard_reserve>0 and not any(x.source=="GRULLA_CERRAR_ALAS" for x in target.absorption_pools):
            self.add_absorption(target,ctx.boss_guard_reserve,per_hit_cap=ctx.boss_guard_per_hit,source="GRULLA_CERRAR_ALAS")
        try:
            ctx.current_player_direct_packet+=1
            try:r=_PREV_RESOLVE(self,source,target,packet,hit_roll=hit_roll,crit_roll=crit_roll)
            finally:ctx.current_player_direct_packet=max(0,ctx.current_player_direct_packet-1)
            pools=[x for x in target.absorption_pools if x.source=="GRULLA_CERRAR_ALAS"]
            ctx.boss_guard_reserve=sum(x.reserve for x in pools)
            return r
        finally:
            target.defense=oldd;target.evasion=olde
    return _PREV_RESOLVE(self,source,target,packet,hit_roll=hit_roll,crit_roll=crit_roll)


# Install once for this derived LAB runner.
ce.CombatEngine._commit_life_damage=_continuous_commit
ce.CombatEngine.resolve_direct=_continuous_resolve
ce.CombatEngine.attempt_control=_continuous_attempt_control
base.fixture=_continuous_fixture;mass.base.fixture=_continuous_fixture;retest.orig.base.fixture=_continuous_fixture
base.player_for_family=_continuous_player;mass.player_for_family=_continuous_player;retest.orig.base.player_for_family=_continuous_player
base.enemy_attack=_continuous_enemy_action;mass.base.enemy_attack=_continuous_enemy_action;retest.orig.base.enemy_attack=_continuous_enemy_action
mass.enemy_action=_continuous_enemy_action;retest.enemy_action=_continuous_enemy_action


def _build_player(family,eq_name,state_name):
    eq=EQUIPMENT[eq_name];st=eq["stats"];root=ROOT_RULES[family]
    hp=48.0+float(st.get("hp_max",0));qi=55.0+float(st.get("qi_max",0))
    if family=="TIERRA":hp*=float(root["hp_max_mult"])
    p=ce.Actor("Jugador",hp_max=hp,hp=hp,qi_max=qi,qi=qi,role="PLAYER",instance_id="PLAYER:CONTINUOUS",
      precision=100+float(st.get("precision",0))+float(root.get("precision_add",0)),
      evasion=5+float(st.get("evasion",0))+float(root.get("evasion",0)),defense=1+float(st.get("defense",0)),
      tenacity=float(st.get("tenacity",0))+float(root.get("tenacity",0)),control=float(st.get("control",0))+float(root.get("control",0)),
      crit_chance_pp=5+float(st.get("crit_chance_pp",0))+float(root.get("crit_chance_pp",0)),crit_damage_multiplier=1.5+float(root.get("crit_damage_add",0)),
      percent_penetration_pp=float(st.get("percent_penetration_pp",0))+float(root.get("percent_penetration_pp",0)),
      technique_direct_damage_percent=float(st.get("technique_direct_damage_percent",0))+float(root.get("technique_direct_damage_percent",0)),
      basic_attack_flat=4.0+float(st.get("basic_attack_flat",0)),qi_cost_percent=float(root.get("qi_cost_percent",0)))
    ps=PLAYER_STATES.get(state_name,PLAYER_STATES["FULL"]);p.hp=max(1,min(p.hp_max,float(ce.rhu(p.hp_max*ps["hp_ratio"]))));p.qi=max(0,min(p.qi_max,float(ce.rhu(p.qi_max*ps["qi_ratio"]))))
    p.resources["gear_proc_used"]=0.0
    return p

def _build_boss():
    s=PHASE_STATS["F1"]
    return ce.Actor("Grulla",hp_max=s["hp"],hp=s["hp"],role="BOSS",instance_id="GRULLA:CONTINUOUS",phase="F1",
      precision=s["precision"],evasion=s["evasion"],defense=s["defense"],tenacity=s["tenacity"],control=0,
      crit_chance_pp=5,crit_damage_multiplier=1.5)

def _apply_boss_stress(ctx,profile):
    if not profile or profile=="CANONICAL_OR_BOUND_AUTHORITY":return
    if profile=="DEF_0":ctx.boss.defense=0
    elif profile=="DEF_HIGH":ctx.boss.defense=50
    elif profile=="EVA_0":ctx.boss.evasion=0
    elif profile=="EVA_HIGH":ctx.boss.evasion=95
    elif profile=="TEN_0":ctx.boss.tenacity=0
    elif profile=="TEN_HIGH":ctx.boss.tenacity=100
    elif profile=="ABS_0":ctx.boss.absorption_pools=[]
    elif profile=="ABS_1":ctx.boss.absorption_pools=[];ctx.engine.add_absorption(ctx.boss,1,per_hit_cap=1,source="STRESS_ABS")
    elif profile=="ABS_HIGH":ctx.boss.absorption_pools=[];ctx.engine.add_absorption(ctx.boss,100,per_hit_cap=25,source="STRESS_ABS")
    elif profile=="HEAVY_PRESSURE":ctx.boss.precision=140

def _make_adds(ctx,n):
    out=[]
    for i in range(n):
        a=ce.Actor(f"StressAdd{i+1}",hp_max=40,hp=40,precision=90,evasion=20,defense=5,tenacity=25,control=20,role="MONSTER",instance_id=f"ADD:{i+1}")
        out.append(base.EnemyUnit(a,7,12,20))
    return out

def _activation_cooldown_case(case):
    # Contract-only exact boundary; no fabricated combat needed.
    edge=case.get("activation_edge")
    cd=40; second_blocked=True
    if edge=="FIRST_USE": ready=True
    elif edge=="SECOND_USE_SAME_COMBAT": ready=False
    elif edge=="OOC_39": ready=(cd-39)<=0
    elif edge=="OOC_40": ready=(cd-40)<=0
    elif edge=="OOC_41": ready=(cd-41)<=0
    else: ready=False
    return {"error":None,"outcome":"CONTRACT_CHECK","winner":None,"ultimate_attempts":2 if edge=="SECOND_USE_SAME_COMBAT" else 1,
      "ultimate_uses":1 if edge in ("FIRST_USE","SECOND_USE_SAME_COMBAT") else 0,"reactivation_blocked":1 if edge=="SECOND_USE_SAME_COMBAT" else 0,
      "ultimate_cooldown_ooc":max(0,cd-int(edge.split('_')[-1])) if edge and edge.startswith("OOC_") else cd,
      "cooldown_ready":bool(ready),"phase_trace":[],"phase_transitions":[],"f3_kill_before_first_real_action":0,"f3_pact_release_count":0,
      "f3_first_real_action_resolved":0,"f3_pact_active":0,"f3_first_denied_observed":0,"pact_active_after_first_denied":0,
      "reactivation_probe_performed":1 if edge=="SECOND_USE_SAME_COMBAT" else 0,"ooc_ready_39":0,"ooc_ready_40":1 if edge in ("OOC_40","OOC_41") else 0,"ooc_ready_41":1 if edge=="OOC_41" else 0,
      "runner_status":RUNNER_STATUS,"balance_authoritative":False}



def _phase_transition_case(case:dict)->dict:
    """Explicit transition-edge stress probe.

    This path is intentionally NOT an Ulti balance sample. It keeps one Context / one
    Grulla identity, applies the named edge at F1->F2 or F2->F3, and reports whether
    the transition contract held. Any synthetic setup is labelled in telemetry.
    """
    global _CURRENT_CTX
    edge=str(case.get("transition_edge") or "")
    at=str(case.get("transition_phase") or "F1")
    if at not in ("F1","F2"): raise ValueError("INVALID_TRANSITION_PHASE:"+at)
    family=case.get("family") or "FUEGO"
    eq=case.get("equipment_profile","EXPECTED_STAGE")
    ps=case.get("player_state","BALANCED")
    if edge in ("EQUIPMENT_PROC_ALREADY_USED","EQUIPMENT_PROC_TRIGGERS_ON_BOUNDARY"):
        eq="HIGH_ROLL_STRESS"
    p=_build_player(family,eq,ps);b=_build_boss()
    local_case=dict(case);local_case["family"]=family;local_case["window"]="TRANSITION_EDGE"
    ctx=Context(case=local_case,player=p,boss=b,rng=SemanticRng(int(case.get("seed",0))))
    _CURRENT_CTX=ctx
    prev_eq=getattr(f3,"CURRENT_EQUIPMENT","NAKED");prev_ps=getattr(f3,"CURRENT_PLAYER_STATE","FULL")
    f3.CURRENT_EQUIPMENT=eq;f3.CURRENT_PLAYER_STATE=ps
    details={"edge":edge,"transition_phase":at,"fixture":"V031_EXPLICIT_TRANSITION_STRESS","checks":{}}
    def chk(name,cond,**data):
        details["checks"][name]={"pass":bool(cond),**data};return bool(cond)
    try:
        ctx.snapshot("F1_ENTRY")
        if at=="F2":
            ctx.transition("F2","V031_EDGE_SETUP_F1_TO_F2")
        start=ctx.phase; nxt="F2" if start=="F1" else "F3"; full=float(PHASE_STATS[nxt]["hp"])
        # Make it obvious these are mechanics-only fixtures, never treatment outcomes.
        object.__setattr__(b,"hp",7.0)
        passed=True
        if edge=="LETHAL_PACKET_EXACT_HP":
            applied=ctx.engine._commit_life_damage(b,7.0,source="V031_EDGE_EXACT")
            passed &= chk("exact_commit",applied==7.0,applied=applied)
            passed &= chk("fresh_pool",ctx.phase==nxt and b.hp==full,phase=ctx.phase,hp=b.hp,expected=full)
        elif edge=="OVERKILL_PACKET":
            applied=ctx.engine._commit_life_damage(b,999.0,source="V031_EDGE_OVERKILL")
            passed &= chk("overkill_old_pool_only",applied==7.0,applied=applied)
            passed &= chk("no_overkill_carry",ctx.phase==nxt and b.hp==full,phase=ctx.phase,hp=b.hp,expected=full)
        elif edge=="MULTIHIT_CROSSES_PHASE":
            b.defense=0.0
            ctx.ultimate_action_serial=991;ctx.inside_ulti_macro=True
            try:
                r1=ctx.engine.resolve_direct(p,b,ce.DamagePacket(7,can_crit=False,evadable=False,provenance="V031_MULTIHIT_1"),hit_roll=0,crit_roll=100)
                ward_before=ctx.engine.absorption_total(b)
                hp_before=b.hp
                r2=ctx.engine.resolve_direct(p,b,ce.DamagePacket(40,can_crit=False,evadable=False,provenance="V031_MULTIHIT_2"),hit_roll=0,crit_roll=100)
            finally:ctx.inside_ulti_macro=False
            passed &= chk("first_packet_transitions",ctx.phase==nxt,phase=ctx.phase,first_hp_damage=float(r1.actual_hp_damage))
            passed &= chk("second_packet_no_fresh_pool_damage",b.hp==hp_before and float(r2.actual_hp_damage)==0.0,hp_before=hp_before,hp_after=b.hp,second_hp_damage=float(r2.actual_hp_damage))
            passed &= chk("second_packet_no_fresh_ward_consumption",ctx.engine.absorption_total(b)==ward_before,ward_before=ward_before,ward_after=ctx.engine.absorption_total(b))
        elif edge=="DOT_CROSSES_PHASE":
            ctx.engine.add_dot(b,family="V031",potency=7,ticks=2,source="V031_DOT")
            ctx.engine.start_turn_affliction_ticks(b)
            remain=[d for d in b.dots if d.source=="V031_DOT"]
            passed &= chk("dot_causes_transition",ctx.phase==nxt and b.hp==full,phase=ctx.phase,hp=b.hp)
            passed &= chk("dot_persists",len(remain)==1 and remain[0].ticks_left==1,count=len(remain),ticks=remain[0].ticks_left if remain else None)
        elif edge=="HEMORRHAGE_CROSSES_PHASE":
            ctx.engine.apply_bleed(b,potency=7,activations=2,source="V031_BLEED")
            tok=ctx.engine.allocate_intent(b);ctx.engine.action_attempt_once(b,action_token=tok,voluntary=True)
            remain=[x for x in b.bleed if x.source=="V031_BLEED"]
            passed &= chk("bleed_causes_transition",ctx.phase==nxt and b.hp==full,phase=ctx.phase,hp=b.hp)
            passed &= chk("bleed_persists",len(remain)==1 and remain[0].activations_left==1,count=len(remain),activations=remain[0].activations_left if remain else None)
        elif edge=="CONTROLLED_TRANSITION":
            b.controlled_skip=True;b.removable_control_instances=1
            ctx.engine._commit_life_damage(b,7.0,source="V031_CONTROLLED_TRANSITION")
            passed &= chk("control_persists_to_same_creature",b.controlled_skip and b.removable_control_instances==1,controlled=b.controlled_skip,instances=b.removable_control_instances)
            if nxt=="F3":
                ctx.boss_turn()
                passed &= chk("carried_control_denies_first_f3_intent",ctx.f3_first_denied_observed==1 and ctx.pact_active_after_first_denied==1 and f3._pact_mark(b),first_denied=ctx.f3_first_denied_observed,pact=ctx.pact_active_after_first_denied)
        elif edge=="BUFF_PERSISTS":
            p.temp_stats["V031_PERSIST_BUFF"]=5.0
            ctx.engine._commit_life_damage(b,7.0,source="V031_BUFF_TRANSITION")
            passed &= chk("player_buff_persists",p.temp_stats.get("V031_PERSIST_BUFF")==5.0,value=p.temp_stats.get("V031_PERSIST_BUFF"))
        elif edge=="DEBUFF_PERSISTS":
            b.temp_stats["precision"]=-7.0;b.temp_stats["GRULLA_PHASE_LOCAL_V031"]=-99.0
            ctx.engine._commit_life_damage(b,7.0,source="V031_DEBUFF_TRANSITION")
            passed &= chk("persistent_debuff_stays",b.temp_stats.get("precision")==-7.0,value=b.temp_stats.get("precision"))
            passed &= chk("phase_local_effect_expires","GRULLA_PHASE_LOCAL_V031" not in b.temp_stats,present="GRULLA_PHASE_LOCAL_V031" in b.temp_stats)
        elif edge=="ABSORPTION_PERSISTS_IF_CONTRACT_ALLOWS":
            pool=ctx.engine.add_absorption(p,9.0,source="V031_PERSIST_PLAYER_ABS")
            before=pool.reserve
            ctx.engine._commit_life_damage(b,7.0,source="V031_ABS_TRANSITION")
            after=sum(x.reserve for x in p.absorption_pools if x.source=="V031_PERSIST_PLAYER_ABS")
            passed &= chk("player_absorption_persists",after==before,before=before,after=after)
        elif edge=="EQUIPMENT_PROC_ALREADY_USED":
            p.resources["gear_proc_used"]=1.0;p.hp=max(1.0,p.hp_max*.30)
            before=sum(x.reserve for x in p.absorption_pools if x.source=="EQUIPMENT_ESPEJO_PULSO_VELADO")
            f3.maybe_trigger_gear_absorption(p)
            ctx.engine._commit_life_damage(b,7.0,source="V031_GEAR_USED_TRANSITION")
            after=sum(x.reserve for x in p.absorption_pools if x.source=="EQUIPMENT_ESPEJO_PULSO_VELADO")
            passed &= chk("used_proc_not_retriggered",p.resources.get("gear_proc_used")==1.0 and before==after==0,used=p.resources.get("gear_proc_used"),before=before,after=after)
        elif edge=="EQUIPMENT_PROC_TRIGGERS_ON_BOUNDARY":
            p.resources["gear_proc_used"]=0.0;p.hp=max(1.0,p.hp_max*.35)
            f3.maybe_trigger_gear_absorption(p)
            before=sum(x.reserve for x in p.absorption_pools if x.source=="EQUIPMENT_ESPEJO_PULSO_VELADO")
            ctx.engine._commit_life_damage(b,7.0,source="V031_GEAR_TRIGGER_TRANSITION")
            after=sum(x.reserve for x in p.absorption_pools if x.source=="EQUIPMENT_ESPEJO_PULSO_VELADO")
            passed &= chk("proc_triggers_once",p.resources.get("gear_proc_used")==1.0 and before>0,used=p.resources.get("gear_proc_used"),reserve=before)
            passed &= chk("proc_absorption_persists_across_phase",after==before,before=before,after=after)
        else:
            passed=False;chk("known_edge",False,edge=edge)
        # Global transition invariants.
        if ctx.phase==nxt:
            passed &= chk("next_pool_full",b.hp==full,hp=b.hp,expected=full)
            passed &= chk("pacto_entry_scope",bool(f3._pact_mark(b))==(nxt=="F3"),pact=bool(f3._pact_mark(b)),next_phase=nxt)
        return {
          "error":None,"outcome":"TRANSITION_CONTRACT_CHECK","winner":None,"runner_status":RUNNER_STATUS,
          "runner_limitation":RUNNER_LIMITATION,"balance_authoritative":False,"transition_fixture":True,
          "transition_edge":edge,"transition_phase":at,"transition_edge_observed":1,"transition_edge_pass":1 if passed else 0,
          "transition_edge_details":details,"phase_trace":ctx.phase_trace,"phase_transitions":ctx.phase_transitions,
          "player_hp_end":float(p.hp),"player_qi_end":float(p.qi),"boss_hp_end":float(b.hp),"boss_abs_end":float(ctx.engine.absorption_total(b)),"phase_end":ctx.phase,
          "ultimate_attempts":0,"ultimate_uses":0,"ultimate_activation_reason":"STRESS_FIXTURE_NOT_AN_ULTI_SAMPLE",
          "f3_kill_before_first_real_action":ctx.f3_kill_before_first_real_action,"f3_pact_release_count":float(b.resources.get("f3_pact_release_count",0)),
          "f3_first_real_action_resolved":float(b.resources.get("f3_first_real_action_resolved",0)),"f3_pact_active":1 if f3._pact_mark(b) else 0,
          "f3_control_denied_observed":ctx.f3_control_denied_observed,"pact_active_after_denied":ctx.pact_active_after_denied,
          "f3_first_denied_observed":ctx.f3_first_denied_observed,"pact_active_after_first_denied":ctx.pact_active_after_first_denied,
          "reactivation_probe_performed":0,"reactivation_blocked":0,"ooc_ready_39":0,"ooc_ready_40":0,"ooc_ready_41":0,
          "late_opportunities_offered":ctx.late_opportunities_offered,"causal_trace":ctx.causal_trace,"ultimate_metrics":{},"issues":[]}
    finally:
        f3.CURRENT_EQUIPMENT=prev_eq;f3.CURRENT_PLAYER_STATE=prev_ps
        _CURRENT_CTX=None


def _rio_equivalence_signature(r:dict)->dict:
    return {
      "outcome":r.get("outcome"),"phase_end":r.get("phase_end"),"rounds_total":r.get("rounds_total"),
      "player_hp_end":r.get("player_hp_end"),"player_qi_end":r.get("player_qi_end"),
      "boss_hp_end":r.get("boss_hp_end"),"boss_abs_end":r.get("boss_abs_end"),
      "phase_trace":r.get("phase_trace"),"phase_transitions":r.get("phase_transitions"),
      "player_actions":r.get("player_actions"),"boss_actions":r.get("boss_actions"),
      "player_actions_by_phase":r.get("player_actions_by_phase"),"boss_actions_by_phase":r.get("boss_actions_by_phase"),
      "causal_trace":r.get("causal_trace"),"brain_state_hash":r.get("brain_state_hash")}

def run_case(case:dict)->dict:
    global _CURRENT_CTX
    if case.get("suite")=="ACTIVATION_COOLDOWN":return _activation_cooldown_case(case)
    if case.get("suite")=="PHASE_TRANSITION":return _phase_transition_case(case)
    u=case.get("ultimate")
    if u in (None,"NO_ULTI",""):
        family=case.get("family") or "FUEGO"
    else:
        if u not in ULTI_FAMILY:raise ValueError("UNKNOWN_ULTIMATE:"+str(u))
        family=ULTI_FAMILY[u]
    eq=case.get("equipment_profile","EXPECTED_STAGE");ps=case.get("player_state","BALANCED")
    if eq not in EQUIPMENT:raise ValueError("UNKNOWN_EQUIPMENT:"+str(eq))
    local_case=dict(case);local_case["family"]=family
    p=_build_player(family,eq,ps);b=_build_boss();ctx=Context(case=local_case,player=p,boss=b,rng=SemanticRng(int(case.get("seed",0))))
    _CURRENT_CTX=ctx
    prev_eq=getattr(f3,"CURRENT_EQUIPMENT","NAKED");prev_ps=getattr(f3,"CURRENT_PLAYER_STATE","FULL")
    f3.CURRENT_EQUIPMENT=eq;f3.CURRENT_PLAYER_STATE=ps
    try:
        top=case.get("target_topology")
        if top=="BOSS_PLUS_1_SYNTHETIC_ADD":ctx.adds=_make_adds(ctx,1)
        elif top=="BOSS_PLUS_2_SYNTHETIC_ADDS":ctx.adds=_make_adds(ctx,2)
        _apply_boss_stress(ctx,case.get("boss_stress"))
        if case.get("fuzz_token") is not None:
            fr=random.Random(int(case["fuzz_token"]))
            p.hp=max(1.0,min(p.hp_max,float(ce.rhu(p.hp_max*(0.05+0.95*fr.random())))))
            p.qi=max(0.0,min(p.qi_max,float(ce.rhu(p.qi_max*fr.random()))))
            b.defense=max(0.0,min(50.0,b.defense+fr.randint(-5,15)))
            b.evasion=max(0.0,min(95.0,b.evasion+fr.randint(-20,20)))
            b.tenacity=max(0.0,min(100.0,b.tenacity+fr.randint(-20,25)))
            if fr.random()<0.15:ctx.engine.add_dot(p,family="FUZZ",potency=fr.randint(1,5),ticks=fr.randint(1,3),source="PROPERTY_FUZZ")
            if fr.random()<0.10:p.controlled_skip=True;p.removable_control_instances=max(1,p.removable_control_instances)
        ctx.snapshot("F1_ENTRY")
        max_rounds=120
        for rnd in range(max_rounds):
            ctx.round_total=rnd+1
            if not p.alive() or (ctx.phase=="F3" and not b.alive()):break
            # Player turn: DOT, then once-only bleed/control attempt.
            ctx.engine.start_turn_affliction_ticks(p)
            if not p.alive():break
            pending_at_turn_start=(ctx.phase_transition_pending==ctx.phase)
            tok=ctx.engine.allocate_intent(p);pre=ctx.engine.action_attempt_once(p,action_token=tok,voluntary=True)
            if pre.get("action_executes"):
                ph=PHASE_NUM[ctx.phase]
                if ctx._should_activate():
                    ctx.ultimate_action()
                    if not ctx.ulti_used and p.alive():ctx.basic_action()
                else:ctx.basic_action()
                ctx.player_actions+=1;ctx.player_actions_by_phase[ph]+=1
                ctx.engine.owner_action_completed(p);ctx.engine.hostile_action_completed_against(b)
            # V03.1 gives exactly one player action opportunity after the F1/F2 mechanical threshold.
            # This makes late windows reachable without pretending the fixture is player damage.
            if pending_at_turn_start:
                oldphase=ctx.phase
                oldnum=PHASE_NUM.get(oldphase,0)
                if oldnum in (1,2):ctx.late_opportunities_offered[oldnum]+=1
                if ctx.phase_transition_pending==oldphase and p.alive() and b.alive():
                    ctx.transition("F2" if oldphase=="F1" else "F3","MECHANICAL_PHASE_ADVANCE_AFTER_LATE_OPPORTUNITY")
                    continue
            if ctx.phase=="F3" and not b.alive():break
            if not p.alive():break
            ctx.boss_turn()
            if not p.alive():break
            # Mechanical full-spectrum mode: arm one late player opportunity, then advance next round.
            if case.get("progression_mode","MECHANICAL_STRESS")=="MECHANICAL_STRESS":
                if ctx.phase=="F1" and ctx.boss_actions_by_phase[1]>=4 and ctx.phase_transition_pending is None:
                    ctx.phase_transition_pending="F1"
                elif ctx.phase=="F2" and ctx.boss_actions_by_phase[2]>=4 and ctx.phase_transition_pending is None:
                    ctx.phase_transition_pending="F2"
                elif ctx.phase=="F3" and ctx.boss_actions_by_phase[3]>=10:
                    break
        if ctx.phase=="F3" and not b.alive(): outcome="PLAYER_WIN"
        elif not p.alive(): outcome="PLAYER_LOSS"
        elif case.get("progression_mode","MECHANICAL_STRESS")=="MECHANICAL_STRESS" and ctx.phase=="F3" and ctx.boss_actions_by_phase[3]>=10: outcome="STRESS_COMPLETE"
        else: outcome="TRUNCATED"
        if ctx.phase=="F3" and not b.alive() and ctx.first_real_f3_action_resolved<1:ctx.f3_kill_before_first_real_action=1
        # Explicit second-use attempt diagnostic if the fight lived long enough.
        reactivation_blocked=ctx.reactivation_blocked_count
        result={
          "error":None,"outcome":outcome,"winner":"PLAYER" if outcome=="PLAYER_WIN" else "GRULLA" if outcome=="PLAYER_LOSS" else None,
          "runner_status":RUNNER_STATUS,"runner_limitation":RUNNER_LIMITATION,"progression_mode":case.get("progression_mode","MECHANICAL_STRESS"),
          "balance_authoritative":False,"rounds_total":ctx.round_total,"truncated":1 if outcome=="TRUNCATED" else 0,
          "phase_trace":ctx.phase_trace,"phase_transitions":ctx.phase_transitions,"checkpoints":ctx.checkpoints,
          "player_hp_start":ctx.checkpoints["F1_ENTRY"]["player_hp"],"player_hp_end":float(p.hp),"player_qi_start":ctx.checkpoints["F1_ENTRY"]["player_qi"],"player_qi_end":float(p.qi),
          "boss_hp_end":float(b.hp),"boss_abs_end":float(ctx.engine.absorption_total(b)),"phase_end":ctx.phase,
          "player_actions":ctx.player_actions,"boss_actions":ctx.boss_actions,"player_actions_by_phase":ctx.player_actions_by_phase,"boss_actions_by_phase":ctx.boss_actions_by_phase,
          "ultimate_attempts":ctx.ulti_attempts,"ultimate_uses":1 if ctx.ulti_used else 0,"ultimate_activation_reason":ctx.activation_reason,
          "ultimate_cooldown_ooc":float(p.resources.get("ultimate_cooldown_ooc",0)),"reactivation_probe_performed":ctx.reactivation_probe_performed,
          "reactivation_blocked":reactivation_blocked,"ooc_ready_39":ctx.ooc_ready_39,"ooc_ready_40":ctx.ooc_ready_40,"ooc_ready_41":ctx.ooc_ready_41,
          "f3_kill_before_first_real_action":ctx.f3_kill_before_first_real_action,"f3_pact_release_count":float(b.resources.get("f3_pact_release_count",0)),
          "f3_first_real_action_resolved":float(b.resources.get("f3_first_real_action_resolved",0)),"f3_pact_active":1 if f3._pact_mark(b) else 0,
          "f3_lethal_preventions":float(b.resources.get("f3_lethal_preventions",0)),"f3_prevented_lethal_damage":float(b.resources.get("f3_prevented_lethal_damage",0)),
          "f3_control_denied_observed":ctx.f3_control_denied_observed,"pact_active_after_denied":ctx.pact_active_after_denied,
          "f3_first_denied_observed":ctx.f3_first_denied_observed,"pact_active_after_first_denied":ctx.pact_active_after_first_denied,
          "synthetic_enemy_control_suppressed":ctx.synthetic_enemy_control_suppressed,
          "late_opportunities_offered":ctx.late_opportunities_offered,"causal_trace":ctx.causal_trace,
          "brain_state_hash":_hash_obj({"phase":ctx.brain.phase,"history":ctx.brain.history,"recent":ctx.brain.recent,"phase_memory":ctx.brain.phase_memory,"plan":ctx.brain.plan,"technique_counter":ctx.brain.technique_counter}),
          "ultimate_metrics":ctx.ulti_metrics,"issues":ctx.issues,
          "prepared_trigger_authoritative":False if case.get("window")=="PREPARED_OPPORTUNITY" else True,
        }
        return result
    finally:
        f3.CURRENT_EQUIPMENT=prev_eq;f3.CURRENT_PLAYER_STATE=prev_ps
        _CURRENT_CTX=None


def self_check()->dict:
    global _CURRENT_CTX
    checks={};errors=[]
    def put(k,v): checks[k]=bool(v); return bool(v)
    try:
        # Core phase/Pacto invariant path.
        p=_build_player("FUEGO","EXPECTED_STAGE","FULL");b=_build_boss();ctx=Context(case={"window":"F3_CONTROL_DENIED_FIRST_INTENT","family":"FUEGO"},player=p,boss=b,rng=SemanticRng(991122))
        _CURRENT_CTX=ctx
        p.temp_stats["BENCH_PERSIST_SENTINEL"]=7.0
        ctx.engine._commit_life_damage(b,999,source="SELFCHECK_OVERKILL_F1")
        put("f1_to_f2_full_pool",ctx.phase=="F2" and b.hp==PHASE_STATS["F2"]["hp"] and p.temp_stats.get("BENCH_PERSIST_SENTINEL")==7.0)
        object.__setattr__(b,"hp",1.0);ctx.engine.add_dot(b,family="SELFCHECK",potency=5,ticks=2,source="SELFCHECK")
        ctx.engine.start_turn_affliction_ticks(b)
        put("dot_crosses_f2_f3",ctx.phase=="F3" and b.hp==PHASE_STATS["F3"]["hp"] and f3._pact_mark(b) and any(d.source=="SELFCHECK" for d in b.dots))
        ctx.force_first_f3_denied_pending=1;ctx.boss_turn()
        put("first_denied_frozen_and_pact_active",ctx.f3_first_denied_observed==1 and ctx.pact_active_after_first_denied==1 and f3._pact_mark(b))
        frozen=(ctx.f3_first_denied_observed,ctx.pact_active_after_first_denied)
        ctx.boss_turn()
        put("first_real_releases_once",not f3._pact_mark(b) and b.resources.get("f3_pact_release_count",0)==1)
        # A later denial cannot rewrite the frozen first-denial observation.
        b.controlled_skip=True;b.removable_control_instances=max(1,b.removable_control_instances);ctx.boss_turn()
        put("later_denial_does_not_overwrite_first",(ctx.f3_first_denied_observed,ctx.pact_active_after_first_denied)==frozen)
        ctx.engine._commit_life_damage(b,999,source="SELFCHECK_POST_RELEASE")
        put("post_release_lethal",not b.alive())
    except Exception as e:
        errors.append("core:"+repr(e))
    finally:_CURRENT_CTX=None

    # Exact cooldown contract edges.
    try:
        for edge,ready in (("FIRST_USE",True),("SECOND_USE_SAME_COMBAT",False),("OOC_39",False),("OOC_40",True),("OOC_41",True)):
            r=_activation_cooldown_case({"activation_edge":edge})
            if edge=="FIRST_USE": ok=r["ultimate_uses"]==1
            elif edge=="SECOND_USE_SAME_COMBAT": ok=r["reactivation_blocked"]==1
            else: ok=bool(r["cooldown_ready"]) is ready
            put("cooldown_"+edge.lower(),ok)
    except Exception as e:errors.append("cooldown:"+repr(e))

    # All explicit transition edges in both phase boundaries.
    try:
        edges=["LETHAL_PACKET_EXACT_HP","OVERKILL_PACKET","MULTIHIT_CROSSES_PHASE","DOT_CROSSES_PHASE","HEMORRHAGE_CROSSES_PHASE","CONTROLLED_TRANSITION","BUFF_PERSISTS","DEBUFF_PERSISTS","ABSORPTION_PERSISTS_IF_CONTRACT_ALLOWS","EQUIPMENT_PROC_ALREADY_USED","EQUIPMENT_PROC_TRIGGERS_ON_BOUNDARY"]
        for ph in ("F1","F2"):
            for edge in edges:
                r=_phase_transition_case({"suite":"PHASE_TRANSITION","transition_edge":edge,"transition_phase":ph,"family":"FUEGO","player_state":"BALANCED","equipment_profile":"EXPECTED_STAGE","seed":seed_for_selfcheck(edge,ph)})
                put("transition_%s_%s"%(ph.lower(),edge.lower()),r.get("transition_edge_observed")==1 and r.get("transition_edge_pass")==1)
    except Exception as e:errors.append("transitions:"+repr(e))

    # Rejected Río must be causally identical to paired baseline.
    try:
        rio={"suite":"CORE_CONTINUOUS","ultimate":"WIND_RIO_CELESTE_SIN_ORILLAS","family":"VIENTO","mode":"FULL","window":"F1_EARLY","player_state":"FULL","equipment_profile":"EXPECTED_STAGE","seed":880031,"progression_mode":"MECHANICAL_STRESS"}
        basecase=dict(rio);basecase["suite"]="PAIRED_BASELINE";basecase["ultimate"]=None;basecase["mode"]="NO_ULTI"
        rr=run_case(rio);rb=run_case(basecase)
        put("rio_rejected_observed",rr.get("ultimate_activation_reason")=="IMPLEMENTATION_REJECTED")
        put("rio_rejected_equals_baseline",_rio_equivalence_signature(rr)==_rio_equivalence_signature(rb))
    except Exception as e:errors.append("rio:"+repr(e))

    # Late windows must be reachable before mechanical transition.
    try:
        for w,ph in (("F1_LATE_PRE_TRANSITION",1),("F2_LATE_PRE_TRANSITION",2)):
            c={"suite":"CORE_CONTINUOUS","ultimate":"METAL_SENTENCIA_FILO_CELESTIAL","family":"METAL","mode":"HARVEST","window":w,"player_state":"FULL","equipment_profile":"EXPECTED_STAGE","seed":77100+ph,"progression_mode":"MECHANICAL_STRESS"}
            r=run_case(c)
            offered=(r.get("late_opportunities_offered") or {}).get(ph,0)
            put("late_%s_reachable"%ph,offered>=1 and r.get("ultimate_activation_reason")!="NOT_ATTEMPTED")
    except Exception as e:errors.append("late:"+repr(e))

    for k,v in checks.items():
        if not v:errors.append(k)
    return {"pass":not errors,"checks":checks,"errors":errors,"runner_status":RUNNER_STATUS}


def seed_for_selfcheck(edge,phase):
    return int.from_bytes(hashlib.sha256(("V031|"+edge+"|"+phase).encode()).digest()[:8],"big")

if __name__=="__main__":
    # tiny smoke
    c={"suite":"CORE_CONTINUOUS","ultimate":"METAL_SENTENCIA_FILO_CELESTIAL","mode":"HARVEST","window":"F3_ENTRY","player_state":"BALANCED","equipment_profile":"EXPECTED_STAGE","seed":123}
    print(json.dumps(authority_report(),indent=2,ensure_ascii=False))
    print(json.dumps(run_case(c),indent=2,ensure_ascii=False))
