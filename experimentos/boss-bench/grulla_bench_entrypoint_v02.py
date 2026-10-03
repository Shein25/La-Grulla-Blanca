#!/usr/bin/env python3
"""
GRULLA BENCH ENTRYPOINT V0.2

Selector estable entre:
- ULTIS_ONLY
- FULL_LOADOUT

Este entrypoint valida autoridad y gates. La ejecución de combate real se
conectará al runner/adapters ya preparados; nunca cae a fixtures inventados.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from player_loadout_adapter_contract_v01 import (
    BenchMode,
    LoadoutAuthorityError,
    require_mode_ready,
)

HERE = Path(__file__).resolve().parent
RELEASE_GATE = HERE / "FULL_LOADOUT_RELEASE_GATE_V0_1.json"
TECHNIQUE_CATALOG = HERE.parent / "balance_nuevo" / "techniques_arc1_catalog.json"
EQUIPMENT_CATALOG = HERE.parent / "balance_nuevo" / "equipment_arc1_catalog.json"
STAGES = HERE / "GRULLA_BENCH_EXECUTION_STAGES_V0_2.json"


def stage_manifest(mode: BenchMode) -> dict:
    stages = json.loads(STAGES.read_text(encoding="utf-8"))
    return stages["modes"][mode.value]


def validate_stage(mode: BenchMode) -> dict:
    if mode is BenchMode.ULTIS_ONLY:
        readiness = require_mode_ready(mode)
    else:
        readiness = require_mode_ready(
            mode,
            release_gate_path=RELEASE_GATE,
            technique_catalog_path=TECHNIQUE_CATALOG,
            equipment_catalog_path=EQUIPMENT_CATALOG,
        )

    return {
        "pass": True,
        "mode": mode.value,
        "readiness": readiness,
        "stage": stage_manifest(mode),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=[m.value for m in BenchMode],
        default=BenchMode.ULTIS_ONLY.value,
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Valida gates/autoridades sin lanzar peleas.",
    )
    args = parser.parse_args()
    mode = BenchMode(args.mode)

    try:
        result = validate_stage(mode)
    except LoadoutAuthorityError as exc:
        print(json.dumps({
            "pass": False,
            "mode": mode.value,
            "error": str(exc),
        }, ensure_ascii=False, indent=2))
        return 2

    print(json.dumps(result, ensure_ascii=False, indent=2))

    if args.check_only:
        return 0

    # No se inventa fallback.
    raise RuntimeError(
        "COMBAT_EXECUTION_NOT_WIRED_YET: conecta GrullaAdapter + UltimateAdapter "
        "al runner pareado antes de ejecutar combates."
    )


if __name__ == "__main__":
    raise SystemExit(main())
