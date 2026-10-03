#!/usr/bin/env python3
"""
EQUIPMENT BENCH ADAPTER V0.1

Carga exclusivamente equipo desde equipment_arc1_catalog.json para el bench de
la Grulla. No carga técnicas ni consumibles. No inventa piezas ni stats.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import json

STAGE = "LianQi_IV"
PRIMARY_PROFILES = ("MANDATORY_ENTRY", "EXPECTED_STAGE", "HIGH_ROLL_STRESS")
ALL_PROFILES = ("NAKED",) + PRIMARY_PROFILES


class EquipmentAuthorityError(RuntimeError):
    pass


@dataclass(frozen=True)
class EquipmentLoadout:
    profile: str
    stage: str
    item_ids: tuple[str, ...]
    stats: dict[str, float]
    effects: tuple[dict[str, Any], ...]
    slots: dict[str, tuple[str, ...]]


def load_catalog(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _items_by_id(catalog: dict[str, Any]) -> dict[str, dict[str, Any]]:
    items = catalog.get("items")
    if not isinstance(items, list):
        raise EquipmentAuthorityError("EQUIPMENT_ITEMS_NOT_LIST")
    by_id: dict[str, dict[str, Any]] = {}
    for item in items:
        iid = item.get("item_id")
        if not isinstance(iid, str) or not iid:
            raise EquipmentAuthorityError("EQUIPMENT_ITEM_WITHOUT_ID")
        if iid in by_id:
            raise EquipmentAuthorityError(f"DUPLICATE_EQUIPMENT_ITEM:{iid}")
        by_id[iid] = item
    return by_id


def profile_item_ids(catalog: dict[str, Any], profile: str, stage: str = STAGE) -> tuple[str, ...]:
    if profile == "NAKED":
        return ()
    if profile not in PRIMARY_PROFILES:
        raise EquipmentAuthorityError(f"UNKNOWN_EQUIPMENT_PROFILE:{profile}")
    try:
        ids = catalog["simulation_loadouts"][profile][stage]
    except KeyError as exc:
        raise EquipmentAuthorityError(f"MISSING_LOADOUT:{profile}:{stage}") from exc
    if not isinstance(ids, list) or any(not isinstance(x, str) for x in ids):
        raise EquipmentAuthorityError(f"INVALID_LOADOUT:{profile}:{stage}")
    return tuple(ids)


def resolve_equipment_loadout(
    catalog: dict[str, Any],
    profile: str,
    *,
    stage: str = STAGE,
) -> EquipmentLoadout:
    ids = profile_item_ids(catalog, profile, stage)
    by_id = _items_by_id(catalog)
    slot_limits = catalog.get("slots", {})
    stats: dict[str, float] = {}
    effects: list[dict[str, Any]] = []
    slots: dict[str, list[str]] = {}

    for iid in ids:
        item = by_id.get(iid)
        if item is None:
            raise EquipmentAuthorityError(f"LOADOUT_ITEM_MISSING:{profile}:{iid}")

        slot = item.get("slot")
        if slot not in slot_limits:
            raise EquipmentAuthorityError(f"UNKNOWN_SLOT:{iid}:{slot}")
        slots.setdefault(slot, []).append(iid)

        for key, value in (item.get("stats") or {}).items():
            if not isinstance(value, (int, float)):
                raise EquipmentAuthorityError(f"NON_NUMERIC_STAT:{iid}:{key}")
            stats[key] = stats.get(key, 0.0) + float(value)

        effect = item.get("effect")
        if effect is not None:
            if not isinstance(effect, dict):
                raise EquipmentAuthorityError(f"INVALID_EFFECT:{iid}")
            effects.append({"item_id": iid, **effect})

    for slot, equipped in slots.items():
        limit = slot_limits[slot]
        if len(equipped) > limit:
            raise EquipmentAuthorityError(
                f"SLOT_LIMIT_EXCEEDED:{profile}:{slot}:{len(equipped)}>{limit}"
            )

    return EquipmentLoadout(
        profile=profile,
        stage=stage,
        item_ids=ids,
        stats=stats,
        effects=tuple(effects),
        slots={k: tuple(v) for k, v in slots.items()},
    )


def validate_liv_profiles(catalog: dict[str, Any]) -> dict[str, Any]:
    resolved = {}
    failures = []
    for profile in ALL_PROFILES:
        try:
            loadout = resolve_equipment_loadout(catalog, profile)
            resolved[profile] = {
                "items": list(loadout.item_ids),
                "stats": loadout.stats,
                "effects": list(loadout.effects),
                "slots": {k: list(v) for k, v in loadout.slots.items()},
            }
        except EquipmentAuthorityError as exc:
            failures.append(str(exc))
    return {
        "pass": not failures,
        "stage": STAGE,
        "profiles": resolved,
        "failures": failures,
    }


def apply_equipment_stats(base_stats: dict[str, float], loadout: EquipmentLoadout) -> dict[str, float]:
    out = {k: float(v) for k, v in base_stats.items()}
    for key, value in loadout.stats.items():
        out[key] = out.get(key, 0.0) + float(value)
    return out


def equipment_runtime_effects(loadout: EquipmentLoadout) -> tuple[dict[str, Any], ...]:
    return loadout.effects


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("catalog")
    args = parser.parse_args()
    result = validate_liv_profiles(load_catalog(args.catalog))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["pass"] else 1)
