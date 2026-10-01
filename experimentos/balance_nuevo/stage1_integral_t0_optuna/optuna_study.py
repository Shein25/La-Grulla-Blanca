"""Optuna real para Stage1 T0.

Usa SQLite persistente, sampler explícito con seed y study.optimize(...,n_jobs=1).
"""
from __future__ import annotations

from pathlib import Path
from typing import Callable

import optuna

from candidate import candidate_id
from objective_contract import objective_directions
from objective_eval import objective_values
from proposal import suggest_candidate


class DegenerateCandidate(RuntimeError):
    pass


def create_species_study(
    species_id: str,
    *,
    storage_path: str|Path,
    sampler_seed: int,
    study_name: str|None=None,
):
    path=Path(storage_path).resolve()
    path.parent.mkdir(parents=True,exist_ok=True)
    sampler=optuna.samplers.NSGAIISampler(seed=int(sampler_seed))
    return optuna.create_study(
        study_name=study_name or f"STAGE1_INTEGRAL_T0_OPTUNA::{species_id}::v0.1",
        storage=f"sqlite:///{path.as_posix()}",
        directions=list(objective_directions(species_id)),
        sampler=sampler,
        load_if_exists=True,
    )


def run_species_study(
    species_id: str,
    *,
    study,
    evaluator: Callable,
    n_trials: int,
):
    def objective(trial):
        candidate=suggest_candidate(trial,species_id)
        cid=candidate_id(candidate,trial.number)
        trial.set_user_attr("candidate_id",cid)
        try:
            aggregate=evaluator(candidate,trial.number)
        except DegenerateCandidate as exc:
            trial.set_user_attr("degenerate_reason",str(exc))
            raise optuna.TrialPruned(str(exc))
        trial.set_user_attr("fights",int(aggregate["fights"]))
        trial.set_user_attr("win_rate_observed",float(aggregate["win_rate"]))
        trial.set_user_attr("timeout_rate",float(aggregate["timeout_rate"]))
        trial.set_user_attr("hp_final_pct_mean",float(aggregate["hp_final_pct_mean"]))
        return objective_values(species_id,candidate,aggregate)

    study.optimize(objective,n_trials=int(n_trials),n_jobs=1)
    return study
