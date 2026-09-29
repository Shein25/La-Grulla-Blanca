"""Motor mínimo reproducible para balance del NUEVO contrato de combate.

No contiene cifras de ver74. Los valores viven en configs de laboratorio/canon.
Diseñado para ejecutarse localmente o en Google Colab.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Iterable, Optional, Sequence
import math
import random
import re
import statistics


def clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def round_half_up(x: float) -> int:
    return int(math.floor(x + 0.5))


@dataclass(frozen=True)
class Dice:
    notation: str

    def roll(self, rng: random.Random) -> float:
        total = 0
        expr = self.notation.replace(" ", "")
        # admite NdM, constantes y signos +/-
        for token in re.findall(r"[+-]?[^+-]+", expr):
            sign = -1 if token.startswith("-") else 1
            body = token[1:] if token[:1] in "+-" else token
            if "d" in body.lower():
                n_s, sides_s = body.lower().split("d", 1)
                n = int(n_s) if n_s else 1
                sides = int(sides_s)
                total += sign * sum(rng.randint(1, sides) for _ in range(n))
            else:
                total += sign * int(body)
        return float(total)

    def mean(self) -> float:
        total = 0.0
        expr = self.notation.replace(" ", "")
        for token in re.findall(r"[+-]?[^+-]+", expr):
            sign = -1 if token.startswith("-") else 1
            body = token[1:] if token[:1] in "+-" else token
            if "d" in body.lower():
                n_s, sides_s = body.lower().split("d", 1)
                n = int(n_s) if n_s else 1
                sides = int(sides_s)
                total += sign * n * (sides + 1) / 2
            else:
                total += sign * int(body)
        return total


@dataclass
class ActorStats:
    hp_max: float
    qi_max: float
    precision: float = 100.0
    evasion: float = 0.0
    defense: float = 0.0
    percent_penetration: float = 0.0
    flat_penetration: float = 0.0
    crit_chance: float = 5.0
    crit_damage: float = 1.50
    control: float = 0.0
    tenacity: float = 0.0
    damage_done_percent: float = 0.0


@dataclass
class Technique:
    name: str
    qi_cost: float
    damage: Optional[Dice] = None
    precision_mod: float = 0.0
    damage_percent: float = 0.0
    crit_chance_mod: float = 0.0
    crit_damage_mod: float = 0.0
    percent_penetration: float = 0.0
    flat_penetration: float = 0.0
    aoe: bool = False
    aoe_single_target_scalar: float = 0.65


@dataclass
class HitResult:
    hit: bool
    critical: bool
    rolled_damage: float
    damage_before_def: float
    effective_def: float
    damage_after_def_decimal: float
    damage_after_def: int


def hit_probability(attacker: ActorStats, target: ActorStats, technique: Technique) -> float:
    return clamp(attacker.precision + technique.precision_mod - target.evasion, 5.0, 100.0) / 100.0


def effective_def(attacker: ActorStats, target: ActorStats, technique: Technique) -> float:
    pct_pen = clamp(attacker.percent_penetration + technique.percent_penetration, 0.0, 100.0)
    flat_pen = max(0.0, attacker.flat_penetration + technique.flat_penetration)
    after_pct = max(0.0, target.defense * (1.0 - pct_pen / 100.0))
    return max(0.0, after_pct - flat_pen)


def resolve_direct_hit(
    rng: random.Random,
    attacker: ActorStats,
    target: ActorStats,
    technique: Technique,
    target_count: int = 1,
) -> HitResult:
    if technique.damage is None:
        return HitResult(False, False, 0, 0, effective_def(attacker, target, technique), 0, 0)

    if rng.random() >= hit_probability(attacker, target, technique):
        return HitResult(False, False, 0, 0, effective_def(attacker, target, technique), 0)

    rolled = technique.damage.roll(rng)
    normal_pct = attacker.damage_done_percent + technique.damage_percent
    modified = rolled * max(0.0, 1.0 + normal_pct / 100.0)

    crit_chance = clamp(attacker.crit_chance + technique.crit_chance_mod, 0.0, 100.0)
    critical = rng.random() < crit_chance / 100.0
    if critical:
        modified *= max(0.0, attacker.crit_damage + technique.crit_damage_mod)

    if technique.aoe and target_count == 1:
        modified *= technique.aoe_single_target_scalar

    edef = effective_def(attacker, target, technique)
    after_def_decimal = max(0.0, modified - edef)
    # Contrato nuevo §24: un único redondeo al crear el paquete discreto,
    # después de DEF y antes de Absorción/Vida.
    after_def = round_half_up(after_def_decimal)

    return HitResult(
        hit=True,
        critical=critical,
        rolled_damage=rolled,
        damage_before_def=modified,
        effective_def=edef,
        damage_after_def_decimal=after_def_decimal,
        damage_after_def=after_def,
    )


@dataclass
class MonteCarloSummary:
    iterations: int
    hit_rate: float
    crit_rate_per_action: float
    mean_damage_after_def_decimal: float
    mean_damage_after_def: float
    median_damage_after_def: float
    p10_damage_after_def: float
    p90_damage_after_def: float


def _percentile(sorted_values: Sequence[float], q: float) -> float:
    if not sorted_values:
        return 0.0
    pos = (len(sorted_values) - 1) * q
    lo = math.floor(pos)
    hi = math.ceil(pos)
    if lo == hi:
        return float(sorted_values[lo])
    frac = pos - lo
    return float(sorted_values[lo] * (1 - frac) + sorted_values[hi] * frac)


def monte_carlo_hit(
    attacker: ActorStats,
    target: ActorStats,
    technique: Technique,
    iterations: int = 100_000,
    seed: int = 20260929,
    target_count: int = 1,
) -> MonteCarloSummary:
    rng = random.Random(seed)
    damages_decimal: list[float] = []
    damages: list[float] = []
    hits = 0
    crits = 0

    for _ in range(iterations):
        r = resolve_direct_hit(rng, attacker, target, technique, target_count)
        hits += int(r.hit)
        crits += int(r.critical)
        damages_decimal.append(r.damage_after_def_decimal)
        damages.append(float(r.damage_after_def))

    damages.sort()
    return MonteCarloSummary(
        iterations=iterations,
        hit_rate=hits / iterations,
        crit_rate_per_action=crits / iterations,
        mean_damage_after_def_decimal=statistics.fmean(damages_decimal),
        mean_damage_after_def=statistics.fmean(damages),
        median_damage_after_def=statistics.median(damages),
        p10_damage_after_def=_percentile(damages, 0.10),
        p90_damage_after_def=_percentile(damages, 0.90),
    )


def as_dict(summary: MonteCarloSummary) -> dict:
    return {
        "iterations": summary.iterations,
        "hit_rate": summary.hit_rate,
        "crit_rate_per_action": summary.crit_rate_per_action,
        "mean_damage_after_def_decimal": summary.mean_damage_after_def_decimal,
        "mean_damage_after_def": summary.mean_damage_after_def,
        "median_damage_after_def": summary.median_damage_after_def,
        "p10_damage_after_def": summary.p10_damage_after_def,
        "p90_damage_after_def": summary.p90_damage_after_def,
    }
