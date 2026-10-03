#!/usr/bin/env python3
"""
GRULLA_ULTI25_BENCH_RUNNER_V0_3

Pareado por:
- estado del jugador
- perfil de equipo
- brazo de consumibles
- seed

Headline: consumable arm NONE.
Stress: brazos HP1..3 / Qi0..1 por separado.

Técnicas normales siguen deshabilitadas en este runner.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from hashlib import sha256
from typing import Any, Iterable
import json

class Window(str, Enum):
    F1_EARLY="F1_EARLY"
    F2_ENTRY="F2_ENTRY"
    F3_ENTRY="F3_ENTRY"
    PREPARED_OPPORTUNITY="PREPARED_OPPORTUNITY"

class PlayerState(str, Enum):
    FULL="FULL"
    BALANCED="BALANCED"
    DISADVANTAGE="DISADVANTAGE"
    NEAR_DEATH="NEAR_DEATH"

EQUIPMENT_PROFILES=("MANDATORY_ENTRY","EXPECTED_STAGE","HIGH_ROLL_STRESS")
HEADLINE_CONSUMABLE_ARMS=("NONE",)
STRESS_CONSUMABLE_ARMS=(
    "HP1_EXCEPTIONAL","HP2_EXCEPTIONAL","HP3_EXCEPTIONAL",
    "HP1_QI1_EXCEPTIONAL","HP2_QI1_EXCEPTIONAL","HP3_QI1_EXCEPTIONAL"
)
ALL_CONSUMABLE_ARMS=HEADLINE_CONSUMABLE_ARMS+STRESS_CONSUMABLE_ARMS
NORMAL_TECHNIQUES_ENABLED=False
CONSUMABLE_QUANTITIES_CANON=False
ENCOUNTER_STAGE="LianQi_IV"

ULTIMATES_25=(
"Renacer del Sol Carmesí","Corazón de la Montaña Ardiente","Aguja del Crisol Rojo",
"Loto de Vapor Concordante 1.1","Brasa del Vendaval 0.4","Sentencia del Filo Celestial",
"Forja de la Espada Carmesí","Espejo del Acero Fluido","Mandato de la Montaña de Hierro",
"Tormenta del Horizonte Partido","Océano Invertido 0.5","Caldera del Sol Sumergido 0.2",
"Luna de Acero sobre el Lago Inmóvil","Delta de las Diez Mil Corrientes",
"Dominio del Mar sin Horizonte 0.4","Sepulcro de las Diez Mil Montañas",
"Trono del Volcán Sepultado 0.2","Ciudadela de la Espada Inamovible 0.2",
"Presa de los Nueve Mares 1.0","Horizonte de las Montañas Errantes",
"Danza del Viento sin Huella","Cometa Carmesí de los Nueve Cielos 0.3",
"Vendaval de las Mil Heridas 0.2","Río Celeste sin Orillas 0.2",
"Desierto Suspendido de las Mil Dunas 0.2"
)

@dataclass(frozen=True)
class ScenarioKey:
    player_state:str
    equipment_profile:str
    consumable_arm:str
    seed_index:int
    ultimate:str|None
    window:str

    @property
    def pair_id(self)->str:
        return (
            f"{self.player_state}:{self.equipment_profile}:"
            f"{self.consumable_arm}:{self.seed_index:06d}"
        )

def master_seed(player_state:str,equipment_profile:str,consumable_arm:str,seed_index:int,
                base_seed:int=2026100201)->int:
    payload=f"{base_seed}|{player_state}|{equipment_profile}|{consumable_arm}|{seed_index}".encode()
    return int.from_bytes(sha256(payload).digest()[:8],"big")

class RngStreams:
    DOMAINS=(
        "boss_decision","boss_accuracy","boss_crit",
        "player_normal_accuracy","player_normal_crit",
        "control","status","ultimate","equipment_effect",
        "consumable_hp","consumable_qi","aux_neutral_action"
    )
    def __init__(self,master_seed_value:int):
        self.master_seed=int(master_seed_value)
    def seed_for(self,domain:str,*coords:Any)->int:
        if domain not in self.DOMAINS: raise ValueError(f"RNG domain no autorizado: {domain}")
        payload="|".join(map(str,(self.master_seed,domain,*coords))).encode()
        return int.from_bytes(sha256(payload).digest()[:8],"big")

def iter_scenarios(seeds:int,*,consumable_arms:tuple[str,...]=HEADLINE_CONSUMABLE_ARMS)->Iterable[ScenarioKey]:
    for ps in PlayerState:
        for eq in EQUIPMENT_PROFILES:
            for ca in consumable_arms:
                if ca not in ALL_CONSUMABLE_ARMS: raise ValueError(ca)
                for i in range(seeds):
                    for ulti in ULTIMATES_25:
                        for w in Window:
                            yield ScenarioKey(ps.value,eq,ca,i,ulti,w.value)

def iter_baselines(seeds:int,*,consumable_arms:tuple[str,...]=HEADLINE_CONSUMABLE_ARMS)->Iterable[ScenarioKey]:
    for ps in PlayerState:
        for eq in EQUIPMENT_PROFILES:
            for ca in consumable_arms:
                if ca not in ALL_CONSUMABLE_ARMS: raise ValueError(ca)
                for i in range(seeds):
                    yield ScenarioKey(ps.value,eq,ca,i,None,"BASELINE_NO_ULTI")

def expected_counts(seeds:int,*,consumable_arms:tuple[str,...]=HEADLINE_CONSUMABLE_ARMS)->dict[str,int]:
    baselines=len(PlayerState)*len(EQUIPMENT_PROFILES)*len(consumable_arms)*seeds
    ulti=baselines*len(ULTIMATES_25)*len(Window)
    return {
        "seeds":seeds,
        "equipment_profiles":len(EQUIPMENT_PROFILES),
        "consumable_arms":len(consumable_arms),
        "baseline_encounters":baselines,
        "ulti_encounters":ulti,
        "total_encounters":baselines+ulti
    }

def self_check_design()->dict[str,Any]:
    failures=[]
    headline=expected_counts(20)
    stress=expected_counts(20,consumable_arms=STRESS_CONSUMABLE_ARMS)
    if len(ULTIMATES_25)!=25: failures.append("ULTIMATE_COUNT")
    if NORMAL_TECHNIQUES_ENABLED: failures.append("TECHNIQUES_MUST_BE_OFF")
    if CONSUMABLE_QUANTITIES_CANON: failures.append("QUANTITY_STRESS_MUST_NOT_BE_CANON")
    if headline["ulti_encounters"]!=24000: failures.append("HEADLINE_SMOKE_COUNT")
    if stress["ulti_encounters"]!=144000: failures.append("STRESS_SMOKE_COUNT")
    return {
      "pass":not failures,"failures":failures,
      "headline_smoke":headline,"consumable_stress_smoke":stress,
      "stress_is_separate":True
    }

if __name__=="__main__":
    r=self_check_design()
    print(json.dumps(r,ensure_ascii=False,indent=2))
    raise SystemExit(0 if r["pass"] else 1)
