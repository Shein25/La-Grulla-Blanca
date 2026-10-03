#!/usr/bin/env python3
"""
Grulla Blanca v2 — final boss LAB on top of ETAPA19B combat contract.

STATUS: LAB / PROVISIONAL / NO RUNTIME / NO MERGE.

This module deliberately imports the current new-contract combat engine and only
adds boss-specific orchestration required to test:
- three chained phases;
- boss penetration;
- mitigation independent from flat DEF;
- F3 capped absorption;
- healing / Qi-recovery suppression;
- reflection as an Arc-2 preview mechanic;
- old Grulla memory concepts (Silencio / Buscar Pulso / Romper Ritmo);
- consumable-aware veteran player policies.

Run from experimentos/balance_nuevo, or from repository root:
  python experimentos/balance_nuevo/grulla_v2_final_boss_lab.py --mode smoke --runs 200
  python experimentos/balance_nuevo/grulla_v2_final_boss_lab.py --mode matrix --runs 5000
  python experimentos/balance_nuevo/grulla_v2_final_boss_lab.py --mode sensitivity --runs 2000
  python experimentos/balance_nuevo/grulla_v2_final_boss_lab.py --mode trace --root metal --build pen_shred
"""

from __future__ import annotations

import argparse
import copy
import csv
import json
import math
import random
import statistics
from collections import Counter, deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import etapa19b_combat_engine as eng

HERE = Path(__file__).resolve().parent
CONFIG_PATH = HERE / "grulla_v2_lab_config.json"
TECHNIQUE_PATH = HERE / "techniques_arc1_catalog.json"
EQUIPMENT_PATH = HERE / "equipment_arc1_catalog.json"
RESULTS_DIR = HERE / "resultados_grulla_v2"

POLICIES = ("GREEDY", "VETERAN_BLIND", "MASTER_READER", "PREPARED_MASTER")


def load_config(path: Path = CONFIG_PATH) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def mean_dice(notation: str) -> float:
    # Reuse the engine parser behavior without consuming RNG.
    total = 0.0
    import re
    for token in re.findall(r"[+-]?[^+-]+", notation.replace(" ", "")):
        sign = -1 if token.startswith("-") else 1
        body = token[1:] if token[:1] in "+-" else token
        if "d" in body.lower():
            n_s, sides_s = body.lower().split("d", 1)
            n = int(n_s) if n_s else 1
            sides = int(sides_s)
            total += sign * n * (sides + 1) / 2
        else:
            total += sign * int(body)
    return total


@dataclass
class LabCounters:
    reflected_damage_to_player: float = 0.0
    healing_raw: float = 0.0
    healing_effective: float = 0.0
    qi_recovery_raw: float = 0.0
    qi_recovery_effective: float = 0.0
    potions_hp_used: int = 0
    potions_qi_used: int = 0
    heal_suppression_apps: int = 0
    qi_suppression_apps: int = 0
    boss_penetrating_hits: int = 0
    boss_mitigations: int = 0
    boss_reflect_stances: int = 0
    boss_reflect_triggers: int = 0
    boss_evasion_stances: int = 0
    boss_absorption_stances: int = 0
    control_degrades: int = 0
    damage_degrades: int = 0
    silencio_armed: int = 0
    silencio_broken: int = 0
    buscar_armed: int = 0
    buscar_broken: int = 0
    romper_casts: int = 0
    campana_casts: int = 0
    tormenta_casts: int = 0
    generic_defends: int = 0
    f3_shield_absorbed: float = 0.0
    f3_shield_break_round: int = 0
    last_breath_activated: int = 0


@dataclass
class GrullaLabState:
    config: dict
    phase: int = 1
    phase_round: int = 0
    total_round: int = 0
    forced_intent: str | None = None
    boss_evasion_bonus: float = 0.0
    boss_mitigation: float = 0.0
    reflect_active: bool = False
    heal_mult: float = 1.0
    heal_mult_turns: int = 0
    qi_recovery_mult: float = 1.0
    qi_recovery_mult_turns: int = 0
    generic_guard_pct: float = 0.0
    phase_absorption_cap: float = 0.0
    close_absorption_cap: float = 0.0
    last_breath_turns: int = 0
    plan_ref_technique: str | None = None
    plan_ref_element: str | None = None
    recent_boss_intents: deque = field(default_factory=lambda: deque(maxlen=4))
    player_history: deque = field(default_factory=lambda: deque(maxlen=8))
    phase_rounds: dict = field(default_factory=lambda: {1: 0, 2: 0, 3: 0})
    phase_entries: dict = field(default_factory=lambda: {1: True, 2: False, 3: False})
    phase_hp_start_player: dict = field(default_factory=dict)
    phase_qi_start_player: dict = field(default_factory=dict)
    counters: LabCounters = field(default_factory=LabCounters)
    trace: list[dict] = field(default_factory=list)

    def cfg_phase(self) -> dict:
        return self.config["phase_stats"][str(self.phase)]

    def ability(self, key: str) -> dict:
        return self.config["abilities"][key]


# ---------------------------------------------------------------------------
# Boss construction / phase lifecycle
# ---------------------------------------------------------------------------


def phase_actor(cfg: dict, phase: int) -> eng.Actor:
    p = cfg["phase_stats"][str(phase)]
    return eng.Actor(
        hp_max=float(p["hp"]), hp=float(p["hp"]),
        precision=float(p["precision"]), evasion=float(p["evasion"]),
        defense=float(p["defense"]), tenacity=float(p["tenacity"]),
        control=0.0, crit_chance=float(p["crit_chance"]),
        crit_damage=float(p.get("crit_damage", 1.5)),
    )


def enter_phase(lab: GrullaLabState, state: eng.FightState, phase: int) -> None:
    old_dots = list(state.monster.dots)
    old_effects = list(state.monster.stat_effects)
    p = lab.config["phase_stats"][str(phase)]
    state.monster.hp_max = float(p["hp"])
    state.monster.hp = float(p["hp"])
    state.monster.precision = float(p["precision"])
    state.monster.evasion = float(p["evasion"])
    state.monster.defense = float(p["defense"])
    state.monster.tenacity = float(p["tenacity"])
    state.monster.crit_chance = float(p["crit_chance"])
    state.monster.crit_damage = float(p.get("crit_damage", 1.5))
    state.monster.absorption = 0.0
    state.monster.absorption_max = 0.0
    state.monster.dots = old_dots              # same creature: DOTs persist
    state.monster.stat_effects = old_effects   # temporary shred/debuff may persist
    state.monster.skip_next_action = False

    lab.phase = phase
    lab.phase_round = 0
    lab.phase_entries[phase] = True
    lab.phase_hp_start_player[phase] = state.player.hp
    lab.phase_qi_start_player[phase] = state.player.qi
    lab.boss_evasion_bonus = 0.0
    lab.boss_mitigation = 0.0
    lab.reflect_active = False
    lab.close_absorption_cap = 0.0
    lab.forced_intent = None

    if phase == 3:
        reserve = float(p["initial_absorption"])
        state.monster.absorption = reserve
        state.monster.absorption_max = reserve
        lab.phase_absorption_cap = float(p["absorption_per_hit_cap"])
    else:
        lab.phase_absorption_cap = 0.0


