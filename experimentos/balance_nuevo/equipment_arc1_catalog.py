"""Validador y adaptador para equipment_arc1_catalog.json.

No toca runtime. Diseñado para importarse desde Colab/Monte Carlo.
"""
from __future__ import annotations

from collections import Counter
from copy import deepcopy
import csv
import json
from pathlib import Path

CATALOG_PATH = Path(__file__).with_name("equipment_arc1_catalog.json")


def load_catalog(path: str | Path = CATALOG_PATH) -> dict:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


CATALOG = load_catalog()
ITEMS = CATALOG["items"]
ITEM_BY_ID = {item["item_id"]: item for item in ITEMS}
STAGE_ORDER = {"LianQi_I": 1, "LianQi_II": 2, "LianQi_III": 3, "LianQi_IV": 4}


def item_power_budget(item: dict) -> float:
    weights = CATALOG["power_budget_weights"]
    effect_weights = CATALOG["effect_budget_weights"]
    value = sum(abs(float(v)) * float(weights[k]) for k, v in item.get("stats", {}).items())
    effect = item.get("effect")
    if effect:
        value += float(effect_weights.get(effect.get("type"), 1.0))
    return round(value, 4)


def aggregate_stats(item_ids: list[str]) -> dict:
    out: Counter[str] = Counter()
    for item_id in item_ids:
        item = ITEM_BY_ID[item_id]
        for stat, amount in item.get("stats", {}).items():
            out[stat] += amount
    return dict(out)


def aggregate_effects(item_ids: list[str]) -> list[dict]:
    return [
        deepcopy(ITEM_BY_ID[item_id]["effect"])
        for item_id in item_ids
        if ITEM_BY_ID[item_id].get("effect")
    ]


def validate_loadout(item_ids: list[str]) -> list[str]:
    errors: list[str] = []
    slots: Counter[str] = Counter()
    unique_seen: set[str] = set()
    capacities = CATALOG["slots"]

    for item_id in item_ids:
        if item_id not in ITEM_BY_ID:
            errors.append(f"UNKNOWN_ITEM:{item_id}")
            continue
        item = ITEM_BY_ID[item_id]
        slots[item["slot"]] += 1
        if item.get("unique"):
            if item_id in unique_seen:
                errors.append(f"DUPLICATE_UNIQUE:{item_id}")
            unique_seen.add(item_id)

    for slot, count in slots.items():
        if count > capacities[slot]:
            errors.append(f"SLOT_OVERFLOW:{slot}:{count}>{capacities[slot]}")
    return errors


def available_by_stage(stage: str) -> list[dict]:
    rank = STAGE_ORDER[stage]
    return [
        deepcopy(item)
        for item in ITEMS
        if STAGE_ORDER[item["min_stage"]] <= rank
    ]


def items_with_tag(tag: str, stage: str | None = None) -> list[dict]:
    pool = ITEMS if stage is None else available_by_stage(stage)
    return [deepcopy(item) for item in pool if tag in item.get("build_tags", [])]


