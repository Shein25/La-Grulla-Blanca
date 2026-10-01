"""Conversión de métricas agregadas a objetivos Optuna para los cinco LianQi I."""
from __future__ import annotations

from dice_space import dice_mean
from search_space import LIANQI_I_T0_SEARCH_SPACES, MeanDamageRange, NumericRange

def _normalized(value: float,low: float,high: float) -> float:
    if high<=low:
        return 0.0
    return max(0.0,min(1.0,(float(value)-float(low))/(float(high)-float(low))))

def _free_value(candidate,key: str):
    if key=="hp": return float(candidate.stats["hp"])
    if key=="defense": return float(candidate.stats["defense"])
    if key=="evasion": return float(candidate.stats["evasion"])
    if key=="tenacity": return float(candidate.stats["tenacity"])
    if key=="precision": return float(candidate.stats["precision"])
    if key=="basic_damage_mean": return dice_mean(candidate.stats["basic_damage"])
    p=candidate.technique_params or {}
    if key=="technique_cadence": return float(p["cadence"])
    if key=="poison_damage_per_tick_mean": return dice_mean(p["poison"]["damage"])
    if key=="poison_ticks": return float(p["poison"]["ticks"])
    if key=="technique_direct_damage_mean": return dice_mean(p["direct_damage"])
    if key=="qi_drain": return float(p["qi_drain"])
    raise KeyError(key)

def normalized_candidate_budget(candidate) -> float:
    space=LIANQI_I_T0_SEARCH_SPACES[candidate.species_id]
    parts=[]
    for key,spec in space.free.items():
        value=_free_value(candidate,key)
        if isinstance(spec,(NumericRange,MeanDamageRange)):
            score=_normalized(value,spec.low,spec.high)
        else:
            raise TypeError(f"unsupported search-space spec for {key}")
        # Menor cadence = técnica más frecuente = mayor presupuesto efectivo.
        if key=="technique_cadence":
            score=1.0-score
        parts.append(score)
    return sum(parts)/len(parts)

def objective_values(species_id: str,candidate,aggregate: dict) -> tuple[float,...]:
    pressure=1.0-float(aggregate["hp_final_pct_mean"])
    budget=normalized_candidate_budget(candidate)
    if species_id=="rata_qi":
        return (pressure,budget)
    if species_id=="avispa_jade":
        return (pressure,float(aggregate["monster_dot_fraction"]),budget)
    if species_id=="serpiente_qi":
        return (
            float(aggregate["monster_dot_damage_mean"]),
            float(aggregate["monster_dot_fraction"]),
            budget,
        )
    if species_id=="mono_pildoras":
        return (
            float(aggregate["qi_drained_mean"]),
            float(aggregate["forced_basic_due_to_qi_mean"]),
            pressure,
            budget,
        )
    if species_id=="lobo_espiritual":
        return (
            pressure,
            float(aggregate["monster_damage_total_p90"]),
            budget,
        )
    raise KeyError(f"unknown Stage1 species: {species_id}")
