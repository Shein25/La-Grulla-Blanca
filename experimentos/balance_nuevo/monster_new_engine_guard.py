"""Hard guard for Arc 1 monster balance after the 2026-09-30 migration audit.

New balance runners must consume monster_arc1_new_engine_registry_v0_2.json.
They must never silently fall back to monster_arc1_new_contract_lab.json.
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REGISTRY = HERE / "monster_arc1_new_engine_registry_v0_2.json"
DEPRECATED = HERE / "monster_arc1_new_contract_lab.json"

PENDING = "PENDING_INTEGRAL_REBALANCE_NEW_ENGINE"


class MonsterStatsNotMigrated(RuntimeError):
    pass


def load_registry(path: Path = REGISTRY) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("hard_rules", {}).get("legacy_numeric_import") != "FORBIDDEN":
        raise AssertionError("legacy_numeric_import guard missing")
    if data.get("hard_rules", {}).get("legacy_stat_formula_translation") != "FORBIDDEN":
        raise AssertionError("legacy formula translation guard missing")
    if data.get("profile_count") != 18 or len(data.get("profiles", {})) != 18:
        raise AssertionError("Arc 1 registry must contain exactly 18 monsters")
    return data


def require_ready_profile(monster_id: str, registry: dict | None = None) -> dict:
    data = registry or load_registry()
    try:
        profile = data["profiles"][monster_id]
    except KeyError as exc:
        raise KeyError(f"monster not registered in new-engine registry: {monster_id}") from exc

    if profile.get("stats_status") == PENDING:
        raise MonsterStatsNotMigrated(
            f"{monster_id}: T0 stats are still pending new-engine integral rebalance; "
            "legacy fallback is forbidden"
        )

    policy = profile.get("source_policy", {})
    if policy.get("numeric_source") != "NEW_ENGINE_ONLY":
        raise AssertionError(f"{monster_id}: numeric_source must be NEW_ENGINE_ONLY")
    if policy.get("legacy_numeric_values_allowed") is not False:
        raise AssertionError(f"{monster_id}: legacy numeric values must be forbidden")
    if policy.get("legacy_formula_translation_allowed") is not False:
        raise AssertionError(f"{monster_id}: legacy formula translation must be forbidden")

    stats = profile.get("new_engine_stats", {})
    unresolved = [k for k, v in stats.items() if v is None]
    if unresolved:
        raise MonsterStatsNotMigrated(
            f"{monster_id}: unresolved new-engine stats: {', '.join(unresolved)}"
        )
    return profile


def assert_deprecated_source_is_diagnostic_only(path: Path = DEPRECATED) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("status") != "DEPRECATED_LEGACY_CONTAMINATED_DIAGNOSTIC_ONLY":
        raise AssertionError("legacy-contaminated source is not explicitly deprecated")
    if data.get("deprecation", {}).get("hard_guard") != "DO_NOT_USE_FOR_NEW_MONSTER_BALANCE":
        raise AssertionError("deprecated source hard guard missing")


def selfcheck() -> None:
    data = load_registry()
    assert_deprecated_source_is_diagnostic_only()
    assert len(data["profiles"]) == 18
    blocked = 0
    for monster_id in data["profiles"]:
        try:
            require_ready_profile(monster_id, data)
        except MonsterStatsNotMigrated:
            blocked += 1
    if blocked != 18:
        raise AssertionError(f"expected 18 pending profiles to be blocked, got {blocked}")
    print("PASS: 18/18 monster profiles are registered and blocked until new-engine T0 rebalance.")
    print("PASS: legacy-contaminated translation is diagnostic-only.")


if __name__ == "__main__":
    selfcheck()
