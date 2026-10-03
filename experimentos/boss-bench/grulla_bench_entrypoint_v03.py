#!/usr/bin/env python3
"""
GRULLA BENCH ENTRYPOINT V0.3

Modo primario actual:
  ULTIS_EQUIPMENT

Controles:
  ULTIS_ONLY

Futuro:
  FULL_LOADOUT (bloqueado hasta cierre humano de técnicas)
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from equipment_bench_adapter_v01 import (
    ALL_PROFILES,
    PRIMARY_PROFILES,
    load_catalog,
    resolve_equipment_loadout,
    validate_liv_profiles,
)

HERE = Path(__file__).resolve().parent
BALANCE_DIR = HERE.parent / "balance_nuevo"
EQUIPMENT_CATALOG = BALANCE_DIR / "equipment_arc1_catalog.json"
STAGES = HERE / "GRULLA_BENCH_EXECUTION_STAGES_V0_3.json"
FULL_GATE = HERE / "FULL_LOADOUT_RELEASE_GATE_V0_2.json"
EQUIPMENT_AUTHORITY = HERE / "EQUIPMENT_BENCH_AUTHORITY_OVERLAY_2026-10-02.json"

MODES = ("ULTIS_ONLY", "ULTIS_EQUIPMENT", "FULL_LOADOUT")


class BenchGateError(RuntimeError):
    pass


def _read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_equipment_authority() -> dict:
    authority = _read(EQUIPMENT_AUTHORITY)
    if authority.get("human_decision", {}).get("equipment_approved") is not True:
        raise BenchGateError("EQUIPMENT_NOT_HUMAN_APPROVED")

    catalog = load_catalog(EQUIPMENT_CATALOG)
    profiles = validate_liv_profiles(catalog)
    if not profiles["pass"]:
        raise BenchGateError("EQUIPMENT_PROFILE_VALIDATION_FAILED: " + ", ".join(profiles["failures"]))

    return {
        "authority": authority,
        "profile_validation": profiles,
        "catalog_status_label": catalog.get("status"),
    }


def validate_mode(mode: str, equipment_profile: str | None = None) -> dict:
    if mode not in MODES:
        raise BenchGateError(f"UNKNOWN_MODE:{mode}")

    stages = _read(STAGES)
    stage = stages["modes"][mode]
    if stage.get("enabled") is not True:
        raise BenchGateError(f"MODE_DISABLED:{mode}")

    if mode == "ULTIS_ONLY":
        return {
            "pass": True,
            "mode": mode,
            "equipment_profile": "NAKED",
            "techniques_enabled": False,
            "consumables_enabled": False,
        }

    equipment = validate_equipment_authority()

    if mode == "ULTIS_EQUIPMENT":
        profile = equipment_profile or "EXPECTED_STAGE"
        if profile not in PRIMARY_PROFILES:
            raise BenchGateError(
                f"PRIMARY_EQUIPMENT_PROFILE_REQUIRED:{profile}; allowed={','.join(PRIMARY_PROFILES)}"
            )
        catalog = load_catalog(EQUIPMENT_CATALOG)
        loadout = resolve_equipment_loadout(catalog, profile)
        return {
            "pass": True,
            "mode": mode,
            "equipment_profile": profile,
            "equipment_items": list(loadout.item_ids),
            "equipment_stats": loadout.stats,
            "equipment_effects": list(loadout.effects),
            "techniques_enabled": False,
            "consumables_enabled": False,
            "catalog_status_label": equipment["catalog_status_label"],
            "human_equipment_approval": True,
        }

    gate = _read(FULL_GATE)
    if gate.get("release_modes", {}).get("FULL_LOADOUT") is not True:
        raise BenchGateError("FULL_LOADOUT_BLOCKED_TECHNIQUES_NOT_APPROVED")
    if gate.get("human_approvals", {}).get("techniques_approved") is not True:
        raise BenchGateError("FULL_LOADOUT_BLOCKED_TECHNIQUES_NOT_APPROVED")

    raise BenchGateError("FULL_LOADOUT_RUNTIME_ADAPTER_NOT_READY")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=MODES, default="ULTIS_EQUIPMENT")
    parser.add_argument(
        "--equipment-profile",
        choices=ALL_PROFILES,
        default="EXPECTED_STAGE",
    )
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()

    try:
        result = validate_mode(args.mode, args.equipment_profile)
    except BenchGateError as exc:
        print(json.dumps({
            "pass": False,
            "mode": args.mode,
            "error": str(exc),
        }, ensure_ascii=False, indent=2))
        return 2

    print(json.dumps(result, ensure_ascii=False, indent=2))
    if args.check_only:
        return 0

    raise RuntimeError(
        "COMBAT_EXECUTION_NOT_WIRED_YET: falta conectar GrullaAdapter + UltimateAdapter "
        "al loop pareado; la autoridad de equipo ya está lista."
    )


if __name__ == "__main__":
    raise SystemExit(main())