def trigger_last_breath_if_needed(lab: GrullaLabState, state: eng.FightState, had_absorption: bool) -> None:
    if lab.phase != 3 or not had_absorption or state.monster.absorption > 0:
        return
    if lab.last_breath_turns > 0 or lab.counters.last_breath_activated:
        return
    p = lab.cfg_phase()
    lab.last_breath_turns = int(p["last_breath_rounds"])
    lab.counters.last_breath_activated = 1
    lab.counters.f3_shield_break_round = lab.phase_round


def boss_evasion(lab: GrullaLabState, state: eng.FightState) -> float:
    e = eng._monster_dynamic_evasion(state) + lab.boss_evasion_bonus
    if lab.phase == 3 and lab.last_breath_turns > 0:
        e += float(lab.cfg_phase()["last_breath_evasion"])
    return e


def boss_precision(lab: GrullaLabState, state: eng.FightState, bonus: float = 0.0) -> float:
    p = state.monster.effective("precision") + bonus
    if lab.phase == 3 and lab.last_breath_turns > 0:
        p += float(lab.cfg_phase()["last_breath_precision"])
    if state.arrastre_precision_debuff:
        p -= state.arrastre_precision_debuff
    return p


# ---------------------------------------------------------------------------
# Player -> Grulla resolution, preserving ETAPA19B rules plus LAB boss layers
# ---------------------------------------------------------------------------


def _boss_absorb_packet(lab: GrullaLabState, state: eng.FightState, amount: float) -> tuple[float, float]:
    if amount <= 0 or state.monster.absorption <= 0:
        return amount, 0.0
    cap = lab.phase_absorption_cap if lab.phase == 3 else lab.close_absorption_cap
    if cap <= 0:
        cap = state.monster.absorption
    used = min(float(amount), state.monster.absorption, cap)
    state.monster.absorption -= used
    state.metrics.monster_absorbed += used
    if lab.phase == 3:
        lab.counters.f3_shield_absorbed += used
    return amount - used, used


def resolve_player_direct_lab(lab: GrullaLabState, state: eng.FightState, rng: random.Random,
                              c: dict | None, basic: bool = False) -> dict:
    p, m, met = state.player, state.monster, state.metrics
    met.player_attempts += 1

    if basic:
        dice = state.player_basic_dice
        precision_mod = crit_pp = crit_add = pct_pen = flat_pen = 0.0
        direct_pct = p.direct_damage_pct
        aoe = 1.0
    else:
        dice = c["damage_dice"]
        precision_mod = c["precision_mod"]
        crit_pp = c["crit_pp"]
        crit_add = c["crit_damage_add"]
        pct_pen = c["percent_pen_pp"]
        flat_pen = c["flat_pen"]
        direct_pct = p.direct_damage_pct + p.technique_direct_damage_pct + c["direct_pct"]
        aoe = c["aoe_scalar"]
        if state.resonance and c["root"] == "tierra":
            precision_mod += state.resonance["precision"]
        if state.player_next_wind and c["root"] == "viento":
            precision_mod += state.player_next_wind["precision"]
            crit_pp += state.player_next_wind["crit_pp"]
        if c["technique_id"] == "golpe_montana":
            precision_mod += state.player_next_golpe_precision
        if c["technique_id"] == "latigazo_marea":
            precision_mod += state.next_latigazo_precision
        if c.get("max_peso_bonus_pct") and state.peso["stacks"] >= state.peso["max"]:
            direct_pct += c["max_peso_bonus_pct"]

    phit = eng.clamp(p.effective("precision") + precision_mod - boss_evasion(lab, state), 5, 100) / 100
    hit = rng.random() < phit
    if not hit:
        met.monster_evades += 1
        if not basic and c["root"] == "viento" and state.player_next_wind:
            state.player_next_wind = None
        if not basic and c["technique_id"] == "golpe_montana":
            state.player_next_golpe_precision = 0
        if not basic and c["technique_id"] == "latigazo_marea":
            state.next_latigazo_precision = 0
        return {"hit": False, "critical": False, "actual_hp_damage": 0.0, "absorbed": 0.0, "effective_def": None}

    met.player_hits += 1
    rolled = eng.roll_dice(rng, dice) + (p.basic_attack_flat if basic else 0)
    if not basic:
        rolled *= state.tech_scalar
    dmg = rolled * max(0.0, 1 + direct_pct / 100)

    crit = rng.random() < eng.clamp(p.crit_chance + crit_pp, 0, 100) / 100
    if crit:
        met.player_crits += 1
        cmult = max(0.0, p.crit_damage + crit_add)
        if lab.phase == 3:
            factor = float(lab.cfg_phase()["crit_bonus_received_factor"])
            cmult = 1 + (cmult - 1) * factor
        dmg *= cmult

    dmg *= aoe
    if lab.boss_mitigation > 0:
        dmg *= max(0.0, 1 - lab.boss_mitigation)
        lab.counters.boss_mitigations += 1

    real_def = max(0.0, eng._monster_dynamic_defense(state))
    pct = eng.clamp(p.percent_penetration + pct_pen, 0, 100)
    fp = max(0.0, p.flat_penetration + flat_pen)
    eff_def = max(0.0, real_def * (1 - pct / 100) - fp)
    after_decimal = max(0.0, dmg - eff_def)
    after = eng.round_half_up(after_decimal)
    met.monster_def_prevented += max(0.0, dmg - after_decimal)

    had_absorption = m.absorption > 0
    after, absorbed = _boss_absorb_packet(lab, state, float(after))
    actual = min(m.hp, float(after))
    m.hp -= actual
    met.player_damage_direct += actual
    trigger_last_breath_if_needed(lab, state, had_absorption)

    if not basic and c["root"] == "viento" and state.player_next_wind:
        state.player_next_wind = None
    if not basic and c["technique_id"] == "golpe_montana":
        state.player_next_golpe_precision = 0
    if not basic and c["technique_id"] == "latigazo_marea":
        state.next_latigazo_precision = 0

    return {
        "hit": True, "critical": crit, "actual_hp_damage": actual,
        "absorbed": absorbed, "damage_after_def": after, "effective_def": eff_def,
    }


