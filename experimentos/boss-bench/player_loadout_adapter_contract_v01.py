#!/usr/bin/env python3
"""
PLAYER LOADOUT ADAPTER CONTRACT V0.1

Prepara el segundo estadio del benchmark de la Grulla.
No resuelve stats ni inventa builds. ULTIS_ONLY puede funcionar sin este módulo.
FULL_LOADOUT queda bloqueado hasta aprobación humana explícita.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any
import json


class BenchMode(str, Enum):
    ULTIS_ONLY = "ULTIS_ONLY"
    FULL_LOADOUT = "FULL_LOADOUT"


@dataclass(frozen=True)
class FullLoadoutRelease:
    techniques_approved: bool
    equipment_approved: bool
    player_build_approved: bool
    technique_catalog_non_provisional: bool
    equipment_catalog_non_provisional: bool
    technique_runtime_adapter_pass: bool
    equipment_runtime_adapter_pass: bool
    release: bool


class LoadoutAuthorityError(RuntimeError):
    pass


def _read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def read_release_gate(path: str | Path) -> FullLoadoutRelease:
    raw = _read_json(path)
    h = raw.get("human_approvals", {})
    a = raw.get("authority_checks", {})
    return FullLoadoutRelease(
        techniques_approved=h.get("techniques_approved") is True,
        equipment_approved=h.get("equipment_approved") is True,
        player_build_approved=h.get("player_build_approved") is True,
        technique_catalog_non_provisional=a.get("technique_catalog_non_provisional") is True,
        equipment_catalog_non_provisional=a.get("equipment_catalog_non_provisional") is True,
        technique_runtime_adapter_pass=a.get("technique_runtime_adapter_pass") is True,
        equipment_runtime_adapter_pass=a.get("equipment_runtime_adapter_pass") is True,
        release=raw.get("release") is True,
    )


def validate_catalog_statuses(technique_catalog: dict[str, Any], equipment_catalog: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    t_status = str(technique_catalog.get("status", ""))
    e_status = str(equipment_catalog.get("status", ""))

    if "PROVISIONAL" in t_status.upper() or "NOT_RUNTIME_CANON" in t_status.upper():
        issues.append("TECHNIQUE_CATALOG_PROVISIONAL")
    if "PROVISIONAL" in e_status.upper() or "DEFERRED" in e_status.upper():
        issues.append("EQUIPMENT_CATALOG_PROVISIONAL")
    return issues


def require_mode_ready(
    mode: BenchMode,
    *,
    release_gate_path: str | Path | None = None,
    technique_catalog_path: str | Path | None = None,
    equipment_catalog_path: str | Path | None = None,
) -> dict[str, Any]:
    if mode is BenchMode.ULTIS_ONLY:
        return {
            "ready": True,
            "mode": mode.value,
            "loadout_sources_loaded": False,
            "message": "ULTIS_ONLY no depende de técnicas/equipo en ajuste.",
        }

    if release_gate_path is None or technique_catalog_path is None or equipment_catalog_path is None:
        raise LoadoutAuthorityError("FULL_LOADOUT_REQUIRES_EXPLICIT_AUTHORITY_PATHS")

    gate = read_release_gate(release_gate_path)
    tech = _read_json(technique_catalog_path)
    equip = _read_json(equipment_catalog_path)
    issues = validate_catalog_statuses(tech, equip)

    required_flags = {
        "TECHNIQUES_APPROVED_BY_HUMAN": gate.techniques_approved,
        "EQUIPMENT_APPROVED_BY_HUMAN": gate.equipment_approved,
        "PLAYER_BUILD_APPROVED_BY_HUMAN": gate.player_build_approved,
        "TECHNIQUE_CATALOG_NON_PROVISIONAL": gate.technique_catalog_non_provisional,
        "EQUIPMENT_CATALOG_NON_PROVISIONAL": gate.equipment_catalog_non_provisional,
        "TECHNIQUE_RUNTIME_ADAPTER_PASS": gate.technique_runtime_adapter_pass,
        "EQUIPMENT_RUNTIME_ADAPTER_PASS": gate.equipment_runtime_adapter_pass,
        "FULL_LOADOUT_RELEASE_GATE_TRUE": gate.release,
    }
    missing = [name for name, ok in required_flags.items() if not ok]
    missing.extend(issues)

    if missing:
        raise LoadoutAuthorityError("FULL_LOADOUT_BLOCKED: " + ", ".join(sorted(set(missing))))

    return {
        "ready": True,
        "mode": mode.value,
        "loadout_sources_loaded": True,
        "technique_status": tech.get("status"),
        "equipment_status": equip.get("status"),
    }


def normalize_loadout_fixture(raw: dict[str, Any]) -> dict[str, Any]:
    """
    Sólo normaliza la forma. No calcula stats, no elige equipo y no completa
    campos faltantes con valores inventados.
    """
    required = ("fixture_id", "player_stats", "techniques", "equipment")
    missing = [k for k in required if k not in raw]
    if missing:
        raise LoadoutAuthorityError("LOADOUT_FIXTURE_MISSING: " + ", ".join(missing))

    if not isinstance(raw["techniques"], list):
        raise LoadoutAuthorityError("LOADOUT_TECHNIQUES_MUST_BE_LIST")
    if not isinstance(raw["equipment"], list):
        raise LoadoutAuthorityError("LOADOUT_EQUIPMENT_MUST_BE_LIST")
    if not isinstance(raw["player_stats"], dict):
        raise LoadoutAuthorityError("LOADOUT_PLAYER_STATS_MUST_BE_OBJECT")

    return {
        "fixture_id": raw["fixture_id"],
        "player_stats": dict(raw["player_stats"]),
        "techniques": list(raw["techniques"]),
        "equipment": list(raw["equipment"]),
        "consumables": list(raw.get("consumables", [])),
        "notes": raw.get("notes"),
    }


if __name__ == "__main__":
    print(json.dumps(
        require_mode_ready(BenchMode.ULTIS_ONLY),
        ensure_ascii=False,
        indent=2,
    ))
