"""ETAPA 19B — motor unificado 1v1 para matriz masiva Arco 1.

LAB ONLY. No toca runtime/HTML.

Objetivo:
- interpretar las 15 técnicas y sus ramas desde techniques_arc1_catalog.json;
- aplicar raíces, progresión, equipo y monstruos traducidos al contrato nuevo;
- resolver T0/T1 (y dejar stats T2-T4 legibles) con CADENCE_COMPAT;
- producir métricas reproducibles para el screen masivo posterior.

No declara números nuevos como CANON. Los dos umbrales que el laboratorio de IA
no congeló (qué significa SELF_LOW_HP y TOOK_HEAVY_HIT) se exponen como
LabSignalBridge y se registran en cada salida. Deben someterse a sensibilidad.
"""
from __future__ import annotations

from collections import Counter, deque
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence
import json
import math
import random
import re
import statistics

HERE = Path(__file__).resolve().parent
TECHNIQUE_CATALOG_PATH = HERE / "techniques_arc1_catalog.json"
MONSTER_CATALOG_PATH = HERE / "monster_arc1_new_contract_lab.json"
EQUIPMENT_CATALOG_PATH = HERE / "equipment_arc1_catalog.json"

STAGES = {
    "LianQi_I":   {"hp": 30, "qi": 37, "basic_attack": "1d4+4", "tech_scalar": 1.00},
    "LianQi_II":  {"hp": 36, "qi": 43, "basic_attack": "1d4+5", "tech_scalar": 1.08},
    "LianQi_III": {"hp": 42, "qi": 49, "basic_attack": "1d4+6", "tech_scalar": 1.16},
    "LianQi_IV":  {"hp": 48, "qi": 55, "basic_attack": "1d4+7", "tech_scalar": 1.24},
}
ROOTS = {
    "fuego":  {"direct_damage_pct": 10.0, "crit_chance_pp": 5.0},
    "metal":  {"percent_penetration_pp": 10.0, "precision": 5.0},
    "agua":   {"qi_cost_mult": 0.90, "control": 5.0},
    "tierra": {"hp_max_mult": 1.10, "tenacity": 5.0},
    "viento": {"evasion": 10.0, "crit_damage_add": 0.05},
}
ROOT_TECHNIQUES = {
    "fuego": ("palma_ardiente", "cuerpo_horno", "circulo_cien_ascuas"),
    "metal": ("destello_plata", "armadura_plata", "lluvia_filos"),
    "agua": ("latigazo_marea", "espejo_luna", "marea_ocho_orillas"),
    "tierra": ("golpe_montana", "piel_cobre", "temblor_montana"),
    "viento": ("lanza_nubes", "paso_nube", "tijera_vendaval"),
}
OFFENSE_PREFS = {
    "rata_qi":1.0,"serpiente_qi":0.9,"lobo_espiritual":1.05,"eco_caido":1.0,
    "pez_lunar":1.05,"sombra_ahogada":0.9,"centinela_pluma":1.05,"devorador_niebla":1.05,
    "avispa_jade":0.9,"mono_pildoras":0.9,"sapo_ceniza":0.9,"sapo_caldera":0.9,
    "escarabajo_hierro":1.1,"rey_escarabajo":1.05,"anguila_estelar":0.9,
    "guardian_coral":0.9,"halcon_tormenta":1.1,"mantis_nube":1.1,
}
PROFILE_NEXT = {
    "INSTINTIVO":"REACTIVO_1","REACTIVO_1":"CAZADOR_2","CAZADOR_2":"TACTICO_3",
    "TACTICO_3":"MASTER_4","MASTER_4":"MASTER_4",
}
PROFILE_PARAMS = {
    "INSTINTIVO": {"repetition":3.0,"jitter":4.0},
    "REACTIVO_1": {"repetition":5.0,"jitter":3.0},
    "CAZADOR_2": {"repetition":8.0,"jitter":2.0},
    "TACTICO_3": {"repetition":12.0,"jitter":1.5},
    "MASTER_4": {"repetition":16.0,"jitter":1.0},
}


def clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def round_half_up(x: float) -> int:
    return int(math.floor(float(x) + 0.5))


def roll_dice(rng: random.Random, notation: str) -> float:
    total = 0.0
    for token in re.findall(r"[+-]?[^+-]+", notation.replace(" ", "")):
        sign = -1 if token.startswith("-") else 1
        body = token[1:] if token[:1] in "+-" else token
        if "d" in body.lower():
            n_s, sides_s = body.lower().split("d", 1)
            n = int(n_s) if n_s else 1
            sides = int(sides_s)
            total += sign * sum(rng.randint(1, sides) for _ in range(n))
        else:
            total += sign * int(body)
    return total


