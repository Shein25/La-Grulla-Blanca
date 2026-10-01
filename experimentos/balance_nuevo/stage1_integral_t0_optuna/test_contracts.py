"""Tests adversariales del contrato Stage1. Ejecutable sin Optuna."""
from __future__ import annotations

from pathlib import Path
import tempfile

from candidate import (
    CandidateContractError,
    ENGINE_CONTRACT,
    LAB_CANDIDATE_STATUS,
    T0LabCandidate,
)
from guards import Stage1GuardError, validate_action_space, validate_package_sources, validate_tier


def rata_raw():
    return {
        "species_id":"rata_qi",
        "candidate_status":LAB_CANDIDATE_STATUS,
        "engine_contract":ENGINE_CONTRACT,
        "stats":{
            "hp":8,
            "qi_max":None,
            "precision":80,
            "evasion":0,
            "defense":0,
            "tenacity":0,
            "control":0,
            "crit_chance":5,
            "crit_damage":1.50,
            "basic_damage":"1d4+1",
        },
        "technique_params":None,
    }


def must_fail(label,fn,exc_type):
    try:
        fn()
    except exc_type:
        return
    raise AssertionError(f"{label}: expected {exc_type.__name__}")


def run():
    ok=T0LabCandidate.from_mapping(rata_raw())
    assert ok.species_id=="rata_qi"

    bad=rata_raw();bad["candidate_status"]="READY"
    must_fail("candidate READY",lambda:T0LabCandidate.from_mapping(bad),CandidateContractError)

    bad=rata_raw();bad["unexpected"]=1
    must_fail("unknown candidate field",lambda:T0LabCandidate.from_mapping(bad),CandidateContractError)

    bad=rata_raw();bad["stats"]["qi_max"]=1
    must_fail("implicit monster qi",lambda:T0LabCandidate.from_mapping(bad),CandidateContractError)

    bad=rata_raw();bad["technique_params"]={"cadence":3}
    must_fail("rata technique",lambda:T0LabCandidate.from_mapping(bad),CandidateContractError)

    must_fail("T1 forbidden",lambda:validate_tier("T1"),Stage1GuardError)
    must_fail(
        "Definitive forbidden",
        lambda:validate_action_space(["palma_ardiente","DEFINITIVA_FUEGO"]),
        Stage1GuardError,
    )

    with tempfile.TemporaryDirectory() as td:
        p=Path(td)
        (p/"bad.py").write_text("import sim_core\n",encoding="utf-8")
        must_fail(
            "old numeric source import",
            lambda:validate_package_sources(p),
            Stage1GuardError,
        )

    print("PASS: Stage1 contract adversarial tests")


if __name__=="__main__":
    run()
