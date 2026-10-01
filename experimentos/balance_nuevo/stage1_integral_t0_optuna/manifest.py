"""Manifiesto reproducible del laboratorio Stage1."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import platform
from typing import Any

from contexts import BLOCKED_CONTEXTS, PRIMARY_CONTEXTS, STRESS_CONTEXTS
from seeds import MASTER_SEED


def sha256_file(path: str|Path) -> str:
    h=hashlib.sha256()
    with Path(path).open("rb") as fh:
        for chunk in iter(lambda:fh.read(1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()


def build_manifest(
    *,
    repository_head: str,
    branch: str,
    engine_path: str|Path,
    registry_path: str|Path,
    techniques_path: str|Path,
    equipment_path: str|Path,
    optuna_version: str|None=None,
    sampler: dict[str,Any]|None=None,
) -> dict[str,Any]:
    if not repository_head:
        raise ValueError("repository_head is required; never infer it")
    return {
        "experiment":"STAGE1_INTEGRAL_T0_OPTUNA",
        "status":"ARCHITECTURE_READY_NOT_CANON",
        "branch":branch,
        "repository_head":repository_head,
        "engine_contract":"NEW_COMBAT_STATS_V0_1",
        "master_seed":MASTER_SEED,
        "python_version":platform.python_version(),
        "optuna_version":optuna_version,
        "sampler":sampler,
        "n_jobs_optuna":1,
        "files":{
            "combat_engine":{"path":str(engine_path),"sha256":sha256_file(engine_path)},
            "monster_registry":{"path":str(registry_path),"sha256":sha256_file(registry_path)},
            "techniques":{"path":str(techniques_path),"sha256":sha256_file(techniques_path)},
            "equipment":{"path":str(equipment_path),"sha256":sha256_file(equipment_path)},
        },
        "contexts":{
            "primary":[x.__dict__ for x in PRIMARY_CONTEXTS],
            "stress":[x.__dict__ for x in STRESS_CONTEXTS],
            "blocked":[x.__dict__ for x in BLOCKED_CONTEXTS],
        },
        "rules":{
            "canonical_profiles_must_remain_pending_during_search":True,
            "t1_t4_forbidden":True,
            "definitives_forbidden":True,
            "target_win_rate_objective_forbidden":True,
            "old_monster_numeric_profiles_forbidden":True,
            "human_final_selection_required":True,
        },
    }


def write_manifest(path: str|Path,manifest: dict[str,Any]) -> None:
    Path(path).write_text(
        json.dumps(manifest,ensure_ascii=False,indent=2,sort_keys=True)+"\n",
        encoding="utf-8",
    )
