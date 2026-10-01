"""Runner LAB que conecta T0LabCandidate con ETAPA19B sin falsear READY.

No modifica el catálogo canónico. El bypass de build_monster existe únicamente
dentro del context manager de esta corrida y acepta sólo un T0LabCandidate ya
validado contra un perfil canónico PENDING.
"""
from __future__ import annotations

from contextlib import contextmanager
from copy import deepcopy
import math
from pathlib import Path
import sys
from typing import Any

HERE=Path(__file__).resolve().parent
PARENT=HERE.parent
if str(PARENT) not in sys.path:
    sys.path.insert(0,str(PARENT))

import etapa19b_combat_engine as engine

from candidate import LAB_CANDIDATE_STATUS, T0LabCandidate, candidate_id
from guards import validate_action_space, validate_tier
from player_policy_veteran import (
    DEFAULT_VETERAN_CONFIG,
    VETERAN_BASIC,
    VeteranPolicyConfig,
    choose_veteran_action,
)
from telemetry import fight_once_observed

RUNTIME_QI_SENTINEL="UNRESOLVED_QI_NAN_SENTINEL"
BASIC_PROXY_SENTINEL_COST=10**9


def _lab_profile(candidate: T0LabCandidate, canonical_profile: dict) -> dict:
    candidate.validate_against_pending_profile(canonical_profile)
    profile=deepcopy(canonical_profile)
    profile["stats_status"]=LAB_CANDIDATE_STATUS
    profile["stats"]=dict(candidate.stats)
    tech=profile.get("technique")
    if tech is not None:
        tech["params_status"]=LAB_CANDIDATE_STATUS
        tech["params"]=deepcopy(candidate.technique_params)
    return profile


def _candidate_actor(candidate: T0LabCandidate) -> engine.Actor:
    s=candidate.stats
    # qi_max no participa todavía en ninguna mecánica T0 de estos monstruos.
    # NaN es un sentinel deliberado: si una futura ruta intenta usarlo, debe
    # contaminar/fallar en vez de introducir silenciosamente un número ficticio.
    return engine.Actor(
        hp_max=float(s["hp"]),
        hp=float(s["hp"]),
        qi_max=math.nan,
        qi=math.nan,
        precision=float(s["precision"]),
        evasion=float(s["evasion"]),
        defense=float(s["defense"]),
        tenacity=float(s["tenacity"]),
        control=float(s["control"]),
        crit_chance=float(s["crit_chance"]),
        crit_damage=float(s["crit_damage"]),
    )


@contextmanager
def _stage1_runtime(
    candidate: T0LabCandidate,
    canonical_profile: dict,
    policy_config: VeteranPolicyConfig,
):
    lab_profile=_lab_profile(candidate,canonical_profile)
    originals={
        "build_monster":engine.build_monster,
        "compile_build":engine.compile_build,
        "choose_player_action":engine.choose_player_action,
        "execute_player_technique":engine.execute_player_technique,
    }

    def build_monster(profile,tier):
        validate_tier(tier)
        if profile is not lab_profile:
            raise RuntimeError("Stage1 runner received an unexpected monster profile")
        return _candidate_actor(candidate)

    def compile_build(root,paths,catalog=None):
        compiled=originals["compile_build"](root,paths,catalog)
        compiled=dict(compiled)
        compiled[VETERAN_BASIC]={
            "technique_id":VETERAN_BASIC,
            "name":"Ataque básico",
            "root":root,
            "role":"BASIC_PROXY",
            "targeting":"UNITARGET",
            # No se paga: el runner intercepta el proxy. El coste sentinel alto
            # evita contaminar los cálculos del motor que buscan el mínimo coste
            # ofensivo para detectar agotamiento real de Qi.
            "qi_cost":BASIC_PROXY_SENTINEL_COST,
        }
        return compiled

    def choose_player_action(state,policy):
        if policy!="VETERAN":
            return originals["choose_player_action"](state,policy)
        action=choose_veteran_action(state,policy_config)
        validate_action_space([action])
        return action

    def execute_player_technique(state,rng,c):
        if c.get("technique_id")==VETERAN_BASIC:
            engine.execute_basic(state,rng)
            return True
        return originals["execute_player_technique"](state,rng,c)

    engine.build_monster=build_monster
    engine.compile_build=compile_build
    engine.choose_player_action=choose_player_action
    engine.execute_player_technique=execute_player_technique
    try:
        yield lab_profile
    finally:
        for name,fn in originals.items():
            setattr(engine,name,fn)


def fight_candidate_once(
    *,
    candidate: T0LabCandidate,
    canonical_profile: dict,
    trial_number: int,
    root: str,
    item_ids,
    paths,
    seed: int,
    policy_config: VeteranPolicyConfig=DEFAULT_VETERAN_CONFIG,
    technique_catalog: dict|None=None,
    equipment_catalog: dict|None=None,
    max_rounds: int=100,
) -> dict[str,Any]:
    candidate.validate_against_pending_profile(canonical_profile)
    validate_tier("T0")
    cid=candidate_id(candidate,trial_number)

    with _stage1_runtime(candidate,canonical_profile,policy_config) as lab_profile:
        row=fight_once_observed(
            stage="LianQi_I",
            root=root,
            item_ids=item_ids,
            paths=paths,
            monster_profile=lab_profile,
            tier="T0",
            policy="VETERAN",
            seed=seed,
            technique_catalog=technique_catalog,
            equipment_catalog=equipment_catalog,
            max_rounds=max_rounds,
        )

    return {
        **row,
        "candidate_id":cid,
        "candidate_status":LAB_CANDIDATE_STATUS,
        "canonical_profile_status":canonical_profile["stats_status"],
        "runtime_qi_policy":RUNTIME_QI_SENTINEL,
        "veteran_policy":policy_config.__dict__,
    }
