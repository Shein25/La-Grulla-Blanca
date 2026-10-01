"""Reportes descriptivos de Stage1. No selecciona CANON."""
from __future__ import annotations

from collections import Counter
from typing import Any


def _trial_row(t) -> dict[str,Any]:
    return {
        "number":t.number,
        "state":t.state.name,
        "values":t.values,
        "params":t.params,
        "candidate_id":t.user_attrs.get("candidate_id"),
        "candidate_hash":t.user_attrs.get("candidate_hash"),
        "aggregate_summary":t.user_attrs.get("aggregate_summary"),
    }


def build_report(study) -> dict[str,Any]:
    trials=list(study.trials)
    states=Counter(t.state.name for t in trials)
    complete=[t for t in trials if t.state.name=="COMPLETE"]
    pareto=list(study.best_trials)

    objective_ranges=[]
    if complete and complete[0].values is not None:
        for idx in range(len(complete[0].values)):
            vals=[float(t.values[idx]) for t in complete]
            objective_ranges.append({
                "index":idx,
                "min":min(vals),
                "max":max(vals),
            })

    coverage={}
    all_keys=sorted({k for t in complete for k in t.params})
    for key in all_keys:
        vals=[t.params[key] for t in complete if key in t.params]
        if vals and all(
            isinstance(x,(int,float)) and not isinstance(x,bool)
            for x in vals
        ):
            coverage[key]={
                "type":"numeric",
                "min":min(vals),
                "max":max(vals),
                "unique":len(set(vals)),
            }
        else:
            coverage[key]={
                "type":"categorical",
                "unique_values":sorted(set(str(x) for x in vals)),
            }

    wins=[
        float(t.user_attrs["win_rate_observed"])
        for t in complete if "win_rate_observed" in t.user_attrs
    ]

    return {
        "study_name":study.study_name,
        "states":dict(states),
        "complete_trials":len(complete),
        "pareto_trials":len(pareto),
        "objective_ranges":objective_ranges,
        "observed_win_rate_range":{
            "min":min(wins) if wins else None,
            "max":max(wins) if wins else None,
        },
        "parameter_coverage":coverage,
        "pareto":[_trial_row(t) for t in sorted(pareto,key=lambda x:x.number)],
        "selection_performed":False,
        "canonical_promotion_performed":False,
    }
