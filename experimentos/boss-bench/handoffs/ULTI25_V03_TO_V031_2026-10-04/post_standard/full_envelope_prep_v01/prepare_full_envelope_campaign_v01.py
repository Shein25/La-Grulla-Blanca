#!/usr/bin/env python3
"""Preflight + deterministic five-way manifest generator for the future full-envelope campaign.

This tool intentionally DOES NOT simulate combat. It refuses to invent missing authority.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOTS = ("FIRE", "METAL", "WATER", "EARTH", "WIND")
SHA64 = set("0123456789abcdef")


def _sha_ok(value: object) -> bool:
    return isinstance(value, str) and len(value) == 64 and set(value) <= SHA64


def validate(cfg: dict) -> list[str]:
    errors: list[str] = []
    if not cfg.get("campaign_id"):
        errors.append("MISSING_CAMPAIGN_ID")

    auth = cfg.get("authorities") or {}
    for key in ("technique_catalog_sha256", "ultimate_catalog_sha256", "grulla_runner_sha256"):
        if not _sha_ok(auth.get(key)):
            errors.append(f"AUTHORITY_REQUIRED:{key}")

    roots = cfg.get("roots")
    if roots != list(ROOTS):
        errors.append("ROOTS_MUST_BE_CANONICAL_FIVE_ORDER")

    techniques = cfg.get("techniques") or []
    if len(techniques) != 15:
        errors.append(f"TECHNIQUE_COUNT_EXPECTED_15_GOT_{len(techniques)}")
    tc = Counter(x.get("root") for x in techniques if isinstance(x, dict))
    for root in ROOTS:
        if tc[root] != 3:
            errors.append(f"TECHNIQUE_ROOT_COUNT:{root}:EXPECTED_3:GOT_{tc[root]}")

    ultimates = cfg.get("ultimates") or []
    if len(ultimates) != 25:
        errors.append(f"ULTIMATE_COUNT_EXPECTED_25_GOT_{len(ultimates)}")
    uc = Counter(x.get("root") for x in ultimates if isinstance(x, dict))
    for root in ROOTS:
        if uc[root] != 5:
            errors.append(f"ULTIMATE_ROOT_COUNT:{root}:EXPECTED_5:GOT_{uc[root]}")

    execution = cfg.get("execution") or {}
    if execution.get("notebooks") != 5:
        errors.append("EXECUTION_REQUIRES_5_NOTEBOOKS")
    for key in ("checkpoint_every_cases", "checkpoint_every_minutes", "session_budget_minutes", "watchdog_reserve_minutes"):
        if not isinstance(execution.get(key), int) or execution[key] <= 0:
            errors.append(f"INVALID_EXECUTION_SETTING:{key}")
    if isinstance(execution.get("session_budget_minutes"), int) and isinstance(execution.get("watchdog_reserve_minutes"), int):
        if execution["watchdog_reserve_minutes"] >= execution["session_budget_minutes"]:
            errors.append("WATCHDOG_RESERVE_MUST_BE_LT_SESSION_BUDGET")

    unresolved = cfg.get("unresolved_authority") or {}
    if unresolved.get("rejected_ulti_consumes_shared_budget") not in (True, False):
        errors.append("AUTHORITY_REQUIRED:rejected_ulti_consumes_shared_budget")
    if unresolved.get("same_primary_and_grafted_element_legal") not in (True, False):
        errors.append("AUTHORITY_REQUIRED:same_primary_and_grafted_element_legal")

    ids = [x.get("id") for x in techniques + ultimates if isinstance(x, dict)]
    if any(not x for x in ids) or len(ids) != len(set(ids)):
        errors.append("MISSING_OR_DUPLICATE_TECHNIQUE_ULTIMATE_IDS")
    return errors


def seed_for(comparison_group_id: str) -> int:
    # Stable across notebooks and independent of candidate/choice alternative.
    return int.from_bytes(hashlib.sha256(comparison_group_id.encode("utf-8")).digest()[:8], "big")


def build_manifests(cfg: dict) -> dict[str, dict]:
    same_ok = cfg["unresolved_authority"]["same_primary_and_grafted_element_legal"]
    manifests: dict[str, dict] = {}
    for primary in ROOTS:
        grafts = [r for r in ROOTS if same_ok or r != primary]
        manifests[primary] = {
            "schema": "FULL_ENVELOPE_NOTEBOOK_MANIFEST_V01",
            "campaign_id": cfg["campaign_id"],
            "primary_element": primary,
            "allowed_grafted_elements": grafts,
            "ultimate_repertoire": {
                "max_equipped": 2,
                "primary_slots": 1,
                "grafted_slots": 1,
                "shared_successful_activations_per_combat": 1,
            },
            "authorities": cfg["authorities"],
            "execution": cfg["execution"],
            "seed_rule": "sha256(comparison_group_id) first 8 bytes big-endian; candidate choice excluded",
            "checkpoint_schema": "campaign/root/shard + committed case ids + replica ranges + progressive depth",
        }
    return manifests


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("campaign_json")
    ap.add_argument("--out-dir", required=True)
    args = ap.parse_args()
    cfg = json.loads(Path(args.campaign_json).read_text(encoding="utf-8"))
    errors = validate(cfg)
    if errors:
        print(json.dumps({"status": "AUTHORITY_REQUIRED_OR_INVALID", "errors": errors}, indent=2))
        return 2

    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    manifests = build_manifests(cfg)
    for root, manifest in manifests.items():
        p = out / f"NOTEBOOK_{root}_MANIFEST_V01.json"
        p.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    index = {
        "schema": "FULL_ENVELOPE_5WAY_INDEX_V01",
        "campaign_id": cfg["campaign_id"],
        "roots": list(ROOTS),
        "files": [f"NOTEBOOK_{r}_MANIFEST_V01.json" for r in ROOTS],
        "status": "READY_FOR_NOTEBOOK_BUILD",
    }
    (out / "FULL_ENVELOPE_5WAY_INDEX_V01.json").write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(index, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
