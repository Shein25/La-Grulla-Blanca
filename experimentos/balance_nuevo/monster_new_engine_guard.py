"""Arc 1 monster-stat guard — NEW_COMBAT_STATS_V0_1 only.

There is one source of monster combat stats: monster_arc1_registry.json.
No conversion, fallback or retired combat-stat field is accepted.
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REGISTRY = HERE / "monster_arc1_registry.json"
PENDING = "PENDING_INTEGRAL_REBALANCE"
READY = "READY"

REQUIRED_STATS = (
    "hp", "qi_max", "precision", "evasion", "defense",
    "tenacity", "control", "crit_chance", "crit_damage", "basic_damage",
)
FORBIDDEN_PROFILE_FIELDS = (
    "legacy", "legacy_attack", "legacy_defense",
    "attack", "ataque", "daño", "damage",
)
FORBIDDEN_TECHNIQUE_FIELDS = (
    "cada", "daño", "drenaQi", "veneno", "quemadura",
    "attack", "ataque", "defense", "defensa", "attackBonus",
)


class MonsterStatsNotReady(RuntimeError):
    pass


def _reject_fields(obj: dict, fields: tuple[str, ...], label: str) -> None:
    for key in fields:
        if key in obj:
            raise AssertionError(f"{label}: forbidden retired field {key}")


def validate_profile(profile: dict, *, require_ready: bool = True) -> dict:
    if not isinstance(profile, dict):
        raise TypeError("monster profile must be dict")

    _reject_fields(profile, FORBIDDEN_PROFILE_FIELDS, "monster profile")

    monster_id = profile.get("id", "?")
    if profile.get("engine_contract") != "NEW_COMBAT_STATS_V0_1":
        raise AssertionError(f"{monster_id}: wrong engine contract")

    stats = profile.get("stats")
    if not isinstance(stats, dict):
        raise AssertionError(f"{monster_id}: stats object required")
    if set(stats) != set(REQUIRED_STATS):
        raise AssertionError(
            f"{monster_id}: stats schema must match NEW_COMBAT_STATS_V0_1 exactly"
        )

    technique = profile.get("technique")
    if technique is not None:
        if not isinstance(technique, dict):
            raise AssertionError(f"{monster_id}: technique must be object")
        _reject_fields(technique, FORBIDDEN_TECHNIQUE_FIELDS, "monster technique")
        if not isinstance(technique.get("mechanics"), list):
            raise AssertionError(f"{monster_id}: technique mechanics required")

    if require_ready:
        if profile.get("stats_status") != READY:
            raise MonsterStatsNotReady(f"{monster_id}: T0 stats are not READY")
        unresolved = [key for key in REQUIRED_STATS if stats.get(key) is None]
        if unresolved:
            raise MonsterStatsNotReady(
                f"{monster_id}: unresolved stats: {', '.join(unresolved)}"
            )
        if technique:
            if technique.get("params_status") != READY:
                raise MonsterStatsNotReady(
                    f"{monster_id}: technique params are not READY"
                )
            if not isinstance(technique.get("params"), dict):
                raise MonsterStatsNotReady(
                    f"{monster_id}: technique READY params object required"
                )
    return profile


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
    for monster_id, profile in profiles.items():
        if profile.get("id") != monster_id:
            raise AssertionError(f"{monster_id}: id mismatch")
        validate_profile(profile, require_ready=False)
    return data


def require_ready_profile(monster_id: str, registry: dict | None = None) -> dict:
    data = registry or load_registry()
    try:
        profile = data["profiles"][monster_id]
    except KeyError as exc:
        raise KeyError(f"monster not registered: {monster_id}") from exc
    return validate_profile(profile, require_ready=True)


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
    print("PASS: 18/18 monsters use NEW_COMBAT_STATS_V0_1.")
    print("PASS: retired monster-stat fields are rejected.")
    print("PASS: 18/18 remain blocked until their T0 profile is READY.")


if __name__ == "__main__":
    selfcheck()
