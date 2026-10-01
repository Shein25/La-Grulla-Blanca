"""Contrato de candidatos LAB para balance integral T0.

Un T0LabCandidate NO es un perfil canónico READY. Se mantiene separado del
registro y sólo puede promocionarse mediante una operación humana posterior.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import math
from typing import Any, Mapping

ENGINE_CONTRACT = "NEW_COMBAT_STATS_V0_1"
LAB_CANDIDATE_STATUS = "LAB_CANDIDATE"
CANON_PENDING_STATUS = "PENDING_INTEGRAL_REBALANCE"
ARC1_MONSTER_RESOURCE_MODEL = "NONE"

LIANQI_I_IDS = (
    "rata_qi",
    "avispa_jade",
    "serpiente_qi",
    "mono_pildoras",
    "lobo_espiritual",
)

STAT_FIELDS = (
    "hp",
    "qi_max",
    "precision",
    "evasion",
    "defense",
    "tenacity",
    "control",
    "crit_chance",
    "crit_damage",
    "basic_damage",
)

CANDIDATE_FIELDS = (
    "species_id",
    "candidate_status",
    "engine_contract",
    "stats",
    "technique_params",
)

TECHNIQUE_SHAPES = {
    "rata_qi": None,
    "avispa_jade": {"cadence", "poison"},
    "serpiente_qi": {"cadence", "poison"},
    "mono_pildoras": {"cadence", "direct_damage", "qi_drain"},
    "lobo_espiritual": {"cadence", "direct_damage"},
}


class CandidateContractError(ValueError):
    pass


def _exact_keys(mapping: Mapping[str, Any], expected: set[str], label: str) -> None:
    actual = set(mapping)
    if actual != expected:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        raise CandidateContractError(
            f"{label}: exact schema required; missing={missing}; extra={extra}"
        )


def _finite_number(value: Any, label: str, *, minimum: float | None = None) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise CandidateContractError(f"{label}: finite number required")
    x = float(value)
    if not math.isfinite(x):
        raise CandidateContractError(f"{label}: finite number required")
    if minimum is not None and x < minimum:
        raise CandidateContractError(f"{label}: must be >= {minimum}")
    return x


def _dice(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CandidateContractError(f"{label}: explicit dice notation required")
    # El parser completo pertenece al Combat Engine. Aquí sólo impedimos
    # números implícitos y valores vacíos.
    if "d" not in value.lower():
        raise CandidateContractError(f"{label}: dice notation must contain 'd'")
    return value


@dataclass(frozen=True)
class T0LabCandidate:
    species_id: str
    candidate_status: str
    engine_contract: str
    stats: Mapping[str, Any]
    technique_params: Mapping[str, Any] | None

    @classmethod
    def from_mapping(cls, raw: Mapping[str, Any]) -> "T0LabCandidate":
        if not isinstance(raw, Mapping):
            raise CandidateContractError("candidate must be a mapping")
        _exact_keys(raw, set(CANDIDATE_FIELDS), "candidate")
        obj = cls(
            species_id=raw["species_id"],
            candidate_status=raw["candidate_status"],
            engine_contract=raw["engine_contract"],
            stats=dict(raw["stats"]),
            technique_params=(
                None if raw["technique_params"] is None
                else dict(raw["technique_params"])
            ),
        )
        obj.validate_shape()
        return obj

    def validate_shape(self) -> None:
        if self.species_id not in LIANQI_I_IDS:
            raise CandidateContractError(f"unsupported T0 species: {self.species_id}")
        if self.candidate_status != LAB_CANDIDATE_STATUS:
            raise CandidateContractError(
                "LAB candidate must never claim READY/canonical status"
            )
        if self.engine_contract != ENGINE_CONTRACT:
            raise CandidateContractError("wrong engine contract")
        if not isinstance(self.stats, Mapping):
            raise CandidateContractError("stats mapping required")
        _exact_keys(self.stats, set(STAT_FIELDS), f"{self.species_id}.stats")

        _finite_number(self.stats["hp"], "hp", minimum=1)
        # Arco 1: resource_model=NONE; qi_max=None es N/A autoritativo.
        if self.stats["qi_max"] is not None:
            raise CandidateContractError(
                "Arc 1 monsters use resource_model=NONE and require qi_max=None"
            )
        for key in ("precision", "evasion", "defense", "tenacity", "control"):
            _finite_number(self.stats[key], key, minimum=0)
        if float(self.stats["control"]) != 0.0:
            raise CandidateContractError(
                "T0 LianQi I identities in this study do not expose a Control mechanic"
            )
        if float(self.stats["crit_chance"]) != 5.0:
            raise CandidateContractError("crit_chance is fixed at canonical base 5")
        if float(self.stats["crit_damage"]) != 1.50:
            raise CandidateContractError("crit_damage is fixed at canonical base 1.50")
        _dice(self.stats["basic_damage"], "basic_damage")

        expected = TECHNIQUE_SHAPES[self.species_id]
        if expected is None:
            if self.technique_params is not None:
                raise CandidateContractError(
                    f"{self.species_id}: T0 has no technique parameters"
                )
            return

        if not isinstance(self.technique_params, Mapping):
            raise CandidateContractError(
                f"{self.species_id}: technique_params mapping required"
            )
        _exact_keys(
            self.technique_params,
            expected,
            f"{self.species_id}.technique_params",
        )
        cadence = self.technique_params["cadence"]
        if isinstance(cadence, bool) or not isinstance(cadence, int) or cadence < 1:
            raise CandidateContractError("technique cadence must be integer >= 1")

        if self.species_id in {"avispa_jade", "serpiente_qi"}:
            poison = self.technique_params["poison"]
            if not isinstance(poison, Mapping):
                raise CandidateContractError("poison object required")
            _exact_keys(poison, {"damage", "ticks"}, "poison")
            _dice(poison["damage"], "poison.damage")
            ticks = poison["ticks"]
            if isinstance(ticks, bool) or not isinstance(ticks, int) or ticks < 1:
                raise CandidateContractError("poison.ticks must be integer >= 1")

        if self.species_id == "mono_pildoras":
            _dice(self.technique_params["direct_damage"], "direct_damage")
            _finite_number(self.technique_params["qi_drain"], "qi_drain", minimum=0)

        if self.species_id == "lobo_espiritual":
            _dice(self.technique_params["direct_damage"], "direct_damage")

    def validate_against_pending_profile(self, profile: Mapping[str, Any]) -> None:
        self.validate_shape()
        if profile.get("id") != self.species_id:
            raise CandidateContractError("candidate/profile id mismatch")
        if profile.get("engine_contract") != ENGINE_CONTRACT:
            raise CandidateContractError("canonical profile uses wrong engine contract")
        if profile.get("resource_model") != ARC1_MONSTER_RESOURCE_MODEL:
            raise CandidateContractError("Arc 1 monster profile must use resource_model=NONE")
        if profile.get("stats",{}).get("qi_max") is not None:
            raise CandidateContractError("Arc 1 resource_model=NONE requires qi_max=None")
        if profile.get("stats_status") != CANON_PENDING_STATUS:
            raise CandidateContractError(
                "study input must remain PENDING_INTEGRAL_REBALANCE"
            )

        canonical_tech = profile.get("technique")
        if self.technique_params is None:
            if canonical_tech is not None:
                raise CandidateContractError("canonical technique unexpectedly present")
        else:
            if not isinstance(canonical_tech, Mapping):
                raise CandidateContractError("canonical technique required")
            if canonical_tech.get("params_status") != CANON_PENDING_STATUS:
                raise CandidateContractError(
                    "canonical technique must remain PENDING_INTEGRAL_REBALANCE"
                )
            if canonical_tech.get("params") is not None:
                raise CandidateContractError(
                    "canonical pending technique must not carry numeric params"
                )

    def canonical_payload(self) -> dict[str, Any]:
        """Canonical JSON for hashing/reproducibility, never for registry writes."""
        self.validate_shape()
        return {
            "species_id": self.species_id,
            "candidate_status": self.candidate_status,
            "engine_contract": self.engine_contract,
            "stats": {key: self.stats[key] for key in STAT_FIELDS},
            "technique_params": (
                None if self.technique_params is None
                else json.loads(json.dumps(self.technique_params, sort_keys=True))
            ),
        }


def candidate_hash(candidate: T0LabCandidate) -> str:
    raw = json.dumps(
        candidate.canonical_payload(),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def candidate_id(candidate: T0LabCandidate, trial_number: int) -> str:
    if isinstance(trial_number, bool) or not isinstance(trial_number, int) or trial_number < 0:
        raise CandidateContractError("trial_number must be integer >= 0")
    return f"{candidate.species_id}-t{trial_number:06d}-{candidate_hash(candidate)[:12]}"
