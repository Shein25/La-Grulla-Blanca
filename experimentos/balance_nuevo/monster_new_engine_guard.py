"""Arc 1 monster-stat guard — NEW_COMBAT_STATS_V0_1 only.

There is one source of monster combat stats: monster_arc1_registry.json.
Profiles are validated against the exact active schema. Unknown fields fail.
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REGISTRY = HERE / "monster_arc1_registry.json"
READY = "READY"

REGISTRY_FIELDS = {
    "schema_version", "status", "engine_contract", "authority", "rules", "profiles",
}
PROFILE_FIELDS = {
    "id", "name", "native_stage", "native_stage_index", "role", "region",
    "element", "unique", "engine_contract", "resource_model", "stats_status", "stats",
    "technique", "ai", "adaptive",
}
REQUIRED_STATS = {
    "hp", "qi_max", "precision", "evasion", "defense",
    "tenacity", "control", "crit_chance", "crit_damage", "basic_damage",
}
TECHNIQUE_FIELDS = {"name", "mechanics", "params_status", "params"}
AI_FIELDS = {"cognition", "social"}
ADAPTIVE_FIELDS = {"status", "rule"}


class MonsterStatsNotReady(RuntimeError):
    pass


def _require_exact_fields(obj: dict, expected: set[str], label: str) -> None:
    actual = set(obj)
    if actual != expected:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        parts = []
        if missing:
            parts.append("missing=" + ",".join(missing))
        if extra:
            parts.append("extra=" + ",".join(extra))
        raise AssertionError(f"{label}: schema mismatch ({'; '.join(parts)})")


def validate_profile(profile: dict, *, require_ready: bool = True) -> dict:
    if not isinstance(profile, dict):
        raise TypeError("monster profile must be dict")

    _require_exact_fields(profile, PROFILE_FIELDS, "monster profile")
    monster_id = profile["id"]

    if profile["engine_contract"] != "NEW_COMBAT_STATS_V0_1":
        raise AssertionError(f"{monster_id}: wrong engine contract")

    resource_model=profile["resource_model"]
    if resource_model not in {"NONE","QI"}:
        raise AssertionError(f"{monster_id}: unsupported resource_model {resource_model!r}")

    stats = profile["stats"]
    if not isinstance(stats, dict):
        raise AssertionError(f"{monster_id}: stats object required")
    _require_exact_fields(stats, REQUIRED_STATS, f"{monster_id}.stats")

    ai = profile["ai"]
    if not isinstance(ai, dict):
        raise AssertionError(f"{monster_id}: ai object required")
    _require_exact_fields(ai, AI_FIELDS, f"{monster_id}.ai")

    adaptive = profile["adaptive"]
    if not isinstance(adaptive, dict):
        raise AssertionError(f"{monster_id}: adaptive object required")
    _require_exact_fields(adaptive, ADAPTIVE_FIELDS, f"{monster_id}.adaptive")

    technique = profile["technique"]
    if technique is not None:
        if not isinstance(technique, dict):
            raise AssertionError(f"{monster_id}: technique must be object")
        _require_exact_fields(technique, TECHNIQUE_FIELDS, f"{monster_id}.technique")
        if not isinstance(technique["mechanics"], list):
            raise AssertionError(f"{monster_id}: technique mechanics required")

    if require_ready:
        if profile["stats_status"] != READY:
            raise MonsterStatsNotReady(f"{monster_id}: T0 stats are not READY")
        unresolved = [
            key for key in REQUIRED_STATS
            if stats[key] is None and not (key=="qi_max" and resource_model=="NONE")
        ]
        if unresolved:
            raise MonsterStatsNotReady(
                f"{monster_id}: unresolved stats: {', '.join(sorted(unresolved))}"
            )
        if resource_model=="NONE" and stats["qi_max"] is not None:
            raise MonsterStatsNotReady(
                f"{monster_id}: resource_model=NONE requires qi_max=null"
            )
        if resource_model=="QI" and stats["qi_max"] is None:
            raise MonsterStatsNotReady(
                f"{monster_id}: resource_model=QI requires numeric qi_max"
            )
        if technique:
            if technique["params_status"] != READY:
                raise MonsterStatsNotReady(
                    f"{monster_id}: technique params are not READY"
                )
            if not isinstance(technique["params"], dict):
                raise MonsterStatsNotReady(
                    f"{monster_id}: technique READY params object required"
                )
    return profile


def load_registry(path: Path = REGISTRY) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    _require_exact_fields(data, REGISTRY_FIELDS, "monster registry")
    if data["schema_version"] != "arc1-monsters-v1":
        raise AssertionError("unexpected monster registry schema")
    if data["status"] != "NEW_ENGINE_ONLY":
        raise AssertionError("monster registry must be NEW_ENGINE_ONLY")
    if data["engine_contract"] != "NEW_COMBAT_STATS_V0_1":
        raise AssertionError("wrong combat-stat contract")
    profiles = data["profiles"]
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
    if blocked != 13:
        raise AssertionError(f"expected 13 pending profiles after all five LianQi-I T0 closures, got {blocked}")
    ready=[mid for mid,p in data["profiles"].items() if p["stats_status"]==READY]
    expected_ready=["rata_qi","serpiente_qi","lobo_espiritual","pez_lunar","devorador_niebla","avispa_jade","mono_pildoras","sapo_ceniza","escarabajo_hierro","anguila_estelar","halcon_tormenta"]
    if ready!=expected_ready:
        raise AssertionError(f"expected READY profiles {expected_ready}, got {ready}")
    print("PASS: 18/18 monsters use NEW_COMBAT_STATS_V0_1.")
    print("PASS: monster registry/profile schemas are exact.")
    if set(data["rules"]["ready_profiles"]) != set(expected_ready):\n        raise AssertionError("rules.ready_profiles does not match actual READY profiles")\n    print("PASS: 11/18 Arc 1 monsters are T0 READY; 7 unique encounters remain pending.")


if __name__ == "__main__":
    selfcheck()
