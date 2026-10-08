# LianQi II — Stage-Real Preflight V01 — Audit review

Fecha: 2026-10-07
Rama: `experiment/monster-adaptive-six-revalidation-v0.1`
Estado: **PASS_PREFLIGHT_ONLY** / NO LII FREEZE / NO MONSTER RECALIBRATION

## Evidence / integrity
- Review ZIP: `LII_STAGE_REAL_PREFLIGHT_V01_REVIEW.zip`
- Review ZIP SHA-256: `e0faf92a34fbc12a5b2631238841f70d8662be407e451ff754dc9487f4084a65`
- Source commit: `f710dacff7b061a4da9ff0cd399ce6b7efa91ac4`
- Runner SHA-256: `df581ccc28e06cb4985e68619fdbab5d3060293e499e453d330e8ca1c80771ba`
- Valid ZIP; no corrupt member.
- 7/7 manifest listed artifacts byte sizes and SHA-256 match.
- 8 files in archive including PACKAGE_MANIFEST.
- 960 unique scenario rows, 160 compiled technique rows, 960 versus-base rows.
- R24, WORKERS=2, 23,040 represented fights.
- No missing values in SMOKE_CONTEXTS, no duplicate scenario keys, no nonfinite values.
- 80 unique monoroot builds = 5 roots × 16 configurations.
- 0 AOE uses; 0 timeout-rate in all 960 contexts.
- DEFENSE_OPEN activates a defensive technique in all 480 relevant contexts, precisely once per fight on average.
- Checks match expected inertness: DEF_T1 specialization under UNITARGET_FIRST produces identical outputs to BASE_0 (90 context comparisons).

## Preliminary result — T0 smoke only
Across all contexts (equally-weighted, overlapping builds):
- UNITARGET_FIRST win: 89.55%; mean final HP: 37.51%; mean rounds 8.13.
- DEFENSE_OPEN win: 93.02%; mean final HP: 42.87%; mean rounds 9.29.
- Difference: +3.47 pp win, +5.36 pp final HP, +1.16 rounds, +3.38 Qi spent.
- These are smoke-cohort means, not a canonical effect size for LII T1/T2.
- Root delta DEFENSE_OPEN minus offensive-only:
  - Agua: +6.60 pp
  - Fuego: -0.95 pp
  - Metal: +8.03 pp
  - Tierra: +3.82 pp
  - Viento: -0.13 pp
- No conclusion of broken Fire/Wind defenses from R24 or a first-turn-only policy.

### Native T0 monsters
- Sapo de Ceniza: MANDATORY_ENTRY 87.6%; EXPECTED 97.6%; HIGH_ROLL 99.2%.
- Escarabajo de Hierro: MANDATORY_ENTRY 68.3%; EXPECTED 98.8%; HIGH_ROLL 96.2%.
- Extremely high win-rates with advanced gear suggest ceiling effects in a T0-only smoke; do **not** nerf gear/techniques or inflate monster stats.
- Escarabajo HIGH_ROLL lower than EXPECTED in raw cohorts does not prove causal regression (seeds vary with gear_id; equipment profiles differ).
- Fase B should prioritize full T1/T2 + tactical defensive timing + stage realistic acquired gear.

### Compiler checks
- 5 offensive/control BASE + 5 defensive SELF.
- Tramo I 3 branches per technique, 2 points total, no Tramo II/III.
- All 160 compiled rows valid, 5 defensive model families recognized.
- Same-root-only subspace is a starter smoke, not the complete legal multi-element build space.

## Important engineering blocker for next phase
The laboratory engine `etapa19b_combat_engine.py` explicitly rejects tiers other than `T0` in `_require_monster_ready`. It is **not correct** to invoke that baseline engine with `tier='T1'` or `tier='T2'` and present outputs as adapted fights.

The registry declares `sapo_ceniza` and `escarabajo_hierro` stats READY, T0 frozen, and T1/T2 human-ratified (READY_FOR_T3_RECALIBRATION):
- Sapo T1 reactive MITIGATE_NEXT 60% / CD3; natural HP ≤30% OR hit≥20%.
- Escarabajo T1 reactive DEFENSE_UP +4 / CD3; same natural triggers.
- T2: memory 2, repeat2, EFECTIVA-only, anticipation HP≤40% or hit≥15%, natural T1 priority, preserve canonical due. These are registry summaries, not a substitute for executing the full frozen contract.

The next runner must load verified T1/T2 implementation or construct a **lab-only canonical adapter** with event-level parity tests, without importing LI-specific survival magnitudes or changing native monster records. Gate this adapter **before** mass simulation.

## Decision
- PASS_PREFLIGHT_ONLY.
- No LI reopen, no LII numeric changes, no T1/T2 balance conclusions yet.
- Next: `LII_T1_T2_ADAPTIVE_BRIDGE_CONTRACT_GATE_V01`, then LII defensive causal benchmarks.
- No main / merge / runtime integration; Astra handoff after lab closures.