def execute_player_technique_lab(lab: GrullaLabState, state: eng.FightState, rng: random.Random, c: dict) -> dict:
    if c["role"] == "DEFENSIVE":
        ok = eng.activate_defense(state, c)
        return {"ok": ok, "hit": False, "actual_hp_damage": 0.0, "kind": "DEFENSIVE"}

    if not eng._pay_qi(state, c["qi_cost"]):
        return {"ok": False, "hit": False, "actual_hp_damage": 0.0, "kind": "TECHNIQUE"}
    state.metrics.skill_usage[c["technique_id"]] += 1
    r = resolve_player_direct_lab(lab, state, rng, c, False)
    state.last_player_hp_damage_to_monster = r["actual_hp_damage"]

    # Cuerpo-Horno stored Heat follows current motor: separate direct packet,
    # normal DEF and absorption. It is not technique-rescaled again.
    if c["root"] == "fuego" and state.player_heat > 0:
        stored = state.player_heat
        state.player_heat = 0.0
        if r["hit"] and state.monster.alive():
            real_def = max(0.0, eng._monster_dynamic_defense(state))
            after = eng.round_half_up(max(0.0, stored - real_def))
            had_absorption = state.monster.absorption > 0
            after, _ = _boss_absorb_packet(lab, state, float(after))
            actual = min(state.monster.hp, float(after))
            state.monster.hp -= actual
            state.metrics.player_damage_direct += actual
            r["actual_hp_damage"] += actual
            trigger_last_breath_if_needed(lab, state, had_absorption)

    if not r["hit"] or not state.monster.alive():
        return {**r, "ok": True, "kind": "TECHNIQUE"}

    if c.get("dot"):
        eng._add_dot(state.monster, c["dot"], c["technique_id"])
    if c.get("debuff"):
        db = c["debuff"]
        eng._replace_effect(state.monster, db["stat"], db["amount"], db["turns"], f"{c['technique_id']}:{db['stat']}")
        if db.get("next_water_control"):
            state.next_water_control_bonus = max(state.next_water_control_bonus, db["next_water_control"])
    if c.get("control"):
        ctl = c["control"]
        if not (ctl["anti_lock"] and state.arrastre_locked):
            state.metrics.control_attempts += 1
            base = ctl["base"] + ctl["bonus"] + state.player.control + state.next_water_control_bonus
            state.next_water_control_bonus = 0
            if rng.random() < eng.clamp(base - state.monster.tenacity, 5, 100) / 100:
                state.metrics.control_successes += 1
                state.monster.skip_next_action = True
                state.arrastre_locked = True
                if ctl["precision_debuff_on_success"]:
                    state.arrastre_precision_debuff = ctl["precision_debuff_on_success"]
                if ctl["next_precision"]:
                    state.next_latigazo_precision = ctl["next_precision"]
    if c["model"] == "EARTH_OFFENSE":
        stab = c.get("self_stability", {})
        if stab.get("tenacity"):
            eng._replace_effect(state.player, "tenacity", stab["tenacity"], 1, "golpe:tenacity")
        if stab.get("defense"):
            eng._replace_effect(state.player, "defense", stab["defense"], 1, "golpe:defense")
        state.peso["per_stack"] = c["peso"]["evasion_per_stack"]
        state.peso["max"] = c["peso"]["max_stacks"]
        state.peso["stacks"] = min(state.peso["max"], state.peso["stacks"] + 1)
        state.peso["duration"] = c["peso"]["duration"]
        if state.resonance:
            if state.resonance.get("extra_peso_stack"):
                state.peso["stacks"] = min(state.peso["max"], state.peso["stacks"] + state.resonance["extra_peso_stack"])
            state.resonance = None
    if c.get("resonance"):
        state.resonance = dict(c["resonance"])

    return {**r, "ok": True, "kind": "TECHNIQUE"}


def execute_basic_lab(lab: GrullaLabState, state: eng.FightState, rng: random.Random) -> dict:
    state.metrics.basic_usage += 1
    r = resolve_player_direct_lab(lab, state, rng, None, True)
    state.last_player_hp_damage_to_monster = r["actual_hp_damage"]
    return {**r, "ok": True, "kind": "BASIC"}


# ---------------------------------------------------------------------------
# Boss -> player resolution with boss penetration and recovery debuffs
# ---------------------------------------------------------------------------


def resolve_boss_direct(lab: GrullaLabState, state: eng.FightState, rng: random.Random,
                        ability: dict, damage_mult: float = 1.0) -> dict:
    p, m, met = state.player, state.monster, state.metrics
    met.monster_attempts += 1
    precision = boss_precision(lab, state, float(ability.get("precision_bonus", 0)))
    peva = eng._player_dynamic_evasion(state)
    hit = rng.random() < eng.clamp(precision - peva, 5, 100) / 100
    if not hit:
        met.player_evades += 1
        ds = state.player_defense
        if ds and ds["kind"] == "WIND_STEP" and ds["response_count"] > 0 and not ds["response_created"]:
            state.player_next_wind = {"precision": ds["response_precision"], "crit_pp": ds["response_crit_pp"]}
            ds["response_created"] = True
            met.defense_procs += 1
        return {"hit": False, "actual_hp_damage": 0.0, "effective_def": None}

    met.monster_hits += 1
    dmg = eng.roll_dice(rng, ability["dice"]) * damage_mult
    crit = rng.random() < m.crit_chance / 100
    if crit:
        met.monster_crits += 1
        dmg *= m.crit_damage

    real_def = max(0.0, eng._player_dynamic_defense(state))
    pct = eng.clamp(float(ability.get("percent_penetration", 0)), 0, 100)
    flat = max(0.0, float(ability.get("flat_penetration", 0)))
    eff_def = max(0.0, real_def * (1 - pct / 100) - flat)
    if pct or flat:
        lab.counters.boss_penetrating_hits += 1
    after_decimal = max(0.0, dmg - eff_def)
    after = eng.round_half_up(after_decimal)
    met.player_def_prevented += max(0.0, dmg - after_decimal)

    # Generic DEFEND is a LAB bridge; technique defenses remain engine-native.
    if lab.generic_guard_pct > 0 and after > 0:
        after = eng.round_half_up(after * (1 - lab.generic_guard_pct))
        lab.generic_guard_pct = 0.0

    eng._post_player_hit_defense_consumption(state, after)
    after, absorbed = eng._absorb(p, float(after), met, True, state)
    actual = min(p.hp, float(after))
    p.hp -= actual
    met.monster_damage_direct += actual
    eng._maybe_trigger_gear_absorption(state)

    ds = state.player_defense
    if ds and ds["kind"] == "EARTH_SKIN" and actual > 0:
        gain = 1
        if not ds["large_hit_used"] and actual >= ds["large_hit_ratio"] * p.hp_max:
            gain = 2
            ds["large_hit_used"] = True
        old = ds["arraigo"]
        ds["arraigo"] = min(ds["max_arraigo"], old + gain)
        if ds["stratum_defense"] and ds["arraigo"] > old and ds["arraigo"] in (2, 3):
            ds["stratum"] = True
        if old < ds["max_arraigo"] and ds["arraigo"] == ds["max_arraigo"]:
            if not ds["max_extension_used"]:
                ds["turns_left"] += ds["reach_max_duration_extension"]
                ds["max_extension_used"] = True
            if not ds["reach_heal_used"] and ds["reach_max_heal_pct"] > 0:
                eng._heal_player(state, ds["reach_max_heal_pct"] * p.hp_max)
                ds["reach_heal_used"] = True
        if ds["low_hp_threshold"] and p.hp > 0 and p.hp / p.hp_max < ds["low_hp_threshold"] and not ds["low_heal_used"]:
            eng._heal_player(state, ds["low_hp_heal_pct"] * p.hp_max)
            ds["low_heal_used"] = True

    if actual > 0:
        if ability.get("qi_drain"):
            amt = min(p.qi, float(ability["qi_drain"]))
            p.qi -= amt
            met.qi_drained += amt
        turns = int(ability.get("debuff_turns", 0))
        if ability.get("heal_received_mult") is not None and turns > 0:
            lab.heal_mult = min(lab.heal_mult, float(ability["heal_received_mult"]))
            lab.heal_mult_turns = max(lab.heal_mult_turns, turns)
            lab.counters.heal_suppression_apps += 1
        if ability.get("qi_recovery_mult") is not None and turns > 0:
            lab.qi_recovery_mult = min(lab.qi_recovery_mult, float(ability["qi_recovery_mult"]))
            lab.qi_recovery_mult_turns = max(lab.qi_recovery_mult_turns, turns)
            lab.counters.qi_suppression_apps += 1

    return {"hit": True, "critical": crit, "actual_hp_damage": actual, "absorbed": absorbed, "effective_def": eff_def}


