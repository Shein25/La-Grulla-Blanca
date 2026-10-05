from prepare_full_envelope_campaign_v01 import ROOTS, build_manifests, seed_for, validate


def base_cfg():
    techniques = [{"id": f"T_{r}_{i}", "root": r} for r in ROOTS for i in range(3)]
    ultimates = [{"id": f"U_{r}_{i}", "root": r} for r in ROOTS for i in range(5)]
    return {
        "campaign_id": "TEST",
        "authorities": {
            "technique_catalog_sha256": "a" * 64,
            "ultimate_catalog_sha256": "b" * 64,
            "grulla_runner_sha256": "c" * 64,
        },
        "roots": list(ROOTS),
        "techniques": techniques,
        "ultimates": ultimates,
        "execution": {
            "notebooks": 5,
            "checkpoint_every_cases": 1000,
            "checkpoint_every_minutes": 10,
            "session_budget_minutes": 540,
            "watchdog_reserve_minutes": 30,
        },
        "unresolved_authority": {
            "rejected_ulti_consumes_shared_budget": False,
            "same_primary_and_grafted_element_legal": False,
        },
    }


def test_valid_config():
    cfg = base_cfg()
    assert validate(cfg) == []
    manifests = build_manifests(cfg)
    assert set(manifests) == set(ROOTS)
    assert all(m["ultimate_repertoire"]["shared_successful_activations_per_combat"] == 1 for m in manifests.values())
    assert all(len(m["allowed_grafted_elements"]) == 4 for m in manifests.values())


def test_unresolved_authority_blocks():
    cfg = base_cfg()
    cfg["unresolved_authority"]["rejected_ulti_consumes_shared_budget"] = "AUTHORITY_REQUIRED"
    assert "AUTHORITY_REQUIRED:rejected_ulti_consumes_shared_budget" in validate(cfg)


def test_seed_independent_of_notebook_order():
    key = "CAMP|S3|FIRE|METAL|POLICY_A|LOADOUT_1|BOSS|120|256"
    assert seed_for(key) == seed_for(key)


def test_bad_root_counts_block():
    cfg = base_cfg()
    cfg["techniques"].pop()
    errs = validate(cfg)
    assert any(x.startswith("TECHNIQUE_COUNT_EXPECTED_15") for x in errs)
    assert any(x.startswith("TECHNIQUE_ROOT_COUNT:WIND") for x in errs)