def validate_catalog() -> list[str]:
    errors: list[str] = []
    ids = [item["item_id"] for item in ITEMS]
    if len(ids) != len(set(ids)):
        errors.append("DUPLICATE_ITEM_ID")

    ceilings = CATALOG["stage_power_budget_ceiling"]
    percentage_keys = {"crit_chance_pp", "crit_damage_pp", "percent_penetration_pp", "technique_direct_damage_percent"}

    for item in ITEMS:
        for stat, amount in item.get("stats", {}).items():
            if stat not in percentage_keys and abs(float(amount) - round(float(amount))) > 1e-9:
                errors.append(f"FRACTIONAL_FLAT_STAT:{item['item_id']}:{stat}:{amount}")
        if not str(item.get("description", "")).strip():
            errors.append(f"MISSING_DESCRIPTION:{item['item_id']}")
        if "pendiente de redacción" in str(item.get("description", "")).lower():
            errors.append(f"PLACEHOLDER_DESCRIPTION:{item['item_id']}")
        actual = item_power_budget(item)
        stored = float(item["power_budget"])
        if abs(actual - stored) > 0.011:
            errors.append(f"BUDGET_MISMATCH:{item['item_id']}:{stored}!={actual}")
        if actual > float(ceilings[item["min_stage"]]):
            errors.append(f"BUDGET_OVER:{item['item_id']}:{actual}>{ceilings[item['min_stage']]}")

        source = item["source_type"]
        if source in {"STONE_PURCHASE", "WORKSHOP_SERVICE_STONES"} and not item.get("price_stones"):
            errors.append(f"MISSING_STONE_PRICE:{item['item_id']}")
        if ("CONTRIBUTION" in source or source == "MISSION_UNLOCK_REDEMPTION") and not item.get("price_contribution"):
            errors.append(f"MISSING_CONTRIB_PRICE:{item['item_id']}")
        if source == "WORKSHOP_SERVICE_DUAL" and not (item.get("price_stones") and item.get("price_contribution")):
            errors.append(f"MISSING_DUAL_PRICE:{item['item_id']}")

    legacy_policy = CATALOG.get("legacy_equipment_policy", {})
    if legacy_policy.get("coexistence_forbidden"):
        legacy_ids = set(legacy_policy.get("replacements", {}).keys())
        collisions = sorted(legacy_ids.intersection(ITEM_BY_ID))
        for item_id in collisions:
            errors.append(f"LEGACY_ID_REUSED:{item_id}")

    treasures = [item for item in ITEMS if item["slot"] == "TESORO_ESPIRITUAL"]
    expected_treasures = int(CATALOG.get("treasure_policy", {}).get("obtainable_arc1", len(treasures)))
    if len(treasures) != expected_treasures:
        errors.append(f"TREASURE_COUNT:{len(treasures)}!={expected_treasures}")

    prologue = CATALOG.get("prologue_issue", {})
    for item_id in prologue.get("guaranteed_items", []):
        if item_id not in ITEM_BY_ID:
            errors.append(f"BAD_PROLOGUE_ITEM:{item_id}")

    for profile, stages in CATALOG["simulation_loadouts"].items():
        for stage, item_ids in stages.items():
            for err in validate_loadout(item_ids):
                errors.append(f"{profile}:{stage}:{err}")
    return errors


def max_stat_by_stage(stage: str, stat: str) -> tuple[float, list[str]]:
    """Máximo teórico optimizando un único stat, útil como stress; no representa build normal."""
    available = available_by_stage(stage)
    capacities = CATALOG["slots"]
    total = 0.0
    chosen: list[str] = []

    for slot, capacity in capacities.items():
        pool = sorted(
            [item for item in available if item["slot"] == slot],
            key=lambda item: float(item.get("stats", {}).get(stat, 0)),
            reverse=True,
        )
        for item in pool[:capacity]:
            value = float(item.get("stats", {}).get(stat, 0))
            if value > 0:
                total += value
                chosen.append(item["item_id"])
    return total, chosen


def profile_summary() -> dict:
    out = {}
    for profile, stages in CATALOG["simulation_loadouts"].items():
        out[profile] = {}
        for stage, item_ids in stages.items():
            out[profile][stage] = {
                "items": item_ids,
                "stats": aggregate_stats(item_ids),
                "effects": aggregate_effects(item_ids),
                "errors": validate_loadout(item_ids),
            }
    return out


def export_csv(path: str = "equipment_arc1_catalog.csv") -> None:
    fields = [
        "item_id", "name", "min_stage", "slot", "grade", "accessibility",
        "power_budget", "source_type", "source_npc", "source_location",
        "source_mission", "price_stones", "price_contribution",
        "required_permission", "materials", "unique", "build_tags",
        "stats", "effect", "description", "availability", "notes",
    ]
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        for item in ITEMS:
            row = dict(item)
            row["materials"] = "|".join(item.get("materials", []))
            row["build_tags"] = "|".join(item.get("build_tags", []))
            row["stats"] = json.dumps(item.get("stats", {}), ensure_ascii=False)
            row["effect"] = json.dumps(item.get("effect"), ensure_ascii=False)
            writer.writerow({field: row.get(field) for field in fields})


if __name__ == "__main__":
    errors = validate_catalog()
    print({
        "total_items": len(ITEMS),
        "stage_counts": dict(Counter(item["min_stage"] for item in ITEMS)),
        "slot_counts": dict(Counter(item["slot"] for item in ITEMS)),
        "validation_errors": errors,
    })
    print(profile_summary())
    if errors:
        raise SystemExit(1)