def apply_reflection(lab: GrullaLabState, state: eng.FightState, direct_hp_damage: float) -> float:
    if not lab.reflect_active or direct_hp_damage <= 0 or not state.player.alive():
        return 0.0
    cfg = lab.ability("ESPEJO_ROTO_F3")
    packet = min(float(cfg["reflect_cap"]), direct_hp_damage * float(cfg["reflect_ratio"]))
    if cfg.get("resolution") == "NORMAL_DIRECT":
        packet = float(eng.round_half_up(max(0.0, packet - eng._player_dynamic_defense(state))))
    # Baseline preview rule: post-resolution reflection does not recurse and
    # only meets absorption. It never triggers another reflection/retaliation.
    packet, _ = eng._absorb(state.player, packet, state.metrics, True, state)
    actual = min(state.player.hp, packet)
    state.player.hp -= actual
    lab.counters.reflected_damage_to_player += actual
    lab.counters.boss_reflect_triggers += 1
    eng._maybe_trigger_gear_absorption(state)
    return actual


# ---------------------------------------------------------------------------
# Consumables / player policy
# ---------------------------------------------------------------------------


def make_consumables(cfg: dict, profile: str) -> list[dict]:
    out = []
    for item in cfg["consumable_profiles"][profile]:
        x = dict(item)
        x["remaining"] = int(x.pop("count"))
        out.append(x)
    return out


def consumable_available(inv: list[dict], kind: str) -> dict | None:
    for x in inv:
        if x["kind"] == kind and x["remaining"] > 0:
            return x
    return None


def use_heal(lab: GrullaLabState, state: eng.FightState, rng: random.Random, item: dict) -> dict:
    raw = eng.roll_dice(rng, item["dice"])
    scaled = eng.round_half_up(raw * lab.heal_mult)
    actual = min(state.player.hp_max - state.player.hp, float(scaled))
    state.player.hp += actual
    item["remaining"] -= 1
    lab.counters.healing_raw += raw
    lab.counters.healing_effective += actual
    lab.counters.potions_hp_used += 1
    return {"kind": "HEAL", "item": item["id"], "raw": raw, "actual": actual, "qi_spent": 0.0, "damage": 0.0}


def use_qi(lab: GrullaLabState, state: eng.FightState, item: dict) -> dict:
    raw = float(item["amount"])
    scaled = eng.round_half_up(raw * lab.qi_recovery_mult)
    actual = min(state.player.qi_max - state.player.qi, float(scaled))
    state.player.qi += actual
    item["remaining"] -= 1
    state.metrics.qi_restored += actual
    lab.counters.qi_recovery_raw += raw
    lab.counters.qi_recovery_effective += actual
    lab.counters.potions_qi_used += 1
    return {"kind": "QI", "item": item["id"], "raw": raw, "actual": actual, "qi_spent": 0.0, "damage": 0.0}


def primary_offensive(state: eng.FightState) -> str:
    return eng.ROOT_TECHNIQUES[state.player_root][0]


def defensive_technique(state: eng.FightState) -> str:
    return eng.ROOT_TECHNIQUES[state.player_root][1]


def aoe_technique(state: eng.FightState) -> str:
    return eng.ROOT_TECHNIQUES[state.player_root][2]


def can_pay(state: eng.FightState, tid: str) -> bool:
    return tid in state.compiled and state.player.qi >= state.compiled[tid]["qi_cost"]


def last_history(lab: GrullaLabState) -> dict | None:
    return lab.player_history[-1] if lab.player_history else None


def choose_player_action(lab: GrullaLabState, state: eng.FightState, policy: str,
                         intent: str, inv: list[dict]) -> dict:
    off = primary_offensive(state)
    deff = defensive_technique(state)
    aoe = aoe_technique(state)
    hp_ratio = state.player.hp / state.player.hp_max
    qi_ratio = state.player.qi / state.player.qi_max if state.player.qi_max else 0
    heal = consumable_available(inv, "HEAL")
    qipot = consumable_available(inv, "QI")
    dangerous = intent in {"TORMENTA_F1", "TORMENTA_F2", "CAMPANA_F3", "ROMPER_F3"}
    avoid_burst = intent in {"PATA", "ALA", "RECORDAR", "ESPEJO_ROTO"}

    if policy == "GREEDY":
        if hp_ratio <= 0.22 and heal:
            return {"kind": "HEAL", "item": heal}
        return {"kind": "TECH", "tid": off} if can_pay(state, off) else {"kind": "BASIC"}

    # Consumables are evaluated against visible danger, not RNG future.
    heal_threshold = 0.42 if policy == "VETERAN_BLIND" else 0.50
    if heal and hp_ratio <= heal_threshold and not dangerous:
        missing = state.player.hp_max - state.player.hp
        expected = mean_dice(heal["dice"]) * lab.heal_mult
        if missing >= expected * 0.65:
            return {"kind": "HEAL", "item": heal}

    if qipot and qi_ratio <= (0.18 if policy == "VETERAN_BLIND" else 0.28) and not dangerous:
        if lab.qi_recovery_mult >= 0.75 or state.player.qi < state.compiled[off]["qi_cost"]:
            return {"kind": "QI", "item": qipot}

    if dangerous:
        if can_pay(state, deff) and policy in {"MASTER_READER", "PREPARED_MASTER"}:
            return {"kind": "TECH", "tid": deff}
        return {"kind": "DEFEND"}

    if policy in {"MASTER_READER", "PREPARED_MASTER"}:
        if intent == "BUSCAR":
            return {"kind": "BASIC"}
        if intent == "SILENCIO":
            last = last_history(lab)
            if last and last.get("technique_id") == off:
                return {"kind": "BASIC"}
            return {"kind": "TECH", "tid": off} if can_pay(state, off) else {"kind": "BASIC"}
        if avoid_burst:
            if heal and hp_ratio <= 0.72:
                return {"kind": "HEAL", "item": heal}
            if qipot and qi_ratio <= 0.55 and lab.qi_recovery_mult >= 0.75:
                return {"kind": "QI", "item": qipot}
            if can_pay(state, deff) and state.player_defense is None:
                return {"kind": "TECH", "tid": deff}
            return {"kind": "BASIC"}

        # Metal veteran intentionally opens a window with Lluvia de Filos when
        # its build contains Rupture and no active DEF shred exists.
        if state.player_root == "metal" and aoe in state.compiled:
            c = state.compiled[aoe]
            if c.get("debuff") and c["debuff"].get("stat") == "defense" and state.monster.effect_sum("defense") >= 0 and can_pay(state, aoe):
                return {"kind": "TECH", "tid": aoe}

    if can_pay(state, off):
        return {"kind": "TECH", "tid": off}
    if qipot and lab.qi_recovery_mult >= 0.50:
        return {"kind": "QI", "item": qipot}
    return {"kind": "BASIC"}


