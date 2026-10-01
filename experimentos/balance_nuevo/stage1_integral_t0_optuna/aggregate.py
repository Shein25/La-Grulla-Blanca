"""Agregación reproducible de peleas Stage1."""
from __future__ import annotations

from collections import Counter,defaultdict
import statistics


def percentile(values,q: float) -> float:
    values=sorted(float(x) for x in values)
    if not values:
        return 0.0
    pos=(len(values)-1)*q
    lo=int(pos);hi=min(lo+1,len(values)-1);frac=pos-lo
    return values[lo]*(1-frac)+values[hi]*frac


def aggregate_fights(rows: list[dict]) -> dict:
    if not rows:
        raise ValueError("no fight rows")
    n=len(rows)
    def mean(key):
        return statistics.fmean(float(r[key]) for r in rows)

    rounds=[r["rounds"] for r in rows]
    hp=[r["player_hp_final_pct"] for r in rows]
    hpmin=[r["player_hp_min_pct"] for r in rows]
    qi=[r["player_qi_final"] for r in rows]

    pattempts=sum(float(r["metrics"]["player_attempts"]) for r in rows)
    phits=sum(float(r["metrics"]["player_hits"]) for r in rows)
    mattempts=sum(float(r["metrics"]["monster_attempts"]) for r in rows)
    mhits=sum(float(r["metrics"]["monster_hits"]) for r in rows)
    cattempts=sum(float(r["metrics"]["control_attempts"]) for r in rows)
    csuccess=sum(float(r["metrics"]["control_successes"]) for r in rows)

    monster_dot=sum(float(r["monster_dot_damage"]) for r in rows)
    monster_direct=sum(
        float(r["monster_basic_damage"])+float(r["monster_skill_direct_damage"])
        for r in rows
    )
    monster_total=monster_dot+monster_direct

    death_causes=Counter(r.get("death_cause") or "NONE" for r in rows)
    root_breakdown=defaultdict(lambda:{"fights":0,"wins":0,"hp_final_pct_sum":0.0})
    loadout_breakdown=defaultdict(lambda:{"fights":0,"wins":0,"hp_final_pct_sum":0.0})
    for r in rows:
        rb=root_breakdown[r["root"]];rb["fights"]+=1;rb["wins"]+=int(r["win"]);rb["hp_final_pct_sum"]+=float(r["player_hp_final_pct"])
        lb=loadout_breakdown[r["loadout_profile"]];lb["fights"]+=1;lb["wins"]+=int(r["win"]);lb["hp_final_pct_sum"]+=float(r["player_hp_final_pct"])

    def finish(d):
        return {
            k:{
                **v,
                "win_rate":v["wins"]/v["fights"],
                "hp_final_pct_mean":v["hp_final_pct_sum"]/v["fights"],
            }
            for k,v in d.items()
        }

    return {
        "fights":n,
        "win_rate":sum(bool(r["win"]) for r in rows)/n,
        "loss_rate":sum(bool(r["loss"]) for r in rows)/n,
        "timeout_rate":sum(bool(r["timeout"]) for r in rows)/n,
        "rounds_mean":statistics.fmean(rounds),
        "rounds_p10":percentile(rounds,0.10),
        "rounds_p50":percentile(rounds,0.50),
        "rounds_p90":percentile(rounds,0.90),
        "hp_final_pct_mean":statistics.fmean(hp),
        "hp_final_pct_p10":percentile(hp,0.10),
        "hp_final_pct_p50":percentile(hp,0.50),
        "hp_final_pct_p90":percentile(hp,0.90),
        "hp_min_pct_mean":statistics.fmean(hpmin),
        "qi_final_mean":statistics.fmean(qi),
        "qi_spent_mean":mean("player_qi_spent"),
        "qi_drained_mean":mean("player_qi_drained"),
        "player_hit_rate":phits/pattempts if pattempts else 0.0,
        "monster_hit_rate":mhits/mattempts if mattempts else 0.0,
        "control_success_rate":csuccess/cattempts if cattempts else 0.0,
        "defensive_activation_mean":mean("defensive_activations"),
        "potion_use_rate":sum(int(r["potion_uses"])>0 for r in rows)/n,
        "monster_skill_use_mean":mean("monster_skill_uses"),
        "monster_basic_use_mean":mean("monster_basic_uses"),
        "monster_skipped_action_mean":mean("monster_skipped_actions"),
        "forced_basic_due_to_qi_mean":mean("forced_basic_due_to_qi"),
        "monster_damage_total_mean":monster_total/n,
        "monster_dot_fraction":monster_dot/monster_total if monster_total else 0.0,
        "death_causes":dict(death_causes),
        "root_breakdown":finish(root_breakdown),
        "loadout_breakdown":finish(loadout_breakdown),
    }
