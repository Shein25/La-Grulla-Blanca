"""Guards del nuevo laboratorio T0.

Estos guards impiden reintroducir fuentes numéricas anteriores o ampliar el
alcance a T1-T4/Definitivas por accidente.
"""
from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import Iterable

ENGINE_CONTRACT = "NEW_COMBAT_STATS_V0_1"
EXPECTED_PENDING = "PENDING_INTEGRAL_REBALANCE"
ARC1_MONSTER_RESOURCE_MODEL = "NONE"
LIANQI_I_IDS = {
    "rata_qi", "avispa_jade", "serpiente_qi", "mono_pildoras", "lobo_espiritual",
}

FORBIDDEN_IMPORT_MODULES = {
    "config_lianqi1_naked",
    "phase_a_enemy_profiles_lab",
    "sim_core",
    "etapa19c_li_screen",
}

FORBIDDEN_SOURCE_MARKERS = {
    # Bloquea la forma operativa del antiguo objetivo centrado en win rate.
    # La frase "target_win_rate_objective_forbidden" puede aparecer legalmente
    # en manifests/tests como una aserción de seguridad.
    "abs(win_rate",
    "Mordisco Frenético",
    "Reflejo de Madriguera",
}

DEFINITIVE_MARKERS = {"DEFINITIVA", "ULTIMATE"}


class Stage1GuardError(RuntimeError):
    pass


def validate_registry_for_stage1(registry_path: str | Path) -> dict:
    data=json.loads(Path(registry_path).read_text(encoding="utf-8"))
    if data.get("status")!="NEW_ENGINE_ONLY":
        raise Stage1GuardError("monster registry is not NEW_ENGINE_ONLY")
    if data.get("engine_contract")!=ENGINE_CONTRACT:
        raise Stage1GuardError("wrong monster engine contract")
    profiles=data.get("profiles")
    if not isinstance(profiles,dict) or len(profiles)!=18:
        raise Stage1GuardError("Arc 1 registry must contain exactly 18 profiles")

    rules=data.get("rules",{})
    if rules.get("arc1_monster_resource_model")!=ARC1_MONSTER_RESOURCE_MODEL:
        raise Stage1GuardError("Arc 1 registry must declare resource_model=NONE")
    for monster_id,profile in profiles.items():
        if profile.get("resource_model")!=ARC1_MONSTER_RESOURCE_MODEL:
            raise Stage1GuardError(f"{monster_id}: resource_model must be NONE")
        if profile.get("stats",{}).get("qi_max") is not None:
            raise Stage1GuardError(f"{monster_id}: resource_model=NONE requires qi_max=None")

    native={k:v for k,v in profiles.items() if v.get("native_stage")=="LianQi_I"}
    if set(native)!=LIANQI_I_IDS:
        raise Stage1GuardError(
            f"LianQi I set mismatch: {sorted(native)}"
        )
    for monster_id,profile in native.items():
        if profile.get("id")!=monster_id:
            raise Stage1GuardError(f"{monster_id}: id mismatch")
        if profile.get("engine_contract")!=ENGINE_CONTRACT:
            raise Stage1GuardError(f"{monster_id}: wrong contract")
        if profile.get("stats_status")!=EXPECTED_PENDING:
            raise Stage1GuardError(f"{monster_id}: T0 must remain pending")
        if profile.get("adaptive",{}).get("status")!="BLOCKED_UNTIL_T0_READY":
            raise Stage1GuardError(f"{monster_id}: adaptive layer must remain blocked")
        tech=profile.get("technique")
        if tech is not None:
            if tech.get("params_status")!=EXPECTED_PENDING:
                raise Stage1GuardError(f"{monster_id}: technique must remain pending")
            if tech.get("params") is not None:
                raise Stage1GuardError(f"{monster_id}: pending technique has params")
    return data


def _imports(path: Path) -> set[str]:
    tree=ast.parse(path.read_text(encoding="utf-8"),filename=str(path))
    out=set()
    for node in ast.walk(tree):
        if isinstance(node,ast.Import):
            out.update(alias.name.split(".")[-1] for alias in node.names)
        elif isinstance(node,ast.ImportFrom) and node.module:
            out.add(node.module.split(".")[-1])
    return out


def validate_package_sources(package_dir: str | Path) -> None:
    root=Path(package_dir)
    for path in sorted(root.glob("*.py")):
        imported=_imports(path)
        bad=sorted(imported & FORBIDDEN_IMPORT_MODULES)
        if bad:
            raise Stage1GuardError(
                f"{path.name}: forbidden numeric source import(s): {bad}"
            )
        text=path.read_text(encoding="utf-8")
        for marker in FORBIDDEN_SOURCE_MARKERS:
            # guards.py documenta los propios markers; no se auto-invalida.
            if path.name!="guards.py" and marker.lower() in text.lower():
                raise Stage1GuardError(
                    f"{path.name}: forbidden source marker: {marker}"
                )


def validate_action_space(action_ids: Iterable[str]) -> None:
    for action_id in action_ids:
        upper=str(action_id).upper()
        if any(marker in upper for marker in DEFINITIVE_MARKERS):
            raise Stage1GuardError(
                f"Definitives are forbidden in monster balance: {action_id}"
            )


def validate_tier(tier: str) -> None:
    if tier!="T0":
        raise Stage1GuardError("STAGE1_INTEGRAL_T0_OPTUNA accepts T0 only")