def execute_player_action(lab: GrullaLabState, state: eng.FightState, rng: random.Random,
                          action: dict) -> dict:
    q0 = state.player.qi
    if action["kind"] == "HEAL":
        out = use_heal(lab, state, rng, action["item"])
    elif action["kind"] == "QI":
        out = use_qi(lab, state, action["item"])
    elif action["kind"] == "DEFEND":
        lab.generic_guard_pct = float(lab.config["lab_bridges"]["generic_defend_mitigation"])
        lab.counters.generic_defends += 1
        out = {"kind": "DEFEND", "damage": 0.0, "qi_spent": 0.0}
    elif action["kind"] == "TECH":
        c = state.compiled[action["tid"]]
        r = execute_player_technique_lab(lab, state, rng, c)
        out = {"kind": "TECH", "technique_id": action["tid"], "element": c["root"],
               "damage": float(r.get("actual_hp_damage", 0.0)), "qi_spent": q0 - state.player.qi,
               "hit": bool(r.get("hit", False)), "critical": bool(r.get("critical", False))}
    else:
        r = execute_basic_lab(lab, state, rng)
        out = {"kind": "BASIC", "damage": float(r.get("actual_hp_damage", 0.0)), "qi_spent": 0.0,
               "hit": bool(r.get("hit", False)), "critical": bool(r.get("critical", False))}

    if out.get("damage", 0) >= float(lab.config["lab_bridges"]["heavy_hit_ratio"]) * state.monster.hp_max:
        out["damage_band"] = "HEAVY"
    elif out.get("damage", 0) > 0:
        out["damage_band"] = "NORMAL"
    else:
        out["damage_band"] = "NONE"
    return out


# ---------------------------------------------------------------------------
# Grulla intent selection and resolution
# ---------------------------------------------------------------------------


def repeated_technique(lab: GrullaLabState) -> bool:
    xs = [x.get("technique_id") for x in list(lab.player_history)[-2:]]
    return len(xs) == 2 and xs[0] is not None and xs[0] == xs[1]


def repeated_element(lab: GrullaLabState) -> bool:
    xs = [x.get("element") for x in list(lab.player_history)[-2:]]
    return len(xs) == 2 and xs[0] is not None and xs[0] == xs[1]


def qi_streak(lab: GrullaLabState) -> bool:
    xs = list(lab.player_history)[-2:]
    return len(xs) == 2 and all(float(x.get("qi_spent", 0)) > 0 for x in xs)


def offense_streak(lab: GrullaLabState) -> bool:
    xs = list(lab.player_history)[-2:]
    return len(xs) == 2 and all(x.get("kind") in {"TECH", "BASIC"} and float(x.get("damage", 0)) > 0 for x in xs)


def intent_recent(lab: GrullaLabState, intent: str, depth: int = 2) -> bool:
    return intent in list(lab.recent_boss_intents)[-depth:]


def pick_max_score(rng: random.Random, scores: dict[str, float], jitter: float = 0.8) -> str:
    best = None
    bestv = -1e18
    for k, v in scores.items():
        x = v + (rng.random() * 2 - 1) * jitter
        if x > bestv:
            bestv, best = x, k
    assert best is not None
    return best


def choose_boss_intent(lab: GrullaLabState, state: eng.FightState, rng: random.Random) -> str:
    if lab.forced_intent:
        x = lab.forced_intent
        lab.forced_intent = None
        return x

    php = state.player.hp / state.player.hp_max
    pqi = state.player.qi / state.player.qi_max if state.player.qi_max else 0
    bhp = state.monster.hp / state.monster.hp_max
    heavy = any(x.get("damage_band") == "HEAVY" for x in list(lab.player_history)[-2:])

    if lab.phase == 1:
        scores = {
            "GOLPE_F1": 30,
            "TORMENTA_F1": 24 + (8 if php <= 0.45 else 0) - (24 if intent_recent(lab, "TORMENTA_F1") else 0),
            "PATA": 16 + (16 if heavy else 0) - (20 if intent_recent(lab, "PATA") else 0),
            "ALA": 14 + (15 if offense_streak(lab) else 0) - (20 if intent_recent(lab, "ALA") else 0),
        }
    elif lab.phase == 2:
        scores = {
            "GOLPE_F2": 26,
            "TORMENTA_F2": 27 + (12 if php <= 0.45 else 0) + (6 if pqi >= 0.60 else 0) - (30 if intent_recent(lab, "TORMENTA_F2") else 0),
            "CERRAR": 16 + (18 if heavy else 0) + (10 if bhp <= 0.35 else 0) - (30 if intent_recent(lab, "CERRAR") else 0),
            "RECORDAR": 12 + (34 if repeated_technique(lab) else 0) + (14 if repeated_element(lab) else 0) - (36 if intent_recent(lab, "RECORDAR") else 0),
            "ECO": 12 + (32 if qi_streak(lab) else 0) + (8 if pqi <= 0.25 else 0) - (30 if intent_recent(lab, "ECO") else 0),
            "PATA": 14 + (14 if heavy else 0) - (24 if intent_recent(lab, "PATA") else 0),
        }
    else:
        scores = {
            "PICOTAZO_F3": 25 + (8 if php <= 0.30 else 0),
            "CAMPANA_F3": 25 + (18 if php <= 0.40 else 0) + (8 if pqi >= 0.55 else 0) - (38 if intent_recent(lab, "CAMPANA_F3") else 0),
            "ALA": 16 + (17 if offense_streak(lab) else 0) + (10 if heavy else 0) - (28 if intent_recent(lab, "ALA") else 0),
            "PATA": 16 + (18 if heavy else 0) - (28 if intent_recent(lab, "PATA") else 0),
            "SILENCIO": 10 + (34 if repeated_technique(lab) else 0) + (16 if repeated_element(lab) else 0) - (45 if intent_recent(lab, "SILENCIO", 3) else 0),
            "BUSCAR": 10 + (30 if qi_streak(lab) else 0) + (8 if pqi >= 0.55 else 0) - (45 if intent_recent(lab, "BUSCAR", 3) else 0),
            "ESPEJO_ROTO": 14 + (22 if heavy else 0) + (8 if bhp <= 0.50 else 0) - (35 if intent_recent(lab, "ESPEJO_ROTO") else 0),
        }
        if lab.last_breath_turns > 0:
            scores["PICOTAZO_F3"] += 8
            scores["CAMPANA_F3"] += 10
            scores["PATA"] -= 8
            scores["ALA"] -= 6
            scores["ESPEJO_ROTO"] -= 5
    return pick_max_score(rng, scores)


