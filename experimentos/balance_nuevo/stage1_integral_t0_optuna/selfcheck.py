"""Self-check de STAGE1_INTEGRAL_T0_OPTUNA."""
from __future__ import annotations

import json
from pathlib import Path

from candidate import (
    CANDIDATE_FIELDS,
    ENGINE_CONTRACT,
    LAB_CANDIDATE_STATUS,
    LIANQI_I_IDS,
    T0LabCandidate,
    candidate_id,
)
from contexts import expanded_primary_context_ids
from guards import (
    validate_action_space,
    validate_package_sources,
    validate_registry_for_stage1,
    validate_tier,
)
from metrics_contract import FIGHT_REQUIRED_METRICS, AGGREGATE_REQUIRED_METRICS
from objective_contract import objective_directions
from search_space import LIANQI_I_T0_SEARCH_SPACES

HERE=Path(__file__).resolve().parent
REGISTRY=HERE.parent/"monster_arc1_registry.json"


def _rata_candidate() -> T0LabCandidate:
    # Valores internos de self-check: prueban shape/guards, NO son balance.
    return T0LabCandidate.from_mapping({
        "species_id":"rata_qi",
        "candidate_status":LAB_CANDIDATE_STATUS,
        "engine_contract":ENGINE_CONTRACT,
        "stats":{
            "hp":8,
            "qi_max":None,
            "precision":80,
            "evasion":0,
            "defense":0,
            "tenacity":0,
            "control":0,
            "crit_chance":5,
            "crit_damage":1.50,
            "basic_damage":"1d4+1",
        },
        "technique_params":None,
    })


def _require_source(path: Path,needles: tuple[str,...],errors: list[str]) -> None:
    text=path.read_text(encoding="utf-8")
    for needle in needles:
        if needle not in text:
            errors.append(f"SOURCE_GUARD:{path.name}:missing:{needle}")


def run() -> dict:
    errors=[]
    try:
        registry=validate_registry_for_stage1(REGISTRY)
    except Exception as exc:
        return {"status":"FAIL","errors":[f"REGISTRY:{exc}"]}

    profiles=registry["profiles"]
    if tuple(LIANQI_I_T0_SEARCH_SPACES)!=LIANQI_I_IDS:
        errors.append("SEARCH_SPACE_ORDER_OR_IDS")
    if set(LIANQI_I_T0_SEARCH_SPACES)!=set(LIANQI_I_IDS):
        errors.append("SEARCH_SPACE_SET")

    try:
        candidate=_rata_candidate()
        candidate.validate_shape()
        cid=candidate_id(candidate,0)
        if not cid.startswith("rata_qi-t000000-"):
            errors.append("CANDIDATE_ID")
    except Exception as exc:
        errors.append(f"CANDIDATE:{exc}")

    try:
        validate_package_sources(HERE)
        validate_tier("T0")
        validate_action_space([
            "ataque_basico",
            "palma_ardiente",
            "cuerpo_horno",
            "circulo_cien_ascuas",
        ])
    except Exception as exc:
        errors.append(f"GUARDS:{exc}")

    if len(set(CANDIDATE_FIELDS))!=len(CANDIDATE_FIELDS):
        errors.append("CANDIDATE_FIELDS_DUPLICATED")
    if len(FIGHT_REQUIRED_METRICS)<30:
        errors.append("FIGHT_METRICS_TOO_SMALL")
    if len(AGGREGATE_REQUIRED_METRICS)<20:
        errors.append("AGG_METRICS_TOO_SMALL")
    if len(expanded_primary_context_ids())!=10:
        errors.append("PRIMARY_CONTEXT_COUNT")
    if objective_directions("rata_qi")!=("maximize","minimize"):
        errors.append("RATA_OBJECTIVE_DIRECTIONS")

    # Optuna debe estar realmente cableado, no sólo listado como dependencia.
    _require_source(
        HERE/"optuna_study.py",
        (
            "optuna.create_study(",
            "NSGAIISampler(seed=",
            "study.optimize(",
            "n_jobs=1",
        ),
        errors,
    )
    _require_source(
        HERE/"proposal.py",
        ("trial.suggest_int(", "trial.suggest_categorical("),
        errors,
    )

    ready_ids=[
        mid for mid in LIANQI_I_IDS
        if profiles[mid]["stats_status"]=="READY"
    ]
    expected_ready={"rata_qi","avispa_jade","serpiente_qi","lobo_espiritual"}
    if set(ready_ids)!=expected_ready:
        errors.append(f"READY_LIANQI_I_MISMATCH:{sorted(ready_ids)}")
    if profiles["mono_pildoras"]["stats_status"]!="PENDING_INTEGRAL_REBALANCE":
        errors.append("MONO_MUST_REMAIN_PENDING")
    ready=len(ready_ids)

    return {
        "status":"PASS" if not errors else "FAIL",
        "errors":errors,
        "engine_contract":ENGINE_CONTRACT,
        "lianqi_i_profiles":len(LIANQI_I_IDS),
        "lianqi_i_ready":ready,
        "search_spaces":list(LIANQI_I_T0_SEARCH_SPACES),
        "primary_contexts_expanded":len(expanded_primary_context_ids()),
        "fight_metric_contract_size":len(FIGHT_REQUIRED_METRICS),
        "aggregate_metric_contract_size":len(AGGREGATE_REQUIRED_METRICS),
        "rata_objective_directions":objective_directions("rata_qi"),
        "optuna_pipeline_implemented":True,
        "optuna_executed":False,
        "canonical_registry_modified":True,
        "ready_profiles":["rata_qi","avispa_jade","serpiente_qi","lobo_espiritual"],
        "pending_lianqi_i_profile":"mono_pildoras",
    }


if __name__=="__main__":
    out=run()
    print(json.dumps(out,ensure_ascii=False,indent=2))
    if out["errors"]:
        raise SystemExit(1)