def load_json(path: str | Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


@dataclass(frozen=True)
class LabSignalBridge:
    """Adaptador LAB para señales que E1 dejó sin umbral numérico canónico."""
    low_hp_ratio: float = 0.30
    heavy_hit_ratio: float = 0.20
    provenance: str = "LAB_SIGNAL_BRIDGE_SENSITIVITY_REQUIRED"

    def validate(self) -> None:
        if not (0 < self.low_hp_ratio < 1):
            raise ValueError("low_hp_ratio debe estar en (0,1)")
        if not (0 < self.heavy_hit_ratio < 1):
            raise ValueError("heavy_hit_ratio debe estar en (0,1)")


@dataclass
class Metrics:
    player_damage_direct: float = 0.0
    player_damage_dot: float = 0.0
    monster_damage_direct: float = 0.0
    monster_damage_dot: float = 0.0
    player_def_prevented: float = 0.0
    monster_def_prevented: float = 0.0
    player_absorbed: float = 0.0
    monster_absorbed: float = 0.0
    player_hits: int = 0
    player_attempts: int = 0
    player_crits: int = 0
    monster_hits: int = 0
    monster_attempts: int = 0
    monster_crits: int = 0
    player_evades: int = 0
    monster_evades: int = 0
    control_attempts: int = 0
    control_successes: int = 0
    defense_procs: int = 0
    adaptation_procs: int = 0
    skill_usage: Counter = field(default_factory=Counter)
    basic_usage: int = 0
    qi_spent: float = 0.0
    qi_drained: float = 0.0
    qi_restored: float = 0.0
    overheal: float = 0.0


@dataclass
class Actor:
    hp_max: float
    hp: float
    qi_max: float = 0.0
    qi: float = 0.0
    precision: float = 100.0
    evasion: float = 0.0
    defense: float = 0.0
    tenacity: float = 0.0
    control: float = 0.0
    crit_chance: float = 5.0
    crit_damage: float = 1.50
    percent_penetration: float = 0.0
    flat_penetration: float = 0.0
    direct_damage_pct: float = 0.0
    technique_direct_damage_pct: float = 0.0
    basic_attack_flat: float = 0.0
    absorption: float = 0.0
    absorption_max: float = 0.0
    dots: list[dict] = field(default_factory=list)
    stat_effects: list[dict] = field(default_factory=list)
    skip_next_action: bool = False

    def alive(self) -> bool:
        return self.hp > 0

    def effect_sum(self, stat: str) -> float:
        return sum(float(e.get("amount", 0.0)) for e in self.stat_effects if e.get("stat") == stat)

    def effective(self, stat: str) -> float:
        return float(getattr(self, stat)) + self.effect_sum(stat)


@dataclass
class FightState:
    player: Actor
    monster: Actor
    player_root: str
    stage: str
    tier: str
    player_basic_dice: str
    tech_scalar: float
    compiled: dict[str, dict]
    monster_profile: dict
    signal_bridge: LabSignalBridge
    metrics: Metrics = field(default_factory=Metrics)
    round_no: int = 0
    player_defense: dict | None = None
    player_heat: float = 0.0
    player_next_wind: dict | None = None
    player_next_earth_precision: float = 0.0
    player_next_golpe_precision: float = 0.0
    next_latigazo_precision: float = 0.0
    equipment_effects: list[dict] = field(default_factory=list)
    gear_absorption: float = 0.0
    gear_abs_triggered: bool = False
    monster_survival: dict | None = None
    monster_survival_cd: int = 0
    monster_recent_actions: deque = field(default_factory=lambda: deque(maxlen=4))
    last_player_hp_damage_to_monster: float = 0.0
    arrastre_locked: bool = False
    arrastre_precision_debuff: float = 0.0
    peso: dict = field(default_factory=lambda: {"stacks":0,"duration":0,"per_stack":3.0,"max":2})
    resonance: dict | None = None
    next_water_control_bonus: float = 0.0
    loss_used_basic_after_qi_exhaustion: bool = False


# ---------------------------------------------------------------------------
# Catalog compilation
# ---------------------------------------------------------------------------

def _families(spec: dict, choices: Sequence[int]) -> list[str]:
    out=[]
    for tramo_idx, choice in enumerate(choices):
        if tramo_idx >= len(spec["tramos"]):
            raise ValueError("choice supera tramos")
        if choice not in (0,1,2):
            raise ValueError("choice debe ser 0..2")
        out.append(spec["tramos"][tramo_idx][choice]["family"])
    return out


def _base_compiled(spec: dict, choices: Sequence[int]) -> dict:
    b=spec["base"]
    return {
        "technique_id":spec["technique_id"],"name":spec["name"],"root":spec["root"],
        "role":spec["role_primary"],"targeting":spec["targeting"],"model":spec["model"],
        "choices":tuple(choices),"families":_families(spec, choices),
        "qi_cost_raw":float(b.get("qi_cost",0)),"damage_dice":b.get("damage_dice"),
        "nominal_damage":float(b.get("nominal_damage",0)),"direct_pct":0.0,
        "precision_mod":0.0,"crit_pp":0.0,"crit_damage_add":0.0,
        "percent_pen_pp":0.0,"flat_pen":0.0,"aoe_scalar":1.0,
        "dot":None,"control":None,"debuff":None,"defensive":None,
    }


def _apply_eff_cost(c: dict, flat: float=0.0, mults: Iterable[float]=()) -> None:
    c["qi_cost_raw"] += flat
    for m in mults: c["qi_cost_raw"] *= float(m)


def compile_technique(spec: dict, choices: Sequence[int], root: str | None=None) -> dict:
    c=_base_compiled(spec,choices); f=c["families"]; p=spec["model_params"]; model=spec["model"]
    def at(i,name): return len(f)>i and f[i]==name
    def count(name): return f.count(name)

    if model in {"FIRE_OFFENSE","FIRE_AOE"}:
        if model=="FIRE_AOE": c["aoe_scalar"]=float(p["aoe_single_target_scalar"])
        for i in range(min(3,len(f))):
            if f[i]=="DIRECT":
                c["direct_pct"] += p["direct_pct"][i]
                if "direct_qi_add" in p: c["qi_cost_raw"] += p["direct_qi_add"][i]
        if at(0,"DIRECT") and at(1,"DIRECT"): c["crit_damage_add"] += p.get("direct_synergy_crit_damage",p.get("direct_t1_t2_crit_damage",0))
        if len(f)==3 and all(x=="DIRECT" for x in f): c["crit_pp"] += p.get("full_direct_crit_pp",0)
        if count("DOT"):
            d=p["dot"]
            if len(f)==3 and all(x=="DOT" for x in f): cfg=d["full"]
            elif len(f)>=2 and at(0,"DOT") and at(1,"DOT"): cfg=d["t1_t2"]
            elif at(0,"DOT"): cfg=d["t1"]
            else: cfg=d["standalone_late"]
            c["dot"]={"family":"BURN","flat_per_tick":round_half_up(c["nominal_damage"]*cfg["pct_nominal"]),"ticks":cfg["ticks"],"max_stacks":cfg["max_stacks"]}
        eff=p["eff"]
        if at(0,"EFFICIENCY"): c["qi_cost_raw"] += eff["t1_flat_cost"]
        if at(1,"EFFICIENCY"): c["qi_cost_raw"] *= eff.get("t2_cost_mult",eff.get("t2_mult",1))
        if at(2,"EFFICIENCY"): c["qi_cost_raw"] *= eff.get("t3_cost_mult",eff.get("t3_mult",1))
        if at(0,"EFFICIENCY") and at(1,"EFFICIENCY"): c["precision_mod"] += eff.get("t1_t2_precision",0)
        if len(f)==3 and all(x=="EFFICIENCY" for x in f): c["precision_mod"] = max(c["precision_mod"],eff.get("full_precision",c["precision_mod"]))

    elif model=="FIRE_BARRIER":
        absorption=p["absorption_pct"]; duration=p["duration"]
        for fam in f:
            if fam=="BARRIER": absorption+=p["barrier_pp_each"]
        if at(0,"BARRIER") and at(1,"BARRIER"): absorption+=p["barrier_t1_t2_synergy_pp"]
        conv=count("CONVERSION"); rate=cap=0.0
        if conv:
            cfg=p["conversion_by_count"][str(conv)]; rate=cfg["rate"]; cap=cfg["cap_pct"]
            if at(0,"CONVERSION") and conv==1:
                q=p["conversion_overrides"]["T1_ONLY"]; rate=q["rate"];cap=q["cap_pct"]
            if at(0,"CONVERSION") and at(1,"CONVERSION") and conv==2:
                q=p["conversion_overrides"]["T1_T2"]; rate=q["rate"];cap=q["cap_pct"]
        eff=p["eff"]
        if at(0,"EFFICIENCY"): c["qi_cost_raw"]+=eff["t1_flat_cost"]
        if at(1,"EFFICIENCY"):
            c["qi_cost_raw"]*=eff["later_mult"]
            if at(0,"EFFICIENCY"): duration=eff["t1_t2_duration"]
        if at(2,"EFFICIENCY"):
            c["qi_cost_raw"]*=eff["later_mult"]
            if len(f)==3 and all(x=="EFFICIENCY" for x in f):
                duration=eff["full_duration"]; absorption+=eff["full_absorption_pp"]
        c["defensive"]={"kind":"FIRE_BARRIER","absorption_pct":absorption,"duration":duration,"heat_rate":rate,"heat_cap_pct":cap}

    elif model=="METAL_OFFENSE":
        c["percent_pen_pp"]+=p["base_percent_pen_pp"]
        pen=p["penetration"]
        if at(0,"PENETRATION"): c["percent_pen_pp"]+=pen["t1_percent_pp"]
        if at(1,"PENETRATION"): c["flat_pen"]+=pen["t1_t2_flat"] if at(0,"PENETRATION") else pen["t2_flat"]
        if at(2,"PENETRATION"):
            c["percent_pen_pp"]+=pen["t3_percent_pp"]
            if len(f)==3 and all(x=="PENETRATION" for x in f): c["flat_pen"]=pen["full_flat"]
        ex=p["execution"]
        for i in range(min(3,len(f))):
            if f[i]=="EXECUTION": c["precision_mod"]+=ex["precision"][i]; c["crit_pp"]+=ex["crit_pp"][i]
        if at(0,"EXECUTION") and at(1,"EXECUTION"): c["crit_damage_add"]+=ex["t1_t2_crit_damage"]
        if len(f)==3 and all(x=="EXECUTION" for x in f): c["crit_damage_add"]=ex["full_crit_damage"]
        eff=p["eff"]
        if at(0,"EFFICIENCY"): c["qi_cost_raw"]+=eff["t1_flat_cost"]
        if at(1,"EFFICIENCY"): c["qi_cost_raw"]*=eff["t2_mult"]
        if at(2,"EFFICIENCY"): c["qi_cost_raw"]*=eff["t3_mult"]
        if at(0,"EFFICIENCY") and at(1,"EFFICIENCY"): c["precision_mod"]+=eff["t1_t2_precision"]
        if len(f)==3 and all(x=="EFFICIENCY" for x in f): c["precision_mod"]=max(c["precision_mod"],eff["full_precision"])

    elif model=="METAL_PLATES":
        rc=count("RESISTANCE"); ac=count("ADAPTATION"); qc=count("QUANTITY")
        plate_def=p["base_defense_per_plate"] if rc==0 else p["resistance_defense_by_count"][str(rc)]
        plates=p["base_plates"] if qc==0 else p["quantity_plates_by_count"][str(qc)]
        adapt_ten=0 if ac==0 else p["adapt_tenacity_by_count"][str(ac)]
        c["defensive"]={"kind":"METAL_PLATES","duration":p["duration"],"plates":plates,"plate_def":plate_def,"adapt_count":ac,"adapt_tenacity":adapt_ten,"no_consume_zero":ac>=p["adapt_no_consume_zero_from_count"],"recover_on_control_fail":ac>=p["adapt_recover_plate_on_control_fail_count"]}

    elif model=="METAL_AOE":
        c["aoe_scalar"]=p["aoe_single_target_scalar"]; c["percent_pen_pp"]+=p["base_percent_pen_pp"]
        for i in range(min(3,len(f))):
            if f[i]=="DIRECT": c["direct_pct"]+=p["direct_pct"][i]; c["qi_cost_raw"]+=p["direct_qi_add"][i]
        if len(f)==3 and all(x=="DIRECT" for x in f): c["crit_pp"]+=p["full_direct_crit_pp"]; c["crit_damage_add"]+=p["full_direct_crit_damage"]
        ru=p["rupture"]
        if count("RUPTURE"):
            if len(f)==3 and all(x=="RUPTURE" for x in f): c["debuff"]={"stat":"defense","amount":-ru["full_def_shred"],"turns":ru["full_duration"],"post_hit":True}; c["percent_pen_pp"]+=ru["full_pen_pp"]
            elif at(0,"RUPTURE") and at(1,"RUPTURE"): c["debuff"]={"stat":"defense","amount":-ru["t1_t2_def_shred"],"turns":ru["t1_t2_duration"],"post_hit":True}; c["percent_pen_pp"]+=ru["t1_t2_pen_pp"]
            else: c["debuff"]={"stat":"defense","amount":-ru["single_def_shred"],"turns":ru["single_duration"],"post_hit":True}
        eff=p["eff"]
        if at(0,"EFFICIENCY"): c["qi_cost_raw"]+=eff["t1_flat_cost"]
        if at(1,"EFFICIENCY"): c["qi_cost_raw"]*=eff["t2_mult"]
        if at(2,"EFFICIENCY"): c["qi_cost_raw"]*=eff["t3_mult"]
        if at(0,"EFFICIENCY") and at(1,"EFFICIENCY"): c["precision_mod"]+=eff["t1_t2_precision"]
        if len(f)==3 and all(x=="EFFICIENCY" for x in f): c["precision_mod"]=max(c["precision_mod"],eff["full_precision"]); c["percent_pen_pp"]+=eff["full_pen_pp"]

    elif model=="WATER_CONTROL":
        c["control"]={"base":p["base_control"],"bonus":count("CONTROL")*p["control_bonus_each"],"anti_lock":p["anti_lock"],"precision_debuff_on_success":0,"next_precision":0}
        if at(0,"CONTROL") and at(1,"CONTROL"): c["control"]["precision_debuff_on_success"]=p["control_t1_t2_precision_debuff"]
        if len(f)==3 and all(x=="CONTROL" for x in f): c["control"]["next_precision"]=p["full_control_next_precision"]
        for i in range(min(3,len(f))):
            if f[i]=="DIRECT": c["direct_pct"]+=p["direct_pct"][i]
        if at(0,"DIRECT") and at(1,"DIRECT"): c["crit_pp"]+=p["direct_t1_t2_crit_pp"]
        eff=p["eff"]
        if at(0,"EFFICIENCY"): c["qi_cost_raw"]+=eff["t1_flat_cost"]
        if at(1,"EFFICIENCY"): c["qi_cost_raw"]*=eff["t2_mult"]
        if at(2,"EFFICIENCY"): c["qi_cost_raw"]*=eff["t3_mult"]
        if at(0,"EFFICIENCY") and at(1,"EFFICIENCY"): c["precision_mod"]+=eff["t1_t2_precision"]
        if len(f)==3 and all(x=="EFFICIENCY" for x in f): c["precision_mod"]=max(c["precision_mod"],eff["full_precision"])

    elif model=="WATER_MIRROR":
        reserve=p["reserve_pct"]+count("RESERVE")*p["reserve_pp_each"]
        if at(0,"RESERVE") and at(1,"RESERVE"): reserve+=p["reserve_t1_t2_synergy_pp"]
        reflow=min(p["reflow_cap"],p["reflow_pct"]+count("REFLOW")*p["reflow_pp_each"])
        reconstruct=0.0; duration=p["duration"]
        if at(0,"REFLOW") and at(1,"REFLOW"): reconstruct=p["reconstruct_t1_t2_pct"]
        if reconstruct and at(2,"REFLOW"): reconstruct=p["reconstruct_with_t3_pct"]
        eff=p["eff"]
        if at(0,"EFFICIENCY"): c["qi_cost_raw"]+=eff["t1_flat_cost"]
        if at(1,"EFFICIENCY"):
            c["qi_cost_raw"]*=eff["later_mult"]
            if at(0,"EFFICIENCY"): duration=eff["t1_t2_duration"]
        restore=0
        if at(2,"EFFICIENCY"):
            c["qi_cost_raw"]*=eff["later_mult"]; restore=eff["t3_restore_qi_on_natural_expire"]
            if len(f)==3 and all(x=="EFFICIENCY" for x in f): duration=eff["full_duration"]
        c["defensive"]={"kind":"WATER_MIRROR","reserve_pct":reserve,"reflow_pct":reflow,"duration":duration,"reconstruct_pct":reconstruct,"restore_qi_on_natural_expire":restore}

    elif model=="WATER_AOE":
        c["aoe_scalar"]=p["aoe_single_target_scalar"]
        amount=p["base_precision_debuff"]; dur=p["base_debuff_duration"]; ctl=0
        if at(0,"DEBUFF"): amount=p["debuff"]["t1_precision"]
        if at(1,"DEBUFF"):
            dur=p["debuff"]["t2_duration"]; ctl=p["debuff"]["t2_next_water_control"]
            if at(0,"DEBUFF"): amount=p["debuff"]["t1_t2_precision"]
        if at(2,"DEBUFF") and len(f)==3 and all(x=="DEBUFF" for x in f): amount=p["debuff"]["full_precision"]; ctl=p["debuff"]["full_next_water_control"]
        c["debuff"]={"stat":"precision","amount":-amount,"turns":dur,"next_water_control":ctl}
        for i in range(min(3,len(f))):
            if f[i]=="DIRECT": c["direct_pct"]+=p["direct_pct"][i]; c["qi_cost_raw"]+=p["direct_qi_add"][i]
        if at(0,"DIRECT") and at(1,"DIRECT"): c["crit_pp"]+=p["direct_t1_t2_crit_pp"]
        eff=p["eff"]
        if at(0,"EFFICIENCY"): c["qi_cost_raw"]+=eff["t1_flat_cost"]
        if at(1,"EFFICIENCY"): c["qi_cost_raw"]*=eff["t2_mult"]
        if at(2,"EFFICIENCY"): c["qi_cost_raw"]*=eff["t3_mult"]
        if at(0,"EFFICIENCY") and at(1,"EFFICIENCY"): c["precision_mod"]+=eff["t1_t2_precision"]
        if len(f)==3 and all(x=="EFFICIENCY" for x in f): c["precision_mod"]=max(c["precision_mod"],eff["full_precision"])

    elif model=="EARTH_OFFENSE":
        ps=p["peso"]; per=ps["base_evasion_per_stack"]; mx=ps["base_max_stacks"]; dur=ps["base_duration"]
        if at(0,"PRESSURE"): per=ps["t1_evasion_per_stack"]
        if at(1,"PRESSURE"): mx=ps["t2_max_stacks"]; dur=ps["t2_max_duration"] if at(0,"PRESSURE") else dur
        if len(f)==3 and all(x=="PRESSURE" for x in f): per=ps["full_evasion_per_stack"];mx=ps["full_max_stacks"];dur=ps["full_duration"]
        c["peso"]={"evasion_per_stack":per,"max_stacks":mx,"duration":dur}
        for i in range(min(3,len(f))):
            if f[i]=="DIRECT": c["direct_pct"]+=p["direct_pct"][i]
        c["max_peso_bonus_pct"]=p["direct_full_max_peso_bonus_pct"] if len(f)==3 and all(x=="DIRECT" for x in f) else (p["direct_t2_max_peso_bonus_pct"] if at(0,"DIRECT") and at(1,"DIRECT") else 0)
        sc=count("STABILITY"); st=p["stability"]
        c["self_stability"]={"tenacity":sc*st["tenacity_each"],"defense":st["full_defense"] if sc==3 else (st["t1_t2_defense"] if at(0,"STABILITY") and at(1,"STABILITY") else 0),"next_precision_on_control_fail":st["full_next_precision_on_control_fail"] if sc==3 else 0}

    elif model=="EARTH_SKIN":
        fort=count("FORTIFICATION"); stab=count("STABILITY"); end=count("ENDURANCE")
        dur=p["duration"]+(p["endurance_duration_bonus_cap"] if (at(0,"ENDURANCE") or at(2,"ENDURANCE")) else 0)
        c["defensive"]={"kind":"EARTH_SKIN","duration":dur,"activation_defense":p["activation_defense"],"initial_arraigo":p["initial_arraigo"],"max_arraigo":p["max_arraigo"],"tenacity_per_arraigo":p["stability_t1_tenacity_per_arraigo"] if at(0,"STABILITY") else p["tenacity_per_arraigo"],"arraigo_defense":p["fort_t1_arraigo_defense"] if at(0,"FORTIFICATION") else p["arraigo_defense"],"large_hit_ratio":p["large_hit_ratio"],"reach_max_duration_extension":p["reach_max_duration_extension"],"stratum_defense":p["fort_t2_stratum_defense"] if at(1,"FORTIFICATION") else 0,"rock_guard_defense":p["fort_t3_rock_guard_defense"] if at(2,"FORTIFICATION") else 0,"extra_tenacity_at_2":p["stability_t2_extra_tenacity_at_2"] if at(1,"STABILITY") else 0,"control_fail_extension":p["stability_t2_control_fail_extension"] if at(0,"STABILITY") and at(1,"STABILITY") else 0,"extra_tenacity":p["stability_t3_extra_tenacity"] if at(2,"STABILITY") else 0,"next_golpe_precision":p["stability_t3_next_golpe_precision"] if at(2,"STABILITY") else 0,"reach_max_heal_pct":(p["endurance_t2_reach_max_heal_pct"] if at(1,"ENDURANCE") else 0)+(p["endurance_t3_reach_max_heal_pct"] if at(2,"ENDURANCE") else 0),"low_hp_threshold":p["endurance_t3_low_hp_threshold"] if at(2,"ENDURANCE") else 0,"low_hp_heal_pct":p["endurance_t3_low_hp_heal_pct"] if at(2,"ENDURANCE") else 0}

    elif model=="EARTH_AOE":
        c["aoe_scalar"]=p["aoe_single_target_scalar"]
        amount=p["base_evasion_debuff"]; dur=p["base_duration"]
        if at(0,"DEBUFF"): amount=p["debuff"]["t1_evasion"]
        if at(1,"DEBUFF"):
            dur=p["debuff"]["t2_duration"]
            if at(0,"DEBUFF"): amount=p["debuff"]["t1_t2_evasion"]
        if len(f)==3 and all(x=="DEBUFF" for x in f): amount=p["debuff"]["full_evasion"];dur=p["debuff"]["full_duration"]
        c["debuff"]={"stat":"evasion","amount":-amount,"turns":dur}
        for i in range(min(3,len(f))):
            if f[i]=="DIRECT": c["direct_pct"]+=p["direct_pct"][i]; c["qi_cost_raw"]+=p["direct_qi_add"][i]
        if at(0,"DIRECT") and at(1,"DIRECT"): c["crit_pp"]+=p["direct_t1_t2_crit_pp"]
        if len(f)==3 and all(x=="DIRECT" for x in f): c["crit_damage_add"]+=p["full_direct_crit_damage"]
        if count("PREPARATION"):
            prep=p["prep"]; prec=prep["t1_precision"] if at(0,"PREPARATION") else prep["t2_alone_precision"]; pd=prep["t1_duration"]
            if at(1,"PREPARATION"): prec=prep["t2_with_t1_precision"] if at(0,"PREPARATION") else prep["t2_alone_precision"];pd=prep["t2_duration"]
            extra=0
            if len(f)==3 and all(x=="PREPARATION" for x in f): prec=prep["full_precision"];extra=prep["full_extra_peso_stack"]
            c["resonance"]={"precision":prec,"duration":pd,"extra_peso_stack":extra}

    elif model=="WIND_OFFENSE":
        c["precision_mod"]+=p["base_precision"]; c["crit_pp"]+=p["base_crit_pp"]
        pr=p["precision"]
        for i in range(min(3,len(f))):
            if f[i]=="PRECISION": c["precision_mod"]+=pr["each"]
        if at(1,"PRECISION"): c["crit_pp"]+=pr["t2_crit_pp"]
        if at(0,"PRECISION") and at(1,"PRECISION"): c["crit_damage_add"]+=pr["t1_t2_crit_damage"]
        if at(2,"PRECISION"): c["crit_pp"]+=pr["t3_crit_pp"]
        for i in range(min(3,len(f))):
            if f[i]=="DIRECT": c["direct_pct"]+=p["direct_pct"][i]
        if at(1,"DIRECT"): c["qi_cost_raw"]+=p["direct_t2_qi_add"]
        eff=p["eff"]
        if at(0,"EFFICIENCY"): c["qi_cost_raw"]+=eff["t1_flat_cost"]
        if at(1,"EFFICIENCY"): c["qi_cost_raw"]*=eff["t2_mult"]
        if at(2,"EFFICIENCY"): c["qi_cost_raw"]*=eff["t3_mult"]
        if at(0,"EFFICIENCY") and at(1,"EFFICIENCY"): c["precision_mod"]+=eff["t1_t2_precision"]
        if len(f)==3 and all(x=="EFFICIENCY" for x in f): c["precision_mod"]=max(c["precision_mod"],p["base_precision"]+eff["full_precision"])

    elif model=="WIND_STEP":
        ev=p["evasion_granted"]+count("EVASION")*p["evasion_each"]; resp=count("RESPONSE"); duration=p["duration"]
        eff=p["eff"]
        if at(0,"EFFICIENCY"): c["qi_cost_raw"]+=eff["t1_flat_cost"]
        if at(1,"EFFICIENCY"):
            c["qi_cost_raw"]*=eff["later_mult"]
            if at(0,"EFFICIENCY"): duration+=eff["duration_bonus_if_prior"]
        if at(2,"EFFICIENCY"):
            c["qi_cost_raw"]*=eff["later_mult"]
            if at(0,"EFFICIENCY") or at(1,"EFFICIENCY"): duration+=eff["duration_bonus_if_prior"]
        c["defensive"]={"kind":"WIND_STEP","duration":duration,"evasion":ev,"response_count":resp,"response_precision":0 if resp==0 else p["response_precision_by_count"][str(resp)],"response_crit_pp":p["response_full_crit_pp"] if resp==3 else 0}

    elif model=="WIND_AOE":
        c["aoe_scalar"]=p["aoe_single_target_scalar"]
        amount=p["base_precision_debuff"];dur=p["base_debuff_duration"]
        if at(0,"INTERFERENCE"): amount=p["interference"]["t1_precision"]
        if at(1,"INTERFERENCE"):
            dur=p["interference"]["t2_duration"]
            if at(0,"INTERFERENCE"): amount=p["interference"]["t1_t2_precision"]
        if len(f)==3 and all(x=="INTERFERENCE" for x in f): amount=p["interference"]["full_precision"];dur=p["interference"]["full_duration"]
        c["debuff"]={"stat":"precision","amount":-amount,"turns":dur}
        for i in range(min(3,len(f))):
            if f[i]=="DIRECT": c["direct_pct"]+=p["direct_pct"][i];c["qi_cost_raw"]+=p["direct_qi_add"][i]
        if at(0,"DIRECT") and at(1,"DIRECT"): c["crit_pp"]+=p["direct_t1_t2_crit_pp"]
        if len(f)==3 and all(x=="DIRECT" for x in f): c["crit_pp"]=p["full_direct_crit_pp"];c["crit_damage_add"]+=p["full_direct_crit_damage"]
        fl=p["flow"]
        if at(0,"FLOW"): c["qi_cost_raw"]+=fl["t1_flat_cost"];c["precision_mod"]+=fl["t1_precision"]
        if at(1,"FLOW"): c["qi_cost_raw"]*=fl["t2_mult"]
        if at(2,"FLOW"): c["qi_cost_raw"]*=fl["t3_mult"]
        if at(0,"FLOW") and at(1,"FLOW"): c["precision_mod"]=max(c["precision_mod"],fl["t1_t2_precision"])
        if len(f)==3 and all(x=="FLOW" for x in f): c["precision_mod"]=fl["full_precision"]
    else:
        raise ValueError(f"modelo no soportado: {model}")

    # Raíz Agua: capa global de coste; el piso exacto sigue PENDIENTE, por lo
    # que el LAB no inventa uno adicional. Todas las cifras actuales quedan >0.
    if (root or spec["root"]) == "agua": c["qi_cost_raw"] *= ROOTS["agua"]["qi_cost_mult"]
    c["qi_cost"] = max(0, round_half_up(c["qi_cost_raw"]))
    return c


def compile_build(root: str, paths: Mapping[str, Sequence[int]], catalog: dict | None=None) -> dict[str,dict]:
    if catalog is None: catalog=load_json(TECHNIQUE_CATALOG_PATH)
    out={}
    for tid in ROOT_TECHNIQUES[root]:
        out[tid]=compile_technique(catalog["techniques"][tid], tuple(paths.get(tid, ())), root)
    return out


# ---------------------------------------------------------------------------
# Actor construction
# ---------------------------------------------------------------------------

def aggregate_items(item_ids: Sequence[str], equipment_catalog: dict) -> tuple[dict, list[dict]]:
    by_id={x["item_id"]:x for x in equipment_catalog["items"]}; stats=Counter();effects=[]
    for iid in item_ids:
        if iid not in by_id: raise KeyError(f"item desconocido: {iid}")
        it=by_id[iid]
        for k,v in it.get("stats",{}).items(): stats[k]+=float(v)
        if it.get("effect"): effects.append(dict(it["effect"]))
    return dict(stats),effects


def build_player(stage: str, root: str, item_ids: Sequence[str], equipment_catalog: dict) -> tuple[Actor,dict]:
    s=STAGES[stage]; stats,effects=aggregate_items(item_ids,equipment_catalog)
    hp=float(s["hp"])+stats.get("hp_max",0); qi=float(s["qi"])+stats.get("qi_max",0)
    if root=="tierra": hp*=ROOTS[root]["hp_max_mult"]
    a=Actor(hp_max=hp,hp=hp,qi_max=qi,qi=qi,precision=100+stats.get("precision",0),evasion=5+stats.get("evasion",0),defense=1+stats.get("defense",0),tenacity=stats.get("tenacity",0),control=stats.get("control",0),crit_chance=5+stats.get("crit_chance_pp",0),crit_damage=1.50,percent_penetration=stats.get("percent_penetration_pp",0),flat_penetration=0,direct_damage_pct=0,technique_direct_damage_pct=stats.get("technique_direct_damage_percent",0),basic_attack_flat=stats.get("basic_attack_flat",0))
    r=ROOTS[root]
    a.direct_damage_pct+=r.get("direct_damage_pct",0);a.crit_chance+=r.get("crit_chance_pp",0);a.percent_penetration+=r.get("percent_penetration_pp",0);a.precision+=r.get("precision",0);a.control+=r.get("control",0);a.tenacity+=r.get("tenacity",0);a.evasion+=r.get("evasion",0);a.crit_damage+=r.get("crit_damage_add",0)
    return a,{"equipment_stats":stats,"equipment_effects":effects}


def build_monster(profile: dict, tier: str) -> Actor:
    n=profile["new_contract_lab"]; ad=profile["adaptive_c_staggered"][tier]
    hp=float(n["hp"])*float(ad["hp_mult"])
    return Actor(hp_max=hp,hp=hp,precision=float(n["precision"])+float(ad.get("precision_bonus",0)),evasion=float(n["evasion"])+float(ad.get("evasion_bonus",0)),defense=float(n["defense"]),tenacity=float(n["tenacity"]),control=float(n.get("control",0)),crit_chance=float(ad.get("crit_chance",n.get("crit_chance",5))),crit_damage=float(n.get("crit_damage",1.5)))


# ---------------------------------------------------------------------------
# Effects / damage
# ---------------------------------------------------------------------------

def _tick_effects(actor: Actor) -> None:
    kept=[]
    for e in actor.stat_effects:
        e=dict(e); e["turns"]-=1
        if e["turns"]>0: kept.append(e)
    actor.stat_effects=kept


def _replace_effect(actor: Actor, stat: str, amount: float, turns: int, tag: str) -> None:
    actor.stat_effects=[e for e in actor.stat_effects if e.get("tag")!=tag]
    actor.stat_effects.append({"stat":stat,"amount":amount,"turns":int(turns),"tag":tag})


def _absorb(actor: Actor, amount: float, metrics: Metrics, target_is_player: bool, state: FightState | None=None) -> tuple[float,float]:
    if amount<=0: return amount,0.0
    used_total=0.0
    technique_used=0.0
    if actor.absorption>0:
        used=min(actor.absorption,amount);actor.absorption-=used;amount-=used;used_total+=used;technique_used=used
    if target_is_player and state is not None and amount>0 and state.gear_absorption>0:
        used=min(state.gear_absorption,amount);state.gear_absorption-=used;amount-=used;used_total+=used
    if target_is_player: metrics.player_absorbed+=used_total
    else: metrics.monster_absorbed+=used_total
    if target_is_player and state is not None and used_total>0:
        ds=state.player_defense
        # Sólo la parte absorbida por el pool de Cuerpo-Horno genera Calor. El
        # tesoro usa un pool independiente y no alimenta esta técnica.
        if ds and ds["kind"]=="FIRE_BARRIER" and technique_used>0:
            if ds["heat_rate"]>0:
                cap=ds["heat_cap_pct"]*actor.hp_max
                state.player_heat=min(cap,state.player_heat+technique_used*ds["heat_rate"])
    return amount,used_total


def _maybe_trigger_gear_absorption(state: FightState) -> None:
    if state.gear_abs_triggered or not state.player.alive(): return
    for effect in state.equipment_effects:
        if effect.get("type")!="HP_THRESHOLD_ABSORPTION": continue
        threshold=float(effect.get("threshold_pct",0))/100.0
        if state.player.hp/state.player.hp_max<=threshold:
            state.gear_absorption=float(effect.get("absorption_max_hp_percent",0))/100.0*state.player.hp_max
            state.gear_abs_triggered=True
            state.metrics.defense_procs+=1
            return


def _player_dynamic_defense(state: FightState) -> float:
    d=state.player.effective("defense"); ds=state.player_defense
    if not ds: return d
    if ds["kind"]=="METAL_PLATES" and ds["plates"]>0: d+=ds["plate_def"]
    elif ds["kind"]=="EARTH_SKIN":
        ar=ds["arraigo"];d+=ds["activation_defense"]+ds["arraigo_defense"][ar]
        if ds.get("stratum"): d+=ds["stratum_defense"]
        if ds.get("rock_guard"): d+=ds["rock_guard_defense"]
    return d


def _player_dynamic_evasion(state: FightState) -> float:
    e=state.player.effective("evasion");ds=state.player_defense
    if ds and ds["kind"]=="WIND_STEP": e+=ds["evasion"]
    return e


def _player_dynamic_tenacity(state: FightState) -> float:
    t=state.player.effective("tenacity");ds=state.player_defense
    if ds and ds["kind"]=="EARTH_SKIN":
        ar=ds["arraigo"];t+=ds["tenacity_per_arraigo"]*ar
        if ar>=2:t+=ds["extra_tenacity_at_2"]
        if ar>=1:t+=ds["extra_tenacity"]
    return t


def _monster_dynamic_defense(state: FightState) -> float:
    d=state.monster.effective("defense")
    s=state.monster_survival
    if s and s["kind"]=="DEFENSE_UP": d+=s["defense_bonus"]
    return d


def _monster_dynamic_evasion(state: FightState) -> float:
    e=state.monster.effective("evasion")
    if state.peso["duration"]>0: e-=state.peso["stacks"]*state.peso["per_stack"]
    s=state.monster_survival
    if s and s["kind"]=="EVADE_NEXT": e+=s["evasion_bonus"]
    return e


def _consume_monster_survival_after_player_action(state: FightState, connected: bool) -> None:
    s=state.monster_survival
    if not s: return
    if s["kind"] in {"EVADE_NEXT","DEFENSE_UP"}: state.monster_survival=None
    elif s["kind"]=="MITIGATE_NEXT" and connected: state.monster_survival=None
    # ABSORB_RESERVE persists in Actor.absorption until reserve exhausted.


def _post_player_hit_defense_consumption(state: FightState, damage_after_def: int) -> None:
    ds=state.player_defense
    if not ds:return
    if ds["kind"]=="METAL_PLATES" and ds["plates"]>0:
        if not (damage_after_def==0 and ds["no_consume_zero"]):
            ds["plates"]-=1;state.metrics.defense_procs+=1
    elif ds["kind"]=="EARTH_SKIN":
        if ds.get("stratum"): ds["stratum"]=False;state.metrics.defense_procs+=1
        if ds.get("rock_guard"): ds["rock_guard"]=False;state.metrics.defense_procs+=1


def resolve_player_direct(state: FightState, rng: random.Random, c: dict | None, basic: bool=False) -> dict:
    p,m,met=state.player,state.monster,state.metrics
    met.player_attempts+=1
    if basic:
        dice=state.player_basic_dice; precision_mod=0; crit_pp=0;crit_add=0;pct_pen=0;flat_pen=0;direct_pct=p.direct_damage_pct; aoe=1.0
    else:
        dice=c["damage_dice"]; precision_mod=c["precision_mod"];crit_pp=c["crit_pp"];crit_add=c["crit_damage_add"];pct_pen=c["percent_pen_pp"];flat_pen=c["flat_pen"];direct_pct=p.direct_damage_pct+p.technique_direct_damage_pct+c["direct_pct"];aoe=c["aoe_scalar"]
        if state.resonance and c["root"]=="tierra": precision_mod+=state.resonance["precision"]
        if state.player_next_wind and c["root"]=="viento": precision_mod+=state.player_next_wind["precision"];crit_pp+=state.player_next_wind["crit_pp"]
        if c["technique_id"]=="golpe_montana": precision_mod+=state.player_next_golpe_precision
        if c["technique_id"]=="latigazo_marea": precision_mod+=state.next_latigazo_precision
        if c.get("max_peso_bonus_pct") and state.peso["stacks"]>=state.peso["max"]: direct_pct+=c["max_peso_bonus_pct"]
    target_eva=_monster_dynamic_evasion(state)
    phit=clamp(p.effective("precision")+precision_mod-target_eva,5,100)/100
    hit=rng.random()<phit
    if not hit:
        met.monster_evades+=1;_consume_monster_survival_after_player_action(state,False)
        if not basic and c["root"]=="viento" and state.player_next_wind: state.player_next_wind=None
        if not basic and c["technique_id"]=="golpe_montana": state.player_next_golpe_precision=0
        if not basic and c["technique_id"]=="latigazo_marea": state.next_latigazo_precision=0
        return {"hit":False,"critical":False,"actual_hp_damage":0,"absorbed":0}
    met.player_hits+=1
    rolled=roll_dice(rng,dice)+(p.basic_attack_flat if basic else 0)
    if not basic: rolled*=state.tech_scalar
    dmg=rolled*max(0,1+direct_pct/100)
    crit=rng.random()<clamp(p.crit_chance+crit_pp,0,100)/100
    if crit: met.player_crits+=1;dmg*=max(0,p.crit_damage+crit_add)
    dmg*=aoe
    # T1 MITIGATE_NEXT reduces the incoming direct packet before flat DEF (LAB bridge).
    s=state.monster_survival
    if s and s["kind"]=="MITIGATE_NEXT": dmg*=1-s["damage_reduction_pct"]/100
    real_def=max(0,_monster_dynamic_defense(state)); pct=clamp(p.percent_penetration+pct_pen,0,100); fp=max(0,p.flat_penetration+flat_pen)
    eff_def=max(0,real_def*(1-pct/100)-fp)
    after_decimal=max(0,dmg-eff_def); after=round_half_up(after_decimal)
    met.monster_def_prevented+=max(0,dmg-after_decimal)
    # Survival ABSORB has a per-hit cap, unlike generic player absorption.
    absorbed=0.0
    if s and s["kind"]=="ABSORB_RESERVE" and m.absorption>0:
        absorbed=min(after,m.absorption,s["absorb_per_hit"]);m.absorption-=absorbed;after-=absorbed;met.monster_absorbed+=absorbed
        if m.absorption<=0: state.monster_survival=None
    else:
        after,absorbed=_absorb(m,float(after),met,False)
    actual=min(m.hp,float(after));m.hp-=actual;met.player_damage_direct+=actual
    _consume_monster_survival_after_player_action(state,True)
    if not basic and c["root"]=="viento" and state.player_next_wind: state.player_next_wind=None
    if not basic and c["technique_id"]=="golpe_montana": state.player_next_golpe_precision=0
    if not basic and c["technique_id"]=="latigazo_marea": state.next_latigazo_precision=0
    return {"hit":True,"critical":crit,"actual_hp_damage":actual,"absorbed":absorbed,"damage_after_def":after,"effective_def":eff_def}


def resolve_monster_direct(state: FightState, rng: random.Random, dice: str) -> dict:
    p,m,met=state.player,state.monster,state.metrics;met.monster_attempts+=1
    precision=m.effective("precision")
    if state.arrastre_precision_debuff: precision-=state.arrastre_precision_debuff
    peva=_player_dynamic_evasion(state)
    hit=rng.random()<clamp(precision-peva,5,100)/100
    if not hit:
        met.player_evades+=1
        ds=state.player_defense
        if ds and ds["kind"]=="WIND_STEP" and ds["response_count"]>0 and not ds["response_created"]:
            state.player_next_wind={"precision":ds["response_precision"],"crit_pp":ds["response_crit_pp"]};ds["response_created"]=True;met.defense_procs+=1
        return {"hit":False,"actual_hp_damage":0}
    met.monster_hits+=1
    mult=float(state.monster_profile["adaptive_c_staggered"][state.tier]["damage_mult"])
    dmg=roll_dice(rng,dice)*mult
    crit=rng.random()<m.crit_chance/100
    if crit:met.monster_crits+=1;dmg*=m.crit_damage
    target_def=_player_dynamic_defense(state); after_decimal=max(0,dmg-target_def);after=round_half_up(after_decimal)
    met.player_def_prevented+=max(0,dmg-after_decimal)
    _post_player_hit_defense_consumption(state,after)
    after,absorbed=_absorb(p,float(after),met,True,state)
    actual=min(p.hp,float(after));p.hp-=actual;met.monster_damage_direct+=actual
    _maybe_trigger_gear_absorption(state)
    ds=state.player_defense
    # Piel gains Arraigo only if HP was actually lost.
    if ds and ds["kind"]=="EARTH_SKIN" and actual>0:
        gain=1
        if not ds["large_hit_used"] and actual>=ds["large_hit_ratio"]*p.hp_max: gain=2;ds["large_hit_used"]=True
        old=ds["arraigo"];ds["arraigo"]=min(ds["max_arraigo"],old+gain)
        if ds["stratum_defense"] and ds["arraigo"]>old and ds["arraigo"] in (2,3): ds["stratum"]=True
        if old<ds["max_arraigo"] and ds["arraigo"]==ds["max_arraigo"]:
            if not ds["max_extension_used"]: ds["turns_left"]+=ds["reach_max_duration_extension"];ds["max_extension_used"]=True
            if not ds["reach_heal_used"] an