def pre_player_intent(lab: GrullaLabState, state: eng.FightState, intent: str) -> None:
    lab.boss_evasion_bonus = 0.0
    lab.boss_mitigation = 0.0
    lab.reflect_active = False
    lab.generic_guard_pct = 0.0

    if intent == "PATA":
        lab.boss_mitigation = float(lab.ability("PATA_MITIGATION")[str(lab.phase)])
    elif intent == "ALA":
        lab.boss_evasion_bonus = float(lab.ability("ALA_EVASION")[str(lab.phase)])
        lab.counters.boss_evasion_stances += 1
    elif intent == "RECORDAR":
        lab.boss_evasion_bonus = float(lab.ability("RECORDAR_F2")["evasion_bonus"])
        lab.counters.boss_evasion_stances += 1
    elif intent == "CERRAR":
        c = lab.ability("CERRAR_F2")
        state.monster.absorption = max(state.monster.absorption, float(c["reserve"]))
        state.monster.absorption_max = max(state.monster.absorption_max, state.monster.absorption)
        lab.close_absorption_cap = float(c["per_hit_cap"])
        lab.counters.boss_absorption_stances += 1
    elif intent == "ESPEJO_ROTO":
        lab.reflect_active = True
        lab.counters.boss_reflect_stances += 1
    elif intent == "SILENCIO":
        last = last_history(lab)
        lab.plan_ref_technique = last.get("technique_id") if last else None
        lab.plan_ref_element = last.get("element") if last else None
    elif intent == "BUSCAR":
        lab.plan_ref_technique = None
        lab.plan_ref_element = None


def post_player_intent(lab: GrullaLabState, state: eng.FightState, rng: random.Random,
                       intent: str, action_record: dict) -> dict | None:
    # Reflection resolves even if the direct hit has just reduced F3 to zero.
    if intent == "ESPEJO_ROTO":
        apply_reflection(lab, state, float(action_record.get("damage", 0.0)))

    if not state.player.alive() or not state.monster.alive():
        return None

    control_success = bool(state.monster.skip_next_action)
    if control_success:
        state.monster.skip_next_action = False

    if intent in {"GOLPE_F1", "TORMENTA_F1", "GOLPE_F2", "TORMENTA_F2", "PICOTAZO_F3", "CAMPANA_F3", "ROMPER_F3"}:
        mult = 1.0
        if control_success:
            mult = min(mult, float(lab.config["lab_bridges"]["telegraph_control_degrade_mult"]))
            lab.counters.control_degrades += 1
        threshold = None
        if intent == "TORMENTA_F2":
            threshold = float(lab.config["lab_bridges"]["telegraph_break_damage_f2"])
        elif intent in {"CAMPANA_F3", "ROMPER_F3"}:
            threshold = float(lab.config["lab_bridges"]["telegraph_break_damage_f3"])
        if threshold is not None and float(action_record.get("damage", 0.0)) >= threshold:
            mult = min(mult, float(lab.config["lab_bridges"]["telegraph_break_damage_mult"]))
            lab.counters.damage_degrades += 1
        if intent.startswith("TORMENTA"):
            lab.counters.tormenta_casts += 1
        if intent == "CAMPANA_F3":
            lab.counters.campana_casts += 1
        if intent == "ROMPER_F3":
            lab.counters.romper_casts += 1
        return resolve_boss_direct(lab, state, rng, lab.ability(intent), mult)

    if intent == "ECO":
        if float(action_record.get("qi_spent", 0)) > 0:
            c = lab.ability("ECO_F2")
            amt = min(state.player.qi, float(c["qi_drain"]))
            state.player.qi -= amt
            state.metrics.qi_drained += amt
            lab.qi_recovery_mult = min(lab.qi_recovery_mult, float(c["qi_recovery_mult"]))
            lab.qi_recovery_mult_turns = max(lab.qi_recovery_mult_turns, int(c["debuff_turns"]))
            lab.counters.qi_suppression_apps += 1
        return None

    if intent == "SILENCIO":
        same_tech = lab.plan_ref_technique is not None and action_record.get("technique_id") == lab.plan_ref_technique
        same_elem = lab.plan_ref_element is not None and action_record.get("element") == lab.plan_ref_element and action_record.get("kind") == "TECH"
        if same_tech or same_elem:
            lab.forced_intent = "ROMPER_F3"
            lab.counters.silencio_armed += 1
        else:
            lab.counters.silencio_broken += 1
        return None

    if intent == "BUSCAR":
        if float(action_record.get("qi_spent", 0)) > 0:
            lab.forced_intent = "CAMPANA_F3"
            lab.counters.buscar_armed += 1
        else:
            lab.counters.buscar_broken += 1
        return None

    return None


# ---------------------------------------------------------------------------
# Fight / Monte Carlo
# ---------------------------------------------------------------------------


def tick_recovery_debuffs_after_player_action(lab: GrullaLabState) -> None:
    if lab.heal_mult_turns > 0:
        lab.heal_mult_turns -= 1
        if lab.heal_mult_turns <= 0:
            lab.heal_mult = 1.0
    if lab.qi_recovery_mult_turns > 0:
        lab.qi_recovery_mult_turns -= 1
        if lab.qi_recovery_mult_turns <= 0:
            lab.qi_recovery_mult = 1.0


def build_fight(cfg: dict, root: str, build_name: str, loadout_name: str) -> tuple[eng.FightState, GrullaLabState]:
    tech_catalog = eng.load_json(TECHNIQUE_PATH)
    eq_catalog = eng.load_json(EQUIPMENT_PATH)
    player, meta = eng.build_player(cfg["stage"], root, cfg["equipment_loadouts"][loadout_name], eq_catalog)
    paths = cfg["builds"][root][build_name]
    compiled = eng.compile_build(root, paths, tech_catalog)
    boss = phase_actor(cfg, 1)
    profile_stub = {
        "monster_id": "grulla_blanca_v2_lab",
        "new_contract_lab": {"hp": 150, "precision": 90, "evasion": 55, "defense": 12, "tenacity": 40, "control": 0,
                             "crit_chance": 5, "crit_damage": 1.5, "damage": "1d1", "technique": None},
        "adaptive_c_staggered": {"T0": {"hp_mult": 1, "damage_mult": 1, "precision_bonus": 0, "evasion_bonus": 0, "crit_chance": 5}},
        "ai": {},
    }
    state = eng.FightState(
        player=player, monster=boss, player_root=root, stage=cfg["stage"], tier="T0",
        player_basic_dice=eng.STAGES[cfg["stage"]]["basic_attack"],
        tech_scalar=eng.STAGES[cfg["stage"]]["tech_scalar"], compiled=compiled,
        monster_profile=profile_stub,
        signal_bridge=eng.LabSignalBridge(
            low_hp_ratio=float(cfg["lab_bridges"]["low_hp_ratio"]),
            heavy_hit_ratio=float(cfg["lab_bridges"]["heavy_hit_ratio"]),
        ),
        equipment_effects=meta["equipment_effects"],
    )
    lab = GrullaLabState(config=cfg)
    lab.phase_hp_start_player[1] = player.hp
    lab.phase_qi_start_player[1] = player.qi
    return state, lab


