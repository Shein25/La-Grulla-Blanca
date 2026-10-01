"""Arc 1 monster-stat guard.

There is one source of monster combat stats: monster_arc1_registry.json.
Pending T0 profiles cannot enter balance simulations.
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REGISTRY = HERE / "monster_arc1_registry.json"
PENDING = "PENDING_INTEGRAL_REBALANCE"
READY = "READY"


class MonsterStatsNotReady(RuntimeError):
    pass


def load_registry(path: Path = REGISTRY) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != "arc1-monsters-v1":
        raise AssertionError("unexpected monster registry schema")
    if data.get("status") != "NEW_ENGINE_ONLY":
        raise AssertionError("monster registry must be NEW_ENGINE_ONLY")
    if data.get("engine_contract") != "NEW_COMBAT_STATS_V0_1":
        raise AssertionError("wrong combat-stat contract")
    profiles = data.get("profiles", {})
    if len(profiles) != 18:
        raise AssertionError("Arc 1 registry must contain exactly 18 monsters")
    return data


def require_ready_profile(monster_id: str, registry: dict | None = None) -> dict:
    data = registry or load_registry()
    try:
        profile = data["profiles"][monster_id]
    except KeyError as exc:
        raise KeyError(f"monster not registered: {monster_id}") from exc

    if profile.get("engine_contract") != "NEW_COMBAT_STATS_V0_1":
        raise AssertionError(f"{monster_id}: wrong engine contract")
    if profile.get("stats_status") != READY:
        raise MonsterStatsNotReady(f"{monster_id}: T0 stats are not READY")

    stats = profile.get("stats", {})
    required = (
        "hp", "qi_max", "precision", "evasion", "defense",
        "tenacity", "control", "crit_chance", "crit_damage", "basic_damage"
    )
    unresolved = [key for key in required if stats.get(key) is None]
    if unresolved:
        raise MonsterStatsNotReady(
            f"{monster_id}: unresolved stats: {', '.join(unresolved)}"
        )

    technique = profile.get("technique")
    if technique and technique.get("params_status") != READY:
        raise MonsterStatsNotReady(f"{monster_id}: technique params are not READY")
    return profile


def selfcheck() -> None:
    data = load_registry()
    blocked = 0
    for monster_id in data["profiles"]:
        try:
            require_ready_profile(monster_id, data)
        except MonsterStatsNotReady:
            blocked += 1
    if blocked != 18:
        raise AssertionError(f"expected 18 pending profiles, got {blocked}")
    print("PASS: 18/18 monsters use the new registry.")
    print("PASS: 18/18 remain blocked until their T0 profile is READY.")


if __name__ == "__main__":
    selfcheck()
