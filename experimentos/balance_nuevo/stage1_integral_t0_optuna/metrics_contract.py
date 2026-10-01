"""Contrato mínimo de observabilidad para STAGE1_INTEGRAL_T0_OPTUNA."""
from __future__ import annotations

FIGHT_REQUIRED_METRICS = (
    "win",
    "loss",
    "timeout",
    "rounds",
    "player_hp_final",
    "player_hp_final_pct",
    "player_hp_min",
    "player_hp_min_pct",
    "player_qi_final",
    "player_qi_spent",
    "player_qi_drained",
    "player_hit_rate",
    "monster_hit_rate",
    "player_basic_damage",
    "player_skill_direct_damage",
    "player_dot_damage",
    "monster_basic_damage",
    "monster_skill_direct_damage",
    "monster_dot_damage",
    "player_crits",
    "monster_crits",
    "control_attempts",
    "control_successes",
    "defensive_activations",
    "defensive_procs",
    "potion_uses",
    "potion_action_cost",
    "monster_skill_uses",
    "monster_basic_uses",
    "monster_skipped_actions",
    "death_side",
    "death_cause",
    "death_round",
    "per_player_technique_usage",
    "per_monster_action_usage",
    "forced_basic_due_to_qi",
)

AGGREGATE_REQUIRED_METRICS = (
    "win_rate",
    "loss_rate",
    "timeout_rate",
    "rounds_mean",
    "rounds_p10",
    "rounds_p50",
    "rounds_p90",
    "hp_final_pct_mean",
    "hp_final_pct_p10",
    "hp_final_pct_p50",
    "hp_final_pct_p90",
    "hp_min_pct_mean",
    "qi_final_mean",
    "qi_spent_mean",
    "qi_drained_mean",
    "player_hit_rate",
    "monster_hit_rate",
    "control_success_rate",
    "defensive_activation_mean",
    "potion_use_rate",
    "monster_skill_use_mean",
    "monster_basic_use_mean",
    "monster_skipped_action_mean",
    "death_causes",
    "root_breakdown",
    "loadout_breakdown",
)


class MetricsContractError(ValueError):
    pass


def require_metric_keys(row: dict, required=FIGHT_REQUIRED_METRICS) -> None:
    missing=[key for key in required if key not in row]
    if missing:
        raise MetricsContractError("missing metrics: " + ", ".join(missing))


def require_aggregate_keys(row: dict) -> None:
    require_metric_keys(row, AGGREGATE_REQUIRED_METRICS)