def fight_once(cfg: dict, *, root: str, build_name: str, loadout: str, consumables: str,
               policy: str, seed: int, max_rounds: int = 120, trace: bool = False) -> dict:
    state, lab = build_fight(cfg, root, build_name, loadout)
    inv = make_consumables(cfg, consumables)
    rng = random.Random(seed)
    win = False
    double_ko = False

    while state.player.alive() and lab.total_round < max_rounds:
        if lab.phase > 3:
            win = True
            break

        lab.total_round += 1
        lab.phase_round += 1
        lab.phase_rounds[lab.phase] += 1
        state.round_no += 1

        eng.player_turn_start(state, rng)
        if not state.player.alive():
            break

        intent = choose_boss_intent(lab, state, rng)
        pre_player_intent(lab, state, intent)
        boss_hp_before = state.monster.hp
        boss_abs_before = state.monster.absorption
        player_hp_before = state.player.hp
        player_qi_before = state.player.qi

        action = choose_player_action(lab, state, policy, intent, inv)
        rec = execute_player_action(lab, state, rng, action)
        rec.setdefault("technique_id", None)
        rec.setdefault("element", None)
        rec["phase"] = lab.phase
        rec["intent"] = intent

        # Debuff durations are measured in player actions. Effects applied by
        # the boss later in this round therefore begin ticking next action.
        tick_recovery_debuffs_after_player_action(lab)
        post_player_intent(lab, state, rng, intent, rec)

        # Player history observes resolved action only, as in the closed Grulla lab.
        lab.player_history.append(dict(rec))
        lab.recent_boss_intents.append(intent)

        # DOT on Grulla resolves at its turn start and still respects absorption.
        if state.player.alive() and state.monster.alive():
            had_abs = state.monster.absorption > 0
            eng.monster_turn_start(state, rng)
            trigger_last_breath_if_needed(lab, state, had_abs)

        if trace:
            lab.trace.append({
                "round": lab.total_round, "phase": lab.phase, "phase_round": lab.phase_round,
                "intent": intent, "player_action": rec,
                "player_hp_before": player_hp_before, "player_hp_after": state.player.hp,
                "player_qi_before": player_qi_before, "player_qi_after": state.player.qi,
                "boss_hp_before": boss_hp_before, "boss_hp_after": state.monster.hp,
                "boss_abs_before": boss_abs_before, "boss_abs_after": state.monster.absorption,
                "heal_mult": lab.heal_mult, "qi_recovery_mult": lab.qi_recovery_mult,
                "last_breath_turns": lab.last_breath_turns,
            })

        if state.player.hp <= 0 and state.monster.hp <= 0:
            double_ko = True
            break
        if state.player.hp <= 0:
            break

        if state.monster.hp <= 0:
            if lab.phase == 3:
                lab.phase = 4
                win = True
                break
            enter_phase(lab, state, lab.phase + 1)
            continue

        # A normal boss resolution releases Water anti-lock after one action window.
        if state.arrastre_locked:
            state.arrastre_locked = False
            state.arrastre_precision_debuff = 0.0

        eng.end_round(state)
        lab.boss_evasion_bonus = 0.0
        lab.boss_mitigation = 0.0
        lab.reflect_active = False
        lab.close_absorption_cap = lab.close_absorption_cap if state.monster.absorption > 0 else 0.0
        if lab.last_breath_turns > 0:
            lab.last_breath_turns -= 1

    c = lab.counters
    return {
        "win": bool(win and state.player.hp > 0),
        "double_ko": double_ko,
        "timeout": lab.total_round >= max_rounds and state.player.alive() and lab.phase <= 3,
        "root": root, "build": build_name, "loadout": loadout, "consumables": consumables, "policy": policy,
        "rounds": lab.total_round,
        "phase1_rounds": lab.phase_rounds[1], "phase2_rounds": lab.phase_rounds[2], "phase3_rounds": lab.phase_rounds[3],
        "reached_phase2": lab.phase_entries[2], "reached_phase3": lab.phase_entries[3],
        "player_hp_final": max(0.0, state.player.hp), "player_hp_max": state.player.hp_max,
        "player_qi_final": max(0.0, state.player.qi), "player_qi_max": state.player.qi_max,
        "player_damage_direct": state.metrics.player_damage_direct,
        "player_damage_dot": state.metrics.player_damage_dot,
        "boss_damage_direct": state.metrics.monster_damage_direct,
        "player_def_prevented": state.metrics.player_def_prevented,
        "boss_def_prevented": state.metrics.monster_def_prevented,
        "player_absorbed": state.metrics.player_absorbed,
        "boss_absorbed": state.metrics.monster_absorbed,
        "player_hit_rate_num": state.metrics.player_hits, "player_hit_rate_den": state.metrics.player_attempts,
        "boss_hit_rate_num": state.metrics.monster_hits, "boss_hit_rate_den": state.metrics.monster_attempts,
        "control_successes": state.metrics.control_successes, "control_attempts": state.metrics.control_attempts,
        "qi_spent": state.metrics.qi_spent, "qi_drained": state.metrics.qi_drained, "qi_restored": state.metrics.qi_restored,
        **vars(c),
        "trace": lab.trace if trace else None,
    }


def summarize(rows: list[dict]) -> dict:
    n = len(rows)
    reached3 = [r for r in rows if r["reached_phase3"]]
    wins = [r for r in rows if r["win"]]
    p_attempts = sum(r["player_hit_rate_den"] for r in rows)
    p_hits = sum(r["player_hit_rate_num"] for r in rows)
    b_attempts = sum(r["boss_hit_rate_den"] for r in rows)
    b_hits = sum(r["boss_hit_rate_num"] for r in rows)
    ctr_attempts = sum(r["control_attempts"] for r in rows)
    ctr_success = sum(r["control_successes"] for r in rows)
    return {
        "iterations": n,
        "win_rate": sum(r["win"] for r in rows) / n,
        "double_ko_rate": sum(r["double_ko"] for r in rows) / n,
        "timeout_rate": sum(r["timeout"] for r in rows) / n,
        "reach_phase3_rate": len(reached3) / n,
        "mean_rounds": statistics.fmean(r["rounds"] for r in rows),
        "mean_phase1_rounds": statistics.fmean(r["phase1_rounds"] for r in rows),
        "mean_phase2_rounds": statistics.fmean(r["phase2_rounds"] for r in rows),
        "mean_phase3_rounds_all": statistics.fmean(r["phase3_rounds"] for r in rows),
        "mean_phase3_rounds_if_reached": statistics.fmean(r["phase3_rounds"] for r in reached3) if reached3 else 0.0,
        "mean_phase3_rounds_on_win": statistics.fmean(r["phase3_rounds"] for r in wins) if wins else 0.0,
        "mean_player_hp_final_pct": statistics.fmean(r["player_hp_final"] / r["player_hp_max"] for r in rows),
        "mean_player_qi_final": statistics.fmean(r["player_qi_final"] for r in rows),
        "player_hit_rate": p_hits / p_attempts if p_attempts else 0.0,
        "boss_hit_rate": b_hits / b_attempts if b_attempts else 0.0,
        "control_success_rate": ctr_success / ctr_attempts if ctr_attempts else 0.0,
        "mean_reflected_damage": statistics.fmean(r["reflected_damage_to_player"] for r in rows),
        "mean_healing_effective": statistics.fmean(r["healing_effective"] for r in rows),
        "mean_qi_recovery_effective": statistics.fmean(r["qi_recovery_effective"] for r in rows),
        "mean_hp_potions": statistics.fmean(r["potions_hp_used"] for r in rows),
        "mean_qi_potions": statistics.fmean(r["potions_qi_used"] for r in rows),
        "mean_f3_shield_absorbed": statistics.fmean(r["f3_shield_absorbed"] for r in reached3) if reached3 else 0.0,
        "mean_boss_penetrating_hits": statistics.fmean(r["boss_penetrating_hits"] for r in rows),
        "mean_romper_casts": statistics.fmean(r["romper_casts"] for r in rows),
        "mean_campana_casts": statistics.fmean(r["campana_casts"] for r in rows),
        "mean_tormenta_casts": statistics.fmean(r["tormenta_casts"] for r in rows),
    }


