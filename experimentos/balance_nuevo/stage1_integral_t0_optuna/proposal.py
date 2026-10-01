"""Traducción explícita Trial -> T0LabCandidate."""
from __future__ import annotations

from candidate import (
    ENGINE_CONTRACT,
    LAB_CANDIDATE_STATUS,
    T0LabCandidate,
    candidate_hash,
)
from dice_space import dice_candidates
from search_space import LIANQI_I_T0_SEARCH_SPACES, MeanDamageRange, NumericRange


def _suggest_numeric(trial,name: str,spec: NumericRange):
    low=int(spec.low);high=int(spec.high);step=int(spec.step)
    if (low,high,step)!=(spec.low,spec.high,spec.step):
        raise ValueError(f"{name}: Stage1 currently requires integral NumericRange")
    return trial.suggest_int(name,low,high,step=step)


def _suggest_damage(trial,name: str,spec: MeanDamageRange) -> str:
    choices=dice_candidates(spec.low,spec.high)
    return trial.suggest_categorical(name,list(choices))


def suggest_candidate(trial,species_id: str) -> T0LabCandidate:
    try:
        space=LIANQI_I_T0_SEARCH_SPACES[species_id]
    except KeyError as exc:
        raise KeyError(f"unknown Stage1 species: {species_id}") from exc

    def n(key):
        spec=space.free[key]
        if not isinstance(spec,NumericRange):
            raise TypeError(f"{key}: NumericRange expected")
        return _suggest_numeric(trial,key,spec)

    def d(key,param_name):
        spec=space.free[key]
        if not isinstance(spec,MeanDamageRange):
            raise TypeError(f"{key}: MeanDamageRange expected")
        return _suggest_damage(trial,param_name,spec)

    stats={
        "hp":n("hp"),
        "qi_max":None,
        "precision":n("precision"),
        "evasion":n("evasion"),
        "defense":n("defense"),
        "tenacity":n("tenacity"),
        "control":0,
        "crit_chance":5,
        "crit_damage":1.50,
        "basic_damage":d("basic_damage_mean","basic_damage"),
    }

    technique_params=None
    if species_id in {"avispa_jade","serpiente_qi"}:
        technique_params={
            "cadence":n("technique_cadence"),
            "poison":{
                "damage":d("poison_damage_per_tick_mean","poison_damage"),
                "ticks":n("poison_ticks"),
            },
        }
    elif species_id=="mono_pildoras":
        technique_params={
            "cadence":n("technique_cadence"),
            "direct_damage":d("technique_direct_damage_mean","technique_direct_damage"),
            "qi_drain":n("qi_drain"),
        }
    elif species_id=="lobo_espiritual":
        technique_params={
            "cadence":n("technique_cadence"),
            "direct_damage":d("technique_direct_damage_mean","technique_direct_damage"),
        }

    candidate=T0LabCandidate.from_mapping({
        "species_id":species_id,
        "candidate_status":LAB_CANDIDATE_STATUS,
        "engine_contract":ENGINE_CONTRACT,
        "stats":stats,
        "technique_params":technique_params,
    })
    trial.set_user_attr("candidate_hash",candidate_hash(candidate))
    trial.set_user_attr("candidate_status",LAB_CANDIDATE_STATUS)
    return candidate
