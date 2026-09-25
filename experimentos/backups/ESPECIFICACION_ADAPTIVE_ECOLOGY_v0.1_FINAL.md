# LA GRULLA BLANCA
# Adaptive Ecology v0.1 — FINAL
## Population Pressure & Adaptation Resolver
### Especificación contractual congelada para implementación — 2026-09-25

**DISEÑO CONGELADO. APTO PARA IMPLEMENTACIÓN EXPERIMENTAL.**

Baseline Git de referencia:

`5812deb59cd1c133383b9af973486a702a26daf4`

Rama futura propuesta:

`experiment/monster-ecology-adaptation-v0.1`

## Contrato congelado

```text
SPECIES_KILLED
→ pressure
→ decay
→ tier derivado
→ activeAdaptations derivadas
→ effectiveKit determinista
```

### Fuente de verdad persistente

```text
populationId
speciesId
territoryId
pressure
lastUpdate
recentEventIds
```

### Derivado

```text
tier
activeAdaptations
effectiveKit
```

### Config

```text
baseKit
thresholds
adaptationCatalog
pressurePerKill
decayPerTimeUnit
dedupWindowSize
knownAbilityIds
```

### Evento único v0.1

```text
SPECIES_KILLED
```

`occurredAt` es metadata opaca de debug/telemetría y no participa en decay, orden, dedup, locality ni decisiones.

### Orden transaccional

```text
1. validar input estructural
1.b validar now >= lastUpdate
2. validar locality del evento
3. calcular decay hasta now
4. actualizar lastUpdate
5. comprobar deduplicación
6. aplicar pressurePerKill si corresponde
7. clamp 0..100
8. actualizar recentEventIds con poda FIFO
9. derivar tier
10. derivar activeAdaptations
11. derivar effectiveKit
12. devolver
```

### Tiers

Thresholds estrictamente crecientes. Límite inferior inclusivo:

```text
T3 si pressure >= tier3
T2 si pressure >= tier2
T1 si pressure >= tier1
T0 si no
```

### Errores

Resultados de dominio:

```text
OK
DUPLICATE_EVENT
INVALID_POPULATION
```

Errores contractuales:

`ContractError`

Incluye `now < lastUpdate`.

### Dedup

`recentEventIds` es FIFO por orden de aplicación.

Sólo protege reintentos cercanos. No ofrece exactly-once histórico.

Un eventId expulsado de la ventana puede volver a aplicarse; esto es limitación conocida de v0.1.

### Adaptaciones

Acumulativas y reversibles por tier.

Sin observations.
Sin hysteresis.
Sin cooldown de tier.

La ausencia de hysteresis queda diferida hasta que exista un consumidor real de transiciones (telegraph o Monster AI).

### effectiveKit

```text
baseKit + activeAdaptations
```

- sin duplicados;
- unknown ability IDs filtrados y reportados sólo en debug;
- orden canónico por abilityId;
- reorder invariant.

### Prohibiciones

- no stat scaling;
- no HP/damage/defense/resistance modifiers;
- no cognitiveProfile changes;
- no Monster Utility;
- no combat execution;
- no loot;
- no observations;
- no RNG;
- no producción;
- no ver74;
- no merge.

## Revisión conceptual

REV3 externa:

`ADAPTIVE_ECOLOGY_V01_REV3_APTA_PARA_IMPLEMENTAR`

No quedaron bloqueantes contractuales.

## Goldens adicionales finales

Además de A–AG:

```text
AH threshold exact boundary
AI now < lastUpdate → ContractError sin mutación
```

## Estado

```text
DESIGN_STATUS:
FROZEN_FOR_EXPERIMENTAL_IMPLEMENTATION
```