def scenario_rows(cfg: dict, runs: int, *, root: str, build: str, loadout: str,
                  consumables: str, policy: str, seed: int) -> tuple[list[dict], dict]:
    rows = [fight_once(cfg, root=root, build_name=build, loadout=loadout, consumables=consumables,
                       policy=policy, seed=seed + i * 1009) for i in range(runs)]
    s = summarize(rows)
    s.update(root=root, build=build, loadout=loadout, consumables=consumables, policy=policy)
    return rows, s


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    keys = [k for k in rows[0].keys() if k != "trace"]
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for row in rows:
            w.writerow({k: row.get(k) for k in keys})


def run_matrix(cfg: dict, runs: int, seed: int, smoke: bool = False) -> list[dict]:
    scenarios = [
        ("VETERAN_BLIND", "guaranteed", "standard"),
        ("MASTER_READER", "veteran_balanced", "standard"),
        ("PREPARED_MASTER", "veteran_balanced", "prepared"),
        ("PREPARED_MASTER", "MAX_AUTO", "max_reasonable"),
    ]
    summaries = []
    all_rows = []
    local_runs = min(runs, 200) if smoke else runs
    for root, builds in cfg["builds"].items():
        for build in builds:
            for policy, loadout, consumables in scenarios:
                actual_loadout = "max_penetration" if loadout == "MAX_AUTO" and root == "metal" else ("veteran_balanced" if loadout == "MAX_AUTO" else loadout)
                rows, s = scenario_rows(cfg, local_runs, root=root, build=build, loadout=actual_loadout,
                                        consumables=consumables, policy=policy,
                                        seed=seed + len(summaries) * 1000003)
                summaries.append(s)
                all_rows.extend(rows)
                print(json.dumps(s, ensure_ascii=False))
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(RESULTS_DIR / ("grulla_v2_smoke_raw.csv" if smoke else "grulla_v2_matrix_raw.csv"), all_rows)
    write_csv(RESULTS_DIR / ("grulla_v2_smoke_summary.csv" if smoke else "grulla_v2_matrix_summary.csv"), summaries)
    return summaries


def run_sensitivity(cfg: dict, runs: int, seed: int) -> list[dict]:
    # One-factor-at-a-time around the baseline to preserve interpretability.
    cases: list[tuple[str, dict]] = [("baseline", copy.deepcopy(cfg))]
    for triplet in cfg["sensitivity"]["defense_triplets"]:
        c = copy.deepcopy(cfg)
        for i, v in enumerate(triplet, 1):
            c["phase_stats"][str(i)]["defense"] = v
        cases.append((f"def_{triplet[0]}_{triplet[1]}_{triplet[2]}", c))
    for v in cfg["sensitivity"]["f3_absorption"]:
        c = copy.deepcopy(cfg); c["phase_stats"]["3"]["initial_absorption"] = v
        cases.append((f"f3abs_{v}", c))
    for v in cfg["sensitivity"]["f3_absorption_cap"]:
        c = copy.deepcopy(cfg); c["phase_stats"]["3"]["absorption_per_hit_cap"] = v
        cases.append((f"f3cap_{v}", c))
    for v in cfg["sensitivity"]["f3_pata_mitigation"]:
        c = copy.deepcopy(cfg); c["abilities"]["PATA_MITIGATION"]["3"] = v
        cases.append((f"pata3_{v}", c))
    for v in cfg["sensitivity"]["reflect_ratio"]:
        c = copy.deepcopy(cfg); c["abilities"]["ESPEJO_ROTO_F3"]["reflect_ratio"] = v
        cases.append((f"reflect_{v}", c))
    for v in cfg["sensitivity"]["campana_heal_mult"]:
        c = copy.deepcopy(cfg); c["abilities"]["CAMPANA_F3"]["heal_received_mult"] = v
        cases.append((f"campana_heal_{v}", c))

    summaries = []
    for case_idx, (case, ccfg) in enumerate(cases):
        for root, builds in ccfg["builds"].items():
            # First build is the root's representative veteran build for OFAT.
            build = next(iter(builds))
            loadout = "max_penetration" if root == "metal" else "veteran_balanced"
            _, s = scenario_rows(ccfg, runs, root=root, build=build, loadout=loadout,
                                 consumables="prepared", policy="PREPARED_MASTER",
                                 seed=seed + case_idx * 10000019 + list(ccfg["builds"]).index(root) * 100003)
            s["case"] = case
            summaries.append(s)
            print(json.dumps(s, ensure_ascii=False))
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(RESULTS_DIR / "grulla_v2_sensitivity_summary.csv", summaries)
    return summaries


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=("smoke", "matrix", "sensitivity", "trace"), default="smoke")
    ap.add_argument("--runs", type=int, default=1000)
    ap.add_argument("--seed", type=int, default=20260930)
    ap.add_argument("--root", choices=tuple(eng.ROOT_TECHNIQUES), default="metal")
    ap.add_argument("--build", default=None)
    ap.add_argument("--loadout", default="max_penetration")
    ap.add_argument("--consumables", default="prepared")
    ap.add_argument("--policy", choices=POLICIES, default="PREPARED_MASTER")
    args = ap.parse_args()

    cfg = load_config()
    if args.mode == "smoke":
        run_matrix(cfg, args.runs, args.seed, smoke=True)
    elif args.mode == "matrix":
        run_matrix(cfg, args.runs, args.seed, smoke=False)
    elif args.mode == "sensitivity":
        run_sensitivity(cfg, args.runs, args.seed)
    else:
        build = args.build or next(iter(cfg["builds"][args.root]))
        row = fight_once(cfg, root=args.root, build_name=build, loadout=args.loadout,
                         consumables=args.consumables, policy=args.policy, seed=args.seed, trace=True)
        RESULTS_DIR.mkdir(parents=True, exist_ok=True)
        path = RESULTS_DIR / f"trace_{args.root}_{build}_{args.seed}.json"
        path.write_text(json.dumps(row, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps({k: v for k, v in row.items() if k != "trace"}, ensure_ascii=False, indent=2))
        print(f"TRACE={path}")


if __name__ == "__main__":
    main()
