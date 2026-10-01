# Parallel Arc 1 work package — 2026-10-01

**Branch:** `experiment/parallel-balance-npc-equipment-v0.1`  
**Status:** LAB / CI PASS / NO MERGE / NO MAIN / NO AUTOMATIC CANON PROMOTION

## 1. Mono Ladrón de Píldoras — QI_DRAIN ablation

Ready for heavy execution in Kaggle.

Input candidates: overnight trials:

```text
1211
1179
1068
1331
1274
```

Paired design:

```text
A = original candidate
B = identical candidate with qi_drain = 0
```

Common random numbers isolate the effect of QI_DRAIN.

Output:

`RESULTADOS_MONO_QI_DRAIN_ABLATION.zip`

No candidate selection is performed automatically.

## 2. Directed T0 revalidation — Avispa / Serpiente / Lobo

Ready for heavy execution in Kaggle.

No broad Optuna search is repeated. The five overnight high-precision survivors
for each species are revalidated with common random numbers and high fight
counts.

Output:

`RESULTADOS_T0_DIRIGIDOS_AVISPA_SERPIENTE_LOBO.zip`

No candidate selection is performed automatically.

## 3. Remaining 13 Arc 1 monsters

`monster_extrapolation_matrix.json` maps each remaining monster to existing
LianQi-I empirical anchors by role/mechanic.

The matrix transfers:

- measurement methodology;
- search-space priors;
- relevant telemetry;
- ablation patterns;
- role/mechanic envelopes.

It explicitly does **not** transfer final numeric stats.

Target-stage player progression/equipment must be simulated directly.

## 4. Rata T2–T4

`RATA_T2_T4_STRUCTURAL_AUDIT.md` prepares only structure and telemetry.

No T2–T4 combat execution is authorized before sequential T1 closure.

Preserved sequence:

```text
T0 READY
→ T1 Reflejo de Madriguera CLOSED
→ T2
→ T3
→ T4 Mordisco Frenético
```

## 5. NPC equipment v0.3

32/32 A07.9 actors are represented.

This layer separates player-catalog combat gear from NPC-specific wardrobe and
personal equipment.

Assignment modes:

```text
PERSONALIZATION_REQUIRED             6
BESPOKE_NPC_GEAR_REQUIRED            7
AUTO_CATALOG_ROLE_GUIDED            11
WARDROBE_OR_COMBAT_ROLE_REQUIRED     8
TOTAL                               32
```

### PERSONALIZATION_REQUIRED

The six companion/peer actors do not receive cloned combat specializations
because the accepted A07.9 role data does not close individual combat builds.

### BESPOKE_NPC_GEAR_REQUIRED

The seven senior authorities are never auto-dressed from player progression
gear. Their distinctive NPC-owned equipment must be designed separately.

### AUTO_CATALOG_ROLE_GUIDED

Eleven role-grounded field/combat actors may use existing non-unique catalog
item types.

Guards:

- automatic catalog assignment starts at story LianQi II;
- only items of the exact current story stage are considered;
- player `unique=true` items are excluded;
- per-family thematic item pools prevent mechanically valid but narratively
  wrong gear;
- `source_npc` never implies the NPC wears an item;
- slots remain sparse.

### WARDROBE_OR_COMBAT_ROLE_REQUIRED

Civil, administrative and logistical occupations do not imply a combat
loadout. Their ordinary wardrobe is kept separate until explicitly designed.

### Combat stats

NPC equipment currently does **not** modify NPC combat stats.

That integration remains blocked until an NPC combat-stat/equipment adapter is
defined. This prevents a second hidden combat engine.

## 6. CI status

Workflow:

`.github/workflows/parallel-arc1-balance-npc-equipment-check.yml`

Current validated blocks:

- directed T0 smoke: PASS;
- Mono QI_DRAIN ablation smoke: PASS;
- 13-monster extrapolation guard: PASS;
- 32/32 NPC equipment regeneration and gating: PASS;
- Rata T2–T4 structure-only guard: PASS.

## 7. Human decisions still required

Heavy simulation outputs:
- Mono QI_DRAIN ablation;
- Avispa/Serpiente/Lobo directed T0 revalidation;
- Rata T1 Reflejo de Madriguera.

NPC design:
- personal combat/equipment identities for 6 companions;
- bespoke NPC-owned gear for 7 authorities;
- wardrobe/combat distinction for 8 civil/admin/logistics actors;
- later decision on whether/how equipment stats enter NPC combat.

No automatic promotion is authorized by this package.
