"""Instrumentación serial para ETAPA19B sin duplicar fórmulas de combate.

Este módulo envuelve temporalmente puntos del motor existente, llama SIEMPRE a
las funciones originales y agrega observabilidad. No modifica daño, hit, DEF,
DOT, Control, Qi ni orden de turnos.

La estrategia de monkey-patch es deliberadamente TEMPORAL para el smoke serial.
No debe usarse con threads. Antes de paralelizar Monte Carlo se migrarán estos
hooks al motor como callbacks explícitos o se usará aislamiento por procesos.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
import sys
from typing import Any

PARENT=Path(__file__).resolve().parent.parent
if str(PARENT) not in sys.path:
    sys.path.insert(0,str(PARENT))

import etapa19b_combat_engine as engine


@dataclass
class FightTelemetry:
    player_hp_start: float = 0.0
    player_hp_min: float = float("inf")
    player_hp_min_pct: float = 1.0
    player_basic_damage: float = 0.0
    player_skill_direct_damage: float = 0.0
    player_dot_damage: float = 0.0
    monster_basic_damage: float = 0.0
    monster_skill_direct_damage: float = 0.0
    monster_dot_damage: float = 0.0
    defensive_activations: int = 0
    potion_uses: int = 0
    potion_action_cost: int = 0
    monster_skill_uses: int = 0
    monster_basic_uses: int = 0
    monster_skipped_actions: int = 0
    forced_basic_due_to_qi: int = 0
    death_side: str | None = None
    death_cause: str | None = None
    death_round: int | None = None
    per_player_technique_usage: Counter = field(default_factory=Counter)
    per_monster_action_usage: Counter = field(default_factory=Counter)
    current_player_action: str | None = None
    current_monster_action: str | None = None

    def observe_player_hp(self,state) -> None:
        hp=max(0.0,float(state.player.hp))
        self.player_hp_min=min(self.player_hp_min,hp)
        if state.player.hp_max>0:
            self.player_hp_min_pct=min(
                self.player_hp_min_pct,
                hp/float(state.player.hp_max),
            )

    def mark_death(self,side: str,cause: str,state) -> None:
        if self.death_side is None:
            self.death_side=side
            self.death_cause=cause
            self.death_round=int(state.round_no)

    def as_dict(self) -> dict[str,Any]:
        hp_min=0.0 if self.player_hp_min==float("inf") else self.player_hp_min
        return {
            "player_hp_min":hp_min,
            "player_hp_min_pct":self.player_hp_min_pct,
            "player_basic_damage":self.player_basic_damage,
            "player_skill_direct_damage":self.player_skill_direct_damage,
            "player_dot_damage":self.player_dot_damage,
            "monster_basic_damage":self.monster_basic_damage,
            "monster_skill_direct_damage":self.monster_skill_direct_damage,
            "monster_dot_damage":self.monster_dot_damage,
            "defensive_activations":self.defensive_activations,
            "potion_uses":self.potion_uses,
            "potion_action_cost":self.potion_action_cost,
            "monster_skill_uses":self.monster_skill_uses,
            "monster_basic_uses":self.monster_basic_uses,
            "monster_skipped_actions":self.monster_skipped_actions,
            "forced_basic_due_to_qi":self.forced_basic_due_to_qi,
            "death_side":self.death_side,
            "death_cause":self.death_cause,
            "death_round":self.death_round,
            "per_player_technique_usage":dict(self.per_player_technique_usage),
            "per_monster_action_usage":dict(self.per_monster_action_usage),
        }


class _Instrument:
    """Context manager que restaura el motor incluso si la pelea falla."""

    def __init__(self):
        self.t=FightTelemetry()
        self.originals={}

    def _patch(self,name,fn):
        self.originals[name]=getattr(engine,name)
        setattr(engine,name,fn)

    def __enter__(self):
        original_build_player=engine.build_player
        original_resolve_player=engine.resolve_player_direct
        original_resolve_monster=engine.resolve_monster_direct
        original_tick_dots=engine._tick_dots
        original_activate_defense=engine.activate_defense
        original_execute_player=engine.execute_player_technique
        original_execute_basic=engine.execute_basic
        original_execute_monster=engine.execute_monster_turn

        def build_player(*args,**kwargs):
            actor,meta=original_build_player(*args,**kwargs)
            self.t.player_hp_start=float(actor.hp)
            self.t.player_hp_min=float(actor.hp)
            self.t.player_hp_min_pct=1.0
            return actor,meta

        def resolve_player_direct(state,rng,c,basic=False):
            out=original_resolve_player(state,rng,c,basic)
            damage=float(out.get("actual_hp_damage",0))
            if basic:
                self.t.player_basic_damage+=damage
            else:
                self.t.player_skill_direct_damage+=damage
            if state.monster.hp<=0:
                cause="PLAYER_BASIC" if basic else f"PLAYER_SKILL:{self.t.current_player_action or 'UNKNOWN'}"
                self.t.mark_death("MONSTER",cause,state)
            return out

        def resolve_monster_direct(state,rng,dice):
            out=original_resolve_monster(state,rng,dice)
            damage=float(out.get("actual_hp_damage",0))
            if self.t.current_monster_action=="TECHNIQUE":
                self.t.monster_skill_direct_damage+=damage
            else:
                self.t.monster_basic_damage+=damage
            self.t.observe_player_hp(state)
            if state.player.hp<=0:
                cause="MONSTER_SKILL_DIRECT" if self.t.current_monster_action=="TECHNIQUE" else "MONSTER_BASIC"
                self.t.mark_death("PLAYER",cause,state)
            return out

        def tick_dots(target,state,rng,target_is_player):
            before=float(target.hp)
            original_tick_dots(target,state,rng,target_is_player)
            dealt=max(0.0,before-float(target.hp))
            if target_is_player:
                self.t.monster_dot_damage+=dealt
                self.t.observe_player_hp(state)
                if state.player.hp<=0:
                    self.t.mark_death("PLAYER","MONSTER_DOT",state)
            else:
                self.t.player_dot_damage+=dealt
                if state.monster.hp<=0:
                    self.t.mark_death("MONSTER","PLAYER_DOT",state)

        def activate_defense(state,c):
            ok=original_activate_defense(state,c)
            if ok:
                self.t.defensive_activations+=1
                self.t.per_player_technique_usage[c["technique_id"]]+=1
            return ok

        def execute_player_technique(state,rng,c):
            prior=self.t.current_player_action
            self.t.current_player_action=c["technique_id"]
            if c["role"]!="DEFENSIVE":
                # Sólo contamos si el motor pudo pagar la técnica.
                before=float(state.player.qi)
                ok=original_execute_player(state,rng,c)
                if ok and float(state.player.qi)<before:
                    self.t.per_player_technique_usage[c["technique_id"]]+=1
            else:
                ok=original_execute_player(state,rng,c)
            self.t.current_player_action=prior
            self.t.observe_player_hp(state)
            return ok

        def execute_basic(state,rng):
            min_cost=min(
                (x["qi_cost"] for x in state.compiled.values() if x["role"]!="DEFENSIVE"),
                default=999,
            )
            if state.player.qi<min_cost:
                self.t.forced_basic_due_to_qi+=1
            return original_execute_basic(state,rng)

        def execute_monster_turn(state,rng):
            if state.monster.skip_next_action:
                self.t.monster_skipped_actions+=1
                self.t.per_monster_action_usage["SKIPPED"]+=1
                prior=self.t.current_monster_action
                self.t.current_monster_action="SKIPPED"
                try:
                    return original_execute_monster(state,rng)
                finally:
                    self.t.current_monster_action=prior

            tech=state.monster_profile.get("technique")
            params=(tech or {}).get("params") or {}
            due=bool(
                tech
                and params.get("cadence")
                and state.round_no%int(params["cadence"])==0
            )
            action="TECHNIQUE" if due else "BASIC"
            if due:
                self.t.monster_skill_uses+=1
            else:
                self.t.monster_basic_uses+=1
            self.t.per_monster_action_usage[action]+=1
            prior=self.t.current_monster_action
            self.t.current_monster_action=action
            try:
                return original_execute_monster(state,rng)
            finally:
                self.t.current_monster_action=prior

        self._patch("build_player",build_player)
        self._patch("resolve_player_direct",resolve_player_direct)
        self._patch("resolve_monster_direct",resolve_monster_direct)
        self._patch("_tick_dots",tick_dots)
        self._patch("activate_defense",activate_defense)
        self._patch("execute_player_technique",execute_player_technique)
        self._patch("execute_basic",execute_basic)
        self._patch("execute_monster_turn",execute_monster_turn)
        return self

    def __exit__(self,exc_type,exc,tb):
        for name,fn in self.originals.items():
            setattr(engine,name,fn)
        return False


def fight_once_observed(**kwargs) -> dict[str,Any]:
    """Ejecuta una pelea mediante ETAPA19B y añade telemetría sin cambiar resolución."""
    with _Instrument() as inst:
        result=engine.fight_once(**kwargs)
    t=inst.t.as_dict()
    metrics=result["metrics"]
    attempts=float(metrics.get("player_attempts",0))
    hits=float(metrics.get("player_hits",0))
    mattempts=float(metrics.get("monster_attempts",0))
    mhits=float(metrics.get("monster_hits",0))

    return {
        **result,
        "loss":bool((not result["win"]) and (not result["timeout"])),
        "player_qi_drained":float(metrics.get("qi_drained",0)),
        "player_hit_rate":hits/attempts if attempts else 0.0,
        "monster_hit_rate":mhits/mattempts if mattempts else 0.0,
        "player_crits":int(metrics.get("player_crits",0)),
        "monster_crits":int(metrics.get("monster_crits",0)),
        "control_attempts":int(metrics.get("control_attempts",0)),
        "control_successes":int(metrics.get("control_successes",0)),
        "defensive_procs":int(metrics.get("defense_procs",0)),
        **t,
    }
